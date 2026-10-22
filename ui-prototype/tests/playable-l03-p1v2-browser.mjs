import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { command, DEFAULT_CONFIG, initialState, key } from '../src/playable-l03/rules.ts';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const binding = JSON.parse(fs.readFileSync(path.join(root, '.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path));
assert.equal(fs.realpathSync(binding.path), binding.path);
assert.equal(fs.statSync(binding.path).size, binding.bytes);
assert.equal(hash(fs.readFileSync(binding.path)), binding.sha256);
const { chromium } = await import('playwright');
const before = process.argv.includes('--before');
const phase = before ? 'before' : 'after';
const output = path.join(root, process.argv.includes('--p1v5') ? 'ui-prototype/docs/playable-l03-p1v5/p1v2-regression' : process.argv.includes('--p1v4') ? 'ui-prototype/docs/playable-l03-p1v4/p1v2-regression' : process.argv.includes('--p1v3') ? 'ui-prototype/docs/playable-l03-p1v3/p1v2-regression' : 'ui-prototype/docs/playable-l03-p1v2');
const scratch = path.join(root, 'scratch/playable-l03-p1v2-browser');
fs.mkdirSync(output, { recursive: true }); fs.mkdirSync(scratch, { recursive: true });
const env = Object.fromEntries(['SystemRoot', 'WINDIR', 'SystemDrive'].filter(k => process.env[k]).map(k => [k, process.env[k]]));
Object.assign(env, { TEMP: scratch, TMP: scratch });
const context = await chromium.launchPersistentContext(path.join(scratch, 'profile'), {
  executablePath: binding.path, headless: true, viewport: { width: 1280, height: 720 }, env,
});
const url = 'http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*', route => new URL(route.request().url()).origin === new URL(url).origin ? route.continue() : route.abort());
const page = context.pages()[0];
const checks = [], captures = [], errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
const sourceFiles = ['ui-prototype/src/playable-l03/PlayableL03.tsx', 'ui-prototype/src/playable-l03/playable.css',
  ...(process.argv.includes('--p1v3') || process.argv.includes('--p1v4') ? ['ui-prototype/src/playable-l03/presentation.tsx'] : []),
  'ui-prototype/src/playable-l03/rules.ts', 'ui-prototype/src/l03Scene.ts', 'ui-prototype/src/AnimatedActor.tsx',
  'ui-prototype/tests/playable-l03-p1v2-browser.mjs', 'ui-prototype/docs/playable-l03-p0/success.jsonl',
  ...['l03-party-v1.png','l03-enemies-v1.png'].map(f => `ui-prototype/public/art/${f}`)];
const report = { phase, started_at: new Date().toISOString(), browser: binding,
  source_sha256: Object.fromEntries(sourceFiles.map(f => [f, hash(fs.readFileSync(path.join(root,f)))])),
  checks, captures, errors, human_playtest: 'HUMAN_PENDING' };
const state = () => page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const settled = () => page.waitForSelector('[data-p1v-busy="false"]');
const initial = () => initialState('open', {...DEFAULT_CONFIG, p0c:{survivalTurns:6}});
const names = { karen:'凱倫', lace:'蕾絲', thoma:'托瑪', 'knight-1':'騎士一', 'knight-2':'騎士二' };
const overlap = (a,b) => Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>0.5 && Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>0.5;
async function load(size) {
  await page.setViewportSize(size); await page.goto(url); await settled();
  assert.deepEqual(await state(),initial());
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(e=>e.getAttribute('href')))].map(src=>new Promise((done,fail)=>{
      const bitmap=new Image(); bitmap.onload=done; bitmap.onerror=fail; bitmap.src=src;
    })));
  });
  await page.getByLabel('跳過動畫').check();
}
async function capture(name) {
  await page.mouse.move(8,8);
  const file = `${phase}-${page.viewportSize().width}x${page.viewportSize().height}-${name}.png`;
  await page.screenshot({path:path.join(output,file)});
  captures.push({path:path.relative(root,path.join(output,file)).replaceAll('\\','/'),sha256:hash(fs.readFileSync(path.join(output,file))),state:await state(),viewport:page.viewportSize()});
}
async function clickTile(cell, offset = {x:0,y:0}) {
  const tile=page.locator(`[data-p1v-cell="${key(cell)}"]`);
  const box=await tile.boundingBox(); assert(box);
  // Real pointer at projected tile centre (or an interior point), no force or DOM dispatch.
  const x=box.x+box.width/2+box.width*offset.x, y=box.y+box.height/2+box.height*offset.y;
  if (!before) assert.equal(await page.evaluate(({x,y})=>document.elementFromPoint(x,y)?.getAttribute('data-p1v-cell'),{x,y}),key(cell),'only the tile may receive the hit');
  await page.mouse.click(x,y);
}
async function verifyUnits(name) {
  const original=await state();
  const geometry=[];
  for (const unit of original.units) {
    for (const offset of [{x:0,y:0},{x:0,y:-.3},{x:.3,y:0},{x:0,y:.3},{x:-.3,y:0}]) {
      await clickTile(unit.cell,offset);
      assert.equal(await page.locator('[data-p1v-inspected]').getAttribute('data-p1v-inspected'),unit.id);
      assert.equal(await page.locator(`[data-p1v-cell="${key(unit.cell)}"]`).getAttribute('aria-pressed'),'true');
      const actionable=unit.side==='ally' && !original.moved.includes(unit.id);
      assert.equal(await page.locator('[data-p1v-selected]').getAttribute('data-p1v-selected'),actionable ? unit.id : '');
      assert.deepEqual(await state(),original,'inspection must never change rules');
    }
    await page.mouse.move(8,8); // persisted label, not hover-only
    const label=page.locator(`[data-p1v-label="${unit.id}"]`);
    assert(await label.isVisible()); assert((await label.textContent()).includes(names[unit.id]));
    const labelBox=await label.boundingBox(); assert(labelBox);
    assert(labelBox.x>=0 && labelBox.y>=0 && labelBox.x+labelBox.width<=page.viewportSize().width);
    // Nested SVG getBoundingClientRect includes the unclipped atlas image.
    // Measure its rendered, clipped viewport in screen coordinates instead.
    const figures=await page.locator('[data-p1v-figure]').evaluateAll(nodes=>nodes.map(n=>{
      const transform=n.parentNode.getScreenCTM();
      const a=new DOMPoint(n.x.baseVal.value,n.y.baseVal.value).matrixTransform(transform);
      const b=new DOMPoint(n.x.baseVal.value+n.width.baseVal.value,n.y.baseVal.value+n.height.baseVal.value).matrixTransform(transform);
      return {id:n.dataset.p1vFigure,box:{x:a.x,y:a.y,width:b.x-a.x,height:b.y-a.y}};
    }));
    for (const f of figures) {
      const own=original.units.find(u=>u.id===f.id);
      const tileBox=await page.locator(`[data-p1v-cell="${key(own.cell)}"]`).boundingBox();
      assert(Math.abs(f.box.y+f.box.height-(tileBox.y+tileBox.height/2))<.5,`${f.id} feet must anchor to its tile centre`);
      assert(Math.abs(f.box.x+f.box.width/2-(tileBox.x+tileBox.width/2))<.5,`${f.id} horizontal anchor`);
    }
    for (const f of figures) assert(!overlap(labelBox,f.box),`${unit.id} label overlaps ${f.id}`);
    assert(await label.evaluate(el=>{const b=el.getBoundingClientRect();return [[.1,.5],[.5,.5],[.9,.5]].every(([x,y])=>el.contains(document.elementFromPoint(b.x+b.width*x,b.y+b.height*y)));}),'label is covered');
    geometry.push({unit:unit.id,label:labelBox,figures});
  }
  const figures=geometry[0].figures;
  for (let a=0;a<figures.length;a++) for(let b=a+1;b<figures.length;b++) assert(!overlap(figures[a].box,figures[b].box),`figures overlap: ${figures[a].id}/${figures[b].id}`);
  const order=await page.locator('[data-p1v-unit]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.p1vUnit,x:n.transform.baseVal.consolidate().matrix.e,y:n.transform.baseVal.consolidate().matrix.f})));
  assert.deepEqual(order,[...order].sort((a,b)=>a.y-b.y || a.x-b.x || a.id.localeCompare(b.id)),'front units must paint last');
  checks.push({name:`${page.viewportSize().width}: ${name} — all five tiles selected/inspected at five interior points, names unobscured, figures separated, depth order`,geometry,order});
  console.log(`PASS ${checks.length}: ${checks.at(-1).name}`);
}
try {
  for (const size of [{width:1280,height:720},{width:1920,height:1080}]) {
    await load(size);
    // Initial Lace (1,3) / Thoma (1,4) are adjacent in a map column.
    if (!before) await verifyUnits('two units in a column');
    await capture('column');
    // Actual P0 success commands produce the tight diagonal by the winch.
    const commands=fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p0/success.jsonl'),'utf8').trim().split('\n').map(JSON.parse).flatMap(r=>r.command ? [r.command] : []);
    let expected=initial();
    for (const input of commands.slice(0,3)) {
      await page.locator(`[data-p1v-select="${input.unit}"]`).click();
      await clickTile(input.to); await settled();
      expected=command(expected,input).state; assert.deepEqual(await state(),expected);
    }
    // This is the exact cluster captured in the original P1v intent screenshot.
    if (!before) await verifyUnits('P0 winch cluster (1,1)/(2,2)/(3,3)');
    if (!before) await clickTile({x:2,y:2});
    await capture('winch');
    if (!before) {
      await page.locator('[data-p1v-cell="1,1"]').focus(); await page.keyboard.press('Space');
      assert.equal(await page.locator('[data-p1v-label="lace"]').count(),1);
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('[data-p1v-inspected]').getAttribute('data-p1v-inspected'),'');
      assert.equal(await page.locator('[data-p1v-label]').count(),0);
      checks.push({name:`${size.width}: keyboard inspection and Esc clear label`});
      await page.locator('[data-p1v-cell="1,1"]').hover();
      assert(await page.locator('[data-p1v-label="lace"]').isVisible());
      await page.mouse.move(8,8);
      assert.equal(await page.locator('[data-p1v-label]').count(),0);
      await page.evaluate(()=>document.documentElement.style.fontSize='32px');
      const beforeHover=await page.locator('.p1v-map').boundingBox();
      await clickTile({x:2,y:2});
      assert.equal(await page.locator('[data-p1v-inspected]').getAttribute('data-p1v-inspected'),'thoma');
      assert.deepEqual(await page.locator('.p1v-map').boundingBox(),beforeHover,'name changes must not move the tile under the pointer');
      const label=page.locator('[data-p1v-label="thoma"]');
      assert.equal(await label.evaluate(el=>getComputedStyle(el).fontSize),'32px');
      const labelBox=await label.boundingBox(), boardBox=await page.locator('.p1v-map').boundingBox();
      assert(!overlap(labelBox,boardBox),'200% name must remain outside the board');
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      await capture('text-200');
      await page.evaluate(()=>document.documentElement.style.fontSize='');
      checks.push({name:`${size.width}: hover clears on exit; name scales to 200% without covering board or horizontal overflow`});
    }
  }
  if (!before) {
    await load({width:1280,height:720});
    await page.getByLabel('跳過動畫').uncheck();
    await clickTile({x:1,y:3});
    await clickTile({x:1,y:1});
    await page.waitForFunction(()=>{
      const raw=document.querySelector('[data-p1v-frame]')?.dataset.p1vFrame;
      const f=raw ? JSON.parse(raw) : null; return f && f.progress>.2 && f.progress<.8;
    });
    const positions=await page.locator('[data-p1v-unit]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.p1vUnit,x:n.transform.baseVal.consolidate().matrix.e,y:n.transform.baseVal.consolidate().matrix.f})));
    assert.deepEqual(positions,[...positions].sort((a,b)=>a.y-b.y || a.x-b.x || a.id.localeCompare(b.id)));
    await settled();
    assert.deepEqual(await state(),command(initial(),{type:'move',turn:1,unit:'lace',to:{x:1,y:1}}).state);
    checks.push({name:'animated foot positions stay depth-sorted; final state equals unchanged pure command',positions});
  }
  assert.deepEqual(errors,[]);
  for(const [file,digest] of Object.entries(report.source_sha256)) assert.equal(hash(fs.readFileSync(path.join(root,file))),digest,`source changed: ${file}`);
  report.exit_code=0;
} catch(e) {
  report.exit_code=1; report.failure=e.stack; console.error(e); process.exitCode=1;
  await page.screenshot({path:path.join(scratch,`${phase}-failure.png`)}).catch(()=>{});
} finally {
  report.finished_at=new Date().toISOString();
  fs.writeFileSync(path.join(output,`${phase}-results.json`),JSON.stringify(report,null,2)+'\n');
  await context.close();
}
