<p align="center">
  <img src="assets/Slide.PNG" alt="Robyroy-V4 — Governed Operator Skill" width="900">
</p>

# Robyroy-V4
## Governed Operator Skill for Structured Agent Work

Robyroy-V4 turns agent work into structured, scoped, validated and traceable execution.

## What is Robyroy-V4?

Robyroy-V4 is a Governed Operator Skill for local agents such as Codex and Cody. It is designed to help an agent move from an open-ended request to controlled execution through operative modes, a Goal Contract, Scope Guard, an Agent Skill Contract Layer, Active Event Logging, a Controlled Mini-Prompt Chain, local validation and a final receipt.

It is more than a long prompt. It is a reusable operating pattern with instructions, contract files, local scripts and validation checks that make agent work easier to inspect, continue and review.

## Why it exists

A long prompt can help an agent behave better, but it remains fragile. It can be forgotten, interpreted loosely or applied inconsistently across tasks.

Robyroy-V4 packages the method as a skill. The workflow becomes reusable. The boundaries become explicit. The contract layer makes expectations machine-readable. Local checks make the work easier to validate before it is presented as done.

The goal is practical: help agents do real work with clearer scope, safer continuation and better final reporting.

## Core idea

**Goal → Skill → Guard → Runner → Result**

- **Goal:** the user defines the task.
- **Skill:** Robyroy-V4 structures the workflow.
- **Guard:** scope, mode and risk are checked.
- **Runner:** multi-step work can be split into controlled mini-prompts.
- **Result:** the final output is validated and reported.

## Key capabilities

### Mode Detection

Classifies work as SAFE, BUILD, POWER, REVIEW, PROMPT, DOC, RAPID or DA_CONFERMARE so the agent can choose the right level of caution.

### Goal Contract

Defines the user goal, workspace, allowed paths, forbidden paths, success criteria, validation commands, stop conditions and claim limits before meaningful work begins.

### Scope Guard

Checks whether a target path or action is inside the declared workspace and outside forbidden targets.

### Agent Skill Contract Layer

Adds machine-readable contract files for modes, capabilities, blocked actions, failure policies, report schema and repair hints.

### Capabilities Declaration

Declares what the skill is allowed to do and which actions are blocked by design.

### Failure Codes

Uses stable failure codes for blocked or risky situations, making stops easier to understand and repair.

### Report Schema

Defines a final receipt format so results include goal, scope, changed files, validations, limits, status and next action.

### Active Event Logging

Records operational events such as mode detection, scope checks, mini-prompt use, validation runs and task stops.

### Improvement Candidates

When repeated patterns appear, the skill can suggest improvement candidates for human review. It does not apply them automatically.

### Controlled Mini-Prompt Chain

Splits eligible multi-step work into small internal prompts, each checked before use.

### Doctor / Contract Checks

Local scripts validate the contract layer, required files and cautious operating rules.

### Final Receipt

Every run should end with a structured report that states what happened, what was checked and what remains limited.

## How the Controlled Mini-Prompt Chain works

Robyroy-V4 can generate internal mini-prompts to continue the current task. Before using a mini-prompt, it checks scope, mode, goal alignment, chain limit, forbidden actions and stop conditions.

```text
generate mini-prompt → guard check → use inside current task → log event → continue or stop
```

The chain is bounded. It is not a daemon, background process or external automation. It is internal skill orchestration for the current task.

## Repository structure

```text
robyroy-v4/
├── README.md
├── LICENSE
├── NOTICE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── SKILL.md
├── contract/
├── scripts/
├── references/
├── docs/
├── examples/
├── assets/
│   └── Slide.PNG
└── repo/
    └── suggested-layout.md
```

## Installation

Install the skill manually into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R robyroy-v4 ~/.codex/skills/robyroy-v4
```

Then invoke it explicitly:

```text
$robyroy-v4
```

## Usage

Example 1:

```text
$robyroy-v4
Analyze this repository and produce a scoped improvement plan.
```

Example 2:

```text
$robyroy-v4
Create a Goal Contract before editing this project.
```

Example 3:

```text
$robyroy-v4
Run a controlled documentation update with validation and final receipt.
```

## Validation

Run local checks from the repository root:

```bash
python3 scripts/v4_doctor_check.py
python3 scripts/v4_contract_check.py
python3 scripts/v4_prompt_runner.py --list
```

## Example final receipt

```text
MODE:
GOAL:
SCOPE:
FILES_CREATED:
FILES_MODIFIED:
SCRIPTS_COMMANDS_USED:
TESTS_VALIDATIONS:
LIMITS:
STATUS:
NEXT_ACTION:
STOP_CONDITIONS:
```

## Project status

Robyroy-V4 is a structured experimental skill pattern for local agent workflows. It is designed to make agent work easier to scope, validate, continue and review through contracts, checks, event logging and controlled mini-prompt chains.

## Roadmap

- More usage examples
- More contract fixtures
- More validator checks
- Public demo workflows
- Improved documentation templates
- Additional controlled runner examples
- Cleaner install package

## License

See [LICENSE](LICENSE).
