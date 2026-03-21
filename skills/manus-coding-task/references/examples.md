# Manus prompt examples

## Bug fix

```text
You are working on this repository:
- Repo: <repo>
- Branch: <branch>

Objective:
Fix the failing typecheck in the worker package.

Relevant context:
- apps/worker/src/...
- package.json and tsconfig files may need alignment

Constraints:
- Keep the fix minimal
- Do not change unrelated behavior
- Preserve passing tests

Acceptance criteria:
- pnpm typecheck passes
- existing tests still pass
- summarize exactly what caused the failure
```

## Feature

```text
Objective:
Implement support for <feature> with tests.

Acceptance criteria:
- users can do <thing>
- tests cover success and main failure path
- docs updated if setup/usage changed
```

## Refactor

```text
Objective:
Refactor <module> for clarity without changing external behavior.

Acceptance criteria:
- public behavior unchanged
- tests still pass
- code is simpler and duplication is reduced
```
