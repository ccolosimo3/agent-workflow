# Spec Re-Review Kickoff

```text
Re-review plan / spec <path> after revisions following a prior ACTIONABLE spec review.

## Prior review
- verdict: ACTIONABLE
- source kickoff: <pointer to original Spec Review Kickoff if present>
- findings (restated verbatim from prior reviewer):
  - [severity] section-or-line | category | issue | required fix
  - ...

## Revisions applied
- artifact path: <path>
- summary of revisions: <one or two sentences mapping revisions to findings>
- diff (if version-controlled): <verbatim output of `git diff <base>..HEAD -- <artifact path>`, or before/after snippet>

## Repo conventions to enforce
Resolve per HANDOFF.md step 3.

## Verify
Return:
1. Per-finding status: for each prior finding, "addressed" or "not addressed", with the revised section quoted or referenced.
2. New issues introduced by the revisions (rare but possible — e.g. revisions widened scope, introduced contradictions with non-goals, broke self-containment).
3. Verdict: APPROVED or ACTIONABLE.

When Verdict is ACTIONABLE, mark any finding requiring operator input with `[decision-required]` and append the Planner directive (`~/.agents/workflow/kickoffs/planner-directive.md`) verbatim.

Focus on the revisions and the prior findings. Do not perform a fresh broad spec review.
```
