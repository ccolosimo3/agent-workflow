# External PR Review Kickoff

For reviewing someone else's PR as a fresh-context strict pass. Findings feed
the operator's `calibrate-review` step, not the implementation loop. Normally
populated and spawned by the `prreview` skill; usable manually too.

```text
Review external PR <number/url> (author: <login>) against <target branch>, as a
fresh-context reviewer. The PR author is a coworker, not this session's
implementer.

Apply the Review Rubric in `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL — read
it first, run its Required investigation against the diff, and return per its
Output contract — with these external-PR deltas:

- There is no implementer session. The PR title/body and the linked issue are
  the author's CLAIM; the Context below is the populator's reading of them. The
  diff and the repo are the source of truth.
- Verify locally; do not trust stated results. Before `gh pr checkout <number>`,
  run `git status --short` — if the tree is dirty, stop and ask (or use a
  separate worktree) rather than switching over local changes. Then run the
  Context item 4 gates yourself on the checked-out branch.
- GitHub is read-only for you: fetch, check out, and read threads, but post no
  comment, review, or approval.
- Read review comments already posted on the PR (automated + human) first. Do
  not re-litigate them; note material agreement or disagreement only.
- Do NOT append the rubric's implementer directive. Findings return to the
  OPERATOR for calibration and author conversation (calibrate-review skill) —
  never address the author directly. `[decision-required]` marks decisions for
  the operator/author conversation.
- Append output item 8, the Verified-clean record. It is the evidence basis the
  operator may later rely on with the author, so list only checks you ran.

Context (per-task):

1. Work item
   - PR: <url> (author: <login>, target branch: <branch>)
   - issue/spec link: <url from the PR body, or "none linked">
   - review range: `<base sha>..<tip sha>` (base = merge-base with the target
     branch; tip = PR head). Run `git diff <base>..<tip>` and `git diff --stat
     <base>..<tip>` yourself — they are NOT pasted into this prompt.
   - acceptance criteria (populator's reading of the linked issue — re-derive
     them yourself; if no issue is linked, the narrowest reasonable reading of
     the PR body is the authorized scope):
     - [ ] <AC bullet>

2. Author's stated summary (from the PR body — a CLAIM)
   <what the PR says it does and why>

2a. Original request / intent (from the linked issue, verbatim or close)
   <the ask that triggered this PR; compare the diff against THIS, not only the
    ACs, to catch unrequested approach substitutions>

3. CI / existing review state
   - checks: <gh pr checks rollup: pass / fail / pending>
   - author-stated manual verification (a CLAIM): <quote, or "none stated">
   - already-posted review comments: <automated + human threads, or "none">
   - automated-reviewer exclusions: <.coderabbit.yaml path_filters, or "no file">

4. Local verification to run (on the checked-out PR branch; record each
   command + result in your Return)
   - <repo-appropriate gates, e.g. typecheck / lint / affected tests>

5. Surfaces touched (populator's read — verify from the diff)
   - <customer UI / internal admin / dev-only tool / backend service /
     migration / generated contract / provider-infra>

6. Repo conventions to enforce: resolve per HANDOFF.md step 3.

Return: the rubric Output contract in full (acceptance-criteria coverage,
per-test ledger, test-quality sub-verdict, verdict, findings with
severities, verification notes, convention conformance, residual risk), plus:

8. Verified-clean record — bullets of the specific checks that came back CLEAN:
   files read, traces followed (X -> Y), commands run with results, contracts
   compared. Only what you actually did — this record is consumed by
   calibrate-review as the evidence behind anything the operator relays to the
   author.
```
