import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const output = path.join(
  root,
  "ui-prototype/screenshots/art-gate/legacy-regression",
);
const hash = (file) =>
  crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const report = JSON.parse(
  fs.readFileSync(path.join(output, "capture-record.json")),
);
assert.equal(report.pass, true);
assert.deepEqual(report.errors, []);
assert.equal(report.human_playtest, false);
for (const name of [
  "geometry-layout-1280",
  "geometry-layout-1920",
  "visible-confirmation-1280",
  "visible-confirmation-1920",
  "confirm-impact-1280",
  "confirm-impact-1920",
  "branch-reset-1280",
  "branch-reset-1920",
  "real-path-and-broken-bridge",
  "double-confirm",
  "branch-switch-cancels",
  "cancel-before-impact",
  "cancel-after-impact",
  "reduced-motion",
  "support-contract",
  "rope-contract",
  "keyboard-grid",
  "dialog-focus",
  "large-and-narrow",
  "unmount-cancel",
  "failed-art-fallback",
  "legacy-full-residents",
  "legacy-full-grain",
])
  assert(
    report.checks.some((c) => c.name === name && c.pass),
    `Missing actual check ${name}`,
  );
for (const [file, digest] of Object.entries(report.inputs))
  assert.equal(hash(path.join(root, file)), digest, `Stale source ${file}`);
for (const capture of report.captures)
  assert.equal(
    hash(path.join(output, capture.file)),
    capture.sha256,
    `Changed capture ${capture.file}`,
  );
for (const width of [1280, 1920])
  for (const name of ["open", "preview", "sealed", "legacy-baseline"])
    assert(
      report.captures.some(
        (c) => c.file === `${name}-${width}.png` && c.viewport.width === width,
      ),
    );
console.log(
  `PASS: ${report.checks.length} actual browser checks, ${report.captures.length} screenshots, current source and asset hashes. Human art/playtest approval remains pending.`,
);
