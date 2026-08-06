# Re-Review Kickoff

```text
Re-review work item <id/link> / PR <id/link> / branch <branch> against <base>.

Apply the Review Rubric in `~/.agents/workflow/REVIEW_RUBRIC.md`, "Re-review mode":
your scope is the changed lines + the prior findings, not a fresh broad review.
Still load its Required reading and apply its test-quality, masking, and
decision-required rules to what changed.

## Prior review
- verdict: ACTIONABLE
- source kickoff: <pointer/quote of original Review Kickoff if present>
- findings (restated verbatim from prior reviewer):
  - [severity] path:line | category | issue | impact | required fix
  - ...

## Patches applied since the prior review
- review range: `<base sha>..<tip sha>` (base = prior-review tip; tip = HEAD)
- commits: <`git log --oneline <base>..<tip>`>
- diff stat: <`git diff --stat <base>..<tip>`>
- implementer notes (if any): <how each finding was patched>

## Repo conventions to enforce
Resolve per HANDOFF.md step 3.

## Return
The "addressed" bar, reverse-tautology rule, and OUTSTANDING
`[decision-required]` handling are owned by REVIEW_RUBRIC.md "Re-review mode".
1. Per-finding status: for each prior finding, "addressed" / "not addressed" /
   "OUTSTANDING" (unresolved `[decision-required]`) with `path:line` evidence.
2. Regressions: any behavior the patches broke that worked under the prior reviewed
   state.
3. New issues in the changed lines — apply the rubric's Behavior-proof and
   Contract-propagation audits, Scope-vs-intent check, plus missing docs.
4. Verdict: APPROVED or ACTIONABLE. When ACTIONABLE, mark operator-input findings
   `[decision-required]` and append the rubric's implementer directive.

If Verdict is ACTIONABLE, return findings and end this invocation. Any further
patch returns to this same reviewer per `HANDOFF.md` re-review reuse.
```
