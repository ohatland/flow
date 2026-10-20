# Working in a phase

You are one phase of a step in `<state>/goals/<goal>/steps/<NN>-<slug>.md` (layout in
`state.md` next to this file). The session that started you is the orchestrator: it talks
to the user, commits, and moves the step on. Everything you need from the user goes
through your result message.

## Inputs

You get the step file path, the `goal.md` path, the step's **base commit**, the gate
command line and this shared folder. The step's changes so far are `git diff <base>`
(committed) plus the working tree. The step file holds the approved Contract, the
acceptance criteria, the Test seams, the Clarifications and the record of earlier phases.
Research notes, when the dispatch names them, replace exploring the same ground again.
The contract's limits (what is read, what stays unchanged) and the Test seams hold for
every test you add, whatever your phase.

Run the gate with its output redirected to a file (`<gate> <base> > <scratch>/gate.txt 2>&1`)
and read its `SUMMARY` there, so its exit code is the gate's own. Builds and test runs go
the same way: to a file, or behind `set -o pipefail` when piped. The gate, with the
options your role's **Done when** names, is the last act of your phase, run once, and once
more after each fix of what it found; while working,
run the narrowest test command the repo's knowledge gives (one file, one test). Write your
part of the step file under your phase's `##` heading, above the next `##` heading.

The repo describes itself in its profile, `.flow/project.md` (`profile.md` next to this
file). Load the sections your role names, and the knowledge its `## Knowledge` section lists
for your role and for `all`. `CLAUDE.md` is already in your context.

Open items addressed to your phase come first: failures under `## Verification`, or
findings routed to you in the latest round under `## Review`. When you fix a finding, fill
in its `Resolved in` cell (for example "Implementation, later round 2").

Navigate with an LSP where the repo has one, Grep and targeted Reads. Read the step file
in sections (`sections.sh <step file> <heading>...` in this folder), the ones your role
names. Read what you already know you need in one call: several files in one Bash call, or
parallel Reads in one message. With a Code map in the step file, the developer writes its
first test within about five turns.

## Later rounds

You are the step's only agent in your role, and you are resumed for each later round (a
review round, a failed verification) with its round number, the open items for you and the
commit the round starts from. What you read before still holds: read what changed since
(`git diff <that commit>`, the step file sections the message names) rather than the step
again. Add to your section under `### Later round <n>`: what you did about each open item and a
Hotwash for the round; what you wrote before stays. A reviewer answers in its message: first
whether each of its earlier findings is resolved, then new findings in the round's diff.

## Stop and ask

Return to the orchestrator, leaving the working tree as it is, when your role's triggers
apply, and always when:

- A change in a contract category (the profile's `## Contract`) would go beyond the
  approved contract.
- A recorded decision (the profile's `## Records`: ADRs) conflicts with the step, or would
  need to change.
- An action is listed under the profile's `## Stop and ask`, or reaches outside the working
  tree (a push, a shared database, a publish).
- Anything else only the user can decide.

Start the message with:

- `QUESTIONS`, then numbered questions, each with the context, the options and your
  recommendation, worded so that "yes" accepts the recommendation; or
- `BLOCKED`, then what stops you and exactly what the user must do (for example start
  a container, or run a command with `! <command>`).

You will be resumed in this same conversation with the answers; continue where you were.
Internal matters (code structure, naming, test design) are yours to decide.

## Keep the step small

When the step turns out much bigger than one focused session, finish the current
increment so the gate's build and tests are green, record what is done and what remains
under your section, and return `PARTIAL` with a proposal for how to split the rest.

## Git

The working tree is yours; commits, branches and pushes belong to the orchestrator.

## Report

Fill in your section of the step file, in the language the profile's `## Project` names,
ending with your **Hotwash** (below). Then return a message that starts with your result
keyword (`DONE`, `PASSED`/`FAILED` for the tester, `PARTIAL`, `QUESTIONS`, `BLOCKED`) and a
summary of at most about 15 lines. Details go in the step file; the orchestrator's context
stays small.

## Hotwash

Your context is gone when you return, so record your own account now, at the end of your
section (agents without a section in the step file put it at the end of their message).
Reviewers and the retro read it afterwards and compare it with a trace of your tool calls
and with what other phases found, so state facts with evidence (file:line, command, finding)
and mark interpretation as such. At most about 10 lines; leave out a line that has nothing.

- **Intent**: what you set out to do, in one line.
- **Deviations**: where you departed from the contract, the step's plan or your own first
  approach, and why.
- **Unsure**: where you guessed, chose between close options or could not verify, with
  file:line.
- **Sustain**: what in the workflow (instructions, profile, scripts, knowledge) helped.
- **Improve**: what slowed you down: missing information, unclear instructions, a blocked
  or failed tool call, a check that would have helped. Say whether the fix belongs to the
  process (plugin) or to the repo (profile, `CLAUDE.md`, a knowledge skill).
