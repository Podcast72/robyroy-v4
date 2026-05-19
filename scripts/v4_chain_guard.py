#!/usr/bin/env python3
import argparse
import json
import re

POWER_PATTERNS = {
    "network": r"\b(network|internet|download|curl|wget|fetch)\b",
    "sudo": r"\bsudo\b",
    "git_mutation": r"\bgit\s+(push|commit|reset|clean|checkout|tag)\b",
    "config": r"\bconfig\.toml\b",
    "hooks": r"\b(hook|hooks|activate\s+hook|attiva\s+hook)\b",
    "destructive": r"\brm\s+-rf\b|\bdelete\b|\bcancella\b",
    "install": r"\b(install|npm\s+install|pip\s+install|brew\s+install)\b",
    "secret": r"\b(token|secret|password|credential|\.env)\b",
}

def contains_power(text):
    return [name for name, pattern in POWER_PATTERNS.items() if re.search(pattern, text or "", re.I)]

def goal_aligned(goal, prompt):
    goal_words = {w.lower() for w in re.findall(r"[A-Za-z0-9_]{4,}", goal or "")}
    prompt_words = {w.lower() for w in re.findall(r"[A-Za-z0-9_]{4,}", prompt or "")}
    if not goal_words:
        return False
    return bool(goal_words & prompt_words)

def evaluate(goal, prompt, mode, step_index, max_steps):
    if step_index > max_steps:
        return {
            "allowed": False,
            "reason": "chain step exceeds maximum allowed steps",
            "failure_code": "MINI_PROMPT_CHAIN_LIMIT_REACHED",
            "requires_user_confirmation": False,
        }
    flags = contains_power(prompt)
    if mode.upper() == "POWER" or flags:
        return {
            "allowed": False,
            "reason": "mini-prompt requires POWER-level or blocked action: " + ", ".join(flags or ["POWER mode"]),
            "failure_code": "MINI_PROMPT_POWER_REQUIRED",
            "requires_user_confirmation": True,
        }
    if not goal_aligned(goal, prompt):
        return {
            "allowed": False,
            "reason": "mini-prompt does not clearly align with current goal",
            "failure_code": "MINI_PROMPT_GOAL_MISMATCH",
            "requires_user_confirmation": False,
        }
    if re.search(r"\b(outside scope|fuori scope|unknown path|path incerto)\b", prompt or "", re.I):
        return {
            "allowed": False,
            "reason": "mini-prompt scope is unclear or outside declared scope",
            "failure_code": "MINI_PROMPT_SCOPE_BLOCKED",
            "requires_user_confirmation": False,
        }
    return {
        "allowed": True,
        "reason": "mini-prompt is within chain limit, goal-aligned and does not require POWER",
        "failure_code": "",
        "requires_user_confirmation": False,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-goal", required=True)
    parser.add_argument("--mini-prompt-text", required=True)
    parser.add_argument("--mode", default="SAFE")
    parser.add_argument("--step-index", type=int, required=True)
    parser.add_argument("--max-steps", type=int, default=3)
    args = parser.parse_args()
    out = evaluate(args.current_goal, args.mini_prompt_text, args.mode, args.step_index, args.max_steps)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["allowed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
