---
name: v2-spec
description: Turn an operator-selected work item into one grounded, right-sized, implementation-ready Task with behavioral acceptance and risk-selected verification. Use for a formal spec; not for casual planning, architectural option comparison, or implementation.
---

# V2 Spec

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`, and
`../../references/PLANNING.md` completely. Stop if any cannot be resolved. Then
read the repository instructions and adapter relevant to the work item.

## Specify the next Task

Confirm the operator selected a formal spec. Re-ground the raw outcome against
current source, owners, nearest complete patterns, and relevant landed work.
Treat prior plans and summaries as claims. Resolve ordinary mechanical ambiguity
through repository evidence; pause only for a material direction choice owned by
the operator.

Define the next independently reviewable risk boundary using the Spec contents in
`PLANNING.md`. Make acceptance behavioral and verification falsifying. Preserve
implementation latitude while naming mechanisms that are genuinely load-bearing.
Apply the minimum-sufficient shape check before declaring review-ready.

Work serially by default. A bounded evidence helper may answer a distinct factual
question under `WORKFLOW.md`; it does not author a second spec or certify this
one.

Write one compact living spec at the repository's declared plan location. Do not
implement code, mutate trackers, or promote the plan merely because drafting is
complete.

Before review, resolve `v2-specreview`. If unavailable, report “review phase not
implemented” without promotion or kickoff. Otherwise invoke it;
`v2-specreview` owns authority resolution, payload construction, and review
loops.
