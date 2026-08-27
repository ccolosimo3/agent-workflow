---
name: technical-writing
description: Write or review substantial engineering documentation that a tired developer can use on the first read. Use for specifications, RFCs, runbooks, READMEs, developer guides, and meaningful PR descriptions; not for ordinary chat, tiny notes, or product UI copy.
metadata:
  opencode/autoinvoke: true
  workflow/kind: expert-guidance
---

# Technical Writing

Make the selected document easier to use without changing its approved scope,
claims, authority, or repository-owned structure. Do not create an additional
document, checklist, or workflow artifact unless the task calls for it.

## Choose the reader's job

Identify the document's dominant mode and optimize for it:

- **Tutorial:** help a learner succeed through visible steps.
- **How-to:** help a competent reader complete a real task.
- **Reference:** make exact facts, options, limits, and errors easy to find.
- **Explanation:** build understanding of a bounded design, decision, or tradeoff.

Small documents may combine modes when the result stays easy to navigate. Split
or link only when mixing learning, procedure, lookup, and rationale makes the
document harder to use.

## Write for one reading

- Use the repository's real symbols, paths, flags, commands, and domain terms.
  Do not invent synonyms for established names.
- Lead with the outcome or governing fact. Put prerequisites, warnings, and
  conditions immediately before the instruction or claim they constrain.
- Write instructions as direct actions. Keep the common path first and put
  exceptions next to the affected step.
- Give each concept one stable name. Replace an ambiguous `it`, `this`, or
  `they` with the noun when a reader could choose more than one referent.
- Prefer short, ordinary words and concrete consequences. Remove throat-clearing,
  duplicated qualifiers, and claims that do not help the reader decide or act.
- Use sentence length and punctuation for clarity rather than enforcing a
  mechanical word limit or house style the repository does not own.

## Keep claims honest

- Separate verified behavior, requirements, decisions, and hypotheses. Match
  confidence to the evidence and keep unresolved facts visibly unresolved.
- Make commands, paths, counts, and compatibility claims true for the revision
  being documented. Include a reproduction or regeneration command when it is
  part of maintaining the claim.
- Preserve meaningful rationale and constraints. Concision is not permission to
  delete why a non-obvious boundary exists.
- Keep reference material descriptive and procedures actionable. Avoid burying
  required steps inside background prose.

Before finishing, read from the target audience's position: can they find the
answer, distinguish fact from judgment, and take the next action without
reinterpreting a sentence?
