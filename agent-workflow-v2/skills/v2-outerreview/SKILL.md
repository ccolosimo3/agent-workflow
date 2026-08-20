---
name: v2-outerreview
description: Run the fresh independent outer gate for a converged V2 implementation when risk routing or the operator selects it, then re-review its patches in the same conversation. Not for coworker PRs or inner review.
---

# V2 Outer Implementation Review

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`; load
`../../references/FRONTEND.md` only for UI scope. Stop if an applicable authority
is unavailable, then read repository instructions and the relevant adapter.

## First pass

This skill runs inside the fresh outer-review context; do not spawn another
reviewer. Before the first verdict, confirm from host/task provenance that this
context was created specifically as a fresh outer reviewer and contains no
planning, implementation, or prior-review history. If that cannot be established,
stop without a verdict and request fresh isolated dispatch. Preflight the live
checkout read-only. Require a clean, committed, inner-converged candidate,
determine the integration branch from repository instructions, and independently
compute merge-base, live tip, and review range. Treat any receipt SHA or path as a
claim and navigation hint, never range or checkout authority.

Read the work item/spec and entire changed surface. Do not read prior findings,
verdicts, review logs, or kickoff prompts. Build the Implementation initial
payload from current source and apply `REVIEW.md`'s Implementation method and
Output contract. Reuse green verification only when it matches the reviewed tip
and environment and the diff gives no causal reason to doubt it; run the
narrowest decisive check for concrete review hypotheses.

Remain read-only: no edits, commits, branch switches, tracker/GitHub mutation, or
provider activity. Return `APPROVED` or `ACTIONABLE` with the certified range and
tip, findings, reused/rerun evidence, and concise verified-clean record.

## Follow-up

After a scoped patch, preflight and compute the new tip, then re-review here using
`REVIEW.md`'s Re-review mode. Inspect the entire delta from the previously
reviewed tip. A hunk unrelated to an outer finding is scope expansion and returns
to the operator; do not reopen the inner reviewer automatically. Do not demand a
fresh outer task merely because the tip moved.
