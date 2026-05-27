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
6. exact verification plan
7. issue/ticket-ready markdown
8. decision brief: chosen approach, one rejected alternative, tradeoff, assumptions
```

## Domain Pass

```text
Run a domain pass on <feature/plan>.

Challenge terminology against current repo language and code. Resolve canonical terms,
flag overloaded words, update/prepare CONTEXT.md entries when terms are settled, and
suggest an ADR only if the decision is hard to reverse, surprising without context, and
based on a real trade-off.
```

## Issue Draft Kickoff

```text
Draft an issue from approved spec <path or link> for repo <repo>.

Output: a single markdown file under plans/<topic>/issues/*.md (or local equivalent) that can land verbatim as a GitHub issue body via `gh issue create`.

Pre-promotion review (recommended for non-trivial specs): before drafting the issue body, spawn a fresh-context reviewer agent against the source spec. The reviewer validates scope coverage, file/line claim accuracy, label correctness against the repo's label set (`gh label list --repo <repo>`), self-containment of the eventual issue body, and dependency claims. Apply review feedback to the spec before drafting. This catches stale paths, missed scope, mislabeled categories, and assumed-but-wrong code claims at the cheapest possible point.

Structure (required unless marked optional, in this order):

# <Title Case, action-verb start, no leading [tag]; taxonomy lives in Type below>

## Metadata
- Type: <Polish / Perf / Migration / Hygiene / Verification slice / ...>
- Labels: <platform + subsystem + workstream + work-type labels from the local shim's label set>
- (optional) Priority: <P0|P1>
- Execution mode: <build paths allowed; explicit guardrails on remote/EAS builds; manual gates>
- Suggested branch: `<task|fix|chore>/<topic-slug>`
- Source spec: `<plans/.../rough-spec.md>`
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
```

## Plan Review Kickoff

```text
Review plan / spec / issue draft <path or link> for <feature/workstream>.

Context (filled by planner; reviewer treats this as the source of truth for what to validate against):

1. Plan artifact
   - path or link: <url or path>
   - artifact type: <rough-spec | issue-draft | other planning markdown>
   - intended downstream action: <gh issue create | implementation kickoff | other>
   - target repo (if filing an issue): <repo>
   - target labels (if filing an issue): <comma-separated; pulled from `gh label list --repo <repo>`>

2. Planner summary (2-3 sentences)
   <what the plan delivers and why>

3. Source material
   - upstream spec / rough-spec (if reviewing a derived artifact): <path>
   - related issues, ADRs, prior discussion: <urls or paths>
   - touched modules / files claimed in scope: <paths>

4. Scope coverage
   - intended in-scope items: <bullets>
   - intentional out-of-scope items: <bullets + reason>
   - dependency / ordering claims: <"blocks #X" / "blocked by #Y" / "ordered after #Z">

5. Hot spots / known risk in the plan
   - <ambiguous areas; claims the reviewer should fact-check against the code>
   - <decisions made and rejected alternatives>

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
3. Notes on scope or framing improvements (non-blocking but useful)

When Verdict is ACTIONABLE, mark any finding requiring operator input (scope change, contract decision, label policy interpretation) with `[decision-required]` in its required fix. Append this planner directive verbatim at the end of your output so it stays with the findings when the operator forwards them:

> Planner: address every finding autonomously. For any finding marked `[decision-required]`, skip the revision, summarize the decision needed, and return to the operator. Do not block other revisions on those.

Focus on whether the plan is correct, complete, and self-contained enough to be acted on. Do not write the implementation. Do not propose new scope unless it closes a coverage gap the plan claims to cover.

If Verdict is ACTIONABLE, return findings and stop. The planner revises and hands back to the operator; no second review cycle from this reviewer.
```

## Plan Re-Review Kickoff

```text
Re-review plan / spec / issue draft <path> after revisions following a prior ACTIONABLE plan review.

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
2. restate goal, non-goals, acceptance criteria, and verification commands
3. identify files in scope and out of scope
4. create/switch to the team-standard branch if edits are expected
5. implement minimally; if mode=gated, pause for operator review after step 2 and after first Tier 1 verification
6. run verification by tier
7. summarize changes and verification
8. hand the operator a populated Review Kickoff prompt as a required completion
   artifact:
   a. Produce one Review Kickoff with all context blocks pre-populated from this session (see Review Kickoff template).
   b. Emit the full populated prompt in chat verbatim under `Review Kickoff Prompt` before spawning any reviewer subagent.
   c. Treat the implementation summary as incomplete until that prompt has been shown to the operator in chat. Do not wait until the reviewer has completed to show it.
9. obtain two independent fresh-context review verdicts. Do not stop after
   producing the prompt:
   a. After the `Review Kickoff Prompt` is visible in chat, spawn exactly one fresh-context reviewer agent with that exact prompt, or with one focused variant if the work item needs a specific review angle. Announce "spawning one reviewer" so the operator sees the handoff.
   b. Tell the operator that the same `Review Kickoff Prompt` is for their second independent reviewer. The implementer must not spawn a second reviewer unless the operator explicitly asks in the current session.
   c. Wait for both verdicts before PR handoff: one from the implementer-spawned reviewer and one supplied by the operator from their separately launched reviewer. If the operator waives or defers the second review, record that explicitly before continuing.
   Step 9 is complete only after the implementer-spawned reviewer verdict is in hand and the operator has either supplied the second verdict or explicitly waived/deferred it. Emitting the prompt without spawning one reviewer is not a valid completion state.
10. on ACTIONABLE verdict: patch listed findings, rerun targeted verification,
   post a brief patch summary, then run another fresh-context review pass when
   the patch is non-trivial, touches lifecycle/state/concurrency, changes
   acceptance behavior, or the operator asks for another pass.
11. before PR authorization, prepare both PR handoff artifacts:
   a. PR body file.
   b. PR review-summary comment file using the PR Review Comment template below.
   Show both artifacts to the operator.
12. open/update PR only when authorized; use `Fixes #<issue>` in the PR body
   only when the PR fully resolves the source issue. Use `Refs #<issue>` or
   `Part of #<issue>` for partial phases, validation-only slices, or follow-up
   work that should not close the issue on merge. Before asking for PR
   authorization, fetch the source issue labels, filter them through the local
   label policy, and state which labels will be applied to the PR. Carry issue
   labels onto the PR only when those labels still describe the diff; omit stale
   status labels or subsystem labels that do not describe the PR. Apply the
   selected labels during `gh pr create` or immediately after PR creation with
   `gh pr edit --add-label`, after stating the exact command and getting
   approval. Git Bash label recipe:
   gh issue view <issue> --repo Enbasis/clearsnake-mobile --json labels --jq '.labels[].name'
   gh pr edit <pr> --repo Enbasis/clearsnake-mobile --add-label "<comma-separated labels that still apply>"
13. after the PR exists, post the prepared review-cycle summary comment under
   the PR with `gh pr comment <pr> --repo <repo> --body-file <comment-file>` or
   an equivalent `gh` command after stating the exact command and getting
   approval for that externally visible mutation.

Scope-creep guard:
- If you discover work outside the original acceptance criteria, do not expand silently. List it under "discovered follow-ups" in the Review Kickoff so the operator can capture it as a separate issue.
```

## Review Kickoff

```text
Review work item <id/link> / PR <id/link> / branch <branch> against <base>.

Context (filled by implementer; reviewer treats this as the source of truth for what to verify against):

1. Work item
   - issue/spec link: <url or path>
   - acceptance criteria, copied inline:
     - [ ] <AC bullet>
     - [ ] <AC bullet>

2. Implementer summary (2-3 sentences)
   <what changed and why>

3. Scope
   - in scope, files touched: <paths>
   - out of scope, noticed but intentionally not touched: <items + reason>
   - discovered follow-ups: <items, to be captured as separate issues>

4. Verification run
   - <command>: <one-line result with a useful number, e.g. "typecheck: 0 errors across 412 files">
   - <command>: <...>

5. Hot spots / known risk
   - <areas wanting extra review attention>
   - <deviations from spec or assumptions made>

6. Tier 4 gate
   - required: yes/no
   - if yes, what: <manual QA / hardware / live provider, and who runs it>

Return:
1. Verdict: APPROVED or ACTIONABLE
2. Findings if ACTIONABLE: [severity] path:line | category | issue | impact | required fix
3. Verification notes
4. Residual risk or testing gaps

When Verdict is ACTIONABLE, mark any finding that requires operator input (scope change, contract decision, ambiguous spec interpretation) with `[decision-required]` in its required fix. Append this implementer directive verbatim at the end of your output so it stays with the findings when the operator forwards them:

> Implementer: patch every finding autonomously. For any finding marked `[decision-required]`, skip the patch, summarize the decision needed, and return to the operator. Do not block other patches on those.

Focus on correctness, regressions, contract drift, state/failure behavior, security,
data loss, and missing tests/docs. Do not rerun broad verification already reported
green unless the diff makes that evidence suspect.

If Verdict is ACTIONABLE, return findings and stop. The implementer patches and hands back to the operator; no second review cycle from this reviewer.
```

## Re-Review Kickoff

```text
Re-review work item <id/link> / PR <id/link> / branch <branch> against <base>.

## Prior review
- verdict: ACTIONABLE
- source kickoff: <pointer/quote of original Review Kickoff if present>
- findings (restated verbatim from prior reviewer):
  - [severity] path:line | category | issue | impact | required fix
  - ...

## Patches applied since the prior review
- base: <commit sha>
- tip: <commit sha>
- commits:
  - <sha> <subject>
  - ...
- diff stat: <verbatim output of `git diff --stat <base>..HEAD`>
- implementer notes (if any): <summary of how each finding was patched>

## Verify
Return:
1. Per-finding status: for each prior finding, "addressed" or "not addressed" with `path:line` evidence in the new code. If `[decision-required]` was on a finding, the implementer may have skipped it — note that and do not mark it not addressed.
2. Regressions: any behavior the patches broke that worked under the prior reviewed state.
3. New issues: anything surfaced in the changed lines that wasn't a prior finding (correctness, regression, contract drift, state/failure behavior, security, data loss, missing tests/docs).
4. Verdict: APPROVED or ACTIONABLE.

When Verdict is ACTIONABLE, mark any finding requiring operator input (scope change, contract decision, ambiguous spec interpretation) with `[decision-required]` in its required fix. Append this implementer directive verbatim at the end of your output:

> Implementer: patch every finding autonomously. For any finding marked `[decision-required]`, skip the patch, summarize the decision needed, and return to the operator. Do not block other patches on those.

Focus on the changed lines and the prior findings. Do not rerun broad verification already reported green unless the patch makes that evidence suspect.

If Verdict is ACTIONABLE, return findings and stop. The implementer patches and hands back to the operator; no second review cycle from this reviewer.
```

## PR Review Comment

```text
Compose a PR review-cycle summary comment spanning the full review cycle for work item <id/link> / PR <id/link>.

Source material:
- populated Review Kickoff prompt(s)
- reviewer verdict(s)
- findings patched in this implementation
- final verification run after patching
- deferred follow-ups and residual risk

Cover:
- initial implementation outcome
- any review findings and how they were resolved
- follow-ups discovered but intentionally not done here

Format (keep under ~150 words after the heading):
1. Start with this exact heading on the first line: `# Review Summary`
2. Verdicts (APPROVED) — one line naming both independent reviews
3. Scope recap — one sentence
4. Findings patched in this PR — bullet list, brief description with `path:line`
5. Follow-ups deferred — bullet list, each captured as a separate issue (note issue link if filed)
6. Residual risk — one or two sentences, omit if none

Constraints:
- plain `path:line`, no markdown file links (GitHub does not resolve them in PR comments)
- factual and concise, no marketing tone
- if no findings were patched or no follow-ups remain, omit those sections entirely rather than write "None"
- return the comment body only, no preamble like "here is the comment"
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
