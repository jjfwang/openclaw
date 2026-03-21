---
name: manus-review-loop
description: Orchestrate a simple OpenClaw-side implementation loop where Manus builds, then OpenClaw reviews the result locally or with another coding agent before deciding on a follow-up Manus iteration. Use when the user wants Manus work checked instead of blindly accepted.
---

# Manus Review Loop

Use OpenClaw as the orchestrator. Manus builds; OpenClaw verifies.

## Default loop

1. Use `manus-coding-task` to prepare and send the implementation request.
2. Wait for Manus completion or fetch the current task state.
3. Review the result using one or more of:
   - direct repo inspection
   - test/typecheck/build runs
   - a coding agent for independent review
4. If problems remain, send a focused continuation prompt with `--continue-task-id`.
5. Repeat until the result is good enough.

## Review strategy

Prefer this order:
1. local tests/typecheck/build
2. direct code inspection
3. optional independent challenger/collaborator agent

## Continuation prompt pattern

```text
Follow up on the prior task.

What still needs to be fixed:
- <issue 1>
- <issue 2>

Additional constraints:
- keep previous good changes
- do not rewrite unrelated modules

Acceptance criteria:
- <criterion 1>
- <criterion 2>
```

## Guidance

- Do not blindly trust Manus output.
- Keep each follow-up prompt narrow and evidence-based.
- If local edits are now simpler than another remote iteration, stop using Manus and patch locally.
