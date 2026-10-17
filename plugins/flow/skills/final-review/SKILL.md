---
name: final-review
description: Final gate for a flow step - the gate, parallel reviewers (spec, slop and the profile's axes), route findings, then mark Done and run the retro.
argument-hint: "[step-file | goal-slug]"
---

Review step: $ARGUMENTS

Follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read it, `state.md` next to it and
`.flow/project.md`, if you have not in this session).

1. **Find the step** with status `Reviewing`. This round is the number of `### Round`
   entries under `## Review` plus one.
2. **Gate.** Run the gate with output saved to a file under the scratchpad or `$TMPDIR`;
   read the summary.
3. **Gate failures** need no reviewers: build or test failures route to `implement`,
   formatting and lint failures to `refine`. A failure the agents cannot fix (a container or
   service not reachable) is `BLOCKED`: tell the user what to do and rerun the gate. Record
   gate failures as the round's findings and go to step 6.
4. **Review.** Dispatch one `flow:reviewer` per axis together in one message, in the
   foreground: `spec`, `slop`, and each axis under the profile's `## Review axes` whose
   `Applies when:` paths (if it has the line) the step's diff touches; name skipped axes in
   the round. Give each
   the step file, `goal.md`, base commit, gate report path, its axis, and the shared folder
   path.
5. **Collect.** Keep findings per axis: one axis can mask another, so spec findings are not
   merged into or reranked against slop findings. Within an axis, drop findings without
   concrete evidence; across axes, mark exact duplicates (same file:line and cause) once
   with both axes named.
6. **Record** `### Round <n>` under `## Review`: the gate result, one findings table per
   axis (severity, title, file:line, route, `Resolved in` empty; minors have neither until the user chooses to fix them, then they
   get a route and `Resolved in` like the rest),
   **Where the user should look**, the reviewers' Hotwash checks and Hotwash blocks, and a
   trace line per reviewer.
7. **Route.** Round 2 or later with blockers or majors left: stop and let the user decide
   instead of looping again. Otherwise:
   - No `blocker` or `major`: set `Status: Done`, add a row to the goal's Progress table
     (step, result, direction from the gate if it has one, learned, peak context
     impl/verify/refine/review), and give the user the digest. Write your own `## Hotwash`
     in the step file (`orchestrating.md`), then call the Skill tool with `flow:retro` for
     this step. After the retro, stop the app if you started it, and suggest
     `/flow:handoff` + `/clear` before `/flow:next-step` (or `/flow:close-goal` if the
     success criteria look met).
   - Findings routed to `user`: put them to the user in the grilling format first.
   - Otherwise set the status to `Implementing` if any finding routes to `implement`, else
     `Refining`, and call the Skill tool with that phase (`flow:implement` or
     `flow:refine`); it fixes the open findings first, and the step comes back here.

Nothing to commit in this phase unless a later phase changes code. The digest is short:
verdict, blocking findings (spec first), minor findings, places worth a human look, and
any `Not run` criteria from `## Verification` the user has not confirmed yet.
