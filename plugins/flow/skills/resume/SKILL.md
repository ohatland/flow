---
name: resume
description: Take over flow orchestration from a handoff written by /flow:handoff, after /clear, reading only what the handoff points to.
argument-hint: "[goal-slug | handoff path]"
disable-model-invocation: true
---

Take over the orchestration from a handoff: $ARGUMENTS

You are the orchestrator now; follow `${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md` (read
it, `state.md` next to it and `.flow/project.md`).

1. Read the handoff: the path given, `<state>/goals/<goal>/handoff.md` for the goal given
   (or the only `Status: Active` goal), else `<state>/goals/handoff.md`. If none exists, say
   so and stop.
2. Check it against reality: current directory and branch match the goal's Worktree and
   Branch, `git log --oneline -5`, `git status --short`, the app's health check. Point out
   differences.
3. Read only the files under **Read first**, as far as the focus needs.
4. A phase that was in progress restarts from the step file with a fresh agent.
5. Reply in a few lines: where we are, open threads and missing approvals, the next
   command. Ask the user to confirm before starting. Delete the handoff file once the user
   confirms.
