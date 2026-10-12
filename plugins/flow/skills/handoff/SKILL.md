---
name: handoff
description: Hand flow orchestration over to a fresh session - a short handoff from this orchestrator to its successor, so the user can /clear and continue with /flow:resume.
argument-hint: "[what the next session will focus on]"
disable-model-invocation: true
---

You are the orchestrator. Write a handoff to the next orchestrating session so it can take
over without this conversation. Focus: $ARGUMENTS

## 1. Make durable what should outlive the session

Decisions about the product belong in `goal.md` / step files (Clarifications, Contract) or
ADRs; workflow rules in the plugin or the repo's profile and knowledge; user preferences in
memory. If something is missing, list it and ask before writing it. Uncommitted work is
named, not committed silently.

## 2. Write the handoff

Write `<state>/goals/<goal>/handoff.md` (overwrite). Without an active goal, write
`<state>/goals/handoff.md`. Under about 50 lines; point to paths and hashes, never copy what
they say:

- **Focus**: what the next session does.
- **State**: goal, step and status, worktree and branch, latest commits, uncommitted
  changes, whether the app is running (and its PID if you started it).
- **Process position**: phase in progress and the next command. Phase agents do not
  survive `/clear`; name any that were mid-phase, so the successor restarts from the step
  file.
- **Open threads**: questions waiting for the user, missing approvals, promised follow-ups.
- **Decisions not yet recorded elsewhere**: ideally none.
- **Read first**: the few files the next session needs, in order.
- **Next command and skills**: for example `/flow:next-step <goal>`, plus any skills the
  successor should load.

No secrets or personal data.

## 3. Tell the user

The path, a three-line summary, and: run `/clear`, then `/flow:resume [goal]`.
