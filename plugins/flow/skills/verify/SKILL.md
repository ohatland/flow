---
name: verify
description: Verify the current flow step (Verify: yes) with the tester agent against the acceptance criteria left for it and the contract in the running app or real output, then chain into refine or back to implement.
argument-hint: "[step-file | goal-slug]"
---

Verify step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Pass the shared folder path to the
agent.

1. **Find the step** with status `Verifying`. The tester checks the criteria `step.md` leaves
   for it; the gate's tests and the user's looks at the bits cover the rest.
2. **App.** Per the profile's `## Running the app`: run its health check; if the app is not
   running, start it as a background command (so it survives the tester) and wait for
   health. If it cannot start, tell the user what is needed; the tester may still run the
   automated tests.
3. Dispatch `flow:tester` with the step folder, the goal folder, the base commit, the gate command
   line, the shared folder path, and that the app is running and must be left running. In a
   later round, resume the step's tester instead (`orchestrating.md`, "One agent per role")
   with the round number, the criteria to check again and the commit the round starts from.
4. Handle `QUESTIONS`, `BLOCKED` and `PARTIAL` per `orchestrating.md`. When the user
   supplies a missing fact about running the app, record it for the retro (it belongs in
   the repo's knowledge).
5. Record the tester's trace line at the end of `verification.md`.
6. **`PASSED`**: commit any tests the tester added, after the user has read them
   (`orchestrating.md`, "Commits"), report criteria results, findings and
   observations in a few lines, and give the user the exact steps for each `Not run`
   criterion (they stay open until the user confirms). Then set the status to `Refining`
   and call the Skill tool with `flow:refine`; in a later round with no open finding routed
   to `refine`, set it to `Reviewing` and call `flow:final-review` instead.
7. **`FAILED`**: present the failures. A failure where the contract itself looks wrong is
   the user's decision; everything else goes back to the developer as a bit `V<round>` under
   `## Bits` with the failures as its open items. Commit the tester's tests after the user has
   read them, set the status to `Implementing`, and call the Skill tool with `flow:implement`.
