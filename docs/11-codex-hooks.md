# Codex Hook Readiness

Project-local lifecycle hooks for controlled Robyroy-V4 automation.

## Overview

Codex Hooks can run deterministic scripts during selected lifecycle events. Robyroy-V4 treats hooks as readiness material for projects that want extra observability or warning checks.

The model is intentionally project-local and reviewable. The hook templates in this repository are proposal-only until a user copies or configures them in a project-local `.codex` directory and reviews them through Codex `/hooks`.

Global hooks are not active by default. This repository does not require editing global Codex configuration.

## Why Hooks Matter

A skill can guide an agent, but a reviewed project-local hook can help a project observe lifecycle events, warn before risky tool use or check final receipts.

Hooks can help:

- detect `$robyroy-v4` usage;
- log lifecycle events;
- warn before risky tool usage;
- support controlled continuation only with explicit markers;
- make repeatable workflows more observable.

## The Robyroy-V4 Approach

Robyroy-V4 treats hooks as an advanced acceleration layer, not as a hidden default.

The order is:

1. Skill first.
2. Hook readiness second.
3. Project-local activation only if needed.
4. Manual trust review.
5. Small deterministic scripts.
6. Smoke tests before use.
7. Warning/logging-only behavior first.

## Candidate Hooks

### UserPromptSubmit

Purpose: detect `$robyroy-v4` usage and log a minimal invocation event.

### PreToolUse

Purpose: warn or block obvious risky tool usage before execution, such as git push, sudo, config changes, hook activation or sensitive file access.

### Stop

Purpose: support controlled continuation only when explicit markers are present.

## Controlled Continuation Markers

Stop continuation must only occur with explicit markers:

```text
V4_CONTINUE_ALLOWED: YES
V4_NEXT_PROMPT:
V4_CHAIN_STEP:
```

The chain step must stay inside the configured maximum, and the next prompt must not request POWER actions, network, sudo, git mutation, config changes, hook activation or destructive operations.

## Project-local Hooks

The recommended strategy is project-local:

```text
.codex/hooks.json
.codex/hooks/
```

Project-local hooks keep automation tied to the repository that needs it. They avoid turning a useful project workflow into a global default.

## Trust Review

Before running project-local hooks, the user should open `/hooks`, review the hook sources and trust only scripts whose behavior is clear.

This review matters because hooks enter the operational lifecycle of Codex. Even small scripts can alter the flow of work, block actions or continue a turn.

## Safety Model

Robyroy-V4 hook readiness follows a conservative operating model:

- small scripts;
- explicit markers;
- max chain steps;
- no silent activation;
- no global config mutation;
- rollback by removing `.codex/hooks.json` or disabling trust;
- smoke test before use.

## Suggested Adoption Path

1. Use Robyroy-V4 normally as a skill.
2. Ask Robyroy-V4 to create a Hook Readiness Plan.
3. Generate project-local hook templates.
4. Run smoke tests.
5. Review with `/hooks`.
6. Trust only if the behavior is clear.
7. Start with logging or warning-only behavior.

Hook readiness is not AIOS and not a security runtime. It is a project-local readiness pack for users who choose to review and trust it.
