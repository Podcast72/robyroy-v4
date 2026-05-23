# Current Local Design Alignment

This document explains the current Robyroy-V4 design in public-safe terms. It reflects the active local skill direction without publishing private event logs, local machine traces or AIOS internals.

## 1. What Robyroy-V4 Is

Robyroy-V4 is a governed operator skill for structured local agent work. It helps an agent define a goal, keep scope narrow, make controlled edits, run local checks and close with a receipt.

It is not AIOS, not a production security runtime and not global enforcement. It depends on the agent following the skill unless a user separately adds reviewed project-local hooks or another runtime governance layer.

## 2. Architecture

Robyroy-V4 is made of several layers:

- `SKILL.md`: human/operator instructions.
- `contract/*.json`: structured machine-readable skill contract.
- `scripts/*.py`: deterministic local helpers.
- `templates/*.md`: stable output forms.
- report checks: consistency and missing-status warnings.
- `evolution/*.jsonl`: local/private event and improvement logs.
- `hooks-readiness/`: proposal and readiness material only.

## 3. Karpathy Discipline Layer

For coding/refactor/patch/migration work, V4 should use a compact discipline:

- think before coding;
- prefer simple sufficient changes;
- keep changes surgical;
- connect every file edit to the goal;
- distinguish implemented, checked, partially checked and not checked;
- report evidence and limits.

This is local behavior guidance, not magic enforcement.

## 4. Trace / Logging Applicability Policy

V4 should declare whether logging, trace, handoff, prompt-chain and runner logic were used. For tiny tasks these may be `NOT_APPLICABLE`. For serious tasks, V4 should update event/usage logs when safe or explain why it did not.

If no project-local trace is created, the final receipt should say why.

## 5. Auto Session Lifecycle

V4 should open and close a lightweight local session for non-trivial tasks. The lifecycle can be compact for small tasks.

The helper `scripts/v4_session_lifecycle.py` supports operations such as:

```bash
python3 scripts/v4_session_lifecycle.py start --mode BUILD --task "short description"
python3 scripts/v4_session_lifecycle.py event --event mode_detected --mode BUILD
python3 scripts/v4_session_lifecycle.py check-report --report path/to/report.md
python3 scripts/v4_session_lifecycle.py finish --status COMPLETED --report path/to/report.md
python3 scripts/v4_session_lifecycle.py suggest --summary "repeated issue"
```

Modern V4 receipts should include:

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

## 6. Improvement Candidates

V4 can record repeated issues or improvement candidates. These are proposal-only. V4 must not auto-edit itself based only on thresholds or patterns. A user must approve actual skill changes.

## 7. Controlled Mini-Prompt Chain and Handoff

For multi-step work, V4 can structure small internal prompts and handoff notes. This is bounded and scoped. It must not become an endless autonomous loop and must not execute POWER actions automatically.

Trace templates can materialize next prompts or handoff notes when continuation planning matters.

## 8. Hook Readiness

The hook readiness pack exists for project-local proposals. Hooks are not active by default. Manual trust review, smoke tests and project-local configuration are required before use.

Recommended starting posture: warning/logging-only first.

## 9. Practical Usage

```text
$robyroy-v4
OBJECTIVE: Update this README section.
CONSTRAINTS: no commit, no push, docs only.
```

V4 should handle lifecycle, report and trace/logging discipline internally. Users should not need to list every lifecycle field manually for ordinary V4 work.

## 10. Limitations

- V4 is local skill behavior.
- It depends on the agent following the skill.
- Hooks are not globally active.
- Logs are local/private runtime artifacts.
- V4 is not a replacement for AIOS or other runtime governance systems.
- V4 is not a security product.
