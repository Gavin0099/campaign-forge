import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { command, initialState, DEFAULT_CONFIG, resolve, key } from '../src/playable-l03/rules.ts';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path)); assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes); assert.equal(hash(fs.readFileSync(binding.path)),binding.sha256);
const {chromium}=await import('playwright');
const evidenceDir=process.argv.includes('--p1v5') ? 'ui-prototype/docs/playable-l03-p1v5/p1v3-regression' : process.argv.includes('--p1v4') ? 'ui-prototype/docs/playable-l03-p1v4/p1v3-regression' : 'ui-prototype/docs/playable-l03-p1v3';
const output=path.join(root,evidenceDir);
fs.mkdirSync(output,{recursive:true});
const scratch=path.join(root,'scratch/playable-l03-p1v3-browser');
fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const context=await chromium.launchPersistentContext(path.join(scratch,'profile'),{executablePath:binding.path,headless:true,viewport:{width:1280,height:720},env});
const url='http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*',route=>new URL(route.request().url()).origin===new URL(url).origin?route.continue():route.abort());
const page=context.pages()[0],checks=[],captures=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const sourceFiles=['PlayableL03.tsx','playable.css','presentation.tsx','rules.ts'].map(f=>`ui-prototype/src/playable-l03/${f}`)
  .concat(['ui-prototype/tests/playable-l03-p1v3-browser.mjs'],['terrain-v2.png','props-v2.png','ferry-scene-v2.png','l03-party-v1.png','l03-enemies-v1.png'].map(f=>`ui-prototype/public/art/${f}`));
const report={started_at:new Date().toISOString(),browser:binding,source_sha256:Object.fromEntries(sourceFiles.map(f=>[f,hash(fs.readFileSync(path.join(root,f)))])),checks,captures,errors,human_playtest:'HUMAN_PENDING'};
const state=()=>page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const initial=()=>initialState('open',{...DEFAULT_CONFIG,p0c:{survivalTurns:6}});
const settled=()=>page.waitForSelector('[data-p1v-busy="false"]');
const tile=p=>page.locator(`[data-p1v-cell="${key(p)}"]`);
function pass(name,detail={}){checks.push({name,...detail});console.log(`PASS ${checks.length}: ${name}`);}
async function load(size){
  await page.setViewportSize(size); await page.goto(url); await settled();
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(e=>e.getAttribute('href')))].map(src=>new Promise((done,fail)=>{const im=new Image();im.onload=done;im.onerror=fail;im.src=src;})));});
  assert.deepEqual(await state(),initial());
}
async function capture(name){
  const file=`after-${page.viewportSize().width}x${page.viewportSize().height}-${name}.png`;
  await page.screenshot({path:path.join(output,file)});
  captures.push({path:`${evidenceDir}/${file}`,sha256:hash(fs.readFileSync(path.join(output,file))),viewport:page.viewportSize(),state:await state(),frame:await page.locator('[data-p1v-frame]').getAttribute('data-p1v-frame')});
}
try {
  for(const size of [{width:1280,height:720},{width:1920,height:1080}]){
    await load(size);
    assert.equal(await page.locator('[data-p1v-landmark="winch"]').textContent(),'絞盤');
    assert.equal(await page.locator('.p1v-portrait').count(),5);
    assert.equal(await page.locator('.p1v-gauge:first-child .filled').count(),1);
    assert.equal(await page.locator('.p1v-gauge.danger .filled').count(),0);
    await page.getByLabel('開發資訊').check();
    assert.equal(await page.locator('[data-p1v-landmark="winch"]').textContent(),'絞盤 (2,1)');
    await page.getByLabel('開發資訊').uncheck();
    assert.deepEqual(await state(),initial());
    pass(`${size.width}: five original portraits, accurate gauges, debug toggle changes presentation only`);

    await page.locator('[data-p1v-select="lace"]').click();
    const destination={x:1,y:1}; await tile(destination).hover();
    const expected=command(initial(),{type:'move',turn:1,unit:'lace',to:destination});
    const pathText=expected.events.find(e=>e.type==='move').path.map(key).join(';');
    assert.equal(await page.locator('[data-p1v-move-path]').getAttribute('data-p1v-move-path'),pathText);
    assert.deepEqual(await state(),initial());
    await capture('path-preview');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('[data-p1v-move-path]').count(),0);
    await page.locator('[data-p1v-cell="1,3"]').focus();await page.keyboard.press('Space');
    await page.keyboard.press('ArrowUp'); await page.keyboard.press('ArrowUp');
    assert.equal(await page.locator('[data-p1v-move-path]').getAttribute('data-p1v-move-path'),pathText);
    // Observe on every frame before triggering the move: selector backoff polling
    // can skip the entire 180ms landing effect under concurrent browser load.
    const arrivalSeen=page.waitForFunction(()=>{
      const node=document.querySelector('.p1v-arrival');
      return node ? getComputedStyle(node).animationName : false;
    },undefined,{polling:'raf'});
    await page.keyboard.press('Space');
    assert.equal(await (await arrivalSeen).jsonValue(),'p1v-land');
    await settled(); assert.deepEqual(await state(),expected.state);
    await page.waitForTimeout(220); assert.equal(await page.locator('.p1v-arrival').count(),0);
    pass(`${size.width}: pointer/keyboard preview uses exact pure-rule path; Esc clears; arrival fires and returns to rest`);

    await load(size);
    await page.locator('[data-p1v-end]').click();
    await page.waitForSelector('[data-p1v-turn-banner="enemy"]');
    await page.waitForTimeout(160); await capture('enemy-turn-banner');
    assert.equal(await page.locator('[data-p1v-phase]').textContent(),'敵方回合');
    await settled();
    await page.waitForSelector('[data-p1v-turn-banner="ally"]');
    await page.waitForTimeout(160); await capture('ally-turn-banner');
    assert.deepEqual(await state(),resolve(initial(),1).state);
    await page.waitForTimeout(850);assert.equal(await page.locator('[data-p1v-turn-banner]').count(),0);
    assert.equal(await page.locator('[data-p1v-phase]').textContent(),'我方回合');
    pass(`${size.width}: enemy/ally banners follow actual playback, decay, and leave persistent phase; state unchanged`);

    await page.emulateMedia({reducedMotion:'reduce'});await load(size);
    await page.locator('[data-p1v-select="lace"]').click();
    const animations=await page.locator('.p1v-water-glint,.p1v-selection-ring').evaluateAll(nodes=>nodes.map(n=>getComputedStyle(n).animationName));
    assert(animations.length>1);assert(animations.every(n=>n==='none'));
    await tile(destination).click();await settled();
    assert.equal(await page.locator('.p1v-arrival').count(),0); assert.deepEqual(await state(),expected.state);
    await page.locator('[data-p1v-end]').click();await settled();
    assert.equal(await page.locator('[data-moving="true"]').count(),0);
    assert.equal(await page.locator('[data-p1v-turn-banner]').evaluate(e=>getComputedStyle(e).animationName),'none');
    assert.deepEqual(await state(),resolve(expected.state,1).state);
    pass(`${size.width}: reduced motion disables water/pulse/bounce/banner fades without changing results`);
    await page.emulateMedia({reducedMotion:'no-preference'});
  }
  assert.deepEqual(errors,[]);
  for(const [f,digest] of Object.entries(report.source_sha256))assert.equal(hash(fs.readFileSync(path.join(root,f))),digest,`source changed: ${f}`);
  pass('all new presentation source/asset hashes stable; no browser errors');report.exit_code=0;
} catch(e){report.exit_code=1;report.failure=e.stack;process.exitCode=1;console.error(e);await page.screenshot({path:path.join(scratch,'failure.png')}).catch(()=>{});}
finally{report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(output,'visual-results.json'),JSON.stringify(report,null,2)+'\n');await context.close();}
