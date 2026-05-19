#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EVOLUTION_DIR = BASE_DIR / "evolution"
LOG_PATH = EVOLUTION_DIR / "usage_log.jsonl"
COUNTERS_PATH = EVOLUTION_DIR / "counters.json"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="")
    parser.add_argument("--task-type", default="")
    parser.add_argument("--success", default="")
    parser.add_argument("--issue", default="")
    parser.add_argument("--candidate", default="")
    parser.add_argument("--profiles", default="")
    return parser.parse_args()


def load_counters():
    if not COUNTERS_PATH.exists():
        return {
            "total_uses": 0,
            "last_self_audit_at": 0,
            "last_upgrade_proposal_at": 0,
            "policy": {},
        }
    with COUNTERS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_counters(counters):
    with COUNTERS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(counters, handle, indent=2)
        handle.write("\n")


def append_log(entry):
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def main():
    args = parse_args()
    counters = load_counters()
    total_uses = int(counters.get("total_uses", 0)) + 1
    counters["total_uses"] = total_uses

    entry = {
        "ts": int(time.time()),
        "mode": args.mode,
        "task_type": args.task_type,
        "success": args.success,
        "issue": args.issue,
        "candidate": args.candidate,
        "profiles": args.profiles,
    }

    append_log(entry)
    save_counters(counters)

    result = {
        "ok": True,
        "total_uses": total_uses,
        "log_path": str(LOG_PATH),
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
