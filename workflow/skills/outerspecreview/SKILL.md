---
name: outerspecreview
description: Run the operator-owned outer-gate second review of their OWN plan /
  spec, in a fresh conversation in the other app/model, after the planning
  session's specreview ⇄ specrereview loop has converged to APPROVED. Self-
  populates the Spec Review Kickoff from the spec file (never from a pasted
  prompt), deliberately ignores prior spec-review findings, and performs a
  holistic whole-plan review itself in this conversation per
  ~/.agents/workflow/REVIEW_RUBRIC.md + the Spec Review Kickoff validation
  categories — verifying the spec's file:line claims against current source —
  then returns a strict verdict for the operator to carry back. Use when the
  operator says /outerspecreview, "second spec review", "independent fresh pass
  on the whole spec", or names a converged spec for outer-gate review. Not the
  planning session's own loop (specreview / specrereview), not a code review
  (outerreview), not a coworker PR (prreview).
---

# outerspecreview

The outer gate of the plan flow — the planning analog of `outerreview`. Apply
the shared `~/.agents/workflow/HANDOFF.md` "Outer-gate protocol" for the
mechanics every outer gate shares — conversation-is-the-reviewer / no subagent
(do the review here in the main thread), self-populate from the spec file (never
a paste), the independence seal, the populated kickoff is INTERNAL orientation
you do NOT print, the carry-back return shape, and the strict verdict (no
softening, an early non-converged read never counts). This skill keeps only the
spec specifics below. It exists because the `specreview` loop converges through
`specrereview`, which is delta-scoped — so the converged plan never got a cold,
holistic whole-artifact read. This gate is that read, from a different model,
un-anchored by the loop.

## When invoked

Everything the outer gates share (independence seal, self-populate-never-paste,
kickoff-is-internal, carry-back shape, strict verdict) is in HANDOFF.md
"Outer-gate protocol"; the steps below are only the spec-review specifics.

1. **Preflight (read-only).** Confirm the spec under review (operator pointer, or
   auto-detect the active work-item folder, e.g.
   `<root>/.agent-workflow/plans/active/<ISSUE>-*/`). Confirm it is **converged** —
   the `specreview` loop reached APPROVED and the operator advanced `status` to
   `final` (or `promoted`). Read that from the spec's `status:` frontmatter or the
   operator's word that the loop converged — NOT from `reviews.md` (the shared
   independence seal forbids it); if neither signal is available, ask rather than
   opening `reviews.md`. `review-ready` means the loop has not necessarily run
   yet, so if `status` is `review-ready` or `rough`, say so and treat this as a
   directional early read, not the certifying second verdict. Read-only: no edits
   to the spec, no branch, no tracker mutation.
2. **Locate the artifact.** Read the living spec (`README.md` or the named spec
   file) and the sibling docs it depends on (`*_OPTIONS.md`, `*_SPIKE.md`,
   `verification.md`) — the spec is what you are reviewing.
3. **Populate the `## Spec Review Kickoff` template** from
   `~/.agents/workflow/kickoffs/spec-review.md` as INTERNAL orientation per the
   shared protocol — filled from the spec itself, not session memory; do NOT
   print it back.
4. **Perform the review yourself** in this conversation, per `REVIEW_RUBRIC.md`
   and the Spec Review Kickoff validation categories — a **holistic whole-plan**
   pass, not a delta (the cold full read is the entire point of this gate). Verify
   every file:line claim and existing-mechanism (4a) claim against CURRENT source
   yourself — read the cited code; do not trust the spec's claims. Cover scope
   coverage, self-containment, dependency claims, label correctness, test-strategy
   quality (per TESTING.md; for UI specs also design-strategy quality per
   FRONTEND.md), and over-scope / existing-mechanism reuse. For any
   external/library/API/version/deprecation or "current best-practice" claim the
   spec rests on, verify it via web search against official upstream docs (cite
   source + date) and temper "latest" against the repo's pinned major — don't
   approve or reject a dated claim from memory.
5. **Return** per the shared carry-back shape, with these spec specifics:
   - verdict line: `APPROVED` or `ACTIONABLE` (name the spec + its `status`)
   - findings with severity and section or file:line (ACTIONABLE only); mark
     direction decisions `[decision-required]`
   - what you verified clean (claims checked against source, sections traced)
   - one line: paste this into the planning session; autonomous ACTIONABLE
     findings go through `specrereview` there (the loop handles them), while
     `[decision-required]`/direction findings stop for the operator (specreview's
     disposition). Re-run this gate only if the plan changed materially.

## Guardrails

- Read-only: verify the spec's claims by reading current source; no spec/code
  edits, no branch, no tracker mutation. A plan has no code to execute — assess
  the spec's verification plan, don't run an implementation gate.
- Accidental prior-review exposure is not a stop condition: apply HANDOFF's
  quarantine rule, disclose it, and still return the strict verdict.
- Strict-verdict / no-soften / no-early-read-counts per the shared protocol.
- One pass only — this gate does not loop. The `specreview` ⇄ `specrereview` loop
  in the planning session owns iteration; re-run this gate only if the plan
  changed materially after re-converging.

## Failure modes

The shared ones in HANDOFF.md "Outer-gate protocol", plus spec specifics:
trusting the spec's file:line / 4a claims instead of verifying them against
current source; delta-reviewing instead of a holistic whole-plan pass (the cold
full read is the point); reviewing a `rough`/mid-loop draft as if certifying it.
