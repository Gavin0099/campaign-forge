const names = ['k1_gate', 'teo_fate', 'notes_saved', 'notes_holder', 'starplate_saved', 'starplate_holder', 'sawin_sheltered', 'sawin_fate', 'isera_recruited', 'odo_recruited', 'quin_bond', 'quin_taken', 'l07_protected', 'l07_saved', 'tide', 'wick_wall', 'maggie_alive', 'trust_lis', 'trust_thoma', 'trust_isera', 'trust_sawin', 'trust_odo', 'key_explained', 'soul_cycle_known', 'thoma_refused', 'thoma_public'];
function invariants(s, { scene = '', ending = false, choices = [] } = {}) {
  const errors = [];
  const must = (condition, id) => { if (!condition) errors.push(id); };
  for (const n of ['notes_saved', 'starplate_saved', 'sawin_sheltered', 'isera_recruited', 'odo_recruited', 'quin_taken', 'maggie_alive', 'key_explained', 'soul_cycle_known', 'thoma_refused', 'thoma_public']) must(typeof s[n] === 'boolean', `type:${n}`);
  for (const n of names.filter(n => n.startsWith('trust_'))) must(Number.isInteger(s[n]) && s[n] >= -5 && s[n] <= 9, `trust:${n}`);
  must(['', 'open', 'sealed'].includes(s.k1_gate), 'enum:k1_gate');
  must(['', 'safe', 'missing'].includes(s.teo_fate), 'enum:teo_fate');
  must(['weide', 'river'].includes(s.notes_holder), 'enum:notes_holder');
  must(['tower', 'party', 'moriane'].includes(s.starplate_holder), 'enum:starplate_holder');
  must(['absent', 'party', 'injured', 'protected'].includes(s.sawin_fate), 'enum:sawin_fate');
  must(['', 'quin', 'starplate', 'sawin'].includes(s.l07_protected), 'enum:l07_protected');
  must(Number.isInteger(s.wick_wall) && s.wick_wall >= 0 && s.wick_wall <= 2, 'wick_wall');
  must(Number.isInteger(s.l07_saved) && s.l07_saved >= 0 && s.l07_saved <= 6, 'l07_saved');
  must(s.maggie_alive, 'maggie_reappeared_after_death');
  if (s.k1_gate) must(s.key_explained, 'K1_without_key_information');
  if (s.teo_fate) {
    must(s.teo_fate === (s.k1_gate === 'open' ? 'safe' : 'missing'), 'teo_continuity');
    must(s.notes_saved === (s.k1_gate === 'sealed'), 'K1_notes');
    must(s.notes_holder === (s.notes_saved ? 'weide' : 'river'), 'notes_possession');
  }
  if (s.odo_recruited) must(s.k1_gate === 'open', 'odo_unearned_recruitment');
  must(s.sawin_sheltered === (s.sawin_fate !== 'absent'), 'sawin_absent_reappearance');
  if (!s.sawin_sheltered) must(!choices.some(c => c.text.includes('擋在薩溫')), 'absent_rescue_choice');
  if (s.soul_cycle_known) must(s.isera_recruited, 'soul_knowledge_before_witness');
  if (s.thoma_public) must(s.thoma_refused && s.trust_thoma >= 3, 'public_without_courage');
  if (s.l07_protected) {
    must(s.isera_recruited && s.soul_cycle_known, 'L07_without_witness_information');
    must(s.thoma_refused, 'thoma_moral_boundary');
    must(s.thoma_public === (s.trust_thoma >= 3), 'thoma_public_threshold');
    must(s.quin_bond >= 3, 'quin_emotional_setup');
    must(s.quin_taken === (s.l07_protected !== 'quin'), 'quin_loss');
    must(s.starplate_saved === (s.l07_protected === 'starplate'), 'starplate_loss');
    must(s.starplate_holder === (s.starplate_saved ? 'party' : 'moriane'), 'starplate_possession');
    if (s.l07_protected === 'sawin') must(s.sawin_sheltered && s.sawin_fate === 'protected', 'sawin_rescue');
    else if (s.sawin_sheltered) must(s.sawin_fate === 'injured', 'sawin_injury_erased');
    must((s.notes_saved || s.starplate_saved) === (s.notes_holder === 'weide' || s.starplate_holder === 'party'), 'name_key_possession');
  }
  if (ending) {
    must(scene === 'L07_post' && !!s.l07_protected, 'unexpected_end');
    must(s.tide === 3, 'chapter_clock');
    must(s.odo_recruited === (s.k1_gate === 'open'), 'odo_route');
  }
  return errors;
}
module.exports = { invariants, names };
