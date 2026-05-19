# V4 Mini-Prompts

The canonical mini-prompt library is in `scripts/v4_prompt_runner.py`. These prompts are templates only and must not execute file changes by themselves.

## create_goal_contract

MODE:
GOAL CONTRACT CREATION

Define:
- User goal
- Exact workspace
- Allowed files/paths
- Forbidden files/paths
- Success criteria
- Validation commands
- Stop conditions
- Claim limits

Do not proceed to write actions until the Goal Contract is clear.

## run_safe_inventory

MODE:
SAFE INVENTORY

Inspect only the declared workspace.
Do not modify files.
Do not scan home-wide directories.
List:
- relevant files
- candidate files to edit
- risks
- missing context
- recommended next step

## run_scope_check

MODE:
SCOPE CHECK

Before any write:
- confirm target path
- confirm allowed root
- confirm forbidden paths
- check whether the target touches config, hooks, secrets, V3, AIOS repos, public repos or global settings
If unsafe, stop with failure code.

## create_patch_plan

MODE:
PATCH PLAN

Create a minimal patch plan:
- files to create
- files to modify
- reason for each change
- validation for each change
- rollback notes
Do not edit until the plan is coherent and inside scope.

## validate_contract

MODE:
CONTRACT VALIDATION

Validate:
- skill.contract.json
- capabilities.json
- failure_codes.json
- report_schema.json
- repair_hints.json
Check JSON parse, required fields, blocked actions, required outputs, failure policy and auto_apply:false.

## validate_report

MODE:
REPORT VALIDATION

Check final report contains:
- MODE
- GOAL
- SCOPE
- FILES_CREATED
- FILES_MODIFIED
- SCRIPTS_COMMANDS_USED
- TESTS_VALIDATIONS
- LIMITS
- STATUS
- NEXT_ACTION
- STOP_CONDITIONS
If missing, fix the report before final answer.

## log_improvement_candidate

MODE:
PASSIVE IMPROVEMENT LOG

If the task reveals a reusable improvement:
- write one JSONL candidate
- do not apply it
- mark requires_user_approval:true
- mark auto_apply:false
- summarize the reason

## downgrade_claim

MODE:
CLAIM DOWNGRADE

Review the claim.
If tests/evidence are insufficient:
- remove VERIFIED
- remove production-ready
- remove release-ready
- replace with evidence-limited status
- list missing proof

## stop_with_failure_code

MODE:
CONTROLLED STOP

Stop the task and report:
- failure_code
- severity
- reason
- allowed_next_steps
- files untouched
- what evidence is missing
Do not invent fallback.

## final_receipt

MODE:
FINAL RECEIPT

Return:
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

## automatic_internal_runner

Use the local controlled task runner or equivalent runner logic automatically when a V4 task is multi-step, repetitive, documentation-heavy, validation-heavy, or needs controlled continuation. Roberto does not need to manually launch `python3 scripts/v4_task_runner.py`.

The runner may plan up to 3 internal steps. Each step must pass Goal Contract alignment, scope, mode, risk, forbidden target and stop-condition checks. Use only SAFE or BUILD low/medium-risk steps. Stop for POWER, network, sudo, git push, git commit, config edits, hooks, robyroy-v3 edits, destructive operations, unclear scope, or unsupported claims.
