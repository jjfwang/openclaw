---
name: manus-coding-task
description: Prepare high-quality coding prompts for Manus and run them through the manus-api skill. Use when the user wants Manus to implement a feature, fix a bug, refactor code, or work on a repository with explicit acceptance criteria. Not for tiny local edits that are faster to do directly.
---

# Manus Coding Task

Use this skill to turn a coding request into a Manus-ready task.

## Workflow

1. Understand the target repo, branch, and exact task.
2. Gather the minimum code/context needed.
3. Write a concrete Manus prompt.
4. Save it to a temp file if the prompt is long.
5. Use the `manus-api` skill to create the task.
6. Wait for completion when the user wants a finished result, or return the task id for long-running work.

## Required prompt sections

Always include:
- repo URL or local repo path
- target branch
- objective
- constraints
- acceptance criteria
- expected output summary

## Prompt template

```text
You are working on this repository:
- Repo: <repo>
- Branch: <branch>

Objective:
<clear statement of the work>

Relevant context:
- <important file or subsystem>
- <important file or subsystem>

Constraints:
- Preserve existing architecture unless necessary
- Run or describe appropriate validation
- Keep changes scoped to the task

Acceptance criteria:
- <criterion 1>
- <criterion 2>
- <criterion 3>

Return:
- summary of changes
- files changed
- tests run
- open risks or follow-ups
```

## Guidance

- Be concrete; Manus does better with explicit acceptance criteria.
- Prefer narrower prompts over vague “improve this repo” prompts.
- If continuing an existing task, summarize what changed since the prior attempt.
- For large jobs, ask Manus for a scoped implementation, not a grand rewrite.

## References

Read `references/examples.md` when you need examples for bugfix vs feature vs refactor prompts.
