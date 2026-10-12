---
name: review-delivery
description: Review an operator-selected integrated delivery against its original goal and acceptance, with risk-selected independent challenge. Use for combined own-work behavior across tasks or a batch; not for coworker PRs or ordinary inner/outer gate dispatch.
---

# Review Delivery

This is an optional aggregate-review phase. It reuses existing review standards;
it does not add a required closeout stage or replace ordinary inner/outer gates.
The invoking agent coordinates; one independent lead owns the delivery verdict.

## Authorities and scope

Resolve the real package directory when discovered through a link. Read
`../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`, plus repository
instructions and its adapter. Resolve profiles through `../../HOST.local.md`
when present; load `../../references/FRONTEND.md` only for UI scope.

Use the original goal, non-goals and existing acceptance. Freeze a clean,
committed candidate and the baseline covering the selected delivery. Derive the
integration range from repository instructions and reconcile any explicitly
selected range; a last-task or integration-only delta is not necessarily the
whole delivery. Resolve material scope ambiguity before claiming coverage.

Keep source read-only. Review combined behavior and affected consumers within
that scope; do not absorb unrelated historical defects. Reuse valid verification
and keep closed constituent gates closed unless corrections invalidate them.

## Independent review and fan-out

The lead starts without planning, implementation or prior-review history. Use
this conversation only when it already has that independence; otherwise dispatch
one fresh lead. The lead and helpers inherit the invoking host, model and effort
unless the operator selects another profile; helpers inherit no conversation
history. Give initial reviewers the raw goal, acceptance, frozen range, checkout,
authority paths and verification evidence, withholding prior findings/verdicts.

Choose the smallest topology that fits:

- One lead for a cohesive low-risk delivery.
- Add one fresh blind challenger for material risk or cross-task interactions
  requiring an independent trace.
- Add specialists only for independent material seams needing separate traces,
  never more than three helpers total. Assign each one bounded question, not a
  fixed department or a duplicate whole-delivery review.

The lead applies `REVIEW.md`'s implementation investigation and verdict rules to
the entire selected delivery, including test quality and inclusion under
`TESTING.md`. Specialist coverage does not replace the lead's complete coverage.
Helpers return sourced candidates, counterevidence, important clean claims and
proof gaps; they do not own severity or verdicts. The lead coordinates proof;
helpers stay read-only except for an explicitly assigned narrow check.

Collect the blind reports on the unchanged candidate before reconciliation.
Then ask the same challenger to refute material findings and clean claims at
the actual boundary, investigate a potentially missed seam, and identify decisive
proof for disagreements. Continue only while material evidence changes.
Unavailable helpers permit useful lead work with disclosed topology limits;
missing required investigation or material proof still prevents approval.

## Evidence and closure

Run narrow proof only when a changed seam or concrete hypothesis can invalidate
existing evidence. Explain the supported trigger, delivery relevance and actual
consequence, including recovery; distinguish exercised boundaries from simulated
or unperformed paths. Agreement and passing test counts do not establish those
claims. All operations remain within `KERNEL.md` authority.

Return `REVIEW.md`'s implementation output with the exact delivery range and tip,
one lead verdict, findings, actual verification and material limits. Name remaining
proof that could change the verdict. Keep detail in its existing owner; add no
manifest, checklist or mandatory audit artifact.

Return corrections to the delivery's existing author/integration owner. Review
does not select implementation. When corrections are authorized, use the ordinary
own-work review route for affected source, then return the committed delta and
invalidated proof to the same delivery lead under `REVIEW.md`'s re-review/recovery
rules. Final approval covers the whole accumulated delivery at the final tip.
Do not reopen unaffected gates or replace reviewers because of their findings.
