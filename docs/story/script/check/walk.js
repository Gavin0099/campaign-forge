const {Story}=require(process.env.INKJS||'inkjs');const j=require('fs').readFileSync(process.argv[2]||'/tmp/out.json','utf8').replace(/^\uFEFF/,'');
let ends=0,errs=[],combos={};
function v(s,n){return s.variablesState.$(n)}
const s=new Story(j);s.onError=(m)=>errs.push(m);
function run(path,snap){if(snap)s.state.LoadJson(snap);
 while(s.canContinue)s.Continue();
 if(s.currentChoices.length){const here=s.state.ToJson();const m=s.currentChoices.length;let n=0;for(let i=0;i<m;i++){s.state.LoadJson(here);s.ChooseChoiceIndex(i);n+=run(path.concat([i]),null)}return n}
 ends++;const k1=v(s,'k1_gate'),teo=v(s,'teo_fate'),notes=v(s,'notes_saved'),qt=v(s,'quin_taken'),sp=v(s,'starplate_saved');
 const bad=[];
 if(!(k1==='open'&&teo==='safe'&&!notes)&&!(k1==='sealed'&&teo==='missing'&&notes))bad.push('K1/teo/notes mismatch');
 if(!qt&&sp)bad.push('quin saved and starplate saved together');
 if(v(s,'tide')!==3)bad.push('tide');
 if(v(s,'quin_bond')<2)bad.push('quin_bond low');
 if(bad.length)errs.push(path.join('')+':'+bad);
 const key=`${k1}|quin_taken=${qt}|starplate=${sp}|sawin=${v(s,'sawin_sheltered')}`;combos[key]=(combos[key]||0)+1;return 1}
const n=run([]);console.log('terminal paths',n,'errors',errs.length);errs.slice(0,5).forEach(e=>console.log(e));
console.log(Object.entries(combos).map(e=>e.join(' x')).join('\n'));
