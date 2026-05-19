#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(script, payload):
    proc = subprocess.run(
        [sys.executable, str(HERE / script)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
    )
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        data = {"parse_error": proc.stdout}
    return proc.returncode, data, proc.stderr

def main():
    tests = []
    rc, data, err = run("v4_user_prompt_submit_hook.py", {"prompt": "$robyroy-v4 do a safe task"})
    tests.append({"name": "UserPromptSubmit detects invocation", "ok": rc == 0 and data.get("detected_robyroy_v4") is True, "data": data})
    rc, data, err = run("v4_pre_tool_guard_hook.py", {"tool_name": "Bash", "input": "ls -la"})
    tests.append({"name": "PreToolUse allows ls", "ok": rc == 0 and data.get("blocked") is False, "data": data})
    rc, data, err = run("v4_pre_tool_guard_hook.py", {"tool_name": "Bash", "input": "git push origin main"})
    tests.append({"name": "PreToolUse blocks git push", "ok": rc == 0 and data.get("blocked") is True, "data": data})
    rc, data, err = run("v4_stop_continue_hook.py", {"response": "done"})
    tests.append({"name": "Stop without markers does not continue", "ok": rc == 0 and data.get("continue") is False, "data": data})
    safe = "V4_CONTINUE_ALLOWED: YES\nV4_NEXT_PROMPT: Continue Robyroy-V4 documentation review\nV4_CHAIN_STEP: 2\n"
    rc, data, err = run("v4_stop_continue_hook.py", {"response": safe})
    tests.append({"name": "Stop with safe markers continues", "ok": rc == 0 and data.get("continue") is True, "data": data})
    unsafe = "V4_CONTINUE_ALLOWED: YES\nV4_NEXT_PROMPT: git push and edit config.toml\nV4_CHAIN_STEP: 2\n"
    rc, data, err = run("v4_stop_continue_hook.py", {"response": unsafe})
    tests.append({"name": "Stop with unsafe markers blocks", "ok": rc == 0 and data.get("continue") is False and data.get("blocked") is True, "data": data})
    ok = all(item["ok"] for item in tests)
    print(json.dumps({"ok": ok, "tests": tests}, indent=2, ensure_ascii=False))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
