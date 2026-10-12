---
name: verify
description: Verify the current flow step with the tester agent against its acceptance criteria and contract in the running app or real output, then chain into refine or back to implement.
argument-hint: "[step-file | goal-slug]"
---

Verify step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Pass the shared folder path to the
agent.

1. **Find the step** with status `Verifying`.
2. **App.** Per the profile's `## Running the app`: run its health check; if the app is not
   running, start it as a background command (so it survives the tester) and wait for
   health. If it cannot start, tell the user what is needed; the tester may still run the
   automated tests.
3. Dispatch `flow:tester` with the step file, `goal.md`, the base commit, the gate command
   line, the shared folder path, and that the app is running and must be left running.
4. Handle `QUESTIONS`, `BLOCKED` and `PARTIAL` per `orchestrating.md`. When the user
   supplies a missing fact about running the app, record it for the retro (it belongs in
   the repo's knowledge).
5. Record the tester's trace line in `## Verification`.
6. **`PASSED`**: set the status to `Refining`, commit any tests the tester added, report
   criteria results, findings and observations in a few lines, give the user the exact
   steps for each `Not run` criterion (they stay open until the user confirms), and call
   the Skill tool with `flow:refine`.
7. **`FAILED`**: present the failures. A failure where the contract itself looks wrong is
   the user's decision; everything else goes back to the developer. Commit the tester's
   tests, set the status to `Implementing`, and call the Skill tool with `flow:implement`.
