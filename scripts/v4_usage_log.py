#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
EVOLUTION = BASE / "evolution"
EVENTS = EVOLUTION / "events.jsonl"
USAGE = EVOLUTION / "usage_log.jsonl"
COUNTERS = EVOLUTION / "counters.json"
IMPROVEMENTS = EVOLUTION / "improvement_candidates.jsonl"
SECRET_KEYS = ("token", "secret", "password", "credential", ".env", "api_key", "apikey")
ALLOWED_EVENTS = {
    "v4_invoked", "mode_detected", "goal_contract_created", "scope_checked", "scope_blocked",
    "unsafe_action_requested", "mini_prompt_generated", "mini_prompt_used", "mini_prompt_blocked",
    "task_step_completed", "validation_run", "report_schema_checked", "claim_risk_detected",
    "test_missing", "improvement_candidate_detected", "task_completed", "task_stopped",
    "report_schema_failure", "contract_validation_failure", "da_confermare_required",
}
THRESHOLDS = {
    "total_events_light_review": 10,
    "total_events_deep_review": 25,
    "same_failure_code": 5,
    "report_schema_failure": 3,
    "mini_prompt_blocked": 3,
    "scope_blocked": 3,
}

def now():
    return datetime.now(timezone.utc).isoformat()

def sanitize(value, limit=500):
    text = str(value or "")
    lower = text.lower()
    if any(key in lower for key in SECRET_KEYS):
        return "[redacted]"
    return text[:limit]

def load_counters():
    if COUNTERS.exists():
        try:
            data = json.loads(COUNTERS.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return {"skill": "robyroy-v4", "total_events": 0, "event_counts": {}, "failure_counts": {}, "thresholds_emitted": [], "auto_apply": False}

def save_counters(counters):
    counters["skill"] = "robyroy-v4"
    counters["auto_apply"] = False
    COUNTERS.write_text(json.dumps(counters, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def append_jsonl(path, entry):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

def candidate(candidate_type, trigger, summary, suggested_change):
    return {
        "timestamp": now(),
        "skill": "robyroy-v4",
        "candidate_type": candidate_type,
        "trigger": trigger,
        "summary": summary,
        "suggested_change": suggested_change,
        "requires_user_approval": True,
        "auto_apply": False,
    }

def maybe_emit_thresholds(counters, event_type, failure_code):
    emitted = set(counters.setdefault("thresholds_emitted", []))
    created = []
    total = int(counters.get("total_events", 0))
    checks = []
    if total and total % THRESHOLDS["total_events_light_review"] == 0:
        checks.append(("threshold_review", f"total_events:{total}:light", "Event count reached a light review threshold.", "Review recent V4 events and propose small clarity improvements only."))
    if total and total % THRESHOLDS["total_events_deep_review"] == 0:
        checks.append(("threshold_review", f"total_events:{total}:deep", "Event count reached a deeper review threshold.", "Perform a manual improvement review of recurring V4 events before editing anything."))
    counts = counters.get("event_counts", {})
    repeated = {
        "report_schema_failure": ("report_schema_improvement", "Report schema failures repeated.", "Clarify final receipt rules or report validation guidance."),
        "mini_prompt_blocked": ("mini_prompt_improvement", "Mini-prompt blocks repeated.", "Clarify mini-prompt chain stop rules or prompt templates."),
        "scope_blocked": ("scope_rule_clarification", "Scope blocks repeated.", "Clarify scope examples and forbidden target rules."),
    }
    for name, (ctype, summary, suggestion) in repeated.items():
        value = int(counts.get(name, 0))
        threshold = THRESHOLDS[name]
        if value and value % threshold == 0:
            checks.append((ctype, f"{name}:{value}", summary, suggestion))
    if failure_code:
        failures = counters.get("failure_counts", {})
        value = int(failures.get(failure_code, 0))
        if value and value % THRESHOLDS["same_failure_code"] == 0:
            checks.append(("failure_pattern", f"failure_code:{failure_code}:{value}", f"Failure code {failure_code} repeated.", "Consider a targeted rule or mini-prompt clarification after user approval."))
    for ctype, trigger, summary, suggestion in checks:
        if trigger in emitted:
            continue
        entry = candidate(ctype, trigger, summary, suggestion)
        append_jsonl(IMPROVEMENTS, entry)
        emitted.add(trigger)
        created.append(entry)
    counters["thresholds_emitted"] = sorted(emitted)
    return created

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--mode", default="")
    parser.add_argument("--risk", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--suggestion", default="")
    parser.add_argument("--failure-code", default="")
    parser.add_argument("--usage", action="store_true")
    args = parser.parse_args()
    EVOLUTION.mkdir(parents=True, exist_ok=True)
    event_type = sanitize(args.event_type, 120)
    warnings = []
    if event_type not in ALLOWED_EVENTS:
        warnings.append("event_type_not_in_declared_set")
    failure_code = sanitize(args.failure_code, 120)
    entry = {
        "timestamp": now(),
        "skill": "robyroy-v4",
        "event_type": event_type,
        "mode": sanitize(args.mode, 80),
        "risk": sanitize(args.risk, 80),
        "summary": sanitize(args.summary),
        "suggestion": sanitize(args.suggestion),
        "failure_code": failure_code,
        "auto_apply": False,
    }
    target = USAGE if args.usage else EVENTS
    append_jsonl(target, entry)
    counters = load_counters()
    counters["total_events"] = int(counters.get("total_events", 0)) + 1
    event_counts = counters.setdefault("event_counts", {})
    event_counts[event_type] = int(event_counts.get(event_type, 0)) + 1
    if failure_code:
        failure_counts = counters.setdefault("failure_counts", {})
        failure_counts[failure_code] = int(failure_counts.get(failure_code, 0)) + 1
    improvements = maybe_emit_thresholds(counters, event_type, failure_code)
    save_counters(counters)
    print(json.dumps({"ok": True, "path": str(target), "event": entry, "threshold_improvements": improvements, "warnings": warnings}, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
