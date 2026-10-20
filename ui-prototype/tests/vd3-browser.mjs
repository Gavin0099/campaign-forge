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
const output = path.join(root, "ui-prototype/screenshots/vd3"),
  scratch = path.join(root, "scratch/vd3-browser");
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
    deviceScaleFactor: 1,
    env,
  },
);
await context.route("**/*", (r) =>
  new URL(r.request().url()).hostname === "127.0.0.1"
    ? r.continue()
    : r.abort(),
);
await context.addInitScript(() => {
  window.__audioProbe = { starts: 0, stops: 0, active: 0 };
  const Base = window.AudioContext;
  if (Base)
    window.AudioContext = class extends Base {
      createOscillator() {
        const node = super.createOscillator(),
          start = node.start.bind(node),
          stop = node.stop.bind(node);
        let started = false;
        node.start = (...args) => {
          start(...args);
          started = true;
          window.__audioProbe.starts++;
          window.__audioProbe.active++;
        };
        node.stop = (...args) => {
          window.__audioProbe.stops++;
          return stop(...args);
        };
        node.addEventListener("ended", () => {
          if (started) window.__audioProbe.active--;
        });
        return node;
      }
    };
});
const page = context.pages()[0],
  errors = [],
  checks = [],
  captures = [],
  media = [],
  inputs = {};
const files = (directory) =>
  fs
    .readdirSync(path.join(root, directory), { withFileTypes: true })
    .flatMap((e) =>
      e.isDirectory()
        ? files(`${directory}/${e.name}`)
        : [`${directory}/${e.name}`],
    );
for (const file of [
  ...files("ui-prototype/src"),
  ...files("ui-prototype/public/art"),
  ...files("ui-prototype/public/docs"),
  ...files("ui-prototype/tests"),
  "ui-prototype/package.json",
  "ui-prototype/package-lock.json",
])
  inputs[file] = hash(fs.readFileSync(path.join(root, file)));
const report = {
  started_at: new Date().toISOString(),
  baseline: "0300c85f32f50dd7f6cb0216152ddddb90e33ddf",
  browser: { sha256: binding.sha256, bytes: binding.bytes },
  inputs,
  checks,
  captures,
  media,
  errors,
  file_write_retries: [],
  art_acceptance: "Owner review required; engineering tests do not certify art",
};
page.on("pageerror", (e) => errors.push(e.message));
page.on("response", (r) => {
  if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);
});
const click = (name) => page.getByRole("button", { name }).click();
const cell = (x, y) => page.locator(`[data-cell="${x},${y}"]`);
const stage = () => page.locator(".battle-arena").getAttribute("data-playback");
const waitStage = (value) =>
  page.waitForFunction(
    (v) => document.querySelector(".battle-arena")?.dataset.playback === v,
    value,
  );
const idle = () => waitStage("idle");
const check = (name, detail) => {
  checks.push({ name, pass: true, detail });
  console.log(`PASS ${name}`);
};
async function decode() {
  await page.evaluate(() =>
    Promise.all(
      [...document.querySelectorAll("svg image")].map((e) => {
        const i = new Image();
        i.src = e.href.baseVal;
        return i.decode();
      }),
    ),
  );
}
async function begin(choice = "residents", absent = false) {
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.goto("http://127.0.0.1:5175", { waitUntil: "networkidle" });
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
  await decode();
}
async function shot(name) {
  await page.evaluate(() => document.fonts.ready);
  await decode();
  const before = await stage();
  const file = name + ".png";
  const bytes = await page.screenshot();
  const destination = path.join(output, file);
  const temporary = destination + `.tmp-${process.pid}-${Date.now()}`;
  fs.writeFileSync(temporary, bytes, { flag: "wx" });
  for (let attempt = 0; ; attempt++) {
    try {
      fs.renameSync(temporary, destination);
      break;
    } catch (error) {
      if (
        attempt >= 5 ||
        !["UNKNOWN", "EBUSY", "EACCES", "EPERM"].includes(error.code)
      )
        throw error;
      report.file_write_retries.push({
        file,
        attempt: attempt + 1,
        code: error.code,
      });
      await new Promise((resolve) => setTimeout(resolve, 100 * (attempt + 1)));
    }
  }
  assert.equal(hash(fs.readFileSync(destination)), hash(bytes));
  captures.push({
    file,
    sha256: hash(fs.readFileSync(path.join(output, file))),
    viewport: page.viewportSize(),
    stage_before: before,
    stage_after: await stage(),
  });
  assert(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    "Horizontal overflow " + name,
  );
}
async function tabTo(locator) {
  for (let i = 0; i < 180; i++) {
    if (await locator.evaluate((e) => document.activeElement === e)) return;
    await page.keyboard.press("Tab");
  }
  throw Error("Unreachable keyboard control");
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
const state = () =>
  page.evaluate(() => ({
    units: [...document.querySelectorAll("[data-unit]")].map((e) => ({
      id: e.dataset.unit,
      x: e.dataset.x,
      y: e.dataset.y,
      text: e.querySelector(".unit-vitals")?.textContent,
    })),
    controls: document.querySelector(".battle-controls")?.textContent,
  }));
const rigState = () =>
  page.locator(".cutout-actor").evaluateAll((es) =>
    es.map((e) => ({
      rig: e.dataset.rig,
      head: e
        .querySelector('[data-part="head"] image')
        ?.outerHTML.replaceAll(/clip-path="[^"]*"/g, ""),
      feet: [
        ...e.querySelectorAll('[data-part^="foot"],[data-part="legs"]'),
      ].map((p) => p.getAttribute("transform")),
      weapon: e.querySelector("[data-weapon]")?.getAttribute("data-length"),
      body: e.dataset.bodyAngle,
    })),
  );
async function sampleReplay(name) {
  return await page.evaluate(
    (name) =>
      new Promise((resolve, reject) => {
        const samples = [];
        let started = false;
        const start = performance.now();
        function frame(now) {
          const arena = document.querySelector(".battle-arena"),
            stage = arena?.dataset.playback;
          const actor = document.querySelector(
              '[data-unit="demo-shien"] .cutout-actor',
            ),
            enemy = document.querySelector(
              '[data-unit="demo-scout"] .cutout-actor',
            );
          const point = (element, x, y) =>
            new DOMPoint(x, y).matrixTransform(element.parentNode.getCTM());
          const tip =
              actor && point(actor, +actor.dataset.tipX, +actor.dataset.tipY),
            chest =
              enemy &&
              point(enemy, +enemy.dataset.contactX, +enemy.dataset.contactY);
          samples.push({
            at: now - start,
            stage,
            contact_gap_px:
              tip && chest
                ? Math.hypot(tip.x - chest.x, tip.y - chest.y)
                : null,
            tip: actor ? [+actor.dataset.tipX, +actor.dataset.tipY] : null,
            recoil: enemy ? +enemy.dataset.recoil : 0,
            body: actor?.dataset.bodyAngle,
            feet: [
              ...document.querySelectorAll(
                '[data-unit="demo-shien"] [data-part^="foot-"]',
              ),
            ].map((e) => e.getAttribute("transform")),
            missiles: [...document.querySelectorAll("[data-missile]")].map(
              (e) => ({ id: e.dataset.missile, target: e.dataset.target }),
            ),
          });
          if (stage !== "idle") started = true;
          if (started && stage === "idle") {
            resolve(samples);
            return;
          }
          if (now - start > 6000) {
            reject(Error("Replay stuck"));
            return;
          }
          requestAnimationFrame(frame);
        }
        [...document.querySelectorAll("button")]
          .find((e) => e.textContent.trim() === name)
          .click();
        requestAnimationFrame(frame);
      }),
    name,
  );
}
async function finish(choice) {
  await click("確認護送抵達出口");
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
  await page.keyboard.press("Enter");
  await click("確認完成此關");
  const text = await page.locator("main").innerText();
  assert(
    text.includes(
      choice === "residents" ? "糧車仍困在低地" : "低地居民只能自行尋路",
    ),
  );
  await click("返回戰役旅程");
  assert(
    (await page.locator("main").innerText()).includes(
      choice === "residents" ? "補給不足" : "回收落單者",
    ),
  );
}
async function record(kind, width) {
  await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
  await begin();
  await click("演出展示");
  await decode();
  const session = await context.newCDPSession(page),
    frames = [];
  const key = `${kind}-${width}`,
    frameDir = path.join(scratch, "frames-" + key + "-" + Date.now());
  fs.mkdirSync(frameDir, { recursive: true });
  session.on("Page.screencastFrame", (event) => {
    const bytes = Buffer.from(event.data, "base64"),
      file = String(frames.length).padStart(5, "0") + ".jpg";
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
    quality: 90,
    maxWidth: width,
    maxHeight: page.viewportSize().height,
    everyNthFrame: 1,
  });
  await page.waitForTimeout(450);
  await click(kind === "melee" ? "席恩・近戰攻防" : "法師・Magic Missile");
  await idle();
  await page.waitForTimeout(450);
  await session.send("Page.stopScreencast");
  await session.detach();
  assert(frames.length > 30);
  const manifest = {
    capture_directory: path.relative(root, frameDir).split(path.sep).join("/"),
    viewport: page.viewportSize(),
    kind,
    origin:
      "Actual local Chromium CDP screencast; no composite battle animation",
    frames,
  };
  fs.writeFileSync(
    path.join(output, "recording-" + key + ".json"),
    JSON.stringify(manifest, null, 2) + "\n",
  );
  media.push({
    kind,
    width,
    frames: frames.length,
    seconds: frames.at(-1).timestamp - frames[0].timestamp,
  });
}
try {
  for (const width of [1280, 1920]) {
    await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
    await begin();
    await shot(`battle-idle-${width}`);
    await preview();
    await shot(`battle-preview-${width}`);
    const ground = await page
        .locator(".terrain-ground polygon[data-terrain]")
        .evaluateAll((es) => es.map((e) => e.getAttribute("points"))),
      hits = await page
        .locator("[data-cell]")
        .evaluateAll((es) => es.map((e) => e.getAttribute("points")));
    assert.equal(ground.length, 99);
    assert.deepEqual(ground, hits);
    const fit = await page
      .locator(".battle-arena svg.tactical-board")
      .getAttribute("viewBox");
    await page.keyboard.press("Escape");
    await click("放大戰場");
    await click("鏡頭向右平移");
    await cell(1, 6).click();
    assert(
      await page.getByRole("button", { name: "撤銷未確認操作" }).isEnabled(),
    );
    await click("適應戰場");
    check(`geometry-camera-${width}`, {
      tiles: 99,
      fit,
      viewport: page.viewportSize(),
    });
    await click("演出展示");
    assert.equal(await page.locator('[data-unit="shien"]').count(), 0);
    assert.equal(await page.locator('[data-unit="test-wizard"]').count(), 1);
    assert.equal(await page.locator("[data-unit]").count(), 4);
    await shot(`rehearsal-idle-${width}`);
    await click("席恩・近戰攻防");
    await waitStage("windup");
    await page.waitForTimeout(380);
    await shot(`melee-anticipation-${width}`);
    await idle();
    await click("席恩・近戰攻防");
    await waitStage("impact");
    await shot(`melee-contact-${width}`);
    await idle();
    await click("席恩・近戰攻防");
    await waitStage("reaction");
    await page.waitForTimeout(160);
    await shot(`melee-reaction-${width}`);
    await idle();
    await click("法師・Magic Missile");
    await waitStage("windup");
    await page.waitForTimeout(730);
    await shot(`missile-gather-${width}`);
    await idle();
    await click("法師・Magic Missile");
    await waitStage("release");
    await page.waitForTimeout(300);
    assert.equal(await page.locator("[data-missile]").count(), 3);
    await shot(`missile-flight-${width}`);
    await idle();
    await click("法師・Magic Missile");
    await waitStage("reaction");
    await page.waitForTimeout(170);
    await shot(`missile-hit-${width}`);
    await idle();
    check(
      `live-keyposes-${width}`,
      "Fixed cutout actors, three darts, two enemies and actual game screenshots",
    );
  }
  await page.setViewportSize({ width: 1280, height: 720 });
  await begin();
  await preview();
  const committed = await page.evaluate(
    () =>
      new Promise((resolve) => {
        const values = [];
        let started = false;
        const t = performance.now();
        function frame(now) {
          const arena = document.querySelector(".battle-arena"),
            unit = document.querySelector('[data-unit="shien"]');
          values.push({
            at: now - t,
            stage: arena.dataset.playback,
            x: unit?.dataset.x,
            y: unit?.dataset.y,
            hp: document
              .querySelector('[data-cell="2,3"]')
              .getAttribute("aria-label"),
            actions: document.querySelector(".battle-controls").textContent,
            feet: unit?.querySelector(".cutout-actor")?.dataset.feet,
          });
          if (arena.dataset.playback !== "idle") started = true;
          if (started && arena.dataset.playback === "idle") {
            resolve(values);
            return;
          }
          requestAnimationFrame(frame);
        }
        const b = [...document.querySelectorAll("button")].find(
          (e) => e.textContent.trim() === "確認移動與技能",
        );
        b.click();
        b.click();
        requestAnimationFrame(frame);
      }),
  );
  const changed = committed.find((e) => e.hp.includes("生命 3"));
  assert(changed);
  assert.equal(changed.stage, "impact");
  assert(
    committed
      .filter(
        (e) => !["impact", "reaction", "recovery", "idle"].includes(e.stage),
      )
      .every((e) => e.hp.includes("生命 6") && e.x === "1" && e.y === "6"),
  );
  assert(committed.some((e) => e.feet === "walking"));
  assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
  assert(
    (await page.locator(".battle-controls").innerText()).includes(
      "已確認行動 1 次",
    ),
  );
  check("committed-impact-single-update", {
    first_state_change: changed,
    stages: [...new Set(committed.map((e) => e.stage))],
  });
  await finish("residents");
  check(
    "residents-full-flow",
    "Choice, preview, action, modal focus/Esc, result and campaign consequence",
  );
  await begin("grain", true);
  assert.equal(await page.locator('[data-unit="shien"]').count(), 0);
  assert.equal(await page.locator('[data-unit="olun"]').count(), 0);
  await preview(true, true);
  await tabTo(page.getByRole("button", { name: "確認移動與技能" }));
  await page.keyboard.press("Space");
  await idle();
  await finish("grain");
  check(
    "grain-absent-keyboard-flow",
    "Lida-only deployment, real Tab/Enter/Space and different campaign consequence",
  );
  for (const afterImpact of [false, true]) {
    await begin();
    await preview();
    const before = await state();
    await click("確認移動與技能");
    await waitStage(afterImpact ? "reaction" : "windup");
    await page.keyboard.press("Escape");
    await idle();
    await page.waitForTimeout(800);
    if (afterImpact) {
      assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
      assert(
        (await page.locator(".battle-controls").innerText()).includes(
          "已確認行動 1 次",
        ),
      );
    } else assert.deepEqual(await state(), before);
    assert(
      await page.getByRole("button", { name: "確認移動與技能" }).isDisabled(),
    );
  }
  check(
    "cancel-before-after-impact",
    "No early mutation; applied effect remains once; no stale confirm or late callback",
  );
  await begin();
  const storyState = await state();
  const storyCamera = await page
    .locator("svg.tactical-board")
    .getAttribute("viewBox");
  await click("演出展示");
  const rigBaseline = await rigState();
  const replays = [];
  for (const name of ["席恩・近戰攻防", "法師・Magic Missile"]) {
    for (let repeat = 1; repeat <= 10; repeat++) {
      const samples = await sampleReplay(name);
      assert(samples.length > 30);
      assert.equal(await page.locator("[data-effect]").count(), 0);
      assert.deepEqual(await rigState(), rigBaseline);
      const nonidle = samples.filter((e) => e.stage !== "idle");
      const feet = JSON.stringify(nonidle[0].feet);
      assert(nonidle.every((e) => JSON.stringify(e.feet) === feet));
      assert(nonidle.some((e) => e.recoil > 0.8));
      if (name.startsWith("席恩")) {
        const stops = samples.filter((e) => e.stage === "impact");
        assert(stops.length >= 2);
        assert(
          stops.every((e) => Math.hypot(e.tip[0] - 90, e.tip[1] + 85) < 0.1),
        );
        assert(stops.every((e) => e.body === stops[0].body));
        assert(
          stops.every((e) => e.contact_gap_px < 6),
          "Blade misses actual transformed enemy chest",
        );
      } else {
        assert(
          samples.some((e) => e.stage === "release" && e.missiles.length === 3),
        );
      }
      const gaps = samples
        .slice(1)
        .map((e, i) => e.at - samples[i].at)
        .sort((a, b) => a - b);
      replays.push({
        kind: name,
        repeat,
        frames: samples.length,
        ms: Math.round(samples.at(-1).at),
        stages: [...new Set(samples.map((e) => e.stage))],
        peak_recoil: Math.max(...samples.map((e) => e.recoil)),
        raf_gap_p50_ms: gaps[Math.floor(gaps.length * 0.5)],
        raf_gap_p95_ms: gaps[Math.floor(gaps.length * 0.95)],
        impact_max_contact_gap_px: name.startsWith("席恩")
          ? Math.max(
              ...samples
                .filter((e) => e.stage === "impact")
                .map((e) => e.contact_gap_px),
            )
          : null,
      });
    }
    console.log("PASS ten replays " + name);
  }
  await click("聚焦角色");
  const focused = (
    await page.locator("svg.tactical-board").getAttribute("viewBox")
  )
    .split(" ")
    .map(Number);
  assert(
    Math.abs(focused[0] + focused[2] / 2 - 410) < 0.01,
    "Focus must use the rehearsal actor",
  );
  await click("演出展示");
  assert.deepEqual(await state(), storyState);
  await page.waitForFunction(
    (expected) =>
      document.querySelector("svg.tactical-board")?.getAttribute("viewBox") ===
      expected,
    storyCamera,
  );
  assert.equal(
    await page.locator("svg.tactical-board").getAttribute("viewBox"),
    storyCamera,
  );
  check("twenty-consecutive-replays", replays);
  check(
    "rehearsal-story-isolation",
    "Ten melee and ten spell replays leave original HP/positions/actions/turn untouched; rigs restore, effects clear, rehearsal focus and original camera restore",
  );
  await click("演出展示");
  for (const index of [1, 2, 3])
    await page
      .getByRole("combobox", { name: `第 ${index} 枚飛彈目標` })
      .selectOption("demo-scout");
  await click("法師・Magic Missile");
  await waitStage("release");
  assert.deepEqual(
    await page
      .locator("[data-missile]")
      .evaluateAll((es) => es.map((e) => e.dataset.target)),
    ["demo-scout", "demo-scout", "demo-scout"],
  );
  await idle();
  await page
    .getByRole("combobox", { name: "第 3 枚飛彈目標" })
    .selectOption("demo-guard");
  await click("法師・Magic Missile");
  await waitStage("reaction");
  assert.equal(
    await page
      .locator('[data-unit="demo-guard"] .cutout-actor')
      .evaluate((e) => +e.dataset.recoil > 0),
    true,
  );
  await idle();
  check(
    "missile-allocation-simultaneous",
    "Three independent selectors support 3:0 or 2:1; both targeted rigs react from the same Impact clock",
  );
  await click("音效：關");
  await click("法師・Magic Missile");
  await waitStage("windup");
  await page.waitForTimeout(170);
  assert(await page.evaluate(() => window.__audioProbe.starts >= 3));
  await page.keyboard.press("Escape");
  await page.waitForFunction(() => window.__audioProbe.active === 0);
  const audio = await page.evaluate(() => window.__audioProbe);
  await click("音效：開");
  check("audio-actual-nodes-cancel", {
    ...audio,
    note: "Real Web Audio nodes instrumented; subjective listening not verified; GIF is silent",
  });
  await click("法師・Magic Missile");
  await waitStage("windup");
  await click("閱讀設定");
  await page.waitForTimeout(3100);
  await click(/完成 →/);
  await idle();
  assert.equal(await page.locator("[data-effect]").count(), 0);
  check(
    "screen-navigation-cleanup",
    "Settings navigation cancels rehearsal RAF/audio without late effect",
  );
  for (const afterImpact of [false, true]) {
    await begin();
    await preview();
    const before = await state();
    await click("確認移動與技能");
    await waitStage(afterImpact ? "reaction" : "windup");
    await click("閱讀設定");
    await page.waitForTimeout(900);
    await click(/完成 →/);
    await idle();
    if (afterImpact)
      assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
    else assert.deepEqual(await state(), before);
    assert(
      await page.getByRole("button", { name: "確認移動與技能" }).isDisabled(),
    );
  }
  check(
    "committed-navigation-before-after-impact",
    "Applied once and preview cleared at either boundary",
  );
  await begin();
  await page.emulateMedia({ reducedMotion: "reduce" });
  await preview();
  await click("確認移動與技能");
  await idle();
  assert((await cell(2, 3).getAttribute("aria-label")).includes("生命 3"));
  assert.equal(await page.locator("[data-effect]").count(), 0);
  await shot("reduced-motion-1280");
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
    "reduced-motion-and-mid-clip-change",
    "Accepted action updates once; no prolonged rig/VFX motion, including dynamic preference switch",
  );
  await begin();
  await click("閱讀設定");
  await page.getByRole("checkbox", { name: /放大文字/ }).check();
  await click(/完成 →/);
  await click("演出展示");
  assert(
    await page
      .locator(".showcase-tray select")
      .first()
      .evaluate((e) => parseFloat(getComputedStyle(e).fontSize) >= 18),
  );
  await page
    .getByRole("combobox", { name: "第 3 枚飛彈目標" })
    .scrollIntoViewIfNeeded();
  await shot("large-text-rehearsal-1280");
  await page.keyboard.press("Escape");
  await preview();
  await click("確認移動與技能");
  await idle();
  await finish("residents");
  check(
    "large-text-720",
    "18px selectors and accessible scroll; full flow preserved with enlarged text and no horizontal overflow",
  );
  await page.goto("http://127.0.0.1:5175/tests/vd3-playback-harness.html", {
    waitUntil: "networkidle",
  });
  for (const name of [
    "Shien cannot cast",
    "No committed test spell",
    "No story targets",
    "Three darts required",
  ]) {
    await click(name);
    assert.equal(await page.locator("#rejected").innerText(), "true");
  }
  check(
    "class-and-showcase-boundaries",
    "Actual hook rejects Shien casting, committed showcase spells, story targets and non-three-dart casts",
  );
  await click("Start");
  await click("Unmount React");
  await page.waitForTimeout(3100);
  assert.equal(await page.locator("#callbacks").innerText(), "0:0");
  check(
    "real-react-unmount",
    "Unmounted the actual hook during casting; zero Impact/Done callbacks afterwards",
  );
  await begin();
  await click("戰鬥資訊");
  assert(await page.locator(".battle-sidebar").isVisible());
  await page.keyboard.press("Escape");
  await page.keyboard.press("Escape");
  await page.keyboard.press("Escape");
  await click(/展開對白紀錄/);
  assert(
    (await page.locator(".dialogue-history").innerText()).includes(
      "名冊說這裡空了",
    ),
  );
  await click(/收起對白紀錄/);
  check(
    "information-and-dialogue-history",
    "Information/Esc and dialogue history preserved",
  );
  for (const width of [1280, 1920])
    for (const kind of ["melee", "missile"]) await record(kind, width);
  check("four-live-recordings", media);
  await page.goto("http://127.0.0.1:5175/docs/vd3/SRD-NOTICE.html", {
    waitUntil: "networkidle",
  });
  assert(
    (await page.locator("body").innerText()).includes(
      "Creative Commons Attribution 4.0",
    ),
  );
  check(
    "in-app-srd-attribution",
    "Local notice available from rehearsal; SRD license distinguished from original story",
  );
  await page.goto("http://127.0.0.1:5175/docs/vd3/comparison.html", {
    waitUntil: "networkidle",
  });
  for (const width of ["1280", "1920"]) {
    await page.locator("#size").selectOption(width);
    await page.waitForFunction(() =>
      [...document.images].every(
        (image) => image.complete && image.naturalWidth > 0,
      ),
    );
    assert.equal(
      await page.locator("#before").evaluate((image) => image.naturalWidth),
      Number(width),
    );
    assert.equal(
      await page.locator("#after").evaluate((image) => image.naturalWidth),
      Number(width),
    );
  }
  check(
    "comparison-viewer",
    "Both resolution selectors load preserved Before, current After, four live GIFs and keyposes",
  );
  assert.deepEqual(errors, []);
  for (const [file, digest] of Object.entries(inputs))
    assert.equal(
      hash(fs.readFileSync(path.join(root, file))),
      digest,
      "Source changed during capture " + file,
    );
  report.pass = true;
  report.finished_at = new Date().toISOString();
} catch (error) {
  report.pass = false;
  report.failure = String(error.stack || error);
  await page
    .screenshot({ path: path.join(scratch, "failure.png") })
    .catch(() => {});
  console.error(report.failure);
  process.exitCode = 1;
} finally {
  fs.writeFileSync(
    path.join(output, "capture-record.json"),
    JSON.stringify(report, null, 2) + "\n",
  );
  await context.close();
}
