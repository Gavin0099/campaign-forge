import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { initialState, DEFAULT_CONFIG, command, resolve } from '../src/playable-l03/rules.ts';

const root=path.resolve(import.meta.dirname,'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path));assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes);assert.equal(hash(fs.readFileSync(binding.path)),binding.sha256);
const {chromium}=await import('playwright');
const evidenceDir='ui-prototype/docs/playable-l03-p1v7',output=path.join(root,evidenceDir);
const scratch=path.join(root,'scratch/playable-l03-p1v7-browser');
fs.mkdirSync(output,{recursive:true});fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const context=await chromium.launchPersistentContext(path.join(scratch,'profile'),{executablePath:binding.path,headless:true,env,viewport:{width:1280,height:720}});
const url='http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(url).origin?r.continue():r.abort());
const page=context.pages()[0],checks=[],captures=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const sources=['feedback.ts','PlayableL03.tsx','presentation.tsx','playable.css','rules.ts'].map(f=>`ui-prototype/src/playable-l03/${f}`)
  .concat('ui-prototype/tests/playable-l03-p1v7-browser.mjs','ui-prototype/tests/playable-l03-p1v7-feedback.mjs');
const report={started_at:new Date().toISOString(),browser:binding,source_sha256:Object.fromEntries(sources.map(f=>[f,hash(fs.readFileSync(path.join(root,f)))])),checks,captures,errors,human_playtest:'HUMAN_PENDING'};
const initial=()=>initialState('open',{...DEFAULT_CONFIG,p0c:{survivalTurns:6}});
const state=()=>page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const settled=()=>page.waitForSelector('[data-p1v-busy="false"]');
const transient='[data-p1v-footstep],[data-p1v-winch-feedback],[data-p1v-block-feedback],[data-p1v-clash],[data-p1v-confirm],.p1v-winch-jerk';
const baselineFile=path.join(root,'ui-prototype/src/playable-l03/.p1v7-baseline.tsx');
function pass(name,details={}){checks.push({name,...details});console.log(`PASS ${checks.length}: ${name}`);}
async function load(){await page.emulateMedia({reducedMotion:'no-preference'});await page.goto(url);await settled();
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(n=>n.getAttribute('href')))].map(async src=>{const i=new Image();i.src=src;await i.decode();}));});assert.deepEqual(await state(),initial());}
async function turn(){const before=await state(),expected=resolve(before,before.turn);await page.locator('[data-p1v-end]').click();await settled();assert.deepEqual(await state(),expected.state);return expected;}
async function prime(){await page.getByLabel('跳過動畫').check();for(let i=0;i<3;i++)await turn();await page.getByLabel('跳過動畫').uncheck();}
async function blockSetup(count=8){
  await page.getByLabel('跳過動畫').check();
  const rows=fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p0/success.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
  for(const {command:input} of rows.filter(r=>r.command).slice(0,count)){
    if(input.type==='resolve'){await turn();continue;}
    const expected=command(await state(),input);assert(expected.ok);
    await page.locator(`[data-p1v-select="${input.unit}"]`).click();
    await page.locator(`[data-p1v-cell="${input.to.x},${input.to.y}"]`).click();await settled();assert.deepEqual(await state(),expected.state);
  }
  await page.getByLabel('跳過動畫').uncheck();
}
async function watch(autoSelect=false){await page.evaluate(autoSelect=>{
  window.p1v7Observer?.disconnect();window.p1v7Trace=[];
  const root=document.querySelector('.p1v'),initialTurn=root.dataset.p1vTurn;
  let selected=false;
  const sample=()=>{
    const d=root.dataset;
    const row={time:performance.now(),turn:d.p1vTurn,busy:d.p1vBusy,cue:d.p1vSettledCue || null,selected:d.p1vSelected,
      markers:[...document.querySelectorAll('[data-p1v-blocked-marker]')].map(n=>[n.dataset.p1vBlockedMarker,n.dataset.cell]),
      blocks:[...document.querySelectorAll('[data-p1v-block-feedback]')].map(n=>n.dataset.p1vBlockFeedback),
      winch:!!document.querySelector('[data-p1v-winch-feedback]')};
    window.p1v7Trace.push(row);
    if(autoSelect && !selected && row.turn!==initialTurn && row.busy==='false'){
      selected=true;window.p1v7InputAt=performance.now();document.querySelector('[data-p1v-select="karen"]').click();
    }
  };
  window.p1v7Observer=new MutationObserver(sample);window.p1v7Observer.observe(root,{subtree:true,childList:true,attributes:true});sample();
},autoSelect);}
async function clickEnd(){await page.evaluate(()=>{window.p1v7ClickAt=performance.now();document.querySelector('[data-p1v-end]').click();});}
async function capture(name){const file=`1280x720-${name}.png`;const before=await page.evaluate(()=>({time:performance.now(),busy:document.querySelector('.p1v').dataset.p1vBusy,
  cue:document.querySelector('.p1v').dataset.p1vSettledCue || null,markers:[...document.querySelectorAll('[data-p1v-blocked-marker]')].map(n=>[n.dataset.p1vBlockedMarker,n.dataset.cell])}));
  await page.screenshot({path:path.join(output,file)});captures.push({path:`${evidenceDir}/${file}`,sha256:hash(fs.readFileSync(path.join(output,file))),viewport:page.viewportSize(),before,state:await state()});}
async function assertZeroCue(kind){
  const before=await state(),expected=resolve(before,before.turn);
  assert(!expected.events.some(e=>e.type==='move' && e.path.length>1));
  assert(expected.events.some(e=>kind==='block'?e.type==='intent' && e.reason==='blocked':e.type==='progress' && e.delta>0));
  await watch();await clickEnd();await settled();assert.deepEqual(await state(),expected.state);
  assert.equal(await page.locator('[data-p1v-end]').isEnabled(),true);
  assert.equal(await page.locator('[data-p1v-settled-cue]').count(),1);
  await page.waitForTimeout(330);
  const selector=kind==='block'?'.p1v-block-pop':'.p1v-winch-pop';
  const visible=await page.locator(selector).evaluate(n=>({opacity:Number(getComputedStyle(n).opacity),text:n.textContent}));
  assert(visible.opacity>.25,`cue opacity ${visible.opacity}`);
  const trace=await page.evaluate(()=>window.p1v7Trace),commit=trace.find(r=>r.turn!==String(before.turn));
  const times=await page.evaluate(()=>({now:performance.now(),click:window.p1v7ClickAt}));
  assert(commit && commit.busy==='false' && commit.cue);assert(times.now-commit.time>=300);
  assert(commit.time-times.click<100,`zero-step commit delayed ${commit.time-times.click}ms`);
  return {commit,visible,elapsedAfterCommit:times.now-commit.time,trace};
}
try{
  // Actual P1v6 component, served by the same Vite process and same browser.
  // Prepare scratch/p1v7-baseline-component.tsx with git show c980e5a:<path>.
  // A temporary sibling keeps its original relative imports; never committed.
  assert(!fs.existsSync(baselineFile));
  const baseline=fs.readFileSync(path.join(root,'scratch/p1v7-baseline-component.tsx'));
  report.baseline_component_sha256=hash(baseline);report.baseline_commit='c980e5a';
  fs.writeFileSync(baselineFile,baseline);
  const baselineRoute=async r=>{const response=await r.fetch({url:new URL('/src/playable-l03/.p1v7-baseline.tsx',url).href});await r.fulfill({response});};
  await page.route('**/src/playable-l03/PlayableL03.tsx',baselineRoute);
  const durations={baseline:[],current:[]};
  for(const version of ['baseline','current']){
    if(version==='current')await page.unroute('**/src/playable-l03/PlayableL03.tsx',baselineRoute);
    for(let i=0;i<3;i++){
      await load();await watch();await clickEnd();await settled();assert.deepEqual(await state(),resolve(initial(),1).state);
      const trace=await page.evaluate(()=>window.p1v7Trace),begin=trace.find(r=>r.busy==='true'),end=trace.find(r=>r.turn==='2');
      assert(begin && end);durations[version].push(end.time-begin.time);
    }
  }
  const average=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
  assert(durations.current.every(ms=>ms>=6*230 && ms<6*230+220));
  assert(Math.abs(average(durations.current)-average(durations.baseline))<90);
  pass('normal six-step turns preserve measured P1v6 lock duration (3 baseline and 3 current replays)',{durations});

  await load();await prime();const winch=await assertZeroCue('winch');await capture('zero-step-winch-after-commit');
  const zeroWinchState=await state();
  pass('zero-step winch remains visibly painted 300ms after immediate commit, with end-turn enabled',winch);
  await page.waitForTimeout(550);assert.equal(await page.locator('[data-p1v-settled-cue]').count(),0);assert.equal(await page.locator(transient).count(),0);
  assert.deepEqual(await state(),zeroWinchState);
  pass('independent zero-step expiry removes all feedback without a second state commit');

  await load();await blockSetup();const block=await assertZeroCue('block');await capture('zero-step-block-after-commit');
  pass('zero-step confirmed block remains visible after commit with original rule outcome',block);
  await page.locator('[data-p1v-select="karen"]').click();assert.equal(await page.locator('[data-p1v-settled-cue]').count(),0);
  assert.equal(await page.locator('[data-p1v-block-feedback]').count(),0);
  pass('a new selection clears the settled cue immediately');

  await load();await prime();await watch(true);await clickEnd();
  await page.waitForFunction(()=>document.querySelector('.p1v').dataset.p1vSelected==='karen');
  const immediate=await page.evaluate(()=>({trace:window.p1v7Trace,inputAt:window.p1v7InputAt}));
  const commit=immediate.trace.find(r=>r.turn==='5'),accepted=immediate.trace.find(r=>r.selected==='karen');
  assert(commit && accepted);assert(immediate.inputAt-commit.time<20);assert(accepted.time-commit.time<100);
  assert.equal(await page.locator('[data-p1v-settled-cue]').count(),0);
  pass('real input dispatched at the committed DOM is accepted immediately; no cue-owned lock',{commitToDispatchMs:immediate.inputAt-commit.time,commitToAcceptedMs:accepted.time-commit.time});
  // A second resolution replaces the old cue; Retry during terminal feedback
  // must cancel its expiry and cannot later change the fresh initial state.
  await load();await prime();await turn();const first=await page.locator('.p1v').getAttribute('data-p1v-settled-cue');
  assert(first);await clickEnd();await settled();const second=await page.locator('.p1v').getAttribute('data-p1v-settled-cue');assert(second && second!==first);
  await page.getByRole('button',{name:'重試',exact:true}).click();assert.deepEqual(await state(),initial());
  assert.equal(await page.locator('[data-p1v-settled-cue]').count(),0);await page.waitForTimeout(850);assert.deepEqual(await state(),initial());assert.equal(await page.locator(transient).count(),0);
  pass('new resolution replaces the cue; Retry cancels it with no stale effects or double commit');

  for(const mode of ['skip','reduce'])for(const kind of ['winch','block']){
    await load();if(kind==='winch')await prime();else await blockSetup();
    if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await watch();await turn();assert.equal(await page.locator(transient).count(),0);assert.equal(await page.locator('[data-p1v-settled-cue]').count(),0);
    const trace=await page.evaluate(()=>window.p1v7Trace);assert(trace.every(r=>!r.cue && !r.winch && !r.blocks.length));
    if(kind==='block')assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),1);
    pass(`${mode}: zero-step ${kind} commits without transient mounts; static markers remain`,{trace});
  }
  for(const mode of ['skip','reduce']){
    await load();await prime();await turn();assert.equal(await page.locator('[data-p1v-settled-cue]').count(),1);
    if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await page.waitForFunction(()=>!document.querySelector('[data-p1v-settled-cue]'));
    assert.equal(await page.locator(transient).count(),0);await page.waitForTimeout(800);assert.equal(await page.locator(transient).count(),0);
    pass(`${mode}: toggling during settled feedback cancels it permanently`);
  }
  await load();await blockSetup(6);
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),1); // unchanged preview
  const expected=resolve(await state(),3),blockIndex=expected.events.findIndex(e=>e.type==='intent' && e.reason==='blocked');
  assert(expected.events.slice(0,blockIndex).some(e=>e.type==='move'));
  await watch();await clickEnd();await page.waitForFunction(()=>document.querySelector('.p1v').dataset.p1vBusy==='true');
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),0);
  await capture('synced-marker-before-event');
  await page.waitForSelector('[data-p1v-block-feedback="knight-2"]');
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').getAttribute('data-cell'),'2,3');
  await capture('synced-marker-after-event');await settled();assert.deepEqual(await state(),expected.state);
  const trace=await page.evaluate(()=>window.p1v7Trace);
  assert(trace.filter(r=>r.busy==='true' && !r.blocks.length).every(r=>!r.markers.some(([id])=>id==='knight-2')));
  pass('late blocked intent stays absent throughout the earlier move and appears at its event/current cell; preview and committed prediction retained',{blockIndex,trace});

  // The converse ordering proves an already-played block persists while a
  // later enemy is still moving, then returns to the NEW prediction on finish.
  await load();await page.getByLabel('跳過動畫').check();await turn();
  const beforeRetreat=await state(),retreat={type:'move',turn:2,unit:'lace',to:{x:0,y:3}};
  const retreated=command(beforeRetreat,retreat);assert(retreated.ok);
  await page.locator('[data-p1v-select="lace"]').click();await page.locator('[data-p1v-cell="0,3"]').click();await settled();assert.deepEqual(await state(),retreated.state);
  await page.getByLabel('跳過動畫').uncheck();
  const earlyExpected=resolve(await state(),2);
  assert.equal(earlyExpected.events[0].reason,'blocked');assert(earlyExpected.events.some(e=>e.type==='move' && e.unit==='knight-2'));
  await clickEnd();await page.waitForFunction(()=>document.querySelector('.p1v').dataset.p1vBusy==='true');
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-1"]').getAttribute('data-cell'),'1,5');
  await capture('synced-marker-during-later-move');await settled();assert.deepEqual(await state(),earlyExpected.state);
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-1"]').count(),0);
  pass('reached block stays at its visual cell during a later enemy move, then resets to the new-state prediction on finish');
  assert.deepEqual(errors,[]);
  for(const [file,digest] of Object.entries(report.source_sha256))assert.equal(hash(fs.readFileSync(path.join(root,file))),digest);
  report.exit_code=0;
}catch(e){report.exit_code=1;report.failure=e.stack;process.exitCode=1;console.error(e);await page.screenshot({path:path.join(output,'failure.png')}).catch(()=>{});}
finally{report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(output,'feedback-results.json'),JSON.stringify(report,null,2)+'\n');await context.close();if(fs.existsSync(baselineFile))fs.unlinkSync(baselineFile);}
