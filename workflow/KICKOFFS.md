# Portable Kickoffs

Copy these prompts into an agent session when you want a consistent workflow.

## Planning Kickoff

```text
Run planning kickoff for <feature/workstream> from <source>.

Mode: <task|gated|fast>  # default task
No code changes.

Deliver:
1. problem framing
2. goal and non-goals
3. risks and edge cases
4. 3-5 step implementation plan
5. testable acceptance criteria
6. exact verification plan by tier, including any broader local gates selected
   or intentionally not selected
7. review-ready spec markdown that can become the final tracker issue body
8. decision brief: chosen approach, one rejected alternative, tradeoff, assumptions
9. claim grounding: confirm each load-bearing code claim (where to wire a change,
   what a file already does, what a contract exempts, "follows pattern X") against
   current source, citing the file:line you checked; mark any claim you could not
   confirm as an open question instead of asserting it from memory. Scale to risk —
   fast-mode fixes can ground inline.
10. Domain Pass decision (one line): per the AGENTS.md "## Domain Pass" triggers,
    state whether this plan needs a Domain Pass and why or why not; if yes, run it
    or flag it as required before the spec goes review-ready.
```

## Domain Pass

```text
Run a domain pass on <feature/plan>.

Challenge terminology against current repo language and code. Resolve canonical terms,
flag overloaded words, update/prepare CONTEXT.md entries when terms are settled, and
suggest an ADR only if the decision is hard to reverse, surprising without context, and
based on a real trade-off.
```

## Final Spec Promotion Kickoff

```text
Prepare final spec <path or link> for tracker publication in repo <repo>.

Output: update the same spec file in place so it can land verbatim as the GitHub issue body via `gh issue create`. Do not create a separate issue-draft file unless the spec must be split, redacted, or substantially reshaped for publication.

Pre-promotion review (recommended for non-trivial specs): spawn a fresh-context reviewer agent against the spec before publication. The reviewer validates scope coverage, file/line claim accuracy, label correctness against the repo's label set (`gh label list --repo <repo>`), self-containment of the final issue body, and dependency claims. Apply review feedback directly to the spec before marking it final. This catches stale paths, missed scope, mislabeled categories, and assumed-but-wrong code claims at the cheapest possible point.

Publication approval: `gh issue create` / `gh issue edit` follow the kernel's
Destructive Action Policy, including the `ISSUE-GO` prepared-packet shorthand.

Lifecycle: advance the spec `rough` -> `review-ready` -> `final` -> `promoted`
-> `implemented` per the statuses and update rules in
`~/.agents/workflow/PLANS.md`. Move to `review-ready` only when the spec is
coherent AND its load-bearing code claims (paths, identifiers, behavior-parity
claims) have been grounded against current code with file:line evidence; log
any claim you could not ground as an open question rather than asserting it.

Structure (required unless marked optional, in this order):

# <Title Case, action-verb start, no leading [tag]; taxonomy lives in Type below>

## Metadata
- Type: <Polish / Perf / Migration / Hygiene / Verification slice / ...>
- Labels: <platform + subsystem + workstream + work-type labels from the local shim's label set>
- (optional) Priority: <P0|P1>
- Execution mode: <build paths allowed; explicit guardrails on remote/EAS builds; manual gates>
- Suggested branch: `<per the local repo shim's branch convention>`
- Source / prior context: `<paths, issue links, audits, or parent specs>`
- (optional) Parent workstream / Supersedes / Related roadmap
- (optional) Blocked by / Ordered after: <full GitHub issue URLs>

## What to build              # use "What to verify" if no source changes except a reverted-before-merge edit
<1-3 paragraphs: goal + framing; code fence for flow diagrams or contracts when useful>

## Scope
<concrete bullets, each a verb + named file/identifier; subheadings for larger issues>

## (optional) Implementation notes
<HOW guidance when non-obvious; otherwise omit>

## Non-goals
<bullets starting "Do not ..."; one per intentional exclusion>

## Acceptance criteria
<- [ ] testable conditions, mirroring Scope but checkable post-implementation>

## Verification
<Tier 1 commands in code fences with language tags;
 broader local gates selected for this task, such as build/e2e/contract/manual
 QA/local-stack QA; gates considered but not selected with short rationale;
 manual smoke as `- [ ]` checklist mapping to acceptance criteria;
 use Environment setup / Test sequence / Reporting subsections only when long>

## (optional) Blocks
<full GitHub URLs of downstream issues this gates>

## (optional) Notes
<editorial caveats, why-this-issue-exists, intentional out-of-scope edge cases>

Conventions:
- Title Case in titles, action verb first, no `[tag]` prefix
- Hand-wrap lines at ~78 chars for readability in the GitHub web view
- Backticks for identifiers, paths, commands; code fences with language tags for runnable blocks
- `- [ ]` for acceptance criteria and manual verification items; plain `-` for scope/non-goals/notes
- Cross-issue references as full GitHub URLs, not markdown links
- Pull repo-specific defaults (branch prefixes, verification commands, target device, build-path guardrails) from the local repo shim
- If a required section cannot be filled, insert `<!-- TODO: ... -->` rather than skip silently
- If the spec has local-only notes, move them under `## Planning Notes` and remove that section before publishing, or explicitly mark it as not included in the tracker body.
```

## Plan Review Kickoff

```text
Review plan / spec <path or link> for <feature/workstream>.

Context (filled by the planner as ORIENTATION ONLY — it is the planner's CLAIM,
not ground truth, and the plan itself is what you are reviewing). The spec, the
repo, and the real code are the source of truth; where the Context and the
artifact disagree, verify against the code and treat the discrepancy as a finding.
Re-derive scope and dependency claims yourself rather than assuming the bullets
below are complete or faithful. Treat every line — summary, scope-coverage list,
and ESPECIALLY the test-strategy self-report in section 6 — as a claim to confirm
or refute. Assume the most important gap is something the planner did NOT list.

1. Plan artifact
   - path or link: <url or path>
   - artifact type: <rough-spec | review-ready-spec | final-spec | other planning markdown>
   - intended downstream action: <gh issue create | implementation kickoff | other>
   - target repo (if filing an issue): <repo>
   - target labels (if filing an issue): <comma-separated; pulled from `gh label list --repo <repo>`>

2. Planner summary (2-3 sentences)
   <what the plan delivers and why>

3. Source material
   - upstream context / parent spec / audit (if any): <path or URL>
   - related issues, ADRs, prior discussion: <urls or paths>
   - touched modules / files claimed in scope: <paths>

4. Scope coverage
   - intended in-scope items: <bullets>
   - intentional out-of-scope items: <bullets + reason>
   - dependency / ordering claims: <"blocks #X" / "blocked by #Y" / "ordered after #Z">

4a. Existing-mechanism claim (required for bug fixes, edge cases,
    fallback/error/loading behavior, and business-rule tweaks; planner's CLAIM —
    the reviewer verifies it)
   - adjacent mechanism: <the current code path that already handles analogous
     behavior, file:line — or "none found" + where you searched>
   - plan's relationship to it: <reuses/extends it | bypasses it, with why a
     narrower condition change cannot reach the existing path>

5. Hot spots / known risk in the plan
   - <ambiguous areas; claims the reviewer should fact-check against the code>
   - <decisions made and rejected alternatives>

6. Test strategy quality (planner's CLAIM — verify against the repo testing doc; do NOT accept these bullets)
   - behavior/failure mode each planned test protects: <bullets>
   - real operation boundary planned for tests: <service/API/job/UI/persistence/etc.>
   - implementation-shape tests, if any, and why that shape is contractual or supplemental:
   - manual/Tier 4 proof needed when automation cannot represent the failure mode:

7. Repo conventions to enforce (optional — include only when the repo shim names
   conventions the reviewer must check; real, existing paths in the repo under review)
   - testing: `~/.agents/workflow/TESTING.md`
   - coding-standards / patterns: <path, or "none found">
   - verification policy: <path, or "none found">
   - local shim: <path, or "none found">

Return:
1. Verdict: APPROVED or ACTIONABLE
2. Findings if ACTIONABLE: [severity] section-or-line | category | issue | required fix
   Validation categories (focus, not exhaustive):
   - scope coverage gaps (missing acceptance criteria, undefined non-goals)
   - file/line claim accuracy (do paths claimed in scope exist; do referenced symbols exist)
   - label correctness against the repo's actual label set
   - self-containment of an issue body (would this issue be actionable to someone with no prior context)
   - dependency claims (do blocked/ordered-after references point at real issues with the claimed state)
   - time-sensitive / external claims: if the plan picks a library, API, pattern, or
     version, or asserts something is deprecated / current / best-practice, verify it
     against the repo's pinned version + bundled SME/doc skills, then official
     upstream docs via web search (cite source + date) — don't approve or reject a
     dated claim from memory; temper "latest" against the repo's actual pinned major
   - ambiguous terminology or undefined nouns
   - missing or untestable acceptance criteria
   - missing or wrong verification commands
   - weak test strategy: BEFORE judging, open `~/.agents/workflow/TESTING.md`
     (Part 1 principles + Part 2 universal anti-patterns + the repo's stack
     section) and apply its anti-pattern tables + 10-second check to each PLANNED
     test; flag ACTIONABLE any planned test that, as described, matches an
     anti-pattern or would still pass if the fix were reverted. For any planned
     migration/schema/persisted-field change, apply the migration bar in
     REVIEW_RUBRIC.md "Surface-specific test bars" at plan time: a spec that
     plans only implementation-shape assertions, or only "add a migration
     test", is a blocking finding.
   - convention conformance: if any plan step explicitly proposes hand-rolling a
     component, helper, hook, loading state, or style primitive, open this repo's
     patterns doc (townchest:
     `.agent-workflow/plans/reference/coding-standards.md`; clearsnake:
     `mobile/CLAUDE.md`) and flag ACTIONABLE if the repo already has an
     established primitive for it (e.g. a custom Box/@keyframes shimmer where the
     repo mandates the existing Skeleton/loading primitive). Do not flag steps
     that reuse existing primitives or where no repo primitive is documented.
   - existing-mechanism reuse / over-scope: does the plan invent a new helper,
     policy, query, filter, fallback, branch, state, or UI behavior where the
     codebase already has an adjacent mechanism? Verify the 4a claim by reading
     the FULL function/module the plan modifies, not only the lines it cites —
     the missed mechanism is usually adjacent to the cited ones. For bug fixes
     the default is routing the case into the existing path via a narrower
     condition change; a new mechanism with no 4a justification (or a 4a of
     "none found" the code contradicts) is a blocking finding.
   - local-only/private notes that should not be published
3. Notes on scope or framing improvements (non-blocking but useful)

When Verdict is ACTIONABLE, mark any finding requiring operator input (scope change, contract decision, label policy interpretation) with `[decision-required]` in its required fix. Append this planner directive verbatim at the end of your output so it stays with the findings when the operator forwards them:

> Planner: address every finding autonomously. For any finding marked `[decision-required]`, skip the revision, summarize the decision needed, and return to the operator. Do not block other revisions on those.

Focus on whether the plan is correct, complete, and self-contained enough to be acted on. Do not write the implementation. Do not propose new scope unless it closes a coverage gap the plan claims to cover.

If Verdict is ACTIONABLE, return findings and stop. The planner revises and hands back to the operator; no second review cycle from this reviewer.
```

## Plan Re-Review Kickoff

```text
Re-review plan / spec <path> after revisions following a prior ACTIONABLE plan review.

## Prior review
- verdict: ACTIONABLE
- source kickoff: <pointer to original Plan Review Kickoff if present>
- findings (restated verbatim from prior reviewer):
  - [severity] section-or-line | category | issue | required fix
  - ...

## Revisions applied
- artifact path: <path>
- summary of revisions: <one or two sentences mapping revisions to findings>
- diff (if version-controlled): <verbatim output of `git diff <base>..HEAD -- <artifact path>`, or before/after snippet>

## Repo conventions to enforce (optional)
Include only when the repo shim names conventions the reviewer must check;
real, existing paths in the repo under review.
- testing: `~/.agents/workflow/TESTING.md`
- coding-standards / patterns: <path, or "none found">
- verification policy: <path, or "none found">
- local shim: <path, or "none found">

## Verify
Return:
1. Per-finding status: for each prior finding, "addressed" or "not addressed", with the revised section quoted or referenced.
2. New issues introduced by the revisions (rare but possible — e.g. revisions widened scope, introduced contradictions with non-goals, broke self-containment).
3. Verdict: APPROVED or ACTIONABLE.

When Verdict is ACTIONABLE, mark any finding requiring operator input with `[decision-required]` and append the planner directive verbatim:

> Planner: address every finding autonomously. For any finding marked `[decision-required]`, skip the revision, summarize the decision needed, and return to the operator. Do not block other revisions on those.

Focus on the revisions and the prior findings. Do not perform a fresh broad plan review.

If Verdict is ACTIONABLE, return findings and stop. The planner revises and hands back to the operator; no second review cycle from this reviewer.
```

## Execution Kickoff / Implementation Kickoff

```text
Run execution kickoff for existing work item <id/link>.
Mode: <task|gated|fast>  # default task; gated for high-risk/multi-step work; fast per the Fast Fix kickoff. State the mode and the one risk signal driving it.

Execute Startup Routing A ("Implement Existing Work Item") in AGENTS.md end to end:
read the item + local shim, restate goal/non-goals/AC, scope in/out, spot-check the
spec's load-bearing file:line claims against the tree before editing (surface any
conflict instead of coding against a stale claim), branch from a clean tree,
implement minimally, verify by tier, hand off for review (emit the Review Kickoff in
chat BEFORE spawning exactly one reviewer; the operator owns the second), then PR.
Do NOT restate the rules AGENTS.md already owns — follow them: Verification Tiers,
the Destructive Action Policy (identify every approval-gated command before running
it), the Review Loop, PR Handoff (PR body in the locked shape below, labels, PR-GO),
and Definition of Done.

Enforce these forcing functions ON TOP of Routing A:

- Surface-tied verification: if the diff touches a surface the repo verification doc
  (clearsnake `mobile/VERIFICATION.md`, townchest `AGENTS.local.md`) names a gate
  for — migration/schema/persisted state, native config, routing, auth, contract —
  that gate is REQUIRED; "Tier 1 sufficient" is not a valid record. Name the surface
  you changed and why no surface-triggered gate applies.
- Honest verification reporting: claim a gate passed only if it actually ran this
  session/branch; report each as a real result/number; mark un-run gates as not-run
  (reason/blocker or CI-owned), never as passing.
- Docs impact: state `Docs impact: none` or the updated tracked-doc path in the
  summary (per the Docs Impact Check).
- Commit discipline: commit after implementation and each patch round as real
  commits (no push, no amend); record the `<base>..<tip>` range so reviewers and
  re-reviewers diff a precise range. Commit freely on the branch; do NOT locally
  squash/rewrite/force-push — rely on GitHub squash-merge for one mainline commit
  per PR (townchest's squash body concatenates commit messages, so keep subjects
  presentable).
- Re-review trigger: on an ACTIONABLE verdict, patch + rerun targeted verification +
  re-review (cjcrereview) when the patch is non-trivial, touches lifecycle/state/
  concurrency, changes acceptance behavior, or rewrites/adds a test for a
  test-quality finding; skip only for a truly trivial patch, stated. A test-quality
  finding is addressed only if the new/edited test exercises the real boundary and
  goes RED on revert.
- Scope-creep guard covers SUBSTITUTION, not only addition (the rule and masking
  check live in REVIEW_RUBRIC.md, Stance / Scope-vs-intent sections): list
  out-of-scope work as "discovered follow-ups"; disclose any unrequested swap in the
  Review Kickoff Hot spots as "approach substitution: <old> -> <new>, not requested"
  and flag any preserved identifier (testid/route/name) whose implementation changed
  underneath it.
- One-off verification tests (a static-asset/config/data repair proof with no ongoing
  regression surface) → pocket to the work-item `artifacts/`, don't commit to the
  suite; disclose in the Review Kickoff.
- If mode=gated: pause for operator review after the restate step and after the first
  Tier 1 verification.
```

## Review Kickoff

```text
Review work item <id/link> / PR <id/link> / branch <branch> against <base>.

Apply the Review Rubric in `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL: read it
first, run its Required investigation against the diff, and return per its Output
contract (per-test ledger, a separate Test-quality PASS/FAIL sub-verdict, the
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
    rubric's "Scope-vs-intent & contract-identity check" and Stance checks
    compare the diff against THIS)
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

6. Test quality (implementer's CLAIM — do NOT accept; re-derive each test per the
   rubric's Test-quality rules + inclusion-disposition check and
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

9. Repo conventions to enforce (optional — include only when the repo shim names
   conventions the reviewer must check; real, existing paths in the repo under review)
   - testing: `~/.agents/workflow/TESTING.md`
   - coding-standards / patterns: <path, or "none found">
   - verification policy: <path, or "none found">
   - local shim: <path, or "none found">
```

## Re-Review Kickoff

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

## Repo conventions to enforce (optional)
Include only when the repo shim names conventions the reviewer must check;
real, existing paths in the repo under review.
- testing: `~/.agents/workflow/TESTING.md`
- coding-standards / patterns: <path, or "none found">
- verification policy: <path, or "none found">
- local shim: <path, or "none found">

## Return
The "addressed" bar, reverse-tautology rule, and OUTSTANDING
`[decision-required]` handling are owned by REVIEW_RUBRIC.md "Re-review mode".
1. Per-finding status: for each prior finding, "addressed" / "not addressed" /
   "OUTSTANDING" (unresolved `[decision-required]`) with `path:line` evidence.
2. Regressions: any behavior the patches broke that worked under the prior reviewed
   state.
3. New issues in the changed lines — apply the rubric's test-quality, masking/swap,
   and contract checks (Stance section of REVIEW_RUBRIC.md) plus missing docs.
4. Verdict: APPROVED or ACTIONABLE. When ACTIONABLE, mark operator-input findings
   `[decision-required]` and append the rubric's implementer directive.

If Verdict is ACTIONABLE, return findings and stop; no second review cycle from
this reviewer.
```

## External PR Review Kickoff

For reviewing someone else's PR as a fresh-context strict pass. Findings feed
the operator's `calibrate-review` step, not the implementation loop. Normally
populated and spawned by the `cjcprreview` skill; usable manually too.

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

6. Repo conventions to enforce (real, existing paths in the repo under review)
   - testing: `~/.agents/workflow/TESTING.md`
   - coding-standards / patterns: <path, or "none found">
   - verification policy: <path, or "none found">
   - local shim: <path, or "none found">

Return: the rubric Output contract in full (diff-coverage confirmation,
per-test ledger, test-quality sub-verdict, verdict, findings with severities,
verification notes, convention conformance, residual risk), plus:

8. Verified-clean record — bullets of the specific checks that came back CLEAN:
   files read, traces followed (X -> Y), commands run with results, contracts
   compared. Only what you actually did — this record is consumed by
   calibrate-review as the evidence behind anything the operator relays to the
   author.
```

## PR Body / Optional Review Notes

```text
Compose PR handoff text for work item <id/link> / PR <id/link>.

# Locked PR body shape

Required core, always present and in this order: `## Summary`, `## Verification`,
`## Docs Impact`. Optional sections appear ONLY when they carry real content, in
the order shown below. Omit an optional section entirely rather than writing
"None" — except Docs Impact, which is required and may be "None".

Closing reference — the FIRST line of the body, above `## Summary`:
- GitHub issue (e.g. clearsnake): `Fixes #<n>` when merge fully resolves it;
  `Refs #<n>` or `Part of #<n>` for partial / phase / validation-only work.
- Linear (e.g. townchest): `Closes <full https://linear.app/...> URL` when fully
  resolved; `Part of <url>` for partial. GitHub keywords do NOT close a Linear
  issue; the `issue.gitBranchName` branch also auto-links it. Never use a prose
  "Source issue: <url>" line to close — it does not auto-close.

Layout (annotations are not part of the output):

  <closing reference>                 # top line, per above

  ## Summary            (required)
  <one sentence: what changed + why, in user-facing/product terms>
  - <concrete change bullet>
  - <concrete change bullet>

  ## Root Cause         (optional — bug or non-obvious change)
  <why it broke / why this is needed; system nouns over implementation trivia>

  ## Impact             (optional — what now works or what risk is reduced; NOT a second summary)
  <one short paragraph>

  ## Screenshots        (optional — UI; or `## Visual QA`)
  <images / before -> after>

  ## Verification       (required)
  - `<command>` -> <result with a useful number>
  - <manual / Tier-4 proof, or state none>
  - gates considered but not selected: <reason>   # omit line if N/A

  ## Docs Impact        (required)
  None
  # or: <updated tracked-doc path> — <one line on what changed>

  ## Risks              (optional)
  <residual risk, 1-2 sentences>

  ## Follow-ups         (optional)
  - <deferred item> — <full issue URL if filed>

  ## Notes              (optional)
  - <rollback / migration / dependency / generated-output / build caveat>

Constraints:
- Keep review verdicts OUT of the PR body by default — review evidence stays
  local. Mention a review finding only in `## Notes`, and only when it explains a
  patched edge case, residual risk, or deferred follow-up. No standalone
  `## Review Summary` section.
- Plain `path:line` and full issue URLs; no markdown file links (GitHub does not
  resolve them in PR comments).
- Factual and concise, no marketing tone; prefer "no remaining blocking issues
  found" over absolutes like "approved", "fully safe", or "all issues resolved".
- Do not mention plan review by default; accepted specs normally pass plan review
  before coding.
- Return the PR body only, no preamble like "here is the summary".

# Optional separate review-record comment (only when the operator requests one)

A separate PR comment, not the body. Start with `# Review Notes`. Include: findings
patched in this PR as a brief bullet list with `path:line`; deferred follow-ups,
each captured as a separate issue when applicable; residual risk in one or two
sentences (omit if none). Use neutral labels ("Implementation review", "Second
independent review", "Operator review") and treat it as a verification record, not
a certification.
```

## Fast Fix

```text
Run fast-fix kickoff for <bug/maintenance item>.

Allowed only if no schema/API/security/dependency/toolchain/state-machine change is
needed. If scope grows, switch to normal task mode.

Deliver:
1. tiny scope statement
2. changed files
3. targeted verification
4. PR/commit summary
```

## Post-Plan Grill

```text
Grill this plan for execution risk, hidden edge cases, sequencing problems, and
verification gaps. Ask one question at a time and recommend an answer for each. Stop
when the remaining risk is named and manageable.
```
