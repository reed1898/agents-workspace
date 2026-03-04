#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const http = require("http");
const { execFile } = require("child_process");

const HOST = "127.0.0.1";
const PORT = Number(process.env.PORT || process.argv[2] || 8899);
const PUBLIC_DIR = path.join(__dirname, "public");
const INDEX_PATH = path.join(PUBLIC_DIR, "index.html");

function execFileAsync(file, args, options) {
  return new Promise((resolve) => {
    execFile(file, args, options, (error, stdout, stderr) => {
      resolve({ error, stdout, stderr });
    });
  });
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
      if (data.length > 2 * 1024 * 1024) {
        reject(new Error("Request body too large"));
      }
    });
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch (err) {
        reject(new Error("Invalid JSON body"));
      }
    });
    req.on("error", reject);
  });
}

function writeJson(res, code, payload) {
  const text = JSON.stringify(payload, null, 2);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(text),
  });
  res.end(text);
}

function percentile(sorted, q) {
  if (!sorted.length) return null;
  const idx = Math.min(
    sorted.length - 1,
    Math.max(0, Math.ceil((q / 100) * sorted.length) - 1)
  );
  return sorted[idx];
}

function computeStats(samples) {
  if (!samples.length) {
    return {
      count: 0,
      min: null,
      max: null,
      avg: null,
      std: null,
      p50: null,
      p95: null,
      p99: null,
    };
  }

  const sorted = [...samples].sort((a, b) => a - b);
  const n = sorted.length;
  const sum = sorted.reduce((acc, v) => acc + v, 0);
  const avg = sum / n;
  const variance =
    sorted.reduce((acc, v) => acc + (v - avg) * (v - avg), 0) / n;
  return {
    count: n,
    min: sorted[0],
    max: sorted[n - 1],
    avg,
    std: Math.sqrt(Math.max(0, variance)),
    p50: percentile(sorted, 50),
    p95: percentile(sorted, 95),
    p99: percentile(sorted, 99),
  };
}

function normalizeTargets(input) {
  if (!Array.isArray(input)) return [];
  const out = [];
  for (const raw of input) {
    if (typeof raw !== "string") continue;
    const trimmed = raw.trim();
    if (!trimmed) continue;
    try {
      const u = new URL(trimmed);
      if (u.protocol !== "http:" && u.protocol !== "https:") continue;
      out.push(trimmed);
    } catch {
      // Ignore invalid URL.
    }
  }
  return [...new Set(out)];
}

function joinUrl(base, endpointPath) {
  const b = new URL(base);
  if (!endpointPath) return b.toString();
  const safePath = endpointPath.startsWith("/") ? endpointPath : `/${endpointPath}`;
  b.pathname = safePath;
  b.search = "";
  b.hash = "";
  return b.toString();
}

function buildCurlArgs(opts) {
  const args = [
    "--silent",
    "--show-error",
    "--output",
    "/dev/null",
    "--write-out",
    "%{http_code} %{time_total}",
    "--connect-timeout",
    String(opts.connectTimeoutSec),
    "--max-time",
    String(opts.maxTimeSec),
    "-X",
    opts.method,
  ];

  if (opts.noProxy) {
    args.push("--noproxy", "*");
  }

  if (opts.method !== "GET") {
    args.push("-H", "content-type: application/json");
    args.push("-d", opts.body || "{}");
  }

  args.push(opts.url);
  return args;
}

function buildExecEnv() {
  const env = { ...process.env };
  const keys = [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
  ];
  for (const k of keys) delete env[k];
  return env;
}

async function runSingle(targetUrl, opts) {
  const args = buildCurlArgs({
    url: targetUrl,
    method: opts.method,
    body: opts.body,
    noProxy: true,
    connectTimeoutSec: opts.connectTimeoutSec,
    maxTimeSec: opts.maxTimeSec,
  });
  const env = buildExecEnv();
  const { error, stdout, stderr } = await execFileAsync("curl", args, { env });

  const text = (stdout || "").trim();
  const parts = text.split(/\s+/);
  const httpCode = Number(parts[0]) || 0;
  const timeSec = Number(parts[1]) || 0;
  const okExec = !error;

  return {
    httpCode,
    timeSec,
    okExec,
    error: okExec ? null : (stderr || error.message || "curl failed").trim(),
  };
}

async function runTarget(baseUrl, opts) {
  const targetUrl = joinUrl(baseUrl, opts.path);
  const attempts = [];
  for (let i = 0; i < opts.runs; i += 1) {
    // eslint-disable-next-line no-await-in-loop
    const one = await runSingle(targetUrl, opts);
    attempts.push(one);
  }

  const successful = attempts.filter((x) => x.okExec);
  const failedExec = attempts.filter((x) => !x.okExec).length;
  const non2xx = successful.filter((x) => x.httpCode < 200 || x.httpCode >= 300).length;
  const timings = successful.map((x) => x.timeSec);

  return {
    baseUrl,
    targetUrl,
    runs: opts.runs,
    successExec: successful.length,
    failedExec,
    non2xx,
    stats: computeStats(timings),
    lastError: attempts.find((x) => x.error)?.error || null,
    samples: attempts,
  };
}

function sanitizeNumber(value, fallback, min, max) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.min(max, Math.max(min, n));
}

async function handleRun(req, res) {
  try {
    const body = await parseJsonBody(req);
    const targets = normalizeTargets(body.targets);
    if (!targets.length) {
      writeJson(res, 400, { error: "targets is empty or invalid" });
      return;
    }

    const runs = sanitizeNumber(body.runs, 30, 1, 200);
    const connectTimeoutSec = sanitizeNumber(body.connectTimeoutSec, 5, 1, 30);
    const maxTimeSec = sanitizeNumber(body.maxTimeSec, 20, 2, 120);
    const method = String(body.method || "GET").toUpperCase() === "POST" ? "POST" : "GET";
    const endpointPath = typeof body.path === "string" ? body.path.trim() : "/api/health";
    const requestBody =
      typeof body.requestBody === "string" && body.requestBody.trim()
        ? body.requestBody
        : "{}";

    const startedAt = new Date().toISOString();
    const results = await Promise.all(
      targets.map((baseUrl) =>
        runTarget(baseUrl, {
          path: endpointPath,
          runs,
          connectTimeoutSec,
          maxTimeSec,
          method,
          body: requestBody,
        })
      )
    );
    const finishedAt = new Date().toISOString();

    writeJson(res, 200, {
      startedAt,
      finishedAt,
      config: {
        runs,
        connectTimeoutSec,
        maxTimeSec,
        method,
        path: endpointPath,
        mode: "direct",
      },
      results,
    });
  } catch (err) {
    writeJson(res, 500, { error: err.message || "Unknown server error" });
  }
}

function serveIndex(res) {
  try {
    const html = fs.readFileSync(INDEX_PATH);
    res.writeHead(200, {
      "Content-Type": "text/html; charset=utf-8",
      "Content-Length": html.length,
    });
    res.end(html);
  } catch (err) {
    writeJson(res, 500, { error: "Failed to load index.html", detail: err.message });
  }
}

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/") {
    serveIndex(res);
    return;
  }
  if (req.method === "POST" && req.url === "/api/test") {
    handleRun(req, res);
    return;
  }
  if (req.method === "GET" && req.url === "/health") {
    writeJson(res, 200, { ok: true, ts: new Date().toISOString() });
    return;
  }
  writeJson(res, 404, { error: "Not found" });
});

server.listen(PORT, HOST, () => {
  // eslint-disable-next-line no-console
  console.log(`Speed test web is running at http://${HOST}:${PORT}`);
});
