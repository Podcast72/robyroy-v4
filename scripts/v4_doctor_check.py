#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REQUIRED_SCRIPTS = ["v4_mode_detect.py", "v4_scope_guard.py", "v4_report_check.py", "v4_usage_log.py", "v4_contract_check.py", "v4_doctor_check.py", "v4_improvement_log.py", "v4_prompt_runner.py", "v4_chain_guard.py", "v4_task_runner.py"]
REQUIRED_CONTRACT = ["skill.contract.json", "capabilities.json", "failure_codes.json", "report_schema.json", "repair_hints.json"]
REQUIRED_EVOLUTION = ["events.jsonl", "usage_log.jsonl", "counters.json", "improvement_candidates.jsonl", "README.md"]
BLOCKED_CLAIMS = ["production-ready", "release-ready", "secure-by-default"]
ACTIVE_FAILURES = {"RUNNER_NOT_AVAILABLE", "RUNNER_SCOPE_BLOCKED", "RUNNER_POWER_BLOCKED", "RUNNER_CHAIN_LIMIT_REACHED", "RUNNER_MANUAL_FALLBACK_USED", "MINI_PROMPT_SCOPE_BLOCKED", "MINI_PROMPT_POWER_REQUIRED", "MINI_PROMPT_CHAIN_LIMIT_REACHED", "MINI_PROMPT_GOAL_MISMATCH", "EVENT_LOGGING_FAILED", "IMPROVEMENT_THRESHOLD_REACHED"}

def json_files_ok(errors):
    for path in (BASE / "contract").glob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid json {path.name}: {exc}")

def no_auto_apply_true(errors):
    for path in list((BASE / "contract").glob("*.json")) + list((BASE / "evolution").glob("*.json")):
        text = path.read_text(encoding="utf-8").lower()
        if '"auto_apply": true' in text or '"auto_apply":true' in text:
            errors.append(f"auto_apply true found in {path}")

def claim_check(errors):
    for path in [BASE / "SKILL.md", BASE / "README.md"]:
        if path.exists():
            text = path.read_text(encoding="utf-8").lower()
            for term in BLOCKED_CLAIMS:
                if term in text and "not " + term not in text and "non " + term not in text:
                    errors.append(f"unsupported claim term in {path.name}: {term}")

def active_contract_check(errors):
    contract = json.loads((BASE / "contract" / "skill.contract.json").read_text(encoding="utf-8"))
    runtime = contract.get("active_runtime_behaviors", {})
    if not runtime:
        errors.append("active_runtime_behaviors missing")
        return
    if runtime.get("controlled_mini_prompt_chain", {}).get("auto_loop") is not False:
        errors.append("controlled mini-prompt chain auto_loop must be false")
    runner = contract.get("automatic_internal_runner_use", {})
    if runner.get("enabled") is not True:
        errors.append("automatic_internal_runner_use missing or disabled")
    if runner.get("user_manual_launch_required") is not False:
        errors.append("automatic runner must not require Roberto manual launch")
    if runner.get("external_runtime_enforcement") is not False or runner.get("global_hooks_required") is not False:
        errors.append("automatic runner must not require external runtime enforcement or hooks")
    thresholds = runtime.get("improvement_suggestion_thresholds", {})
    for key in ["total_events_light_review", "total_events_deep_review", "same_failure_code", "report_schema_failure", "mini_prompt_blocked", "scope_blocked"]:
        if key not in thresholds:
            errors.append(f"threshold missing: {key}")
    failures = json.loads((BASE / "contract" / "failure_codes.json").read_text(encoding="utf-8"))
    missing = sorted(ACTIVE_FAILURES - set(failures))
    if missing:
        errors.append("missing active failure codes: " + ", ".join(missing))

def config_hook_check(errors):
    active_markers = ["active = true", "enabled = true"]
    for path in (BASE / "config").glob("*.toml"):
        text = path.read_text(encoding="utf-8").lower()
        for marker in active_markers:
            if marker in text and not text[text.find(marker)-3:text.find(marker)].strip().startswith("#"):
                errors.append(f"active config marker found in proposal file: {path.name}")

def main():
    errors = []
    warnings = []
    if not (BASE / "SKILL.md").exists():
        errors.append("SKILL.md missing")
    for name in REQUIRED_CONTRACT:
        if not (BASE / "contract" / name).exists():
            errors.append(f"contract missing {name}")
    for name in REQUIRED_SCRIPTS:
        if not (BASE / "scripts" / name).exists():
            errors.append(f"script missing {name}")
    for name in REQUIRED_EVOLUTION:
        if not (BASE / "evolution" / name).exists():
            errors.append(f"evolution missing {name}")
    json_files_ok(errors)
    no_auto_apply_true(errors)
    claim_check(errors)
    active_contract_check(errors)
    config_hook_check(errors)
    contract = subprocess.run([sys.executable, str(BASE / "scripts" / "v4_contract_check.py")], text=True, capture_output=True)
    if contract.returncode != 0:
        errors.append("contract check failed")
        warnings.append(contract.stdout.strip() or contract.stderr.strip())
    out = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
