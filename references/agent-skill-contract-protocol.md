# Agent Skill Contract Protocol

A governed skill is an operational contract, not only a prose instruction file. `SKILL.md` is still the human-readable entrypoint, but it is not enough for stable governance because prose is hard to validate.

Robyroy-V4 adds contract JSON:

- `skill.contract.json`: identity, lineage, modes, claim policy, failure policy and confirmation requirements.
- `capabilities.json`: allowed capabilities and blocked actions.
- `failure_codes.json`: stable warn/block failures with next steps and repair hints.
- `report_schema.json`: final receipt requirements.
- `repair_hints.json`: allowed and forbidden repair patterns.

Doctor/check scripts parse these files locally and fail closed when risky fields are missing or invalid. This pattern connects conceptually with AIOS: the skill can declare intent and constraints, while a runtime or governance layer can enforce actions, approvals and boundaries. V4 itself is not a security boundary.
