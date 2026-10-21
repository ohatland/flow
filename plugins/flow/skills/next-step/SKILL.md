---
name: next-step
description: Plan the next step toward a flow goal as a whole with the architect, split into bits implemented one at a time, and get the user's explicit approval of its contract, acceptance criteria and bits.
argument-hint: "[goal-slug]"
disable-model-invocation: true
---

Plan the next step toward goal: $ARGUMENTS

You are the orchestrator. Read `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md`,
`${CLAUDE_PLUGIN_ROOT}/shared/state.md` and `.flow/project.md` if you have not in this
session. Pass the shared folder path `${CLAUDE_PLUGIN_ROOT}/shared` to agents.

Find the goal as described in `state.md`. A step is a delivery that belongs together,
planned as a whole and split into 3-8 bits that the developer implements one at a time, each
read by the user before it is committed (`state.md`, "Bits"). It says *what*, never *how*.

## Process

1. **Check place.** The current directory must be the goal's Worktree and on its Branch;
   if not, tell the user and stop. `git status --short` must be clean, or the user decides
   what to do with the changes. If this session already took a step to `Done`, ask the user
   to run `/flow:handoff`, `/clear` and `/flow:resume` first.
2. **Read** `goal.md`, `candidates.md` (the parts for the area), the previous steps' Task
   and Retro (`sections.sh <step folder>/step.md Task Retro`), and
   `git log --oneline <goal base>..HEAD`. If the retro is due (`orchestrating.md`, "Finishing
   a phase"), call the Skill tool with `flow:retro` first; its candidate steps are input here.
3. **Done?** If every success criterion is met, suggest `/flow:close-goal` and stop.
4. **Plan.** Dispatch `flow:architect`, duty `/next-step` plan, with the goal folder, the
   previous step folders, research note paths, the peak context of recent phases from their
   trace lines (above about 200k means plan smaller), and the shared folder path. It may
   split goal files that are too large (`state.md`, "Size"); otherwise it answers in its
   message.
5. **Approve the plan.** Present it compactly and put the open questions to the user in the
   grilling format. The contract covers exactly the profile's contract categories that
   change. Do not ask about internal code structure. Questions the user decides by looking at
   the output come with the architect's evidence per option. Get explicit approval of the
   contract, the acceptance criteria and the bits: show the bits one line each (what,
   criteria, `User looks`) and `Verify:` with its reason and the `Estimate:` on one line.
   Show the proposed test seams in one line each; they are accepted unless the user objects.
   More than eight bits, or an implement context above about 200k, means two steps.
6. **Write** `<state>/goals/<goal>/steps/<NN>-<slug>/step.md` from the template in `state.md`
   (numbering from `01`), Status `Planned`, the approved `Verify:` and `## Bits`, the
   architect's `Estimate:`, Base commit = current `HEAD`, with today's approval date, the
   Neighbours, the Test seams and the architect's ID under `## Agents`; questions about this
   step and changes to its plan go to that architect. Record the answered questions under
   `## Clarifications`, a line per decision in `decisions.md`, and remove from
   `candidates.md` what the step does.
7. **Next.** Call the Skill tool with `flow:implement` unless the user wants to stop here
   (for example to hand off to a fresh session first).
