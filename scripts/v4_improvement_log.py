#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "evolution" / "improvement_candidates.jsonl"
ALLOWED_TYPES = {
    "clarify_rule", "add_failure_code", "improve_prompt", "tighten_scope", "improve_report_schema",
    "threshold_review", "failure_pattern", "report_schema_improvement", "mini_prompt_improvement",
    "scope_rule_clarification",
}
SECRET_KEYS = ("token", "secret", "password", "credential", ".env", "api_key", "apikey")

def sanitize(value, limit=1000):
    text = str(value or "")
    if any(key in text.lower() for key in SECRET_KEYS):
        return "[redacted]"
    return text[:limit]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-event", default="")
    parser.add_argument("--trigger", default="")
    parser.add_argument("--candidate-type", required=True, choices=sorted(ALLOWED_TYPES))
    parser.add_argument("--summary", required=True)
    parser.add_argument("--suggested-change", required=True)
    args = parser.parse_args()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": "robyroy-v4",
        "source_event": sanitize(args.source_event, 200),
        "trigger": sanitize(args.trigger, 200),
        "candidate_type": args.candidate_type,
        "summary": sanitize(args.summary, 500),
        "suggested_change": sanitize(args.suggested_change, 1000),
        "requires_user_approval": True,
        "auto_apply": False,
    }
    with OUT.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(json.dumps({"ok": True, "path": str(OUT), "entry": entry}, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
