import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

function run(args) {
  const r = spawnSync('node', [path.resolve('src/oc-webwatch.js'), ...args], {
    encoding: 'utf8'
  });
  return { code: r.status, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
}

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'oc-webwatch-test-'));

// 1) baseline
const r1 = run(['https://example.com', '--dir', tmpDir, '--mode', 'text', '--selector', 'h1', '--out', 'json']);
if (r1.code !== 1) {
  console.error('Expected baseline exit code 1');
  console.error({ r1, tmpDir });
  process.exit(1);
}

// 2) unchanged
const r2 = run(['https://example.com', '--dir', tmpDir, '--mode', 'text', '--selector', 'h1', '--out', 'json']);
if (r2.code !== 0) {
  console.error('Expected unchanged exit code 0');
  console.error({ r2, tmpDir });
  process.exit(1);
}

console.log('SELFTEST_OK');
