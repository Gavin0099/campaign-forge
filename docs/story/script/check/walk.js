/* Execute the actual Ink at every choice boundary. Enumeration is not player probability. */
const fs = require('node:fs');
const path = require('node:path');
const { Story } = require(process.env.INKJS || 'inkjs');
const { invariants, names } = require('./invariants.js');
const file = process.argv[2];
if (!file) throw Error('Usage: node check/walk.js compiled.json [--out=report.json] [--inject=fault]');
const inject = process.argv.find(x => x.startsWith('--inject='))?.slice(9);
const out = process.argv.find(x => x.startsWith('--out='))?.slice(6);
const story = new Story(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const report = { terminalPaths: 0, choiceBoundaries: 0, errors: [], combinations: {}, thoma: { refused: 0, public: 0 }, sceneVisits: {}, samples: {} };
const crypto = require('node:crypto');
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
report.compiledHash = digest(fs.readFileSync(file));
report.sources = ['main.ink', 'globals.ink', 'ch01.ink', 'ch02.ink'].map(name => ({ name, sha256: digest(fs.readFileSync(path.join(__dirname, '..', name))) }));
report.sourceHash = digest(JSON.stringify(report.sources));
report.validator = Object.fromEntries(['walk.js', 'invariants.js'].map(name => [name, digest(fs.readFileSync(path.join(__dirname, name)))]));
report.l07Saved = {};
story.onError = message => { throw Error(message); };
let injected = false;
function state() { return Object.fromEntries(names.map(n => [n, story.variablesState.$(n)])); }
function run(route, scene = '', ending = false) {
  while (story.canContinue) {
    story.Continue();
    for (const tag of story.currentTags) {
      if (tag.startsWith('scene:')) { scene = tag.slice(6); report.sceneVisits[scene] = (report.sceneVisits[scene] || 0) + 1; }
      if (tag === 'ending:L07') ending = true;
    }
  }
  const choices = story.currentChoices.map(c => ({ index: c.index, text: c.text }));
  if (!injected && inject && scene === 'L07_post') {
    const faults = {
      notes: ['notes_holder', story.variablesState.$('notes_holder') === 'weide' ? 'river' : 'weide'],
      starplate: ['starplate_holder', story.variablesState.$('starplate_holder') === 'party' ? 'moriane' : 'party'],
      resurrection: ['teo_fate', story.variablesState.$('teo_fate') === 'safe' ? 'missing' : 'safe'],
      absent: ['sawin_fate', story.variablesState.$('sawin_sheltered') ? 'absent' : 'protected'],
      knowledge: ['key_explained', false], soul_knowledge: ['soul_cycle_known', false],
      trust: ['trust_thoma', 99], refusal: ['thoma_refused', false],
      public: ['thoma_public', !story.variablesState.$('thoma_public')], tide: ['tide', 2],
      loss: ['quin_taken', !story.variablesState.$('quin_taken')], recruitment: ['isera_recruited', false],
      death: ['maggie_alive', false], count: ['l07_saved', 7],
    };
    if (!faults[inject]) throw Error('Unknown injection');
    story.variablesState.$(...faults[inject]);
    injected = true;
  }
  const value = state();
  const errors = invariants(value, { scene, ending, choices });
  if (errors.length) throw Error(JSON.stringify({ route, scene, errors }));
  if (!choices.length) {
    if (!ending) throw Error('Unexpected termination before L07: ' + route.join(','));
    report.terminalPaths++;
    const key = `${value.k1_gate}|${value.l07_protected}|sawin=${value.sawin_sheltered}`;
    report.combinations[key] = (report.combinations[key] || 0) + 1;
    report.thoma.refused += Number(value.thoma_refused);
    report.thoma.public += Number(value.thoma_public);
    report.l07Saved[value.l07_saved] = (report.l07Saved[value.l07_saved] || 0) + 1;
    const sampleKey = `${key}|public=${value.thoma_public}`;
    if (!report.samples[sampleKey]) report.samples[sampleKey] = { route, state: value };
    return;
  }
  report.choiceBoundaries++;
  const snapshot = story.state.ToJson();
  for (const choice of choices) {
    story.state.LoadJson(snapshot);
    story.ChooseChoiceIndex(choice.index);
    run(route.concat(choice.index), scene, ending);
  }
}
try {
  run([]);
  if (inject) throw Error('Fault injection unexpectedly survived: ' + inject);
  if (Object.keys(report.combinations).length !== 10) throw Error('Missing K1 × protection × recruitment combinations');
} catch (error) {
  report.errors.push(error.message);
  process.exitCode = 1;
}
report.exitCode = process.exitCode || 0;
console.log(JSON.stringify(report, null, 2));
if (out) { fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(report, null, 2) + '\n'); }
