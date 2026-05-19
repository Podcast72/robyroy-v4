#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LOG = BASE / "logs" / "hooks_events.jsonl"
SECRET_WORDS = ("token", "secret", "password", ".env", "api key", "apikey", "credential")

def sanitize(text):
    text = str(text or "")
    if any(word in text.lower() for word in SECRET_WORDS):
        return "[redacted]"
    return text[:300]

def read_payload():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}

def find_prompt(payload):
    for key in ("prompt", "user_prompt", "input", "text"):
        if isinstance(payload.get(key), str):
            return payload[key]
    return json.dumps(payload, ensure_ascii=False)

def append_event(entry):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    payload = read_payload()
    prompt = find_prompt(payload)
    invoked = "$robyroy-v4" in prompt
    if invoked:
        append_event({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "skill": "robyroy-v4",
            "event_type": "v4_prompt_submitted",
            "summary": sanitize("Robyroy-V4 invocation detected"),
            "auto_apply": False,
        })
    print(json.dumps({"continue": True, "detected_robyroy_v4": invoked, "blocked": False}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
