# Flow profile: <repo name>

<!-- What the flow needs to know about this repo. See shared/profile.md in the flow plugin.
     Keep it short: repo knowledge belongs in CLAUDE.md, skills and docs, linked from
     Knowledge. Headings must stay as they are; the text may be in any language. -->

## Project

<What the repo is, the stack in one or two lines.> Files the flow writes (goal and step
files, tests, commit messages) are in <language>.

## Contract

The user approves these in every step; everything else is the agents' to decide.

### <Category, e.g. Data model>

<What it covers.>

### <Category, e.g. Public API>

<What it covers.>

### Dependencies

New packages or tools, and why.

## Stop and ask

- <Expensive, irreversible or shared actions that need the user's go-ahead.>

## Knowledge

- all: <the repo's overview (what each part is for), and skills or docs every role needs beyond CLAUDE.md>
- architect: <...>
- developer: <...>
- tester: <...>
- refiner: <...>
- reviewer: <...>

## Gate

`.flow/check <base> [--all-tests] [--no-tests]` from the repo root. Checks: <list>.

<Optional: Before each commit, `<command>` runs and its output is shown with the diff.>

## Running the app

<Where it is documented, the health check, how to stop it. Or: None, the gate's tests are
the only check.>

## Review axes

### <axis, e.g. security>

<What to check, and the standards sources.>

## Neighbourhood

<What a module and its neighbours are here, and which areas belong to other owners.>

## Git

- Branch: <work on main | one feature branch per goal; protected branches>
- Worktrees: <none | the command>
- Commit messages: <style>
- Never committed: <paths>

## Records

- ADRs: <folder, or none>
- Glossary: <file, or none>
- Retro: every 3 steps
- State: `.agent-work/` (gitignored)
