# The project profile

The plugin knows the process; the repo knows itself. Everything the process needs to know
about a repo is in its **profile**, `.flow/` at the repository root:

```text
.flow/
  project.md    the answers to the questions below, one `##` section each
  check         the gate, an executable (see "Gate")
```

`.flow/` may be committed, or a symlink excluded with `.git/info/exclude` when the repo is
not yours to change. Start a new profile with `/flow:init`.

## Where things belong

Three layers, sorted with two questions:

1. **Would it be true in any other repo?** Then it is process and lives in this plugin
   (agents, skills, `shared/`).
2. **Would it be true in this repo without the flow** (an ordinary session, a human
   developer)? Then it is repo knowledge: `CLAUDE.md` for what every session needs, topic
   skills or docs for the rest (conventions, testing, running the app, the domain).
3. Otherwise it is the flow's question with this repo's answer, and lives in the profile.

Repo knowledge is organised by topic, not by role: the same conventions serve the developer,
the refiner and the reviewer. A profile that grows long is holding repo knowledge.

## Sections of `project.md`

Agents load the sections they need with
`<shared>/sections.sh .flow/project.md "<heading>"...` (prefix match on the heading text).
Headings are exactly these; the text under them may be in any language. A section that
does not apply says so in one line.

### `## Project`

What the repo is and does, the stack in one or two lines, and the language for files the
flow writes (goal and step files, tests, commit messages). The user is always answered in
their own language.

### `## Contract`

The categories the user approves in every step, one `###` per category with a line on what
it covers. They become the `### ` sections of a step's `## Contract`. Typical: data model,
public API, user-facing behavior, dependencies. Everything outside the contract is the
agents' to decide.

### `## Stop and ask`

Actions that need the user's go-ahead in this repo beyond `protocol.md`: expensive,
irreversible or shared things (a long build, a migration against a shared database,
downloads, publishing, changing approved tests).

### `## Knowledge`

What each role loads before working: repo skills (by name, loaded with the Skill tool),
docs (paths) or `sections.sh` commands into existing files. One line per role
(`architect`, `developer`, `tester`, `refiner`, `reviewer`) plus `all` for what every role
needs beyond `CLAUDE.md`.

### `## Gate`

The command, its options and what it checks. Contract: run from the repo root as
`.flow/check <base> [--all-tests] [--no-tests]` plus any options described here; prints one
`===== <name> =====` section per check and ends with a `SUMMARY` block of
`PASS|FAIL|FLAG  <text>` lines; exit 0, 1 on any FAIL, 2 on usage errors. FAIL blocks the
step; FLAG is fixed or explained. An optional line `direction: BETTER|NEUTRAL|WORSE|MIXED`
is recorded in the goal's progress.

### `## Running the app`

How the tester sees the change working: where that is documented (a skill or doc), the
health check, whether one instance is shared, how to stop it. `None` when the gate's tests
are the only check.

### `## Review axes`

Axes beyond `spec` and `slop`, which every review has. One `###` per axis: what it checks
and its standards sources. For example `security`, `accessibility`, `cartography`. An axis
may end with `Applies when:` and the paths whose change calls for it; without that line it
runs in every review.

### `## Neighbourhood`

What a module and its neighbours are here, for the refiner's ring 2 (sibling files in the
same folder, a feature slice, a pipeline stage) and which areas count as another owner's.

### `## Git`

Branch policy (work on `main`, or one feature branch per goal), worktrees (the command, or
none), commit message style, protected branches, paths never committed.

### `## Records`

Where decisions and vocabulary live: the ADR folder (or none), the glossary (or none), and
the state folder (default `.agent-work/`, which must be gitignored).
