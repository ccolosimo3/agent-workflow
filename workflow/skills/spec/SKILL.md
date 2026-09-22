---
name: spec
description: Turn an operator-selected work item into one grounded, right-sized, implementation-ready Task with behavioral acceptance and risk-selected verification. Use for a formal spec; not for casual planning, architectural option comparison, or implementation.
metadata:
  opencode/autoinvoke: true
---

# Spec

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`, and
`../../references/PLANNING.md` completely. Stop if any cannot be resolved. Then
read the repository instructions and adapter relevant to the work item.

## Specify the next Task

Confirm the operator selected a formal spec. Re-ground the raw outcome against
current source, owners, nearest complete patterns, and relevant landed work.
Treat prior plans and summaries as claims. Resolve ordinary mechanical ambiguity
through repository evidence. Apply `PLANNING.md`'s grounding and scope rule to
consequential before/after behavior; keep unsettled operator choices visible in
the draft and return them before review-ready promotion or dependent work.

Define one independently valid Task. Use these as compact contents, not mandatory
headings:

- goal, non-goals, current behavior, settled decisions, and source evidence
  (file:line for load-bearing repository claims);
- chosen approach, rejected alternatives and tradeoffs, design risks, unresolved
  choices, and the minimum-sufficient shape with implementation latitude;
- ordered steps, affected owners/files, dependencies, valid intermediate state,
  and behavioral acceptance including meaningful failures;
- verification under `TESTING.md`: reuse, first falsifier at the real operation,
  exact selected checks, and remaining operator/platform proof and owner;
- approval-gated actions, documentation impact, review/implementation state,
  and a tracker-ready summary only when applicable.

When an established repository pattern or previously settled decision determines
the approach, cite that basis instead of manufacturing alternatives. Explain
credible alternatives and tradeoffs for consequential choices that remain open.

Read `../../references/TESTING.md` while drawing up verification. For UI scope,
also read `../../references/FRONTEND.md` and include the UI strategy. Run a domain
pass only for a changed core noun, lifecycle meaning, user terminology, service
boundary, or cross-system contract; record canonical terms and real choices
without manufacturing an architecture record for ordinary work. Apply
`PLANNING.md`'s review-readiness bar before promotion.

Work serially by default. A bounded evidence helper may answer a distinct factual
question under `WORKFLOW.md`; it does not author a second spec or certify this
one.

Write the living spec at the repository's declared plan location. Drafting alone
does not authorize implementation, tracker mutation, or promotion.

Before review, resolve `review-spec`. If unavailable, report “review phase not
implemented” without promotion or kickoff. Otherwise invoke it;
`review-spec` owns authority resolution, payload construction, and review
loops.
After required approval, continue into `implement` in this task when execution
is already authorized; otherwise return the spec and its remaining decision.
