---
name: testing
description: Principles for tests worth keeping, in any stack - what a good test is, where tests go (seams), anti-patterns and what to fake. Use when writing or reviewing tests; the repo's own testing knowledge says where its seams and helpers are.
metadata:
  source: Adapted from mattpocock/skills (engineering/tdd), MIT License, Copyright (c) 2026 Matt Pocock
---

# Testing

The repo's own testing knowledge (named in `.flow/project.md` under `## Knowledge`) says
where its seams, helpers and fixtures are. This is what holds everywhere.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can
change entirely; tests shouldn't. A good test reads like a specification ("approved time
entries cannot be edited", "light flares are not drawn below zoom 13"): it says what
capability exists, and survives refactors because it doesn't care about internal structure.

- Tests behavior that users or callers care about.
- Uses the public interface only.
- Describes WHAT, not HOW; one logical assertion per test.
- Expected values come from an independent source of truth: a known literal, a worked
  example, the contract, the user's words.

## Seams: where tests go

A **seam** is the public boundary you test at. Prefer the highest seam that gives fast,
clear feedback: the HTTP API, the CLI, the built artifact, the rendered page. Drop to a
module's interface for rules with many cases where the high seam would be slow or obscure
the rule. Record the seams you chose under Decisions in the step file.

## Anti-patterns

- **Implementation-coupled**: fakes internal collaborators, tests private functions,
  asserts call counts or order, or verifies through a side channel instead of the
  interface. The tell: the test breaks when you refactor but behavior hasn't changed.
  (Checking storage directly is right when storage *is* the behavior.)
- **Tautological**: the assertion recomputes the expected value the way the code does, so it
  passes by construction.
- **Bent to pass**: an expected value changed, an assertion removed or loosened, a test
  skipped or marked as expected to fail, to make a change green. A changed existing test
  needs a reason tied to the contract.
- **Cannot fail**: an assertion that holds for any output (a non-empty list where the
  criterion names specific items, `>= 0` counts).

## What to fake

Fake only at **system boundaries** you do not control: time, external services, identity
providers. Never fake your own modules or internal collaborators, and use the real database
or file format when it is part of the behavior. When code talks to an external service,
inject a specific client per service with one method per operation, so each fake returns
one known shape without conditional logic.
