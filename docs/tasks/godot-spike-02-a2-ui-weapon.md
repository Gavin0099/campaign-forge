# Task Godot spike 02 A2: Thoma's own weapon, a tactics-RPG battle HUD, knight readability

Authorized by Gavin on 2026-10-23 (Asia/Taipei): 「先修介面和 Thoma 的劍，再做比較」 ("Fix the UI and Thoma's sword first, then do the comparison").

This is a **small fix segment** on top of spike-02 Phase A (`46edbc6`). It runs **before** Phase B. **Do not start Phase B** (the React vs Godot A/B in `docs/tasks/godot-spike-02-swing-and-ab.md`). The engine decision (P010) stays **PROPOSED**.

## Why
The GPT review of Phase A (`docs/review/gpt-godot-spike-02a.md` on `origin/review/gpt-godot-spike`, commit `1238310`) returned **CONDITIONAL ACCEPT**, no P0. Its open P1 items, which this segment fixes:
1. **Weapon identity.** Thoma's original crop is empty-handed, so the 6 swing frames borrowed the sword of another party member (Karen, column 1 of `l03-party-v1.png`). All six are **PLACEHOLDER**. The weapon does not match the character, and the swing still reads weak (score: weapon and motion consistency 55/100).
2. **UI is NOT FIXED.** The default view still shows the scenario number, a hotkey line and technical status text. There is no tactics-RPG information hierarchy (score: UI blending into the battlefield 40/100).
3. **Knight readability.** Knight A and knight B are still hard to tell apart at a distance, and the 1.5× attack zoom overlaps a little.

Read first: that review (`git fetch origin review/gpt-godot-spike` then `git show origin/review/gpt-godot-spike:docs/review/gpt-godot-spike-02a.md`), the **"spike-02 Phase A"** section of `godot-spike/docs/HANDOFF.md`, `godot-spike/docs/ANIMATION-ADAPTER.md`, `shared-anim/README.md`, `shared-anim/SOURCES.md`, `shared-anim/manifest.json`, `godot-spike/scripts/skirmish.gd`, `godot-spike/tests/*`, `ui-prototype/docs/playable-l03-p1v3/STYLE.md`, `ui-prototype/docs/playable-l03-p1v4/STYLE.md`, and `docs/review/RESOURCE-CHECKLIST.md` (game-feel, game-ui-ux).

## Thoma's weapon: what the repo says (researched for this brief)
The canon **does not name a weapon** for Thoma. Evidence:
- `ui-prototype/docs/l03/character-prompt.txt:1`: Thoma is an "older male medical friar … gray hair and short gray beard, layered muted teal robe and ivory stole, plain satchel with linen rolls, small simple brass medallion, **empty hands, no staff or book or magical glow**".
- `ui-prototype/docs/l03/ART-DIRECTION.md:9`: 「右托瑪醫療袋／青綠」 (medical satchel, teal). `ui-prototype/src/l03Scene.ts:51–54`: 托瑪, role 「醫療與支援」.
- `ui-prototype/docs/playable-l03-research/DEMO-CONTRACT.md:17`: Thoma has melee 3 (近戰3) and heals 3, so a melee strike is in his kit.
- On `origin/story/strengthen-narrative`: `docs/story/STORY.md:56` 「托瑪・赫斯特修士｜牧師：治療、驅散亡魂、祝福｜Cleric｜黎明誓院的醫療修士」; `docs/story/COMPANION-ARCS.md:28` 「托瑪・赫斯特修士（牧師，Cleric）」; `COMPANION-ARCS.md:34` and `docs/story/script/ch01.ink:306` / `ch02.ink:250`: he carries a **聖徽** (holy symbol) that he grips. `docs/story/CREATIVE-BIBLE.md:74`: 「托瑪的年齡、法衣與聖徽要獨立審查」. None of these names a weapon.
- `docs/DECISIONS.md:35` (U003): party is built on a D&D-style class frame (fighter, wizard, cleric, rogue), with original content.
- `shared-anim/README.md` "Provenance caveat": the Phase A sword is Karen's, explicitly PLACEHOLDER, "not an equipment or story decision".

**Decision for this segment: the canon is silent, so you propose a weapon, label it `PROPOSED` (Owner confirmation pending) in the handoff, SOURCES.md and frame-audit.json, and still implement it.**
- It must fit an **older medical friar / cleric** (黎明誓院 healer, carries a holy symbol, not a soldier) and the existing portrait silhouette (teal robe, ivory stole, satchel, brass medallion; no staff).
- **Default proposal: a short one-handed flanged mace** (dark iron head, worn oak haft, small brass collar echoing his medallion), about forearm length, carried in his right hand. Rationale: the classic cleric weapon, blunt rather than bladed (fits a healer), short enough not to read as a staff, and it gives a weighty blunt impact. You may propose a different weapon only if it fits the same constraints better (for example a brass-bound oak cudgel); state the reason in the handoff.
- Not allowed: any sword or blade, a staff or quarterstaff (contradicts `character-prompt.txt`), a book or magic glow, or anything copied from another party member. The holy symbol stays a medallion, not a weapon.

## Hard boundaries
- Work only in the worktree `D:\campaign-forge\scratch\godot-spike`, branch `codex/godot-spike`. It must start clean at this brief's commit (on top of `46edbc6`). Do not touch the main checkout `D:\campaign-forge` or any other `scratch/*` worktree.
- You may change only `shared-anim/`, `godot-spike/` and this segment's handoff section. **Do not change anything under `ui-prototype/`.** You may *read* files there and *copy* bytes from them into `godot-spike/` (for example a portrait crop), recorded in SOURCES.md. Never edit or move original PNGs.
- Godot 4.7.2 standard build, **GDScript only**. No C#, no GDExtension, no new addons beyond the vendored GUT.
- No rules changes. Forecast numbers come from the existing rules events (`scripts/rules/grid_rules.gd`). G005 is untouched.
- Do not adopt the on-hold Ferry Dusk palette. Do not regenerate the battlefield, props or any character other than the frames listed below.
- The total normal attack (strike to input-ready) must stay **≤ 1.7 s**, and close to the current 0.91–0.92 s unless a stated reason justifies more weight.
- `rg` is not installed; use `Select-String` or `git grep`.

## Do
Work in order. **Commit after each step.**

### W1. Thoma's weapon and swing frames
- Write the weapon proposal in `shared-anim/README.md` (replace the Provenance caveat): the weapon, why it fits, and the evidence list above, marked **PROPOSED, Owner confirmation pending**.
- **New idle frame `thoma/idle/01.png`** (or replace `thoma/idle/00` and keep the original crop as a reference only; document which): Thoma holding the proposed weapon at rest, identical to the original crop in face, robe, stole, satchel, medallion, proportions, palette and light. The manifest must use the weapon idle as the rest pose, so idle and swing are consistent (the weapon must no longer appear and disappear).
- **Repaint all 6 swing frames** with Thoma's own weapon, same canvas 512×512 and pivot `[256,464]`:
  1. **anticipation**: a clear, readable wind-up: weight shifted back, weapon cocked high or behind, body coiled. It must read at 720p in silhouette.
  2. **raise / start of swing**.
  3. **swing with a painted smear or arc** for the weapon head (hand-painted, same palette, not a vector streak). Reduced Motion must not show the smear.
  4. **contact**: a stronger contact pose: weight fully forward, arms extended, weapon head on the target's contact anchor.
  5. **follow-through**.
  6. **recover**, ending compatible with the new weapon idle.
- Adjust manifest timing if it helps weight (for example a slightly longer anticipation hold and a faster swing), keeping the ≤ 1.7 s budget, and update the contact anchor/events to the new weapon head.
- **Image generation is allowed for these 7 Thoma frames only**, using the original Thoma crop (`references/thoma.png`) and the new idle as references. Do **not** use Karen's sword or `references/sword-reference.png`. At most **3 attempts per frame**. Clean each frame as in Phase A (alpha, halo, registration to the pivot, palette mapping from the source crop).
- Record every attempt in `shared-anim/SOURCES.md` and `generation-prompts.json`: tool, full prompt, references, raw and runtime SHA-256, cleanup. Rejected attempts stay out of the runtime folder (a few in `shared-anim/rejected/`, listed).
- **Style check:** make `shared-anim/thoma-weapon-style-check.png`: the original crop, the new idle, and all 6 swing frames side by side at the same scale on a neutral dark background, plus one row at 720p in-game size. Self-review each frame for face, costume, proportions, palette, light direction and stroke. **Remove PLACEHOLDER only for frames that pass**; keep the rest PLACEHOLDER with the reason in `frame-audit.json`. Weapon identity stays **PROPOSED** regardless.
- Re-run the sync step so `godot-spike/art/anim-shared/` matches byte for byte. Regenerate `shared-anim/contact-sheet.png`.
- Commit.

### W2. Tactics-RPG battle HUD (Godot only)
Reference genre conventions (曹操傳, Fire Emblem, Tactics Ogre) for the **information hierarchy only**. All art and layout are original.
- **Remove from the default view:** the scenario number/title, the hotkey line, phase or timing text and any technical status. Debug stays behind **F1** (and backtick). Add a small, dismissable **help overlay on `?` or `H`** listing the controls in Traditional Chinese. Both are off by default.
- **Information hierarchy:**
  - **Selected-unit panel** (bottom-left): painted portrait crop of the unit, name (托瑪), class or role line (修士／醫療), HP bar with numbers, and one short in-world status line. Styled like the game, not a dev panel.
  - **Attack forecast panel** while the attack is armed and before contact: attacker vs target, side by side with portraits; damage (from the rules event), the target's HP before → after, and the outcome: 擊退一格 for open, or 受阻 with the reason (被友軍阻擋 / 被斷橋阻擋) for blocked. Values must come from the rules result, not hard-coded.
  - **Turn or phase banner**: a short painted banner such as 「我方回合」 that slides in and out at the start, not a persistent label.
  - **HP bars or pips over units**, small, in the bone/brass palette, readable at 720p, hidden or dimmed during hitstop only if that looks better (document).
  - Scenario switching (1/2/3) stays on keys; if you keep a visible control, make it an in-world styled tab, not a debug button.
- **Look:** framed, painted-style panels consistent with the P1v3 UI frame rules in `ui-prototype/docs/playable-l03-p1v3/STYLE.md` and P1v4 STYLE.md (dark iron/moss panel fill, brass trim, bone text). If no reusable frame asset exists, make a simple **9-slice** frame texture (`NinePatchRect` / `StyleBoxTexture`) in that style under `godot-spike/art/ui/`, procedural or hand-cleaned, with provenance in `godot-spike/art/SOURCES.md`. No new character art for the UI beyond portrait crops of existing sprites (Thoma from `l03-party-v1.png`; knights from `l03-enemies-v1.png` and `ui-prototype/public/art/l03-p1v4/knight-2-portrait.png` if suitable, copied, not edited).
- **Text:** all player-facing labels in Traditional Chinese, with a font that renders CJK at 720p (use a system/bundled font already available or document a fallback; do not add a font file without a license note). Check contrast of every text/background pair against **WCAG AA** (4.5:1 normal, 3:1 large) and save the table to `godot-spike/docs/evidence/spike02-a2/contrast.json`.
- HUD stays in the always-processing CanvasLayer, so hitstop does not freeze it. Keyboard focus and input locks behave as in Phase A.
- Commit.

### W3. Knight readability
- Make knight A and knight B distinguishable at 720p **in the default (unzoomed) view and when zoomed**, without relying on the HUD: a distinct silhouette element or a strong color accent (for example a different helm crest/plume or shield device), applied consistently across knight B's idle, hit and stagger frames. Image editing of the existing knight B frames is allowed (max 3 attempts per frame, logged); prefer a scripted, consistent edit.
- Add a small name/role tag per knight in the HUD (for example 「議會騎士・甲」/「議會騎士・乙」 or role names), shown in the forecast and on hover/selection, not as permanent debug labels.
- Prove grayscale distinguishability again (`knights-grayscale.png`).
- **Fix the zoom overlap:** adjust zoom framing (focus point, zoom factor) and/or unit offsets so non-participant units never overlap and the attacker/target overlap is only at the intended contact. Re-run the silhouette overlap measurement for all three setups at rest and at contact, and save it as `readability-overlap.json`.
- Commit.

### W4. Tests (GUT, headless)
- All 24 existing tests keep passing. Add tests:
  - **No debug text by default:** after scene load, no visible HUD node contains the scenario number, hotkey text, phase/timing text or other diagnostic strings; after F1 they are visible; the help overlay is hidden by default and toggles with ?/H.
  - **Forecast matches rules:** for each of the three setups, the forecast panel's damage, HP before/after and outcome (擊退 / 受阻 + reason) equal the values in the rules result events.
  - **Manifest still validates:** schema-required fields, every frame exists, the contact index is in range, the idle sequence includes the weapon idle, and hash parity holds after sync.
  - **Knight identity:** knight A and knight B use different textures in every sequence.
  - **Timing:** every scenario is ≤ 1.7 s.
- Save the log to `godot-spike/docs/evidence/spike02-a2/test-run.log`.
- Commit.

### W5. Evidence and verification commit
In `godot-spike/docs/evidence/spike02-a2/`, from a rendered 1280×720 run with a `CAPTURE_COMPLETE … pass=true` marker:
- `default-view.png` (no debug, no hotkeys), `selected-unit.png`, `attack-forecast.png` (open), `forecast-blocked-unit.png`, `forecast-blocked-terrain.png`, `contact.png` (during hitstop), `blocked-stagger.png`, `help-overlay.png`, `debug-f1.png`, `knights-default-view.png`, `knights-zoomed.png`, `knights-grayscale.png`;
- `thoma-weapon-style-check.png` (copy of the W1 sheet);
- a `--write-movie` capture at `--fixed-fps 60` of the open attack from strike to input-ready (subsample if over about 8 MB; document what was kept);
- `timing.json` (normal and Reduced Motion, all three setups), `contrast.json`, `readability-overlap.json`.
- Add a **"spike-02 A2"** section to `godot-spike/docs/VERIFICATION.md` with the commands actually run and their real exit codes.
- Make this the verification commit.

### W6. Handoff, then stop
Add a section **"spike-02 A2"** to `godot-spike/docs/HANDOFF.md`:
- how to run it (sync, import, play; F1 debug; ?/H help);
- each of the three GPT P1 items above: what changed, with evidence links;
- **Thoma's weapon: PROPOSED**, with the evidence list and the rationale, for Owner confirmation;
- the frame table with PASS / PLACEHOLDER per frame and the style-check link;
- the HUD hierarchy and the contrast results;
- knight readability and overlap results;
- timing against the 1.7 s budget;
- limits and a resource self-check against `docs/review/RESOURCE-CHECKLIST.md`. Human playtest stays **HUMAN_PENDING**; P010 stays **PROPOSED**.
- Make this the handoff commit, then **stop**. Phase B remains unstarted.

## Acceptance
- GUT exits 0 with the log committed; the 24 old tests plus the new ones pass.
- Thoma holds his own (PROPOSED) weapon in idle and in all swing frames; no frame uses Karen's sword. The style-check sheet is committed and the PLACEHOLDER flags are honest.
- The default view shows no scenario number, hotkey list or technical text; debug is behind F1 and help behind ?/H.
- The selected-unit panel, forecast panel, turn banner and unit HP bars exist, in Traditional Chinese, with WCAG AA contrast recorded.
- The forecast values equal the rules events in all three setups (tested).
- The knights are distinguishable unlabeled at 720p and in grayscale, and there is no non-participant overlap when zoomed (measured).
- Every scenario is ≤ 1.7 s, measured.
- `git diff --stat 46edbc6..HEAD` shows changes only under `shared-anim/`, `godot-spike/` and this brief. Nothing under `ui-prototype/` changes.

## Stop
**Commit only.** Do not push; the Owner's agent pushes afterwards. Do not merge to main, open a PR or use git stash. Stop after the W6 handoff commit and wait for review.
