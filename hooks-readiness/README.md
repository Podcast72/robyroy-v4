# Robyroy-V4 Codex Hook Readiness Pack

This pack contains proposal-only hook templates for Robyroy-V4. It is not active by default.

Codex lifecycle hooks can run deterministic scripts during events such as `UserPromptSubmit`, `PreToolUse` and `Stop`. Robyroy-V4 can use this model in the future for lightweight logging, warning-only safety checks and controlled continuation reviews.

The recommended first hook is warning-only: either a report checker or a Stop continuation checker that requires explicit continuation markers.

Hooks must be reviewed manually because they run inside the agent lifecycle. A small mistake can block useful work, hide evidence or create continuation loops.

If hooks are ever activated later, disable or remove them by reversing the reviewed configuration snippet and removing the trusted script registration. Do not enable these templates globally without a separate trust review.

Global activation is intentionally avoided. This pack is a readiness layer, not runtime enforcement and not a global Codex configuration change.
