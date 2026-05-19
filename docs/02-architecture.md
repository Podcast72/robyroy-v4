# Architecture

Robyroy-V4 follows a structured execution path:

```text
User Request → Mode Detection → Goal Contract → Scope Guard → Contract Layer → Controlled Runner → Validation → Final Receipt
```

## User Request

The user states the task and, when needed, the working directory and constraints.

## Mode Detection

The skill classifies the request as SAFE, BUILD, POWER, REVIEW, PROMPT, DOC, RAPID or DA_CONFERMARE.

## Goal Contract

The Goal Contract captures the outcome, workspace, allowed paths, forbidden paths, success criteria, validation commands and stop conditions.

## Scope Guard

The guard checks whether each planned target is inside the declared workspace and outside blocked targets.

## Contract Layer

JSON contract files declare capabilities, blocked actions, failure codes and report requirements.

## Controlled Runner

Eligible multi-step work can be split into bounded internal steps. Each step is checked before use.

## Validation

Local scripts validate the contract, report format and operational health of the skill package.

## Final Receipt

The agent closes with a structured receipt that records what changed, what was checked and what remains limited.
