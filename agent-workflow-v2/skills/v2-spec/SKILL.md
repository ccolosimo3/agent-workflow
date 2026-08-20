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

Before entering review, resolve `v2-specreview`, `../../references/REVIEW.md`,
`../../references/TESTING.md`, and the Spec initial payload they require. Stop
with “review phase not implemented” if any is unavailable. Otherwise invoke
`v2-specreview` and let its inner and risk-selected outer loops complete without
an ordinary status pause.
