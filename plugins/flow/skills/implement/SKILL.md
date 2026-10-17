---
name: implement
description: Implement the current flow step with the developer agent, relay its questions to the user, commit, and chain into verify.
argument-hint: "[step-file | goal-slug]"
---

Implement step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Pass the shared folder path to the
agent.

1. **Find the step** with status `Planned` or `Implementing`. Stop if its Contract has no
   approval date: the user approves it with `/flow:next-step` first. Check that you are in
   the goal's worktree and branch.
2. Set the status to `Implementing` and dispatch `flow:developer` with the step file,
   `goal.md`, the base commit, the gate command line, open items to fix first
   (Verification failures, review findings routed to `implement` with an empty
   `Resolved in`), the step's Size, and the shared folder path.
3. Handle `QUESTIONS`, `BLOCKED` and `PARTIAL` per `orchestrating.md`.
4. On `DONE`: look at `git status --short` and `git diff --stat`, and the agent's
   `## Implementation` section only. Record its trace line there (`orchestrating.md`). If
   the change needs an action under the profile's `## Stop and ask` to take effect, tell
   the user; it is their call.
   When the developer's Unsure or observations name a reading of the contract that is
   the user's to choose (wording that allows two behaviors), put it to the user in the
   grilling format now and record the answer in `## Clarifications`; verify starts once
   it is answered.
5. Commit the code and report in a few lines: what changed, the developer's own decisions,
   and its observations. Then set the status to `Verifying` and call the Skill tool with
   `flow:verify`; for `Size: small`, set it to `Reviewing` and call `flow:final-review`
   instead.
