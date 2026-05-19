#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ALLOWED_BASE = BASE.resolve(strict=False)
POWER_PATTERNS = {
    "network": r"\b(network|internet|download|curl|wget|fetch)\b",
    "sudo": r"\bsudo\b",
    "git_push": r"\bgit\s+push\b",
    "git_commit": r"\bgit\s+commit\b",
    "git_mutation": r"\bgit\s+(reset|clean|checkout|tag)\b",
    "config": r"\bconfig\.toml\b",
    "hooks": r"\b(hook|hooks|activate\s+hook|attiva\s+hook)\b",
    "destructive": r"\brm\s+-rf\b|\bdelete\b|\bcancella\b",
    "install": r"\b(install|npm\s+install|pip\s+install|brew\s+install)\b",
    "secret": r"\b(token|secret|password|credential|\.env)\b",
    "v3": r"\brobyroy-v3\b",
}

def now():
    return datetime.now(timezone.utc).isoformat()

def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False

def power_flags(text):
    return [name for name, pattern in POWER_PATTERNS.items() if re.search(pattern, text or "", re.I)]

def log_event(event_type, mode, risk, summary, failure_code=""):
    cmd = [
        sys.executable,
        str(BASE / "scripts" / "v4_usage_log.py"),
        "--event-type", event_type,
        "--mode", mode,
        "--risk", risk,
        "--summary", summary,
    ]
    if failure_code:
        cmd.extend(["--failure-code", failure_code])
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=10)
        return {"ok": proc.returncode == 0, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

def chain_guard(goal, prompt, mode, step_index, max_steps):
    cmd = [
        sys.executable,
        str(BASE / "scripts" / "v4_chain_guard.py"),
        "--current-goal", goal,
        "--mini-prompt-text", prompt,
        "--mode", mode,
        "--step-index", str(step_index),
        "--max-steps", str(max_steps),
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"allowed": False, "reason": "chain guard returned invalid JSON", "failure_code": "RUNNER_SCOPE_BLOCKED", "requires_user_confirmation": False}
    return data

def build_steps(goal, mode, max_steps):
    templates = [
        ("create_goal_contract", f"Create or update the Goal Contract for: {goal}"),
        ("run_scope_check", f"Check scope and forbidden targets for: {goal}"),
        ("validate_report", f"Validate the final report for: {goal}"),
    ]
    return templates[:max_steps]

def run(goal, workspace, mode, max_steps, dry_run):
    workspace_path = Path(workspace).expanduser().resolve(strict=False)
    mode = mode.upper()
    events = []
    report = {
        "timestamp": now(),
        "skill": "robyroy-v4",
        "runner": "v4_task_runner",
        "goal": goal,
        "workspace": str(workspace_path),
        "mode": mode,
        "dry_run": dry_run,
        "max_steps": max_steps,
        "manual_launch_required": False,
        "external_runtime_enforcement": False,
        "global_hooks_required": False,
        "ok": True,
        "status": "runner_plan_created",
        "failure_code": "",
        "steps": [],
        "events": events,
        "limits": [
            "internal skill orchestration only",
            "SAFE/BUILD steps only",
            "no daemon",
            "no background service",
            "no global hooks",
            "no external automation",
        ],
    }
    if max_steps > 3:
        report.update(ok=False, status="blocked", failure_code="RUNNER_CHAIN_LIMIT_REACHED")
        return report
    if not inside(workspace_path, ALLOWED_BASE):
        report.update(ok=False, status="blocked", failure_code="RUNNER_SCOPE_BLOCKED")
        return report
    flags = power_flags(goal)
    if mode not in {"SAFE", "BUILD"} or flags:
        report.update(ok=False, status="blocked", failure_code="RUNNER_POWER_BLOCKED")
        events.append(log_event("task_stopped", mode, "high", "runner blocked goal requiring POWER or forbidden action", "RUNNER_POWER_BLOCKED"))
        return report
    events.append(log_event("task_step_completed", mode, "low", "runner created controlled chain plan"))
    for index, (mini_prompt_id, prompt) in enumerate(build_steps(goal, mode, max_steps), start=1):
        events.append(log_event("mini_prompt_generated", mode, "low", f"runner generated {mini_prompt_id}"))
        guard = chain_guard(goal, prompt, mode, index, max_steps)
        step = {
            "step_index": index,
            "mini_prompt_id": mini_prompt_id,
            "prompt_text": prompt,
            "guard": guard,
            "executed": False,
            "dry_run": dry_run,
        }
        if not guard.get("allowed"):
            report.update(ok=False, status="blocked", failure_code=guard.get("failure_code") or "RUNNER_SCOPE_BLOCKED")
            step["blocked"] = True
            events.append(log_event("mini_prompt_blocked", mode, "medium", f"runner blocked {mini_prompt_id}", report["failure_code"]))
            report["steps"].append(step)
            return report
        step["blocked"] = False
        step["executed"] = not dry_run
        events.append(log_event("mini_prompt_used", mode, "low", f"runner accepted {mini_prompt_id}"))
        report["steps"].append(step)
    report["status"] = "dry_run_completed" if dry_run else "completed"
    return report

def main():
    parser = argparse.ArgumentParser(description="Robyroy-V4 controlled internal task runner.")
    parser.add_argument("--goal", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--mode", default="SAFE")
    parser.add_argument("--max-steps", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report-json", action="store_true")
    args = parser.parse_args()
    report = run(args.goal, args.workspace, args.mode, args.max_steps, args.dry_run)
    if args.report_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("ok") else 1

if __name__ == "__main__":
    raise SystemExit(main())
