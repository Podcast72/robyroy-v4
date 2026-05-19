#!/usr/bin/env python3
import json
import re
import sys

BLOCK_PATTERNS = {
    "GIT_PUSH_BLOCKED": r"\bgit\s+push\b",
    "GIT_COMMIT_BLOCKED": r"\bgit\s+commit\b",
    "GIT_RESET_CLEAN_BLOCKED": r"\bgit\s+(reset|clean)\b",
    "SUDO_BLOCKED": r"\bsudo\b",
    "DESTRUCTIVE_ACTION_BLOCKED": r"\brm\s+-rf\b",
    "BROAD_CHMOD_CHOWN_BLOCKED": r"\b(chmod|chown)\b\s+(-R\s+)?(/|~|/Users|/System|/Library|/etc)\b",
    "CONFIG_MODIFICATION_BLOCKED": r"(~/?\.codex/config\.toml|/\.codex/config\.toml|\bconfig\.toml\b)",
    "HOOK_ACTIVATION_BLOCKED": r"(~/?\.codex/hooks|~/?\.codex/hooks\.json|hook activation|activate hooks?)",
    "SECRET_EXPOSURE_BLOCKED": r"(\.env\b|\btoken\b|\bsecret\b|\bcredentials?\b)",
}
ALLOW_TOOLS = {"ls", "pwd", "grep", "rg", "python", "python3"}

def read_payload():
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}

def flatten(value):
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)

def main():
    payload = read_payload()
    tool_name = str(payload.get("tool_name") or payload.get("tool") or "")
    text = " ".join(flatten(payload.get(key, "")) for key in ("input", "arguments", "command", "tool_input", "params"))
    haystack = f"{tool_name} {text}"
    matched = [code for code, pattern in BLOCK_PATTERNS.items() if re.search(pattern, haystack, re.I)]
    innocuous = tool_name in ALLOW_TOOLS or re.match(r"^\s*(ls|pwd|grep|rg|python3?\s+[^;&|]*check)\b", text)
    blocked = bool(matched) and not innocuous
    out = {
        "decision": "block" if blocked else "allow",
        "blocked": blocked,
        "failure_codes": matched,
        "systemMessage": "Robyroy-V4 hook template blocked a risky action." if blocked else "",
        "continue": not blocked,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
