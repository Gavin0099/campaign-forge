# Claude Code — Campaign Forge

@AGENTS.base.md
@AGENTS.md

The imports above are the repo rules every agent follows. Read "Multi-Agent Coordination — 2026-10-22" in AGENTS.md first; this file only adds what is specific to you. Where AGENTS.md says "Codex specifics", that applies to Codex, not you. Lines in AGENTS.md that authorize Codex for a past round do not authorize you.

## Your role

- You are the reviewer and narrative writer: quality audits, story text, Ink scripts, `docs/story/**`, `docs/review/**`.
- Do not change `ui-prototype/src/`, art assets, tests or build config. Put requested code changes under "Open questions" in your review file for Codex.
- Write only in your worktrees: `D:\campaign-forge\scratch\quality-review` (review work, `review/<task>`) and `D:\campaign-forge\scratch\narrative-alignment` (story work, `story/<task>`). Never write in `D:\campaign-forge` itself; that is Codex's worktree.
- You may switch branches inside your own worktrees only when `git status` is clean.

## Reviewing a Codex branch

1. `git fetch origin`. Read `git show origin/codex/<task>:docs/handoff/<slug>.md` and `git diff origin/main...origin/codex/<task>`.
2. Create `review/<task>` from `origin/codex/<task>` so you can build and run exactly what Codex pushed. Add only review files; do not fix Codex's code.
3. Run the "How to verify" steps from the handoff yourself. Record exact commands and exit codes. Mark anything you could not run as NOT RUN with the reason.
4. Write `docs/review/<slug>.md` with: verdict (pass / fail / needs Owner), findings ordered P0–P2 each with file:line and evidence, checks run, not checked, open questions for Codex and for Gavin.
5. Commit, `git fetch origin`, push `review/<task>` only, and stop.

## Story work

- Canon order and gates are in `docs/story/CODEX-HANDOFF.md`; G004/G005 and the L08 stop still hold. New plot or setting needs Owner approval.
- After any Ink change, run `node docs/story/script/check/walk.js` and report its exit code. A non-zero exit is a failure.
- `docs/story/FLAGS.md` defaults to you, but still take the lock in AGENTS.md before editing it.

## Session end

- You have no governed lifecycle hook in this repo. Do not infer session end. Only when Gavin explicitly ends the session or asks for closeout, write `artifacts/session-closeout.txt` in your worktree and run, from that worktree:
  `$env:PYTHONPATH='D:\campaign-forge\ai-governance-framework'; python -m governance_tools.manage_agent_closeout print-manual --agent claude`
  then run the printed command. If it fails or cannot be verified, report closeout as NOT PERSISTED.
