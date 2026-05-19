#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CONTRACT = BASE / "contract"
REQUIRED_FILES = ["skill.contract.json", "capabilities.json", "failure_codes.json", "report_schema.json", "repair_hints.json"]
REQUIRED_FAILURE = {"RUNNER_NOT_AVAILABLE", "RUNNER_SCOPE_BLOCKED", "RUNNER_POWER_BLOCKED", "RUNNER_CHAIN_LIMIT_REACHED", "RUNNER_MANUAL_FALLBACK_USED", "SCOPE_BLOCKED", "MISSING_GOAL", "CAPABILITY_MISSING", "UNSAFE_ACTION", "CONFIG_MODIFICATION_BLOCKED", "HOOK_ACTIVATION_BLOCKED", "SELF_MODIFICATION_BLOCKED", "CLAIM_TOO_STRONG", "CLAIM_NOT_PROVEN", "TEST_MISSING", "REPORT_SCHEMA_FAILURE", "JSON_CONTRACT_INVALID", "V3_MODIFICATION_BLOCKED", "NETWORK_BLOCKED", "SUDO_BLOCKED", "GIT_PUSH_BLOCKED", "DESTRUCTIVE_ACTION_BLOCKED", "DA_CONFERMARE_REQUIRED", "MINI_PROMPT_SCOPE_BLOCKED", "MINI_PROMPT_POWER_REQUIRED", "MINI_PROMPT_CHAIN_LIMIT_REACHED", "MINI_PROMPT_GOAL_MISMATCH", "EVENT_LOGGING_FAILED", "IMPROVEMENT_THRESHOLD_REACHED"}
REQUIRED_REPORT = ["MODE", "GOAL", "SCOPE", "FILES_CREATED", "FILES_MODIFIED", "SCRIPTS_COMMANDS_USED", "TESTS_VALIDATIONS", "LIMITS", "STATUS", "NEXT_ACTION", "STOP_CONDITIONS"]
REQUIRED_RUNNER_CAPABILITIES = {"automatic_internal_runner_selection", "automatic_chain_plan_creation", "automatic_safe_build_step_execution", "runner_fallback_to_manual_report", "runner_usage_receipt"}
REQUIRED_RUNNER_BLOCKED = {"global_runtime_forcing", "daemonized_runner", "background_runner", "hook_forced_execution_without_approval", "uncontrolled_runner_loop"}
REQUIRED_CAPABILITIES = {"active_event_logging", "threshold_based_improvement_suggestion", "controlled_mini_prompt_generation", "controlled_mini_prompt_execution", "chain_step_scope_check", "chain_step_goal_alignment", "mini_prompt_blocking", "mini_prompt_receipt_generation"}
REQUIRED_BLOCKED = {"autonomous_prompt_loop", "recursive_self_invocation", "external_codex_invocation", "uncontrolled_auto_execution", "mini_prompt_power_execution_without_confirmation", "mini_prompt_out_of_scope_execution"}

def load(name, errors):
    path = CONTRACT / name
    if not path.exists():
        errors.append(f"missing {name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid json {name}: {exc}")
        return {}

def main():
    errors = []
    data = {name: load(name, errors) for name in REQUIRED_FILES}
    skill = data["skill.contract.json"]
    if skill.get("name") != "robyroy-v4":
        errors.append("skill.contract.json name must be robyroy-v4")
    if skill.get("evolution", {}).get("auto_apply") is not False:
        errors.append("skill.contract.json evolution.auto_apply must be false")
    runtime = skill.get("active_runtime_behaviors", {})
    if not runtime:
        errors.append("skill.contract.json missing active_runtime_behaviors")
    thresholds = runtime.get("improvement_suggestion_thresholds", {})
    for key in ["total_events_light_review", "total_events_deep_review", "same_failure_code", "report_schema_failure", "mini_prompt_blocked", "scope_blocked"]:
        if key not in thresholds:
            errors.append(f"missing threshold {key}")
    chain = runtime.get("controlled_mini_prompt_chain", {})
    if chain.get("enabled") is not True or chain.get("auto_loop") is not False:
        errors.append("controlled_mini_prompt_chain must be enabled with auto_loop false")
    if int(chain.get("max_chain_steps_per_task", 0)) != 3:
        errors.append("max_chain_steps_per_task must be 3")
    runner = skill.get("automatic_internal_runner_use", {})
    if runner.get("enabled") is not True:
        errors.append("automatic_internal_runner_use.enabled must be true")
    if runner.get("user_manual_launch_required") is not False:
        errors.append("automatic runner must not require manual launch")
    if runner.get("external_runtime_enforcement") is not False or runner.get("global_hooks_required") is not False:
        errors.append("automatic runner must not require external enforcement or global hooks")
    if int(runner.get("max_chain_steps_per_task", 0)) != 3:
        errors.append("automatic runner max_chain_steps_per_task must be 3")
    caps = data["capabilities.json"]
    if REQUIRED_CAPABILITIES - set(caps.get("allowed_capabilities", [])):
        errors.append("capabilities.json missing active logging or mini-prompt capabilities")
    if REQUIRED_BLOCKED - set(caps.get("blocked_actions", [])):
        errors.append("capabilities.json missing mini-prompt blocked actions")
    if REQUIRED_RUNNER_CAPABILITIES - set(caps.get("allowed_capabilities", [])):
        errors.append("capabilities.json missing automatic runner capabilities")
    if REQUIRED_RUNNER_BLOCKED - set(caps.get("blocked_actions", [])):
        errors.append("capabilities.json missing automatic runner blocked actions")
    failures = data["failure_codes.json"]
    missing_failures = sorted(REQUIRED_FAILURE - set(failures))
    if missing_failures:
        errors.append("missing failure codes: " + ", ".join(missing_failures))
    for code, spec in failures.items():
        if spec.get("severity") not in {"warn", "block"}:
            errors.append(f"{code} has invalid severity")
        if spec.get("auto_apply") is not False:
            errors.append(f"{code} auto_apply must be false")
        if not spec.get("human_message") or not spec.get("agent_next_steps") or not spec.get("allowed_repair_hints"):
            errors.append(f"{code} missing required fields")
    report = data["report_schema.json"]
    required_outputs = report.get("required_outputs", [])
    missing_outputs = [item for item in REQUIRED_REPORT if item not in required_outputs]
    if missing_outputs:
        errors.append("missing report outputs: " + ", ".join(missing_outputs))
    hints = data["repair_hints.json"]
    if not hints.get("allowed_repair_hints") or not hints.get("forbidden_repair_hints"):
        errors.append("repair_hints.json missing hint lists")
    out = {"ok": not errors, "errors": errors, "checked_files": REQUIRED_FILES}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
