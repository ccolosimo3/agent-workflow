# Review Workflow Refinement Proposal

Status: amended design implemented locally; PR #680 forward-test corrections are
applied. Commit/push and remaining historical calibration are pending.

## Recommendation

Keep `REVIEW_RUBRIC.md` as the strict common review engine. Refine its repeated
investigation rules without weakening their concrete mechanics, then turn
`/prreview` from a one-shot report into a proportionate, operator-steerable review
process:

1. frame and map the change;
2. perform the lead's independent strict discovery;
3. for every non-compact PR, run one blind challenger in parallel before either
   reviewer sees prior comments or the other's findings;
4. reconcile the two passes internally: the challenger attacks the lead's
   candidates and clean conclusions, the lead validates disputes, and both reuse
   narrow evidence until the material candidate set stabilizes;
5. emit one non-blocking convergence update with optional steering choices while
   continuing by default; and
6. issue one calibrated merge recommendation backed by a mandatory private
   evidence appendix.

`implreview` and `outerreview` remain strict, single-reviewer
`APPROVED`/`ACTIONABLE` gates. They receive only the shared rubric improvements;
their workflow and verdict ownership do not change.

## Invariants and non-goals

- Strict discovery is not softened in anticipation of coworker-facing calibration.
- The lead applies `REVIEW_RUBRIC.md` in full and owns the complete diff,
  cross-surface reasoning, verification, candidate validation, and final result.
- Compact/cohesive PRs stay lead-only. Standard and large PRs use exactly one blind
  challenger; large PRs may add at most two bounded specialists for genuinely
  independent material questions. The challenger counts against the existing
  three-subagent ceiling.
- The challenger and specialists return adversarial evidence, not an additional
  verdict or vote.
- Confirmed defects, unmet acceptance criteria, tracked required-proof gaps, and
  shared-policy violations cannot disappear during calibration.
- Uncertainty does not establish severity, but lack of local execution does not
  erase a concrete material risk.
- No file-count trigger, duplicate broad verification, per-agent worktree, new
  review verdict, or new approval boundary.
- Do not replace concrete migration, persistence, UI, accessibility, security, or
  contract checks with generic advice.
- Do not add automatic fan-out to `implreview` or `outerreview`.

## Part 1 — Shared rubric refinements

### 1. CI workflow audit

Replace the separate fresh-runner and control-flow additions with one conditional
method under `REVIEW_RUBRIC.md` Required investigation:

> **CI workflow audit.** For every added or changed workflow, reconstruct each
> changed job from a fresh runner and trace its relevant trigger and dependency
> paths through success, failure, skipped, and cancelled states. Verify that
> prerequisites are available before use—including repository files or local
> actions, tools and dependencies, working directories, artifacts and outputs,
> permissions, secrets, and environment values—and that `if`, `needs`, fallback,
> and `continue-on-error` behavior cannot skip or mask required work. Use safe
> execution or the narrowest targeted structural or ordering assertion where
> practical; leave provider-only execution as Tier 4. YAML validity and tests of
> invoked scripts alone do not prove workflow viability.

This would catch Townchest PR #602's missing checkout by requiring the reviewer to
account for a repository-local script on an otherwise empty runner. It generalizes
to tool setup, artifacts/outputs, event context, permissions, recovery conditions,
and masked failures without creating one rule per incident.

### 2. Behavior-proof audit

Consolidate repeated test-quality explanations into one method while retaining the
full quality and inclusion semantics from `TESTING.md`:

> **Behavior-proof audit.** For every added, changed, deleted, or relaxed
> assertion, identify the durable regression and authority it protects, the
> observable outcome and real product boundary it exercises, and whether restoring
> that regression makes the test fail. A test that goes red only for a non-durable
> implementation detail still fails quality. Treat implementation-shape checks as
> supplemental only when the exact shape is contractual or a named real-boundary or
> Tier-4 proof carries the behavior. When coverage is removed, confirm equivalent
> durable proof remains. Apply `TESTING.md`'s independent inclusion axis and preserve
> operator routing for every non-`ship` disposition.

Keep the investigation exhaustive but make the report exception-focused:

```text
Clean coverage: concise behavior/file-family groups naming the real boundary and durable regression.
Exceptions: test/path [add/change/delete/relax] | concern | boundary/regression | quality + inclusion disposition
```

Deleted or relaxed assertions may be grouped when they exclusively protect one
retired behavior and the reviewer names why no retained contract loses coverage.
Individual rows remain required for weak, ambiguous, non-`ship`, finding-bearing,
or potentially coverage-losing assertions.

The consolidation must preserve:

- review of every addition, change, deletion, and relaxation;
- the durable-value and reverse-regression checks;
- real-operation-boundary judgment;
- the anti-pattern table and shape-only sole-proof failure;
- contractual/supplemental proof exceptions;
- equivalent-proof checks when coverage is removed;
- `trim`, `redundant-with-*`, `one-off-proof->pocket`, and
  `obsolete-assertion-cleanup` distinctions; and
- operator ownership of ambiguous or non-`ship` dispositions.

The repeated prose and clean-test output may shrink. The evidence obligations do
not.

### 3. Contract-propagation audit

Consolidate the correctness side of identity, masking, and consumer checks without
removing their falsifiable mechanics:

> **Contract-propagation audit.** For every changed exported/public identity or
> cross-boundary contract, record the relevant before→after identity and trace the
> definition or producer through every affected consumer to observable behavior.
> Use repo-wide reference search for symbols and preserved labels, plus the
> repository's actual producer/consumer mechanisms for schemas, routes, events,
> workflow outputs, configuration, adapters, and persisted fields. Account for
> every consumer and any orphan or dead compatibility path. A preserved symbol,
> route, prop, field, test ID, or label over changed behavior is a masked change,
> not proof of compatibility: name the behavioral test that should have failed and
> verify the changed contract at its real consumer boundary.

Activate this for public/exported identities, cross-boundary data shapes, persisted
contracts, and deliberately preserved compatibility labels—not private local
implementation details. Keep the raw operator-intent/substitution and
proportionality checks separate because they judge authorization rather than
propagation correctness.

### 4. Information-loss audit

Add one standalone conditional method plus a Required-investigation trigger:

> For any changed code that parses, normalizes, groups, filters, allocates, falls
> back, or reduces input, run the Information-loss audit even when the code is
> private and no exported/public identity or cross-boundary contract changed.

> **Information-loss audit.** When changed code parses, normalizes, groups,
> filters, allocates, falls back, or reduces input, identify which distinctions
> the resulting representation preserves and discards. For every discarded
> distinction that could affect correctness, policy, or uniqueness, construct the
> cheapest pair of inputs that become indistinguishable and test the resulting
> behavior.

This is a hypothesis-generation method, not a checklist of known incidents. It
would have exposed Townchest PR #680's loss of value usability (`populated` versus
`blank`) and source identity (`selected stage` versus `fallback`) without naming
whitespace or SST as standing cases. Apply it only when the diff performs one of
the named transformations.

### 5. Candidate admission and material-risk routing

Use a shared validity rule for all review modes:

> **Candidate-admission and routing gate.** Keep a candidate when the reviewed
> change introduced it, exposed or materially increased the reachability or impact
> of an existing defect, left an in-scope requirement unmet, or intentionally made
> an unauthorized scope or contract change; and when it has a concrete supported or
> realistic path, a meaningful consequence or applicable tracked rule, and one of:
> confirmed evidence, a credible material mechanism remaining after the narrowest
> feasible validation, a genuine intent/policy ambiguity affecting the outcome, or
> an objective non-blocking improvement. Drop unrelated pre-existing defects,
> speculation without a concrete mechanism, intentional-and-authorized behavior,
> redundant or stale reports, and personal preference.

Do not classify a realistic introduced path as unsupported merely because current
CI or tests do not exercise it. Require affirmative repo, product, or team authority
excluding the path, and reconcile code comments, documented commands, exposed
configuration/overrides, and established workflows that indicate support.

Keep confidence, impact, authority, and merge action distinct:

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

Replace `If unsure whether a finding is medium-or-higher, treat it as blocking`
with evidence-based routing rather than severity escalation. This is a real policy
change for unverified risk; confirmed-finding thresholds remain strict.

Also give ordinary defects an explicit severity home:

- `high`: a correctness defect in changed production code that causes a wrong
  result, crash, or silently skipped required path on a realistic supported input;
- `medium`: a bounded concrete correctness defect with lower impact, or a
  performance/scale defect on a set that can realistically grow.

Existing critical, substitution, acceptance-criteria, test-quality, and low/nit
classes remain in force and compose with these additions.

### 6. Automated-reviewer awareness without anchoring

Split the always-available configuration check from PR-only comments:

> **Automated-reviewer coverage.** If reviewer configuration exists, inspect its
> path exclusions before review and treat excluded changed surfaces as lacking that
> automated coverage. For `/prreview`, defer reading the content of already-posted
> automated and human comments until independent discovery is complete; then use
> them to deduplicate, confirm current status, and note material agreement or
> disagreement. Do not duplicate mechanical findings, but independently assess
> correctness, contracts, and test quality.

Inner pre-PR reviews apply the configuration half and skip the nonexistent-comments
half.

### 7. Operation-lifecycle audit remains deferred

A generic retry/duplicate/partial-failure/cancellation audit may eventually be
valuable for asynchronous or multi-step work, but its activation boundary is not
yet calibrated. Do not add it in V1. Existing surface-specific and CI rules remain
available where those states are already part of the contract.

## Part 2 — `/prreview` as an operator-steerable process

### 1. Frame and map

The lead:

- records the current branch and clean-tree state;
- uses the clean, available repo-root checkout by default and creates a review
  worktree only when the root is dirty/occupied, switching would disturb active
  work, or verification requires incompatible dependency/tool state;
- resolves and freezes the exact base SHA and PR head SHA;
- reads the PR, linked issue, applicable repo guidance, and automated-reviewer
  configuration, while deferring prior comment content;
- derives the raw ask and acceptance criteria;
- maps the behavior/system flow before→after;
- inventories material risk surfaces, changed tests, verification routes, and
  shared producer/consumer, schema, state, transaction, deployment, and rollout
  seams; and
- chooses a compact, standard, or large review profile.

Profiles control ceremony, not rigor:

- **Compact/cohesive:** eligible only when all are true: the diff changes one
  narrow behavior in one subsystem; it does not add or change an auth/security/
  permission boundary, migration/persistence/data contract, public/external
  contract, concurrency/lifecycle/state machine, cross-package/service seam,
  deployment topology, or shared test/build infrastructure; one focused
  verification route can falsify the change; and mapping leaves no material
  unanswered question. A localized repair to one existing CI/deployment job may
  remain compact only when it restores an established prerequisite or ordering
  invariant without changing triggers, permissions, secrets/environment,
  artifacts/outputs, cross-job `needs`/`if` flow, or deployment targets. Complete
  it in one turn with no subagent or checkpoint unless a real decision appears.
- **Standard:** any review that is not compact and does not qualify as large. The
  lead and one blind challenger perform independent discovery, reconcile
  internally to stable evidence, then emit the non-blocking convergence update.
- **Large/heterogeneous:** when the map contains at least two materially
  independent risk surfaces or subsystems requiring different proof, select large
  unless one trace can cover both and record why. Use the same lead-challenger loop
  and convergence update. Add at most two bounded specialists only when genuinely
  independent material questions remain after mapping; total subagents, including
  the challenger, never exceed three.

The lead records the selected profile and one-line evidence in the kickoff. If any
compact condition is uncertain, select standard. File count alone never selects a
profile or justifies a specialist.

### 2. Blind two-agent discovery

The lead applies `REVIEW_RUBRIC.md` in full, opens every changed file, reads enough
surrounding code to understand each path, and owns every shared seam. It does not
assign final coworker-facing actions while discovery is incomplete.

For standard and large profiles, start one challenger after freezing the range and
deriving the raw ask, but before exposing the lead's risk priorities, candidates,
clean conclusions, or any prior review comments. The lead continues its own pass
while the challenger independently scans the complete diff, chooses its own
highest-risk hypotheses, and deeply traces the paths most likely to falsify the
change. It uses the shared rubric as its discovery standard but does not reproduce
the rubric Output contract.

The challenger receives only:

- absolute checkout path and frozen base/tip SHAs;
- raw ask and acceptance criteria;
- applicable repo guidance and the shared rubric path; and
- the compact return contract below.

```text
Independent risk map:
Highest-risk hypotheses and paths traced:
Candidate evidence: scenario/input | PR relevance | consequence/authority |
supporting and counterevidence | narrow check/result
Important claims that still need proof:
Verified-clean observations:
Residual checks:
```

The challenger does not receive the lead's map or findings, issue a verdict or
severity, read prior comments, use `gh`, switch branches, mutate dependencies or
services, or run broad gates. Its purpose is independent hypothesis generation,
not a second certification.

For a large review only, delegate one specialist per still-unresolved material
question when the question:

- has a bounded primary evidence set;
- can be answered independently;
- does not duplicate another agent's question; and
- does not own a cross-surface seam or broad verification gate.

Use at most two specialists, so the challenger plus specialists remain within the
three-subagent ceiling. Supporting-file overlap is allowed when required for
context; question ownership is not.

Each evidence packet contains only:

- absolute checkout path and frozen base/tip SHAs;
- raw ask and relevant acceptance criteria;
- assigned question and primary evidence paths;
- known lead-owned seams;
- applicable rubric/repo rules;
- any explicitly assigned isolated command; and
- the compact return shape below.

Specialists apply only the named rubric methods relevant to their question. They
do not receive the full external-review kickoff, issue verdicts, classify severity,
read prior review comments, switch branches, use `gh`, change dependencies or
services, or run broad gates.

```text
Question/surface:
Files and surrounding code read:
Operation/call paths traced:
Candidate evidence:
- scenario/input
- PR relevance
- observable consequence or authority
- supporting and counterevidence
- explicitly assigned check + result, if any
Verified-clean observations:
Residual checks:
```

The lead alone owns `gh`, fetch/checkout/restore, dependency or service state,
broad verification, candidate validation, and the final result. Every command has
one owner; challenger and specialist checks must be explicitly assigned or remain
read-only traces.

### 3. Internal reconciliation and validation

After both blind passes, the lead prepares a working set containing every
candidate, material verified-clean conclusion, supporting evidence, and remaining
uncertainty. Give it to the same challenger and ask it to refute proposed blockers,
challenge important clean conclusions, identify unexamined seams, and reconcile
its blind-pass candidates against the lead's evidence.

For every candidate, the lead establishes:

1. **PR relevance:** introduced, newly exposed/worsened, unmet requirement, or
   unaffected/pre-existing;
2. **concrete path:** the supported or realistic scenario and operation/call path;
3. **consequence/authority:** the observable impact or applicable requirement,
   contract, or tracked rule; and
4. **decisive evidence:** confirmation, bounded unresolved mechanism, or refutation
   at the frozen/current tip.

Refutation must exercise the same failure boundary and relevant conditions—such
as concurrency, cardinality, ordering, or lifecycle—as the candidate or clean
conclusion. A narrower green path is counterevidence, not refutation.

Resolve factual disputes through code, history, or the narrowest decisive proof,
then return the updated evidence to the same challenger. Continue the exchange only
while it produces a new material candidate, counterexample, or proof. A full
exchange that changes no material status establishes convergence; route any
remaining provider/access-dependent fact as exact residual verification and any
intent/policy ambiguity to the operator or author. Agreement alone is not proof,
and convergence does not require identical wording.

Every extra pass names the unanswered question or new lens. Do not repeat the full
diff or broad gates for reassurance. If the challenger or a specialist stalls,
errors, or returns no cited trace, the lead takes the question back and continues;
respawn only for a clear transient tooling failure. A replacement challenger must
first complete the original blind-input pass before receiving the working set; if
none can complete both phases, disclose the degraded topology and do not claim
standard/large convergence.

### 4. Synthesis and freshness

Before classification, the lead:

- reviews all cross-surface seams and asks what the initial pass could have missed;
- absorbs or refutes every candidate using current-tip evidence;
- reads prior automated and human comments, deduplicates them, and checks whether
  they are already resolved;
- accounts for every acceptance criterion, changed test, material surface, and
  verification route; and
- re-reads `headRefOid` and review-thread state.

If the PR tip moved, review the delta and invalidate affected evidence. Restart
from a newly frozen tip only when the delta is broad enough that the prior map is no
longer trustworthy.

### 5. Non-blocking convergence update and steering

After internal convergence and freshness reconciliation, emit one progress update:

```text
Frozen range/tip:
Change and risk map:
Solidified findings:
Refuted candidates:
Important verified-clean conclusions:
Remaining factual unknowns or decisions:
Optional deeper areas (ranked):
Default: finalize unless the operator redirects.
```

This is commentary, not a turn-ending checkpoint: do not stop or wait for a reply.
Continue to finalization by default. Accept `zoom out`, `drill into <area>`, `shift
to <area>`, or `challenge <candidate>` if the operator steers while work continues;
run the named investigation, then pass any new material evidence through the same
lead-challenger reconciliation before finalizing. Pause only for a genuine
operator/product decision, operator-controlled access or approval, or an explicit
operator pause.

### 6. Final report and conservation rule

Return the one-screen Action Brief first:

1. **Stance:** approve, comment, request changes, or hold for a named answer/proof.
2. **Request changes — blocking:** confirmed material defects, unmet acceptance
   criteria, applicable merge-rule violations, required-proof gaps, and credible
   unmitigated fail-open material risks.
3. **Discuss with author:** mark each `hold for answer` or `non-blocking`. Keep a
   concern here as a conditional blocker, with both outcomes, when blocking status
   depends on unresolved intent or scope; do not call it confirmed request changes
   until that fact is resolved. A clearly applicable written criterion is not
   ambiguous merely because the reviewer disagrees with it.
4. **Suggestions:** optional improvements where current behavior is correct and
   safe and no applicable authority is violated.
5. **Nits:** confirmed, objective, introduced, low-consequence details with no
   behavioral or contract impact; omit personal taste and mechanical-tool output.
6. **Residual verification:** annotate the blocking proof request or non-blocking
   follow-up it belongs to; it is not a standalone merge action.

`patch myself` remains an optional resolution route attached to an item and requires
separate authorization/team permission. It is not a severity or merge-action class.

Always append an operator-only audit appendix containing:

- the strict rubric result;
- every raw non-clean item mapped to its final action or explicit rejection reason;
- acceptance-criteria exceptions;
- the grouped test-quality summary, exception rows, and Test-quality PASS/FAIL;
- verification commands/results and routing;
- the verified-clean record; and
- remaining residual/Tier-4 checks.

Calibration may change framing, resolution route, or merge recommendation only with
an explicit evidence-based reconciliation. It may not downgrade or omit a confirmed
material defect, unmet acceptance criterion, applicable required-proof gap,
test-quality failure, or tracked shared-policy violation. Do not add a candidate
count or confidence-score ceremony.

### 7. Completion rule

Finalize when:

- every material surface and lead-owned seam has been examined;
- every acceptance criterion is traced;
- every changed/deleted/relaxed test is assessed;
- every candidate is confirmed, refuted, routed for decision, or assigned exact
  residual verification;
- for standard/large reviews, the blind challenger pass and internal evidence
  exchange have stabilized, with every remaining disagreement explicitly routed;
- verification is run or explicitly routed once;
- prior comments are reconciled; and
- the PR tip is fresh.

Additional review after this point requires a changed tip or a named unanswered
question; do not perform another broad pass without a new information target.

## Part 3 — Internal review gates

`implreview` and `outerreview` continue to:

- use one certifying reviewer;
- apply the shared rubric in full;
- use strict `APPROVED`/`ACTIONABLE` semantics;
- hold unmet criteria, weak sole proof, contract/scope drift, applicable policy
  violations, and routed material risk actionable; and
- reuse their existing re-review mechanics.

No direct skill edits are expected for them beyond any pointer names required by
the shared rubric consolidation. Outer-review fan-out is out of scope and its
current no-subagent independence contract remains unchanged.

## Part 4 — Historical read-only calibration pilot

Use actual immutable Townchest ranges rather than building a fixture framework.
No comments, mutations, provider checks, or paid activity.

### Frozen cases

1. **PR #602 — parity workflow with missing checkout**
   - range: `ac4a730d0211e19a2f74b3b79195563861137b12..b8b5fb954ee935fda2f9f3b8b1af8e44b66ef2c9`
   - required discovery: repository-local validation script is invoked from a fresh
     job without checkout;
   - required final action: request changes/blocking;
   - calibration counterexample: absence of an additional ideal Vendure E2E alone
     must not become a merge blocker without a tracked required-proof rule or a
     demonstrated unmitigated material path; provider drill may remain rollout or
     residual verification.
2. **PR #680 — deployment preflight information loss**
   - range: `c84e948ce8cd3ec5beb48ee45f4929e4b7cfb759..473242522f64411a141bbbb3168f657a1eff67f8`
   - required topology: lead plus one blind challenger; specialists only if a
     separate bounded unknown genuinely remains;
   - required independent discovery, without an incident-specific prompt: GitHub
     presence booleans accept whitespace-only required values, and the SST parser
     discards both value usability and selected-stage versus fallback identity;
   - required final action: request changes for the confirmed partial-deployment
     paths;
   - calibration counterexample: if the review raises provider-managed Vercel
     builds as a blocker, supply the operator fact that production activation is
     manual and ordered after GitHub/backend success; the final report must refute
     or downgrade that candidate unless contrary evidence survives.
3. **PR #684 — focused checkout repair**
   - range: `f83365968436c7d9bef522394043b8b445757e49..26bb11d2e47ddf1db3728f044b01a2592ddc936e`
   - required topology: compact/direct, zero subagents;
   - required discovery: checkout precedes the repository-local command on the
     affected path;
   - required final action: no blocker unless the run demonstrates a different
     concrete regression; no unrelated findings.

### Procedure and threshold

1. Record the current skill's historical baselines: PR #602 missed checkout and
   over-weighted an ideal E2E; PR #680 found the SST fallback issue but missed
   blank/whitespace values until explicitly steered, then correctly refuted the
   Vercel blocker and found the GitHub presence-only path.
2. After implementing but before promoting the amended skill, run one fresh
   read-only `/prreview` task against each frozen range using the same chosen
   model/reasoning profile.
3. Invoke with the PR number plus explicit frozen range; do not post to GitHub.
4. Record for each run: topology/subagent count, discovered candidates, raw→final
   mapping, verification commands, final stance, elapsed time, and material tool
   failures in a dated appendix to this proposal.

Pass requires:

- PR #602 catches and blocks the missing checkout without blocking solely on the
  missing ideal E2E;
- PR #680 independently catches both information-loss paths, preserves them as
  blocking after reconciliation, and correctly recalibrates any Vercel candidate
  after the supplied operational fact;
- PR #684 uses zero subagents and manufactures no unrelated blocker;
- no run duplicates broad verification across lead, challenger, or specialists;
- every standard/large run performs one blind challenger pass and continues the
  internal evidence exchange until a full round changes no material status;
- the convergence update does not pause the task absent a real decision, access/
  approval boundary, operator steering, or explicit pause; and
- every raw non-clean item has a final disposition.

Any miss leaves V1 unpromoted and triggers one targeted instruction revision, not
another general checklist expansion. Stop after the stated three-run pilot; any
additional calibration is outside this V1 proposal.

## File-level implementation plan

Before editing the skill, read and follow the available `skill-creator` skill for
the update; do not scaffold a replacement package.

1. `REVIEW_RUBRIC.md`
   - merge the CI bullets;
   - consolidate behavior-proof wording while preserving full investigation and
     switching clean output to grouped summaries plus exception rows;
   - consolidate contract propagation with explicit search/identity/masking proof;
   - add the conditional information-loss audit;
   - add candidate/material-risk routing and correctness/performance severity homes;
   - split automated-reviewer configuration from post-discovery comment handling.
2. `skills/prreview/SKILL.md`
   - implement the compact/standard/large staged process;
   - keep compact reviews lead-only; require one blind challenger for standard and
     large reviews; allow at most two exceptional specialists on large reviews;
   - add the same-challenger evidence loop, evidence-based convergence condition,
     non-blocking progress update, operator steering, lead-owned seams/commands,
     recovery, freshness, validation, and completion rules.
3. `kickoffs/external-pr-review.md`
   - carry the framing inputs and the mandatory final Action Brief + private audit
     appendix; do not give this full-review kickoff to the challenger or specialists;
   - replace `gh pr checkout <number>` with the exact frozen-head checkout/worktree
     prepared by `prreview`; require `HEAD == headRefOid` before verification and
     forbid a second checkout through the moving PR ref.
4. `skills/calibrate-review/SKILL.md`
   - align blocking/discussion/suggestion/nit semantics, residual annotations, the
     optional `patch myself` route, and the raw→final conservation rule.
5. `kickoffs/review.md`, Re-review wording, and `TESTING.md`
   - update only exact references affected by the consolidated behavior-proof name
     or ledger shape; preserve internal verdict and test doctrine.
6. This proposal
   - record the dated calibration receipt before promotion.

After editing, run:

```text
python3 /Users/ccolosimo/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/ccolosimo/.agents/workflow/skills/prreview
python3 /Users/ccolosimo/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/ccolosimo/.agents/workflow/skills/calibrate-review
git diff --check
```

Both skill validators must print `Skill is valid!`; `git diff --check` must be
clean. If the validator is blocked by a missing runtime dependency, report that
exact blocker and use an available YAML parser plus the mechanical diff check as
explicit fallback evidence; do not install anything without approval. If an
edited skill has `agents/openai.yaml`, confirm it still matches `SKILL.md` and
regenerate it with skill-creator only when stale. Neither current skill has that
file.

No review-count, outer-gate, approval, verification-tier, tracker, or GitHub
mutation policy changes are proposed.

## Success criteria

- PR #602 is caught for the correct fresh-runner reason.
- Strict discovery completes before coworker-facing merge classification.
- The operator can zoom out, drill down, shift, or challenge without restarting
  the review, but the default flow does not wait for operator direction.
- A compact PR completes directly with no fan-out or unnecessary checkpoint.
- Every standard/large review receives an independent blind challenger pass and an
  internal evidence exchange that continues until material statuses stabilize;
  compact reviews receive neither.
- The convergence update is informative and non-blocking; only real decisions,
  access/approval boundaries, steering, or an explicit pause interrupt progress.
- A large review uses no more than two exceptional specialists and no more than
  three subagents total, including the challenger.
- A map with independent surfaces requiring different proof selects large unless
  the reviewer records why one trace covers both.
- The lead reviews every changed file and shared seam; the challenger independently
  chooses its own risk hypotheses; no agent duplicates broad gates.
- The lead and challenger use one exact frozen head; neither follows a moving PR
  ref after the range is established.
- Conditional information-loss reasoning generates boundary pairs without adding
  incident-specific checklists.
- No candidate or verified-clean claim is refuted by a green check at a narrower
  failure boundary.
- Every reported defect has PR relevance, a concrete path, consequence/authority,
  and decisive or bounded-unresolved evidence.
- Every raw non-clean item survives to an explicit final disposition.
- Test and contract consolidations retain all existing concrete catch mechanisms.
- `implreview` and `outerreview` remain strict and single-reviewer.
- No new mandatory review phase applies to compact/cohesive work.
