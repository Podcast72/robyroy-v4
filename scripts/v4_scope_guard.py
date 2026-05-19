#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HOME = Path.home().resolve()
BLOCKED_EXACT = {Path("/"), HOME, Path("/etc"), Path("/System"), Path("/Library"), HOME / ".ssh", HOME / ".codex" / "config.toml"}
BLOCKED_PARTS = {"etc", "System", "Library"}

def expand(value):
    return Path(value).expanduser().resolve(strict=False)

def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False

def result(allowed, reason, failure_code=None):
    return {"allowed": allowed, "reason": reason, "failure_code": failure_code}

def check(target_path, allowed_roots):
    target = expand(target_path)
    roots = [expand(r) for r in allowed_roots]
    if target in BLOCKED_EXACT:
        code = "CONFIG_MODIFICATION_BLOCKED" if target.name == "config.toml" else "SCOPE_BLOCKED"
        return result(False, "target path is protected or too broad", code)
    if target == HOME or str(target) in {"/", str(HOME)}:
        return result(False, "home-wide or root-wide target is blocked", "SCOPE_BLOCKED")
    if str(target).startswith(str(HOME / ".ssh")):
        return result(False, "ssh material is blocked", "UNSAFE_ACTION")
    if "robyroy-v3" in target.parts:
        return result(False, "robyroy-v3 is forbidden for V4 tasks", "V3_MODIFICATION_BLOCKED")
    if "config.toml" == target.name and ".codex" in target.parts:
        return result(False, "codex config modification is blocked", "CONFIG_MODIFICATION_BLOCKED")
    for root in roots:
        if root in BLOCKED_EXACT or root == HOME:
            continue
        if inside(target, root):
            return result(True, "target path is inside an allowed root", None)
    return result(False, "target path is outside allowed roots", "SCOPE_BLOCKED")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_path")
    parser.add_argument("allowed_roots", nargs="+")
    args = parser.parse_args()
    out = check(args.target_path, args.allowed_roots)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["allowed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
