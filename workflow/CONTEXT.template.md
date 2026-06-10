# CONTEXT.md - Domain Language

## Purpose

Canonical glossary for product, device, workflow, and business terms. Agents and
contributors should use this file when naming concepts, writing issue titles, drafting
acceptance criteria, and reviewing user-facing copy.

Keep entries focused on domain meaning. Do not add generic implementation nouns like
component, helper, repository, route, or hook unless they have special product meaning.

Update inline during planning when a Domain Pass resolves terminology.

## Language

| Term | Definition |
| --- | --- |
| `<Term>` | `<User-meaningful definition. Include boundaries: what it is and what it is not.>` |

## Relationships

```text
<Term A> -> <Term B> -> <Term C>
```

## Example Usage

- "`<Good phrase>`" means `<specific domain meaning>`.
- Avoid "`<ambiguous phrase>`" when it could mean `<conflicting meaning>`.

## Flagged Ambiguities

- **`<Ambiguous term>`**: `<why it is ambiguous, preferred wording, and open decision if any>`.

## Decision Locks

Use this section only for short-lived terminology decisions that must stay stable during
an active task/spec. Move lasting architecture decisions to ADRs or team decision docs.

- `<Decision>`: `<rationale and revisit trigger>`.
