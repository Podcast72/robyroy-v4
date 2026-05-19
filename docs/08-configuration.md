# Configuration

Robyroy-V4 is configured through files inside the skill package.

## Contract

`contract/skill.contract.json` defines the skill identity, modes, runtime behaviors and automatic internal runner settings.

## Capabilities

`contract/capabilities.json` declares allowed capabilities and blocked actions.

## Failure codes

`contract/failure_codes.json` maps common stop conditions to stable codes and repair hints.

## Report schema

`contract/report_schema.json` defines the required final receipt.

## Runner settings

Automatic internal runner settings are declared in `automatic_internal_runner_use`. The default maximum chain length is 3 steps.

## Event logging

Event logging uses `scripts/v4_usage_log.py` and local files under `evolution/`.
