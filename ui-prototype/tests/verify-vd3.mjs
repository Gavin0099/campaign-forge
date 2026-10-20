import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const output = path.join(root, "ui-prototype/screenshots/vd3");
const hash = (file) =>
  crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const read = (file) => JSON.parse(fs.readFileSync(file));
const report = read(path.join(output, "capture-record.json"));
assert.equal(report.pass, true);
assert.deepEqual(report.errors, []);
for (const name of [
  "geometry-camera-1280",
  "geometry-camera-1920",
  "live-keyposes-1280",
  "live-keyposes-1920",
  "committed-impact-single-update",
  "residents-full-flow",
  "grain-absent-keyboard-flow",
  "cancel-before-after-impact",
  "twenty-consecutive-replays",
  "rehearsal-story-isolation",
  "missile-allocation-simultaneous",
  "audio-actual-nodes-cancel",
  "screen-navigation-cleanup",
  "committed-navigation-before-after-impact",
  "reduced-motion-and-mid-clip-change",
  "large-text-720",
  "class-and-showcase-boundaries",
  "real-react-unmount",
  "information-and-dialogue-history",
  "four-live-recordings",
  "in-app-srd-attribution",
  "comparison-viewer",
]) {
  assert(
    report.checks.some((check) => check.name === name && check.pass),
    `Missing check ${name}`,
  );
}
for (const [file, digest] of Object.entries(report.inputs))
  assert.equal(hash(path.join(root, file)), digest, `Stale input ${file}`);
for (const capture of report.captures)
  assert.equal(
    hash(path.join(output, capture.file)),
    capture.sha256,
    `Changed capture ${capture.file}`,
  );
for (const width of [1280, 1920])
  for (const kind of ["melee", "missile"]) {
    const manifest = read(path.join(output, `recording-${kind}-${width}.json`));
    assert.equal(manifest.viewport.width, width);
    assert.equal(manifest.kind, kind);
    assert(manifest.frames.length > 30);
    assert(manifest.gif.duration_ms > (kind === "melee" ? 2200 : 3500));
    assert.equal(
      hash(path.join(output, manifest.gif.file)),
      manifest.gif.sha256,
    );
    assert.equal(
      fs.statSync(path.join(output, manifest.gif.file)).size,
      manifest.gif.bytes,
    );
  }
const replays = report.checks.find(
  (check) => check.name === "twenty-consecutive-replays",
).detail;
assert.equal(replays.length, 20);
for (const name of ["席恩・近戰攻防", "法師・Magic Missile"])
  assert.equal(replays.filter((row) => row.kind === name).length, 10);
assert(report.art_acceptance.includes("Owner review required"));
const assets = read(path.join(root, "ui-prototype/docs/vd3/assets.json"));
for (const asset of [
  assets.new_asset,
  ...assets.preserved_sources,
  ...assets.preserved_before,
])
  assert.equal(
    hash(path.join(root, asset.file)),
    asset.sha256,
    `Changed original or Before ${asset.file}`,
  );
assert(fs.existsSync(path.join(root, assets.new_asset.prompt)));
console.log(
  `PASS VD3: ${report.checks.length} executed browser checks, ${report.captures.length} PNGs, 4 live GIFs and current source/media hashes. Engineering verified; Owner art gate remains open.`,
);
