// Independent quality-review audit (read-only against app code).
// Usage: serve a build on 127.0.0.1:4317 (npx vite preview --port 4317), then
//   node tests/quality-review-audit.mjs
// Writes screenshots/quality-review/*.png and docs/quality-review/audit-report.json.
// Cell clicks use dispatchEvent so they are deterministic; this proves state logic,
// not pointer hit-testing or human usability.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const ui = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const shots = path.join(ui, "screenshots/quality-review");
const out = path.join(ui, "docs/quality-review/audit-report.json");
fs.mkdirSync(shots, { recursive: true });
fs.mkdirSync(path.dirname(out), { recursive: true });
const BASE = process.env.AUDIT_BASE || "http://127.0.0.1:4317/";
const sha = (f) =>
  crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");

const report = {
  started_at: new Date().toISOString(),
  commit: execSync("git rev-parse HEAD", { cwd: ui }).toString().trim(),
  dirty_src: execSync("git status --porcelain -- src public", { cwd: ui })
    .toString()
    .trim(),
  base_url: BASE,
  method:
    "Playwright headless Chromium; cell picks via dispatchEvent('click'). Agent observation, not human playtest.",
  checks: [],
  observations: {},
  captures: [],
  page_errors: [],
};
const check = (id, pass, detail) => {
  report.checks.push({ id, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"} ${id} — ${JSON.stringify(detail)}`);
};

const browser = await chromium.launch({
  executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  headless: true,
});
async function fresh(width = 1920, height = 1080, query = "") {
  const ctx = await browser.newContext({ viewport: { width, height } });
  await ctx.route("**/*", (r) =>
    new URL(r.request().url()).hostname === "127.0.0.1"
      ? r.continue()
      : r.abort(),
  );
  const page = await ctx.newPage();
  page.on("pageerror", (e) => report.page_errors.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error") report.page_errors.push(`console: ${m.text()}`);
  });
  await page.goto(BASE + query);
  await page.waitForLoadState("networkidle");
  return { ctx, page };
}
async function shot(page, name, note) {
  const file = path.join(shots, `${name}.png`);
  await page.waitForTimeout(250);
  await page.screenshot({ path: file });
  report.captures.push({ file: `screenshots/quality-review/${name}.png`, sha256: sha(file), note });
}
const idle = (page) =>
  page.waitForFunction(() => {
    const b = [...document.querySelectorAll("button")].find((x) => x.textContent?.includes("結束回合"));
    return b && !b.disabled;
  }, null, { timeout: 15000 });
const btn = (page, name) => page.getByRole("button", { name }).first();
const cell = (page, x, y) =>
  page.locator(`[data-cell="${x},${y}"]`).dispatchEvent("click");
const l03cell = (page, x, y) =>
  page.locator(`[data-l03-cell="${x},${y}"]`).dispatchEvent("click");

const mainMap = [
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
function bfs(start, rows, blocked, steps = 3, passable = (t) => t !== "~", enemyBlock = new Set()) {
  const seen = new Set([`${start.x},${start.y}`]);
  let frontier = [start];
  for (let s = 0; s < steps; s++) {
    const next = [];
    for (const p of frontier)
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const q = { x: p.x + dx, y: p.y + dy };
        const k = `${q.x},${q.y}`;
        const t = rows[q.y]?.[q.x];
        if (!t || !passable(t, q) || seen.has(k) || enemyBlock.has(k)) continue;
        seen.add(k);
        next.push(q);
      }
    frontier = next;
  }
  seen.delete(`${start.x},${start.y}`);
  for (const k of blocked) seen.delete(k);
  return seen;
}

async function toBattle(page, choiceTitle, deploy = null) {
  await btn(page, /開始展示／重設/).click();
  await btn(page, /前往營地/).click();
  await btn(page, /前往渡口事件/).click();
  await btn(page, new RegExp(choiceTitle)).click();
  if (deploy) {
    for (const name of ["席恩", "莉妲", "奧倫", "瑪芮"]) {
      const box = page.locator(".deploy-unit", { hasText: name }).locator("input");
      if (!(await box.count())) continue;
      const want = deploy.includes(name);
      if ((await box.isChecked()) !== want && (await box.isEnabled()))
        await box.click();
    }
  }
  await btn(page, /確認出發/).click();
  await page.waitForSelector("[data-cell]");
}
async function battleState(page) {
  return page.evaluate(() => ({
    objective: document.querySelector(".battle-controls strong")?.textContent,
    cells: [...document.querySelectorAll("[data-cell]")].map((c) =>
      c.getAttribute("aria-label"),
    ),
  }));
}
const moveCells = (page) =>
  page.$$eval(".move-cell", (els) => els.map((e) => e.getAttribute("data-cell")));
const hpOf = async (page, x, y) => {
  const label = await page.locator(`[data-cell="${x},${y}"]`).getAttribute("aria-label");
  const m = label?.match(/生命 (\d+)/);
  return m ? Number(m[1]) : null;
};

// ---------- A. First-play walkthrough (1920x1080) ----------
{
  const { ctx, page } = await fresh();
  await shot(page, "01-menu-1920", "首次進入的主選單");
  const menuText = await page.locator("main").innerText();
  await btn(page, /開始展示／重設/).click();
  const journeyText = await page.locator("main").innerText();
  await shot(page, "02-journey-1920", "旅程頁：首次玩家看到的任務說明");
  await btn(page, /前往營地/).click();
  const campText = await page.locator("main").innerText();
  await shot(page, "03-camp-1920", "營地");
  const campNext = page.locator("main button.primary").first();
  const campNextLabel = await campNext.innerText();
  await campNext.click();
  const storyText = await page.locator("main").innerText();
  await btn(page, /展開對白紀錄/).click();
  await shot(page, "04-story-log-1920", "劇情抉擇＋對白紀錄展開");
  await page.keyboard.press("Escape");
  const afterEsc = await page.locator("main h1").innerText();
  check("A1 Esc from story returns to camp", afterEsc.includes("火光"), { afterEsc });
  report.observations.first_five_minutes = {
    menu: menuText.slice(0, 400),
    journey: journeyText.slice(0, 600),
    camp_cta: campNextLabel,
    camp: campText.slice(0, 500),
    story: storyText.slice(0, 900),
  };
  await ctx.close();
}

// ---------- B. Choice → battle differences ----------
const states = {};
for (const [key, title] of [["residents", "先護送居民"], ["grain", "先護送軍糧"]]) {
  const { ctx, page } = await fresh();
  await toBattle(page, title);
  states[key] = await battleState(page);
  await shot(page, `05-battle-${key}-1920`, `戰鬥開場：${title}`);
  // finish with one action, no enemy defeated
  await cell(page, 2, 7); // 奧倫
  const mv = await moveCells(page);
  await cell(page, 2, 5);
  await cell(page, 2, 3); // 追兵
  await btn(page, /確認移動與技能/).click();
  await idle(page);
  const scoutHp = await hpOf(page, 2, 3);
  await btn(page, /確認護送抵達出口/).click();
  await btn(page, /確認完成此關/).click();
  const resultText = await page.locator("main").innerText();
  await shot(page, `06-result-${key}-1920`, `戰後結果：${title}，僅一次行動、未擊倒任何敵人`);
  report.observations[`result_${key}`] = { scoutHp, resultText: resultText.slice(0, 700), olun_moves: mv };
  check(`B-${key} result reachable after 1 action with enemies alive`, /渡口之後/.test(resultText) && scoutHp > 0, { scoutHp });
  await ctx.close();
}
const sameCells = JSON.stringify(states.residents.cells) === JSON.stringify(states.grain.cells);
report.observations.choice_battle_diff = {
  objective_residents: states.residents.objective,
  objective_grain: states.grain.objective,
  board_identical: sameCells,
};
check("B3 [design] residents vs grain board differs beyond text", !sameCells, { board_identical: sameCells });

// ---------- C. Movement legality (main battle) ----------
{
  const { ctx, page } = await fresh();
  await toBattle(page, "先護送居民");
  const units = { shien: [1, 6], lida: [1, 7], olun: [2, 7] };
  const occupied = new Set(["1,6", "1,7", "2,7", "2,3", "8,5"]);
  const illegal = {};
  for (const [id, [x, y]] of Object.entries(units)) {
    await cell(page, x, y);
    const shown = new Set(await moveCells(page));
    const legal = bfs({ x, y }, mainMap, occupied);
    illegal[id] = [...shown].filter((k) => !legal.has(k));
    await page.keyboard.press("Escape");
  }
  // move 奧倫 to (4,7) next to river, end turn, then inspect
  await cell(page, 2, 7);
  await cell(page, 4, 7);
  await cell(page, 2, 3);
  const canTarget = await btn(page, /確認移動與技能/).isEnabled();
  report.observations.olun_target_from_4_7 = canTarget;
  await page.keyboard.press("Escape");
  // second probe: walk 席恩 to the river edge (3,4) in two turns, then inspect range
  await cell(page, 1, 6); await cell(page, 2, 4); await cell(page, 2, 3);
  await btn(page, /確認移動與技能/).click();
  await idle(page);
  await btn(page, /結束回合/).click();
  await cell(page, 2, 4); await cell(page, 3, 4); await cell(page, 2, 3);
  await btn(page, /確認移動與技能/).click();
  await idle(page);
  await btn(page, /結束回合/).click();
  await cell(page, 3, 4);
  const fromEdge = new Set(await moveCells(page));
  const occ2 = new Set(["3,4", "1,7", "2,7", "8,5"]);
  const legal2 = bfs({ x: 3, y: 4 }, mainMap, occ2);
  illegal.shien_from_3_4 = [...fromEdge].filter((k) => !legal2.has(k));
  await shot(page, "07-main-move-range-river", "主流程：席恩在(3,4)河邊時顯示的移動範圍");
  const total = Object.values(illegal).flat().length;
  check("C1 main-battle move cells respect river (path, not Manhattan)", total === 0, illegal);
  await ctx.close();
}

// ---------- D. Adversarial state: double confirm, Esc before/after impact ----------
{
  const { ctx, page } = await fresh();
  await toBattle(page, "先護送居民");
  const hp0 = await hpOf(page, 2, 3);
  await cell(page, 2, 7);
  await cell(page, 2, 5);
  await cell(page, 2, 3);
  const confirm = btn(page, /確認移動與技能/);
  await confirm.click();
  await confirm.click({ force: true }).catch(() => {});
  await idle(page);
  const hp1 = await hpOf(page, 2, 3);
  check("D1 double confirm applies −3 once", hp0 - hp1 === 3, { hp0, hp1 });
  // Esc right after confirm (before impact)
  await cell(page, 1, 6);
  await cell(page, 1, 4);
  await cell(page, 2, 3);
  await confirm.click();
  await page.waitForTimeout(60);
  await page.keyboard.press("Escape");
  await idle(page);
  const hp2 = await hpOf(page, 2, 3);
  const shienAt = await page.locator('[data-cell="1,6"]').getAttribute("aria-label");
  check("D2 Esc before impact: no damage, actor not moved", hp2 === hp1 && /席恩/.test(shienAt), { hp1, hp2, shienAt });
  // settings during animation
  await cell(page, 1, 6);
  await cell(page, 1, 4);
  await cell(page, 2, 3);
  await confirm.click();
  await page.waitForTimeout(60);
  await page.getByRole("button", { name: "閱讀設定" }).click();
  await page.waitForTimeout(4500);
  const hp3 = await page.locator("main h1").innerText();
  await page.keyboard.press("Escape");
  await page.waitForSelector("[data-cell]");
  const hp4 = await hpOf(page, 2, 3);
  check("D3 opening settings mid-animation cancels without ghost damage", hp4 === hp2, { before: hp2, after: hp4, while_in_settings: hp3 });
  // Kill scout then check finish/end-turn behaviour with dead unit
  await btn(page, /結束回合/).click();
  await cell(page, 2, 7).catch(() => {});
  report.observations.after_adversarial_log = await page.locator(".event-log").innerText();
  await ctx.close();
}

// ---------- D2. Stray Esc in battle select phase ----------
{
  const { ctx, page } = await fresh();
  await toBattle(page, "先護送居民");
  await cell(page, 2, 7); await cell(page, 2, 5); await cell(page, 2, 3);
  await btn(page, /確認移動與技能/).click();
  await idle(page);
  const before = await hpOf(page, 2, 3);
  await page.keyboard.press("Escape");
  const where = await page.locator("main h1").innerText();
  await btn(page, /確認出發/).click();
  await page.waitForSelector("[data-cell]");
  const after = await hpOf(page, 2, 3);
  const actions = await page.locator(".battle-controls p").innerText();
  check("D4 one Esc in battle select phase keeps battle progress", after === before, { before, screen_after_esc: where, after_reenter: after, actions });
  await ctx.close();
}

// ---------- E. Absent companions: only 莉妲 ----------
{
  const { ctx, page } = await fresh();
  await toBattle(page, "先護送軍糧", ["莉妲"]);
  const labels = (await battleState(page)).cells.filter((l) => /席恩|奧倫|莉妲/.test(l));
  await cell(page, 1, 7);
  await cell(page, 2, 5);
  await cell(page, 2, 3);
  await btn(page, /確認移動與技能/).click();
  await idle(page);
  await btn(page, /確認護送抵達出口/).click();
  await btn(page, /確認完成此關/).click();
  const r = await page.locator("main").innerText();
  check("E1 solo 莉妲 route completes; absentees not on board", labels.length === 1 && /渡口之後/.test(r), { allyCells: labels });
  report.observations.solo_result = r.slice(0, 500);
  await ctx.close();
}

// ---------- F. 720p + large text ----------
{
  const { ctx, page } = await fresh(1280, 720);
  await toBattle(page, "先護送居民");
  await shot(page, "08-battle-720", "720p 主流程戰鬥");
  await page.getByRole("button", { name: "閱讀設定" }).click();
  const largeToggle = page.getByRole("checkbox").first();
  if (await largeToggle.count()) await largeToggle.check().catch(() => {});
  else await btn(page, /放大|文字/).click().catch(() => {});
  await page.keyboard.press("Escape");
  await shot(page, "09-battle-720-large", "720p＋放大文字");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  check("F1 720p large text no horizontal overflow", !overflow, { overflow });
  await ctx.close();
}

// ---------- G. L03 candidate ----------
const l03Rows = [
  "FFF.~~.....",
  "FF..~~.....",
  "F...~~..F..",
  "....~~.....",
  "...RRRRRR..",
  "....~~.....",
  "....~~...FF",
  "....~~..FFF",
  "....~~.FFFF",
];
for (const [gate, label] of [["open", "開閘接船"], ["sealed", "封閘護橋"]]) {
  const { ctx, page } = await fresh(1920, 1080, "?scene=l03");
  await page.waitForSelector("[data-l03-cell]");
  await btn(page, new RegExp(label)).click();
  const units = await page.$$eval("[data-l03-unit]", (els) =>
    els.map((e) => ({ id: e.getAttribute("data-l03-unit"), hp: e.getAttribute("data-hp") })),
  );
  await shot(page, `10-l03-${gate}-1920`, `L03 ${label} 開場`);
  // movement legality for 凱倫 at (2,5)
  await l03cell(page, 2, 5);
  const shown = await page.$$eval("[data-l03-cell].move", (els) => els.map((e) => e.getAttribute("data-l03-cell")));
  const occ = new Set(["0,2", "1,7", "3,3", "7,4"]);
  const legal = bfs({ x: 2, y: 5 }, l03Rows, occ, 3, (t, q) => t !== "~" && !(gate === "open" && q.y === 4 && (q.x === 4 || q.x === 5)));
  const bad = shown.filter((k) => k !== "2,5" && !legal.has(k));
  check(`G-${gate} L03 move cells respect river/bridge`, bad.length === 0, { bad });
  await page.keyboard.press("Escape");
  report.observations[`l03_${gate}`] = {
    units,
    objective: await page.locator(".l03-ledger h2").first().innerText(),
  };
  await ctx.close();
}
{
  const { ctx, page } = await fresh(1920, 1080, "?scene=l03");
  await page.waitForSelector("[data-l03-cell]");
  const hp = (id) => page.locator(`[data-l03-unit="${id}"]`).getAttribute("data-hp");
  // Defeat the knight (6hp) with two actions, then see whether anything ends.
  await l03cell(page, 2, 5); await l03cell(page, 3, 4); await l03cell(page, 3, 3);
  const commit = btn(page, /確認這次演出/);
  await commit.click();
  await commit.click({ force: true }).catch(() => {});
  await page.waitForTimeout(2000);
  const k1 = await hp("knight");
  await l03cell(page, 0, 2); await l03cell(page, 2, 2); await l03cell(page, 3, 3);
  await btn(page, /確認這次演出/).click();
  await page.waitForTimeout(2000);
  const k2 = await page.locator('[data-l03-unit="knight"]').count() ? await hp("knight") : "removed";
  const status = await page.locator(".l03-status").innerText();
  await shot(page, "11-l03-knight-defeated", "L03 擊倒議會騎士後：沒有勝利、敵方回合或目標進度變化");
  check("G1 L03 double confirm applies −3 once", Number(k1) === 3, { k1 });
  report.observations.l03_after_knight = { k2, status };
  // Esc before impact
  await btn(page, /下一輪預演/).click();
  const c0 = await hp("crawler");
  await l03cell(page, 2, 5); await l03cell(page, 4, 4).catch(() => {});
  await l03cell(page, 5, 4).catch(() => {});
  report.observations.l03_open_bridge_click = await page.locator(".l03-status").innerText();
  await page.keyboard.press("Escape");
  await l03cell(page, 1, 7); await l03cell(page, 1, 7); await l03cell(page, 2, 5);
  report.observations.l03_thoma_support_status = await page.locator(".l03-status").innerText();
  await page.keyboard.press("Escape");
  // Gate switch mid-animation
  await btn(page, /重設預演/).click();
  await l03cell(page, 2, 5); await l03cell(page, 3, 4); await l03cell(page, 3, 3);
  if (await page.locator(".l03-commit").first().isEnabled()) {
    await page.locator(".l03-commit").first().click();
    await page.waitForTimeout(80);
    await btn(page, /封閘護橋/).click();
    await page.waitForTimeout(1800);
    check("G2 gate switch mid-animation resets cleanly", (await hp("knight")) === "6", { knight: await hp("knight") });
  }
  report.observations.l03_crawler_hp = c0;
  // 720p + large text
  await page.setViewportSize({ width: 1280, height: 720 });
  await shot(page, "12-l03-720", "L03 720p");
  await btn(page, /放大文字/).click();
  await shot(page, "13-l03-720-large", "L03 720p 放大文字");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  check("G3 L03 720p large text no horizontal overflow", !overflow, { overflow });
  await ctx.close();
}

// ---------- H. Art gate smoke ----------
{
  const { ctx, page } = await fresh(1920, 1080, "?scene=art-gate");
  await page.waitForTimeout(800);
  await shot(page, "14-art-gate-a-1920", "art-gate A");
  await page.keyboard.press("Escape");
  report.observations.art_gate_text = (await page.locator("body").innerText()).slice(0, 600);
  await ctx.close();
}

report.finished_at = new Date().toISOString();
fs.writeFileSync(out, JSON.stringify(report, null, 2));
await browser.close();
console.log(`errors: ${report.page_errors.length}`);
