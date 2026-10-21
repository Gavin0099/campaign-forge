import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const out = path.join(root, "ui-prototype/screenshots/art-gate");
const report = JSON.parse(
  fs.readFileSync(path.join(out, "capture-record.json")),
);
const hash = (b) => crypto.createHash("sha256").update(b).digest("hex");
assert.equal(report.pass, true);
assert.equal(report.art_quality, "PENDING_OWNER_REVIEW");
assert.deepEqual(report.console_errors, []);
for (const [file, digest] of Object.entries(report.inputs))
  assert.equal(
    hash(fs.readFileSync(path.join(root, file))),
    digest,
    `Stale evidence: ${file}`,
  );
for (const required of [
  "a-1280-composition",
  "b-1280-composition",
  "a-1920-composition",
  "b-1920-composition",
  "switch-preserves-state",
  "landmarks-keyboard-and-escape",
  "landmark-labels",
  "large-text-and-narrow",
  "failed-plate-recovery",
  "reduced-motion-static",
  "menu-entry-and-return",
])
  assert(
    report.checks.some((c) => c.name === required && c.pass),
    `Missing check: ${required}`,
  );
for (const name of [
  "a-1280",
  "b-1280",
  "a-1920",
  "b-1920",
  "maggie-1280",
  "large-1280",
  "large-390",
]) {
  const capture = report.captures.find((c) => c.file === `${name}.png`);
  assert(capture);
  const b = fs.readFileSync(path.join(out, capture.file));
  assert.equal(hash(b), capture.sha256);
  assert.equal(b.readUInt32BE(16), capture.width);
  assert.equal(b.readUInt32BE(20), capture.height);
  assert.equal(capture.state_sha256, report.scene_state_sha256);
}
assert.notEqual(
  report.captures.find((c) => c.file === "a-1280.png").sha256,
  report.captures.find((c) => c.file === "b-1280.png").sha256,
);
const provenance = JSON.parse(
  fs
    .readFileSync(
      path.join(root, "ui-prototype/docs/art-gate/asset-provenance.json"),
      "utf8",
    )
    .replace(/^\uFEFF/, ""),
);
for (const asset of provenance.assets) {
  assert.equal(
    hash(fs.readFileSync(path.join(root, asset.file))),
    asset.sha256,
  );
  assert.equal(
    hash(
      fs.readFileSync(
        path.join(root, "ui-prototype/docs/art-gate", asset.prompt),
      ),
    ),
    asset.prompt_sha256,
  );
  for (const [file, digest] of Object.entries(asset.input_hashes))
    assert.equal(hash(fs.readFileSync(path.join(root, file))), digest);
}
console.log(
  `PASS: ${report.checks.length} runtime checks, ${report.captures.length} captures and all source hashes. Art quality remains pending Owner review.`,
);
