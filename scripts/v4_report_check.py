#!/usr/bin/env python3
import argparse
import json
import sys

REQUIRED = ["MODE", "GOAL", "SCOPE", "FILES_CREATED", "FILES_MODIFIED", "SCRIPTS_COMMANDS_USED", "TESTS_VALIDATIONS", "LIMITS", "STATUS", "NEXT_ACTION", "STOP_CONDITIONS"]
BLOCKED_CLAIMS = ["VERIFIED", "PRODUCTION_READY", "RELEASE_READY", "STANDARD", "SECURE_BY_DEFAULT"]

def check(text):
    upper = text.upper()
    missing = [section for section in REQUIRED if f"{section}:" not in upper]
    warnings = [f"blocked claim term present: {term}" for term in BLOCKED_CLAIMS if term in upper]
    return {"ok": not missing and not warnings, "missing": missing, "warnings": warnings}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", nargs="?")
    args = parser.parse_args()
    text = open(args.report, encoding="utf-8").read() if args.report else sys.stdin.read()
    out = check(text)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
