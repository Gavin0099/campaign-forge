import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { initialState, DEFAULT_CONFIG, command, resolve } from '../src/playable-l03/rules.ts';
import { buildFeedbackTimeline } from '../src/playable-l03/feedback.ts';

const root=path.resolve(import.meta.dirname,'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path)); assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes); assert.equal(hash(fs.readFileSync(binding.path)),binding.sha256);
const {chromium}=await import('playwright');
const evidenceDir=process.argv.includes('--p1v7') ? 'ui-prototype/docs/playable-l03-p1v7/p1v6-regression' : 'ui-prototype/docs/playable-l03-p1v6';
const output=path.join(root,evidenceDir),scratch=path.join(root,'scratch/playable-l03-p1v6-browser');
fs.mkdirSync(output,{recursive:true});fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const context=await chromium.launchPersistentContext(path.join(scratch,'profile'),{executablePath:binding.path,headless:true,env,viewport:{width:1280,height:720}});
const url='http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(url).origin?r.continue():r.abort());
const page=context.pages()[0],checks=[],captures=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const sources=['feedback.ts','PlayableL03.tsx','presentation.tsx','playable.css','rules.ts'].map(f=>`ui-prototype/src/playable-l03/${f}`)
  .concat('ui-prototype/tests/playable-l03-p1v6-browser.mjs','ui-prototype/docs/art-prompts.json','ui-prototype/docs/art-manifest.json',
    ['winch-frames.png','rope-states.png'].map(f=>`ui-prototype/public/art/l03-p1v6/${f}`));
const report={started_at:new Date().toISOString(),browser:binding,source_sha256:Object.fromEntries(sources.map(f=>[f,hash(fs.readFileSync(path.join(root,f)))])),checks,captures,errors,human_playtest:'HUMAN_PENDING'};
const initial=()=>initialState('open',{...DEFAULT_CONFIG,p0c:{survivalTurns:6}});
const state=()=>page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const settled=()=>page.waitForSelector('[data-p1v-busy="false"]');
const transient='[data-p1v-footstep],[data-p1v-winch-feedback],[data-p1v-block-feedback],[data-p1v-clash],[data-p1v-confirm],.p1v-winch-jerk';
function pass(name,details={}){checks.push({name,...details});console.log(`PASS ${checks.length}: ${name}`);}
async function load(){
  await page.emulateMedia({reducedMotion:'no-preference'});await page.goto(url);await settled();
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(n=>n.getAttribute('href')))].map(async src=>{const i=new Image();i.src=src;await i.decode();}));});
  assert.deepEqual(await state(),initial());
}
async function capture(name){
  const file=`1280x720-${name}.png`,before=await page.evaluate(()=>({time:performance.now(),busy:document.querySelector('.p1v').dataset.p1vBusy,
    frames:[...document.querySelectorAll('[data-p1v-winch-frame]')].filter(n=>getComputedStyle(n).opacity==='1').map(n=>n.dataset.p1vWinchFrame)}));
  await page.screenshot({path:path.join(output,file)});
  captures.push({path:`${evidenceDir}/${file}`,sha256:hash(fs.readFileSync(path.join(output,file))),viewport:page.viewportSize(),before,state:await state()});
}
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
async function watch(){
  await page.evaluate(selector=>{
    window.fxTrace=[];window.fxSeen=new WeakSet();window.fxObserver?.disconnect();
    const root=document.querySelector('.p1v');let busy=root.dataset.p1vBusy;
    const record=()=>{
      for(const n of document.querySelectorAll(selector))if(!window.fxSeen.has(n)){
        window.fxSeen.add(n);window.fxTrace.push({kind:n.hasAttribute('data-p1v-footstep')?'landing':'effect',unit:n.dataset.p1vFootstep,
          cell:n.dataset.p1vLandingCell,time:performance.now(),busy:root.dataset.p1vBusy,turn:root.dataset.p1vTurn,
          state:JSON.parse(root.dataset.p1vState)});
      }
      if(busy!==root.dataset.p1vBusy){busy=root.dataset.p1vBusy;window.fxTrace.push({kind:'busy',busy,time:performance.now()});}
    };
    window.fxObserver=new MutationObserver(record);window.fxObserver.observe(root,{subtree:true,childList:true,attributes:true});record();
  },transient);
}
try {
  await load();
  assert.equal(await page.locator('[data-p1v-winch-painted]').count(),1);
  assert.equal(await page.locator('[data-p1v-winch-frame] image[href="/art/l03-p1v6/winch-frames.png"]').count(),4);
  assert.equal(await page.locator('[data-p1v-rope-state="slack"] image[href="/art/l03-p1v6/rope-states.png"]').count(),1);
  assert.equal(await page.locator('.p1v-winch-wheel,.p1v-winch-rope path,ellipse.p1v-winch-alert').count(),0);
  assert((await page.locator('[data-p1v-winch-frame],[data-p1v-rope-state]').evaluateAll(ns=>ns.map(n=>getComputedStyle(n).overflow))).every(v=>v==='hidden'));
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'ui-prototype/docs/art-manifest.json')));
  for(const file of ['winch-frames.png','rope-states.png'])assert.equal(manifest[`l03-p1v6/${file}`].sha256,hash(fs.readFileSync(path.join(root,'ui-prototype/public/art/l03-p1v6',file))));
  pass('four painted winch frames and slack rope load with exact provenance; geometric wheel, rope path and warning ellipse absent');

  await watch();
  const expected=resolve(initial(),1),landings=buildFeedbackTimeline(expected.events,230).filter(c=>c.kind==='landing');assert.equal(landings.length,2);
  await page.locator('[data-p1v-end]').click();
  await settled();assert.deepEqual(await state(),expected.state);
  const trace=await page.evaluate(()=>window.fxTrace),landed=trace.filter(e=>e.kind==='landing');
  assert.deepEqual(landed.map(e=>e.unit),landings.map(e=>e.unit));assert(landed[0].time<landed[1].time);
  assert.deepEqual(landed.map(e=>e.cell),landings.map(c=>`${c.cell.x},${c.cell.y}`));
  assert.deepEqual(landed[0].state,initial());assert.equal(landed[0].busy,'true');
  const finished=trace.find(e=>e.kind==='busy' && e.busy==='false');
  assert(landed.every(e=>e.time<=finished.time));
  assert.equal(landed[0].turn,'1');
  pass('two movers land separately at their own endpoints; first landing precedes atomic state commit, final landing shares finish boundary, no delayed settlement dust',{trace});
  await page.waitForTimeout(240);assert.equal(await page.locator('[data-p1v-footstep]').count(),0);
  assert.equal(await page.locator('[data-p1v-end]').isEnabled(),true);
  pass('independent landing effects expire without extending the existing input lock');
  // Each capture gets its own real replay: screenshot encoding must not make
  // the test miss the next 180ms effect. Production time is never slowed.
  for(let i=0;i<landings.length;i++){
    await load();const cue=landings[i];
    const seen=page.waitForFunction(id=>!!document.querySelector(`[data-p1v-footstep="${id}"]`),cue.unit,{polling:'raf'});
    await page.locator('[data-p1v-end]').click();await seen;await capture(`landing-${i+1}-${cue.unit}`);await settled();
  }

  await load();await prime();
  // Capture compositor frames continuously. Sequential screenshot calls may
  // cross a short sprite interval while encoding a previous PNG.
  const cdp=await context.newCDPSession(page),film=[];
  const onFrame=frame=>{film.push(frame);void cdp.send('Page.screencastFrameAck',{sessionId:frame.sessionId});};
  cdp.on('Page.screencastFrame',onFrame);
  await page.evaluate(()=>{
    window.winchPhases=[];window.recordWinch=true;
    const sample=()=>{
      const frame=document.querySelector('.p1v-winch-jerk [data-p1v-winch-frame]');
      const visible=frame?[...document.querySelectorAll('[data-p1v-winch-frame]')].find(n=>getComputedStyle(n).opacity==='1')?.dataset.p1vWinchFrame:null;
      if(visible!==window.winchPhases.at(-1)?.frame)window.winchPhases.push({frame:visible,time:performance.timeOrigin+performance.now(),
        rope:document.querySelector('[data-p1v-rope-state="taut"] image')?.getAttribute('href') || null});
      if(window.recordWinch)requestAnimationFrame(sample);
    };requestAnimationFrame(sample);
  });
  await cdp.send('Page.startScreencast',{format:'png',maxWidth:1280,maxHeight:720,everyNthFrame:1});
  await page.locator('[data-p1v-end]').click();
  await page.waitForTimeout(750);
  await cdp.send('Page.stopScreencast');cdp.off('Page.screencastFrame',onFrame);await cdp.detach();
  const phases=await page.evaluate(()=>{window.recordWinch=false;return window.winchPhases;});
  assert.deepEqual(phases.filter(p=>p.frame!=null).map(p=>p.frame),['0','1','2','3']);
  assert(phases.filter(p=>p.frame!=null).every(p=>p.rope==='/art/l03-p1v6/rope-states.png'));
  const winning=film.map(f=>({...f,time:f.metadata.timestamp*1000})).filter(f=>Number.isFinite(f.time));
  for(let i=0;i<4;i++){
    const index=phases.findIndex(p=>p.frame===String(i)),begin=phases[index].time,end=phases[index+1]?.time;
    assert(Number.isFinite(end));
    const candidates=winning.filter(f=>f.time>=begin && f.time<end);
    assert(candidates.length,`no compositor frame for phase ${i}`);
    const chosen=candidates.sort((a,b)=>Math.abs(a.time-(begin+end)/2)-Math.abs(b.time-(begin+end)/2))[0];
    const file=`1280x720-winch-turn-0${i}.png`,bytes=Buffer.from(chosen.data,'base64');
    assert.equal(bytes.readUInt32BE(16),1280);assert.equal(bytes.readUInt32BE(20),720);
    fs.writeFileSync(path.join(output,file),bytes);
    captures.push({path:`${evidenceDir}/${file}`,sha256:hash(bytes),viewport:page.viewportSize(),
      frame_index:String(i),compositor_timestamp:chosen.time,phase_interval:[begin,end],
      provenance:'Unmodified Chrome screencast PNG selected inside recorded live CSS frame interval',state:await state()});
  }
  await settled();assert.equal((await state()).progress,2);assert.equal(await page.locator('[data-p1v-end]').isEnabled(),true);
  pass('actual 720p compositor sequence plays rest, turn A, turn B and jerk frames with painted taut rope and no extra lock',{phases,compositor_frames:film.length});
  await page.waitForTimeout(800);assert.equal(await page.locator('[data-p1v-rope-state="slack"]').count(),1);
  assert.equal(await page.locator('[data-p1v-winch-painted][data-warning="true"] .frame-3.p1v-winch-alert').evaluate(n=>getComputedStyle(n).opacity),'1');
  assert.equal(await page.locator('.p1v-winch-alert').evaluate(n=>getComputedStyle(n).filter),'none');
  assert.notEqual(await page.locator('.p1v-winch-alert image').evaluate(n=>getComputedStyle(n).filter),'none');
  assert.equal(await page.locator('[data-p1v-winch-feedback]').count(),0);await capture('warning-2-of-3');
  pass('2/3 warning rests on the painted ember drum; rope returns to slack after transient feedback');

  await load();await blockSetup();
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').getAttribute('data-cell'),'2,3');
  await capture('blocked-marker-preview');
  const beforeBlock=await state(),expectedBlock=resolve(beforeBlock,beforeBlock.turn);
  // Preview still has the marker; during playback P1v7 reveals it at the
  // blocked intent, after the preceding move rather than at phase start.
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),1);
  await page.locator('[data-p1v-end]').click();
  assert.equal(await page.locator('.p1v').getAttribute('data-p1v-busy'),'true');
  await page.waitForSelector('[data-p1v-clash][data-p1v-blocker="thoma"]');await capture('confirmed-block-spark');
  await settled();assert.deepEqual(await state(),expectedBlock.state);
  await page.waitForTimeout(700);assert.equal(await page.locator('[data-p1v-clash]').count(),0);
  assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),1);
  pass('broken-chain marker stays at the blocked enemy feet in preview and after its resolution event; clash targets counterfactually confirmed Thoma');
  for(const mode of ['skip','reduce']){
    await load();await blockSetup();
    if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await watch();await turn();
    assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').count(),1);
    assert.equal(await page.locator('[data-p1v-blocked-marker="knight-2"]').evaluate(n=>getComputedStyle(n).animationName),'none');
    assert.equal(await page.locator(transient).count(),0);assert.deepEqual(await page.evaluate(()=>window.fxTrace.filter(e=>e.kind!=='busy')),[]);
    pass(`${mode}: blocked marker remains static and real block resolution mounts no transient feedback`);
    await load();if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await watch();for(let i=0;i<4;i++)await turn();
    assert.equal((await state()).progress,2);assert.equal(await page.locator(transient).count(),0);
    assert.deepEqual(await page.evaluate(()=>window.fxTrace.filter(e=>e.kind!=='busy')),[]);
    pass(`${mode}: all moves and winch progress preserve exact outcomes without ever mounting transient effects`);
  }
  for(const mode of ['skip','reduce']){
    await load();await watch();const expected=resolve(initial(),1);
    await page.locator('[data-p1v-end]').click();await page.waitForSelector('[data-p1v-footstep="knight-1"]');
    if(mode==='skip')await page.getByLabel('跳過動畫').check();else await page.emulateMedia({reducedMotion:'reduce'});
    await settled();assert.deepEqual(await state(),expected.state);assert.equal(await page.locator(transient).count(),0);
    await page.waitForTimeout(800);
    assert.equal(await page.locator(transient).count(),0);
    const trace=await page.evaluate(()=>window.fxTrace.filter(e=>e.kind==='landing'));
    assert.deepEqual(trace.map(e=>e.unit),['knight-1']);
    pass(`${mode}: changing preference between two landings commits once and permanently cancels future cues`);
  }
  assert.deepEqual(errors,[]);
  for(const [file,digest] of Object.entries(report.source_sha256))assert.equal(hash(fs.readFileSync(path.join(root,file))),digest);
  report.exit_code=0;
}catch(e){report.exit_code=1;report.failure=e.stack;process.exitCode=1;console.error(e);await page.screenshot({path:path.join(output,'failure.png')}).catch(()=>{});}
finally{report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(output,'feedback-results.json'),JSON.stringify(report,null,2)+'\n');await context.close();}
