import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const hash = (b) => crypto.createHash("sha256").update(b).digest("hex");
const binding = JSON.parse(
  fs.readFileSync(path.join(root, ".codex/visual-browser-binding.json")),
);
assert(path.isAbsolute(binding.path));
assert.equal(fs.realpathSync(binding.path), binding.path);
assert.equal(fs.statSync(binding.path).size, binding.bytes);
assert.equal(hash(fs.readFileSync(binding.path)), binding.sha256);
const { chromium } = await import("playwright");
const out = path.join(root, "ui-prototype/screenshots/art-gate");
const scratch = path.join(root, "scratch/art-gate-browser");
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(scratch, { recursive: true });
const files = (dir) =>
  fs
    .readdirSync(path.join(root, dir), { withFileTypes: true })
    .flatMap((e) =>
      e.isDirectory() ? files(`${dir}/${e.name}`) : [`${dir}/${e.name}`],
    );
const inputFiles = [
  ...files("ui-prototype/src"),
  ...files("ui-prototype/public/art/art-gate"),
  "ui-prototype/public/art/l03-party-v1.png",
  "ui-prototype/public/art/l03-enemies-v1.png",
  "ui-prototype/tests/art-gate-browser.mjs",
  "ui-prototype/tests/verify-art-gate.mjs",
  "ui-prototype/package.json",
];
const report = {
  started_at: new Date().toISOString(),
  baseline: "b783cf9093ce878bbb2bfdb6462364fb464e188a",
  browser: binding,
  inputs: Object.fromEntries(
    inputFiles.map((f) => [f, hash(fs.readFileSync(path.join(root, f)))]),
  ),
  checks: [],
  captures: [],
  console_errors: [],
  measurements: [],
  art_quality: "PENDING_OWNER_REVIEW",
  functional_scope:
    "static scene inspection, not movement/grid/animation validation",
  human_playtest: false,
};
const context = await chromium.launchPersistentContext(
  path.join(scratch, "profile"),
  {
    executablePath: binding.path,
    headless: true,
    viewport: { width: 1280, height: 720 },
    env: {
      SystemRoot: process.env.SystemRoot,
      WINDIR: process.env.WINDIR,
      SystemDrive: process.env.SystemDrive,
      TEMP: scratch,
      TMP: scratch,
    },
  },
);
await context.route("**/*", (r) =>
  new URL(r.request().url()).hostname === "127.0.0.1"
    ? r.continue()
    : r.abort(),
);
const page = context.pages()[0];
page.on("pageerror", (e) => report.console_errors.push(e.message));
const check = (name, detail) => {
  report.checks.push({ name, pass: true, detail });
  console.log(`PASS ${name}`);
};
const goto = async (direction) => {
  await page.goto(`http://127.0.0.1:5175/?scene=art-gate&art=${direction}`, {
    waitUntil: "networkidle",
  });
  await page.waitForFunction(
    () => document.querySelector(".ag-app")?.dataset.ready === "true",
  );
  await page.evaluate(() => document.fonts.ready);
};
const shot = async (name) => {
  const f = `${name}.png`;
  await page.screenshot({ path: path.join(out, f), fullPage: false });
  const buf = fs.readFileSync(path.join(out, f));
  report.captures.push({
    file: f,
    sha256: hash(buf),
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
    state_sha256: hash(
      await page.locator(".ag-app").getAttribute("data-scene-state"),
    ),
  });
};
try {
  let state;
  for (const width of [1280, 1920]) {
    await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
    for (const direction of ["a", "b"]) {
      await goto(direction);
      const current = await page
        .locator(".ag-app")
        .getAttribute("data-scene-state");
      if (!state) state = current;
      assert.equal(current, state);
      assert.equal(await page.locator(".ag-actor").count(), 5);
      assert.equal(await page.locator("[data-landmark]").count(), 7);
      const decoded = JSON.parse(current);
      assert.equal(decoded.boats, 3);
      assert.equal(decoded.chests, 3);
      assert.equal(decoded.actions, 0);
      assert.equal(decoded.bridge, "intact");
      assert.equal(decoded.gate, "undecided");
      const geometry = await page.evaluate(() => {
        const stage = document
          .querySelector(".ag-stage")
          .getBoundingClientRect();
        const plate = document.querySelector(".ag-plate");
        return {
          viewport: { width: innerWidth, height: innerHeight },
          plate: {
            naturalWidth: plate.naturalWidth,
            naturalHeight: plate.naturalHeight,
            width: plate.getBoundingClientRect().width,
            height: plate.getBoundingClientRect().height,
          },
          overflow: document.documentElement.scrollWidth > innerWidth,
          actorHitTargets: [...document.querySelectorAll(".ag-actor")].map(
            (e) => {
              const r = e.getBoundingClientRect();
              return {
                id: e.dataset.unit,
                x: r.x,
                y: r.y,
                width: r.width,
                height: r.height,
                visible:
                  r.x >= 0 &&
                  r.y >= 0 &&
                  r.right <= innerWidth &&
                  r.bottom <= innerHeight,
              };
            },
          ),
          stage: { width: stage.width, height: stage.height },
        };
      });
      assert(!geometry.overflow);
      assert(
        geometry.actorHitTargets.every(
          (t) => t.visible && t.width >= 24 && t.height >= 24,
        ),
      );
      assert(geometry.plate.naturalWidth > 1200);
      assert(geometry.plate.width / width > 0.99);
      // Decode every independent transparent atlas too; a loaded backdrop is not sufficient.
      await page.evaluate(async () => {
        const paths = [
          ...new Set(
            [...document.querySelectorAll(".ag-figure image")].map((i) =>
              i.getAttribute("href"),
            ),
          ),
        ];
        await Promise.all(
          paths.map(
            (src) =>
              new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = reject;
                img.src = src;
              }),
          ),
        );
      });
      await page.locator("[data-unit=karen]").click();
      await shot(`${direction}-${width}`);
      report.measurements.push({ direction, width, ...geometry });
      check(
        `${direction}-${width}-composition`,
        "Actual loaded environment + independent actors + HTML HUD; shared pre-K1 state, 5 actor hit targets, 7 narrative inspection points, no horizontal clipping. Object count in painted plate requires visual inspection, not DOM-count proof.",
      );
    }
  }
  report.scene_state_sha256 = hash(state);
  await page.setViewportSize({ width: 1280, height: 720 });
  await goto("a");
  const prior = await page.locator(".ag-app").getAttribute("data-scene-state");
  await page.getByRole("button", { name: /^B 立體造型$/ }).click();
  await page.waitForFunction(
    () => document.querySelector(".ag-app")?.dataset.ready === "true",
  );
  assert.equal(await page.locator(".ag-app").getAttribute("data-art"), "b");
  assert.equal(
    await page.locator(".ag-app").getAttribute("data-scene-state"),
    prior,
  );
  assert.equal(new URL(page.url()).searchParams.get("art"), "b");
  check(
    "switch-preserves-state",
    "Direction control changes scene/actor assets and URL while pre-K1 data remains identical.",
  );
  for (const id of [
    "teo",
    "boats",
    "gate",
    "bridge",
    "maggie",
    "caravan",
    "refugees",
  ]) {
    const target = page.locator(`[data-landmark=${id}]`);
    await target.focus();
    await page.keyboard.press("Enter");
    assert.equal(await target.getAttribute("aria-pressed"), "true");
    await page.keyboard.press("Escape");
    assert.equal(await target.getAttribute("aria-pressed"), "false");
  }
  await page.locator("[data-landmark=maggie]").click();
  await shot("maggie-1280");
  check(
    "landmarks-keyboard-and-escape",
    "All seven narrative targets are keyboard operable; Esc cancels selection without advancing state. Maggie has a scene anchor and inspectable description.",
  );
  await page.getByRole("button", { name: "地標", exact: true }).click();
  assert.equal(await page.locator(".ag-landmarks.show-labels").count(), 1);
  check(
    "landmark-labels",
    "Optional labels are controlled independently of scene data.",
  );
  await page.getByRole("button", { name: "大字", exact: true }).click();
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: width === 1280 ? 720 : 844 });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > innerWidth,
    );
    assert(!overflow);
    await page.getByRole("button", { name: "瑪歌", exact: true }).click();
    assert(
      await page
        .locator(".ag-inspector")
        .getByText("瑪歌", { exact: true })
        .isVisible(),
    );
    await page.locator(".ag-inspector").scrollIntoViewIfNeeded();
    await shot(`large-${width}`);
  }
  check(
    "large-text-and-narrow",
    "200% text setting reflows HUD into document flow; 1280 and 390 have no horizontal overflow; essential landmarks remain available in text index. Narrow image itself is not a desktop-quality tactical view.",
  );
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.route("**/art/art-gate/river-a-v1.png", (r) => r.abort());
  await page.goto("http://127.0.0.1:5175/?scene=art-gate&art=a", {
    waitUntil: "networkidle",
  });
  await page.getByRole("alert").waitFor();
  await page.getByRole("button", { name: "地標", exact: true }).click();
  await page.getByRole("button", { name: "大字", exact: true }).click();
  await page.getByRole("button", { name: "提歐的燈", exact: true }).click();
  assert(
    await page
      .locator(".ag-inspector")
      .getByText("提歐的燈", { exact: true })
      .isVisible(),
  );
  await page.unroute("**/art/art-gate/river-a-v1.png");
  await page.getByRole("button", { name: "重試場景圖片", exact: true }).click();
  await page.waitForFunction(
    () => document.querySelector(".ag-app")?.dataset.ready === "true",
  );
  check(
    "failed-plate-recovery",
    "Real failed scene image request gives an alert, retains narrative inspection and succeeds after retry.",
  );
  await page.emulateMedia({ reducedMotion: "reduce" });
  await goto("b");
  await page.locator("[data-unit=lace]").focus();
  await page.keyboard.press("Space");
  assert.equal(
    await page.locator("[data-unit=lace]").getAttribute("aria-pressed"),
    "true",
  );
  check(
    "reduced-motion-static",
    "No new motion pipeline; selection remains keyboard-operable under reduced motion.",
  );
  await page.getByRole("button", { name: "返回", exact: true }).click();
  assert(await page.getByRole("button", { name: /繼續旅程/ }).isVisible());
  assert.equal(
    await page
      .getByRole("button", { name: /L03 · 美術方向/ })
      .evaluate((e) => e === document.activeElement),
    true,
  );
  await page.getByRole("button", { name: /L03 · 美術方向/ }).click();
  await page.waitForFunction(
    () => document.querySelector(".ag-app")?.dataset.ready === "true",
  );
  check(
    "menu-entry-and-return",
    "Candidate view mounts from original menu and returns without replacing legacy L03 entry.",
  );
  assert.deepEqual(report.console_errors, []);
  for (const [f, digest] of Object.entries(report.inputs))
    assert.equal(
      hash(fs.readFileSync(path.join(root, f))),
      digest,
      `Input changed: ${f}`,
    );
  report.pass = true;
} catch (e) {
  report.pass = false;
  report.failure = String(e.stack || e);
  console.error(report.failure);
  process.exitCode = 1;
  await page.screenshot({
    path: path.join(scratch, "failure.png"),
    fullPage: true,
  });
} finally {
  report.finished_at = new Date().toISOString();
  fs.writeFileSync(
    path.join(out, "capture-record.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  await context.close();
}
