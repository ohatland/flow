---
name: next-step
description: Choose the next small increment toward a flow goal with the architect and get the user's explicit approval of its contract and acceptance criteria.
argument-hint: "[goal-slug]"
disable-model-invocation: true
---

Choose the next step toward goal: $ARGUMENTS

You are the orchestrator. Read `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md`,
`${CLAUDE_PLUGIN_ROOT}/shared/state.md` and `.flow/project.md` if you have not in this
session. Pass the shared folder path `${CLAUDE_PLUGIN_ROOT}/shared` to agents.

Find the goal as described in `state.md`. A step is the smallest increment that brings the
goal observably closer, preferably a thin vertical slice verifiable end to end, small
enough for one developer session. It says *what*, never *how*.

## Process

1. **Check place.** The current directory must be the goal's Worktree and on its Branch;
   if not, tell the user and stop. `git status --short` must be clean, or the user decides
   what to do with the changes.
2. **Read** `goal.md`, the previous steps' Task and Retro sections, and
   `git log --oneline <goal base>..HEAD`. If a retro is due (the `Done` steps with an empty
   `## Retro` section have reached the profile's cadence, `## Records`), call the Skill
   tool with `flow:retro` first; its candidate steps are input here.
3. **Done?** If every success criterion is met, suggest `/flow:close-goal` and stop.
4. **Propose.** Dispatch `flow:architect`, duty `/next-step` proposal, with the goal path,
   the previous step file paths, research note paths, the peak context of recent phases from
   their trace lines (above about 200k means slice smaller), and the shared folder path. It
   answers in its message.
5. **Approve the contract.** Present the proposal compactly and put the open questions to
   the user in the grilling format. The contract covers exactly the profile's contract
   categories. Do not ask about internal code structure. Questions the user decides by
   looking at the output come with the architect's evidence per option. Get explicit approval of the
   contract and of the acceptance criteria. Show the proposed test seams in one line each;
   they are accepted unless the user objects. Present the proposed size (`state.md`,
   "Size"): `small` skips verify and refine and narrows the review, so name what makes
   the step qualify; the user approves it with the contract. If the step looks bigger than
   one session, propose a split (a prefactor step first, or expand / migrate / contract for
   a wide mechanical change).
6. **Write** `<state>/goals/<goal>/steps/<NN>-<slug>.md` from the template in `state.md`
   (numbering from `01`), Status `Planned`, the approved Size, Base commit = current
   `HEAD`, with today's approval date, the Test seams and the Code map. Record the answered questions under
   `## Clarifications` and a line per decision under `## Decisions so far` in `goal.md`.
7. **Next.** Call the Skill tool with `flow:implement` unless the user wants to stop here
   (for example to hand off to a fresh session first).
