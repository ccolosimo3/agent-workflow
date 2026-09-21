---
name: implement
description: Implement one operator-selected work item in its minimum-sufficient repository-conventional shape, verify it proportionally, and drive inner and selected outer review to completion. Use for own-work execution; not for planning or coworker PR review.
metadata:
  opencode/autoinvoke: true
---

# Implement

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, and `../../references/TESTING.md` completely.
Load `../../references/FRONTEND.md` for UI scope; load `../../references/REVIEW.md`
for the lifecycle method below or at review handoff. Stop if an applicable
authority cannot be resolved, then read the repository's instruction chain and
adapter. Reuse unchanged authority reads only as permitted by the kernel.

## Entry and preflight

Confirm implementation is selected directly or by an existing end-to-end grant.
Continue here by default under `WORKFLOW.md`; a phase change requires no new task.

- **Fast:** require every Fast condition in `WORKFLOW.md`, a clear raw ask,
  behavioral acceptance, and one focused falsifier. Do not manufacture a spec.
- **Standard/Assured:** require the named spec to be inner-converged and any
  selected outer-spec gate to be complete. Treat status summaries as claims.

Confirm repository root, checkout/worktree owner, branch and integration base,
`git status`, acceptance and non-goals, current source claims, nearest owners and
complete patterns, approval state, and repository verification routes. Preserve
all unowned changes. Stop rather than guessing when the selected Task, checkout,
or required approval is ambiguous. Retain any named coordinating lead's return
identity, available evidence, and
remaining operator proof. These are current facts, not a new handoff artifact.

## Implement the Task

Apply `KERNEL.md`'s minimum-sufficient check before investing in a material
mechanism. Reuse existing owners and add only behavior unique to the Task.
Implement the smallest complete shape that satisfies acceptance, failures, and
safety; do not add speculative recovery, compatibility, configuration, state, or
abstractions.

### Conditional methods

These methods apply only within an already-selected implementation. They do not
select a phase, expand scope, or require an additional label, artifact, or
receipt.

- **Diagnosis-heavy bug:** When the affected boundary is practical, observe the
  reported symptom there before editing, narrow plausible causes, confirm the
  selected mechanism with repository or runtime evidence, then apply the smallest
  fix and repeat the same observation. Do not start with speculative fallback or
  guard code. If exact reproduction remains unavailable after the narrowest
  reasonable attempt, state why and use the strongest safe proxy plus the exact
  remaining real-boundary proof instead of stalling or inventing weak automation.
- **Repeated corrective layers:** Apply `WORKFLOW.md`'s shared-assumption diagnosis
  before another workaround, expanded harness, or broad rerun. Use the smallest
  discriminating observation at the affected owner; record the conclusion and
  remaining uncertainty in the existing work item.
- **Explicitly authorized behavior-preserving refactor:** Establish the current
  observable contract at the real boundary before structural edits, keep the same
  proof green through small steps, and separate any behavior change discovered.
  For an explicitly authorized internal API convergence where compatibility is
  not required, define the target caller shape, migrate affected callers in
  verifiable steps, and remove the obsolete path; never infer this permission for
  public or independently versioned consumers. Use subtraction when it objectively
  removes obsolete layers, state, or call paths, but observable parity—not a
  subjective reader-load claim—remains the proof.
- **Repetitive mechanical change or sweep:** Establish one representative
  transformation and its real-boundary proof before scaling it. Use the smallest
  deterministic automation only when it is safer or more repeatable than the
  remaining manual edits; confirm it reproduces the proven transformation before
  applying it further, and batch only when that improves proof or fault isolation.
  Remove task-local tooling unless a continuing consumer earns it, and never let
  it own product behavior.
- **Explicit performance outcome:** Capture the baseline at the real boundary,
  change the measured dominant cost, then compare the same workload and check that
  material cost was not merely displaced.
- **Migration or lifecycle:** Identify the invariant and applicable supported
  transitions before editing; read `REVIEW.md` and apply its closed-loop lifecycle
  audit and `TESTING.md`'s persistence/schema bar during implementation, not only after
  handoff. Trace repeat delivery, partial failure, retry or late completion,
  cleanup, and convergence only where changed state or side effects make them
  applicable; prove the material transitions at the real operation boundary.

A simpler repository-conventional mechanism may replace a planned mechanism when
observable behavior and approved contracts remain intact. Return to planning only
when a correction changes behavior, scope, authority, safety, or the Task's risk
boundary. Record adjacent work as a reconciliation fact rather than absorbing it.

Update the existing owning documentation when behavior, contracts, setup,
architecture, verification, or user/operator workflow changes. For UI work,
apply `FRONTEND.md` proportionally and remove temporary fixtures or tooling.

## Verify and review

Use the repository's routes and `TESTING.md`, starting with the earliest safe
falsifier of a load-bearing assumption. Run affected required checks before review
and bind results to the candidate. Reuse causally valid evidence; a broad rerun
needs changed shared infrastructure or insufficient constituent proof. Keep
one-off proofs out of the permanent suite and unavailable checks explicit.

Before review, apply `TESTING.md`'s durable-proof and inclusion decisions to the
changed tests; resolve clear weak, redundant, or oversized proof within its
authority rules instead of leaving the first triage to the reviewer. Repeat the
minimum-sufficient check, remove unearned machinery and temporary residue, inspect
the full diff, and decide documentation impact. Update
this work item's own artifact with delivered facts. Follow `WORKFLOW.md`'s shared
state ownership: a lead implementing here updates its own program/index; a
delegated worker returns those reconciliation facts. Commit every
in-scope change as real commit(s) without amend, squash, rewrite, push, or external
mutation, and disclose any preserved unowned working-tree change. Apply
`REVIEW.md`'s documentation-only off-ramp after reading it; otherwise invoke
`review-change`, which owns handoff and the inner/configured outer correction loops.

## Complete

After review approval or a documentation-only off-ramp determination, confirm the
live tip and that no in-scope change remains uncommitted. Do not mutate the
certified tip. If a proof fails, distinguish whether it disproves product
behavior or only its own premise/harness before reporting implementation state.
Report under `KERNEL.md`, retaining `WORKFLOW.md`'s source, candidate, authority,
evidence, and remaining-proof facts in the existing work item/evidence owner or,
when none exists, the completion. Include the relevant environment and causal
basis for reused checks. Delegated returns carry the reconciliation facts their
lead needs.

Use four compact labeled fields for the normal completion, with detail
proportional to the change:

- **Built:** two or three sentences on the resulting behavior and main
  implementation approach, fewer for a trivial change. Include meaningful
  documentation impact; do not substitute a changed-file list for the outcome.
- **Verified:** checks actually run or reused, their results, and material
  limitations or unrun proof. Link detailed evidence instead of dumping commands.
- **Reviews:** for each inner/outer gate in scope, name the reviewer model and
  reasoning effort, completed initial and follow-up passes (for example,
  `1 initial + 2 follow-ups`), and verdict or pending state. Distinguish phases
  when reporting spec and implementation reviews; give a short reason for a
  skipped gate. Pass counts are not counts of independent reviewers.
- **Status:** commit/PR and publication state, plus remaining actions or decisions.

Use available run metadata for reviewer identity; label launch settings when
those are the only source, and unavailable identity or counts as unknown. Never
infer them from configured defaults or count failed launches as completed passes.
Use existing evidence and handoffs; do not collect extra telemetry, rerun checks,
or create a report or receipt dependency to fill these fields. Omit empty detail
and internal ledgers.

When `KERNEL.md`'s receipt trigger applies, including to a terminal partial,
blocked, or abandoned implementation, read `../../references/RECEIPTS.md` and
project the evidence already gathered above into its self-report and any
separately sourced known annotations; do not rerun or recollect evidence. Keep
the normal chat completion even when the durable write is skipped.

Do not include findings or an internal ledger. When the operator asks for a PR,
compose its body from `../../templates/pr-body.md`; pushing, opening/editing the
PR, tracker mutation, or any other external action still requires `KERNEL.md`
approval.
