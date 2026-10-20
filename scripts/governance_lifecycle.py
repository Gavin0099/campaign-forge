"""Repo-local Codex lifecycle bridge. No transcript or global config access.

The installed command pins this file, Python, Git, and framework source bytes.
Stop validates a task; only SessionEnd calls the canonical closeout entry.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from contextlib import redirect_stdout

EVENTS = ("SessionStart", "UserPromptSubmit", "Stop", "SessionEnd")
READ_ONLY_GIT = {"rev-parse", "ls-tree", "show", "diff", "status", "log",
                 "ls-files", "check-ignore", "rev-list", "cat-file", "config"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(path: Path, root: Path) -> Path:
    absolute = path.absolute()
    if absolute.resolve() != absolute or not absolute.is_relative_to(root):
        raise ValueError("Redirected or out-of-workspace path")
    return absolute


def verify_binding(binding: dict) -> Path:
    root = Path(binding["root"])
    if not root.is_absolute() or root.resolve() != root:
        raise ValueError("Invalid repository root")
    for name, item in binding["executables"].items():
        if name == 'node':  # Qualified separately immediately before builds.
            continue
        path = Path(item["path"])
        if not path.is_absolute() or path.resolve() != path or not path.is_file():
            raise ValueError(f"Executable binding invalid: {name}")
        if path.stat().st_size != item["size"] or digest(path) != item["sha256"]:
            raise ValueError(f"Executable bytes changed: {name}")
    if Path(sys.executable).resolve() != Path(binding["executables"]["python"]["path"]):
        raise ValueError("Unexpected Python executable")
    for rel, expected in binding["sources"].items():
        if digest(inside(root / rel, root)) != expected:
            raise ValueError(f"Source bytes changed; reinstall and review hooks: {rel}")
    source_dirs = ("governance_tools", "runtime_hooks", "memory_pipeline")
    actual = {p.relative_to(root).as_posix()
              for folder in source_dirs
              for p in (root / "ai-governance-framework" / folder).rglob("*.py")}
    expected = {p for p in binding["sources"] if p.startswith("ai-governance-framework/")}
    if actual != expected:
        raise ValueError("Framework Python inventory changed")
    return root


def bind_git(binding: dict, root: Path) -> None:
    """Bind legacy framework bare-git calls before importing framework modules.

    Only this short-lived isolated hook process is affected. No shell or other
    child executable is permitted. Upstream source remains pinned and unedited.
    """
    original = subprocess.Popen
    item = binding["executables"]["git"]
    git = Path(item["path"])
    environment = {key: os.environ[key] for key in ("SystemRoot", "WINDIR") if key in os.environ}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0")

    class BoundGit(original):
        def __init__(self, args, *positional, **kwargs):
            if positional or not isinstance(args, (list, tuple)) or kwargs.get("shell") or kwargs.get("executable"):
                raise ValueError("Hook subprocess requires a bound argv; shells are forbidden")
            if str(args[0]) not in {"git", str(git)}:
                raise ValueError("Unbound hook subprocess")
            argv = list(map(str, args[1:]))
            check = argv[:]
            if check[:1] == ["-C"]:
                inside(Path(check[1]), root)
                check = check[2:]
            if check[:2] == ["-c", "core.quotepath=false"]:
                check = check[2:]
            if not check or check[0] not in READ_ONLY_GIT:
                raise ValueError("Git operation is outside the hook argv contract")
            if check[0] == "config" and not any(flag in check for flag in ("--get", "--get-regexp")):
                raise ValueError("Git config writes are forbidden")
            inside(Path(kwargs.get("cwd") or root), root)
            if git.stat().st_size != item["size"] or digest(git) != item["sha256"]:
                raise ValueError("Git bytes changed before launch")
            kwargs["cwd"] = str(kwargs.get("cwd") or root)
            kwargs["env"] = environment
            mode = binding.get('git_autocrlf')
            if mode not in {'true', 'false', 'input'}:
                raise ValueError('Invalid bound Git line-ending mode')
            super().__init__([str(git), '-c', 'core.autocrlf=' + mode, '-c', 'core.longpaths=true', *argv], **kwargs)

    subprocess.Popen = BoundGit
    identity = subprocess.check_output([str(git), "-C", str(root), "rev-parse",
                                       "--show-toplevel", "--absolute-git-dir", "--git-common-dir"], text=True).splitlines()
    if len(identity) != 3:
        raise ValueError("Unexpected Git repository identity response")
    top, gitdir, common = identity
    common_path = Path(common) if Path(common).is_absolute() else root / common
    if Path(top).resolve() != root or Path(gitdir).resolve() != root / ".git" or common_path.resolve() != root / ".git":
        raise ValueError("Hook repository identity mismatch; linked/redirected git dirs are unsupported")


def bind_consumer_root(root: Path) -> None:
    """Reuse the Git identity verified above for this one hook process.

    Canonical closeout rereads the same envelope many times. Its root helper
    otherwise starts Git on every read (19 launches in the measured closeout).
    Keep strict path checks on each call, accept only the already-bound root,
    and leave envelope, ownership, guard and writer validation untouched.
    """
    from runtime_hooks.core import _canonical_closeout

    def bound_root(path: Path) -> Path:
        if not path.is_absolute() or path.resolve(strict=True) != root:
            raise ValueError("Consumer root differs from the verified hook repository")
        if root.resolve(strict=True) != root or (root / '.git').resolve(strict=True) != root / '.git':
            raise ValueError("Verified hook repository was redirected")
        return root

    _canonical_closeout._consumer_worktree_root = bound_root


def safe_id(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", value):
        raise ValueError("Missing or unsafe event identity")
    if re.fullmatch(r"CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]", value, re.I):
        raise ValueError("Reserved event identity")
    return value


def write_json(path: Path, value: dict, root: Path) -> None:
    inside(path, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contract_text() -> str:
    return ("[Governance Contract]\nLANG = Python\nLEVEL = L1\nSCOPE = feature\n"
            "PLAN = ui-prototype/PLAN.md\nLOADED = SYSTEM_PROMPT,AGENTS.base.md,AGENTS.md\n"
            "CONTEXT = campaign-forge -> local governance; NOT: formal story or S4\n"
            "PRESSURE = SAFE (20/200)\nRULES = common,game-ui-prototype\n"
            "RISK = low\nOVERSIGHT = review-required\nMEMORY_MODE = candidate\n")


def prepare_observed_candidate(root: Path, session: Path, sid: str) -> None:
    """Prepare a candidate only; never invoke the canonical closeout/writer.

    The native SessionEnd budget is three seconds. R2 preparation validates the
    registered submodule and reserves shared-text ownership before that event.
    """
    from governance_tools.prepare_closeout_candidate import prepare
    verdicts = sorted(session.glob('*/post-task.json'))
    tasks = sorted(session.glob('*/task.json'))
    risks = []
    if any(not json.loads(path.read_text(encoding='utf-8')).get('ok') for path in verdicts):
        risks.append('One or more task governance verdicts failed')
    if len(tasks) > len(verdicts):
        risks.append('A submitted task has no completed post-task verdict')
    prepare(root, root / 'ai-governance-framework', sid, {
        'task_intent': 'Persist observed Campaign Forge governance task verdicts',
        'work_summary': (f'Recorded {len(verdicts)} post-task.json governance verdicts' if verdicts else 'NONE'),
        'tools_used': ['post_task_check'] if verdicts else [],
        'artifacts_referenced': [path.relative_to(root).as_posix() for path in verdicts],
        'open_risks': risks, 'checks_run': 'post_task_check' if verdicts else 'NONE',
        'not_done': 'UI behavior and full story semantics were not evaluated by the lifecycle hook',
        'recommended_memory_update': 'NO_UPDATE'})


def handle(payload: dict, event: str, binding: dict, *, replay: bool = False) -> dict:
    root = verify_binding(binding)
    if not isinstance(payload, dict) or payload.get("hook_event_name") != event:
        raise ValueError("Payload event does not match installed event")
    sid = safe_id(payload.get("session_id"))
    cwd = payload.get("cwd")
    if not isinstance(cwd, str):
        raise ValueError("Missing event cwd")
    inside(Path(cwd), root)
    if replay and not sid.startswith("acceptance-"):
        raise ValueError("Replay must use an acceptance session identity")
    bind_git(binding, root)
    sys.path.insert(0, str(root / "scripts"))
    sys.path.insert(0, str(root / "ai-governance-framework"))
    bind_consumer_root(root)
    from runtime_hooks.core._canonical_closeout import read_session_envelope
    session = inside(root / "artifacts/runtime/codex" / sid, root)
    result: dict
    if event == "SessionStart":
        from runtime_hooks.core import session_start
        from runtime_hooks.adapters.codex.session_start import run
        # Upstream identity adapter owns envelope creation and resume checks.
        result = run(payload, root)
        # The pinned context builder still calls its legacy envelope writer.
        # Supply the already-validated native identity instead of allowing that
        # writer to downgrade/recreate the root-bound envelope. Process-local
        # compatibility shim; no framework file is changed.
        envelope = read_session_envelope(sid, root)
        original_writer = session_start.write_session_envelope
        def preserve_identity(session_id, project_root, **kwargs):
            if session_id != sid or project_root.resolve() != root or envelope is None:
                raise ValueError("Context attempted to rebind native identity")
            return envelope
        session_start.write_session_envelope = preserve_identity
        try:
            context = session_start.build_session_start_context(
                project_root=root, session_id=sid, plan_path=root / "ui-prototype/PLAN.md",
                rules="common,game-ui-prototype", risk="low", oversight="review-required",
                memory_mode="candidate", contract_file=root / "contract.yaml")
        finally:
            session_start.write_session_envelope = original_writer
        result.update(ok=context["ok"], context=context)
    else:
        if read_session_envelope(sid, root) is None:
            raise ValueError("SessionStart envelope required; never borrow another session")
        if event == "UserPromptSubmit":
            from runtime_hooks.core.pre_task_check import run_pre_task_check
            turn = safe_id(payload.get("turn_id"))
            prompt = payload.get("prompt")
            if not isinstance(prompt, str):
                raise ValueError("Missing prompt")
            result = run_pre_task_check(
                project_root=root, rules="common,game-ui-prototype", risk="low",
                oversight="review-required", memory_mode="candidate", task_text=prompt,
                contract_file=root / "contract.yaml")
            # Persist authority separately; this is a bridge declaration, not a
            # claim that the assistant emitted its own governance contract.
            write_json(session / turn / "task.json", {
                "ok": result["ok"], "turn_id": turn, "session_id": sid,
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "contract": contract_text(), "declared_by": "repo_lifecycle_bridge",
                "source": "AGENTS.md and contract.yaml", "risk": "low"}, root)
        elif event == "Stop":
            from runtime_hooks.core.post_task_check import run_post_task_check
            turn = safe_id(payload.get("turn_id"))
            task = json.loads(inside(session / turn / "task.json", root).read_text(encoding="utf-8"))
            if not task.get("ok") or task.get("session_id") != sid or task.get("turn_id") != turn:
                raise ValueError("Missing or failed pre-task authority")
            response = payload.get("last_assistant_message")
            if not isinstance(response, str) or not response.strip():
                raise ValueError("Missing task response")
            result = run_post_task_check(
                response_text=task["contract"] + "\n" + response,
                risk="low", oversight="review-required", memory_mode="candidate",
                create_snapshot=False, checks={}, contract_file=root / "contract.yaml", project_root=root)
            result["contract_declaration_source"] = "repo_lifecycle_bridge"
            # Evidence/claim checks are separate from framework formatting.
            from validate_task_evidence import validate_claims
            claim_errors = validate_claims(response, root)
            result["errors"].extend(claim_errors)
            result["ok"] = result["ok"] and not claim_errors
            write_json(session / turn / "post-task.json", result, root)
        elif event == "SessionEnd":
            if payload.get("reason") != "other":
                raise ValueError("Unsupported native SessionEnd reason")
            from governance_tools import session_closeout_entry
            # Never read the platform transcript: it may live outside this repo.
            previous_argv, previous_stdin = sys.argv, sys.stdin
            sys.argv = ["session_closeout_entry", "--project-root", str(root), "--format", "json",
                        "--agent-id", "codex", "--session-id", sid, "--trigger-mode",
                        "synthetic_smoke" if replay else "native_hook"]
            if replay:
                sys.argv.append("--no-ledger-write")
            sys.stdin = io.StringIO(json.dumps({"session_id": sid}))
            capture = io.StringIO()
            try:
                with redirect_stdout(capture):
                    code = session_closeout_entry.main()
            finally:
                sys.argv, sys.stdin = previous_argv, previous_stdin
            entry = json.loads(capture.getvalue())
            receipt = {}
            receipt_name = entry.get('closeout_receipt_artifact')
            if receipt_name:
                receipt = json.loads(inside(Path(receipt_name), root).read_text(encoding='utf-8'))
            quality_ok = (entry.get('closeout_status') == 'valid' and
                          receipt.get('memory_write_claim_verified') is True and
                          (replay or receipt.get('daily_memory_write_status') in {'written', 'already_present'}))
            result = {"ok": code == 0 and quality_ok, "entry_exit_code": code,
                      "errors": [] if quality_ok else ['Canonical closeout quality or writer receipt failed'],
                      "canonical_entry": entry,
                      "ledger_write_allowed": not replay}
        else:
            raise ValueError("Unsupported event")
    if event != 'SessionEnd':
        prepare_observed_candidate(root, session, sid)
    record = {"event": event, "ok": result["ok"], "origin": "replay" if replay else "native_callback",
              "generated_at": datetime.now(timezone.utc).isoformat(), "result": result}
    write_json(session / (event + ".json"), record, root)
    if not result["ok"]:
        return {"decision": "block", "reason": "Governance check failed: " + "; ".join(result.get("errors", [])[:5])}
    if event in {"SessionStart", "UserPromptSubmit"}:
        memory = ""
        if event == "SessionStart":
            memory = "\n" + "\n".join(inside(root / rel, root).read_text(encoding="utf-8")
                                      for rel in ("memory/01_active_task.md", "memory/02_project_facts.md"))
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext":
                "Campaign Forge governance loaded: local UI/governance only; story remains S3. "
                "Before claiming tests/build pass, run scripts/record_governance_checks.py. "
                "Stop validates scope and evidence; only SessionEnd closes the session." + memory}}
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, required=True)
    parser.add_argument("--bindings-sha256", required=True)
    parser.add_argument("--event", choices=EVENTS, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    try:
        if digest(args.bindings) != args.bindings_sha256:
            raise ValueError("Bindings digest mismatch")
        binding = json.loads(args.bindings.read_text(encoding="utf-8"))
        output = handle(json.load(sys.stdin), args.event, binding, replay=args.replay)
        print(json.dumps(output, ensure_ascii=False))
        return 2 if args.event == 'SessionEnd' and output.get('decision') == 'block' else 0
    except Exception as exc:
        # Fail closed, including on a repeated Stop: no silent recursion escape.
        print(json.dumps({"decision": "block", "reason": f"Governance {args.event}: {type(exc).__name__}: {exc}"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
