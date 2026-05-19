# Controlled Mini-Prompt Chain

A documentation-heavy task can be split into bounded internal steps.

```text
$robyroy-v4
Run a controlled documentation update with validation and final receipt.
```

Example internal chain:

1. Create or update the Goal Contract.
2. Check scope and forbidden targets.
3. Validate the final report.

Each step is checked before use. The chain stops if the next step requires POWER, unclear scope or a forbidden action.
