---
name: secondspecreview
description: Run the operator-owned outer-gate second review of their OWN plan /
  spec, in a fresh conversation in the other app/model, after the planning
  session's specreview ⇄ specrereview loop has converged to APPROVED. Self-
  populates the Spec Review Kickoff from the spec file (never from a pasted
  prompt), deliberately ignores prior spec-review findings, and performs a
  holistic whole-plan review itself in this conversation per
  ~/.agents/workflow/REVIEW_RUBRIC.md + the Spec Review Kickoff validation
  categories — verifying the spec's file:line claims against current source —
  then returns a strict verdict for the operator to carry back. Use when the
  operator says /secondspecreview, "second spec review", "independent fresh pass
  on the whole spec", or names a converged spec for outer-gate review. Not the
  planning session's own loop (specreview / specrereview), not a code review
  (secondreview), not a coworker PR (prreview).
---

# secondspecreview

The outer gate of the plan flow — the planning analog of `secondreview`
(sequencing and independence rules: `~/.agents/workflow/HANDOFF.md`). It runs in
a FRESH conversation in the app/model that did NOT plan; the conversation itself
is the fresh-context reviewer, so do the review here in the main thread — do not
spawn a subagent. It exists because the `specreview` loop converges through
`specrereview`, which is delta-scoped — so the converged plan never got a cold,
holistic whole-artifact read. This gate is that read, from a different model,
un-anchored by the loop.

## When invoked

1. **Preflight (read-only).** Confirm the spec under review (operator pointer, or
   auto-detect the active work-item folder, e.g.
   `<root>/.agent-workflow/plans/active/<ISSUE>-*/`). Confirm it is **converged** —
   the `specreview` loop reached APPROVED and the operator advanced `status` to
   `final` (or `promoted`). Read that from the spec's `status:` frontmatter or the
   operator's word that the loop converged — NOT from `reviews.md` (the
   independence seal forbids it); if neither signal is available, ask rather than
   opening `reviews.md`. `review-ready` means the loop has not necessarily run
   yet, so if `status` is `review-ready` or `rough`, say so and treat this as a
   directional early read, not the certifying second verdict. Read-only: no edits
   to the spec, no branch, no tracker mutation.
2. **Locate the artifact.** Read the living spec (`README.md` or the named spec
   file) and the sibling docs it depends on (`*_OPTIONS.md`, `*_SPIKE.md`,
   `verification.md`) — the spec is what you are reviewing.
3. **Independence seal (hard rule).** Do NOT read `reviews.md`, prior spec-review
   verdicts, or prior kickoff prompts — in the folder or in chat. If the operator
   pasted loop findings, set them aside unread; this review must not be anchored
   by what the first lens found. (To re-review *against* prior findings, that is
   `specrereview` in the planning session, not this skill.)
4. **Populate the `## Spec Review Kickoff` template** from
   `~/.agents/workflow/KICKOFFS.md` per the HANDOFF.md protocol (fidelity, honest
   population, repo-conventions resolution from the shim) — filled from the spec
   itself, not session memory. Emit it in chat under `## Spec Review Kickoff
   Prompt` as the record of what was reviewed.
5. **Perform the review yourself** in this conversation, per `REVIEW_RUBRIC.md`
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
6. **Return, formatted for carry-back to the planning session:**
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
- Strict independent verdict — do not soften it calibrate-review-style, and do
  not count an early read of a non-converged plan as the certifying second
  verdict.
- One pass only — this gate does not loop. The `specreview` ⇄ `specrereview` loop
  in the planning session owns iteration; re-run this gate only if the plan
  changed materially after re-converging.

## Failure modes

The shared ones in HANDOFF.md, plus: reading `reviews.md` or pasted prior
findings (independence seal); trusting the spec's file:line / 4a claims instead
of verifying them against current source; delta-reviewing instead of a holistic
whole-plan pass (the cold full read is the point); reviewing a `rough`/mid-loop
draft as if certifying it; spawning a subagent (this conversation IS the fresh
context).
