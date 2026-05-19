# Codex Hook Readiness

Project-local lifecycle hooks for controlled Robyroy-V4 automation.

## Overview

Codex Hooks allow deterministic scripts to run during selected lifecycle events. Robyroy-V4 uses this idea as an advanced readiness layer for projects that need more controlled automation.

The model is intentionally project-local and reviewable. The hook templates in this repository are proposal-only until a user copies or configures them in a project-local `.codex` directory and reviews them through Codex `/hooks`.

## Why hooks matter

A skill can guide an agent, but a project-local hook can help the project observe and shape lifecycle behavior at the right moment.

Hooks can help:

- detect Robyroy-V4 usage
- log lifecycle events
- guard risky tool usage
- support controlled continuation
- make repeatable workflows more observable

## The Robyroy-V4 approach

Robyroy-V4 treats hooks as an advanced acceleration layer, not as a hidden default.

The order is:

1. Skill first.
2. Hook readiness second.
3. Project-local activation.
4. Manual trust review.
5. Small deterministic scripts.
6. Smoke tests before use.

## Candidate hooks

### UserPromptSubmit

Purpose: detect `$robyroy-v4` usage and log a minimal `v4_invoked` event.

This is the recommended first hook because it is low-friction and useful for observability.

### PreToolUse

Purpose: check obvious risky tool usage before execution, such as git push, sudo, config changes, hook activation or sensitive file access.

This hook can be powerful, but it needs careful review because false positives can block normal work.

### Stop

Purpose: support controlled continuation only when explicit markers are present.

Stop continuation should be added late, after the project is comfortable with the skill and with hook review.

## Controlled continuation markers

Stop continuation must only occur with explicit markers:

```text
V4_CONTINUE_ALLOWED: YES
V4_NEXT_PROMPT:
V4_CHAIN_STEP:
```

The chain step must stay inside the configured maximum, and the next prompt must not request POWER actions, network, sudo, git mutation, config changes, hook activation or destructive operations.

## Project-local hooks

The recommended strategy is project-local:

```text
.codex/hooks.json
.codex/hooks/
```

Project-local hooks keep automation tied to the repository that needs it. They avoid turning a useful project workflow into a global default.

## Trust review

Before running project-local hooks, the user should open `/hooks`, review the hook sources and trust only scripts whose behavior is clear.

This review matters because hooks enter the operational lifecycle of Codex. Even small scripts can alter the flow of work, block actions or continue a turn.

## Safety model

Robyroy-V4 hook readiness follows a conservative operating model:

- small scripts
- explicit markers
- max chain steps
- no silent activation
- no global config mutation
- rollback by removing `.codex/hooks.json` or disabling trust
- smoke test before use

## Suggested adoption path

1. Use Robyroy-V4 normally as a skill.
2. Ask Robyroy-V4 to create a Hook Readiness Plan.
3. Generate project-local hook templates.
4. Run smoke tests.
5. Review with `/hooks`.
6. Trust only if the behavior is clear.
7. Start with logging or warning-only behavior.

## Recommended first hook

Start with `UserPromptSubmit` logging. It is the least invasive hook and gives the project basic observability when `$robyroy-v4` is invoked.

After that, consider a warning-oriented `PreToolUse` guard. Add `Stop` continuation only when the project has mature workflow rules and clear rollback expectations.

## Practical value

Hook readiness turns Robyroy-V4 from a structured skill into a project-aware operating layer: still lightweight, still local, but able to observe lifecycle events and support controlled continuation.
