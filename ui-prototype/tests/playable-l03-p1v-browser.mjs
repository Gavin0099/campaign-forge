import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { command, DEFAULT_CONFIG, initialState, key, MAP, resolve } from '../src/playable-l03/rules.ts';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
// Match the existing browser harness: verify Chrome before importing its driver
// or creating a profile, use a private repo-local profile, block remote traffic.
const binding = JSON.parse(fs.readFileSync(path.join(root, '.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path));
assert.equal(fs.realpathSync(binding.path), binding.path);
assert.equal(fs.statSync(binding.path).size, binding.bytes);
assert.equal(hash(fs.readFileSync(binding.path)), binding.sha256);
const { chromium } = await import('playwright');
const output = path.join(root, process.argv.includes('--p1v4') ? 'ui-prototype/docs/playable-l03-p1v4/p1v-regression' : process.argv.includes('--p1v3')
  ? `ui-prototype/docs/playable-l03-p1v3/${process.argv.includes('--before') ? 'before' : 'p1v-regression'}` : process.argv.includes('--p1v2')
  ? 'ui-prototype/docs/playable-l03-p1v2/p1v-regression' : 'ui-prototype/docs/playable-l03-p1v');
const scratch = path.join(root, 'scratch/playable-l03-p1v-browser');
fs.mkdirSync(output, { recursive: true }); fs.mkdirSync(scratch, { recursive: true });
const env = Object.fromEntries(['SystemRoot', 'WINDIR', 'SystemDrive'].filter(k => process.env[k]).map(k => [k, process.env[k]]));
Object.assign(env, { TEMP: scratch, TMP: scratch });
const context = await chromium.launchPersistentContext(path.join(scratch, 'profile'), {
  executablePath: binding.path, headless: true, viewport: { width: 1280, height: 720 }, env,
});
const url = process.env.P1V_URL || 'http://127.0.0.1:5183/';
assert.equal(new URL(url).hostname, '127.0.0.1');
await context.route('**/*', route => new URL(route.request().url()).origin === new URL(url).origin ? route.continue() : route.abort());
const page = context.pages()[0];
const checks = [], captures = [], errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
const sourceFiles = ['ui-prototype/src/main.tsx', 'ui-prototype/src/AnimatedActor.tsx',
  ...((process.argv.includes('--p1v3') || process.argv.includes('--p1v4')) && !process.argv.includes('--before') ? ['ui-prototype/src/playable-l03/presentation.tsx'] : []),
  'ui-prototype/src/playable-l03/PlayableL03.tsx', 'ui-prototype/src/playable-l03/playable.css',
  'ui-prototype/src/playable-l03/rules.ts', 'ui-prototype/src/l03Scene.ts', 'ui-prototype/src/l03.css',
  'ui-prototype/tests/playable-l03-p1v-browser.mjs', 'ui-prototype/package.json', 'ui-prototype/package-lock.json',
  ...['l03-party-v1.png','l03-enemies-v1.png','terrain-v2.png'].map(f => `ui-prototype/public/art/${f}`),
  'ui-prototype/docs/playable-l03-p0/success.jsonl', 'ui-prototype/docs/playable-l03-p0/failure.jsonl'];
const report = { started_at: new Date().toISOString(), url, browser: binding,
  source_sha256: Object.fromEntries(sourceFiles.map(f => [f, hash(fs.readFileSync(path.join(root,f)))])),
  checks, captures, errors, human_playtest: 'HUMAN_PENDING' };
function pass(name, details = {}) { checks.push({name, ...details}); console.log(`PASS ${checks.length}: ${name}`); }
const getState = () => page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
// Unit artwork is noninteractive; use the owning tile for all pointer checks.
const unitTile = async id => page.locator(`[data-p1v-cell="${key((await getState()).units.find(u=>u.id===id).cell)}"]`);
const settled = () => page.waitForSelector('[data-p1v-busy="false"]');
const initial = () => initialState('open', {...DEFAULT_CONFIG, p0c:{survivalTurns:6}});
async function screenshot(name) {
  const file = `${name}.png`;
  await page.screenshot({path:path.join(output,file), fullPage:false});
  captures.push({path:path.relative(root,path.join(output,file)).replaceAll('\\','/'),sha256:hash(fs.readFileSync(path.join(output,file))),
    viewport:page.viewportSize(), state:await getState(), busy:await page.locator('[data-p1v-busy]').getAttribute('data-p1v-busy'),
    frame:await page.locator('[data-p1v-frame]').getAttribute('data-p1v-frame').then(v=>v ? JSON.parse(v) : null)});
}
async function load(size) {
  await page.setViewportSize(size); await page.goto(url);
  await page.getByRole('button',{name:'Playable L03 (P1v)'}).click();
  await settled(); assert.deepEqual(await getState(),initial());
  await page.evaluate(async () => {
    await document.fonts.ready;
    const sources=[...new Set([...document.querySelectorAll('svg image')].map(e=>e.getAttribute('href')))];
    await Promise.all(sources.map(src=>new Promise((done,fail)=>{
      const bitmap=new Image(); bitmap.onload=done; bitmap.onerror=()=>fail(new Error(`Art load failed: ${src}`)); bitmap.src=src;
    })));
    await new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done)));
  });
}
async function retry() {
  await page.getByRole('button',{name:'重試',exact:true}).click(); await settled();
  assert.deepEqual(await getState(),initial());
  assert.equal(await page.locator('[data-p1v-selected]').getAttribute('data-p1v-selected'),'');
  assert.equal(await page.locator('[data-p1v-waited]').getAttribute('data-p1v-waited'),'');
  assert.equal(await page.locator('[data-p1v-cell][data-legal="true"]').count(),0);
  assert.equal(await page.locator('[data-p1v-result]').count(),0);
  assert.equal(await page.locator('[data-moving="true"]').count(),0);
  assert.equal(await page.getByLabel('跳過動畫').isChecked(),false);
  assert.equal(await page.locator('[data-p1v-message]').textContent(),'選擇我方單位，再點亮格移動。');
}
const trace = name => fs.readFileSync(path.join(root,`ui-prototype/docs/playable-l03-p0/${name}.jsonl`),'utf8').trim().split('\n').map(JSON.parse).flatMap(r=>r.command ? [r.command] : []);
async function replay(name, skip, capturePrefix) {
  await page.getByLabel('跳過動畫').setChecked(skip);
  let expected = initial();
  const commands = trace(name);
  // The original five-turn trace is unchanged. A explicitly adds turn six.
  if (name === 'success') commands.push({type:'resolve',turn:6});
  for (const input of commands) {
    const next = command(expected,input); assert(next.ok,next.reason);
    if (input.type === 'move') {
      await page.locator(`[data-p1v-select="${input.unit}"]`).click();
      const actual = await page.locator('[data-p1v-cell][data-legal="true"]').evaluateAll(nodes=>nodes.map(n=>n.dataset.p1vCell).sort());
      const legal = MAP.rows.flatMap((row,y)=>[...row].map((_,x)=>({x,y}))).filter(to=>command(expected,{type:'move',turn:expected.turn,unit:input.unit,to}).ok).map(key).sort();
      assert.deepEqual(actual,legal);
      await page.locator(`[data-p1v-cell="${key(input.to)}"]`).click();
    } else {
      if (capturePrefix && input.turn === 1) await screenshot(`${capturePrefix}-intent`);
      await page.locator('[data-p1v-end]').click();
      if (capturePrefix && input.turn === 1) {
        if (process.argv.includes('--p1v3')) await screenshot(`${capturePrefix}-turn-banner`);
        await page.waitForFunction(()=>{
          const raw=document.querySelector('[data-p1v-frame]')?.dataset.p1vFrame;
          const f=raw ? JSON.parse(raw) : null;
          return f?.unit.startsWith('knight') && f.progress>.38 && f.progress<.75 &&
            document.querySelector('[data-p1v-unit^="knight"][data-moving="true"] [data-feet="walking"]');
        });
        await screenshot(`${capturePrefix}-mid-animation`);
        assert.equal(captures.at(-1).busy,'true','capture must be during actual animation');
        // A rapid keyboard repeat and even a forced click cannot resolve twice.
        await page.keyboard.press('Enter');
        await page.locator('[data-p1v-end]').click({force:true});
      }
    }
    await settled(); expected = next.state; assert.deepEqual(await getState(),expected);
  }
  assert.equal(expected.status,name === 'success' ? 'success' : 'failure');
  await page.getByRole('dialog').waitFor();
  assert.equal(await page.getByRole('button',{name:'重試',exact:true}).evaluate(e=>e===document.activeElement),true);
  await page.keyboard.press('Tab');
  assert.equal(await page.getByRole('button',{name:'重試',exact:true}).evaluate(e=>e===document.activeElement),true);
  return expected;
}
try {
  for (const size of [{width:1280,height:720},{width:1920,height:1080}]) {
    const prefix=`${size.width}x${size.height}`;
    await load(size);
    assert.equal(await page.locator('[data-p1v-cell]').count(),99);
    assert.equal(await page.locator('[data-p1v-unit]').count(),5);
    assert.equal(await page.locator('[data-p1v-intent]').count(),2);
    assert.equal(await page.locator('[data-p1v-intent-path]').count(),2);
    assert(await page.getByText(/^絞盤(?: \(2,1\))?$/).isVisible());
    const layout = await page.evaluate(()=>({width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,
      controls:document.querySelector('.p1v-controls').getBoundingClientRect().toJSON()}));
    assert(layout.scrollWidth<=size.width); assert(layout.controls.bottom<=size.height+1,JSON.stringify(layout));
    await screenshot(`${prefix}-start`);
    pass(`${prefix}: new menu entry, 99 cells, five units, winch, counters, two intent paths; controls fit viewport`);
    const original = await getState();
    await page.locator('[data-p1v-cell="4,0"]').click();
    assert.match(await page.locator('[data-p1v-message]').textContent(),/無法移動/);
    await (await unitTile('knight-1')).click();
    assert.match(await page.locator('[data-p1v-message]').textContent(),/敵方單位無法操作/);
    await page.locator('[data-p1v-select="lace"]').click();
    assert(await page.locator('[data-p1v-cell][data-legal="true"]').count()>0);
    await (await unitTile('thoma')).click();
    assert.deepEqual(await getState(),original);
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('[data-p1v-cell][data-legal="true"]').count(),0);
    await (await unitTile('lace')).click();
    assert.equal(await page.locator('[data-p1v-selected]').getAttribute('data-p1v-selected'),'lace');
    await page.keyboard.press('Escape');
    pass(`${prefix}: illegal water/enemy clicks rejected; occupied ally selects, no state mutation; Esc clears range`);
    await page.locator('[data-p1v-select="lace"]').click();
    await screenshot(`${prefix}-move-range`);
    await page.locator('[data-p1v-cell="0,2"]').click(); await settled();
    assert.deepEqual(await getState(),command(initial(),{type:'move',turn:1,unit:'lace',to:{x:0,y:2}}).state);
    await load(size);
    pass(`${prefix}: highlighted destination behind selected portrait accepts a real pointer click`);

    const animatedSuccess = await replay('success',false,prefix);
    await screenshot(`${prefix}-victory`); await retry();
    pass(`${prefix}: original P0 hold trace + sixth turn wins under A; legal ranges match rules; retry clears all state`);
    const skippedSuccess = await replay('success',true);
    assert.deepEqual(skippedSuccess,animatedSuccess); await retry();
    pass(`${prefix}: skipped victory equals animated victory exactly`);
    const animatedFailure = await replay('failure',false);
    await screenshot(`${prefix}-defeat`); await retry();
    const skippedFailure = await replay('failure',true);
    assert.deepEqual(skippedFailure,animatedFailure); await retry();
    pass(`${prefix}: original P0 idle trace loses; animated/skip states identical; retry clears defeat`);

    // Keyboard selection/movement, local wait, auto-repeat guard, and full turn.
    await page.locator('[data-p1v-cell="1,3"]').focus(); await page.keyboard.press('Space');
    await page.keyboard.press('ArrowUp'); await page.keyboard.press('ArrowUp'); await page.keyboard.press('Space'); await settled();
    let keyboardExpected=command(initial(),{type:'move',turn:1,unit:'lace',to:{x:1,y:1}}).state;
    assert.deepEqual(await getState(),keyboardExpected);
    await (await unitTile('lace')).click();
    assert.match(await page.locator('[data-p1v-message]').textContent(),/已行動/);
    await page.locator('[data-p1v-select="thoma"]').click(); await page.getByRole('button',{name:'等待',exact:true}).click();
    assert(await page.locator('[data-p1v-select="thoma"]').isDisabled());
    await page.locator('[data-p1v-cell="1,3"]').focus(); await page.keyboard.press('Enter'); await settled();
    keyboardExpected=resolve(keyboardExpected,1).state; assert.deepEqual(await getState(),keyboardExpected);
    assert.equal(await page.locator('[data-p1v-waited]').getAttribute('data-p1v-waited'),'');
    pass(`${prefix}: keyboard Space/arrows move; repeat move rejected; Wait consumes only local action; Enter ends one turn`);
  }
  // Mid-play skip and prefers-reduced-motion settle the SAME pending result.
  await load({width:1280,height:720});
  await page.locator('[data-p1v-end]').click(); await page.waitForSelector('[data-p1v-busy="true"]');
  await page.getByLabel('跳過動畫').check(); await settled();
  assert.deepEqual(await getState(),resolve(initial(),1).state);
  await page.waitForTimeout(350); assert.deepEqual(await getState(),resolve(initial(),1).state);
  pass('mid-animation skip settles once; cancelled RAF cannot apply another result');
  await load({width:1280,height:720});
  await page.locator('[data-p1v-end]').click(); await page.waitForSelector('[data-p1v-busy="true"]');
  await page.emulateMedia({reducedMotion:'reduce'}); await settled();
  assert.deepEqual(await getState(),resolve(initial(),1).state);
  await page.locator('[data-p1v-end]').click(); await settled();
  assert.equal(await page.locator('[data-feet="walking"]').count(),0);
  pass('reduced-motion change settles pending result; subsequent turns use no walking animation');
  await page.emulateMedia({reducedMotion:'no-preference'});
  await load({width:1280,height:720}); await page.getByLabel('跳過動畫').check();
  await page.locator('[data-p1v-end]').dblclick(); await settled();
  assert.deepEqual(await getState(),resolve(initial(),1).state);
  await page.locator('[data-p1v-end]').focus();
  await page.keyboard.down('Enter'); await settled();
  const beforeRepeat=await getState();
  await page.keyboard.down('Enter'); await page.keyboard.up('Enter');
  assert.deepEqual(await getState(),beforeRepeat); assert.equal(beforeRepeat.turn,3);
  pass('skip enabled: double-click resolves once; held Enter auto-repeat cannot advance another turn');
  await load({width:1280,height:720}); await page.locator('[data-p1v-end]').click();
  await page.waitForSelector('[data-p1v-busy="true"]'); await page.getByRole('button',{name:'返回選單',exact:true}).click();
  await page.waitForTimeout(350);
  assert(await page.getByRole('button',{name:'Playable L03 (P1v)'}).evaluate(e=>e===document.activeElement));
  await page.keyboard.press('Enter'); await settled(); assert.deepEqual(await getState(),initial());
  pass('exit during animation cancels playback; focus returns to entry; reopen starts clean');
  await page.evaluate(()=>document.documentElement.style.fontSize='32px');
  assert.equal(await page.locator('main.p1v').evaluate(e=>getComputedStyle(e).fontSize),'32px');
  assert(await page.locator('[data-p1v-end]').isVisible());
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.locator('[data-p1v-end]').scrollIntoViewIfNeeded(); await page.locator('[data-p1v-end]').click(); await settled();
  assert.equal((await getState()).turn,2);
  await screenshot('1280x720-text-200');
  pass('200% text remains operable with vertical scrolling and no horizontal overflow');
  await page.evaluate(()=>document.documentElement.style.fontSize='');
  await load({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.locator('[data-p1v-end]').scrollIntoViewIfNeeded(); await page.locator('[data-p1v-end]').click(); await settled();
  assert.equal((await getState()).turn,2);
  pass('390px fallback stacks panels; End Turn reachable without horizontal scrolling');
  await page.setViewportSize({width:1280,height:720});
  await page.goto(new URL('?scene=playable-l03',url).href); await settled();
  assert.deepEqual(await getState(),initial());
  pass('direct ?scene=playable-l03 entry starts A without changing the menu default');
  await page.goto(url); await page.getByRole('button',{name:/碑誓 · L03 戰鬥畫面/}).click();
  assert.equal(await page.locator('[data-l03-cell]').count(),99);
  assert.equal(await page.locator('[data-p1v-state]').count(),0);
  pass('existing L03 preview still opens independently with its original grid');
  // Required project regression paths in the same build, without overwriting
  // the older L03/art-gate evidence or changing their implementation.
  for (const choice of ['residents','grain']) {
    const click = name => page.getByRole('button',{name}).click();
    await page.goto(url); await click(/繼續旅程/); await click(/前往營地/); await click(/前往渡口事件/);
    if (choice === 'residents') {
      await click(/展開對白紀錄/); assert(await page.locator('.dialogue-history').isVisible());
      await click(/收起對白紀錄/); assert.equal(await page.locator('.dialogue-history').count(),0);
    }
    await click(choice === 'residents' ? /先護送居民/ : /先護送軍糧/);
    if (choice === 'grain') {
      await page.getByRole('checkbox',{name:/席恩/}).uncheck(); await page.getByRole('checkbox',{name:/奧倫/}).uncheck();
      await page.getByRole('combobox').selectOption('1');
    }
    await click(/確認出發/);
    const tile = (x,y) => page.locator(`[data-cell="${x},${y}"]`);
    await tile(1,choice === 'residents' ? 6 : 7).click(); await tile(1,4).click(); await tile(2,3).click();
    await page.keyboard.press('Escape');
    await tile(1,choice === 'residents' ? 6 : 7).click(); await tile(1,4).click(); await tile(2,3).click();
    await click('確認移動與技能');
    await page.waitForFunction(()=>document.querySelector('.battle-arena')?.dataset.playback === 'idle');
    await click('確認護送抵達出口'); await page.getByRole('dialog').getByRole('button',{name:/確認/}).click();
    await page.getByRole('button',{name:/返回戰役/}).waitFor(); await click(/返回戰役/);
    pass(`legacy ${choice}: story choice, ${choice === 'grain' ? 'absent allies / solo deployment, ' : 'dialogue log, '}move/skill preview, Esc cancel, confirm, result to campaign`);
  }
  for (const [file,digest] of Object.entries(report.source_sha256)) assert.equal(hash(fs.readFileSync(path.join(root,file))),digest,`source changed during browser verification: ${file}`);
  pass('source and art hashes unchanged for the complete browser run');
  assert.deepEqual(errors,[]); pass('no page errors or failed HTTP responses');
  report.finished_at = new Date().toISOString(); report.exit_code = 0;
} catch (e) {
  report.exit_code=1; report.failure=e.stack; console.error(e);
  console.error(await page.locator('.p1v-header,.p1v-objective,.p1v-layout,.p1v-board,.p1v-map,.p1v-sidebar,.p1v-controls,.p1v-sidebar h2').evaluateAll(nodes=>nodes.map(n=>({cls:n.className.baseVal||n.className,height:n.getBoundingClientRect().height,style:getComputedStyle(n).height,pad:getComputedStyle(n).padding,margin:getComputedStyle(n).margin,font:getComputedStyle(n).fontSize}))));
  await page.screenshot({path:path.join(scratch,'failure.png')}).catch(()=>{});
  process.exitCode=1;
} finally {
  fs.writeFileSync(path.join(output,'browser-results.json'),JSON.stringify(report,null,2)+'\n');
  await context.close();
}
