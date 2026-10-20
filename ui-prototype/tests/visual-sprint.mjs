import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

// Test-only browser binding: no PATH lookup, credentials, remote browser, or deployment.
const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const bindingPath = path.join(root, ".codex/visual-browser-binding.json");
const hash = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
if (process.argv[2] === "--bind") {
  const candidate = process.argv[3];
  assert(
    candidate && path.isAbsolute(candidate),
    "Provide an explicit absolute installed Chrome path",
  );
  const executable = fs.realpathSync(candidate);
  assert(fs.statSync(executable).isFile());
  fs.mkdirSync(path.dirname(bindingPath), { recursive: true });
  fs.writeFileSync(
    bindingPath,
    JSON.stringify(
      {
        path: executable,
        bytes: fs.statSync(executable).size,
        sha256: hash(fs.readFileSync(executable)),
        scope: "local UI browser acceptance only",
      },
      null,
      2,
    ),
  );
  console.log(
    "Bound installed browser for local UI acceptance; rerun without --bind.",
  );
  process.exit(0);
}
const browserBinding = JSON.parse(fs.readFileSync(bindingPath, "utf8"));
assert(path.isAbsolute(browserBinding.path));
assert.equal(fs.realpathSync(browserBinding.path), browserBinding.path);
assert.equal(
  fs.statSync(browserBinding.path).size,
  browserBinding.bytes,
  "Browser bytes changed; inspect and explicitly bind again",
);
assert.equal(
  hash(fs.readFileSync(browserBinding.path)),
  browserBinding.sha256,
  "Browser digest changed",
);
const { chromium } = await import("playwright");
const inputs = {};
for (const directory of ["ui-prototype/src", "ui-prototype/public/art"]) {
  for (const name of fs.readdirSync(path.join(root, directory))) {
    const relative = `${directory}/${name}`;
    if (fs.statSync(path.join(root, relative)).isFile())
      inputs[relative] = hash(fs.readFileSync(path.join(root, relative)));
  }
}
for (const relative of [
  "ui-prototype/tests/visual-sprint.mjs",
  "ui-prototype/package-lock.json",
])
  inputs[relative] = hash(fs.readFileSync(path.join(root, relative)));
const output = path.join(root, "ui-prototype/screenshots/visual-sprint/after");
const scratch = path.join(root, "scratch/visual-acceptance");
fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(scratch, { recursive: true });
const environment = Object.fromEntries(
  ["SystemRoot", "WINDIR", "SystemDrive"]
    .filter((key) => process.env[key])
    .map((key) => [key, process.env[key]]),
);
environment.TEMP = scratch;
environment.TMP = scratch;
const context = await chromium.launchPersistentContext(
  path.join(scratch, "profile"),
  {
    executablePath: browserBinding.path,
    headless: true,
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    env: environment,
  },
);
await context.route("**/*", (route) =>
  new URL(route.request().url()).hostname === "127.0.0.1"
    ? route.continue()
    : route.abort(),
);
const page = context.pages()[0];
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));
page.on("response", (response) => {
  if (response.status() >= 400)
    errors.push(`${response.status()} ${response.url()}`);
});
const records = [];
const captures = [];
const check = (name, detail) => {
  records.push({ name, pass: true, detail });
  console.log(`PASS ${name}`);
};
const click = (name) => page.getByRole("button", { name }).click();
const cell = (x, y) =>
  page.getByRole("button", { name: new RegExp(`^${x} 列 ${y} 行`) });
const unit = (id) => page.locator(`[data-unit="${id}"]`);
async function shot(name) {
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(output, `${name}.png`) });
  const overflow = await page.evaluate(() => ({
    width: innerWidth,
    scroll: document.documentElement.scrollWidth,
  }));
  assert(overflow.scroll <= overflow.width, `Horizontal overflow in ${name}`);
  const record = {
    file: `${name}.png`,
    ...overflow,
    height: page.viewportSize().height,
    sha256: hash(fs.readFileSync(path.join(output, `${name}.png`))),
  };
  captures.push(record);
  return record;
}
async function begin(choice = "residents", absent = false, capture = "") {
  await page.goto("http://127.0.0.1:5173", { waitUntil: "networkidle" });
  await click(/繼續旅程/);
  await click(/前往營地/);
  if (capture) await shot(`camp-${capture}`);
  await click(/前往渡口事件/);
  if (capture) await shot(`story-${capture}`);
  await click(choice === "residents" ? /先護送居民/ : /先護送軍糧/);
  if (absent) {
    await page.getByRole("checkbox", { name: /席恩/ }).uncheck();
    await page.getByRole("checkbox", { name: /奧倫/ }).uncheck();
    await page.getByRole("combobox").selectOption("1");
  }
  if (capture) await shot(`deploy-${capture}`);
  await click(/確認出發/);
}
async function boardCheck(label) {
  const ground = await page
    .locator(".terrain-ground polygon[data-terrain]")
    .evaluateAll((elements) =>
      elements.map((e) => ({
        x: e.getAttribute("data-x"),
        y: e.getAttribute("data-y"),
        terrain: e.getAttribute("data-terrain"),
        points: e.getAttribute("points"),
      })),
    );
  const hits = await page.locator("[data-cell]").evaluateAll((elements) =>
    elements.map((e) => ({
      xy: e.getAttribute("data-cell"),
      terrain: e.getAttribute("data-terrain"),
      points: e.getAttribute("points"),
    })),
  );
  assert.equal(ground.length, 99);
  assert.equal(hits.length, 99);
  for (const tile of ground)
    assert.deepEqual(
      hits.find((e) => e.xy === `${tile.x},${tile.y}`),
      { xy: `${tile.x},${tile.y}`, terrain: tile.terrain, points: tile.points },
    );
  const rows = [
    "...~~.R....",
    "..F~~.R....",
    "..F~~.R.FF.",
    "....~~..FF.",
    ".F..~~.....",
    "....RR.F...",
    "....~~.F...",
    ".....~~....",
    ".....~~~...",
  ];
  for (const tile of ground)
    assert.equal(tile.terrain, rows[Number(tile.y)][Number(tile.x)]);
  check(
    label,
    "All 99 rendered ground polygons exactly match hit polygons and unchanged baseline terrain",
  );
}
async function tabTo(locator) {
  for (let step = 0; step < 120; step++) {
    if (await locator.evaluate((element) => element === document.activeElement))
      return;
    await page.keyboard.press("Tab");
  }
  throw new Error("Control unreachable using real Tab navigation");
}
async function preview(
  actorX = 2,
  actorY = 7,
  destX = 2,
  destY = 5,
  keyboard = false,
) {
  for (const [x, y] of [
    [actorX, actorY],
    [destX, destY],
    [3, 4],
  ]) {
    if (keyboard) {
      await tabTo(cell(x, y));
      await page.keyboard.press("Enter");
    } else await cell(x, y).click();
  }
}
async function finish(choice, keyboard = false) {
  if (keyboard) {
    await tabTo(page.getByRole("button", { name: /確認護送抵達出口/ }));
    await page.keyboard.press("Enter");
  } else await click(/確認護送抵達出口/);
  const dialog = page.getByRole("dialog");
  assert(await dialog.isVisible());
  await page.keyboard.press("Shift+Tab");
  assert.equal(
    await page.evaluate(() => document.activeElement?.textContent),
    "確認完成此關",
  );
  await page.keyboard.press("Tab");
  assert.equal(
    await page.evaluate(() => document.activeElement?.textContent),
    "繼續檢查戰場",
  );
  await page.keyboard.press("Escape");
  assert.equal(await dialog.count(), 0);
  assert.equal(
    await page.evaluate(() => document.activeElement?.textContent),
    "確認護送抵達出口",
  );
  if (keyboard) await page.keyboard.press("Enter");
  else await click(/確認護送抵達出口/);
  if (keyboard) {
    await page.keyboard.press("Tab");
    await page.keyboard.press("Enter");
  } else await click(/確認完成此關/);
  assert(await page.getByRole("heading", { name: /渡口之後/ }).isVisible());
  const resultText = await page.locator("main").innerText();
  assert(
    resultText.includes(
      choice === "residents" ? "糧車仍困在低地" : "低地居民只能自行尋路",
    ),
  );
  assert(
    resultText.includes(
      choice === "residents" ? "要求公開守線風險" : "要求回渡口尋人",
    ),
  );
  if (keyboard) {
    await tabTo(page.getByRole("button", { name: /返回戰役旅程/ }));
    await page.keyboard.press("Enter");
  } else await click(/返回戰役旅程/);
  assert(
    (await page.locator("main").innerText()).includes(
      choice === "residents" ? "補給不足" : "回收落單者",
    ),
  );
  check(
    `complete-${choice}`,
    "Preview, confirm, modal keyboard trap/Esc, result consequences and return to campaign",
  );
}
const report = {
  started_at: new Date().toISOString(),
  browser: { path: browserBinding.path, sha256: browserBinding.sha256 },
  origin:
    "local installed Chrome, real React UI interactions; not generated mock screenshots",
  results: records,
  inputs,
  captures,
  same_state: {
    choice: "residents",
    deployed: ["shien", "lida", "olun"],
    actor: "shien",
    destination: { x: 1, y: 4 },
    target: "scout",
    turn: 1,
    actions: 0,
  },
};
try {
  for (const [width, height] of [
    [1920, 1080],
    [1280, 720],
  ]) {
    await page.setViewportSize({ width, height });
    await begin("residents", false, String(width));
    await boardCheck(`geometry-${width}`);
    await shot(`battle-idle-${width}`);
    await cell(2, 7).click();
    assert.equal(
      await cell(5, 5).getAttribute("aria-disabled"),
      "true",
      "River remains impassable",
    );
    assert.equal(
      await cell(2, 8).getAttribute("aria-disabled"),
      "true",
      "Occupied ally cell remains unavailable",
    );
    await shot(`battle-move-range-${width}`);
    await cell(2, 5).click();
    assert.equal(
      await cell(9, 6).getAttribute("aria-disabled"),
      "true",
      "Distant enemy is outside skill range",
    );
    await shot(`battle-skill-range-${width}`);
    await cell(3, 4).click();
    const forecast = await page.locator(".skill-forecast").boundingBox();
    const confirm = await page
      .getByRole("button", { name: /確認移動與技能/ })
      .boundingBox();
    assert(
      forecast.y + forecast.height <= confirm.y,
      "Forecast must not be covered by confirmation controls",
    );
    assert(
      confirm.y + confirm.height <= height,
      "Confirmation must be in the normal viewport",
    );
    const undo = await page
      .getByRole("button", { name: /撤銷未確認操作/ })
      .boundingBox();
    const inspection = await page
      .locator(".battle-sidebar > .battle-box:nth-child(2)")
      .boundingBox();
    assert(
      undo.y + undo.height <= inspection.y + inspection.height,
      "Undo must not be clipped by its panel",
    );
    assert.equal(await unit("shien").getAttribute("data-y"), "6");
    assert((await cell(3, 4).getAttribute("aria-label")).includes("生命 6"));
    assert.equal(await page.locator(".ghost-unit").count(), 1);
    await shot(`battle-preview-${width}`);
    await click(/撤銷未確認操作/);
    assert.equal(await page.locator(".ghost-unit").count(), 0);
    assert.equal(await unit("shien").getAttribute("data-y"), "6");
    assert((await cell(3, 4).getAttribute("aria-label")).includes("生命 6"));
    assert(
      await page.getByRole("button", { name: /確認移動與技能/ }).isDisabled(),
    );
    await cell(2, 5).click();
    await cell(3, 4).click();
    await click(/確認移動與技能/);
    assert.equal(await unit("shien").getAttribute("data-y"), "4");
    assert((await cell(3, 4).getAttribute("aria-label")).includes("生命 3"));
    assert((await unit("shien").getAttribute("class")).includes("has-acted"));
    await page.waitForTimeout(90);
    await shot(`battle-hit-${width}`);
    await click(/結束回合/);
    assert(!(await unit("shien").getAttribute("class")).includes("has-acted"));
    assert(
      (await page.locator(".turn-marker").innerText()).includes("第 2 回合"),
    );
    await finish("residents");
    check(
      `residents-${width}`,
      "Same baseline preview state, undo leaves position/HP unchanged, confirmation moves and deals exactly 3, turn resets",
    );
  }
  await page.setViewportSize({ width: 1280, height: 720 });
  await begin("grain", true);
  assert.equal(await unit("shien").count(), 0);
  assert.equal(await unit("olun").count(), 0);
  assert.equal(await unit("lida").count(), 1);
  assert(
    (await page.locator(".battle-head").innerText()).includes(
      "奧倫的工事小隊可用",
    ),
  );
  await preview(2, 8, 3, 6, true);
  await tabTo(page.getByRole("button", { name: /確認移動與技能/ }));
  await page.keyboard.press("Space");
  assert.equal(await unit("lida").getAttribute("data-y"), "5");
  assert((await cell(3, 4).getAttribute("aria-label")).includes("生命 3"));
  await finish("grain", true);
  check(
    "absent-characters-keyboard",
    "Only Lida deployed; keyboard activation of SVG cells and confirmation; main flow succeeds without Shien or Olun",
  );
  await begin();
  await click("閱讀設定");
  await page.getByRole("checkbox", { name: /放大文字/ }).check();
  await click(/完成 →/);
  await preview();
  await shot("battle-large-text-1280");
  await click(/確認移動與技能/);
  await finish("residents");
  check(
    "large-text",
    "Enlarged text at 720p; controls reachable and full flow completed without horizontal overflow",
  );
  await page.emulateMedia({ reducedMotion: "reduce" });
  await begin();
  await preview();
  await click(/確認移動與技能/);
  assert.equal(
    await page
      .locator(".hit-feedback")
      .evaluate((e) => getComputedStyle(e).display),
    "none",
  );
  assert(
    (await page.getByRole("status").innerText()).includes("固定示範效果 3"),
  );
  await shot("battle-reduced-motion-1280");
  check(
    "reduced-motion",
    "Animated hit suppressed; live text and final position/HP remain available",
  );
  await page.keyboard.press("Escape");
  assert(
    await page.getByRole("heading", { name: /渡口的最後一趟/ }).isVisible(),
  );
  await page.keyboard.press("Escape");
  await click(/展開對白紀錄/);
  assert(
    (await page.locator(".dialogue-history").innerText()).includes(
      "名冊說這裡空了",
    ),
  );
  await shot("story-history-1280");
  await click(/收起對白紀錄/);
  await page.keyboard.press("Escape");
  for (const [width, height] of [
    [1920, 1080],
    [1280, 720],
  ]) {
    await page.setViewportSize({ width, height });
    for (const name of ["席恩", "莉妲", "奧倫", "瑪芮"]) {
      await page.getByRole("button", { name: new RegExp(`${name}.*`) }).click();
      await shot(
        `character-${{ 席恩: "shien", 莉妲: "lida", 奧倫: "olun", 瑪芮: "marui" }[name]}-${width}`,
      );
    }
  }
  check(
    "history-esc-four-characters",
    "Dialogue history open/close, Esc return and four distinct character views rendered",
  );
  assert.deepEqual(errors, [], "Browser runtime or failed resource requests");
  check("browser-console", "No page errors or failed HTTP resources");
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto("http://127.0.0.1:5173/docs/visual-sprint/comparison.html", {
    waitUntil: "networkidle",
  });
  await page.locator("#split").fill("50");
  await page.screenshot({
    path: path.join(output, "comparison-1080.png"),
    fullPage: true,
  });
  for (const [width, height] of [
    [640, 360],
    [460, 259],
  ]) {
    await page.setViewportSize({ width, height });
    const src =
      "data:image/png;base64," +
      fs
        .readFileSync(path.join(output, "battle-preview-1920.png"))
        .toString("base64");
    await page.setContent(
      `<style>html,body{margin:0;width:100%;height:100%;overflow:hidden}img{display:block;width:100%;height:100%}</style><img alt="Actual game capture scaled by Chromium" src="${src}">`,
    );
    await page.locator("img").evaluate((img) => img.decode());
    const file = `battle-thumbnail-${width}.png`;
    await page.screenshot({ path: path.join(output, file) });
    captures.push({
      file,
      width,
      height,
      sha256: hash(fs.readFileSync(path.join(output, file))),
      origin: "Chromium resampling of actual 1920x1080 capture",
    });
  }
  assert.deepEqual(errors, []);
  for (const [relative, digest] of Object.entries(inputs))
    assert.equal(
      hash(fs.readFileSync(path.join(root, relative))),
      digest,
      "Source changed during capture",
    );
  report.pass = true;
} catch (error) {
  report.pass = false;
  report.failure = error.stack;
  await page.screenshot({
    path: path.join(scratch, "failure.png"),
    fullPage: true,
  });
  throw error;
} finally {
  report.finished_at = new Date().toISOString();
  report.errors = errors;
  report.browser_version = context.browser()?.version();
  fs.writeFileSync(
    path.join(root, "ui-prototype/docs/visual-sprint/browser-results.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  await context.close();
}
