# Review Kickoff

```text
Review work item <id/link> / PR <id/link> / branch <branch> against <base>.

Apply the Review Rubric in `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL: read it
first, run its Required investigation against the diff, and return per its Output
contract (grouped test-quality summary with exception rows, a separate
Test-quality PASS/FAIL sub-verdict, the
overall verdict, and findings with the severity rubric). The Context below is the
implementer's CLAIM and orientation only — the diff and the repo are the source of
truth, and the Context is itself part of what you review.

Context (per-task):

1. Work item
   - issue/spec link: <url or path>
   - review range: `<base sha>..<tip sha>` (base = merge-base with the target
     branch; tip = HEAD). Run `git diff <base>..<tip>` and `git diff --stat
     <base>..<tip>` yourself for the authoritative diff and file list — they are
     NOT pasted into this prompt.
   - acceptance criteria, copied inline:
     - [ ] <AC bullet>
     - [ ] <AC bullet>

2. Implementer summary (2-3 sentences)
   <what changed and why>

2a. Original operator request / intent (verbatim or close paraphrase — the
    rubric's Scope-vs-intent check compares the diff against THIS)
   <the exact ask that triggered this work; if broader than the AC, say so>

3. Scope
   - in scope: <1-2 sentence summary of what changed; do NOT enumerate file
     paths — derive the file list from `git diff --stat <base>..<tip>`>
   - out of scope, noticed but intentionally not touched: <items + reason>
   - discovered follow-ups: <items, to be captured as separate issues>

4. Verification run
   - <command>: <one-line result with a useful number, e.g. "typecheck: 0 errors across 412 files">
   - <command>: <...>

5. Verification routing
   - selected level: <Tier 1/Tier 2/Tier 3/Tier 4 mix>
   - broader local gates considered: <build/e2e/contract/manual/local-stack/etc.>
   - gates not selected or blocked: <short reason, or "none">

5a. Docs impact (per the kernel Docs Impact Check — a CLAIM to confirm)
   - <`none`, or the owning tracked doc path updated in this change>

5b. Visual evidence (UI work only)
   - profile: <standard | composition-heavy — reason>
   - rendered evidence: <path/link, or standard-profile/operator-tier reason>
   - residual visual checks: <items + owner, or none>

6. Test quality (implementer's CLAIM — do NOT accept; re-derive each test per the
   rubric's Behavior-proof audit + inclusion-disposition check and
   `~/.agents/workflow/TESTING.md`)
   - behavior/failure mode each new or changed test protects + real boundary
     exercised + any implementation-shape test (why contractual/supplemental) +
     manual/Tier-4 proof
   - tests written but pocketed/excluded as one-off proof, or that you consider
     marginal to ship (redundant / over-weight): <list + why, or "none">

7. Hot spots / known risk
   - <areas wanting extra review attention>
   - <deviations from spec or assumptions made>

8. Tier 4 gate
   - required: yes/no; if yes, what (manual QA / hardware / live provider) + who runs it

9. Repo conventions to enforce: resolve per HANDOFF.md step 3.
```
