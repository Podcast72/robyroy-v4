#!/usr/bin/env python3
import argparse
import json
import sys

REQUIRED = [
    'PROBLEMA DICHIARATO',
    'PROBLEMA REALE',
    'OBIETTIVO VERIFICABILE',
    'NON-OBIETTIVI',
    'RISCHIO PRINCIPALE',
    'AZIONE MINIMA CORRETTA',
    'MODALITA',
]


def read_text(path):
    if path:
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    return sys.stdin.read()


def main():
    parser = argparse.ArgumentParser(description='Check required sections in a Robyroy V3 Problem Definition Gate.')
    parser.add_argument('file', nargs='?', help='Gate text file. Reads stdin when omitted.')
    args = parser.parse_args()

    text = read_text(args.file).upper()
    checked = list(REQUIRED)
    missing = [section for section in REQUIRED if section + ':' not in text]
    print(json.dumps({
        'ok': not missing,
        'missing': missing,
        'checked_sections': checked,
    }, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == '__main__':
    raise SystemExit(main())
