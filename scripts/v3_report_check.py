#!/usr/bin/env python3
import argparse
import json
import sys

REQUIRED = ['MODE', 'FILE MODIFICATI', 'TEST / VALIDAZIONI', 'LIMITI', 'STATO']


def main():
    parser = argparse.ArgumentParser(description='Check minimum required sections in a Robyroy V3 final report.')
    parser.add_argument('report', nargs='?', help='Report file. Reads stdin when omitted.')
    args = parser.parse_args()
    if args.report:
        with open(args.report, 'r', encoding='utf-8') as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()
    upper = text.upper()
    missing = [section for section in REQUIRED if section + ':' not in upper]
    print(json.dumps({'ok': not missing, 'missing': missing}, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == '__main__':
    raise SystemExit(main())
