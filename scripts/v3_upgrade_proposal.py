#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent
EVOLUTION_DIR = BASE_DIR / "evolution"
REPORTS_DIR = BASE_DIR / "_reports"
LOG_PATH = EVOLUTION_DIR / "usage_log.jsonl"
COUNTERS_PATH = EVOLUTION_DIR / "counters.json"
OUTPUT_PATH = REPORTS_DIR / "upgrade_proposal_latest.md"


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


def detect_patterns(entries, thresholds):
    total_uses = len(entries)
    issue_counter = Counter()
    candidate_counter = Counter()
    for entry in entries:
        issue = str(entry.get("issue", "")).strip()
        candidate = str(entry.get("candidate", "")).strip()
        if issue:
            issue_counter[issue] += 1
        if candidate:
            candidate_counter[candidate] += 1

    minimum = int(thresholds.get("min_occurrences_for_candidate", 5))
    minimum_rate = float(thresholds.get("min_rate_for_candidate", 0.15))
    strong = []
    for name, count in candidate_counter.items():
        if not name or total_uses == 0:
            continue
        rate = count / total_uses
        if count >= minimum and rate >= minimum_rate:
            strong.append((name, count, rate))
    return total_uses, issue_counter, candidate_counter, sorted(strong, key=lambda item: (-item[1], item[0]))


def write_report(total_uses, issue_counter, strong_patterns):
    lines = [
        "# robyroy-v3 upgrade proposal",
        "",
        "SKILL ANALIZZATA:",
        "robyroy-v3",
        "",
        "UTILIZZI ANALIZZATI:",
        str(total_uses),
        "",
        "PATTERN RILEVATI:",
    ]
    if strong_patterns:
        for name, count, rate in strong_patterns:
            lines.append(f"- {name}: {count} occorrenze ({rate:.0%})")
    elif issue_counter:
        lines.append("- Segnali deboli presenti, ma nessun pattern forte oltre soglia.")
    else:
        lines.append("- Nessun segnale utile registrato.")
    lines.extend([
        "",
        "UPGRADE PROPOSTO:",
    ])
    if strong_patterns:
        lines.append("Preparare una revisione manuale mirata della skill sulla base dei pattern sopra elencati.")
    else:
        lines.append("Nessun upgrade consigliato per ora.")
    lines.extend([
        "",
        "FILE CHE VERREBBERO MODIFICATI:",
    ])
    if strong_patterns:
        lines.append("- Da definire dopo autorizzazione esplicita di Roberto.")
    else:
        lines.append("- Nessuno in questa fase.")
    lines.extend([
        "",
        "RISCHIO:",
        "Basso: questa proposta non applica patch e non modifica la skill.",
        "",
        "TEST PREVISTI:",
        "- Validazione manuale della proposta.",
        "- Eventuali smoke test sui file candidati solo dopo autorizzazione.",
        "",
        "AUTORIZZAZIONE RICHIESTA:",
    ])
    if strong_patterns:
        lines.append("Si, prima di qualsiasi modifica ai file della skill.")
    else:
        lines.append("No azione richiesta ora; mantenere osservazione passiva.")
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    counters = load_counters()
    thresholds = counters.get("policy", {})
    entries = load_entries()
    total_uses, issue_counter, _, strong_patterns = detect_patterns(entries, thresholds)
    write_report(total_uses, issue_counter, strong_patterns)
    counters["last_upgrade_proposal_at"] = int(time.time())
    COUNTERS_PATH.write_text(json.dumps(counters, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    result = {
        "ok": True,
        "total_uses": total_uses,
        "report_path": str(OUTPUT_PATH),
        "strong_patterns": [name for name, _, _ in strong_patterns],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
