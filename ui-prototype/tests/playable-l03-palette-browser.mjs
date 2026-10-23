// Same-state, source-preserving A/B screenshot protocol for the Ferry Dusk POC.
// Run Vite at 127.0.0.1:5183 first; use the existing audited browser binding.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = path.resolve(import.meta.dirname, "../..");
const out = path.join(root, "ui-prototype/docs/playable-l03-palette/captures");
const scratch = path.join(root, "scratch/playable-l03-palette");
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(scratch, { recursive: true });

const browserBinding = JSON.parse(fs.readFileSync(path.join(root, ".codex/visual-browser-binding.json"), "utf8"));
assert(path.isAbsolute(browserBinding.path));
assert.equal(fs.realpathSync(browserBinding.path), browserBinding.path);
assert.equal(fs.statSync(browserBinding.path).size, browserBinding.bytes);
const hash = data => crypto.createHash("sha256").update(data).digest("hex");
assert.equal(hash(fs.readFileSync(browserBinding.path)), browserBinding.sha256);

const { chromium } = await import("playwright");
const env = Object.fromEntries(["SystemRoot", "WINDIR", "SystemDrive"].filter(k => process.env[k]).map(k => [k, process.env[k]]));
Object.assign(env, { TEMP: scratch, TMP: scratch });
const context = await chromium.launchPersistentContext(path.join(scratch, "profile"), {
  executablePath: browserBinding.path, headless: true, env
});
const base = new URL(process.env.CAMPAIGN_FORGE_URL || "http://127.0.0.1:5183/");
const page = context.pages()[0];
const errors = [];
page.on("pageerror", e => errors.push(e.message));
page.on("response", r => { if (r.status() >= 400) errors.push(r.status() + " " + r.url()); });
await context.route("**/*", route => new URL(route.request().url()).origin === base.origin
  ? route.continue() : route.abort());

const report = {
  started_at: new Date().toISOString(),
  source_branch: "review/ferry-dusk-palette-poc",
  browser: browserBinding,
  environment: { base: base.origin, reduced_motion: true },
  captures: [], checks: [], errors, owner_review: "HUMAN_PENDING"
};
const cases = [
  { width: 1280, height: 720 },
  { width: 1920, height: 1080 }
];
function nearRect(a, b) {
  return Object.keys(a).every(k => Math.abs(a[k] - b[k]) < 0.1);
}
async function visit(mode, viewport, stage) {
  const u = new URL(base);
  u.searchParams.set("scene", "playable-l03");
  if (mode === "ferry-dusk") u.searchParams.set("palette", mode);
  await page.setViewportSize(viewport);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto(u.href);
  await page.locator('[data-p1v-busy="false"]').waitFor();
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...new Set([...document.querySelectorAll("svg image")]
      .map(n => n.getAttribute("href")).filter(Boolean))].map(async source => {
      const image = new Image(); image.src = source; await image.decode();
    }));
  });
  if (stage === "selected") await page.locator('[data-p1v-select="karen"]').click();
  await page.mouse.move(4, 4);
  const summary = await page.evaluate(() => {
    const el = document.querySelector(".p1v");
    const b = document.querySelector('[data-p1v-battlefield]');
    const frame = document.querySelector(".p1v-map").getBoundingClientRect();
    const units = [...document.querySelectorAll('[data-p1v-unit]')].map(node => {
      const rect = node.getBoundingClientRect();
      return { id: node.getAttribute("data-p1v-unit"), rect: {
        left: rect.left, top: rect.top, width: rect.width, height: rect.height
      }};
    });
    return {
      palette: el.dataset.p1vPalette,
      state: JSON.parse(el.dataset.p1vState),
      selected: el.dataset.p1vSelected,
      battlefieldFilter: getComputedStyle(b).filter,
      mapRect: { left: frame.left, top: frame.top, width: frame.width, height: frame.height },
      units
    };
  });
  assert.equal(summary.palette, mode);
  assert.equal(summary.selected, stage === "selected" ? "karen" : "");
  assert.equal(summary.units.length, 5);
  const filename = viewport.width + "x" + viewport.height + "-" + stage + "-" + mode + ".png";
  await page.screenshot({ path: path.join(out, filename), animations: "disabled" });
  report.captures.push({
    filename, viewport, mode, stage,
    sha256: hash(fs.readFileSync(path.join(out, filename))), summary
  });
  return summary;
}
try {
  for (const viewport of cases) {
    for (const stage of ["start", "selected"]) {
      const normal = await visit("original", viewport, stage);
      const graded = await visit("ferry-dusk", viewport, stage);
      assert.deepEqual(graded.state, normal.state, "game state differs across palettes");
      assert.notEqual(graded.battlefieldFilter, normal.battlefieldFilter, "painted image was not recolored");
      assert(nearRect(graded.mapRect, normal.mapRect), "palette changed map geometry");
      assert.deepEqual(graded.units.map(u => u.id), normal.units.map(u => u.id));
      for (let i = 0; i < graded.units.length; i++) {
        assert(nearRect(graded.units[i].rect, normal.units[i].rect),
          "palette changed unit bounding box: " + graded.units[i].id);
      }
      report.checks.push({ viewport, stage, state_parity: "pass", map_geometry: "pass",
        unit_geometry: "pass", image_filter_difference: "pass" });
    }
  }
  assert.deepEqual(errors, []);
  report.exit_code = 0;
} catch (error) {
  report.exit_code = 1;
  report.failure = String(error.stack || error);
  process.exitCode = 1;
  console.error(error);
} finally {
  report.finished_at = new Date().toISOString();
  fs.writeFileSync(path.join(out, "report.json"), JSON.stringify(report, null, 2) + "\n");
  await context.close();
}
