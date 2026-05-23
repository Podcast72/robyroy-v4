# Architecture

Robyroy-V4 is organized as a local governed operator skill. Its architecture is intentionally simple: instructions, structured contracts, deterministic helper scripts, templates and local/private logs.

```text
User Request -> V4 Session -> Goal Contract -> Scope/Claim Discipline -> Optional Runner/Trace -> Validation -> Lifecycle Receipt
```

## Instruction Layer

`SKILL.md` is the primary operator instruction file. It explains how the agent should classify work, define scope, apply Karpathy-style discipline, handle trace/logging applicability, use bounded prompt chains and close with a final receipt.

## Contract Layer

`contract/*.json` exposes important expectations in machine-readable form:

- `skill.contract.json`: identity, modes, active behaviors, runner and lifecycle policies.
- `capabilities.json`: allowed capabilities and blocked actions.
- `failure_codes.json`: stable stop reasons.
- `report_schema.json`: final receipt expectations and lifecycle status fields.
- `repair_hints.json`: allowed and forbidden repair patterns.

## Script Layer

`scripts/*.py` contains small local helpers. They are dependency-free where practical and should fail safely. Important families include:

- mode/scope/report checks;
- usage and event logging;
- controlled mini-prompt and task runner helpers;
- `v4_session_lifecycle.py` for start/event/check-report/finish/suggest lifecycle operations;
- doctor and contract validation checks.

## Template Layer

`templates/*.md` provides reusable forms for project operating files, final receipts, prompt-chain traces, handoff notes and lifecycle receipts.

## Local Evolution Layer

`evolution/*.jsonl` files store local/private event logs, usage logs and improvement candidates. They support review and improvement, but they are not public proof and should not be copied into documentation.

## Hook Readiness Layer

`hooks-readiness/` contains proposal-only material for project-local hooks. This layer is not active by default and does not change global Codex configuration.

## What Is Automatic Locally

When the skill is used, V4 should automatically apply its session discipline: compact pre-edit thinking, lifecycle status declarations, report checking when feasible and event logging when safe.

## What Is Advisory

The skill guides the agent. Without separate runtime enforcement or trusted project-local hooks, the discipline depends on the agent following the skill instructions.
