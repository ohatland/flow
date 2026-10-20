# flow

A Claude Code plugin for an orchestrator-style workflow in any repo: one session talks to
you and dispatches role agents in their own context windows, work is done in small steps
whose contract you approve, and a retro every few steps improves the setup.

The plugin knows the **process**. Each repo describes **itself** in a small profile,
`.flow/`, and keeps its knowledge (conventions, testing, how to run it) in `CLAUDE.md`,
skills and docs that are useful without the flow too.

Grown out of the AdmMit-AI-Flow plugin and
[ai-workflow-dotnet](https://github.com/ohatland/ai-workflow-dotnet), without their stack.

## The loop

```text
/flow:init        once per repo: survey it and write .flow/ with you
/flow:goal        current state, target state, success criteria (architect)
/flow:next-step   one small step, contract + acceptance criteria approved by you
  implement -> verify -> refine -> final-review   (chained; retro when due)
/flow:close-goal  whole-goal check, docs and glossary sweep, goal retro
/flow:fix         lighter loop for a bug outside a goal
/flow:handoff, /clear, /flow:resume            between steps
```

| Agent | Role |
|---|---|
| `flow:architect` | survey, step proposal with contract draft and test seams, goal review, ADRs after approval |
| `flow:developer` | working code first, test-first; never commits |
| `flow:tester` | the running app or real output, against the acceptance criteria; changes only tests |
| `flow:refiner` | internal quality without behavior change, ring-scoped around the diff |
| `flow:reviewer` | read-only, one axis per instance: `spec`, `slop`, the profile's axes, `fix`, `goal` |

A step has one agent per role, and one reviewer per axis. Later rounds resume the same agent
with `SendMessage`; a new one starts only after `/clear` or above about 150k context.

Knowledge skills shipped with the plugin: `flow:codebase-design`, `flow:testing`.

## Where things belong

1. True in any repo -> the plugin (agents, skills, `shared/`).
2. True in this repo without the flow -> repo knowledge (`CLAUDE.md`, topic skills, docs),
   organised by topic, not by role.
3. The flow's question with this repo's answer -> the profile (`.flow/project.md`,
   `.flow/check`).

`plugins/flow/shared/profile.md` defines the profile's sections; `/flow:init` writes one
from `plugins/flow/templates/`.

## Install

The repo is private. Clone it and add the clone as a marketplace, so edits apply without a
push and the retro can commit approved changes here:

```bash
git clone git@github.com:ohatland/flow.git ~/git/flow
claude plugin marketplace add ~/git/flow
cd <repo> && claude plugin install flow@hatland --scope project
```

Install per project (`--scope project` or `--scope local`), never for the user: another
plugin named `flow` may be active elsewhere. Claude Code runs an installed copy of the plugin
that changes only with `version` in `plugin.json`: after editing agents or skills, raise the
version, run `claude plugin update flow@hatland` for new sessions and `/reload-plugins` in
open ones.

The helper scripts (`shared/trace.py`, `shared/sections.sh`) and the repo's `.flow/check`
ask for permission on first use; allow them by path in the repo's `.claude/settings.json`.

## Hotwash and trace

Every agent, and the orchestrator at the end of a step, writes a **hotwash** (intent,
deviations, unsure, sustain, improve) before its context is gone. `shared/trace.py
<agent-id>` records what the agent actually did from its transcript. Reviewers review blind
first, then compare with the hotwashes; the retro triangulates hotwash, trace and outcomes.

Several rules are adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
(MIT): grilling, retro, diagnosing bugs, code review, test seams, codebase design.

## Known limits

- Plugin agents ignore `hooks`, `mcpServers` and `permissionMode` frontmatter; subagents
  inherit the session's permission mode and load `CLAUDE.md`.
- Agents cannot be resumed after `/clear`; a phase restarts from the step file.
