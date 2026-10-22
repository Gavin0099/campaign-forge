import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { initialState, DEFAULT_CONFIG, command, resolve } from '../src/playable-l03/rules.ts';

const root=path.resolve(import.meta.dirname,'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path)); assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes); assert.equal(hash(fs.readFileSync(binding.path)),binding.sha256);
const {chromium}=await import('playwright');
const output=path.join(root,'ui-prototype/docs/playable-l03-p1v5');
const scratch=path.join(root,'scratch/playable-l03-p1v5-browser');
fs.mkdirSync(output,{recursive:true});fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const context=await chromium.launchPersistentContext(path.join(scratch,'profile'),{executablePath:binding.path,headless:true,env,viewport:{width:1280,height:720}});
const url='http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(url).origin?r.continue():r.abort());
const page=context.pages()[0],checks=[],captures=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const sources=['PlayableL03.tsx','presentation.tsx','playable.css','rules.ts'].map(f=>`ui-prototype/src/playable-l03/${f}`).concat('ui-prototype/tests/playable-l03-p1v5-browser.mjs');
const report={started_at:new Date().toISOString(),browser:binding,source_sha256:Object.fromEntries(sources.map(f=>[f,hash(fs.readFileSync(path.join(root,f)))])),checks,captures,errors,human_playtest:'HUMAN_PENDING'};
const initial=()=>initialState('open',{...DEFAULT_CONFIG,p0c:{survivalTurns:6}});
const state=()=>page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const settled=()=>page.waitForSelector('[data-p1v-busy="false"]');
function pass(name,details={}){checks.push({name,...details});console.log(`PASS ${checks.length}: ${name}`);}
async function load(){await page.goto(url);await settled();await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(n=>n.getAttribute('href')))].map(async src=>{const i=new Image();i.src=src;await i.decode();}));});assert.deepEqual(await state(),initial());}
async function capture(name){const file=`1280x720-${name}.png`;await page.screenshot({path:path.join(output,file)});captures.push({path:`ui-prototype/docs/playable-l03-p1v5/${file}`,sha256:hash(fs.readFileSync(path.join(output,file))),state:await state()});}
async function turn(){const before=await state(),expected=resolve(before,before.turn);await page.locator('[data-p1v-end]').click();await settled();assert.deepEqual(await state(),expected.state);return expected;}
async function prime(){await page.getByLabel('跳過動畫').check();for(let i=0;i<3;i++)await turn();await page.getByLabel('跳過動畫').uncheck();}
async function blockSetup(){
  await page.getByLabel('跳過動畫').check();
  const rows=fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p0/success.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
  for(const {command:input} of rows.filter(r=>r.command).slice(0,6)){
    if(input.type==='resolve'){await turn();continue;}
    const before=await state(),expected=command(before,input);assert(expected.ok);
    await page.locator(`[data-p1v-select="${input.unit}"]`).click();
    await page.locator(`[data-p1v-cell="${input.to.x},${input.to.y}"]`).click();await settled();assert.deepEqual(await state(),expected.state);
  }
  await page.getByLabel('跳過動畫').uncheck();
}
try {
  await load();await prime();
  const seen=page.waitForFunction(()=>!!document.querySelector('[data-p1v-winch-feedback="2"]'),undefined,{polling:'raf'});
  await turn();await seen;
  await capture('winch-interference');
  assert.equal(await page.locator('.p1v-winch-jerk').count(),1);
  assert.equal(await page.locator('.p1v-winch-rope.taut').count(),1);
  assert.equal(await page.locator('.p1v-pip-flash').count(),2);
  assert.equal(await page.locator('.p1v-winch-warning').count(),1);
  assert.equal(await page.locator('[data-p1v-end]').isEnabled(),true);
  await page.waitForTimeout(750);
  assert.equal(await page.locator('[data-p1v-winch-feedback]').count(),0);
  assert.equal(await page.locator('.p1v-winch-jerk').count(),0);
  await capture('warning-2-of-3');
  pass('progress 0→2: jerk, wheel, taut rope, two flashes, pop; warning persists, feedback expires, input already unlocked');
  await turn();assert.equal(await page.locator('[data-p1v-result="failure"]').count(),1);
  assert.equal(await page.getByRole('button',{name:'重試'}).evaluate(e=>e===document.activeElement),true);
  await capture('defeat');await page.getByRole('button',{name:'重試'}).click();
  assert.deepEqual(await state(),initial());assert.equal(await page.locator('.p1v-winch-warning,[data-p1v-winch-feedback]').count(),0);
  pass('threshold crossing enters defeat immediately with Retry focus; Retry clears feedback and warning');
  for(const mode of ['skip','reduce']){
    await page.emulateMedia({reducedMotion:mode==='reduce'?'reduce':'no-preference'});await load();
    if(mode==='skip')await page.getByLabel('跳過動畫').check();
    await page.evaluate(()=>{window.fxSeen=false;window.fxObserver=new MutationObserver(()=>{if(document.querySelector('[data-p1v-winch-feedback],.p1v-winch-jerk,.p1v-winch-rope.taut'))window.fxSeen=true;});window.fxObserver.observe(document.querySelector('.p1v'),{subtree:true,childList:true,attributes:true});});
    for(let i=0;i<4;i++)await turn();
    assert.equal(await page.evaluate(()=>window.fxSeen),false);
    assert.equal(await page.locator('.p1v-winch-alert').evaluate(e=>getComputedStyle(e).animationName),'none');
    assert.equal((await state()).progress,2);
    pass(`${mode}: interference still resolves identically; no transient winch effects ever mount; warning stays static`);
  }
  await page.emulateMedia({reducedMotion:'no-preference'});
  await load();await blockSetup();
  const expectedBlock=resolve(await state(),3);assert(expectedBlock.events.some(e=>e.type==='intent' && e.reason==='blocked'));
  const blockSeen=page.waitForFunction(()=>!!document.querySelector('[data-p1v-block-feedback="knight-2"]'),undefined,{polling:'raf'});
  await turn();await blockSeen;await capture('body-block');
  assert.equal(await page.locator('[data-p1v-clash]').count(),1);
  assert.equal(await page.locator('.p1v-block-recoil').count(),1);
  assert.equal(await page.locator('[data-p1v-end]').isEnabled(),true);
  assert.deepEqual(await state(),expectedBlock.state);
  const cells=await page.locator('[data-p1v-cell]').evaluateAll(ns=>ns.map(n=>{const b=n.getBoundingClientRect();return document.elementFromPoint(b.x+b.width/2,b.y+b.height/2)?.getAttribute('data-p1v-cell')===n.getAttribute('data-p1v-cell');}));
  assert(cells.every(Boolean));
  await page.waitForTimeout(650);assert.equal(await page.locator('[data-p1v-block-feedback]').count(),0);
  pass('real success trace: blocked knight recoils, dust/status/spark appear, all tile hits stay stationary, no extra lock or rule displacement');
  // Continue the same real trace: its single contributor produces the requested 1/3 pop.
  await page.getByLabel('跳過動畫').check();await turn();await page.getByLabel('跳過動畫').uncheck();
  const oneSeen=page.waitForFunction(()=>!!document.querySelector('[data-p1v-winch-feedback="1"]'),undefined,{polling:'raf'});
  await turn();await oneSeen;await capture('winch-1-of-3');
  assert.equal(await page.locator('.p1v-pip-flash').count(),1);
  pass('single-contributor trace shows exactly 絞盤干擾 1/3 and one newly filled pip');
  for(const mode of ['skip','reduce']){
    await load();await blockSetup();
    if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await turn();assert.equal(await page.locator('[data-p1v-block-feedback],.p1v-block-recoil,.p1v-impact-scene').count(),0);
    pass(`${mode}: body-block result preserved without recoil, dust, spark, or shake`);
    await page.emulateMedia({reducedMotion:'no-preference'});
  }
  assert.deepEqual(errors,[]);
  for(const [file,digest] of Object.entries(report.source_sha256))assert.equal(hash(fs.readFileSync(path.join(root,file))),digest);
  report.exit_code=0;
}catch(e){report.exit_code=1;report.failure=e.stack;process.exitCode=1;console.error(e);await page.screenshot({path:path.join(output,'failure.png')}).catch(()=>{});}
finally{report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(output,'feedback-results.json'),JSON.stringify(report,null,2)+'\n');await context.close();}
