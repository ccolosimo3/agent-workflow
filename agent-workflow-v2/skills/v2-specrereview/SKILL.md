---
name: v2-specrereview
description: Reuse the original V2 inner spec reviewer to verify revisions for its ACTIONABLE findings. Use after a v2-specreview revision; outer-spec findings return to their own reviewer.
---

# V2 Spec Re-review

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, `../../references/REVIEW.md`, and
`../../references/TESTING.md`; load `../../references/FRONTEND.md` only for UI
scope. Stop if any applicable authority is unavailable.

Require the prior findings verbatim, the exact artifact revision previously
reviewed, the current artifact, resolutions mapped per finding, and affected
verification. Resume the original reviewer and pass only that delta payload; do
not rebuild the initial kickoff or request a broad review.

The reviewer applies `REVIEW.md`'s Re-review mode. Use a fresh fallback only when
the original cannot be resumed, disclose that fact, and provide the full initial
payload plus prior findings. Return the verdict to `v2-specreview` for its
decision routing, cycle cap, and outer-gate selection.
