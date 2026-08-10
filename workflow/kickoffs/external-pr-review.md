# External PR Review Kickoff

Internal lead context for `prreview`; never give this full kickoff to a
challenger or specialist.

```text
Review external PR <number/url> (author: <login>) against <target branch>.

Read and apply `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL. The PR body,
linked issue, and Context are claims; the frozen diff and repository are truth.
Apply these external-review deltas:

- Verify in the prepared checkout at the frozen tip; never follow a moving PR ref.
- Keep GitHub read-only. Defer posted comment content until independent discovery
  and challenger convergence finish, then deduplicate and reconcile it.
- Return findings to the operator for `calibrate-review`; do not append the
  implementer directive or address the author directly.

Context:

1. Work item
   - PR: <url>; author: <login>; target: <branch>
   - issue/spec: <url, or none>
   - range: `<base sha>..<tip sha>`; derive the diff/stat yourself
   - checkout: <absolute path>; confirm `HEAD == <tip sha>`
   - acceptance criteria: <bullets re-derived from issue/body>
   - profile: <compact | standard | large — reason>

2. Author claims and raw intent
   - summary: <PR claim>
   - original ask: <linked issue text or narrowest reasonable PR-body reading>

3. Existing state
   - CI: <pass/fail/pending>
   - author-stated manual verification: <claim, or none>
   - posted review state: <counts/status only; content deferred>
   - automated-reviewer exclusions: <paths, or none>

4. Local verification
   - `<command>` — <planned purpose; return exact result>

5. Surfaces and seams
   - <behavior, service/UI, contract, persistence, provider/deploy, shared seam>

6. Repo conventions to enforce
   <resolve from the filesystem per HANDOFF.md step 3>

The `prreview` skill owns convergence, steering, and final calibration. Return
its one-screen Action Brief, then one compact operator-only appendix containing
the strict result, non-clean AC/test items, grouped clean test coverage + test
quality verdict, findings and their final actions/rejections, verification,
material verified-clean surfaces, and residual/Tier-4 checks. Never print full
clean AC or per-test ledgers.

8. Verified-clean record
   - <only checks actually performed: files/traces/contracts/commands + results>
```
