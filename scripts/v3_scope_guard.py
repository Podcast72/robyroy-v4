#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

BROAD_BLOCKLIST = {
    Path('/'), Path('/etc'), Path('/System'), Path('/Library'), Path('/bin'), Path('/sbin'),
    Path('/usr'), Path('/usr/bin'), Path('/usr/sbin'), Path('/private/etc'), Path.home(),
}


def expand(path):
    return Path(path).expanduser().resolve(strict=False)


def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check(target, allowed_roots):
    target_path = expand(target)
    roots = [expand(root) for root in allowed_roots]
    warnings = []
    if target_path in BROAD_BLOCKLIST:
        return {'ok': False, 'allowed': False, 'reason': 'target path is too broad or protected', 'path': str(target_path), 'allowed_roots': [str(r) for r in roots], 'warnings': warnings}
    for root in roots:
        if root in BROAD_BLOCKLIST:
            warnings.append(f'allowed root is broad and ignored: {root}')
            continue
        if inside(target_path, root):
            return {'ok': True, 'allowed': True, 'reason': 'target path is inside an allowed root', 'path': str(target_path), 'allowed_roots': [str(r) for r in roots], 'warnings': warnings}
    return {'ok': False, 'allowed': False, 'reason': 'target path is outside allowed roots', 'path': str(target_path), 'allowed_roots': [str(r) for r in roots], 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description='Check that a path is inside allowed roots and not overly broad.')
    parser.add_argument('path', help='Target path to check.')
    parser.add_argument('--allowed-root', action='append', required=True, help='Allowed root. May be passed multiple times.')
    args = parser.parse_args()
    result = check(args.path, args.allowed_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['allowed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
