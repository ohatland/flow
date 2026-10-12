---
name: codebase-design
description: Shared vocabulary and principles for deep modules - interface, seam, depth, leverage, locality. Use when designing or improving a module's interface, judging whether code is a good abstraction or spaghetti, deciding where a seam goes, or when refining or reviewing structure.
metadata:
  source: Adapted from mattpocock/skills (engineering/codebase-design), MIT License, Copyright (c) 2026 Matt Pocock
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean
seam, testable through that interface. The aim is leverage for callers, locality for
maintainers, and testability for everyone.

## Glossary

Use these terms exactly: don't substitute "component," "service," "API," or "boundary."

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic:
a function, a file, a package, a pipeline stage, a tier-spanning slice.

**Interface**: everything a caller must know to use the module correctly: the signature,
but also invariants, ordering constraints, error modes, required configuration, files it
reads and writes, and performance characteristics.

**Implementation**: what's inside a module. Distinct from **Adapter**: a thing can be a small
adapter with a large implementation or a large adapter with a small implementation.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can
exercise per unit of interface they have to learn. **Deep** when a lot of behaviour sits
behind a small interface, **shallow** when the interface is nearly as complex as the
implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that
place; the *location* at which a module's interface lives. Where to put the seam is its own
design decision, distinct from what goes behind it.

**Adapter**: a concrete thing that satisfies an interface at a seam.

**Leverage**: what callers get from depth. One implementation pays back across N call sites
and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge and verification
concentrate in one place. Fix once, fixed everywhere.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be
  composed of small parts internally; they just aren't part of the interface. A module can
  have **internal seams** (used by its own tests) as well as the **external seam** at its
  interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a
  pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want
  to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce
  a seam unless something actually varies across it.

When designing an interface, ask: can I reduce the number of entry points, simplify the
parameters, hide more complexity inside?

## Designing for testability

1. **Accept dependencies, don't create them**: pass in the clock, the client, the paths,
   instead of constructing them inside.
2. **Return results, don't produce side effects**: a function that computes a value is
   easier to test than one that mutates its argument or writes a file as a by-product.
3. **Small surface area**: fewer entry points mean fewer tests; fewer parameters mean
   simpler setup.

## Signs of spaghetti

- Pass-through layers that fail the deletion test.
- The same rule implemented in several places instead of one module.
- Callers that must know ordering constraints or internals to use a module correctly.
- Dependencies that point the wrong way: core logic depending on infrastructure details.
- A change to one behavior that requires edits across many unrelated files.

## Going deeper

- **Deepening a cluster given its dependencies**, see [DEEPENING.md](DEEPENING.md):
  dependency categories, seam discipline, and replace-don't-layer testing.
