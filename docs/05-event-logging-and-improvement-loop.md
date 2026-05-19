# Event Logging and Improvement Loop

Robyroy-V4 records operational events so recurring patterns can be reviewed later.

Events can include invocation, mode detection, Goal Contract creation, scope checks, mini-prompt generation, mini-prompt use, blocked steps, validations, task completion and task stops.

## Counters

`evolution/counters.json` tracks event counts. The public repository ignores runtime counters by default so local runs do not pollute the published package.

## Improvement candidates

When thresholds are reached, Robyroy-V4 can write an improvement candidate. Candidates require human approval and include `auto_apply:false`.

## Review loop

The loop is intentionally passive:

```text
observe → count → suggest → review manually → apply only with explicit approval
```
