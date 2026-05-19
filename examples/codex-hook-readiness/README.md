# Codex Hook Readiness Example

## Scenario

A project uses Robyroy-V4 for structured documentation and validation work. The team wants more observability and a small amount of lifecycle automation, but does not want global hooks.

## When to consider hooks

Consider project-local hooks when the project repeatedly needs:

- V4 invocation logging
- warning-only checks before risky operations
- marker-based controlled continuation
- repeatable validation around agent workflow boundaries

## Recommended first hook

Start with `UserPromptSubmit` logging. It detects `$robyroy-v4` and records a minimal event.

## Sample project-local layout

```text
.codex/
├── hooks.json
└── hooks/
    ├── v4_user_prompt_submit_hook.py
    ├── v4_pre_tool_guard_hook.py
    └── v4_stop_continue_hook.py
```

## Trust review

Before any hook runs, open `/hooks`, inspect the hook source and trust only scripts whose behavior is clear.

## Smoke test

From the readiness pack:

```bash
python3 hooks-readiness/scripts/hooks_smoke_test.py
```

## Final receipt example

```text
MODE:
GOAL:
SCOPE:
HOOK_READINESS_STATUS:
HOOKS_ACTIVE:
TRUST_REVIEW_REQUIRED:
GLOBAL_CONFIG_STATUS:
TESTS_VALIDATIONS:
LIMITS:
STATUS:
NEXT_ACTION:
STOP_CONDITIONS:
```
