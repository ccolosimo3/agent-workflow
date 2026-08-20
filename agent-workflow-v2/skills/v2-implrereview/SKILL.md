---
name: v2-implrereview
description: Reuse the original V2 inner implementation reviewer to verify patches for its ACTIONABLE findings. Use after v2-implreview patches; outer findings return to their own reviewer.
---

# V2 Implementation Re-review

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`; load
`../../references/FRONTEND.md` only for UI scope. Stop if an applicable authority
is unavailable.

Require the prior findings verbatim, prior reviewed tip, current tip, patch range,
resolutions mapped per finding, and affected verification. Resume the original
reviewer with only that delta payload. Do not rebuild the initial handoff or ask
for broad rediscovery.

The reviewer applies `REVIEW.md`'s Re-review mode. Use a fresh fallback only when
the original cannot be resumed, disclose the limitation, and supply the full
initial payload plus prior findings. Return the verdict to `v2-implreview` for
decision routing and outer-gate selection.
