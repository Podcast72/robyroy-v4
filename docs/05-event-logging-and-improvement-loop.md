# Event Logging and Improvement Loop

Robyroy-V4 can record local operational events so recurring patterns can be reviewed later. These logs are local/private runtime artifacts, not public evidence and not material to publish.

Events may include invocation, mode detection, Goal Contract creation, scope checks, runner use, report checks, blocked actions, validations, task completion and task stops.

## Usage and Event Logs

`evolution/events.jsonl` and `evolution/usage_log.jsonl` are append-only local logs. They help a user understand how the skill is being used and where friction repeats.

For simple micro-tasks, logging may be `NOT_APPLICABLE`. For non-trivial tasks, V4 should log when it is safe and in scope, or explain why it did not.

## Lifecycle Statuses

Modern V4 receipts should declare lifecycle statuses such as:

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

This prevents ambiguity about whether logging, trace, handoff, prompt-chain or runner logic was used.

## Improvement Candidates

When repeated patterns appear, V4 can write improvement candidates to `evolution/improvement_candidates.jsonl`. Candidates must include `requires_user_approval:true` and `auto_apply:false`.

The loop is passive:

```text
observe -> count -> suggest -> review manually -> apply only with explicit approval
```

V4 must not auto-edit the skill, contracts, hooks or configuration based only on a threshold.
