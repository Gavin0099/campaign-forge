import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'../..'),dir=path.join(root,'ui-prototype/docs/playable-l03-p1v6');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const reports=['feedback-results.json','p1v-regression/browser-results.json','p1v2-regression/after-results.json',
  'p1v3-regression/visual-results.json','p1v4-regression/art-results.json','p1v5-regression/feedback-results.json'];
let checks=0,captures=0,bindings=0;
for(const file of reports){
  const r=JSON.parse(fs.readFileSync(path.join(dir,file)));
  assert.equal(r.exit_code,0,file);assert.deepEqual(r.errors,[]);checks+=r.checks.length;
  for(const [source,digest] of Object.entries(r.source_sha256)){assert.equal(hash(fs.readFileSync(path.join(root,source))),digest,`stale source: ${file}: ${source}`);bindings++;}
  for(const c of r.captures){assert.equal(hash(fs.readFileSync(path.join(root,c.path))),c.sha256,`capture mismatch: ${c.path}`);captures++;}
}
assert.equal(checks,79);
const feedback=JSON.parse(fs.readFileSync(path.join(dir,'feedback-results.json')));
for(let i=0;i<4;i++){
  const frame=feedback.captures.find(c=>c.path.endsWith(`winch-turn-0${i}.png`));
  assert.equal(frame.frame_index,String(i));
  assert(frame.compositor_timestamp>=frame.phase_interval[0] && frame.compositor_timestamp<frame.phase_interval[1]);
}
const original=JSON.parse(fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p1v5/feedback-results.json')));
assert.equal(hash(fs.readFileSync(path.join(root,'ui-prototype/src/playable-l03/rules.ts'))),original.source_sha256['ui-prototype/src/playable-l03/rules.ts']);
for(const name of ['landing-1-knight-1','landing-2-knight-2','winch-turn-00','winch-turn-01','winch-turn-02','winch-turn-03','warning-2-of-3','blocked-marker-preview','confirmed-block-spark'])
  assert(fs.existsSync(path.join(dir,`1280x720-${name}.png`)));
const manifest=JSON.parse(fs.readFileSync(path.join(root,'ui-prototype/docs/art-manifest.json')));
for(const file of ['winch-frames.png','rope-states.png']){
  const asset=fs.readFileSync(path.join(root,'ui-prototype/public/art/l03-p1v6',file)),entry=manifest[`l03-p1v6/${file}`];
  assert.equal(hash(asset),entry.sha256);assert.equal(asset.length,entry.bytes);assert.equal(asset[25],6,'RGBA PNG');
  assert.equal(asset.readUInt32BE(16),entry.width);assert.equal(asset.readUInt32BE(20),entry.height);
}
const commandFile=path.join(dir,'command-results.json');
const commands=JSON.parse(fs.readFileSync(commandFile,'utf8').replace(/^\uFEFF/,''));
assert.equal(commands.checks.length,7);assert(commands.checks.every(c=>c.exit_code===0));
const replayFile='artifacts/governance-native-acceptance.json';
const replay=JSON.parse(fs.readFileSync(path.join(root,replayFile)));
assert(Object.values(replay.checks).every(c=>c.exit_code===0));
assert.equal(replay.native_execution_claimed,false);
const result={checked_at:new Date().toISOString(),exit_code:0,browser_checks:checks,capture_hashes_checked:captures,
  source_bindings_checked:bindings,rules_unchanged:true,painted_originals:2,
  command_results_sha256:hash(fs.readFileSync(commandFile)),governance_receipt_sha256:hash(fs.readFileSync(path.join(root,replayFile))),
  log_sha256:Object.fromEntries(['p0','p0b','p0c','p1v6-feedback','build','scope','governance'].map(n=>[`${n}.log`,hash(fs.readFileSync(path.join(dir,`${n}.log`)))])),
  scope:'Current-source reports and unmodified execution screenshots; attempts retained as historical failures, excluded from passing totals.',human_playtest:'HUMAN_PENDING'};
fs.writeFileSync(path.join(dir,'evidence-audit.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
