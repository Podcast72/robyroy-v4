#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LOG = BASE / "logs" / "hooks_events.jsonl"
POWER = r"\b(sudo|git\s+(push|commit|reset|clean)|network|download|curl|wget|config\.toml|hooks?|rm\s+-rf|token|secret|\.env)\b"

def read_payload():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}

def text_from_payload(payload):
    for key in ("response", "final_response", "text", "message", "output"):
        if isinstance(payload.get(key), str):
            return payload[key]
    return json.dumps(payload, ensure_ascii=False)

def marker_value(text, marker):
    match = re.search(rf"^{re.escape(marker)}\s*(.*)$", text, re.M)
    return match.group(1).strip() if match else ""

def append(entry):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    payload = read_payload()
    text = text_from_payload(payload)
    allowed = marker_value(text, "V4_CONTINUE_ALLOWED:") == "YES"
    next_prompt = marker_value(text, "V4_NEXT_PROMPT:")
    step_raw = marker_value(text, "V4_CHAIN_STEP:")
    try:
        step = int(step_raw)
    except ValueError:
        step = 0
    should_continue = bool(allowed and next_prompt and 1 <= step <= 3)
    unsafe = bool(re.search(POWER, next_prompt, re.I))
    if should_continue and not unsafe:
        out = {
            "continue": True,
            "continuation_prompt": next_prompt,
            "chain_step": step,
            "systemMessage": "Robyroy-V4 Stop readiness template accepted explicit continuation markers.",
        }
        event_type = "stop_continue_allowed"
    else:
        out = {
            "continue": False,
            "stopReason": "No safe Robyroy-V4 continuation markers found." if not should_continue else "Unsafe continuation prompt blocked.",
            "blocked": bool(unsafe),
            "chain_step": step,
        }
        event_type = "stop_continue_blocked" if unsafe else "stop_no_continue"
    append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": "robyroy-v4",
        "event_type": event_type,
        "auto_apply": False,
    })
    print(json.dumps(out, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
