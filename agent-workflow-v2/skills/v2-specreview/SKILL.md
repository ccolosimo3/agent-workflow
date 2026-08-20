---
name: v2-specreview
description: Hand a completed V2 specification to one fresh inner reviewer and drive its same-reviewer revision loop to approval or a material operator decision. Use after v2-spec or for an explicit V2 spec preflight; not for code review.
---

# V2 Spec Review

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, `../../references/REVIEW.md`, and
`../../references/TESTING.md` completely. If the spec has UI scope, also read
`../../references/FRONTEND.md`. Stop if a required authority cannot be resolved,
then read the repository instructions and relevant adapter.

## Initial review

Confirm the spec is review-ready and build `REVIEW.md`'s Spec initial payload
from the artifact and filesystem. Missing material remains visible; do not invent
it. Hand the payload and authority paths to exactly one fresh reviewer using the
host's isolated review capability. The planning context does not certify its own
spec. If no fresh review capability exists, report that limitation and do not
claim a verdict.

The reviewer applies `REVIEW.md`'s Spec method and Output contract to the entire
artifact and returns strict `APPROVED` or `ACTIONABLE`.

## Convergence

On `ACTIONABLE`, patch grounded mechanical findings autonomously. Stop for a
`[decision-required]` item or any correction that changes product behavior,
scope, policy, authority, safety, or the selected Task boundary. Otherwise run
`v2-specrereview` with the original reviewer. Continue under `REVIEW.md` until
approved or the three-cycle cap is reached.

After approval, apply `WORKFLOW.md`'s outer-spec selector. Launch
`v2-outerspecreview` in a fresh context when selected or requested; otherwise
record the one-line skip reason and finish. Do not pause merely to ask whether to
run a required review gate.
