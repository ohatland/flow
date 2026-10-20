# Goal and step state

All workflow state lives in files under `<state>/goals/`, where `<state>` is the state folder
from the profile's `## Records` (default `.agent-work/`). It is gitignored: nothing here is
committed; code is. With worktrees, `<state>` is shared by all of them (a symlink), so every
worktree sees the same goals.

Every agent reads these files, and what it reads early is sent again with every later turn.
So the state is split into small files, each read whole by the roles that need it.

```text
<state>/goals/<goal-slug>/
  goal.md                 where we are going: status, current and target state, success
                          criteria, out of scope, fog, direction, parts, progress
  decisions.md            one line per user decision, with a pointer
  candidates.md           ideas for later steps
  notes.md                the architect's hotwash and trace lines, the goal retrospective
  steps/<NN>-<slug>/
    step.md               the plan: task, approved contract, criteria, neighbours, seams,
                          code map, clarifications, agents, the orchestrator's hotwash, retro
    implementation.md     the developer's record (one file per phase, written by that phase)
    verification.md       the tester's record
    refinement.md         the refiner's record
    review.md             the review rounds, recorded by the orchestrator
  research/<slug>.md      dated, cited notes; agents get them by path instead of exploring
  traces/<NN>-<phase>-<role>.txt   observed tool calls per agent, from shared/trace.py
  handoff.md              orchestrator handoff between sessions (deleted on resume)
<state>/goals/fixes/<YYYY-MM-DD>-<slug>.md   bug fixes and chores outside a goal
<state>/goals/fixes/traces/<slug>-<role>.txt  traces of fix agents
<state>/goals/process-log.md                  workflow friction for the next retro
```

Write these files in the language the profile's `## Project` names; keep the headings below
as they are, since skills and agents find sections by them.

## Size

Each file stays under about 200 lines. When one grows past that, the architect splits it in
its next duty, by topic, into `<file>-<topic>.md` next to it (`decisions-symbols.md`,
`candidates-data.md`), and lists each part with one line under `## Parts` in `goal.md`; agents
then read only the parts their task touches. When `goal.md` itself outgrows that, because its
target state spans areas that can be finished independently, the architect proposes to the
user to split the goal into separate goals. A `step.md` past about 200 lines means the step is
too big: the architect slices the next steps smaller.

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

## Not yet specified

- <Fog: questions that cannot be stated precisely yet. Later steps and research turn them
  into askable questions; they are not pre-sliced into steps.>

## Direction and constraints

<Approved direction for each contract category. Links to relevant ADRs and glossary terms.>

## Parts

- decisions.md, candidates.md, notes.md <and each split part, one line on what it holds>

## Progress

| Step | Result | Direction | Learned | Peak context (impl/verify/refine/review) |
|---|---|---|---|---|
```

`decisions.md` is `# Decisions` and one line per decision (`- <date> <decision> -> <step
Clarifications, Contract, ADR or research note>`). `candidates.md` is `# Candidate steps`:
ideas from the design input, retros or observations, not a plan; `/next-step` picks one at a
time and removes what a step has done. `notes.md` has `## Agent notes` (the architect's hotwash
and trace line from `/goal` and `/close-goal`) and `## Retrospective` (written by
`/close-goal`).

## steps/<NN>-<slug>/step.md

```markdown
# Step <NN>: <title>

- Goal: [<goal title>](../../goal.md)
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

## Neighbours

<Not part of the contract. From the architect: each neighbour (profile `## Neighbourhood`) of
what the contract changes, *changes* or *stays*, with one line why.>

## Test seams

<Not part of the contract; accepted by default. The highest seams to test at, ideally one,
each with what it catches and what it misses.>

## Code map

<Not part of the contract. From the architect: files and symbols that change, helpers to
reuse, test files to copy the pattern from, commands for data and counts.>

## Clarifications

<Questions raised by phase agents and the user's answers, with dates.>

## Agents

<One line per agent of the step, written by the orchestrator: `developer: <id>`,
`reviewer spec: <id>`. Later rounds resume these (`orchestrating.md`, "One agent per role").>

## Hotwash

## Retro
```

The phase files start with `# <Phase>: step <NN>` and hold what that role's **Done when**
names, ending with its trace line; later rounds add `## Later round <n>`. `review.md` has one
`## Round <n>` per review round.

## fixes/<YYYY-MM-DD>-<slug>.md

A fix is small enough for one file.

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

## Agents

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

The step folder given, or else the highest-numbered step whose `step.md` has the phase's
status in the given goal, or in the only goal with `Status: Active`. Several active goals: ask
which one.
