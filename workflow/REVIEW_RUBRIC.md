# Review Rubric

The standing operating manual for an implementation, outer-gate, or external-PR
code review and for an implementation re-review. The matching kickoff carries
only the per-task Context and points here, so the emitted prompt stays short. Read
this in full before issuing any verdict, and return every item in the Output
contract. This is repo-agnostic; the repo-specific doc paths under "Required
reading" are injected by the review skill or resolved by you.

## Stance

Review adversarially, then report honestly. Your job is to find the problems in
this diff before a human reviewer does, not to confirm the implementer's framing.
Run these checks explicitly and cite what you found:

- For each change: what is the cheapest way this is wrong, weak, or out of scope,
  and did I actually look at the code that would show it? Unrequested
  component/library/contract swaps are out of scope — see the Scope-vs-intent
  check and Contract-propagation audit below.
- For each added or changed current assertion, try to construct a durable
  regression it would NOT catch. For each deleted or relaxed assertion, try to
  construct a durable regression no remaining proof catches. If you can name one
  (revert the fix, narrow it to one column, make the down-path lossy, swap the
  component but keep the testid), call it out.

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
  its shim (`AGENTS.local.md` or the repo's CLAUDE/AGENTS adapter names them).
  The rule the patterns doc enforces: hand-rolled code that duplicates a
  documented repo primitive (e.g. a custom shimmer where the repo mandates the
  existing loading primitive) is convention drift.

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
(c) For any UI or component change, run the Scope-vs-intent check and full identity
    and masking pass in the Contract-propagation audit below.
(d) Open each test file with an added, changed, deleted, or relaxed assertion
    yourself (use the base version for deletions) and run the Behavior-proof audit
    below with `~/.agents/workflow/TESTING.md`; do not rely on the implementer's
    self-report.
(e) For a migration, persistence, data-loss, or contract change, confirm the proof
    exercised the real operation — apply the migration bar under "Surface-specific
    test bars"; if that proof was not run, raise it or mark it `[decision-required]`.
(f) For every changed exported/public identity or cross-boundary contract, run the
    Contract-propagation audit below. Reading only the changed file is invalid.
(g) CI workflow audit. For every added or changed workflow, reconstruct each
    changed job from a fresh runner and trace its relevant trigger and dependency
    paths through success, failure, skipped, and cancelled states. Verify that
    prerequisites are available before use—including repository files or local
    actions, tools and dependencies, working directories, artifacts and outputs,
    permissions, secrets, and environment values—and that `if`, `needs`, fallback,
    and `continue-on-error` behavior cannot skip or mask required work. Use safe
    execution or the narrowest targeted structural or ordering assertion where
    practical; leave provider-only execution as Tier 4. YAML validity and tests of
    invoked scripts alone do not prove workflow viability.
(h) For any changed code that parses, normalizes, groups, filters, allocates,
    falls back, or reduces input, run the Information-loss audit below even when
    the code is private and no exported/public or cross-boundary contract changed.

## Scope-vs-intent check (run BEFORE issuing any verdict)

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
2. Proportionality check. For each materially new abstraction, tool, configuration
   or persisted-state surface, fallback/recovery/compatibility path, or
   cross-package change, identify its current requirement, observed failure, or
   established repo pattern. If none exists, it is unjustified scope expansion.
   Do not flag line count or ordinary local implementation detail; any required
   fix must itself be the simplest complete correction.

Do not fire on cosmetic in-place edits that preserve the component TYPE, signature,
and contract (tweaking a prop value, className, or animation duration on the SAME
component) — those are in-scope refinements, not substitutions.

## Contract-propagation audit

For every changed exported/public identity or cross-boundary contract, record the
relevant before -> after identity and trace its definition or producer through every
affected consumer to observable behavior. Include rendered component/element type;
public name/signature/return shape; HTTP, GraphQL, schema, route, event, workflow
output, configuration, adapter, or persisted-field shape; and accessibility role or
semantics gained or lost. Report changed identities only.

Use repo-wide reference search for changed symbols and deliberately preserved
labels, plus the repository's actual producer/consumer mechanisms. Account for every
consumer and any caller left on the old shape, orphan, dead non-test export, stale
type/test, or inert compatibility path. A preserved symbol, route, prop, field,
class, test ID, or label over changed behavior is a masked change, not proof of
compatibility: name the behavioral test that should have failed and verify the new
contract at its real consumer boundary.

Apply this audit to public/exported identities, cross-boundary data shapes,
persisted contracts, and deliberately preserved compatibility labels—not private
local implementation details. Authorization remains governed by the Scope-vs-intent
check above.

## Information-loss audit

When changed code parses, normalizes, groups, filters, allocates, falls back, or
reduces input, identify which distinctions the resulting representation preserves
and discards. For every discarded distinction that could affect correctness,
policy, or uniqueness, construct the cheapest pair of inputs that become
indistinguishable and test the resulting behavior.

## Behavior-proof audit

For every added, changed, deleted, or relaxed assertion, identify the durable
regression and authority it protects, the observable outcome and real product
boundary it exercises, and whether restoring that regression makes the test fail.
A test that goes red only for a non-durable implementation detail still fails
quality. Treat implementation-shape checks as supplemental only when the exact
shape is contractual or a named real-boundary or Tier-4 proof carries the behavior.
When coverage is removed, confirm equivalent durable proof remains.

Apply `~/.agents/workflow/TESTING.md`'s anti-patterns, 10-second/durable-value
check, and independent inclusion axis. Preserve operator routing for every
non-`ship` disposition and use `[decision-required]` when durable authority or
inclusion is ambiguous; never silently delete a working test.

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
- Component / UI / contract change: the change MUST be covered by a test that
  asserts user-visible behavior through a real render+interaction and would fail
  on the swap.

## Automated-reviewer awareness

If automated-reviewer configuration exists (for example `.coderabbit.yaml`),
inspect its path exclusions before review and treat excluded changed surfaces as
lacking that automated coverage. Apply every relevant rubric method there; the
repo shim names any concrete exclusions.

For `/prreview`, defer reading the content of already-posted automated and human
comments until independent discovery is complete. Then use them to deduplicate,
confirm current status, and note material agreement or disagreement. Do not
duplicate mechanical findings, but independently assess correctness, contracts,
and test quality. Pre-PR reviews apply only the configuration check.

## Candidate admission and material-risk routing

Keep a candidate when the reviewed change introduced it, exposed or materially
increased the reachability or impact of an existing defect, left an in-scope
requirement unmet, or intentionally made an unauthorized scope or contract change;
and when it has a concrete supported or realistic path, a meaningful consequence
or applicable tracked rule, and one of: confirmed evidence, a credible material
mechanism remaining after the narrowest feasible validation, a genuine intent or
policy ambiguity affecting the outcome, or an objective non-blocking improvement.

Do not treat a realistic introduced path as unsupported merely because current CI
or tests do not exercise it. Require affirmative repo, product, or team authority
that excludes it, and reconcile any code comment, documented command, exposed
configuration/override, or established workflow that indicates support.

Drop unrelated pre-existing defects, speculation without a concrete mechanism,
intentional-and-authorized behavior, redundant or stale reports, and personal
preference. Keep confidence, impact, authority, and merge action distinct:

- Assign confirmed-defect severity from demonstrated impact.
- Hold for proof when an acceptance criterion or tracked rule requires it, or when
  merge would accept an unmitigated fail-open material security, data, permission,
  contract, migration, or operational risk.
- Route genuine product/policy ambiguity as `[decision-required]` in internal
  reviews and as a hold-for-answer discussion in `/prreview`.
- Otherwise record a credible but locally unprovable mechanism as residual
  verification with the exact check and owner.
- Never omit a concrete material risk solely because the provider or environment
  prevents local proof.

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

0. Coverage: list any changed file you did NOT open and why (normally empty),
   then state `all acceptance criteria met` or list only each not-met/deferred AC
   with its evidence/gap. Re-derive and account for every AC internally; do not
   print one clean row per AC. A not-met AC is a `[high]` finding.
1. Test-quality summary (REQUIRED). Evaluate every added, changed, deleted, or
   relaxed assertion under the Behavior-proof audit, but do not enumerate clean
   tests assertion by assertion. Group clean coverage concisely by behavior/file
   family and name the real boundary plus durable regression protected. Emit one
   exception row per assertion that is weak, ambiguous, non-`ship`, material to a
   finding, or whose deletion/relaxation may remove durable coverage:
   test/path [add/change/delete/relax] | concern | boundary/regression |
   quality + inclusion disposition
   Deleted/relaxed assertions may be grouped when they exclusively protect the
   same retired behavior; name the files/family and why no retained contract loses
   coverage. When no assertion changed, state that once and judge whether the
   changed behavior still has sufficient durable proof; do not manufacture a
   ledger.
2. Test-quality sub-verdict (MANDATORY, separate line): PASS or FAIL, derived from
   the Behavior-proof audit across every affected assertion, including grouped
   clean coverage. Any quality FAIL forces the overall verdict to ACTIONABLE.

Inclusion disposition is a SECOND axis, about worth rather than weakness —
definitions in `~/.agents/workflow/TESTING.md`
("Inclusion: should this test ship?"). Removing only an assertion proven obsolete
by TESTING.md's removal rule is recorded as `obsolete-assertion-cleanup`; it is
expected cleanup, not a non-`ship` disposition. Any other disposition that is not
`ship` requires an exception row and is a `[decision-required]` finding
(low/medium, NOT a quality FAIL) for the OPERATOR to settle. If durable authority
is ambiguous, use `[decision-required]` rather than defaulting to deletion. Never
silently delete a working test.

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
   - high: a correctness defect in changed production code causes a wrong result,
     crash, or silently skipped required path on a realistic supported input; OR
     the diff SUBSTITUTES an existing public contract, exported symbol,
     component type, schema/field, or library/primitive for a different one the task
     did not ask to change (altering accessibility or framework semantics); OR a
     changed behavior's only test is a delete-on-sight anti-pattern; OR a stated
     acceptance criterion is not actually met. (Net-new code that ADDS a
     component/primitive without replacing an existing one is not automatically
     high — judge it on correctness and coverage.)
   - medium: a bounded concrete correctness defect with lower impact, or a
     performance/scale defect on a set that can realistically grow; OR a test that
     fails the 10-second check or asserts implementation shape only with no real
     operation boundary; OR a risk-bearing new/changed branch,
     failure path, or persisted field that ships with no test at all; OR a
     materially new durable surface fails the proportionality check above.
   - low: maintainability/naming/doc nits with no behavioral or contract impact.
   Do not escalate uncertainty by itself; route it under Candidate admission and
   material-risk routing. If genuinely none, write "none found".
5. Verification notes. Do not rerun broad verification already reported green
   unless the diff makes that evidence suspect.
6. Convention conformance: hand-rolled code that duplicates a documented repo
   primitive is ACTIONABLE convention drift — cite the violated rule. For any UI
   surface apply `~/.agents/workflow/FRONTEND.md`; a broken state/a11y/contrast is
   ACTIONABLE. For visual-design work (building/recomposing a screen or component's
   look) VIEW the render yourself and JUDGE composition — not a presence check on
   the implementer's artifact. Composition/responsive/hostile-data findings are
   low / non-blocking when supported; don't manufacture taste nits where the
   surface reads cleanly. For incidental UI
   (a copy/prop/behavior tweak) do NOT flag a missing screenshot.
7. Residual risk or testing gaps.

## Decision-required handling

When Verdict is ACTIONABLE, mark any finding that requires operator input (scope
change, contract decision, ambiguous spec interpretation) with `[decision-required]`
in its required fix. `[decision-required]` is a routing tag, not a downgrade: the
finding keeps its real severity and the verdict stays ACTIONABLE. It may NOT be used
to park a data-loss, contract-drift, unrequested-component/dependency-swap, or
confirmed failed 10-second/durable-value finding — those stay blocking and are
resolved by the OPERATOR, not skipped by the implementer. Ambiguity about durable
authority remains `[decision-required]` as specified above. Append this implementer
directive verbatim at the end of your output so it stays with the findings when the
operator forwards them:

> Implementer: patch every finding autonomously. For any finding marked
> `[decision-required]`, skip the patch, summarize the decision needed, and return
> to the operator. An unresolved `[decision-required]` finding is an open ACTIONABLE
> item — it blocks PR handoff under the kernel's "Implementation Completion
> Handoff" review floor until the operator resolves it. Do not block other
> patches on those.

## After the verdict

For an implementation or outer-gate review, ACTIONABLE ends the current review
invocation: return the findings to the implementer/caller. Any patch returns to the
same reviewer through the applicable re-review route in `HANDOFF.md`. For
`/prreview`, ACTIONABLE is the strict raw result; continue through calibration and
the mandatory operator-only appendix before ending the invocation.

## Re-review mode (implrereview)

When invoked for a re-review — a prior ACTIONABLE verdict whose findings were
patched — your scope narrows to the changed lines and the prior findings; do NOT
perform a fresh broad review. Still apply Required reading (a reused reviewer
already holds it; a fresh fallback loads it first), the Behavior-proof and
Contract-propagation audits, and the decision-required rules above to what changed
— a patch that renames or removes a symbol still needs the reference sweep. Use the
Re-Review Kickoff's Return shape (per-finding status / regressions / new issues /
verdict), not the full Output contract. A prior weak/false-confidence-test finding
is "addressed" ONLY if the new or edited test exercises the real operation boundary
and would go RED when the original regression returns — a reverse-tautology patch
(editing an expected constant, SQL string, file/class existence, or snapshot to
match the new code) does NOT resolve it. An unresolved `[decision-required]` finding
is OUTSTANDING, not addressed, and keeps the verdict ACTIONABLE.
