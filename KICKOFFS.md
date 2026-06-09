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

Publication approval: before running `gh issue create` or `gh issue edit`, show
the final issue body or requested edit, labels, repo, target issue when editing,
and requested issue action. If the operator has already said `ISSUE-GO` or a
natural equivalent such as "approved, create the issue" or "approved, edit the
issue" after seeing that prepared packet, derive the matching `gh` command,
state it immediately before running it, and run it without asking for another
approval. Ask again if the repo, issue target, title, body, labels, milestone,
assignee, or edit changed materially.

Lifecycle:
- Start with `status: rough`.
- Move to `status: review-ready` only when the spec is coherent AND its
  load-bearing code claims (paths, identifiers, behavior-parity claims) have been
  grounded against current code with file:line evidence; log any claim you could
  not ground as an open question rather than asserting it.
- Move to `status: final` only after review findings are addressed and the operator approves promotion.
- Move to `status: promoted` after `gh issue create` succeeds and add the issue URL.
- Keep the same living spec active after issue creation until implementation
  lands. After implementation, move to `status: implemented`, delete the
  one-off spec, or archive durable context according to the local repo cleanup
  policy.

Structure (required unless marked optional, in this order):

# <Title Case, action-verb start, no leading [tag]; taxonomy lives in Type below>

## Metadata
- Type: <Polish / Perf / Migration / Hygiene / Verification slice / ...>
- Labels: <platform + subsystem + workstream + work-type labels from the local shim's label set>
- (optional) Priority: <P0|P1>
- Execution mode: <build paths allowed; explicit guardrails on remote/EAS builds; manual gates>
- Suggested branch: `<task|fix|chore>/<topic-slug>`
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

5. Hot spots / known risk in the plan
   - <ambiguous areas; claims the reviewer should fact-check against the code>
   - <decisions made and rejected alternatives>

6. Test strategy quality (planner's CLAIM — verify against the repo testing doc; do NOT accept these bullets)
   - behavior/failure mode each planned test protects: <bullets>
   - real operation boundary planned for tests: <service/API/job/UI/persistence/etc.>
   - implementation-shape tests, if any, and why that shape is contractual or supplemental:
   - manual/Tier 4 proof needed when automation cannot represent the failure mode:

Return:
1. Verdict: APPROVED or ACTIONABLE
2. Findings if ACTIONABLE: [severity] section-or-line | category | issue | required fix
   Validation categories (focus, not exhaustive):
   - scope coverage gaps (missing acceptance criteria, undefined non-goals)
   - file/line claim accuracy (do paths claimed in scope exist; do referenced symbols exist)
   - label correctness against the repo's actual label set
   - self-containment of an issue body (would this issue be actionable to someone with no prior context)
   - dependency claims (do blocked/ordered-after references point at real issues with the claimed state)
   - ambiguous terminology or undefined nouns
   - missing or untestable acceptance criteria
   - missing or wrong verification commands
   - weak test strategy: BEFORE judging, open this repo's testing-philosophy.md
     (townchest: `.agent-workflow/plans/reference/testing-philosophy.md`;
     clearsnake: `plans/reference/testing-philosophy.md`) and apply its
     anti-pattern table + 10-second check to each PLANNED test. Flag ACTIONABLE
     any planned test that, as described, would only assert a constant/config
     value, a generated-SQL string, "a mock was called", or that a
     class/migration/file exists — or that would still pass if the fix were
     reverted. For any planned migration/schema/persisted-field change, the spec
     must plan a real import/service/repository save+reload test PLUS a named
     Tier-4 proof (e.g. local-Postgres `migrate:run`, store rehydrate); a spec
     that plans only SQL-string or config-value assertions, or only "add a
     migration test", is a blocking finding at plan time.
   - convention conformance: if any plan step explicitly proposes hand-rolling a
     component, helper, hook, loading state, or style primitive, open this repo's
     patterns doc (townchest:
     `.agent-workflow/plans/reference/coding-standards.md`; clearsnake:
     `mobile/CLAUDE.md`) and flag ACTIONABLE if the repo already has an
     established primitive for it (e.g. a custom Box/@keyframes shimmer where the
     repo mandates the existing Skeleton/loading primitive). Do not flag steps
     that reuse existing primitives or where no repo primitive is documented.
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

Mode: <task|gated|fast>  # inherit from planning if known

Then execute end-to-end:
1. read the work item and local repo shim
2. restate goal, non-goals, acceptance criteria, and verification routing:
   Tier 1 loop checks, Tier 3/PR-parity gates, any broader local gates selected
   for this task, and any available broader gates intentionally not selected.
   Before editing, spot-check the spec's load-bearing source claims (cited
   file:line wiring points and referenced symbols) against the current tree; if a
   claimed path has moved, no longer exists, or the code already contradicts a spec
   assumption, surface the conflict to the operator and adjust scope instead of
   coding against the stale claim.
3. identify files in scope and out of scope
4. identify any approval-gated commands before running them, including
   destructive local data operations, provider mutations, live migrations,
   externally visible tracker/PR actions, dependency/toolchain changes, and
   commands that use staging or production credentials
5. check `git status` first; never build on a dirty tree or discard unowned
   changes, and confirm the intended base branch before you create/switch to the
   team-standard branch (when edits are expected)
6. implement minimally; if mode=gated, pause for operator review after step 2 and after first Tier 1 verification. If you write a test purely to verify a one-time repair (static asset, config, or data fix) with no ongoing regression surface a normal code change would hit, do NOT commit it to the suite — pocket it to the work-item `artifacts/` (or record a Tier-4 note) and disclose it in the Review Kickoff test-quality block for the operator to confirm
7. run verification by tier. Use local repo commands for the selected level of
   verification; run build, contract, e2e, visual/manual QA, local-stack QA, or
   other broader gates when the touched surface or operator request justifies
   them. Tie tier selection to the changed SURFACE, not to convenience: if the diff
   touches a surface that the repo's verification doc (clearsnake
   mobile/VERIFICATION.md, townchest AGENTS.local.md) names a broader gate for —
   migration/schema/persisted state, native config, routing, auth, or a contract
   surface — that named gate is REQUIRED, and "Tier 1 sufficient" is not a valid
   record for it. If a broader local gate is available but not selected, name the
   surface you changed and why no surface-triggered gate applies; if a gate is
   blocked, record the exact blocker.
8. summarize changes and verification. Reconcile the summary against your terminal
   history: claim a gate passed only if it actually ran in this session/branch, and
   report each as a real result (the per-command number goes in Review Kickoff
   section 4). Mark any gate you did not run as not-run (with its reason/blocker or
   as CI-owned) — never as passing. State an explicit docs-impact decision in that
   summary per the Docs Impact Check — either `Docs impact: none` or the updated
   tracked-doc path. Then commit the implementation on the branch (a real commit,
   no push, no amend) and record the review range `<base>..<tip>` (base =
   merge-base with the target branch, tip = HEAD) so reviewers diff a stable range
   from git instead of a pasted file list.
9. hand the operator a populated Review Kickoff prompt as a required completion
   artifact:
   a. Produce one Review Kickoff with all context blocks pre-populated from this session (see Review Kickoff template).
   b. Emit the full populated prompt in chat verbatim under `Review Kickoff Prompt` before spawning any reviewer subagent.
   c. Treat the implementation summary as incomplete until that prompt has been shown to the operator in chat. Do not wait until the reviewer has completed to show it.
10. obtain two independent fresh-context review verdicts. Do not stop after
   producing the prompt:
   a. After the `Review Kickoff Prompt` is visible in chat, spawn exactly one fresh-context reviewer agent with that exact prompt, or with one focused variant if the work item needs a specific review angle. Announce "spawning one reviewer" so the operator sees the handoff.
   b. Tell the operator that the same `Review Kickoff Prompt` is for their second independent reviewer. The implementer must not spawn a second reviewer unless the operator explicitly asks in the current session.
   c. Wait for both verdicts before PR handoff: one from the implementer-spawned reviewer and one supplied by the operator from their separately launched reviewer. If the operator waives or defers the second review, record that explicitly before continuing.
   Step 10 is complete only after the implementer-spawned reviewer verdict is in hand and the operator has either supplied the second verdict or explicitly waived/deferred it. Emitting the prompt without spawning one reviewer is not a valid completion state.
11. on ACTIONABLE verdict: patch listed findings, rerun targeted verification,
   post a brief patch summary, then run another fresh-context review pass
   (cjcrereview) when the patch is non-trivial, touches
   lifecycle/state/concurrency, changes acceptance behavior, rewrites/adds a test
   in response to a test-quality or weak-test finding, or the operator asks. You
   may skip the re-review only for a genuinely trivial patch with no behavior or
   test-assertion change (comment/whitespace/typo/rename/import), and only when
   you state that justification explicitly. A test-quality finding is NOT
   "addressed" on the implementer's say-so: the re-reviewer must confirm the new
   or rewritten test exercises the real operation boundary and goes RED when the
   fix is reverted. A reshaped test that still only asserts a config constant,
   generated-SQL text, file/class existence, or "mock was called" is NOT
   addressed. Commit each patch round as its own real commit (no amend) so the
   re-reviewer can diff `<prior-review-tip>..HEAD` — that range goes in the
   Re-Review Kickoff.
12. before PR authorization, prepare PR handoff artifacts:
   a. PR body file using `## Summary` and `## Verification` as default anchors.
      Add other sections when useful for review, such as Root Cause, Impact,
      Work Item, Screenshots, Visual QA, Docs Impact, Risks, Follow-ups, Notes,
      or Release Notes.
   b. Optional PR review-record comment file using the PR Body / Optional Review
      Notes template below only when the operator requests it.
   Show the PR body, any optional review-record comment artifact, the intended
   labels, and exact PR create/update, label, and optional PR comment commands.
13. open/update PR only when authorized; use `Fixes #<issue>` in the PR body
   only when the PR fully resolves the source issue. Use `Refs #<issue>` or
   `Part of #<issue>` for partial phases, validation-only slices, or follow-up
   work that should not close the issue on merge. Before asking for PR
   authorization, fetch the source issue labels, filter them through the local
   label policy, and state which labels will be applied to the PR. Carry issue
   labels onto the PR only when those labels still describe the diff; omit stale
   status labels or subsystem labels that do not describe the PR. Apply the
   selected labels during `gh pr create` or immediately after PR creation with
   `gh pr edit --add-label`. Git Bash label recipe:
   gh issue view <issue> --repo Enbasis/clearsnake-mobile --json labels --jq '.labels[].name'
   gh pr edit <pr> --repo Enbasis/clearsnake-mobile --add-label "<comma-separated labels that still apply>"
   If the operator has already said `PR-GO` or a natural equivalent such as
   "approved, open the PR" or "approved, edit the PR" after seeing or explicitly
   accepting the current PR body draft/file, final label list, repo, target
   branch for create or target PR for edit/update, optional comment body, and
   requested PR action, derive the matching `gh` command(s), state them
   immediately before running them, and run the PR-handoff packet without asking
   for another approval.
14. after the PR exists, post optional prepared review notes under the PR only
   when the operator requested them and the exact `gh pr comment <pr> --repo
   <repo> --body-file <comment-file>` command, or equivalent `gh` command, was
   covered by the same bundled approval before PR creation.

Scope-creep guard:
- If you discover work outside the original acceptance criteria, do not expand silently. List it under "discovered follow-ups" in the Review Kickoff so the operator can capture it as a separate issue.
- Scope creep includes SUBSTITUTION, not only addition. If you satisfied an acceptance criterion by swapping a component, library, framework primitive, algorithm, or data path the work item did not ask to change, disclose it in the Review Kickoff 'Hot spots' block as 'approach substitution: <old> -> <new>, not explicitly requested', and flag any preserved identifier (testid, route, key, public name) whose underlying implementation changed, since a preserved id can mask the swap from existing tests. An empty 'Hot spots' block is valid only after you have scanned the diff and confirmed no such substitution or masked-identifier case applies. A satisfied AC does not authorize an unrequested mechanism change.

Commit & history discipline:
- Commit freely on the branch during implementation and each review round (real
  commits, no amend) — granular history is what lets reviewers diff a precise
  range, and it does not reach mainline.
- Do NOT locally squash, rewrite, or force-push to "clean up" history before the
  PR. Both repos allow squash-merge: rely on GitHub squash-merge so mainline gets
  exactly one commit per PR while the branch keeps its review-round commits.
  (townchest's squash body defaults to the concatenated commit messages — keep
  commit subjects presentable, or set the PR's squash message at merge time.)
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

2a. Original operator request / intent (verbatim or close paraphrase)
   <the exact ask that triggered this work, e.g. "stronger shimmer on the
    skeleton"; if broader than the AC, say so>

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
   rubric's Test-quality rules + inclusion-disposition check and the repo
   testing-philosophy doc)
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

## Return
1. Per-finding status: for each prior finding, "addressed" / "not addressed" /
   "OUTSTANDING" (unresolved `[decision-required]`) with `path:line` evidence. A
   weak/false-confidence-test finding is "addressed" ONLY if the new or edited test
   exercises the real operation boundary and goes RED when the original regression
   returns; a reverse-tautology patch (editing a constant, SQL string, file/class
   existence, or snapshot to match the new code) does NOT resolve it. An unresolved
   `[decision-required]` stays OUTSTANDING and keeps the verdict ACTIONABLE.
2. Regressions: any behavior the patches broke that worked under the prior reviewed
   state.
3. New issues in the changed lines (correctness, contract drift, an unrequested
   component-type/contract/a11y substitution, weak/missing or false-confidence
   tests, a preserved testid/snapshot masking a changed implementation, missing
   docs).
4. Verdict: APPROVED or ACTIONABLE. When ACTIONABLE, mark operator-input findings
   `[decision-required]` and append the rubric's implementer directive.

If Verdict is ACTIONABLE, return findings and stop; no second review cycle from
this reviewer.
```

## PR Body / Optional Review Notes

```text
Compose PR handoff text for work item <id/link> / PR <id/link>.

Default placement: PR body only. Include `## Summary` and `## Verification` as
default anchors, but do not treat them as the only allowed sections. Add other
sections when useful for review, such as Root Cause, Impact, Work Item,
Screenshots, Visual QA, Docs Impact, Risks, Follow-ups, Notes, or Release Notes.
Do not include a standalone `## Review Summary` section by default. Use a
separate review-record PR comment only when the operator requests it.

Source material:
- populated Review Kickoff prompt(s)
- reviewer verdict(s)
- findings patched in this implementation
- final verification run after patching
- deferred follow-ups and residual risk

Cover:
- `## Summary`: what changed and why, in user-facing/product terms first
- `## Verification`: commands and manual QA actually run, plus any waived or
  blocked gates and any broader local gates considered but not selected
- additional sections when useful: Root Cause, Impact, Work Item, Screenshots,
  Visual QA, Docs Impact, Risks, Follow-ups, Notes, Release Notes, or
  repo-specific sections
- review findings only when they materially help the reviewer understand a
  patched edge case, deferred follow-up, residual risk, or unusual verification
  choice

Format:
1. For PR bodies, include `## Summary` and `## Verification` as anchors and add
   other useful sections as needed. Put material review-driven context in
   `## Notes` only when it explains a patched edge case, residual risk, or
   deferred follow-up.
2. For optional separate review-record comments, start with `# Review Notes`.
3. Scope recap — one sentence when useful.
4. For optional review-record comments, include findings patched in this PR as
   a brief bullet list with `path:line` when this helps the reviewer.
5. Follow-ups deferred — bullet list, each captured as a separate issue when
   applicable.
6. Residual risk — one or two sentences, omit if none.

Constraints:
- plain `path:line`, no markdown file links (GitHub does not resolve them in PR comments)
- factual and concise, no marketing tone
- treat optional review notes as a review/verification record, not a certification
- do not mention plan review by default; accepted implementation specs normally
  pass through plan review before coding
- use neutral labels such as "Implementation review", "Second independent
  review", and "Operator review"
- prefer "no remaining blocking issues found" over absolute claims like
  "approved", "fully safe", or "all issues resolved"
- if no findings were patched or no follow-ups remain, omit those sections entirely rather than write "None"
- return the PR body or optional comment body only, no preamble like "here is
  the summary"
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
