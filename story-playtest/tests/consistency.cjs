const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const { Story } = require(process.env.INKJS || path.join(root, 'scratch/ink-tools/node_modules/inkjs'));
const { names } = require(path.join(root, 'docs/story/script/check/invariants.js'));
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const checks = [];
const flags = read('docs/story/FLAGS.md');
const declarations = [...read('docs/story/script/globals.ink').matchAll(/^VAR (\w+)\s*=/gm)].map(m => m[1]);
assert.deepEqual([...declarations].sort(), [...names].sort());
for (const name of declarations) assert(flags.includes(name), 'Undocumented variable ' + name);
checks.push({ name: 'all-runtime-variables-documented-and-validated', count: names.length, passed: true });
const ink = read('docs/story/script/ch01.ink') + read('docs/story/script/ch02.ink');
for (let n = 1; n <= 7; n++) {
  const id = `L${String(n).padStart(2, '0')}`;
  assert(fs.existsSync(path.join(root, `docs/story/levels/${id}.md`)));
  for (const suffix of ['pre', 'post']) assert(ink.includes(`=== ${id}_${suffix} ===`));
  assert(ink.includes(`#battle:${id}`));
}
assert(!/^=== L(?:0[8-9]|[12]\d)_/m.test(ink));
assert(!/貝恩|洩潮地|燈號簿/.test(ink));
assert(!/beholder|mind flayer|illithid|Forgotten Realms|Baldur.s Gate|Faer[uû]n/i.test(ink));
checks.push({ name: 'seven-level-correspondence-no-future-or-unsourced-script-content', passed: true });
const compiled = read('scratch/story-playtest/story.json');
const walk = JSON.parse(read('docs/story/alignment/evidence/walk.json'));
const manifest = JSON.parse(read('scratch/story-playtest/manifest.json'));
assert([hash(compiled), hash('\uFEFF' + compiled)].includes(walk.compiledHash), 'Browser and path validator must execute identical compiled Ink (allowing the CLI UTF-8 BOM).');
const sources = ['main.ink', 'globals.ink', 'ch01.ink', 'ch02.ink'].map(name => ({ name, sha256: hash(read('docs/story/script/' + name)) }));
assert.deepEqual(sources, walk.sources);
assert.equal(hash(JSON.stringify(sources)), manifest.sourceHash);
assert.equal(walk.sourceHash, manifest.sourceHash);
for (const name of ['walk.js', 'invariants.js']) assert.equal(hash(read('docs/story/script/check/' + name)), walk.validator[name]);
checks.push({ name: 'executed-evidence-matches-current-ink-and-validator', sourceHash: manifest.sourceHash, passed: true });
const probe = new Story(compiled);
for (const [number, stage] of [[-5,'疏離'],[0,'疏離'],[1,'疏離'],[2,'同行'],[3,'同行'],[4,'信賴'],[5,'信賴'],[6,'誓約'],[9,'誓約']]) assert.equal(probe.EvaluateFunction('stage', [number]), stage);
checks.push({ name: 'actual-ink-stage-function-boundaries', cases: 9, passed: true });
for (const [key, sample] of Object.entries(walk.samples)) {
  const s = new Story(compiled); let text = '', phase = '';
  s.onError = message => { throw Error(message); };
  function drain() {
    while(s.canContinue) {
      text += s.Continue();
      for (const tag of s.currentTags) {
        if (tag.startsWith('scene:')) phase = tag.slice(6);
        if (tag === 'speaker:薩溫' && phase !== 'L05_pre' && !s.variablesState.$('sawin_sheltered')) throw Error('Absent Sawin speaks: ' + phase);
        if (tag === 'speaker:提歐' && s.variablesState.$('teo_fate') === 'missing') throw Error('Missing Teo reappears');
        if (tag === 'speaker:伊瑟拉') assert(/L0[67]/.test(phase), 'Isera speaks before her encounter');
      }
    }
  }
  drain();
  for (const index of sample.route) { assert(s.currentChoices[index]); s.ChooseChoiceIndex(index); drain(); }
  assert.equal(s.currentChoices.length, 0);
  assert.equal(s.EvaluateFunction('name_key'), s.variablesState.$('notes_holder') === 'weide' || s.variablesState.$('starplate_holder') === 'party');
  assert(text.includes(sample.state.k1_gate === 'sealed' ? '我會選同一邊' : '如果是我，我會保住筆記'));
  if (!sample.state.notes_saved) assert(text.includes('筆記自渡口沉沒後，沒有再回到他手上'));
  assert.equal(s.variablesState.$('thoma_refused'), true);
  checks.push({ name: 'spoken-knowledge-possession-and-replay:' + key, passed: true });
}
const files = [];
function collect(dir) { for (const item of fs.readdirSync(path.join(root, dir), { withFileTypes: true })) { const p = dir + '/' + item.name; if (item.isDirectory()) collect(p); else if(p.endsWith('.md')) files.push(p); } }
collect('docs/story'); files.push('story-playtest/README.md', 'PLAN.md', 'AGENTS.md', 'docs/DECISIONS.md', 'docs/SOURCES.md', 'memory/01_active_task.md', 'memory/02_project_facts.md');
let links = 0;
for (const file of files) {
  for (const match of read(file).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const target = match[1].split('#')[0];
    if (!target || /^(https?:|mailto:)/.test(target)) continue;
    const resolved = path.resolve(root, path.dirname(file), decodeURIComponent(target));
    assert(resolved.startsWith(root + path.sep), `Escaping link ${file}: ${target}`);
    if (resolved !== path.join(root, 'docs/story/alignment/evidence/consistency.json')) assert(fs.existsSync(resolved), `Broken link ${file}: ${target}`);
    links++;
  }
}
checks.push({ name: 'local-document-links', links, files: files.length, passed: true });
const report = { passed: checks.length, failed: 0, sourceHash: manifest.sourceHash, checks, limitation: 'Semantic prose quality and unmodeled knowledge claims still need human review.' };
fs.writeFileSync(path.join(root, 'docs/story/alignment/evidence/consistency.json'), JSON.stringify(report, null, 2));
assert(fs.existsSync(path.join(root, 'docs/story/alignment/evidence/consistency.json')));
console.log(JSON.stringify({ passed: checks.length, failed: 0, links }));
