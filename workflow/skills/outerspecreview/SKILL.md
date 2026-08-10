---
name: outerspecreview
description: >-
  Run the fresh outer gate for the operator's own converged plan/spec when
  HANDOFF routes it or the operator requests /outerspecreview or a second spec
  review. Supports the skill's documented model override. Not for inner spec
  review, code review, or coworker PRs.
---

# outerspecreview

The outer gate of the plan flow — the planning analog of `outerreview`
(sequencing and independence rules: `~/.agents/workflow/HANDOFF.md`). It runs in
a FRESH conversation in the app/model that did NOT plan; the conversation itself
is the fresh-context reviewer, so do the review here in the main thread — do not
spawn a subagent. It exists because the `specreview` loop converges through
`specrereview`, which is delta-scoped — so the converged plan never got a cold,
holistic whole-artifact read. This gate is that read, from a different model,
un-anchored by the loop.
It may be launched automatically by the planning session after inner convergence
under HANDOFF.md's routing, or explicitly by the operator.

## Invocation router

- **Non-Claude caller:** read HANDOFF.md "Shared Claude CLI review launch" and
  "Claude spec outer gate", resolve the spec path, and launch the fresh
  Claude review. Default to Opus 5 `high`; honor an explicit supported profile.
  Monitor and return the verdict to this planning session. Do not perform the
  review here as well.
- **Claude Code/Claude or explicit `review here`:** perform the review in this
  conversation using the steps below. Do not launch another Claude process.

## When invoked

1. **Preflight (read-only).** Confirm the spec under review (operator pointer, or
   auto-detect the active work-item folder, e.g.
   `<root>/.agent-workflow/plans/active/<ISSUE>-*/`). Confirm it is **converged** —
   the `specreview` loop reached APPROVED. Accept `final`/`promoted` frontmatter,
   the operator's word, or the calling planning session's explicit convergence
   assertion; do NOT open `reviews.md` to prove it. `review-ready` alone is not
   proof, but it is valid with that caller assertion because operator promotion
   happens later. If no signal exists, ask. Read-only: no edits to the spec, no
   branch, no tracker mutation.
2. **Locate the artifact.** Read the living spec (`README.md` or the named spec
   file) and the sibling docs it depends on (`*_OPTIONS.md`, `*_SPIKE.md`,
   `verification.md`) — the spec is what you are reviewing.
3. **Independence seal (hard rule).** Do NOT read `reviews.md`, prior spec-review
   verdicts, or prior kickoff prompts — in the folder or in chat. If the operator
   pasted loop findings, set them aside unread; this review must not be anchored
   by what the first lens found. Inner-review findings belong to `specrereview`;
   this outer conversation may later re-review only its own findings.
4. **Populate the `## Spec Review Kickoff` template** from
   `~/.agents/workflow/kickoffs/spec-review.md` per the HANDOFF.md protocol (fidelity, honest
   population, repo-conventions resolution from the shim) — filled from the spec
   itself, not session memory. This is INTERNAL orientation — assemble the
   context to review against; do NOT print the populated kickoff back to the
   operator. What was reviewed is recorded concisely by the verdict return
   (step 6).
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
   - one line: paste this into the planning session; `[decision-required]` /
     direction findings stop for the operator, while other ACTIONABLE findings
     are patched there and returned to this same outer conversation for
     re-review. Do not route outer findings through `specrereview`.

## Guardrails

- Read-only: verify the spec's claims by reading current source; no spec/code
  edits, no branch, no tracker mutation. A plan has no code to execute — assess
  the spec's verification plan, don't run an implementation gate.
- Strict independent verdict — do not soften it calibrate-review-style, and do
  not count an early read of a non-converged plan as the certifying second
  verdict.
- Only the first pass is fresh and blind. After its ACTIONABLE verdict, re-review
  the mapped revision in this same outer conversation; do not start another
  inner review or fresh outer pass.

## Failure modes

The shared ones in HANDOFF.md, plus: reading `reviews.md` or pasted prior
findings (independence seal); trusting the spec's file:line / 4a claims instead
of verifying them against current source; delta-reviewing instead of a holistic
whole-plan pass (the cold full read is the point); reviewing a `rough`/mid-loop
draft as if certifying it; silently changing an explicit model/effort request;
recursively launching Claude from a Claude reviewer; spawning a subagent (this
conversation IS the fresh context); routing this reviewer's findings through
`specrereview` instead of returning the patch here.
