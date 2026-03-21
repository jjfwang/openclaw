---
name: manus-api
description: Delegate coding, planning, or execution tasks to Manus through the Manus task API. Use when the user wants work run by Manus specifically, when OpenClaw should create/poll/continue Manus tasks, or when replacing ideation's Manus builder with a direct OpenClaw skill. Not for generic local coding work when Codex or direct file edits are simpler.
---

# Manus API

Use Manus as a remote builder/executor, with OpenClaw staying in charge.

## What this skill is for

Use this skill when you need to:
- send a coding or planning task to Manus
- continue an existing Manus task thread
- poll a Manus task until it finishes
- inspect the raw task state/output

Prefer this over ad-hoc curl because the helper script already handles:
- `API_KEY` auth header
- Manus base URL selection
- loading the Manus key from env vars or an env file
- consistent JSON output

## Local assumptions

- Helper script: `/home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py`
- Preferred env vars: `MANUS_API_KEY` / `MANUS_API_BASE`
- Backward-compatible env vars: `ORCH_MANUS_API_KEY` / `ORCH_MANUS_API_BASE`
- Preferred global env file on this machine: `~/.openclaw/.env`
- Legacy fallback env file: `/home/pi/Repos/ideation/manus-orchestrator/.env`
- Default API base URL: `https://api.manus.ai/v1`

This skill now prefers OpenClaw's own global env file so it can outlive ideation cleanly.

## Commands

### Check task creation

```bash
python3 /home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py create \
  --prompt "Say hello and summarize what you can do." \
  --agent-profile manus-1.6-max
```

### Create from a prompt file

```bash
python3 /home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py create \
  --prompt-file /tmp/manus-prompt.txt \
  --agent-profile manus-1.6-max
```

### Inspect a task

```bash
python3 /home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py get <TASK_ID>
```

### Wait for completion

```bash
python3 /home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py wait <TASK_ID> \
  --poll-interval 10 \
  --timeout 3600
```

### Continue an existing task thread

```bash
python3 /home/pi/.openclaw/workspace/skills/manus-api/scripts/manus_task.py create \
  --continue-task-id <TASK_ID> \
  --prompt-file /tmp/followup.txt
```

## Prompt pattern

When sending coding work to Manus, include all of these:
- objective
- repo URL or repo path
- target branch
- files/features to change
- acceptance criteria
- constraints (stack, style, security, tests)
- expected output format

Good prompt skeleton:

```text
You are working on this repository:
- Repo: <repo>
- Branch: <branch>

Task:
<what to build/fix>

Constraints:
- <constraint 1>
- <constraint 2>

Acceptance criteria:
- <criterion 1>
- <criterion 2>

When done, summarize:
- files changed
- tests run
- remaining risks
```

## Operational guidance

- Prefer `create` + `wait` for one-shot tasks.
- Prefer `continue-task-id` when iterating on the same Manus thread.
- Keep prompts explicit; Manus is a builder, not your orchestrator.
- Treat Manus output as something to review, not blindly trust.
- For long jobs, run the helper through `exec` background mode and monitor it.

## Boundaries

- Do not claim Manus is part of OpenClaw core; it is an external task API.
- Do not hardcode API keys into commands or files.
- Do not expose `.env` contents back to the user.
- If a task needs local repo edits in this workspace, decide whether direct edits or a coding agent are simpler before defaulting to Manus.
