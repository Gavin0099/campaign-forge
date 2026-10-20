const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '../..');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const nodeBinding = JSON.parse(fs.readFileSync(process.env.STORY_BINDING)).executables.node;
assert.equal(fs.realpathSync(nodeBinding.path), fs.realpathSync(process.execPath));
assert.equal(fs.statSync(nodeBinding.path).size, nodeBinding.size);
assert.equal(hash(fs.readFileSync(nodeBinding.path)), nodeBinding.sha256);
const binding = JSON.parse(fs.readFileSync(process.env.STORY_BROWSER_BINDING));
assert.equal(fs.realpathSync(binding.path), binding.path);
assert.equal(fs.statSync(binding.path).size, binding.bytes);
assert.equal(hash(fs.readFileSync(binding.path)), binding.sha256);
assert(path.isAbsolute(process.env.STORY_BROWSER_TOOLS));
const { chromium } = require(path.join(process.env.STORY_BROWSER_TOOLS, 'playwright'));
const output = path.join(root, 'docs/story/alignment/evidence');
const env = Object.fromEntries(['SystemRoot', 'WINDIR', 'SystemDrive', 'TEMP', 'TMP'].filter(k => process.env[k]).map(k => [k, process.env[k]]));
const samples = JSON.parse(fs.readFileSync(path.join(output, 'walk.json'))).samples;
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'scratch/story-playtest/manifest.json')));
const url = pathToFileURL(path.join(root, 'scratch/story-playtest/index.html')).href;
const checks = [], screenshots = [], errors = [];
async function capture(page, name) {
  const file = path.join(output, name);
  const bytes = await page.screenshot({ fullPage: true });
  fs.writeFileSync(file, bytes);
  screenshots.push({ file: name, sha256: hash(bytes), bytes: bytes.length });
}
(async () => {
  const browser = await chromium.launch({ executablePath: binding.path, headless: true, env });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, acceptDownloads: true });
    page.on('pageerror', e => errors.push(e.message));
    await page.route('**/*', route => new URL(route.request().url()).protocol === 'file:' ? route.continue() : route.abort());
    for (const width of [1280, 1920]) {
      await page.setViewportSize({ width, height: width === 1280 ? 720 : 1080 });
      await page.goto(url);
      await page.getByRole('button', { name: '寫下自己的名字，掛上燈芯。' }).waitFor();
      assert(await page.getByText('十年了，凱倫第一次推開這扇門。', { exact: false }).count());
      if (width === 1280) {
        const pairs = await page.evaluate(() => {
          const style = (selector) => getComputedStyle(document.querySelector(selector));
          return [
            ['body-text', style('article').color, style('main').backgroundColor, 4.5],
            ['speaker', style('.speaker').color, style('main').backgroundColor, 4.5],
            ['button', style('nav button:not(:disabled)').color, style('nav button:not(:disabled)').backgroundColor, 4.5],
            ['notice', style('.notice').color, style('html').backgroundColor, 4.5],
          ];
        });
        const luminance = rgb => rgb.match(/\d+/g).slice(0, 3).map(Number).map(n => n / 255).map(n => n <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4).reduce((sum, n, i) => sum + n * [.2126, .7152, .0722][i], 0);
        const measured = pairs.map(([name, fg, bg, threshold]) => { const a = luminance(fg), b = luminance(bg), ratio = (Math.max(a,b) + .05) / (Math.min(a,b) + .05); assert(ratio >= threshold, name + ': contrast ' + ratio); return { name, fg, bg, ratio, threshold }; });
        checks.push({ name: 'rendered-normal-text-contrast', measured, passed: true });
      }
      await capture(page, `reading-${width}.png`);
      checks.push({ name: `initial-${width}`, passed: true });
      const key = 'open|quin|sawin=true|public=false';
      for (const index of samples[key].route) {
        const choices = page.getByRole('region', { name: '目前選項' }).getByRole('button');
        await choices.nth(index).click();
      }
      await page.getByRole('heading', { name: '黎明之後', exact: true }).waitFor();
      assert(await page.getByText('托瑪拒絕收魂，仍不敢公開作證', { exact: true }).count());
      await capture(page, `ending-${width}.png`);
      const downloadPromise = page.waitForEvent('download');
      await page.getByRole('button', { name: '匯出選項紀錄' }).click();
      const download = await downloadPromise;
      const downloaded = JSON.parse(fs.readFileSync(await download.path()));
      assert.deepEqual(downloaded.route, samples[key].route);
      assert.equal(downloaded.sourceHash, manifest.sourceHash);
      assert.equal(downloaded.humanFeedback, null);
      await page.getByRole('button', { name: '回上個選項' }).click();
      assert.equal(await page.getByRole('region', { name: '目前選項' }).getByRole('button').count(), 3);
      await page.getByRole('button', { name: '撲向星盤。', exact: true }).click();
      assert(await page.getByText('保住星盤；小昆被帶走', { exact: true }).count());
      checks.push({ name: `actual-choice-buttons-export-undo-${width}`, passed: true });
    }
    for (const [key, sample] of Object.entries(samples)) {
      await page.goto(url + '?route=' + sample.route.join(',') + '&source=' + manifest.sourceHash);
      await page.getByRole('heading', { name: '黎明之後', exact: true }).waitFor();
      const gate = sample.state.k1_gate === 'open' ? '開閘：提歐生還，筆記沉河' : '封閘：保住筆記，提歐失蹤';
      assert(await page.getByText(gate, { exact: true }).count());
      const thoma = sample.state.thoma_public ? '托瑪拒絕收魂，並公開作證' : '托瑪拒絕收魂，仍不敢公開作證';
      assert(await page.getByText(thoma, { exact: true }).count());
      const loss = ({ quin: '小昆隨隊撤出；星盤被帶走', starplate: '保住星盤；小昆被帶走', sawin: '護住薩溫；小昆與星盤被帶走' })[sample.state.l07_protected];
      assert(await page.getByText(loss, { exact: true }).count());
      checks.push({ name: `replay:${key}`, passed: true });
    }
    await page.goto(url);
    await page.getByRole('button', { name: '寫下自己的名字，掛上燈芯。' }).waitFor();
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.textContent), '跳到故事');
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.textContent), '重新開始');
    const firstChoice = page.getByRole('region', { name: '目前選項' }).getByRole('button').first();
    await firstChoice.focus(); await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.activeElement.tagName === 'H2');
    assert.equal(await page.evaluate(() => document.activeElement.tagName), 'H2');
    checks.push({ name: 'keyboard-skip-disabled-button-order-enter-focus', passed: true });
    for (const width of [1280, 390]) {
      await page.setViewportSize({ width, height: 720 });
      await page.getByRole('button', { name: '重新開始' }).click();
      await page.getByRole('button', { name: '放大文字' }).click();
      await page.evaluate(() => document.documentElement.style.fontSize = '200%');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      const choices = page.getByRole('region', { name: '目前選項' }).getByRole('button');
      assert.equal(await choices.count(), 2);
      await choices.first().click();
      await capture(page, `reading-large-${width}.png`);
      await page.evaluate(() => document.documentElement.style.fontSize = '');
      await page.getByRole('button', { name: '放大文字' }).click();
      checks.push({ name: `enlarged-200-percent-reduced-motion-${width}`, passed: true });
    }
    await page.goto(url + '?route=999&source=' + manifest.sourceHash);
    await page.getByRole('alert').waitFor();
    assert(await page.getByRole('alert').innerText().then(t => t.includes('不相容')));
    await page.getByRole('button', { name: '重新開始' }).click();
    assert.equal(await page.getByRole('alert').count(), 0);
    checks.push({ name: 'invalid-replay-recovery', passed: true });
    await page.goto(url + '?route=0&source=stale');
    await page.getByRole('alert').waitFor();
    assert((await page.getByRole('alert').innerText()).includes('另一版'));
    checks.push({ name: 'stale-replay-version-rejection', passed: true });
    await page.goto(url);
    await page.getByRole('button', { name: '寫下自己的名字，掛上燈芯。' }).waitFor();
    await page.getByText('路線比較（含劇透）', { exact: true }).click();
    await page.getByRole('button', { name: '封閘／護薩溫／收留薩溫', exact: true }).click();
    assert(await page.getByText('護住薩溫；小昆與星盤被帶走', { exact: true }).count());
    checks.push({ name: 'route-picker-real-ui', passed: true });
    assert.deepEqual(errors, []);
    checks.push({ name: 'browser-console-errors', passed: true });
    const report = { checks, passed: checks.length, failed: 0, sourceHash: manifest.sourceHash, screenshots, browserVersion: browser.version(), errors, humanPlaytest: false };
    fs.writeFileSync(path.join(output, 'browser.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify({ passed: checks.length, failed: 0, screenshots: screenshots.length }));
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
