import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const output = path.join(root, "ui-prototype/screenshots/vd2/after");
const hash = (file) =>
  crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const report = JSON.parse(
  fs.readFileSync(path.join(output, "capture-record.json")),
);
assert.equal(report.pass, true);
assert(report.checks.length >= 17);
assert.deepEqual(report.errors, []);
for (const [file, digest] of Object.entries(report.inputs))
  assert.equal(hash(path.join(root, file)), digest, `Stale input ${file}`);
for (const capture of report.captures)
  assert.equal(
    hash(path.join(output, capture.file)),
    capture.sha256,
    `Changed capture ${capture.file}`,
  );
for (const width of [1280, 1920]) {
  const manifest = JSON.parse(
    fs.readFileSync(path.join(output, `recording-${width}.json`)),
  );
  assert.equal(manifest.viewport.width, width);
  assert(manifest.frames.length > 40);
  assert(manifest.gif.duration_ms > 7000);
  assert.equal(hash(path.join(output, manifest.gif.file)), manifest.gif.sha256);
}
console.log(
  `PASS VD2 ${report.checks.length} browser checks, ${report.captures.length} PNG captures, 2 live GIF recordings; source and media hashes match. Owner art acceptance remains pending.`,
);
