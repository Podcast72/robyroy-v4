# Validation

Run validation from the repository root:

```bash
python3 scripts/v4_doctor_check.py
python3 scripts/v4_contract_check.py
python3 scripts/v4_prompt_runner.py --list
```

## Doctor Check

Checks required files, contract JSON, active runtime behavior, automatic runner settings and cautious claim rules.

## Contract Check

Validates contract files, required failure codes, capabilities, blocked actions and report schema.

## Report Check

Use `v4_report_check.py` to check final receipts:

```bash
python3 scripts/v4_report_check.py path/to/final-report.md
```

For V4 reports, missing lifecycle statuses should produce warnings. A complete modern receipt should include `V4_SESSION_STATUS`, `EVENT_LOGGING_STATUS`, `V4_TRACE_STATUS`, `HANDOFF_STATUS`, `PROMPT_CHAIN_STATUS`, `RUNNER_STATUS`, `REPORT_CHECK_STATUS` and `IMPROVEMENT_CANDIDATE_STATUS`.

## Session Lifecycle Check

If available, `v4_session_lifecycle.py` can orchestrate lightweight session actions:

```bash
python3 scripts/v4_session_lifecycle.py start --mode BUILD --task "short description"
python3 scripts/v4_session_lifecycle.py check-report --report path/to/final-report.md
python3 scripts/v4_session_lifecycle.py finish --status COMPLETED --report path/to/final-report.md
```

These are local helper operations. They do not activate hooks, edit global configuration or provide external runtime enforcement.

Validation should be treated as local evidence, not as a guarantee.
