#!/usr/bin/env python3
import argparse
import json

MINI_PROMPTS = {
    "create_goal_contract": {
        "id": "create_goal_contract",
        "purpose": "Create a Goal Contract before a serious task.",
        "when_to_use": "Use before multi-step, risky, file-modifying, migration, validation, repo, public docs, AIOS or skill work.",
        "prompt_text": "MODE:\nGOAL CONTRACT CREATION\n\nDefine:\n- User goal\n- Exact workspace\n- Allowed files/paths\n- Forbidden files/paths\n- Success criteria\n- Validation commands\n- Stop conditions\n- Claim limits\n\nDo not proceed to write actions until the Goal Contract is clear.",
        "required_inputs": ["user_goal", "workspace", "known_constraints"],
        "expected_output": "A concise Goal Contract with success criteria and stop conditions.",
        "stop_rules": ["missing workspace", "unclear goal", "unsafe path"],
    },
    "run_safe_inventory": {
        "id": "run_safe_inventory",
        "purpose": "Perform a read-only inventory.",
        "when_to_use": "Use before planning edits or when scope is still being discovered.",
        "prompt_text": "MODE:\nSAFE INVENTORY\n\nInspect only the declared workspace.\nDo not modify files.\nDo not scan home-wide directories.\nList:\n- relevant files\n- candidate files to edit\n- risks\n- missing context\n- recommended next step",
        "required_inputs": ["declared_workspace"],
        "expected_output": "Relevant files, edit candidates, risks, missing context and next step.",
        "stop_rules": ["workspace missing", "home-wide scan requested"],
    },
    "run_scope_check": {
        "id": "run_scope_check",
        "purpose": "Check scope before writing.",
        "when_to_use": "Use immediately before file creation or modification.",
        "prompt_text": "MODE:\nSCOPE CHECK\n\nBefore any write:\n- confirm target path\n- confirm allowed root\n- confirm forbidden paths\n- check whether the target touches config, hooks, secrets, V3, AIOS repos, public repos or global settings\nIf unsafe, stop with failure code.",
        "required_inputs": ["target_path", "allowed_root", "forbidden_paths"],
        "expected_output": "Allow/warn/block decision with failure code when blocked.",
        "stop_rules": ["outside allowed root", "forbidden target", "global config"],
    },
    "create_patch_plan": {
        "id": "create_patch_plan",
        "purpose": "Prepare narrow changes.",
        "when_to_use": "Use before controlled BUILD edits.",
        "prompt_text": "MODE:\nPATCH PLAN\n\nCreate a minimal patch plan:\n- files to create\n- files to modify\n- reason for each change\n- validation for each change\n- rollback notes\nDo not edit until the plan is coherent and inside scope.",
        "required_inputs": ["goal_contract", "file_inventory"],
        "expected_output": "Minimal patch plan with validation notes.",
        "stop_rules": ["plan outside scope", "missing validation"],
    },
    "validate_contract": {
        "id": "validate_contract",
        "purpose": "Validate Agent Skill Contract files.",
        "when_to_use": "Use after contract edits or before final receipt.",
        "prompt_text": "MODE:\nCONTRACT VALIDATION\n\nValidate:\n- skill.contract.json\n- capabilities.json\n- failure_codes.json\n- report_schema.json\n- repair_hints.json\nCheck JSON parse, required fields, blocked actions, required outputs, failure policy and auto_apply:false.",
        "required_inputs": ["contract_directory"],
        "expected_output": "JSON validation and contract consistency result.",
        "stop_rules": ["invalid json", "missing required fields"],
    },
    "validate_report": {
        "id": "validate_report",
        "purpose": "Check final receipt.",
        "when_to_use": "Use before final answer.",
        "prompt_text": "MODE:\nREPORT VALIDATION\n\nCheck final report contains:\n- MODE\n- GOAL\n- SCOPE\n- FILES_CREATED\n- FILES_MODIFIED\n- SCRIPTS_COMMANDS_USED\n- TESTS_VALIDATIONS\n- LIMITS\n- STATUS\n- NEXT_ACTION\n- STOP_CONDITIONS\nIf missing, fix the report before final answer.",
        "required_inputs": ["final_report_text"],
        "expected_output": "Missing sections and warnings.",
        "stop_rules": ["schema failure"],
    },
    "log_improvement_candidate": {
        "id": "log_improvement_candidate",
        "purpose": "Record a passive improvement candidate.",
        "when_to_use": "Use when the task reveals a reusable improvement.",
        "prompt_text": "MODE:\nPASSIVE IMPROVEMENT LOG\n\nIf the task reveals a reusable improvement:\n- write one JSONL candidate\n- do not apply it\n- mark requires_user_approval:true\n- mark auto_apply:false\n- summarize the reason",
        "required_inputs": ["source_event", "candidate_type", "summary", "suggested_change"],
        "expected_output": "One passive JSONL improvement candidate.",
        "stop_rules": ["would auto-apply", "contains secret"],
    },
    "downgrade_claim": {
        "id": "downgrade_claim",
        "purpose": "Avoid unsupported claims.",
        "when_to_use": "Use when a report or doc sounds stronger than evidence.",
        "prompt_text": "MODE:\nCLAIM DOWNGRADE\n\nReview the claim.\nIf tests/evidence are insufficient:\n- remove VERIFIED\n- remove production-ready\n- remove release-ready\n- replace with evidence-limited status\n- list missing proof",
        "required_inputs": ["claim_text", "evidence"],
        "expected_output": "Evidence-limited replacement claim and missing proof list.",
        "stop_rules": ["claim not supported"],
    },
    "stop_with_failure_code": {
        "id": "stop_with_failure_code",
        "purpose": "Stop in a governed way.",
        "when_to_use": "Use when the task hits a blocked action or unsafe ambiguity.",
        "prompt_text": "MODE:\nCONTROLLED STOP\n\nStop the task and report:\n- failure_code\n- severity\n- reason\n- allowed_next_steps\n- files untouched\n- what evidence is missing\nDo not invent fallback.",
        "required_inputs": ["failure_code", "reason"],
        "expected_output": "Controlled stop report.",
        "stop_rules": ["missing failure code"],
    },
    "final_receipt": {
        "id": "final_receipt",
        "purpose": "Produce final receipt.",
        "when_to_use": "Use at the end of every V4 run.",
        "prompt_text": "MODE:\nFINAL RECEIPT\n\nReturn:\nMODE:\nGOAL:\nSCOPE:\nFILES_CREATED:\nFILES_MODIFIED:\nSCRIPTS_COMMANDS_USED:\nTESTS_VALIDATIONS:\nLIMITS:\nSTATUS:\nNEXT_ACTION:\nSTOP_CONDITIONS:",
        "required_inputs": ["mode", "goal", "scope", "files", "validation", "status"],
        "expected_output": "Final report matching the V4 report schema.",
        "stop_rules": ["missing required report section"],
    },
}

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--show")
    group.add_argument("--json")
    group.add_argument("--chain-plan")
    args = parser.parse_args()
    if args.chain_plan:
        summary = args.chain_plan[:500]
        plan = {
            "ok": True,
            "status": "generated",
            "task_summary": summary,
            "chain_limits": {
                "max_chain_steps_per_task": 3,
                "requires_scope_check": True,
                "requires_goal_alignment": True,
                "auto_execute_safe_build_only": True,
                "auto_loop": False,
            },
            "steps": [
                {"step_index": 1, "mini_prompt_id": "run_scope_check", "status": "generated", "use_rule": "run only if inside declared scope"},
                {"step_index": 2, "mini_prompt_id": "create_patch_plan", "status": "generated", "use_rule": "run only for SAFE or BUILD low-risk work"},
                {"step_index": 3, "mini_prompt_id": "validate_report", "status": "generated", "use_rule": "run before final receipt"},
            ],
            "blocked_rules": ["POWER", "network", "sudo", "git mutation", "config.toml", "hooks", "destructive operations"],
        }
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    if args.list:
        for key in sorted(MINI_PROMPTS):
            print(key)
        return 0
    key = args.show or args.json
    if key not in MINI_PROMPTS:
        print(json.dumps({"ok": False, "error": "unknown mini-prompt", "available": sorted(MINI_PROMPTS)}, indent=2))
        return 1
    item = MINI_PROMPTS[key]
    if args.json:
        print(json.dumps(item, indent=2, ensure_ascii=False))
    else:
        print(item["prompt_text"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
