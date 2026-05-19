# Hook Design Notes

## UserPromptSubmit candidate

Purpose:

- detect `$robyroy-v4` invocation
- log `v4_invoked`
- optionally add a short system message

Risk: low if logging-only.

## PreToolUse candidate

Purpose:

- block obvious dangerous operations
- detect git push, sudo, config.toml, hook activation, secrets, `.env` and broad destructive paths

Risk: medium because false positives can block work.

## Stop candidate

Purpose:

- controlled continuation only if final response contains explicit markers

Required markers:

```text
V4_CONTINUE_ALLOWED: YES
V4_NEXT_PROMPT:
V4_CHAIN_STEP:
```

Risk: high if poorly designed, because it can create continuation loops.
