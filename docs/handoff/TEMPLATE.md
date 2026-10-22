# Handoff: <branch>

<!-- Copy to docs/handoff/<branch-with-slashes-as-dashes>.md. Codex fills sections 1–6. Facts only; mark anything unverified. -->

| Field | Value |
| --- | --- |
| Branch | `codex/<task>` |
| Base | `origin/main` @ `<sha>` |
| Head | `<sha>` (pushed: yes / no) |
| Owner instruction | <quote or summary of the instruction this chunk answers> |
| Time window (Asia/Taipei) | <start> – <end> |

## 1. What changed

- <user-visible change> — `<path>`
- Shared files edited: <path list, or NONE>

## 2. How to verify

Run from the worktree root on Windows PowerShell. List every command with the result you got.

| Command | Expected | Your result (exit code) |
| --- | --- | --- |
| `npm run build --prefix ui-prototype` | build succeeds | |
| `python scripts/validate_ui_scope.py` | PASS | |
| <browser check, resolution, route> | <what to see> | |

Screenshots / recordings: `<path>` (captured from the running build, not generated).

## 3. Not done / known limits

- <what is incomplete, placeholder, or failing>

## 4. Risks

- <what might break or be wrong; NONE if none>

## 5. Open questions

- For Claude (review): <specific question>
- For Gavin (decision): <decision needed, options and cost of each>

## 6. Not claimed

- Owner approval, human playtest, commercial art approval, native hook callback: <list what this handoff does not prove>

---

## Review

Claude writes findings in `docs/review/<same-slug>.md` on `review/<task>`, not here.
