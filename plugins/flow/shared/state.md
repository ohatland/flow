# Goal and step state

All workflow state lives in files under `<state>/goals/`, where `<state>` is the state folder
from the profile's `## Records` (default `.agent-work/`). It is gitignored: nothing here is
committed; code is. With worktrees, `<state>` is shared by all of them (a symlink), so every
worktree sees the same goals.

```text
<state>/goals/<goal-slug>/
  goal.md                 current state, target state, success criteria, progress
  steps/<NN>-<slug>.md    one increment: task, approved contract, acceptance criteria,
                          and the record of every phase
  research/<slug>.md      dated, cited notes from research or exploration agents; agents
                          get them by path instead of exploring again
  traces/<NN>-<phase>-<role>.txt   observed tool calls per agent, from shared/trace.py
  handoff.md              orchestrator handoff between sessions (deleted on resume)
<state>/goals/fixes/<YYYY-MM-DD>-<slug>.md   bug fixes outside a goal
<state>/goals/fixes/traces/<slug>-<role>.txt  traces of fix agents
<state>/goals/process-log.md                  workflow friction for the next retro
```

Write these files in the language the profile's `## Project` names; keep the headings below
as they are, since skills and agents find sections by them.

## goal.md

```markdown
# Goal: <title>

- Status: Active
- Started: <YYYY-MM-DD>
- Worktree: <absolute path>
- Branch: <branch>
- Base commit: <hash of HEAD when the goal was approved>
- Design input: <path to a design doc or spec, or None>

## Current state

<What exists today and what the problem is. A few sentences or bullets.>

## Target state

<What is true when we are done, from the user's and the system's point of view.>

## Success criteria

- [ ] <Observable outcome that can be verified in the running app, the output or through
  the public API>

## Out of scope

- <What this goal deliberately does not do. Closed: these never become steps.>

## Decisions so far

- <One line per decision, with a pointer: step file, ADR or research note.>

## Not yet specified

- <Fog: questions that cannot be stated precisely yet. Later steps and research turn them
  into askable questions; they are not pre-sliced into steps.>

## Direction and constraints

<Approved direction for each contract category. Links to relevant ADRs and glossary terms.>

## Candidate steps

<Optional. Ideas for later steps, from the design input, retros or observations. Not a plan:
/next-step picks one at a time and may ignore or reorder these.>

## Progress

| Step | Result | Direction | Learned | Peak context (impl/verify/refine/review) |
|---|---|---|---|---|

## Agent notes

<Hotwash and trace line of the architect from /goal and /close-goal.>

## Retrospective

<Written by /close-goal: what was learned, what changed in the workflow, peak context per
phase.>
```

## steps/<NN>-<slug>.md

```markdown
# Step <NN>: <title>

- Goal: [<goal title>](../goal.md)
- Status: Planned
- Size: normal
- Base commit: <hash of HEAD when the contract was approved>

## Task

<What this step achieves and why, in two to five sentences.>

## Contract

Approved by the user on <YYYY-MM-DD>.

### <one section per category in the profile's ## Contract>

<What changes in this category, or None.>

## Acceptance criteria

1. <Observable scenario: given ..., when ..., then ...>

<Mark a criterion `(verified by the user)` when checking it needs an action under the
profile's `## Stop and ask`. Word criteria about existing tests as "no assertion or expected
value changed in tests committed before the step's base commit", so refine can restructure
tests and the step can adjust its own new tests.>

## Test seams

<Not part of the contract; accepted by default. The highest seams to test at, ideally one,
each with what it catches and what it misses.>

## Clarifications

<Questions raised by phase agents and the user's answers, with dates.>

## Implementation

## Verification

## Refinement

## Review

## Hotwash

## Retro
```

## fixes/<YYYY-MM-DD>-<slug>.md

```markdown
# Fix: <title>

- Base commit: <hash of HEAD when the fix was recorded>
- Branch: <branch>

## Problem

<What happens, with the reproduction.>

## Expected

<What should happen, and where that is decided: a contract, an ADR, a doc, a test or the
user.>

## Implementation

## Review

## Hotwash

## Retro
```

A chore (skill `fix`) has `## Change` in place of `## Problem` and `## Expected`.

## process-log.md

```markdown
<One dated line per open friction item, added at the end of a step or fix; the retro removes
the lines it handled.>

## Retros

- <date> <scope>: <what changed>
```

## Base commit

The Base commit is the point the step's or goal's diff starts from. After merging the main
branch into a goal branch, set it to the merge commit, or the gate and reviews include the
merged changes.

## Status values

`Planned` -> `Implementing` -> `Verifying` -> `Refining` -> `Reviewing` -> `Done`, and back
when a phase sends work back.

## Size

`Size: normal` runs every phase. `Size: small` is for a step whose expected diff is a few files
and whose every acceptance criterion is checked by tests the gate runs, with nothing to judge in
the running app or by eye: it goes `Implementing` -> `Reviewing`, the developer brings its own
diff to the conventions (no refine), and the final review runs `spec` and the profile axes whose
`Applies when:` paths the diff touches. The architect proposes the size; the user approves it
with the contract.

## Finding a step

The step file given, or else the highest-numbered step with the phase's status in the given
goal, or in the only goal with `Status: Active`. Several active goals: ask which one.
