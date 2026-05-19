# Controlled Mini-Prompt Chain

The Controlled Mini-Prompt Chain lets Robyroy-V4 split eligible work into small internal instructions. It is useful when a task has multiple safe steps, such as inventory, plan, patch and validation.

The chain is not an autonomous loop. It is bounded internal orchestration for the current task.

## Flow

```text
generate mini-prompt → guard check → use inside current task → log event → continue or stop
```

## Guard checks

Before a step is used, the skill checks:

- current Goal Contract
- declared scope
- mode and risk
- chain step count
- forbidden actions
- stop conditions

## Limits

The default maximum is 3 chain steps per task. The chain stops for POWER actions, unclear scope, config edits, hook activation, network, sudo, git mutation, destructive operations or unsupported claims.
