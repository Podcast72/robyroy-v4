#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent
EVOLUTION_DIR = BASE_DIR / "evolution"
LOG_PATH = EVOLUTION_DIR / "usage_log.jsonl"
COUNTERS_PATH = EVOLUTION_DIR / "counters.json"
CANDIDATES_PATH = EVOLUTION_DIR / "improvement_candidates.md"


def load_counters():
    with COUNTERS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_entries():
    entries = []
    if not LOG_PATH.exists():
        return entries
    with LOG_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def counter_to_list(counter):
    return [{"name": name, "count": count} for name, count in counter.most_common()]


def update_candidates(entries, issue_counter, candidate_counter, thresholds):
    total_uses = len(entries)
    lines = ["# robyroy-v3 improvement candidates", ""]
    if total_uses == 0:
        lines.append("No upgrade candidates yet.")
    else:
        strong = []
        minimum = thresholds.get("min_occurrences_for_candidate", 5)
        minimum_rate = thresholds.get("min_rate_for_candidate", 0.15)
        for name, count in candidate_counter.items():
            if not name:
                continue
            rate = count / total_uses if total_uses else 0.0
            if count >= minimum and rate >= minimum_rate:
                strong.append((name, count, rate))
        if strong:
            lines.append("Strong recurring candidates:")
            for name, count, rate in sorted(strong, key=lambda item: (-item[1], item[0])):
                lines.append(f"- {name}: {count} occurrences ({rate:.0%})")
        else:
            lines.append("No strong recurring candidates yet.")
        if issue_counter:
            lines.append("")
            lines.append("Observed issues:")
            for name, count in issue_counter.most_common(5):
                if name:
                    lines.append(f"- {name}: {count}")
    lines.extend([
        "",
        "Policy:",
        "- collect evidence first;",
        "- do not propose upgrades from single isolated cases;",
        "- require recurring, measurable, testable patterns;",
        "- do not apply upgrades without Roberto's explicit approval.",
    ])
    CANDIDATES_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    counters = load_counters()
    thresholds = counters.get("policy", {})
    entries = load_entries()
    issue_counter = Counter()
    candidate_counter = Counter()
    for entry in entries:
        issue = str(entry.get("issue", "")).strip()
        candidate = str(entry.get("candidate", "")).strip()
        if issue:
            issue_counter[issue] += 1
        if candidate:
            candidate_counter[candidate] += 1

    update_candidates(entries, issue_counter, candidate_counter, thresholds)
    counters["last_self_audit_at"] = int(time.time())
    COUNTERS_PATH.write_text(json.dumps(counters, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    total_uses = len(entries)
    should_prepare = total_uses >= int(thresholds.get("soft_proposal_threshold", 50)) and any(
        count >= int(thresholds.get("min_occurrences_for_candidate", 5))
        and (count / total_uses) >= float(thresholds.get("min_rate_for_candidate", 0.15))
        for _, count in candidate_counter.items()
        if total_uses
    )
    result = {
        "total_uses": total_uses,
        "top_issues": counter_to_list(issue_counter),
        "top_candidates": counter_to_list(candidate_counter),
        "thresholds": thresholds,
        "should_prepare_upgrade_proposal": should_prepare,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
