---
name: close-goal
description: Close a flow goal - verify success criteria end to end, review the whole goal for drift, check docs and glossary against what shipped, and run a goal retrospective.
argument-hint: "[goal-slug]"
disable-model-invocation: true
---

Close goal: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Small steps can each pass review
while the whole drifts; this checks the whole. Keep your own context small.

Find the goal per `state.md`. If any step is not `Done`, tell the user and ask whether to
continue. The goal base is `Base commit` in `goal.md`.

## 1. Whole-goal check

First run the **gate** over the goal, `.flow/check <goal base> --all-tests`, with output to
a file: the reviewer needs its report, and it may build and test, which would disturb the
tester's running app. Then start the app per the profile if needed, and launch these
together in one message (wait for all three; you aggregate them):

- **Verify.** `flow:tester` verifies the goal's **success criteria** end to end. It reports
  in its message only; it does not edit step files.
- **Review.** `flow:reviewer`, axis `goal`, over `git diff <goal base>`, with the gate
  report path.
- **Architecture.** `flow:architect`, duty `/close-goal` architecture review, including
  proposed changes to the glossary, docs and knowledge skills. No files.

Present the combined result. Each issue the user wants fixed becomes a step through
`/flow:next-step`; the goal stays active. Proposed changes to ADRs, the glossary, docs or
knowledge skills are applied only after the user approves them, and committed separately.

## 2. Retrospective

Call the Skill tool with `flow:retro`, with this goal as scope.

## 3. Close

Tick the success criteria, set `Status: Done`, add a short `## Retrospective` to `goal.md`
(what was learned, what changed in the workflow, the peak context per phase). Stop the app.
Give the user a summary for the merge or release:

- **Evidence**: the tester's screenshot or output paths and the gate summary.
- **Merge danger**: one-way door (a migration, a public interface others depend on, data
  or published output rewritten) or two-way door (revert is enough), and the blast radius.

Pushing, merging and publishing are the user's.
