import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const hash = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const report = JSON.parse(
  fs.readFileSync(
    path.join(root, "ui-prototype/docs/visual-sprint/browser-results.json"),
    "utf8",
  ),
);
assert.equal(report.pass, true);
assert(
  report.results.length >= 13 && report.results.every((result) => result.pass),
);
assert.equal(report.errors.length, 0);
for (const [relative, digest] of Object.entries(report.inputs))
  assert.equal(
    hash(fs.readFileSync(path.join(root, relative))),
    digest,
    `Stale browser evidence: ${relative}`,
  );
for (const capture of report.captures)
  assert.equal(
    hash(
      fs.readFileSync(
        path.join(
          root,
          "ui-prototype/screenshots/visual-sprint/after",
          capture.file,
        ),
      ),
    ),
    capture.sha256,
    `Changed capture: ${capture.file}`,
  );
console.log(
  `PASS: ${report.results.length} real-browser checks, ${report.captures.length} captures; input and capture digests match current source.`,
);
