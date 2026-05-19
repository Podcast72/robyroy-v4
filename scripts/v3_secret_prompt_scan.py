#!/usr/bin/env python3
import argparse
import json
import re
import sys

PATTERNS = [
    ('openai_api_key', re.compile(r'\bsk-[A-Za-z0-9_-]{12,}\b')),
    ('generic_api_key', re.compile(r'(?i)\b(api[_-]?key)\s*[:=]\s*([A-Za-z0-9_./+\-]{8,})')),
    ('token', re.compile(r'(?i)\b(token)\s*[:=]\s*([A-Za-z0-9_./+\-]{8,})')),
    ('password', re.compile(r'(?i)\b(password|passwd|pwd)\s*[:=]\s*([^\s]{4,})')),
    ('env_file', re.compile(r'(?i)(^|[\s/])\.env([\s:]|$)')),
]


def mask_value(value):
    if len(value) <= 8:
        return '*' * len(value)
    return value[:4] + '...' + value[-4:]


def scan(text):
    findings = []
    masked = text
    for kind, pattern in PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(0)
            if kind in {'generic_api_key', 'token', 'password'} and len(match.groups()) >= 2:
                value = match.group(2)
                masked_raw = raw.replace(value, mask_value(value))
            elif kind == 'env_file':
                masked_raw = raw.replace('.env', '[masked-env-file]')
            else:
                masked_raw = mask_value(raw)
            findings.append({'type': kind, 'match': masked_raw})
            masked = masked.replace(raw, masked_raw)
    return {'ok': not findings, 'has_findings': bool(findings), 'findings': findings, 'masked_text': masked}


def main():
    parser = argparse.ArgumentParser(description='Scan prompt text for likely secrets and mask detected values.')
    parser.add_argument('text', nargs='*', help='Text to scan. Reads stdin when omitted.')
    args = parser.parse_args()
    text = ' '.join(args.text) if args.text else sys.stdin.read()
    result = scan(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['has_findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
