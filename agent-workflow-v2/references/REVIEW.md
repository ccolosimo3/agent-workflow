# Agent Workflow V2 Review Authority

This file owns certifying review method, handoff semantics, verdicts, and
same-reviewer convergence. `TESTING.md` owns test quality; `WORKFLOW.md` owns
phase and outer-gate selection; `FRONTEND.md` is conditional on UI scope.

## Review state machine

1. An initial inner review uses exactly one fresh context. The receiver gets
   `WORKFLOW.md`'s envelope plus the applicable payload below and independently
   validates it.
2. `ACTIONABLE` findings are patched by the owning planner or implementer except
   for `[decision-required]` items. Causally affected verification runs, then the
   original reviewer receives the findings verbatim, mapped resolutions, reviewed
   revision, current tip or artifact, and invalidated evidence.
   Implementation patches are committed as new commits without amend or history
   rewrite before re-review; spec revisions identify the exact artifact revision.
3. Re-review is narrow: verify each resolution and inspect its delta for
   regressions. Reuse the same reviewer; use a fresh fallback only when the host
   cannot resume it, and disclose the lost context. Spec convergence stops after
   three revise/re-review cycles or a material operator decision.
4. After inner approval, apply `WORKFLOW.md`'s positive outer selector. Skip the
   outer gate automatically when it does not apply; do not ask for a waiver.
5. A selected outer gate begins in one fresh context, reads no prior findings,
   and reviews the whole converged artifact or final implementation range. Its
   patches return directly to that same outer reviewer. Do not reopen the inner
   reviewer unless the patch expands scope beyond an outer finding.

An `APPROVED` verdict may carry low suggestions. They are optional; leaving them
does not weaken approval. A purely mechanical patch with no behavior, contract,
test, or policy effect may retain approval, while any material patch returns to
the same reviewer.

Selecting a formal spec or implementation includes its inner review gate. Review
loops continue without ordinary status pauses. Stop only for a material decision,
missing required evidence or authority, unavailable review capability, or the
bounded spec retry cap.

### Documentation-only off-ramp

Skip review only when the entire diff is non-generated, non-normative prose that
records established facts or fixes links and changes no executable behavior,
contract, setup, command, verification/security policy, architecture, or operating
procedure. Check source fidelity, links, private-data safety, and
`git diff --check`. Workflow policy never qualifies; uncertainty uses inner review.

## Review payloads

Use semantic fields, not a verbatim template. Never invent missing facts.

**Spec initial:** artifact path/status and downstream action; raw operator ask;
source material; in/out scope; dependencies and valid intermediate state;
load-bearing file:line claims; chosen/rejected approaches; known risks and
unresolved decisions; acceptance and proof strategy; approval-gated activity;
repository convention/testing/design authorities.

**Implementation initial:** work item/spec and raw ask; acceptance; committed
base/tip and checkout; two-sentence change summary; in/out scope and discovered
follow-ups; exact verification/results tied to the tip; changed tests and
inclusion exceptions; hot spots/deviations; documentation impact; remaining
operator or environment proof; repository authorities.

**Re-review:** prior findings verbatim; artifact revision or prior-tip/current-tip
range; resolution per finding; verification invalidated and rerun. Do not rebuild
or resend the initial payload to a resumable reviewer.

Payload summaries are claims. The artifact, diff, repository, and actual command
output are authority. A kickoff or review becomes stale when its named revision
no longer matches the reviewed artifact or tip.

## Stance and required investigation

Review adversarially, then report honestly. Approval is valid only after trying
to refute the change; do not invent findings to appear thorough.

Before a verdict:

1. Read the raw operator ask and source issue/spec; independently derive intended
   behavior, non-goals, and acceptance.
2. Read repository instructions and the applicable portable authorities. Load
   `FRONTEND.md` and repo design guidance only for UI scope.
3. For implementation, inspect the full base-to-tip diff and open every changed
   file around each change. For a spec, read the entire artifact and every
   dependency it makes load-bearing.
4. Treat every summary, acceptance list, risk statement, verification receipt,
   and prior claim as something to confirm or refute.
5. Resolve current external or version-sensitive claims against the repository's
   pinned version and official primary sources; do not judge them from memory. If
   the host lacks public-research capability, disclose it and record the dated
   claim as non-blocking residual proof unless repository evidence or acceptance
   independently requires a hold.

An implementation reviewer also opens every changed assertion, including the base
version of deletions, and traces every changed public or cross-boundary contract
through affected consumers. An approval that leaves a changed file unopened is
invalid.

## Shared audits

### Scope, intent, and proportionality

Compare the artifact or diff with the raw ask, not only acceptance criteria.
Unrequested substitution of a public contract, component, primitive, library,
algorithm, data path, schema, or dependency is `[decision-required]` even if the
new form works. Cosmetic in-place refinements that preserve identity are not
substitutions.

For every new abstraction, configuration, persisted state, fallback/recovery
path, or cross-package responsibility, identify its current requirement, observed
failure, established pattern, or second real consumer. Missing authority is
scope expansion. Apply `KERNEL.md`'s nearest-pattern and exceptional-retry check;
do not use line count as the verdict.

### Contract propagation

For each changed exported/public identity or cross-boundary contract, record the
relevant before/after identity and trace definition or producer through every
affected consumer to observable behavior. Include names, signatures, return/data
shape, routes, events, configuration, workflow outputs, persistence, component
type, and accessibility semantics. Search repository-wide for changed and
deliberately preserved identifiers. A preserved label over changed behavior can
mask a broken contract; prove the real consumer.

### Information loss

When code parses, normalizes, groups, filters, allocates, falls back, or reduces
input, state what distinctions the output preserves and discards. For each
discarded distinction that can affect correctness, policy, or uniqueness,
construct the cheapest pair of inputs that collapse together and test the result.

### Closed-loop lifecycle

For each materially changed stateful surface, trace one realistic adverse state
through every applicable retry, timeout/expiry, cleanup, fallback, recovery, and
rollback transition at the real supported entry and operation boundary. Identify
the invariant and its success/health/completion/reversion oracle. Treat a
transition that can report success or erase actionable evidence while that
invariant remains false as a candidate under the normal admission and severity
rules. Keep the trace internal unless it yields a finding or residual proof.

### Behavior and test proof

Apply `TESTING.md` to every added, changed, deleted, or relaxed assertion;
confirm equivalent durable proof remains after deletion. Shape assertions are
supplemental only when contractual and paired with behavioral or operator proof.
Do not accept a spec-authored equivalence as authority: validate its premise and
the product regression each proof would catch at the minimum causal boundary.

### CI execution context

For every changed CI workflow, reconstruct each changed job as an isolated empty
runner. Trace relevant trigger and dependency paths through success, failure,
skip, cancellation, and retry. Confirm repository files/local actions, tools,
packages, working directories, artifacts/outputs, permissions, secrets, and
environment values exist before use; verify `if`, `needs`, fallback, and
`continue-on-error` cannot skip or mask required work. Use safe execution or the
narrowest structural/ordering proof; leave provider-only execution explicit.

### Spec method

Verify factual and file:line grounding, self-contained goal/non-goals, chosen and
rejected approach tradeoffs, dependency/order claims, one independently valid
Task, minimum-sufficient shape, and implementation latitude. Acceptance must be
behaviorally testable and cover failures/edges; verification must exercise the
real operation boundary and distinguish automated from operator/live proof.
Confirm approval boundaries, documentation impact, and any conditional UI design
strategy, plus tracker metadata when filing is an intended downstream action.
Tracker- or public-facing text must omit private/local-only material and use
project language rather than private workflow shorthand. A reviewer identifies
direction choices but does not make them.

### Implementation method

Account for every acceptance criterion and changed file. Run the shared audits,
repo conventions, and `TESTING.md` real-boundary bars. For migrations or
persistence, confirm save/reload and required schema/upgrade evidence. For UI,
apply `FRONTEND.md` and inspect the render only when the change is genuinely
visual-design work. Inspect automated-review exclusions when configured; an
excluded changed surface has no such coverage. Do not rerun a broad green gate
unless the reviewed delta, environment, missing/stale evidence, or a concrete
hypothesis can invalidate it; use the narrowest decisive check.

On the surfaces touched, explicitly check security/permission behavior and
performance/scale. When state or side effects change, also check partial failure,
repeat delivery, and ordering. Treat an inapplicable concern as clean, not as a
finding to manufacture.

## Candidate admission and severity

Keep a candidate only when the reviewed work introduced it, made it materially
reachable, left an in-scope requirement unmet, or made an unauthorized change;
and it has a concrete supported path, meaningful consequence or applicable rule,
and confirmed evidence, a credible material mechanism after narrow validation,
a real intent/policy ambiguity, or an objective non-blocking improvement. Drop
unrelated pre-existing defects, speculation, authorized behavior, duplicates,
and preference. Hold when acceptance or tracked policy requires proof, or when
merge would accept an unmitigated fail-open material security, permission, data,
contract, migration, or operational risk. Otherwise record a locally unprovable
material mechanism as residual proof with the exact check and owner.

- **critical:** data loss/corruption, security compromise, or silent destructive
  migration/schema behavior.
- **high:** realistic changed-code wrong result, crash, or skipped required path;
  unmet acceptance; unauthorized substitution of a public contract, component,
  schema, library, or primitive; or a changed behavior whose only proof is a test
  anti-pattern.
- **medium:** bounded lower-impact correctness or realistic scale defect; weak
  shape-only test; untested risk-bearing branch/failure/persistence; or unjustified
  durable surface.
- **low:** supported maintainability, naming, documentation, or composition issue
  without behavioral/contract impact.

Uncertainty alone does not raise severity. Tag a material operator-owned scope,
contract, product, policy, or ambiguous durable-authority choice
`[decision-required]`; it remains open and blocks approval. Confirmed defects are
fixed, not parked under that tag.

## Output contract

### Spec review

Return, in order:

1. **Coverage:** source/dependency files not opened (normally none), then only
   unmet or deferred plan requirements. Do not print clean rows.
2. **Proof strategy:** `PASS` or `FAIL`, with only gaps in behavioral acceptance,
   real-boundary verification, failure coverage, or operator proof.
3. **Verdict:** `APPROVED` or `ACTIONABLE`. A proof `FAIL`, medium-or-higher
   finding, skipped required investigation, or unresolved `[decision-required]`
   item forces `ACTIONABLE`.
4. **Findings:** `[severity] artifact-section-or-file:line | category | issue |
   impact | required fix`, or `none found`. Low findings may accompany approval.
5. **Verified clean and residual decisions:** concise claims/sections traced and
   only remaining operator choices or unavailable proof.

### Implementation review

Return, in order:

1. **Coverage:** changed files not opened (normally none), then only unmet or
   deferred acceptance items. Do not print clean acceptance rows.
2. **Test quality:** group clean coverage by behavior/boundary and list only weak,
   ambiguous, deleted-risk, or non-`ship` exceptions; state `PASS` or `FAIL`.
   When no assertion changed, say so once and judge whether proof remains enough.
3. **Verdict:** `APPROVED` or `ACTIONABLE`. Any medium-or-higher finding, test
   `FAIL`, skipped required investigation, or unresolved `[decision-required]`
   item forces `ACTIONABLE`.
4. **Findings:** `[severity] path:line | category | issue | impact | required
   fix`, or `none found`. Low findings may accompany approval.
5. **Verification and residual proof:** what evidence was reused, what narrow
   check was run, and exact remaining operator/environment proof.

Do not print internal ledgers, duplicate findings as risks, or restate stable
policy in either mode.

## Re-review mode

Check each prior finding against its mapped revision, then inspect that delta for
regressions or scope expansion. A test finding is addressed only when the new
proof exercises the real operation and fails when the original regression returns;
updating a constant, snapshot, SQL string, or source-shape assertion is not a fix.
Return per-finding `addressed | outstanding`, new issues in the patch, affected
verification, and `APPROVED | ACTIONABLE`. Do not repeat the full output contract
or restart broad discovery.
