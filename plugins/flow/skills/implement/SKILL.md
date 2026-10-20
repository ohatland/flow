---
name: implement
description: Implement the current flow step bit by bit with the developer agent - a spec check of each bit, the user reads its diff, commit - relay questions to the user, and chain into verify or refine when the bits are done.
argument-hint: "[step-file | goal-slug]"
---

Implement step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session). Pass the shared folder path to the
agents.

1. **Find the step** with status `Planned` or `Implementing`. Stop if its Contract has no
   approval date: the user approves it with `/flow:next-step` first. Check that you are in
   the goal's worktree and branch. Set the status to `Implementing`.
2. **Next bit**: the first `### Bit` under `## Bits` with Status `planned`. Bits that a later
   phase added (`V<n>` for verification failures, `R<n>` for review findings, `Cleanup` for
   the minors the user chose) carry their open items. When the bit has `User looks: yes`,
   make sure the app runs (profile `## Running the app`: health check, else start it in the
   background and wait for health).
3. **Developer.** For the step's first bit, dispatch `flow:developer` with the step folder,
   the goal folder, the base commit, the gate command line, the bit's number, and the shared
   folder path, and record its ID under `## Agents`. For each later bit, resume it
   (`orchestrating.md`, "One agent per role") with the bit's number, its open items and the
   commit it starts from. Handle `QUESTIONS`, `BLOCKED` and `PARTIAL` per `orchestrating.md`.
4. **On `DONE`**: look at `git status --short`, `git diff --stat` and the bit's section in
   `implementation.md` only. If the change needs an action under the profile's
   `## Stop and ask` to take effect, tell the user; it is their call. A reading of the
   contract the developer names as the user's to choose goes to the user now (grilling
   format, recorded in `## Clarifications`).
5. **Bit check.** Dispatch the `spec` reviewer for the step's first bit check (its ID under
   `## Agents` as `reviewer spec`), else resume it, with `Bit check <n>` and the commit the
   bit starts from. Record its answer under `## Bit <n>` in `review.md`. A blocker or major
   goes back to the developer once (same agent) and the reviewer checks again; after that,
   it goes to the user with the diff.
6. **The user reads the diff** (`orchestrating.md`, "Commits"), with the bit check's result
   and, for `User looks: yes`, the before and after URLs. Comments go back to the developer
   and the diff is shown again. When the bit shows the plan no longer fits (the developer's
   Observations or the user's comment), resume the architect (duty: adjust the plan); a
   changed contract or criterion is the user's decision.
7. **Commit** after the user's approval, set the bit's Status to `done <commit>`, and record
   the developer's trace line at the end of the bit's section (`orchestrating.md`, "Trace
   every agent"). Then go to 2 for the next bit, without asking.
8. **When no bit is `planned`**, take the shortest path that still checks the change:
   - A `Cleanup` bit: `Reviewing`, `flow:final-review` (it closes the step).
   - Verification failures (`V<n>`), or a fixed finding changed behavior a criterion that the
     tester checks describes: `Verifying`, `flow:verify`, for those criteria.
   - The step's first pass: `Verifying` and `flow:verify` with `Verify: yes`; else
     `Refining`, `flow:refine`.
   - Otherwise: `Refining`, `flow:refine` when a finding routed to `refine` is still open;
     else `Reviewing`, `flow:final-review`.
