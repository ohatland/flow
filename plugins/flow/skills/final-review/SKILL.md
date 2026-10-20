---
name: final-review
description: Final gate for a flow step - the gate, parallel reviewers (spec, slop and the profile's axes), route findings, then mark Done and run the retro when it is due.
argument-hint: "[step-file | goal-slug]"
---

Review step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session).

1. **Find the step** with status `Reviewing`. This round is the number of `## Round`
   entries in `review.md` plus one.
2. **Gate.** Run the gate with output saved to a file under the scratchpad or `$TMPDIR`;
   read the summary.
3. **Gate failures** need no reviewers: build or test failures route to `implement`,
   formatting and lint failures to `refine`. A failure the agents cannot fix (a container or
   service not reachable) is `BLOCKED`: tell the user what to do and rerun the gate. Record
   gate failures as the round's findings and go to step 6.
4. **Review.** One `flow:reviewer` per axis, launched together in one message: `spec`,
   `slop`, and each axis under the profile's `## Review axes` whose `Applies when:` paths (if it has the line) the step's diff touches (from round 2: the diff
   since the previous round; `spec` always runs); name skipped axes in
   the round. For `Size: small`: `spec` and the axes whose `Applies when:` paths the diff
   touches, nothing else. Each axis has one reviewer for the whole step (`orchestrating.md`,
   "One agent per role"): the first time an axis runs, dispatch it with the step folder,
   the goal folder, base commit, gate report path, its axis and the shared folder path; in later
   rounds, resume it with the round number, the new gate report path and the commit the
   previous round reviewed, so it checks its own earlier findings and the diff since.
5. **Collect.** Keep findings per axis: one axis can mask another, so spec findings are not
   merged into or reranked against slop findings. Within an axis, drop findings without
   concrete evidence; across axes, mark exact duplicates (same file:line and cause) once
   with both axes named.
6. **Record** `## Round <n>` in `review.md`: the commit reviewed (`HEAD`), the gate
   result, one findings table per axis (severity, title, file:line, route, `Resolved in` empty; minors have neither until the user chooses to fix them, then they
   get a route and `Resolved in` like the rest),
   **Where the user should look**, the reviewers' Hotwash checks and Hotwash blocks, and a
   trace line per reviewer.
7. **Route.** From round 2 on, open findings go back to a phase only when the user says so:
   put the blockers and majors left, and any minors, to the user with the options another
   round, a narrow round (wording only, `orchestrating.md`), carrying them over as a
   candidate step in `candidates.md` or a `/flow:fix`, or accepting them. After round 3, recommend
   carrying them over; a fourth round runs only when the user asks for it. Carried over or
   accepted, the step goes on as if they were minors. Otherwise:
   - No `blocker` or `major`: set `Status: Done`, add a row to the goal's Progress table
     (step, result, direction from the gate if it has one, learned, peak context
     impl/verify/refine/review), and give the user the digest. Write your own `## Hotwash`
     in `step.md` (`orchestrating.md`). Then, when the retro is due (`orchestrating.md`,
     "Finishing a phase"; this step counts), call the Skill tool with `flow:retro` for the
     `Done` steps with an empty `## Retro`. Otherwise add one dated line per open friction item from the hotwashes
     (yours and the agents' Improve lines that name the process) to
     `<state>/goals/process-log.md`. Then stop the app if you started it, and suggest
     `/flow:handoff` + `/clear` before `/flow:next-step` (or `/flow:close-goal` if the
     success criteria look met).
   - Findings routed to `user`: put them to the user in the grilling format first.
   - Otherwise set the status to `Implementing` if any finding routes to `implement`, else
     `Refining`, and call the Skill tool with that phase (`flow:implement` or
     `flow:refine`); it fixes the open findings first, and the step comes back here.

Nothing to commit in this phase unless a later phase changes code. The digest is short:
verdict, blocking findings (spec first), minor findings, places worth a human look, and
any `Not run` criteria from `verification.md` the user has not confirmed yet.
