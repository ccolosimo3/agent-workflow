# Review Rubric

The standing operating manual for a code-review (implreview) or re-review
(implrereview) pass. The Review Kickoff / Re-Review Kickoff in `KICKOFFS.md` carry
only the per-task Context and point here, so the emitted prompt stays short. Read
this in full before issuing any verdict, and return every item in the Output
contract. This is repo-agnostic; the repo-specific doc paths under "Required
reading" are injected by the review skill or resolved by you.

## Stance

Review adversarially, then report honestly. Your job is to find the problems in
this diff before a human reviewer does, not to confirm the implementer's framing.
Run these checks explicitly and cite what you found:

- For each change: what is the cheapest way this is wrong, weak, or out of scope,
  and did I actually look at the code that would show it? Unrequested
  component/library/contract swaps are out of scope — see the Scope-vs-intent &
  contract-identity check below.
- For each new or changed test: try to construct a regression the test would NOT
  catch. If you can name one (revert the fix, narrow it to one column, make the
  down-path lossy, swap the component but keep the testid), the test is weak — call
  it out.

Reporting rule: do not invent findings to look thorough. APPROVED with no findings
is a valid outcome — but only state it after listing the specific adversarial
checks above and noting they came back clean. A clean approval with no checks named
is not acceptable.

## The Context block is a CLAIM, not ground truth

The Context block in the kickoff is the implementer's orientation and CLAIM — it is
itself part of what you are reviewing. The diff and the repo are the source of
truth; where the Context and the diff disagree, the diff wins and the discrepancy
is a finding. Treat every line — summary, scope, verification numbers, Hot spots,
and ESPECIALLY the
Test-quality self-report — as a claim to confirm or refute against the changed
lines you actually read. Assume the most important problem is something the
implementer did NOT list as a hot spot, including a component/contract/behavior
change the summary frames as mere polish. Where a claim cannot be confirmed from
code you read, mark it unverified.

## Required reading (load BEFORE judging any test or convention question; do not review from memory)

The skill injects the exact existing paths under "Repo conventions to enforce"; if
it did not, resolve them yourself:

- testing — `~/.agents/workflow/TESTING.md` owns Part 1 (principles) + Part 2
  (universal anti-patterns); apply both, then the repo's own stack section in its
  testing reference (resolved via the repo shim, e.g.
  `plans/reference/testing-philosophy.md`), which names the canonical example files
  and coverage authority for that stack. Use the anti-pattern tables and 10-second
  check as your test rubric.
- frontend/design — for any UI surface in the diff, `~/.agents/workflow/FRONTEND.md`
  owns the cross-repo principles (the oracle, token-sourced values, the state set,
  the accessibility contract, layout stability); apply it plus the repo's own
  design system (resolved via the shim).
- coding-standards / patterns and verification policy — resolved per repo from
  its shim; the paths below are an illustrative example of shim routing from one
  operator's repos — your repo's shim names its own equivalents. The rule the
  patterns doc enforces: hand-rolled code that duplicates a documented repo
  primitive (e.g. a custom shimmer where the repo mandates the existing loading
  primitive) is convention drift.
  - coding-standards / patterns — townchest:
    `.agent-workflow/plans/reference/coding-standards.md`; clearsnake-mobile:
    `mobile/CLAUDE.md`.
  - verification policy — townchest:
    `.agent-workflow/plans/reference/verification.md` (single owner of
    surface->command routing + false-confidence traps;
    `townchest-pr-checklist.md` is a secondary PR-readiness doc);
    clearsnake-mobile: `mobile/VERIFICATION.md`.

If you cannot open a doc in this environment, say so explicitly and fall back to
the kernel "Test Quality Floor" anti-pattern list — do not silently skip this. Cite
the specific rule (file + section) any conformance or test-quality finding
violates; if no documented rule covers it, do not raise it as ACTIONABLE convention
drift.

## Required investigation (an APPROVED that skips any of these is not a valid review)

(a) Open the source issue/spec at the link in Context section 1 and re-derive the
    acceptance criteria yourself; treat the copied bullets and the Implementer
    summary as claims to check, not as ground truth.
(b) Read the actual changed lines via `git diff <base>..<tip>` (the range in
    Context section 1). You may not approve a file you did not open.
(c) For any UI or component change, run the full identity + masking check in the
    Scope-vs-intent & contract-identity section below.
(d) Open each new or changed test file yourself and judge it against the
    Test-quality rules below and `~/.agents/workflow/TESTING.md`; do not rely on
    the implementer's self-report.
(e) For a migration, persistence, data-loss, or contract change, confirm the proof
    exercised the real operation — apply the migration bar under "Surface-specific
    test bars"; if that proof was not run, raise it or mark it `[decision-required]`.
(f) For each exported symbol the diff changes, removes, or renames, `git grep` its
    references repo-wide and account for every one: a caller left on the old shape is
    a regression; a symbol with no remaining non-test consumer is dead code to flag
    per the repo's deprecation convention; a type or test that should have moved with
    it is a gap. Reading only the changed file hides all three.

## Scope-vs-intent & contract-identity check (run BEFORE issuing any verdict)

1. Re-read the ORIGINAL operator request in Context field 2a — the raw ask, not the
   ACs. Compare the diff to THAT. Acceptance criteria can be technically satisfied
   while the implementer met them by SUBSTITUTING an approach the request never
   named: swapping a component, library, framework primitive, element type,
   algorithm, data path, or dependency. A polish / perf / copy / styling ask (e.g.
   "stronger shimmer on the skeleton") does NOT authorize a component,
   public-contract, dependency, or accessibility-semantics change. If 2a is missing,
   vague, or looks reverse-engineered to fit the diff, take the narrowest reasonable
   reading as the authorized scope. Flag any unrequested substitution
   `[decision-required]` even when the ACs pass.
2. Identity diff. For each component / element / exported symbol whose identity the
   diff CHANGES, write before -> after for: rendered component / element TYPE (e.g.
   <Skeleton> -> <Box>); public function / prop / return signature, or exported
   name; HTTP / GraphQL / schema shape; accessibility role or semantics gained or
   lost (loading / aria / disabled / focus). Report only CHANGED identities; you
   need not catalog unchanged ones. A changed identity the work item did not request
   is at minimum `[high]`/`[decision-required]`, and ACTIONABLE if it alters
   behavior, accessibility, or a downstream contract.
3. Masking check. A preserved `data-testid`, prop name, route, class name, or
   exported name over a changed component/contract is a MASKED swap, not
   reassurance. Name the existing test that SHOULD have gone red for this change and
   did not, and raise the missing assertion as a `[test quality]` finding.

Do not fire on cosmetic in-place edits that preserve the component TYPE, signature,
and contract (tweaking a prop value, className, or animation duration on the SAME
component) — those are in-scope refinements, not substitutions.

## Surface-specific test bars (ACTIONABLE if a bar is unmet)

- Migration / schema / custom-field / persisted-field change: the behavior MUST be
  proven through the real import/service/repository path with a save + reload
  (re-fetch the entity and assert the reloaded value), PLUS a named Tier-4 proof
  (e.g. local-Postgres `migrate:run`; for mobile, a store rehydrate). A test that
  mocks `queryRunner.query` and asserts literal SQL strings, asserts a
  custom-field/config constant value, or only proves `migration.up()/down()` were
  called is NOT sufficient on its own — supplemental at best, ACTIONABLE as the sole
  proof. Any lossy or narrowing down-migration (USING clauses, type narrowings) MUST
  carry a reload-after-down assertion proving no silent data loss.
- Component / UI / contract change: first run the authorization + masking check in
  the Scope-vs-intent & contract-identity section. Test bar: the change MUST be
  covered by a test that asserts user-visible behavior through a real
  render+interaction and would fail on the swap; a preserved `data-testid` that lets
  an existing test still pass does NOT count as coverage.

Also flag tests that would not fail for the intended regression, assert
implementation shape only, or create false confidence without a behavior-level/
manual proof.

## Automated-reviewer awareness

If the repo runs an automated PR reviewer (e.g. CodeRabbit via `.coderabbit.yaml`),
check its `path_filters` for EXCLUDED paths — typically migrations and generated
files. On any excluded path you are the ONLY reviewer of that surface: read the diff
line by line and apply the migration bar above. For surfaces the automated reviewer
DOES cover, read its posted comments first and do not re-litigate its mechanical/
lint findings; this does NOT exempt those surfaces from your correctness,
contract/intent, and test-quality review. The repo shim names the concrete excluded
paths.

## Time-sensitive & external claims (verify, don't assert from memory)

**Web search is available to you — use it.** When a finding hinges on a dated
external fact (deprecation, a "current"/"best-practice" pattern, version-specific
behavior, an API/library's present behavior, a CVE) — or when your own review
angle rests on external or current knowledge — corroborate it before you assert:
check the repo's pinned version (package.json / lockfile) and repo-bundled SME/doc
skills, then official upstream docs/changelog via web search, and cite the source +
date you checked. Don't flag OR clear a dated claim from memory. If your host has
no web search, say so and treat the dated claim as a non-blocking note, not
ACTIONABLE.

## Output contract (your Return, in order)

0. Coverage confirmations, both REQUIRED:
   (a) Diff coverage: confirm you ran `git diff <base>..<tip>` and reviewed the full
       diff; list any changed file you did NOT open and why — normally empty; if you
       cannot account for every changed file, the review is incomplete, say so.
   (b) Acceptance-criteria ledger: one row per AC (re-derived in Required
       investigation (a)) — AC | met / not met / deferred | the diff evidence or the
       gap. A "not met" AC is a `[high]` finding; a silently dropped requirement is
       what this ledger exists to surface.
1. Per-test ledger (REQUIRED — one row for EACH added or changed test that carries
   an assertion; quote the key assertion you inspected):
   test name/path | real boundary it drives (service / import / job / API route /
   component render+interaction / hook state machine / store rehydrate / parser / DB
   save+reload) | the exact regression that turns it RED on revert |
   10-second-check PASS/FAIL | anti-pattern row matched, if any (else "none") |
   inclusion disposition (ship / trim / redundant-with-<test> / one-off-proof->pocket)
2. Test-quality sub-verdict (MANDATORY, separate line): PASS or FAIL. Mark FAIL if
   any row is a 10-second-check FAIL, matches a "delete on sight" row, or asserts
   implementation shape (config constant, generated-SQL string, file/class/migration
   existence, "mock was called", snapshot with no behavioral assertion) AS ITS SOLE
   PROOF. Do NOT FAIL a shape-only test when the diff or PR explicitly justifies it
   as clearly-supplemental to a behavior/Tier-4 proof, or when that exact shape IS
   the contract — in that case write the row as PASS and name the complementing
   proof. A FAIL here forces the overall verdict to ACTIONABLE.

Inclusion disposition (a SECOND axis, separate from PASS/FAIL — a test can be a
10-second-check PASS and still not be worth shipping). For each ledger row, judge
whether the test belongs in the PR's permanent suite and record one of
ship / trim / redundant-with-<test> / one-off-proof->pocket; the disposition
definitions live in `~/.agents/workflow/TESTING.md` ("Inclusion: should this
test ship?"). Any row whose disposition is not "ship" is a valid-but-marginal
inclusion call: raise it in Findings as `[decision-required]` (low/medium
severity, NOT a quality FAIL) with your recommendation, so the OPERATOR makes
the final include/exclude decision. Do NOT silently delete a working test and
do NOT auto-FAIL it for worth — disposition is about worth; the sub-verdict
above is about weakness; keep them separate.

3. Overall verdict: APPROVED or ACTIONABLE (cannot be APPROVED while line 2 is FAIL,
   while a Required-investigation step was skipped, or while an unresolved
   `[decision-required]` blocking finding remains).
4. Findings: [severity] path:line | category | issue | impact | required fix.
   Severity rubric — verdict is ACTIONABLE if any finding is medium or higher. A
   finding in these classes may NOT be filed as low/nit or moved into a non-blocking
   bucket ("Residual risk or testing gaps") to preserve APPROVED:
   - critical: data loss/corruption, security, or a migration/schema change that can
     silently truncate or corrupt persisted data (e.g. a lossy down-migration USING
     clause).
   - high: the diff SUBSTITUTES an existing public contract, exported symbol,
     component type, schema/field, or library/primitive for a different one the task
     did not ask to change (altering accessibility or framework semantics); OR a
     changed behavior's only test is a delete-on-sight anti-pattern; OR a stated
     acceptance criterion is not actually met. (Net-new code that ADDS a
     component/primitive without replacing an existing one is not automatically
     high — judge it on correctness and coverage.)
   - medium: a test that fails the 10-second check or asserts implementation shape
     only with no real operation boundary; OR a risk-bearing new/changed branch,
     failure path, or persisted field that ships with no test at all.
   - low: maintainability/naming/doc nits with no behavioral or contract impact.
   If unsure whether a finding is medium-or-higher, treat it as blocking. If
   genuinely none, write "none found".
5. Verification notes. Do not rerun broad verification already reported green
   unless the diff makes that evidence suspect.
6. Convention conformance: for UI/component/loading-state/library/style surfaces in
   the diff (and any surface a documented repo primitive, wrapper, hook, or helper
   plausibly covers), does the change reuse that existing primitive and match
   documented naming/placement/style patterns? Flag hand-rolled code that duplicates
   an existing primitive — e.g. a custom shimmer where the repo's Skeleton/loading
   primitive exists — as ACTIONABLE "convention drift", citing the violated rule.
   For UI surfaces also apply `~/.agents/workflow/FRONTEND.md` — states built and
   proven, the a11y contract (keyboard + name/role/state), contrast / use-of-color,
   layout stability, and composition (hierarchy/density/alignment/hostile-data/
   responsive); a broken state/a11y/contrast is ACTIONABLE. Scope visual evidence to
   the work: for visual-design work (building/recomposing a screen/dashboard/
   component's look) the reviewer VIEWS the render itself — captures it via the
   host's fast tool, or reads the geometry story — and JUDGES composition (not a
   presence check on the implementer's artifact); raise weak composition, an
   unverified hostile-data/responsive state, or a width/padding/spacing change not
   re-checked against the WHOLE surface as a challengeable finding: low /
   non-blocking, exempt from the treat-as-blocking-when-unsure default — don't
   manufacture taste nits where the surface reads cleanly. For incidental UI (a
   copy/prop/behavior tweak) do NOT flag a missing screenshot.
   Skip the primitive-reuse check only when the diff touches no surface a
   documented primitive covers; still apply the FRONTEND.md half whenever the diff
   renders UI, even where the repo documents no primitive — the
   a11y/contrast/state/layout/composition principles are repo-independent.
7. Residual risk or testing gaps.

## Decision-required handling

When Verdict is ACTIONABLE, mark any finding that requires operator input (scope
change, contract decision, ambiguous spec interpretation) with `[decision-required]`
in its required fix. `[decision-required]` is a routing tag, not a downgrade: the
finding keeps its real severity and the verdict stays ACTIONABLE. It may NOT be used
to park a data-loss, contract-drift, unrequested-component/dependency-swap, or
failed-10-second-check finding — those stay blocking and are resolved by the
OPERATOR, not skipped by the implementer. Append this implementer directive verbatim
at the end of your output so it stays with the findings when the operator forwards
them:

> Implementer: patch every finding autonomously. For any finding marked
> `[decision-required]`, skip the patch, summarize the decision needed, and return
> to the operator. An unresolved `[decision-required]` finding is an open ACTIONABLE
> item — it blocks PR handoff under the kernel's "Implementation Completion
> Handoff" requirement (two independent approved review verdicts before PR
> handoff by default) until the operator resolves it. Do not block other
> patches on those.

## After the verdict

If Verdict is ACTIONABLE, return findings and stop. The implementer patches and
hands back to the operator; no second review cycle from this reviewer.

## Re-review mode (implrereview)

When invoked for a re-review — a prior ACTIONABLE verdict whose findings were
patched — your scope narrows to the changed lines and the prior findings; do NOT
perform a fresh broad review. Still apply Required reading (a reused reviewer
already holds it; a fresh fallback loads it first) and the test-quality, masking,
consumer/orphan-sweep (Required investigation (f)), and decision-required rules
above to what changed — a patch that renames or removes a
symbol still needs the reference sweep. Use the
Re-Review Kickoff's Return shape (per-finding status / regressions / new issues /
verdict), not the full Output contract. A prior weak/false-confidence-test finding
is "addressed" ONLY if the new or edited test exercises the real operation boundary
and would go RED when the original regression returns — a reverse-tautology patch
(editing an expected constant, SQL string, file/class existence, or snapshot to
match the new code) does NOT resolve it. An unresolved `[decision-required]` finding
is OUTSTANDING, not addressed, and keeps the verdict ACTIONABLE.
