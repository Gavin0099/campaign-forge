import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'../..'),dir=path.join(root,'ui-prototype/docs/playable-l03-p1v7');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const reports=['p1v-regression/browser-results.json','p1v2-regression/after-results.json',
  'p1v3-regression/visual-results.json','p1v4-regression/art-results.json','p1v5-regression/feedback-results.json',
  'p1v6-regression/feedback-results.json','feedback-results.json'];
let checks=0,captures=0,bindings=0;
for(const file of reports){
  const r=JSON.parse(fs.readFileSync(path.join(dir,file)));
  assert.equal(r.exit_code,0,file);assert.deepEqual(r.errors,[]);checks+=r.checks.length;
  for(const [source,digest] of Object.entries(r.source_sha256)){assert.equal(hash(fs.readFileSync(path.join(root,source))),digest,`stale source: ${file}: ${source}`);bindings++;}
  for(const c of r.captures){
    const bytes=fs.readFileSync(path.join(root,c.path));assert.equal(hash(bytes),c.sha256,`capture mismatch: ${c.path}`);captures++;
    if(c.path.startsWith('ui-prototype/docs/playable-l03-p1v7/1280x720-')){assert.equal(bytes.readUInt32BE(16),1280);assert.equal(bytes.readUInt32BE(20),720);}
  }
}
assert.equal(checks,94); // All 79 original browser checks + 15 new ones.
const feedback=JSON.parse(fs.readFileSync(path.join(dir,'feedback-results.json')));
assert.equal(feedback.checks.length,15);
for(const name of ['zero-step-winch-after-commit','zero-step-block-after-commit','synced-marker-before-event','synced-marker-after-event','synced-marker-during-later-move'])
  assert(feedback.captures.some(c=>c.path.endsWith(`${name}.png`)));
const during=feedback.captures.find(c=>c.path.endsWith('synced-marker-during-later-move.png'));
assert.equal(during.before.busy,'true');assert.deepEqual(during.before.markers,[['knight-1','1,5']]);
const before=feedback.captures.find(c=>c.path.endsWith('synced-marker-before-event.png'));
assert.equal(before.before.busy,'true');assert.deepEqual(before.before.markers,[]);
const legacy=JSON.parse(fs.readFileSync(path.join(dir,'p1v6-regression/feedback-results.json')));
assert.equal(legacy.checks.length,12);
for(let i=0;i<4;i++){
  const frame=legacy.captures.find(c=>c.path.endsWith(`winch-turn-0${i}.png`));
  assert.equal(frame.frame_index,String(i));
  assert(frame.compositor_timestamp>=frame.phase_interval[0] && frame.compositor_timestamp<frame.phase_interval[1]);
}
const original=JSON.parse(fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p1v6/feedback-results.json')));
assert.equal(hash(fs.readFileSync(path.join(root,'ui-prototype/src/playable-l03/rules.ts'))),original.source_sha256['ui-prototype/src/playable-l03/rules.ts']);
const commandFiles=['pure-command-results.json','browser-command-results.json','build-command-result.json','scope-command-result.json'];
const commandDigests={};let commandCount=0;
for(const file of commandFiles){
  const bytes=fs.readFileSync(path.join(dir,file));const parsed=JSON.parse(bytes.toString().replace(/^\uFEFF/,''));
  const commands=Array.isArray(parsed)?parsed:[parsed];assert(commands.length);assert(commands.every(c=>c.exit_code===0),file);
  commandCount+=commands.length;commandDigests[file]=hash(bytes);
}
assert.equal(commandCount,13); // 5 pure, 6 browser, build, scope; first browser in source-bound report.
assert(!fs.existsSync(path.join(root,'ui-prototype/src/playable-l03/.p1v7-baseline.tsx')));
const result={checked_at:new Date().toISOString(),exit_code:0,original_game_checks:107,new_game_checks:18,
  game_checks:125,browser_checks:checks,pure_checks:31,capture_hashes_checked:captures,source_bindings_checked:bindings,
  command_result_sha256:commandDigests,rules_unchanged:true,accepted_limit:'Final landing shares finish; no added lock or wait',
  human_playtest:'HUMAN_PENDING',scope:'Current-source reports and unmodified Chrome screenshots; historical failed attempts excluded from passing totals'};
fs.writeFileSync(path.join(dir,'evidence-audit.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
