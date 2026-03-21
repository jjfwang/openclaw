# Manus via OpenClaw

## Recommended mental model

- OpenClaw = orchestrator / user-facing control plane
- Manus = remote builder/executor
- Codex/other coding agents = reviewer, collaborator, or local fallback

## Why this is cleaner than ideation-as-orchestrator

Using OpenClaw directly avoids a stack like:

Human -> OpenClaw -> ideation -> OpenClaw CLI -> Manus

That recursive orchestration makes debugging and state tracking harder.

A cleaner stack is:

Human -> OpenClaw -> Manus API

Optionally:

Human -> OpenClaw -> Manus API
                \-> Codex / local tools for review and follow-up

## When to prefer Manus

Prefer Manus when:
- the task benefits from a remote sandbox
- the task needs its own longer-running execution context
- the user explicitly asked for Manus

## When not to prefer Manus

Do not default to Manus when:
- the fix is tiny and can be edited directly
- a local coding agent is faster and easier to verify
- the task is mostly analysis rather than execution
