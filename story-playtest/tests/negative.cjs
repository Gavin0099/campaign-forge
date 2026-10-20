const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '../..');
// Existing, reviewed host binding is supplied explicitly, never discovered through PATH.
assert(process.env.STORY_BINDING && path.isAbsolute(process.env.STORY_BINDING));
const binding = JSON.parse(fs.readFileSync(process.env.STORY_BINDING));
const node = binding.executables.node;
assert.equal(fs.realpathSync(node.path), fs.realpathSync(process.execPath));
assert.equal(fs.statSync(node.path).size, node.size);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(node.path)).digest('hex'), node.sha256);
const env = Object.fromEntries(['SystemRoot', 'WINDIR', 'SystemDrive', 'TEMP', 'TMP'].filter(k => process.env[k]).map(k => [k, process.env[k]]));
env.INKJS = path.resolve(process.env.INKJS || path.join(root, 'scratch/ink-tools/node_modules/inkjs'));
const expected = { notes: 'notes_possession', starplate: 'starplate_possession', resurrection: 'teo_continuity', absent: 'sawin_absent_reappearance', knowledge: 'K1_without_key_information', soul_knowledge: 'L07_without_witness_information', trust: 'trust:trust_thoma', refusal: 'thoma_moral_boundary', public: 'thoma_public_threshold', tide: 'chapter_clock', loss: 'quin_loss', recruitment: 'L07_without_witness_information', death: 'maggie_reappeared_after_death', count: 'l07_saved' };
const tests = [];
for (const [fault, invariant] of Object.entries(expected)) {
  const argv = [path.join(root, 'docs/story/script/check/walk.js'), path.join(root, 'scratch/story-playtest/story.json'), `--inject=${fault}`];
  const result = spawnSync(node.path, argv, { cwd: root, env, encoding: 'utf8', timeout: 10000 });
  assert(!result.error, String(result.error));
  assert.equal(result.status, 1, fault + ': real validator must return 1');
  const report = JSON.parse(result.stdout);
  assert(report.errors.some(error => error.includes(invariant)), fault + ': wrong rejection ' + report.errors);
  tests.push({ fault, expectedInvariant: invariant, argv: ['node', ...argv.map(x => x.startsWith(root) ? path.relative(root, x).replaceAll('\\', '/') : x)], exitCode: result.status, observed: report.errors });
}
const report = { tests, passed: tests.length, failed: 0, nodeBound: true, sourceHash: JSON.parse(fs.readFileSync(path.join(root, 'scratch/story-playtest/manifest.json'))).sourceHash };
fs.writeFileSync(path.join(root, 'docs/story/alignment/evidence/negative.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify({ passed: tests.length, failed: 0 }));
