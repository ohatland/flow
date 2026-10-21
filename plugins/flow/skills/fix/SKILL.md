---
name: fix
description: Fix a bug outside a goal with a lighter flow loop - reproduce with a red you can check, minimise, hypothesise, fix the cause with a regression test, the gate and one review. For broken intended behavior, not new behavior. Also chores - small internal changes in no contract category (tooling, test hygiene, cleanups) - with the same record, gate and review.
argument-hint: "<bug description>"
disable-model-invocation: true
---

Fix: $ARGUMENTS

A fix restores intended behavior. A **chore** is a small internal change in no contract
category: tooling, test hygiene, a cleanup, a helper. Its record has `## Change` (what and
why, with the candidate step or observation it comes from) in place of `## Problem` and
`## Expected`, and the developer skips the reproduction loop. New behavior, or a change in
a contract category beyond restoring the intended behavior, is a contract change: propose
a goal or step instead. For both, changing what a committed test requires is the user's
decision (step 2); refactoring tests is allowed.

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` for dispatch, questions and commits
(read it, `state.md` and `.flow/project.md` if you have not). The record is a fix file
instead of a step file.

1. **Place.** Work where the profile's `## Git` allows. If that needs a new branch or
   worktree, propose a name and base and create it after an explicit yes.
2. **Record.** Write `<state>/goals/fixes/<YYYY-MM-DD>-<slug>.md` from the template in
   `state.md`: Base commit (current `HEAD`), `## Problem` (what happens, with the
   reproduction the user gave), `## Expected` (what should happen and where that is
   decided). When the problem is a wrong text or value, search the whole repo for it first
   and list every hit in Problem. Number questions in a fix F1, F2, ... so they never
   collide with a goal's Q numbers. Confirm Expected with the user if it is not written
   down. List every change the fix makes to what committed tests require (a test or
   assertion removed, an expected value changed), and get approval for all of them in one
   question.
3. **Fix.** Dispatch `flow:developer` (record its ID under `## Agents`) with the fix file, the gate command line and the
   shared folder path. It follows its "Bug fixes and chores" section: for a fix, a red loop with a recorded
   command and output, minimised, 3-5 ranked hypotheses, then the fix with the regression
   test red before and green after. "No correct seam for a test" is a finding: put it to the
   user. For a chore: the change itself, test-first where it has behavior, cleaned up.
4. **Gate.** Run the gate, output to a file. Failures go back to the developer (same
   agent).
5. **Review.** One `flow:reviewer`, axis `fix` (its ID under `## Agents`). Blockers and
   majors go back to the same developer once, and the same reviewer checks the result;
   after that, the user decides.
6. **Close.** Record the review and a trace line per agent, write your own hotwash under
   the fix file's top-level `## Hotwash` (the developer's stays in its `### Hotwash`),
   let the user read the diff (`orchestrating.md`, "Commits"), commit, report. If the
   hotwashes or traces show workflow friction, add a line to `<state>/goals/process-log.md`.
