---
name: refine
description: Refactor the current flow step with the refiner agent - conventions, warnings, duplication and structure - without changing behavior, then chain into final-review.
argument-hint: "[step-file | goal-slug]"
---

Refine step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Pass the shared folder path to the
agent.

1. **Find the step** with status `Refining`.
2. Dispatch `flow:refiner` with the step file, `goal.md`, the base commit, the gate command
   line, open findings routed to `refine`, and the shared folder path; in a later round,
   resume the step's refiner with them instead (`orchestrating.md`, "One agent per role").
3. On `DONE`: run the gate with output saved to a file and read the summary. A FAIL sends
   the refiner back (same agent, `SendMessage`). Then compare the refiner's files
   (`git status --porcelain`, new files included) with `git diff --name-only <base> HEAD`:
   each file the refiner changed outside the step's files must be listed under
   **Outside the step** with a ring and a tie, and stay out of areas the profile names as
   another owner's. If not, send the refiner back to revert it or record it.
4. Record the refiner's trace line in `## Refinement`. If the refiner changed nothing, skip
   the commit. Otherwise commit.
5. Set the status to `Reviewing`, report the restructuring, measurements and observations
   in a few lines, and call the Skill tool with `flow:final-review`.

If tests fail and the refiner cannot fix them without changing behavior, report that
plainly and do not move the step on.
