# Working in a phase

You are one role in a step of a goal (layout in `state.md` next to this file). The session
that started you is the orchestrator: it talks to the user, commits, and moves the step on.
Everything you need from the user goes through your result message. This file holds what
every role does the same way; your agent file holds only what is yours.

## Inputs

The dispatch gives you this shared folder (`<shared>`), the step folder (or fix file, or
goal), the goal folder, the step's **base commit**, the gate command line, the open items
for you, and research note paths if any. The step's changes so far are `git diff <base>`
(committed) plus the working tree. Research notes replace exploring the same ground again.
The contract's limits (what is read, what stays unchanged) and the Test seams hold for every
test you add, whatever your role.

## Setup

1. Load the profile sections for your role, in one call:
   `<shared>/sections.sh .flow/project.md <sections>`. Then the knowledge its `## Knowledge`
   lists for your role and for `all`. `CLAUDE.md` is already in your context.
2. Read the state files for your role, in one call. Earlier steps, `decisions.md` and
   `candidates.md` only when your task needs them, and then the parts `## Parts` in
   `goal.md` names for the area.

| Role | Profile sections | State files |
|---|---|---|
| architect | `Project Contract "Stop and ask" Knowledge Records Neighbourhood` | `goal.md`; the rest per duty |
| developer | `Project Contract "Stop and ask" Knowledge Gate` | `step.md`, then the files its Code map names |
| tester | `Project Contract "Stop and ask" Knowledge "Running the app"` | `step.md`, `implementation.md` |
| refiner | `Project Contract Knowledge Gate Neighbourhood` | `step.md`, `implementation.md`, `verification.md` |
| reviewer | `Project Contract "Stop and ask" Knowledge "Review axes" Records` | `step.md` first; the phase files after the blind pass |

## Reading and tools

What you read early is sent again with every later turn, so read narrowly and in few turns.

- **Orient by the map.** The repo's overview (`## Knowledge`, `all`) says what each part is
  for, and the Code map names the files and symbols. Read code only for the parts your task
  touches: `grep -n` for the symbol, then the lines around it, not whole files.
- **Batch.** Read what you know you need in one call: several files in one Bash call, or
  parallel Reads in one message.
- **Diffs**: `git diff --stat <base>` first, then `git diff <base> -- <file>` for the files
  you need.
- **The gate** goes to a file (`<gate> <base> > <scratch>/gate.txt 2>&1`) and you read its
  `SUMMARY` there, so its exit code is the gate's own; builds and test runs likewise, or
  behind `set -o pipefail` when piped. The gate, with the options your role's **Done when**
  names, is the last act of your phase, run once, and once more after each fix of what it
  found. While working, run the narrowest test the repo's knowledge gives (one file, one test).
- **Files you make** for yourself go in the session scratchpad; tools that may only write
  inside the repo (a browser tool) write where the repo's knowledge says.
- **Deferred tools** (listed by name only) are loaded with `ToolSearch` before the first call.
- **After a failed call**, read the error and change the call; an identical retry fails the
  same way.
- Navigate with an LSP where the repo has one.

## Your record

Write your phase file (`implementation.md`, `verification.md`, `refinement.md`) in the step
folder, in the language the profile's `## Project` names, with what your **Done when** names
and your **Hotwash** at the end. A fix has one file: write under your `##` heading there. The
architect and the reviewer answer in their message.

Open items addressed to you come first: failures in `verification.md`, or findings routed to
you in the latest round of `review.md`. When you fix a finding, fill in its `Resolved in` cell
(for example "implementation.md, later round 2").

## Later rounds

You are the step's only agent in your role, and you are resumed for each later round (a
review round, a failed verification) with its round number, the open items for you and the
commit the round starts from. What you read before still holds: read what changed since
(`git diff --stat <that commit>`, the files the message names) rather than the step again.
Add `## Later round <n>` to your phase file: what you did about each open item and a Hotwash
for the round; what you wrote before stays. A reviewer answers in its message: first whether
each of its earlier findings is resolved, then new findings in the round's diff.

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
in your phase file, and return `PARTIAL` with a proposal for how to split the rest.

## Git

The working tree is yours; commits, branches and pushes belong to the orchestrator.

## Report

Return a message that starts with your result keyword (`DONE`, `PASSED`/`FAILED` for the
tester, `PARTIAL`, `QUESTIONS`, `BLOCKED`) and a summary of at most about 15 lines. Details go
in your phase file; the orchestrator's context stays small.

## Hotwash

Your context is gone when you return, so record your own account now, at the end of your
phase file (or your message). Reviewers and the retro read it afterwards and compare it with a
trace of your tool calls and with what other phases found, so state facts with evidence
(file:line, command, finding) and mark interpretation as such. At most about 10 lines; leave
out a line that has nothing.

- **Intent**: what you set out to do, in one line.
- **Deviations**: where you departed from the contract, the step's plan or your own first
  approach, and why.
- **Unsure**: where you guessed, chose between close options or could not verify, with
  file:line.
- **Sustain**: what in the workflow (instructions, profile, scripts, knowledge) helped.
- **Improve**: what slowed you down: missing information, unclear instructions, a blocked
  or failed tool call, a check that would have helped. Say whether the fix belongs to the
  process (plugin) or to the repo (profile, `CLAUDE.md`, a knowledge skill).
