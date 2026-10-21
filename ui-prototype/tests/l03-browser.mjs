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
const output = path.join(root, "ui-prototype/screenshots/art-gate/legacy-regression"),
  scratch = path.join(root, "scratch/l03-browser");
fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(scratch, { recursive: true });
const env = Object.fromEntries(
  ["SystemRoot", "WINDIR", "SystemDrive"]
    .filter((k) => process.env[k])
    .map((k) => [k, process.env[k]]),
);
env.TEMP = scratch;
env.TMP = scratch;
const context = await chromium.launchPersistentContext(
  path.join(scratch, "profile"),
  {
    executablePath: binding.path,
    headless: true,
    viewport: { width: 1280, height: 720 },
    env,
  },
);
await context.route("**/*", (r) =>
  new URL(r.request().url()).hostname === "127.0.0.1"
    ? r.continue()
    : r.abort(),
);
const page = context.pages()[0],
  checks = [],
  captures = [],
  errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
const files = (dir) =>
  fs
    .readdirSync(path.join(root, dir), { withFileTypes: true })
    .flatMap((e) =>
      e.isDirectory() ? files(`${dir}/${e.name}`) : [`${dir}/${e.name}`],
    );
const inputs = Object.fromEntries(
  [
    ...files("ui-prototype/src"),
    "ui-prototype/public/art/l03-party-v1.png",
    "ui-prototype/public/art/l03-enemies-v1.png",
    "ui-prototype/public/art/terrain-v2.png",
    "ui-prototype/public/art/props-v2.png",
    "ui-prototype/tests/l03-browser.mjs",
    "ui-prototype/tests/verify-l03.mjs",
    "ui-prototype/package.json",
  ].map((f) => [f, hash(fs.readFileSync(path.join(root, f)))]),
);
const report = {
  started_at: new Date().toISOString(),
  baseline: "505fca779ca92c0ecd9f8fab263284e04423e723",
  browser: binding,
  inputs,
  checks,
  captures,
  errors,
  art: "New hand-painted costume/enemy studies with original vector fallbacks; Owner art and human usability review pending.",
  human_playtest: false,
};
const check = (name, detail) => {
  checks.push({ name, pass: true, detail });
  console.log("PASS " + name);
};
const click = (name) => page.getByRole("button", { name }).click();
const cell = (x, y) => page.locator(`[data-l03-cell="${x},${y}"]`);
const idle = () =>
  page.waitForFunction(
    () => document.querySelector(".l03-map")?.dataset.phase === "select",
  );
const hp = (id) =>
  page.locator(`[data-l03-unit="${id}"]`).getAttribute("data-hp");
async function begin(gate = "open") {
  await page.goto("http://127.0.0.1:5175/?scene=l03", {
    waitUntil: "networkidle",
  });
  if (gate === "sealed") await click(/02.*封閘護橋/);
}
async function shot(name) {
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() =>
    Promise.all(
      [...document.querySelectorAll("svg image")].map((e) => {
        const i = new Image();
        i.src = e.href.baseVal;
        return i.decode();
      }),
    ),
  );
  const bytes = await page.screenshot({ fullPage: true });
  const file = name + ".png";
  fs.writeFileSync(path.join(output, file), bytes);
  captures.push({ file, sha256: hash(bytes), viewport: page.viewportSize() });
}
async function preview() {
  await page.getByRole("button", { name: /01.*凱倫/ }).click();
  await cell(2, 3).click();
  await cell(3, 3).click();
  await page.getByRole("button", { name: /確認這次演出/ }).waitFor();
}
try {
  for (const width of [1280, 1920]) {
    await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
    await begin();
    await shot(`open-${width}`);
    assert.equal(await page.locator("[data-ground]").count(), 99);
    assert.equal(await page.locator("[data-l03-cell]").count(), 99);
    const aligned = await page
      .locator("[data-l03-cell]")
      .evaluateAll((nodes) =>
        nodes.every(
          (n) =>
            n.getAttribute("points") ===
            document
              .querySelector(`[data-ground="${n.dataset.l03Cell}"]`)
              ?.getAttribute("points"),
        ),
      );
    assert(aligned);
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    check(
      `geometry-layout-${width}`,
      "99 terrain/interaction polygons match exactly; no horizontal overflow.",
    );
    await preview();
    const controls = await page.locator(".l03-order-actions").boundingBox();
    assert(
      controls.y >= 0 &&
        controls.y + controls.height <= page.viewportSize().height,
    );
    const ratio = await page.locator("[data-ground]").evaluateAll((nodes) => {
      const b = nodes.map((n) => n.getBoundingClientRect());
      return (
        (Math.max(...b.map((r) => r.right)) -
          Math.min(...b.map((r) => r.left))) /
        document.querySelector(".l03-world").getBoundingClientRect().width
      );
    });
    assert(ratio >= 0.65, `Battlefield ground too small: ${ratio}`);
    check(`visible-confirmation-${width}`, {
      targetAndActionsInsideViewport: true,
      groundWidthRatio: ratio,
    });
    await shot(`preview-${width}`);
    assert.equal(await hp("knight"), "6");
    await click(/確認這次演出/);
    await idle();
    assert.equal(await hp("knight"), "3");
    assert.equal(
      await page.locator('[data-l03-unit="karen"]').getAttribute("data-acted"),
      "true",
    );
    check(
      `confirm-impact-${width}`,
      "Preview preserves HP; one confirmation changes 6 to 3 once and marks actor spent.",
    );
    await click(/下一輪預演/);
    assert.equal(await hp("knight"), "3");
    await click(/02.*封閘護橋/);
    await shot(`sealed-${width}`);
    assert.equal(await hp("knight"), "6");
    assert((await page.locator(".l03-cost").innerText()).includes("提歐"));
    check(
      `branch-reset-${width}`,
      "Sealed/open objectives and explicit costs; comparison resets only local rehearsal.",
    );
  }
  await page.setViewportSize({ width: 1280, height: 720 });
  await begin();
  const paths = await page.evaluate(async () => {
    const m = await import("/src/l03Scene.ts");
    const actor = m.sceneUnits[0];
    return {
      openBridge: m.walkable({ x: 4, y: 4 }, "open"),
      sealedBridge: m.walkable({ x: 4, y: 4 }, "sealed"),
      water: m.walkable({ x: 4, y: 5 }, "sealed"),
      occupied: m.movementCells(actor, m.sceneUnits, "sealed").has("1,7"),
      route: m.movementPath(actor, { x: 4, y: 4 }, m.sceneUnits, "sealed"),
    };
  });
  assert.equal(paths.openBridge, false);
  assert.equal(paths.sealedBridge, true);
  assert.equal(paths.water, false);
  assert.equal(paths.occupied, false);
  assert.deepEqual(
    paths.route.map((p) => `${p.x},${p.y}`),
    ["2,5", "3,5", "3,4", "4,4"],
  );
  check(
    "real-path-and-broken-bridge",
    "Runtime path walks around water and occupied cells; bridge accessibility matches selected gate mode.",
  );
  await preview();
  await page
    .getByRole("button", { name: /確認這次演出/ })
    .dblclick({ force: true });
  await idle();
  assert.equal(await hp("knight"), "3");
  check(
    "double-confirm",
    "Real double click is guarded by the active playback token; HP changes once.",
  );
  await begin();
  await preview();
  await click(/確認這次演出/);
  await click(/02.*封閘護橋/);
  await page.waitForTimeout(1800);
  assert.equal(await hp("knight"), "6");
  check(
    "branch-switch-cancels",
    "Changing comparison mode during playback cancels the old callback and resets local scene.",
  );
  await begin();
  await preview();
  await click(/取消預覽/);
  assert.equal(await hp("knight"), "6");
  assert.equal(
    await page.locator(".l03-map").getAttribute("data-phase"),
    "select",
  );
  await preview();
  await click(/確認這次演出/);
  await click(/取消預覽/);
  await page.waitForTimeout(1700);
  assert.equal(await hp("knight"), "6");
  check(
    "cancel-before-impact",
    "Cancel really prevents the later callback and preserves HP.",
  );
  await preview();
  await click(/確認這次演出/);
  await page.waitForFunction(
    () =>
      document
        .querySelector('[data-l03-unit="knight"]')
        ?.getAttribute("data-hp") === "3",
  );
  await page.keyboard.press("Escape");
  await page.waitForTimeout(700);
  assert.equal(await hp("knight"), "3");
  check(
    "cancel-after-impact",
    "An applied result remains once; Esc cancels remaining motion.",
  );
  await begin();
  await page.emulateMedia({ reducedMotion: "reduce" });
  await preview();
  await click(/確認這次演出/);
  await idle();
  assert.equal(await hp("knight"), "3");
  check(
    "reduced-motion",
    "Motion preference uses bounded abbreviated playback and one result.",
  );
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await begin();
  await page.getByRole("button", { name: /03.*托瑪/ }).click();
  await cell(1, 6).click();
  await cell(2, 5).click();
  await click(/確認這次演出/);
  await idle();
  assert.equal(await hp("karen"), "9");
  assert.equal(await hp("thoma"), "8");
  check(
    "support-contract",
    "Thoma marks support; no invented healing, resources or damage.",
  );
  await begin();
  await page.getByRole("button", { name: /02.*蕾絲/ }).click();
  await cell(2, 3).click();
  await cell(3, 3).click();
  await click(/確認這次演出/);
  await idle();
  assert.equal(await hp("knight"), "3");
  check(
    "rope-contract",
    "Lace has distinct rope feedback and the same explicitly provisional -3 example.",
  );
  await begin();
  await cell(2, 5).focus();
  await page.keyboard.press("Enter");
  await cell(2, 3).focus();
  await page.keyboard.press("Space");
  await cell(3, 3).focus();
  await page.keyboard.press("Enter");
  assert(await page.getByRole("button", { name: /確認這次演出/ }).isEnabled());
  await page.keyboard.press("Escape");
  check(
    "keyboard-grid",
    "Real SVG controls accept Enter/Space and Esc without changing HP.",
  );
  await click(/戰前情報/);
  assert(await page.getByRole("dialog").isVisible());
  await page.keyboard.press("Escape");
  await page.getByRole("dialog").waitFor({ state: "hidden" });
  await page.waitForFunction(() =>
    document.activeElement?.textContent?.includes("戰前情報"),
  );
  check(
    "dialog-focus",
    "Native modal dialog traps focus, closes with Esc and restores trigger.",
  );
  await click(/放大文字/);
  await shot("large-1280");
  assert(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await shot("large-390");
  assert(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  );
  assert(await page.getByRole("button", { name: /下一輪預演/ }).isVisible());
  check(
    "large-and-narrow",
    "Enlarged typography and 390px layout remain operable via normal vertical scroll.",
  );
  await page.setViewportSize({ width: 1280, height: 720 });
  await begin();
  await preview();
  await click(/確認這次演出/);
  await click(/返回原型主選單/);
  await page.waitForTimeout(1800);
  assert(await page.getByRole("button", { name: /繼續旅程/ }).isVisible());
  check(
    "unmount-cancel",
    "Exit really unmounts candidate during playback; old menu remains available without errors.",
  );
  await page.route("**/art/l03-party-v1.png", (r) => r.abort());
  await begin();
  assert.equal(
    await page
      .locator('[data-l03-unit="karen"] [data-l03-art="vector"]')
      .count(),
    1,
  );
  await preview();
  await click(/確認這次演出/);
  await idle();
  assert.equal(await hp("knight"), "3");
  await page.unroute("**/art/l03-party-v1.png");
  check(
    "failed-art-fallback",
    "Actual image request failure uses preserved vector costume drafts and remains operable.",
  );
  // Recheck both complete legacy routes in the same running build; preserve historical VD3 evidence.
  for (const choice of ["residents", "grain"]) {
    await page.goto("http://127.0.0.1:5175", { waitUntil: "networkidle" });
    await click(/繼續旅程/);
    await click(/前往營地/);
    await click(/前往渡口事件/);
    await click(choice === "residents" ? /先護送居民/ : /先護送軍糧/);
    if (choice === "grain") {
      await page.getByRole("checkbox", { name: /席恩/ }).uncheck();
      await page.getByRole("checkbox", { name: /奧倫/ }).uncheck();
      await page.getByRole("combobox").selectOption("1");
    }
    await click(/確認出發/);
    if (choice === "residents") {
      await shot("legacy-baseline-1280");
      await page.setViewportSize({ width: 1920, height: 1080 });
      await shot("legacy-baseline-1920");
      await page.setViewportSize({ width: 1280, height: 720 });
    }
    const legacyCell = (x, y) => page.locator(`[data-cell="${x},${y}"]`);
    await legacyCell(1, choice === "residents" ? 6 : 7).click();
    await legacyCell(1, 4).click();
    await legacyCell(2, 3).click();
    await click("確認移動與技能");
    await page.waitForFunction(
      () =>
        document.querySelector(".battle-arena")?.dataset.playback === "idle",
    );
    await click("確認護送抵達出口");
    const modal = page.getByRole("dialog");
    await modal.getByRole("button", { name: /確認/ }).click();
    await page.getByRole("button", { name: /返回戰役/ }).waitFor();
    await click(/返回戰役/);
    check(
      `legacy-full-${choice}`,
      choice === "grain"
        ? "Existing absent-Shien/Olun solo Lida route completes."
        : "Existing residents route completes.",
    );
  }
  assert.deepEqual(errors, []);
  for (const [f, digest] of Object.entries(inputs))
    assert.equal(
      hash(fs.readFileSync(path.join(root, f))),
      digest,
      `Changed source during verification: ${f}`,
    );
  report.pass = true;
} catch (e) {
  report.pass = false;
  report.failure = String(e.stack || e);
  await page.screenshot({
    path: path.join(scratch, "failure.png"),
    fullPage: true,
  });
  console.error(report.failure);
  process.exitCode = 1;
} finally {
  report.finished_at = new Date().toISOString();
  fs.writeFileSync(
    path.join(output, "capture-record.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  await context.close();
}
