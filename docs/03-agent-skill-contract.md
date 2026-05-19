# Agent Skill Contract

A free-form prompt can guide behavior, but it is hard to validate. Robyroy-V4 uses a small contract layer so important rules are represented as machine-readable files.

## skill.contract.json

Defines the skill identity, version, lineage, modes, claim policy, failure policy, active runtime behaviors and automatic internal runner settings.

## capabilities.json

Lists allowed capabilities and blocked actions. This makes the skill's operating surface explicit.

## failure_codes.json

Defines stable failure codes with severity, user-facing message, next steps, repair hints and `auto_apply:false`.

## report_schema.json

Defines required final receipt sections and accepted status values.

## repair_hints.json

Lists allowed and forbidden repair patterns so recovery actions remain controlled.

Contract files do not replace judgment, but they make the operating pattern easier to inspect and test than a prompt alone.
