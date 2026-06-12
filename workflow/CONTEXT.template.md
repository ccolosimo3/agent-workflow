# CONTEXT.md - Local Repo Context (template)

Template for a repo's local, git-excluded `CONTEXT.md`: ONE doc owning both
domain language and repo orientation (the merged shape adopted 2026-06). Copy
to the repo root, fill the placeholders, exclude it via `.git/info/exclude`.

Every copy keeps a header block with:

- `Last domain pass: YYYY-MM-DD`
- a local-only notice and authority disclaimer (tracked repo docs and current
  human instructions win on conflict)
- "use as an orientation map, not a substitute for reading the relevant code"

## Start Here

`<3-6 bullets: read-first files, command style, package manager, linter, and
any data-safety rules an agent must never violate>`

## Mental Model

`<5-8 bullets: what the product is, the major systems, and what each is for —
written so a fresh agent knows where things live before reading code>`

## System Map

`<optional mermaid flowchart or table of runtime systems and their
relationships>`

## Repo Map

`<top-level directories → what each owns>`

## Domain Language

Canonical glossary for product, device, workflow, and business terms. Use it
when naming concepts, writing issue titles, drafting acceptance criteria, and
reviewing user-facing copy. Keep entries focused on domain meaning — no
generic implementation nouns (component, helper, repository, route, hook)
unless they carry special product meaning. Update inline when a Domain Pass
resolves terminology.

| Term | Definition |
| --- | --- |
| `<Term>` | `<User-meaningful definition. Include boundaries: what it is and what it is not.>` |

Relationships:

```text
<Term A> -> <Term B> -> <Term C>
```

## Sources Of Truth

`<which system owns which data; where "correct" is defined per surface>`

## Things Not To Confuse

`<pairs of look-alike concepts/systems, one-line distinction each>`

## Per-Surface Patterns

`<one section per major surface (frontend app, backend service, shared
packages): the established patterns, workflows, and conventions an agent
should reuse instead of inventing>`

## Verification

Pointer only — the repo's verification reference doc owns surface→command
routing. Keep at most 2-3 load-bearing one-liners here (e.g. a clean-baseline
trap), never a command matrix.

## ADR-Like Decisions To Know

`<hard-to-reverse decisions with rationale, or pointers to real ADR files>`

## Sharp Edges

`<the traps that bite agents: stale-doc hazards, lint/review exclusions,
destructive command lookalikes, version gotchas>`

## Flagged Ambiguities

- **`<Ambiguous term>`**: `<why it is ambiguous, preferred wording, and the
  open decision if any>`.

## Decision Locks

Short-lived terminology decisions that must stay stable during an active
task/spec. Move lasting architecture decisions to ADRs or team decision docs.

- `<Decision>`: `<rationale and revisit trigger>`.

## Good Places To Read First

`<ordered reading path for a fresh agent or human>`
