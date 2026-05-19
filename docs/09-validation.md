# Validation

Run validation from the repository root:

```bash
python3 scripts/v4_doctor_check.py
python3 scripts/v4_contract_check.py
python3 scripts/v4_prompt_runner.py --list
```

## Doctor check

Checks required files, contract JSON, active runtime behavior, automatic runner settings and cautious claim rules.

## Contract check

Validates contract files, required failure codes, capabilities, blocked actions and report schema.

## Prompt runner check

Lists available mini-prompts and confirms the mini-prompt library can be read.

Validation should be treated as local evidence, not as a guarantee.
