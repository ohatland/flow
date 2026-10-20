---
name: goal
description: Start or revise a flow goal - current state, target state and success criteria with the architect, without an implementation plan. Optionally takes a design doc or spec as design input.
argument-hint: "[idea | goal-slug | path to a design doc]"
disable-model-invocation: true
---

Establish a goal for: $ARGUMENTS

You are the orchestrator. Read `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md`,
`${CLAUDE_PLUGIN_ROOT}/shared/state.md` and `.flow/project.md` if you have not in this
session. The shared folder is `${CLAUDE_PLUGIN_ROOT}/shared`; pass that absolute path to
agents.

A goal says *where we are going and how we know we got there*. It is not a plan: work is
done in steps chosen one at a time with `/flow:next-step`, each planned as a whole and built
in small bits. Keep it short.

If `$ARGUMENTS` names an existing folder in `<state>/goals/`, revise that goal instead. If it
names a design doc or spec, that is the **design input**: it informs the current state,
direction and candidate steps, but its task list is not a plan.

## Process

1. **Current state.** Dispatch `flow:architect` with the idea, the design input path if
   any, and the shared folder path. Duty: `/goal` survey; it answers in its message. If the
   idea depends on facts outside the code (an external API or data source, a library),
   start a research agent in the background at the same time (see "Research" in
   `orchestrating.md`) and pass its note to later agents.
2. **Align.** Use the grilling format (`grilling.md`) with the user on the target state,
   success criteria, what is out of scope, and the *direction* of each contract category.
   Direction only; exact contracts are approved per step. Facts come from agents, decisions
   from the user. Questions that cannot be stated precisely yet go to `## Not yet specified`
   instead of being forced now.
3. **ADR.** If the goal needs a significant architectural decision and the profile has an
   ADR folder, ask the architect (same agent, `SendMessage`) for an ADR proposal and put it
   to the user. Only after approval have it write the ADR, from the approved text.
4. **Where to work** (unless revising), per the profile's `## Git`:
   - Work on the current branch when the profile allows it; or
   - a new branch or worktree: propose a name and base and wait for an explicit yes, then
     create it with the command the profile names.
5. **Write** `<state>/goals/<goal-slug>/goal.md` from the template in `state.md`, with
   Worktree, Branch and Base commit (HEAD there) filled in, and its other files: each
   decision made so far gets a line in `decisions.md`, candidate steps from the design input
   go to `candidates.md`, the architect's hotwash to `notes.md`; open fog goes under
   `## Not yet specified`. Show the user and adjust until approved.
6. **Commit** only an ADR, if one was written. `goal.md` is gitignored.
7. **Next.** In the same checkout: suggest `/flow:next-step <goal-slug>`. In a new
   worktree: subagents run in this session's directory, so tell the user to start a new
   session there and run `/flow:next-step <goal-slug>`.
