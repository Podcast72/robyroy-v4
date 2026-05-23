# Usage

Robyroy-V4 is most useful when a task benefits from scope discipline, local checks and clear reporting.

## Short Documentation Update

```text
$robyroy-v4
OBJECTIVE: Update this README section.
CONSTRAINTS: no commit, no push, docs only.
```

Expected behavior: V4 should apply compact pre-edit discipline, keep changes surgical, check the result and include lifecycle statuses in the final receipt.

## Scoped Analysis

```text
$robyroy-v4
Analyze this repository and produce a scoped improvement plan.
```

Expected behavior: define the scope, avoid unrelated edits and report limits.

## Goal Contract Before Edits

```text
$robyroy-v4
Create a Goal Contract before editing this project.
```

Expected behavior: state goal, workspace, allowed paths, forbidden paths, success criteria, validation commands and stop conditions.

## Controlled Documentation Update

```text
$robyroy-v4
Run a controlled documentation update with validation and final receipt.
```

Expected behavior: use the Karpathy Discipline Layer, run local checks where available and close with lifecycle status fields.

## Multi-step or Handoff Work

```text
$robyroy-v4
Plan and execute a small docs migration. Leave next prompts and handoff notes if anything remains.
```

Expected behavior: use bounded prompt-chain or handoff templates only when useful; do not create autonomous continuation.

## Final Receipt Expectations

A modern V4 final receipt should include the normal report fields plus:

```text
V4_SESSION_STATUS:
EVENT_LOGGING_STATUS:
V4_TRACE_STATUS:
HANDOFF_STATUS:
PROMPT_CHAIN_STATUS:
RUNNER_STATUS:
REPORT_CHECK_STATUS:
IMPROVEMENT_CANDIDATE_STATUS:
```

For micro-tasks, some fields can be `NOT_APPLICABLE`, but they should still be declared.
