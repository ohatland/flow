---
name: retro
description: Retrospective on how the flow workflow is working - turn friction from hotwashes, traces, step files and the process log into improvements to the plugin, the repo's profile or its knowledge, approved by the user one by one. Runs after every step, at close-goal, or on demand.
argument-hint: "[step-file | goal-slug | since-date]"
---

Run a retrospective: $ARGUMENTS

You improve the **workflow**, not the product code. Follow
`${CLAUDE_PLUGIN_ROOT}/shared/orchestrating.md`.

## 1. Scope and sources

- **After a step**: that step file, plus open entries in `<state>/goals/process-log.md`.
- **After a goal**: all the goal's step files and the open log entries.
- **On demand**: everything since the newest line under `## Retros` in the process log.

Three kinds of evidence, read together:

- **Self-report**: each phase agent's **Hotwash**, the reviewers' Hotwash checks, and the
  orchestrator's `## Hotwash`.
- **Observed**: the trace line per agent, and the trace files under `traces/` for the
  phases that show friction (errors, blocked calls, failed gate runs, repeated calls,
  files read many times, high peak context).
- **Outcomes**: Clarifications, Verification failures, Review rounds, Observations, and
  the gate's direction lines.

Triangulate. A hotwash claim that a trace or a finding contradicts is a finding in itself
(an agent sure about code a reviewer found wrong, or reporting no friction where its trace
shows blocked calls). Trace friction no hotwash mentions is a finding too. Read session
transcripts (`~/.claude/projects/<cwd with / replaced by ->/*.jsonl`) only when these
disagree in a way the trace files cannot settle, and then through a `general-purpose`
subagent that reports friction only.

Before proposing a check, read what already exists: `.flow/check`, the repo's CI, linters,
hooks. A check that exists but is unwired or silently broken is the finding.

If nothing points to a change, say so, record it, and stop.

## 2. Find candidates

Most severe first, each with evidence:

- **Checks**: a mechanical mistake (fixed pattern, banned API, file rule) gets a
  deterministic check in `.flow/check`, not a written rule.
- **Standards**: a judgement call the reviewer missed or the refiner got wrong goes to the
  repo's knowledge for that topic. The developer carries the most context; keep what it
  loads lean.
- **Planning gaps**: questions the developer stopped for that next-step should have
  settled -> architect / next-step, or the profile's `## Contract`.
- **Phase friction**: a phase that asked too much or too little of the user, looped, or
  repeated another phase's work.
- **Context size**: phases above about 200k tokens: what they read that they did not need,
  and whether the step should have been sliced smaller.
- **Tool economy**: expensive or repeated tool calls a script or narrower command would
  replace.
- **Information access**: something agents searched for long or lacked (ports, commands,
  test data) -> the repo's knowledge.
- **Calibration**: where agents' Unsure and Deviations lines and the findings disagree,
  which instruction or standard would have made the agent flag it or get it right.
- **No-ops and size**: instructions that change nothing (the model does it anyway) and
  files that keep growing; propose deletions as readily as additions. Sustain lines name
  what to keep.

## 3. Place each change

Sort every candidate with the questions in `${CLAUDE_PLUGIN_ROOT}/shared/profile.md`
("Where things belong"):

- **Plugin** (true in any repo): agents, skills, `shared/`.
- **Repo knowledge** (true here without the flow): `CLAUDE.md`, a knowledge skill, docs.
- **Profile** (the flow's question, this repo's answer): `.flow/project.md`, `.flow/check`.

A plugin change that only one repo needs is a profile change.

## 4. Propose

Number the proposals; for each: **Evidence**, **Where** (plugin, repo knowledge or profile,
with the exact file), **Change**, **Advantages** and **Disadvantages** (context, speed,
prompts). The user approves, adjusts or rejects each; apply only what is approved.

Write proposed wording for agents: state the wanted behavior positively (naming a
forbidden behavior pulls it into context), give a checkable completion criterion, keep each
rule in one place, and inline only what every branch needs.

Product code issues from Observations are candidate steps for `goal.md`, listed separately.

## 5. Apply and record

- **Plugin** changes: in the plugin's source clone (`~/git/flow` by default; without a
  clone, list the changes for the user), committed there (`retro: ...`); tell the user to
  run `/reload-plugins`.
- **Repo knowledge and profile** changes: in this repo, committed separately from product
  code, in the profile's commit style.

Record: each proposal and its outcome in the step or fix file's `## Retro` (for a
goal-scope retro, in `goal.md` under `## Retrospective`), candidate steps under
`## Candidate steps` in `goal.md`, and in `<state>/goals/process-log.md` remove handled
entries and add a dated line under `## Retros` with the scope and what changed.
