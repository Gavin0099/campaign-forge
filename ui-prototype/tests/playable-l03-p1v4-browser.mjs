import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { MAP, initialState, DEFAULT_CONFIG, command, key, walkable } from '../src/playable-l03/rules.ts';

const root=path.resolve(import.meta.dirname,'../..');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path));assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes);assert.equal(hash(fs.readFileSync(binding.path)),binding.sha256);
const {chromium}=await import('playwright');
const output=path.join(root,'ui-prototype/docs/playable-l03-p1v4');
const scratch=path.join(root,'scratch/playable-l03-p1v4-browser');fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const context=await chromium.launchPersistentContext(path.join(scratch,'profile'),{executablePath:binding.path,headless:true,env});
const url='http://127.0.0.1:5183/?scene=playable-l03';
await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(url).origin?r.continue():r.abort());
const page=context.pages()[0],checks=[],captures=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const files=['PlayableL03.tsx','presentation.tsx','playable.css','rules.ts'].map(f=>`ui-prototype/src/playable-l03/${f}`)
  .concat(['ui-prototype/tests/playable-l03-p1v4-browser.mjs','ui-prototype/docs/art-prompts.json','ui-prototype/docs/art-manifest.json'],
    fs.readdirSync(path.join(root,'ui-prototype/public/art/l03-p1v4')).map(f=>`ui-prototype/public/art/l03-p1v4/${f}`));
const report={started_at:new Date().toISOString(),browser:binding,source_sha256:Object.fromEntries(files.map(f=>[f,hash(fs.readFileSync(path.join(root,f)))])),checks,captures,errors,human_playtest:'HUMAN_PENDING'};
function pass(name,detail={}){checks.push({name,...detail});console.log(`PASS ${checks.length}: ${name}`);}
const state=()=>page.locator('[data-p1v-state]').getAttribute('data-p1v-state').then(JSON.parse);
const initial=()=>initialState('open',{...DEFAULT_CONFIG,p0c:{survivalTurns:6}});
async function capture(name){
 const file=`after-${page.viewportSize().width}x${page.viewportSize().height}-${name}.png`;
 await page.screenshot({path:path.join(output,file)});
 captures.push({path:`ui-prototype/docs/playable-l03-p1v4/${file}`,sha256:hash(fs.readFileSync(path.join(output,file))),viewport:page.viewportSize(),state:await state()});
}
try {
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'ui-prototype/docs/art-manifest.json')));
 for(const name of fs.readdirSync(path.join(root,'ui-prototype/public/art/l03-p1v4')))assert.equal(manifest[`l03-p1v4/${name}`].sha256,hash(fs.readFileSync(path.join(root,'ui-prototype/public/art/l03-p1v4',name))));
 pass('every generated original, including the rejected battlefield, matches the recorded SHA-256');
 for(const size of [{width:1280,height:720},{width:1920,height:1080}]){
  await page.setViewportSize(size);await page.goto(url);await page.waitForSelector('[data-p1v-busy="false"]');
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...new Set([...document.querySelectorAll('svg image')].map(n=>n.getAttribute('href')))].map(src=>new Promise((done,fail)=>{const im=new Image();im.onload=done;im.onerror=fail;im.src=src;})));});
  await page.mouse.move(8,8);
  assert.deepEqual(await state(),initial());
  assert.equal(await page.locator('[data-p1v-battlefield]').count(),1);
  assert.equal(await page.locator('.p1v-map pattern').count(),0);
  assert.equal(await page.locator('[data-p1v-prop="winch"]').count(),1);
  assert.equal(await page.locator('[data-p1v-prop="bridge"]').count(),2);
  assert.equal(await page.locator('[data-p1v-prop="wagon"]').count(),1);
  const portraits=await page.locator('.p1v-portrait').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.p1vPortrait,signature:n.getAttribute('viewBox')+'|'+n.querySelector('image').getAttribute('href')})));
  assert.equal(new Set(portraits.map(p=>p.signature)).size,5);
  const idle=await page.locator('[data-p1v-cell]').evaluateAll(nodes=>nodes.map(n=>({fill:getComputedStyle(n).fill,stroke:getComputedStyle(n).stroke})));
  assert.equal(idle.length,99);assert(idle.every(n=>n.fill==='rgba(0, 0, 0, 0)' && n.stroke==='rgba(0, 0, 0, 0)'));
  await capture('start');
  pass(`${size.width}: one painted battlefield, no terrain patterns, four painted prop instances, five distinct portraits, idle grid hidden`,{portraits});

  const hits=await page.locator('[data-p1v-cell]').evaluateAll(nodes=>nodes.map(n=>{
   const [x,y]=n.dataset.p1vCell.split(',').map(Number);
   const expected=new DOMPoint(550+(x-y)*44,70+(x+y+1)*26).matrixTransform(n.getScreenCTM());
   const b=n.getBoundingClientRect();return {cell:n.dataset.p1vCell,hit:document.elementFromPoint(expected.x,expected.y)?.getAttribute('data-p1v-cell'),error:Math.hypot(expected.x-b.x-b.width/2,expected.y-b.y-b.height/2)};
  }));
  assert(hits.every(h=>h.hit===h.cell && h.error<.01));
  const river=[];for(let y=0;y<9;y++)for(const x of [4,5]){
   assert(!walkable({x,y},'open'));assert(!command(initial(),{type:'move',turn:1,unit:'lace',to:{x,y}}).ok);river.push(key({x,y}));
  }
  pass(`${size.width}: all 99 exact rule-grid centres receive their own hit; all 18 river cells remain impassable`,{hits,river});

  const geometry=await page.locator('[data-p1v-figure]').evaluateAll(async nodes=>{
   const results=[];
   for(const n of nodes){
    const im=new Image();im.src=n.querySelector('image').getAttribute('href');await im.decode();
    const canvas=document.createElement('canvas');canvas.width=im.naturalWidth;canvas.height=im.naturalHeight;
    const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(im,0,0);
    const vb=n.viewBox.baseVal,d=ctx.getImageData(vb.x,vb.y,vb.width,vb.height).data;
    let minY=vb.height,maxY=-1;
    for(let y=0;y<vb.height;y++)for(let x=0;x<vb.width;x++)if(d[(y*vb.width+x)*4+3]>=128){minY=Math.min(minY,y);maxY=Math.max(maxY,y);}
    const scale=Math.min(n.width.baseVal.value/vb.width,n.height.baseVal.value/vb.height);
    const screen=n.parentNode.getScreenCTM().d;
    results.push({id:n.dataset.p1vFigure,viewport_height:n.height.baseVal.value,tile_height:52,viewport_ratio:n.height.baseVal.value/52,visible_alpha_height:(maxY-minY+1)*scale,visible_alpha_ratio:(maxY-minY+1)*scale/52,screen_viewport_height:n.height.baseVal.value*screen,screen_tile_height:52*screen,crop:{x:vb.x,y:vb.y,width:vb.width,height:vb.height}});
   }return results;
  });
  assert(geometry.every(g=>Math.abs(g.viewport_ratio-1)<.001 && g.visible_alpha_ratio>.94 && g.visible_alpha_ratio<=1));
  pass(`${size.width}: geometric maximum 1.00 tile-high viewports; actual opaque figure height measured separately`,{geometry});
  const alpha=await page.evaluate(async()=>{const im=new Image();im.src='/art/l03-p1v4/props.png';await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);return [[0,0],[300,200],[600,400],[1000,300],[700,900]].map(([x,y])=>({x,y,alpha:ctx.getImageData(x,y,1,1).data[3]}));});
  assert(alpha.every(p=>p.alpha===0));pass(`${size.width}: prop atlas has true transparent empty space`,{alpha});
  await page.locator('[data-p1v-select="lace"]').click();await page.locator('[data-p1v-cell="1,1"]').hover();
  await capture('selected-path-preview');await page.keyboard.press('Escape');
  await page.locator('[data-p1v-cell="1,8"]').click();await page.mouse.move(8,8);await capture('enemy-intent');
  assert.deepEqual(await state(),initial());
  await page.keyboard.press('Escape');await page.mouse.move(8,8);
  // Diagnostic only: reveal hit polygons for human alignment inspection. This
  // extra screenshot is clearly named and is never used as a normal game state.
  await page.addStyleTag({content:'.p1v-cell{stroke:#f8ebbf!important;stroke-width:.6!important;fill:transparent!important}'});
  await capture('DIAGNOSTIC-grid-alignment');
 }
 assert.deepEqual(errors,[]);
 for(const [f,digest] of Object.entries(report.source_sha256))assert.equal(hash(fs.readFileSync(path.join(root,f))),digest,`source changed: ${f}`);
 report.exit_code=0;
}catch(e){report.exit_code=1;report.failure=e.stack;process.exitCode=1;console.error(e);await page.screenshot({path:path.join(output,'art-check-failure.png')}).catch(()=>{});}
finally{report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(output,'art-results.json'),JSON.stringify(report,null,2)+'\n');await context.close();}
