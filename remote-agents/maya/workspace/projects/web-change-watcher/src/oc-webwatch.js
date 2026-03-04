#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { parse as parseHtml } from 'node-html-parser';

function usage(exitCode = 0) {
  const msg = `
web-change-watcher (MVP)

Usage:
  oc-webwatch <url> [--dir <stateDir>] [--timeoutMs <ms>] [--userAgent <ua>] [--mode <html|text>] [--selector <css>] [--out <text|json>]

Behavior:
  - Fetches URL
  - Stores snapshot + sha256 hash under state dir
  - If changed since last run, prints a unified diff (if 'diff' exists) and exits 2
  - If unchanged, prints 'UNCHANGED' and exits 0
  - First run stores state and exits 1 (baseline)

Exit codes:
  0 unchanged
  1 baseline created (no previous snapshot)
  2 changed
  3 error
`;
  console.log(msg.trim());
  process.exit(exitCode);
}

function parseArgs(argv) {
  const args = {
    url: null,
    dir: '.oc-webwatch',
    timeoutMs: 15000,
    userAgent: 'web-change-watcher/0.1',
    mode: 'html',
    selector: null,
    out: 'text'
  };
  const rest = [];
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') usage(0);
    if (a === '--dir') { args.dir = argv[++i]; continue; }
    if (a === '--timeoutMs') { args.timeoutMs = Number(argv[++i]); continue; }
    if (a === '--userAgent') { args.userAgent = argv[++i]; continue; }
    if (a === '--mode') { args.mode = String(argv[++i] || ''); continue; }
    if (a === '--selector') { args.selector = String(argv[++i] || ''); continue; }
    if (a === '--out') { args.out = String(argv[++i] || ''); continue; }
    rest.push(a);
  }
  if (rest.length !== 1) usage(3);
  args.url = rest[0];
  if (!Number.isFinite(args.timeoutMs) || args.timeoutMs <= 0) throw new Error('invalid --timeoutMs');
  if (!['html', 'text'].includes(args.mode)) throw new Error('invalid --mode (expected html|text)');
  if (args.selector !== null && !args.selector.trim()) throw new Error('invalid --selector');
  if (!['text', 'json'].includes(args.out)) throw new Error('invalid --out (expected text|json)');
  return args;
}

function slugifyUrl(u) {
  return u.replace(/^[a-z]+:\/\//i, '').replace(/[^a-z0-9]+/gi, '_').replace(/^_+|_+$/g, '').slice(0, 120) || 'url';
}

function sha256(text) {
  return crypto.createHash('sha256').update(text).digest('hex');
}

function normalizeHtml(html) {
  // MVP normalization: collapse whitespace, remove trailing spaces per line.
  return html
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(l => l.replace(/\s+$/g, ''))
    .join('\n')
    .replace(/[ \t]+/g, ' ');
}

function decodeBasicEntities(s) {
  // Keep it dependency-free: only decode the entities we commonly see.
  return s
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
}

function htmlToText(html) {
  // WARNING: naive HTML->text, but works well for “did the visible content change?”
  // 1) remove script/style/noscript
  // 2) remove tags
  // 3) decode basic entities
  // 4) normalize whitespace
  const noScripts = html
    .replace(/<script[\s\S]*?<\/script>/gi, '\n')
    .replace(/<style[\s\S]*?<\/style>/gi, '\n')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '\n');

  const tagStripped = noScripts
    .replace(/<br\s*\/?\s*>/gi, '\n')
    .replace(/<\/p\s*>/gi, '\n')
    .replace(/<[^>]+>/g, ' ');

  const decoded = decodeBasicEntities(tagStripped);

  return decoded
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(l => l.trim())
    .filter(Boolean)
    .join('\n')
    .replace(/[ \t]+/g, ' ')
    .trim() + '\n';
}

async function fetchWithTimeout(url, { timeoutMs, userAgent }) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(new Error('timeout')), timeoutMs);
  try {
    const res = await fetch(url, {
      signal: ac.signal,
      headers: {
        'user-agent': userAgent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(t);
  }
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function writeFileAtomic(filePath, content) {
  const tmp = filePath + '.tmp';
  fs.writeFileSync(tmp, content);
  fs.renameSync(tmp, filePath);
}

function runUnifiedDiff(oldFile, newFile) {
  const r = spawnSync('diff', ['-u', oldFile, newFile], { encoding: 'utf8' });
  if (r.error) return { ok: false, output: '' };
  // diff exits 0 (no diff) or 1 (diff) — both are fine.
  return { ok: true, output: (r.stdout || '') + (r.stderr || '') };
}

async function main() {
  try {
    const { url, dir, timeoutMs, userAgent, mode, selector, out } = parseArgs(process.argv);
    ensureDir(dir);

    const key = slugifyUrl(url) + `__${mode}` + (selector ? `__sel_${slugifyUrl(selector)}` : '');
    const snapPath = path.join(dir, `${key}.snapshot.txt`);
    const hashPath = path.join(dir, `${key}.sha256`);

    const raw = await fetchWithTimeout(url, { timeoutMs, userAgent });

    const maybeSelect = (html) => {
      if (!selector) return html;
      const root = parseHtml(html);
      const nodes = root.querySelectorAll(selector);
      if (!nodes?.length) return '';
      if (mode === 'text') {
        return nodes.map(n => n.textContent || '').join('\n') + '\n';
      }
      // mode === 'html'
      return nodes.map(n => n.outerHTML || '').join('\n') + '\n';
    };

    const selected = maybeSelect(raw);
    const snapshot = mode === 'text' ? htmlToText(selected) : normalizeHtml(selected);
    const newHash = sha256(snapshot);

    const emit = (objOrLine) => {
      if (out === 'json') {
        const obj = typeof objOrLine === 'string' ? { message: objOrLine } : objOrLine;
        process.stdout.write(JSON.stringify(obj) + '\n');
        return;
      }
      if (typeof objOrLine === 'string') console.log(objOrLine);
      else console.log(JSON.stringify(objOrLine));
    };

    if (!fs.existsSync(snapPath) || !fs.existsSync(hashPath)) {
      writeFileAtomic(snapPath, snapshot);
      writeFileAtomic(hashPath, newHash + '\n');
      emit({ status: 'BASELINE_CREATED', url, key, mode, hash: newHash });
      process.exit(1);
    }

    const oldHash = fs.readFileSync(hashPath, 'utf8').trim();
    if (oldHash === newHash) {
      emit({ status: 'UNCHANGED', url, key, mode, hash: newHash });
      process.exit(0);
    }

    const oldSnapPath = snapPath + '.prev';
    fs.copyFileSync(snapPath, oldSnapPath);
    writeFileAtomic(snapPath, snapshot);
    writeFileAtomic(hashPath, newHash + '\n');

    emit({ status: 'CHANGED', url, key, mode, oldHash, newHash });

    const d = runUnifiedDiff(oldSnapPath, snapPath);
    if (out === 'json') {
      emit({ diffAvailable: Boolean(d.ok), diff: d.ok ? (d.output || '') : '' });
    } else {
      if (d.ok && d.output.trim()) {
        console.log('--- DIFF_START ---');
        console.log(d.output.trimEnd());
        console.log('--- DIFF_END ---');
      } else {
        console.log('(diff not available or empty)');
      }
    }

    process.exit(2);
  } catch (e) {
    console.error(`ERROR: ${e?.message || e}`);
    process.exit(3);
  }
}

await main();
