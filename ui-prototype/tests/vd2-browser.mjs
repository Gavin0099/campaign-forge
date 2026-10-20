import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const hash = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const binding = JSON.parse(
  fs.readFileSync(path.join(root, ".codex/visual-browser-binding.json")),
);
assert(path.isAbsolute(binding.path));
assert.equal(fs.realpathSync(binding.path), binding.path);
assert.equal(fs.statSync(binding.path).size, binding.bytes);
assert.equal(hash(fs.readFileSync(binding.path)), binding.sha256);
const { chromium } = await import("playwright");
assert(
  !process.argv.includes("--before"),
  "Before is frozen at main@0fc109f; never recapture it from modified source",
);
const mode = "after";
const output = path.join(root, `ui-prototype/screenshots/vd2/${mode}`);
const scratch = path.join(root, "scratch/vd2-browser");
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
    executablePath: binding.path,
    headless: true,
    viewport: { width: 1280, height: 720 },
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
const captures = [];
const checks = [];
const inputs = {};
for (const directory of [
  "ui-prototype/src",
  "ui-prototype/public/art",
  "ui-prototype/tests",
])
  for (const name of fs.readdirSync(path.join(root, directory))) {
    const relative = `${directory}/${name}`;
    if (fs.statSync(path.join(root, relative)).isFile())
      inputs[relative] = hash(fs.readFileSync(path.join(root, relative)));
  }
const report = {
  started_at: new Date().toISOString(),
  inputs,
  captures,
  checks,
  errors,
  media: [],
};
for (const relative of [
  "ui-prototype/package.json",
  "ui-prototype/package-lock.json",
])
  inputs[relative] = hash(fs.readFileSync(path.join(root, relative)));
const check = (name, detail) => {
  checks.push({ name, pass: true, detail });
  console.log(`PASS ${name}`);
};
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
const click = (name) => page.getByRole("button", { name }).click();
const cell = (x, y) => page.locator(`[data-cell="${x},${y}"]`);
const unit = (id) => page.locator(`[data-unit="${id}"]`);
async function decodeArtwork() {
  await page.evaluate(() =>
    Promise.all(
      [...document.querySelectorAll("svg image")].map((element) => {
        const image = new Image();
        image.src = element.href.baseVal;
        return image.decode();
      }),
    ),
  );
}
const stage = () => page.locator(".battle-arena").getAttribute("data-playback");
const snapshot = () =>
  page.locator("[data-unit]").evaluateAll((es) =>
    es.map((e) => ({
      id: e.dataset.unit,
      x: e.dataset.x,
      y: e.dataset.y,
      text: e.textContent,
    })),
  );
async function waitStage(value) {
  await page.waitForFunction(
    (v) => document.querySelector(".battle-arena")?.dataset.playback === v,
    value,
  );
}
async function idle() {
  await waitStage("idle");
}
async function preview(absent = false, keyboard = false) {
  for (const [x, y] of [
    absent ? [1, 7] : [1, 6],
    absent ? [2, 5] : [1, 4],
    [2, 3],
  ]) {
    if (keyboard) {
      await tabTo(cell(x, y));
      await page.keyboard.press("Enter");
    } else await cell(x, y).click();
  }
}
async function tabTo(locator) {
  for (let i = 0; i < 160; i++) {
    if (await locator.evaluate((e) => document.activeElement === e)) return;
    await page.keyboard.press("Tab");
  }
  throw Error("Keyboard control unreachable");
}
async function finish(choice) {
  await click(/確認護送抵達出口/);
  await page.keyboard.press("Shift+Tab");
  assert.equal(
    await page.evaluate(() => document.activeElement.textContent),
    "確認完成此關",
  );
  await page.keyboard.press("Tab");
  assert.equal(
    await page.evaluate(() => document.activeElement.textContent),
    "繼續檢查戰場",
  );
  await page.keyboard.press("Escape");
  assert.equal(await page.getByRole("dialog").count(), 0);
  assert.equal(
    await page.evaluate(() => document.activeElement.textContent),
    "確認護送抵達出口",
  );
  await page.keyboard.press("Enter");
  await click(/確認完成此關/);
  assert(await page.getByRole("heading", { name: /渡口之後/ }).isVisible());
  const text = await page.locator("main").innerText();
  assert(
    text.includes(
      choice === "residents" ? "糧車仍困在低地" : "低地居民只能自行尋路",
    ),
  );
  assert(
    text.includes(
      choice === "residents" ? "要求公開守線風險" : "要求回渡口尋人",
    ),
  );
  await click(/返回戰役旅程/);
  assert(
    (await page.locator("main").innerText()).includes(
      choice === "residents" ? "補給不足" : "回收落單者",
    ),
  );
}
async function record(width) {
  await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
  await begin();
  await preview();
  const session = await context.newCDPSession(page),
    frames = [];
  const frameDir = path.join(scratch, `frames-${width}`);
  fs.mkdirSync(frameDir, { recursive: true });
  session.on("Page.screencastFrame", (event) => {
    const bytes = Buffer.from(event.data, "base64"),
      file = `${String(frames.length).padStart(5, "0")}.jpg`;
    fs.writeFileSync(path.join(frameDir, file), bytes);
    frames.push({
      file,
      timestamp: event.metadata.timestamp,
      sha256: hash(bytes),
    });
    void session.send("Page.screencastFrameAck", {
      sessionId: event.sessionId,
    });
  });
  await session.send("Page.startScreencast", {
    format: "jpeg",
    quality: 85,
    maxWidth: width,
    maxHeight: page.viewportSize().height,
    everyNthFrame: 2,
  });
  await click(/確認移動與技能/);
  await idle();
  await click("演出展示");
  for (const [name, kind] of [
    ["裂潮・光矢", "arcane"],
    ["封蠟・護印", "ward"],
    ["受擊示範", "hit"],
  ]) {
    await click(name);
    await page.waitForFunction(
      (k) => !!document.querySelector(`[data-effect="${k}"]`) || k === "hit",
      kind,
    );
    if (kind !== "hit") {
      await waitStage("impact");
      await shot(`${kind}-impact-${width}`);
    }
    await idle();
  }
  await session.send("Page.stopScreencast");
  await session.detach();
  const manifest = {
    viewport: page.viewportSize(),
    origin:
      "Actual local Chromium CDP screencast JPEG frames, no composited animation",
    frames,
  };
  fs.writeFileSync(
    path.join(output, `recording-${width}.json`),
    JSON.stringify(manifest, null, 2) + "\n",
  );
  report.media.push({
    width,
    frames: frames.length,
    seconds: frames.at(-1).timestamp - frames[0].timestamp,
  });
}
async function begin(choice = "residents", absent = false) {
  await page.goto("http://127.0.0.1:5174", { waitUntil: "networkidle" });
  await click(/繼續旅程/);
  await click(/前往營地/);
  await click(/前往渡口事件/);
  await click(choice === "residents" ? /先護送居民/ : /先護送軍糧/);
  if (absent) {
    await page.getByRole("checkbox", { name: /席恩/ }).uncheck();
    await page.getByRole("checkbox", { name: /奧倫/ }).uncheck();
    await page.getByRole("combobox").selectOption("1");
  }
  await click(/確認出發/);
  await page.waitForLoadState("networkidle");
  await decodeArtwork();
}
async function shot(name) {
  await page.evaluate(() => document.fonts.ready);
  await decodeArtwork();
  const file = `${name}.png`;
  await page.screenshot({ path: path.join(output, file) });
  captures.push({
    file,
    sha256: hash(fs.readFileSync(path.join(output, file))),
    viewport: page.viewportSize(),
  });
  assert(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    `Horizontal overflow: ${name}`,
  );
}
try {
  for (const width of [1280, 1920]) {
    await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
    await begin();
    await shot(`battle-idle-${width}`);
    await cell(1, 6).click();
    await cell(1, 4).click();
    await cell(2, 3).click();
    await shot(`battle-preview-${width}`);
    if (mode === "after") {
      await page
        .getByRole("combobox", { name: "候選美術方向" })
        .selectOption("ember");
      await shot(`candidate-ember-${width}`);
      await page
        .getByRole("combobox", { name: "候選美術方向" })
        .selectOption("cartography");
      await shot(`candidate-cartography-${width}`);
      const geometry = await page
        .locator(".terrain-ground polygon[data-terrain]")
        .evaluateAll((es) =>
          es.map((e) => ({
            x: e.dataset.x,
            y: e.dataset.y,
            t: e.dataset.terrain,
            p: e.getAttribute("points"),
          })),
        );
      const hits = await page.locator("[data-cell]").evaluateAll((es) =>
        es.map((e) => ({
          key: e.dataset.cell,
          t: e.dataset.terrain,
          p: e.getAttribute("points"),
        })),
      );
      assert.equal(geometry.length, 99);
      assert.equal(hits.length, 99);
      for (const g of geometry)
        assert.deepEqual(
          hits.find((h) => h.key === `${g.x},${g.y}`),
          { key: `${g.x},${g.y}`, t: g.t, p: g.p },
        );
      const measure = await page.locator(".terrain-ground").evaluate((g) => {
        const r = g.getBoundingClientRect();
        return {
          width: r.width,
          ratio: r.width / innerWidth,
          left: r.left,
          right: r.right,
        };
      });
      assert(
        measure.ratio >= 0.7 && measure.left >= 0 && measure.right <= width,
        JSON.stringify(measure),
      );
      for (const name of [
        "確認移動與技能",
        "撤銷未確認操作",
        "確認護送抵達出口",
      ]) {
        const r = await page.getByRole("button", { name }).boundingBox();
        assert(r.y >= 0 && r.y + r.height <= page.viewportSize().height);
      }
      check(`geometry-and-width-${width}`, measure);
    }
  }
  if (mode === "after") {
    await page.setViewportSize({ width: 1280, height: 720 });
    await begin();
    const initialView = await page
      .locator(".tactical-board")
      .getAttribute("viewBox");
    await click("放大戰場");
    await click("鏡頭向右平移");
    assert.notEqual(
      await page.locator(".tactical-board").getAttribute("viewBox"),
      initialView,
    );
    // Locator clicks use the transformed polygon's screen centre, after camera changes.
    await cell(1, 6).click();
    assert(
      (await page.locator(".command-context").innerText()).includes("席恩"),
    );
    await click("聚焦角色");
    assert.equal(
      await page.locator('output[aria-label="鏡頭倍率"]').textContent(),
      "165%",
    );
    await click("適應戰場");
    assert.equal(
      await page.locator(".tactical-board").getAttribute("viewBox"),
      initialView,
    );
    const board = await page.locator(".tactical-board").boundingBox();
    await page.keyboard.down("Alt");
    await page.mouse.move(
      board.x + board.width / 2,
      board.y + board.height / 2,
    );
    await page.mouse.down();
    await page.mouse.move(
      board.x + board.width / 2 + 60,
      board.y + board.height / 2 + 20,
      { steps: 5 },
    );
    await page.mouse.up();
    await page.keyboard.up("Alt");
    assert.notEqual(
      await page.locator(".tactical-board").getAttribute("viewBox"),
      initialView,
    );
    await click("適應戰場");
    await page.keyboard.press("Escape");
    check(
      "camera-and-transformed-input",
      "Zoom, button pan, Alt drag, fit, focus and projected cell activation",
    );
    await preview();
    const untouched = await snapshot();
    await click("撤銷未確認操作");
    assert.deepEqual(await snapshot(), untouched);
    await page.keyboard.press("Escape");
    await preview();
    await page.getByRole("button", { name: "確認移動與技能" }).evaluate((b) => {
      b.click();
      b.click();
    });
    await waitStage("move");
    assert.deepEqual(await snapshot(), untouched);
    assert(
      (
        await unit("shien").locator("[data-pose]").getAttribute("data-pose")
      ).startsWith("1:"),
    );
    await waitStage("release");
    assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 6"));
    assert.equal(await unit("shien").getAttribute("data-y"), "6");
    await waitStage("impact");
    assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
    assert.equal(await unit("shien").getAttribute("data-y"), "4");
    await idle();
    assert(
      (await page.locator(".battle-controls").innerText()).includes(
        "已確認行動 1 次",
      ),
    );
    check(
      "physical-state-and-repeat-gate",
      "Real walk row, swing, exactly one damage/position/action update at Impact; duplicate click ignored; undo never mutates state",
    );
    await finish("residents");
    check(
      "complete-residents",
      "Modal focus trap/Esc/restore, branch consequence, campaign return",
    );
    await begin("grain", true);
    assert.equal(await unit("shien").count(), 0);
    assert.equal(await unit("olun").count(), 0);
    await preview(true, true);
    await tabTo(page.getByRole("button", { name: "確認移動與技能" }));
    await page.keyboard.press("Space");
    await idle();
    await finish("grain");
    check(
      "complete-grain-absent-keyboard",
      "Only Lida, real Tab/Enter/Space selection and confirmation, full consequence flow",
    );
    await begin();
    await preview();
    const baseline = await snapshot();
    await click("確認移動與技能");
    await waitStage("windup");
    await page.keyboard.press("Escape");
    await page.waitForTimeout(2300);
    assert.deepEqual(await snapshot(), baseline);
    check(
      "cancel-before-impact",
      "No HP, action or position changes after cancelled action",
    );
    await preview();
    await click("確認移動與技能");
    await waitStage("impact");
    await page.keyboard.press("Escape");
    await page.waitForTimeout(900);
    assert(
      (await page.locator(".battle-controls").innerText()).includes(
        "已確認行動 1 次",
      ),
    );
    assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
    check(
      "cancel-after-impact",
      "Applied effect retained once; no delayed duplicate",
    );
    await begin();
    await click("演出展示");
    const demoBaseline = await snapshot();
    for (const [name, kind] of [
      ["物理攻擊", "physical"],
      ["裂潮・光矢", "arcane"],
      ["封蠟・護印", "ward"],
      ["受擊示範", "hit"],
      ["裂潮・光矢", "arcane"],
    ]) {
      await click(name);
      if (kind !== "hit") {
        await waitStage("release");
        assert.equal(
          await page.locator("[data-effect]").getAttribute("data-effect"),
          kind,
        );
        assert(
          (
            await unit("shien").locator("[data-pose]").getAttribute("data-pose")
          ).startsWith(kind === "physical" ? "2:" : "4:"),
        );
      } else {
        await waitStage("impact");
        assert(
          (
            await unit("shien").locator("[data-pose]").getAttribute("data-pose")
          ).startsWith("3:"),
        );
      }
      await idle();
      assert.deepEqual(await snapshot(), demoBaseline);
    }
    assert(
      (await page.locator(".battle-controls").innerText()).includes(
        "已確認行動 0 次",
      ),
    );
    check(
      "four-clips-and-replay",
      "Actual sword/cast/recoil rows; two spell languages and recovery; replay never changes game state",
    );
    await click("裂潮・光矢");
    await waitStage("windup");
    await click("閱讀設定");
    await page.waitForTimeout(2400);
    await click(/完成 →/);
    await idle();
    assert.deepEqual(await snapshot(), demoBaseline);
    check(
      "navigation-cleanup",
      "Screen navigation cancels RAF; no late state change on return",
    );
    await begin();
    await preview();
    const navigationBaseline = await snapshot();
    await click("確認移動與技能");
    await waitStage("windup");
    await click("閱讀設定");
    await page.waitForTimeout(2300);
    await click(/完成 →/);
    assert.deepEqual(await snapshot(), navigationBaseline);
    assert(
      await page.getByRole("button", { name: "確認移動與技能" }).isDisabled(),
    );
    await preview();
    await click("確認移動與技能");
    await waitStage("impact");
    await click("閱讀設定");
    await page.waitForTimeout(700);
    await click(/完成 →/);
    assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
    assert(
      (await page.locator(".battle-controls").innerText()).includes(
        "已確認行動 1 次",
      ),
    );
    assert(
      await page.getByRole("button", { name: "確認移動與技能" }).isDisabled(),
    );
    check(
      "committed-navigation-before-after-impact",
      "Leaving before impact preserves state; leaving after impact retains one action and clears stale preview so it cannot repeat",
    );
    await page.emulateMedia({ reducedMotion: "reduce" });
    await begin();
    await preview();
    await click("確認移動與技能");
    await idle();
    assert.equal(await page.locator("[data-effect]").count(), 0);
    assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
    await shot("reduced-motion-1280");
    check(
      "reduced-motion",
      "Effects suppressed; exactly one accepted state update and accessible status",
    );
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await begin();
    await preview();
    await click("確認移動與技能");
    await waitStage("windup");
    await page.emulateMedia({ reducedMotion: "reduce" });
    await idle();
    assert(
      (await page.locator(".battle-controls").innerText()).includes(
        "已確認行動 1 次",
      ),
    );
    check(
      "mid-clip-motion-change",
      "Preference switch completes accepted action once without prolonged effects",
    );
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await begin();
    await click("閱讀設定");
    await page.getByRole("checkbox", { name: /放大文字/ }).check();
    await click(/完成 →/);
    await preview();
    assert(
      await page
        .locator(".command-context span")
        .evaluate((e) => parseFloat(getComputedStyle(e).fontSize) >= 18),
    );
    assert(
      await page
        .getByRole("button", { name: "確認移動與技能" })
        .evaluate((e) => parseFloat(getComputedStyle(e).fontSize) >= 18),
    );
    await shot("large-text-1280");
    await click("確認移動與技能");
    await idle();
    await finish("residents");
    check(
      "large-text",
      "720p enlarged text, scroll access, full flow and no horizontal overflow",
    );
    await begin();
    await click("閱讀設定");
    await page.getByRole("checkbox", { name: /放大文字/ }).uncheck();
    await click(/完成 →/);
    const perf = await page.evaluate(
      () =>
        new Promise((resolve) => {
          const gaps = [];
          let last = performance.now();
          const start = last;
          function frame(now) {
            gaps.push(now - last);
            last = now;
            if (now - start < 2200) requestAnimationFrame(frame);
            else {
              gaps.sort((a, b) => a - b);
              resolve({
                samples: gaps.length,
                median: gaps[Math.floor(gaps.length * 0.5)],
                p95: gaps[Math.floor(gaps.length * 0.95)],
              });
            }
          }
          requestAnimationFrame(frame);
        }),
    );
    check("idle-raf-observation", perf);
    await click("演出展示");
    await click("裂潮・光矢");
    const activePerf = await page.evaluate(
      () =>
        new Promise((resolve) => {
          const gaps = [];
          let last = performance.now();
          const start = last;
          function frame(now) {
            gaps.push(now - last);
            last = now;
            if (now - start < 1900) requestAnimationFrame(frame);
            else {
              gaps.sort((a, b) => a - b);
              resolve({
                samples: gaps.length,
                median: gaps[Math.floor(gaps.length * 0.5)],
                p95: gaps[Math.floor(gaps.length * 0.95)],
              });
            }
          }
          requestAnimationFrame(frame);
        }),
    );
    await idle();
    check("spell-raf-observation", activePerf);
    await page.goto("http://127.0.0.1:5174/tests/playback-harness.html", {
      waitUntil: "networkidle",
    });
    await click("Start");
    await click("Unmount React");
    await page.waitForTimeout(2400);
    assert.equal(await page.locator("#callbacks").innerText(), "0:0");
    check(
      "react-hook-unmount",
      "Real React root unmounted during clip; neither Impact nor Done fired afterwards",
    );
    for (const width of [1280, 1920]) await record(width);
    check("live-recordings", report.media);
    await begin();
    await click("戰鬥資訊");
    assert(await page.locator(".battle-sidebar").isVisible());
    await page.keyboard.press("Escape");
    assert.equal(await page.locator(".battle-sidebar").count(), 0);
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
    await shot("story-history-1920");
    await click(/收起對白紀錄/);
    await page.keyboard.press("Escape");
    for (const name of ["席恩", "莉妲", "奧倫", "瑪芮"]) {
      await page.getByRole("button", { name: new RegExp(`${name}.*`) }).click();
      await shot(`character-${name}-1920`);
    }
    check(
      "information-history-camp",
      "Information toggle/Esc, deployment/story return, dialogue history and four character views preserved",
    );
    await page.goto("http://127.0.0.1:5174/docs/vd2/comparison.html", {
      waitUntil: "networkidle",
    });
    await page.locator("#split").fill("35");
    await page.locator("#size").selectOption("1920");
    await page.locator("#play").click();
    await page.locator("#live").evaluate((image) => image.decode());
    check(
      "comparison-page",
      "Actual Before/After slider, both candidate images and 1080p live GIF load without failed resources",
    );
  }
  assert.deepEqual(errors, []);
  for (const [file, digest] of Object.entries(inputs))
    assert.equal(
      hash(fs.readFileSync(path.join(root, file))),
      digest,
      `Source changed: ${file}`,
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
  report.browser = await context.browser()?.version();
  fs.writeFileSync(
    path.join(output, "capture-record.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  await context.close();
}
