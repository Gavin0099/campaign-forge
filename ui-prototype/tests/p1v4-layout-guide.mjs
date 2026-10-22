// Render the source-authored layout diagram, not a game screenshot.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'../..');
const binding=JSON.parse(fs.readFileSync(path.join(root,'.codex/visual-browser-binding.json')));
assert(path.isAbsolute(binding.path)); assert.equal(fs.realpathSync(binding.path),binding.path);
assert.equal(fs.statSync(binding.path).size,binding.bytes);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(binding.path)).digest('hex'),binding.sha256);
const {chromium}=await import('playwright');
const scratch=path.join(root,'scratch/p1v4-guide');fs.mkdirSync(scratch,{recursive:true});
const env=Object.fromEntries(['SystemRoot','WINDIR','SystemDrive'].filter(k=>process.env[k]).map(k=>[k,process.env[k]]));
Object.assign(env,{TEMP:scratch,TMP:scratch});
const browser=await chromium.launch({executablePath:binding.path,headless:true,env});
try {
 const page=await browser.newPage({viewport:{width:1536,height:1024}});
 await page.route('**/*',r=>r.abort());
 await page.setContent('<style>html,body{margin:0;background:#182521}svg{display:block}</style>'+fs.readFileSync(path.join(root,'ui-prototype/docs/playable-l03-p1v4/layout-guide.svg'),'utf8'));
 await page.screenshot({path:path.join(root,'ui-prototype/docs/playable-l03-p1v4/layout-guide.png')});
} finally {await browser.close();}
