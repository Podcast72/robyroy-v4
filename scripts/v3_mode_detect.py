#!/usr/bin/env python3
import argparse
import json
import re
import sys

POWER_PATTERNS = [
    r'\bsudo\b', r'\bgit\s+(push|commit|reset|clean|checkout|tag)\b',
    r'\bchmod\b', r'\bchown\b', r'\brm\s+-rf\b', r'\bcurl\b', r'\bwget\b',
    r'\binstall\b', r'\bnpm\s+install\b', r'\bpip\s+install\b', r'\bbrew\s+install\b',
    r'\btoken\b', r'\bsecret\b', r'\bpassword\b', r'\.env\b', r'\bcredential',
]
BUILD_PATTERNS = [
    r'\bcrea\b', r'\baggiorna\b', r'\bmodifica\b', r'\bcorreggi\b', r'\bfix\b',
    r'\bpatch\b', r'\bwrite\b', r'\bcreate\b', r'\bupdate\b', r'\bedit\b',
]
SAFE_PATTERNS = [
    r'\bleggi\b', r'\banalizza\b', r'\baudit\b', r'\breview\b', r'\bcontrolla\b',
    r'\bsummarize\b', r'\bexplain\b', r'\binspect\b', r'\bread\b',
]
AMBIGUOUS_PATTERNS = [r'\bforse\b', r'\bqualcosa\b', r'\bovunque\b', r'\btutto\b', r'\bwhatever\b']


def matches(patterns, text):
    return [pat for pat in patterns if re.search(pat, text, re.I)]


def classify(prompt):
    prompt = prompt or ''
    power = matches(POWER_PATTERNS, prompt)
    build = matches(BUILD_PATTERNS, prompt)
    safe = matches(SAFE_PATTERNS, prompt)
    ambiguous = matches(AMBIGUOUS_PATTERNS, prompt)
    warnings = []
    if power:
        mode = 'POWER'
        reason = 'prompt contains power-risk action or sensitive material reference'
    elif ambiguous and build:
        mode = 'DA_CONFERMARE'
        reason = 'prompt combines edit intent with ambiguous scope wording'
    elif build:
        mode = 'BUILD'
        reason = 'prompt asks for local creation, update, patch, or fix'
    elif safe:
        mode = 'SAFE'
        reason = 'prompt appears read-only or analytical'
    else:
        mode = 'DA_CONFERMARE'
        reason = 'mode could not be inferred confidently'
    if ambiguous:
        warnings.append('ambiguous scope wording detected')
    return {
        'ok': True,
        'mode': mode,
        'reason': reason,
        'matches': {'power': power, 'build': build, 'safe': safe, 'ambiguous': ambiguous},
        'warnings': warnings,
    }


def main():
    parser = argparse.ArgumentParser(description='Classify a prompt into Robyroy V3 SAFE, BUILD, POWER, or DA_CONFERMARE.')
    parser.add_argument('prompt', nargs='*', help='Prompt text. Reads stdin when omitted.')
    args = parser.parse_args()
    text = ' '.join(args.prompt) if args.prompt else sys.stdin.read()
    print(json.dumps(classify(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
