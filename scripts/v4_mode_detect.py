#!/usr/bin/env python3
import argparse
import json
import re
import sys

MODES = ["SAFE", "BUILD", "POWER", "REVIEW", "PROMPT", "DOC", "RAPID", "DA_CONFERMARE"]
POWER_PATTERNS = {
    "sudo": r"\bsudo\b",
    "install": r"\b(install|npm\s+install|pip\s+install|brew\s+install|uv\s+add)\b",
    "git_push": r"\bgit\s+push\b",
    "git_commit": r"\bgit\s+commit\b",
    "git_reset": r"\bgit\s+reset\b",
    "git_clean": r"\bgit\s+clean\b",
    "rm_rf": r"\brm\s+-rf\b",
    "chmod": r"\bchmod\b",
    "chown": r"\bchown\b",
    "token": r"\btoken\b",
    "secret": r"\bsecret\b",
    "env": r"\.env\b",
    "network_download": r"\b(network|download|curl|wget|fetch|internet)\b",
    "config_toml": r"\bconfig\.toml\b",
    "hook_activation": r"\b(hook|hooks|activate\s+hook|attiva\s+hook)\b",
    "global_change": r"\b(global|system-wide|home-wide|tutta\s+la\s+home)\b",
}
BUILD_PATTERNS = [r"\b(create|write|edit|update|patch|fix|modify|build)\b", r"\b(crea|scrivi|modifica|aggiorna|correggi)\b"]
SAFE_PATTERNS = [r"\b(read|inspect|audit|analyze|review|explain|list)\b", r"\b(leggi|analizza|controlla|elenca)\b"]

def hits(patterns, text):
    if isinstance(patterns, dict):
        return [name for name, pat in patterns.items() if re.search(pat, text, re.I)]
    return [pat for pat in patterns if re.search(pat, text, re.I)]

def classify(text):
    text = text or ""
    risk_flags = hits(POWER_PATTERNS, text)
    reasons = []
    requires_confirmation = False
    if risk_flags:
        mode = "POWER"
        requires_confirmation = True
        reasons.append("power-risk pattern detected")
    elif re.search(r"\b(review|code review|closeout)\b", text, re.I):
        mode = "REVIEW"; reasons.append("review intent detected")
    elif re.search(r"\b(prompt|mini-prompt|payload)\b", text, re.I):
        mode = "PROMPT"; reasons.append("prompt generation intent detected")
    elif re.search(r"\b(doc|docs|document|readme|documentation)\b", text, re.I):
        mode = "DOC"; reasons.append("documentation intent detected")
    elif re.search(r"\b(rapid|micro|quick|veloce)\b", text, re.I):
        mode = "RAPID"; reasons.append("rapid or micro task wording detected")
    elif hits(BUILD_PATTERNS, text):
        mode = "BUILD"; reasons.append("local write or build intent detected")
    elif hits(SAFE_PATTERNS, text):
        mode = "SAFE"; reasons.append("read-only or analytical intent detected")
    else:
        mode = "DA_CONFERMARE"; reasons.append("insufficient signal for confident mode selection"); requires_confirmation = True
    return {"mode": mode, "reasons": reasons, "risk_flags": risk_flags, "requires_confirmation": requires_confirmation}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="*")
    args = parser.parse_args()
    text = " ".join(args.prompt) if args.prompt else sys.stdin.read()
    print(json.dumps(classify(text), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
