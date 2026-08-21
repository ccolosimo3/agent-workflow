---
name: v2-implement
description: Implement one operator-selected V2 work item in its minimum-sufficient repository-conventional shape, verify it proportionally, and drive inner and selected outer review to completion. Use for own-work execution; not for planning or coworker PR review.
---

# V2 Implement

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, `../../references/TESTING.md`, and
`../../references/REVIEW.md` completely. Load `../../references/FRONTEND.md` only
for UI scope. Stop if an applicable authority cannot be resolved, then read the
repository's instruction chain and adapter.

## Entry and preflight

Confirm the operator selected implementation. Build `WORKFLOW.md`'s envelope and
`PLANNING.md`'s Implementation payload from current evidence.

- **Fast:** require every Fast condition in `WORKFLOW.md`, a clear raw ask,
  behavioral acceptance, and one focused falsifier. Do not manufacture a spec.
- **Standard/Assured:** require the named spec to be inner-converged and any
  selected outer-spec gate to be complete. Treat status summaries as claims.

Confirm repository root, checkout/worktree owner, branch and integration base,
`git status`, acceptance and non-goals, current source claims, nearest owners and
complete patterns, approval state, and repository verification routes. Preserve
all unowned changes. Stop rather than guessing when the selected Task, checkout,
or required approval is ambiguous.

## Implement the Task

Apply `KERNEL.md`'s minimum-sufficient check before investing in a material
mechanism. Reuse existing owners and add only behavior unique to the Task.
Implement the smallest complete shape that satisfies acceptance, failures, and
safety; do not add speculative recovery, compatibility, configuration, state, or
abstractions.

A simpler repository-conventional mechanism may replace a planned mechanism when
observable behavior and approved contracts remain intact. Return to planning only
when a correction changes behavior, scope, authority, safety, or the Task's risk
boundary. Record adjacent work as a reconciliation fact rather than absorbing it.

Update the existing owning documentation when behavior, contracts, setup,
architecture, verification, or user/operator workflow changes. For UI work,
apply `FRONTEND.md` proportionally and remove temporary fixtures or tooling.

## Verify and review

Use the repository's verification routes and `TESTING.md`. Run the smallest
falsifying proof during the loop and every risk-selected affected gate once before
review. Tie results to the exact revision. After a patch, rerun only evidence the
delta can invalidate; use a broad gate when shared infrastructure changed or no
valid constituent proof remains. Keep one-off proofs outside the permanent suite
and report unavailable, unselected, or operator-only checks honestly.

Before review, repeat the minimum-sufficient check, remove unearned machinery and
temporary residue, inspect the full diff, and decide documentation impact. Update
this work item's own artifact with delivered facts. When a named main planner is
active, leave shared program/index state to it and retain the planner's return
identity; otherwise perform the repository's normal state update now. Commit every
in-scope change as real commit(s) without amend, squash, rewrite, push, or external
mutation, and disclose any preserved unowned working-tree change. Apply
`REVIEW.md`'s documentation-only off-ramp; otherwise invoke `v2-implreview`
automatically and follow its same-reviewer inner and risk-selected outer loops.
Outer-owned patches return only to the same outer reviewer.

## Complete

After review approval or a documentation-only off-ramp determination, confirm the
live tip and that no in-scope change remains uncommitted. Do not mutate the
certified tip. If a proof fails, distinguish whether it disproves product
behavior or only its own premise/harness before reporting implementation state.
Return shared index/program reconciliation only when a named main planner is
active; otherwise report that the normal state update is already included. Emit
this compact record with real values and `none` for empty sections:

```text
## Completion receipt — <work item ID/title>

Outcome: <observable result and why it matters>
Spec/source: <artifact path, tracker URL, or Fast ask>
Branch / checkout: <branch> | <absolute repository/worktree root>
Range / tip: <base>..<tip> | <full tip SHA>
Working tree: <clean | preserved unowned changes disclosed>
Environment: <only relevant prepared services/data, or default local>

Verification:
- <exact command or proof> — <useful result>

Reused evidence:
- <proof and causal reason, or none>

Not selected or blocked:
- <check and reason, or none>

Docs impact: <updated owner paths and effect, or none>
Review: <inner verdict and pass count | skipped — documentation-only off-ramp>
Outer gate: <approved | skipped — reason | blocked>
Remaining operator proof: <exact check and owner, or none>
```

Do not include findings or an internal ledger. When the operator asks for a PR,
compose its body from `../../templates/pr-body.md`; pushing, opening/editing the
PR, tracker mutation, or any other external action still requires `KERNEL.md`
approval.
