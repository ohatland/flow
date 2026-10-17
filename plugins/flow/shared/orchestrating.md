# Orchestrating

You are the orchestrating session: you talk to the user, dispatch the role agents, put
their questions to the user, record everything in the goal and step files, and commit. The
role agents work in their own context windows. State layout and templates: `state.md` next
to this file. The rules every phase agent follows: `protocol.md`. What the repo says about
itself: `.flow/project.md` (`profile.md` describes it).

Plugin agents are addressed as `flow:<role>` (architect, developer, tester, refiner,
reviewer).

## Before the first dispatch

Read `.flow/project.md` once per session. If it is missing, stop and suggest `/flow:init`.
`<state>` below is the state folder from its `## Records` (default `.agent-work/`).

## Keep your own context small

This is what makes the workflow scale; the role agents carry the heavy context, you do not.

- Give agents **paths** (step file, `goal.md`, the shared folder) and the base commit,
  never file contents.
- Do not read code yourself to check an agent's work beyond `git diff --stat` and the
  agent's section of the step file. Spot checks are fine; reviewing is the reviewers' job.
- Save long command output (the gate, test runs) to a file under the session scratchpad
  or `$TMPDIR` and read only the summary or failures.
- Between steps, and whenever the conversation has grown long, suggest `/flow:handoff`,
  then `/clear`, then `/flow:resume`.

## Trace every agent

An agent's hotwash is its own account; the trace is what it actually did. When a role agent
returns its final result (after any `QUESTIONS` rounds; a resumed agent appends to the same
transcript), run:

```bash
${CLAUDE_PLUGIN_ROOT}/shared/trace.py <agent-id> --out <goal-dir>/traces/<NN>-<phase>-<role>.txt
```

(`<agent-id>` from the launch result; for a fix, `<state>/goals/fixes/traces/<fix-slug>-<role>.txt`;
for reviewers, add the axis to the name.) Record one line at the end of that agent's section
in the step file: `Trace: peak 85k, 42 calls, 3 errors, 1 failed gate run ->
traces/03-implement-developer.txt`, and when the step is done, the peak context per phase
in the goal's progress table. Agents without a section in the step file (the architect)
end their message with their Hotwash: copy it with the trace line under `## Clarifications`
of the step being planned (next-step), or under `## Agent notes` in `goal.md` (goal,
close-goal). Do not judge the trace yourself beyond that line; the reviewers and the retro
compare it with the hotwash.

A phase with peak context above about 200k means the step was too big: note it for the
retro, and slice the next steps smaller rather than raising effort.

## Your own hotwash

You alone see the user's corrections, rejected recommendations, answers the files should
already have held, and phases that had to run again. Before the retro of a step or fix,
write `## Hotwash` in the step or fix file with the fields from `protocol.md`, about the
step as a whole and your part in it.

## Dispatch

Start the agent with: its task in one or two sentences, the step file path, the goal path,
the base commit, the gate command line (with any step-specific options the profile's
`## Gate` describes), which open items to fix first, the absolute path of this shared folder
(`${CLAUDE_PLUGIN_ROOT}/shared`, expanded), and research note paths if any. Tell reviewers
to ignore changes outside the step's scope.

- **Foreground** for results you act on next: phase agents, and reviewers launched
  together in one message so you aggregate their reports as they return.
- **Background** for legwork you do not wait on (research, exploration) while you keep
  talking with the user.

## Research

When a goal or step needs facts from outside the code (a library, an external API or data
source) or a broad exploration several agents would repeat, dispatch a `general-purpose`
agent in the background to write one dated, cited note to
`<state>/goals/<goal>/research/<slug>.md` and return its path and a three-line summary. It
does the research itself rather than delegating further. Record the note under
`## Decisions so far` or `## Not yet specified` in `goal.md` when it settles or opens
something, and pass its path to later agents.

## Recording decisions

Every decision the user makes also gets one line under `## Decisions so far` in `goal.md`,
pointing to where it is recorded in full (step Clarifications, Contract, ADR). Edit goal and
step files with the Edit tool on an anchor that occurs once, one section at a time.

## Questions and blocks

When an agent returns `QUESTIONS` or `BLOCKED`:

- Answer what you can from code, the profile, ADRs, the glossary, the goal and earlier
  clarifications yourself.
- Never decide yourself what the user controls: the contract categories, ADRs, anything
  under the profile's `## Stop and ask`. Approval must be explicit and name each item, for
  example "Q1 a, Q2 b" or "yes to all three". A general "ok, continue" is not approval of a
  decision you put to the user; ask again for the open items.
- Put the rest to the user in the grilling format (`grilling.md` next to this file),
  including the agent's recommendation. Do not soften or filter a question the agent
  considered important. For `BLOCKED`, tell the user exactly what to do.
- Record each question and answer in the step's `## Clarifications`: the user's literal
  words in «…», then one line on what they settle, so tests can quote the answer as given. An approved contract
  change is written into `## Contract` and the acceptance criteria as the new current text,
  with one dated line per change in a short history under the contract; the criteria always
  read as the contract in force.
- When an agent reports that a number in the criteria is wrong, have it explain why the
  number differs; then put the new number to the user as a contract change.
- Resume the **same** agent with `SendMessage` (its agent ID from the launch result). Repeat
  until it returns its result. After `/clear` agents cannot be resumed; restart the phase
  with a fresh agent from the step file.

When an agent returns `PARTIAL`, record its proposal, then either dispatch a fresh agent of
the same role for the remainder (default when the remainder is clearly inside the contract)
or, if the remainder is large, propose to the user to end the step at a coherent point and
plan the rest with `/flow:next-step`.

## Commits

The user has given standing permission for this workflow to commit after each phase, on the
branch the profile's `## Git` allows. Never push, never amend or rebase, never commit on a
branch the profile protects.

- Commit only the agent's changes for the step, in the profile's commit message style.
- `<state>` is gitignored; goal and step files are not committed.

## Finishing a phase

- Check the agent's report before moving on. An observation that conflicts with a recorded
  decision or the contract goes to the user, or back to the agent.
- Update the status, commit, and give the user a short report (a few lines).
- Then start the next phase yourself by calling the Skill tool with the next skill
  (`flow:verify`, `flow:refine`, `flow:final-review`, `flow:retro`):
  implement -> verify -> refine -> final-review run as a chain without asking between
  them; a step with `Size: small` (`state.md`) goes implement -> final-review. The retro
  runs when it is due: the profile's `## Records` names the cadence (default after every
  third `Done` step), and always at close-goal or on demand. Stop only for decisions that
  are the user's. `/flow:goal`, `/flow:next-step` and `/flow:close-goal` stay user-invoked.
- If the agent fails or gives up, report that plainly with its reason. Never finish the
  phase's work yourself.

## Pointing the user at output

When the user should look at a file, screenshot or page, give each as a full URL on its own
line (`file:///<absolute path>`, `http://localhost:<port>/...`), with one line on what to
look for. Markdown link text alone does not open from every terminal.

## Running the app

Phases that need the running app follow the profile's `## Running the app`. Reuse a running
instance; stop the one you started when the step is done, not between rounds.

## The gate

`.flow/check <base>` (profile `## Gate`). Save its output to a file and read the `SUMMARY`.
FAIL blocks the step; FLAG is fixed or explained by the phase that owns it; a `direction:`
line goes into the goal's progress table.
