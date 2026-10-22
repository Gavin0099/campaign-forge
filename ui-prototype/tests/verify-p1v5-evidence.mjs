import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'../..'),dir=path.join(root,'ui-prototype/docs/playable-l03-p1v5');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const reports=['feedback-results.json','p1v-regression/browser-results.json','p1v2-regression/after-results.json','p1v3-regression/visual-results.json','p1v4-regression/art-results.json'];
let checks=0,captures=0,bindings=0;
for(const file of reports){
  const r=JSON.parse(fs.readFileSync(path.join(dir,file)));
  assert.equal(r.exit_code,0,file);assert.deepEqual(r.errors,[]);checks+=r.checks.length;
  for(const [source,digest] of Object.entries(r.source_sha256)){assert.equal(hash(fs.readFileSync(path.join(root,source))),digest,`stale source: ${file}: ${source}`);bindings++;}
  for(const c of r.captures){assert.equal(hash(fs.readFileSync(path.join(root,c.path))),c.sha256,`capture mismatch: ${c.path}`);captures++;}
}
assert.equal(checks,67);
for(const name of ['winch-interference','winch-1-of-3','warning-2-of-3','body-block','intent-pulse'])assert(fs.existsSync(path.join(dir,`1280x720-${name}.png`)));
const report={checked_at:new Date().toISOString(),exit_code:0,browser_checks:checks,capture_hashes_checked:captures,source_bindings_checked:bindings,scope:'Current source and unmodified execution screenshots; historical failed attempts intentionally excluded.',human_playtest:'HUMAN_PENDING'};
fs.writeFileSync(path.join(dir,'evidence-audit.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
