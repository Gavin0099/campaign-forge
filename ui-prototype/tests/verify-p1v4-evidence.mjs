import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'../..');
const dir=path.join(root,'ui-prototype/docs/playable-l03-p1v4');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const reports=['p1v-regression/browser-results.json','p1v2-regression/after-results.json','p1v3-regression/visual-results.json','art-results.json'];
let checks=0,captures=0,bindings=0;
for(const file of reports){
 const r=JSON.parse(fs.readFileSync(path.join(dir,file)));
 assert.equal(r.exit_code,0,file);assert.deepEqual(r.errors,[]);checks+=r.checks.length;
 for(const [f,digest] of Object.entries(r.source_sha256)){assert.equal(hash(fs.readFileSync(path.join(root,f))),digest,`stale source: ${file}: ${f}`);bindings++;}
 for(const c of r.captures){assert.equal(hash(fs.readFileSync(path.join(root,c.path))),c.sha256,`capture mismatch: ${c.path}`);captures++;}
}
assert.equal(checks,53);
for(const size of ['1280x720','1920x1080']){
 for(const f of [`after-${size}-start.png`,`after-${size}-selected-path-preview.png`,`after-${size}-enemy-intent.png`,`p1v3-regression/after-${size}-enemy-turn-banner.png`,`p1v-regression/${size}-victory.png`,`p1v-regression/${size}-defeat.png`])assert(fs.existsSync(path.join(dir,f)),f);
 for(const f of [`p1v-regression/${size}-start.png`,`after-${size}-path-preview.png`,`p1v-regression/${size}-intent.png`,`after-${size}-enemy-turn-banner.png`,`p1v-regression/${size}-victory.png`,`p1v-regression/${size}-defeat.png`,`p1v2-regression/after-${size}-winch.png`])assert(fs.existsSync(path.join(dir,'../playable-l03-p1v3',f)),f);
}
const referenceFiles=['layout-guide.svg','layout-guide.png','STYLE.md','VERIFICATION.md','comparison.html'];
const result={checked_at:new Date().toISOString(),exit_code:0,browser_checks:checks,capture_hashes_checked:captures,source_bindings_checked:bindings,reference_sha256:Object.fromEntries(referenceFiles.map(f=>[f,hash(fs.readFileSync(path.join(dir,f)))])),scope:'Final browser reports/current source, unmodified captures and comparison targets. Historical rejected-scale source is intentionally not current.'};
fs.writeFileSync(path.join(dir,'evidence-audit.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
