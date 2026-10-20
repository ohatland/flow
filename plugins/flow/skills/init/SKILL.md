---
name: init
description: Set up the flow in a repo - survey it, sort what exists into repo knowledge and profile, and draft .flow/project.md and .flow/check with the user.
argument-hint: "[notes about the repo]"
disable-model-invocation: true
---

Set up the flow in this repo. Notes: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/shared/profile.md` first: it defines the profile and where
things belong. Templates are in `${CLAUDE_PLUGIN_ROOT}/templates/` (`project.md`, `check`).

1. **Survey.** Dispatch an `Explore` agent to report: the stack, how to build, test, lint
   and run the app, the test layout, existing docs, ADRs, glossary, `CLAUDE.md`, skills,
   hooks and CI, and anything expensive or irreversible (long builds, shared databases,
   downloads, publishing). Facts only, with paths.
2. **Sort.** List what exists and what is missing per layer (repo knowledge vs profile).
   Repo knowledge that the roles will need but that is only in people's heads, in memory or
   spread over long docs, becomes a proposal: a short `CLAUDE.md` addition or a topic skill
   in `.claude/skills/`. Topic, not role: `testing`, `running-the-app`, conventions per
   area, the domain. Without an overview of the repo (`profile.md`, `## Knowledge`), propose
   one from the survey.
3. **Decide with the user**, in the grilling format (`${CLAUDE_PLUGIN_ROOT}/shared/grilling.md`):
   the contract categories, `Stop and ask`, the review axes beyond spec and slop, the git
   policy (work on the main branch or a branch per goal, worktrees), and what the gate must
   check. Recommend from what the survey found.
4. **Write** `.flow/project.md` from the template and `.flow/check` (executable) from the
   template, filled in for this repo; the knowledge skills and `CLAUDE.md` additions the
   user approved; and the state folder (default `.agent-work/`) in `.gitignore`. When the
   repo is not the user's to change, put `.flow/` in a folder outside it, symlink it, and
   exclude the link in `.git/info/exclude`.
5. **Check** that `.flow/check HEAD --no-tests` runs and ends with a `SUMMARY`, and that
   every section the agents load exists:
   `${CLAUDE_PLUGIN_ROOT}/shared/sections.sh .flow/project.md Project Contract "Stop and ask" Knowledge Gate "Running the app" "Review axes" Neighbourhood Git Records >/dev/null`.
6. **Report** what was written, and suggest `/flow:goal` to start. Commit only after the
   user has looked at it.
