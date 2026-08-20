---
name: v2-outerspecreview
description: Run the fresh independent outer gate for a converged V2 specification when risk routing or the operator selects it, then re-review its patches in the same conversation. Not for inner review or implementation.
---

# V2 Outer Spec Review

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, `../../references/REVIEW.md`, and
`../../references/TESTING.md`; load `../../references/FRONTEND.md` only for UI
scope. Stop if any applicable authority is unavailable, then read the repository
instructions and adapter.

## First pass

This skill runs inside the fresh outer-review context; do not spawn another
reviewer. Before the first verdict, confirm from host/task provenance that this
context was created specifically as a fresh outer reviewer and contains no
planning, implementation, or prior-review history. If that cannot be established,
stop without a verdict and request fresh isolated dispatch. Confirm the named spec
is converged from the operator or caller's explicit assertion. Read the whole spec
and its load-bearing dependencies, but do not read prior review findings,
verdicts, review logs, or kickoff prompts.

Independently build the Spec initial payload from current source and apply
`REVIEW.md`'s Spec method and Output contract holistically. Verify load-bearing
file:line and current external claims yourself. Remain read-only: assess the
verification design but do not edit the spec, code, tracker, or repository state.

Return `APPROVED` or `ACTIONABLE`, findings, and a concise verified-clean record.
Direction findings return to the operator; other findings return to the planner
for a scoped revision.

## Follow-up

When the planner returns revisions, re-review them in this same conversation
using `REVIEW.md`'s Re-review mode. Do not demand a fresh outer task or route the
patch through `v2-specrereview`. Start another blind pass only when the operator
explicitly requests one.
