# Agent Workflow V2 Portable Kernel

This is the normative runtime floor for V2 skills. Repo and host adapters may add
facts or stricter limits; they cannot widen its authority, approval, independence,
or review requirements.

## Precedence and startup

- Follow current-session operator instructions, organization/security/code-owner
  policy, the nearest repository instructions, this kernel, then optional
  preferences.
- Read the repository's instruction chain before substantive work. Inspect the
  exact checkout and `git status` before branching, editing, or dispatching work.
- A full authority read satisfies later skill read requirements in the same
  agent context while the file is unchanged and its full instructions remain
  available. Reread when it changes or those instructions are no longer available;
  a summary or another agent's read is not a substitute. Fresh reviewers read
  their own applicable authorities. This does not waive current checkout checks
  or required source and diff inspection.
- In a linked worktree missing the root `AGENTS.local.md`, resolve the primary
  checkout with `git worktree list --porcelain` and read its adapter when present.
  Treat it as additive local facts; do not copy or stage it or import
  solution-bearing plan state into the worktree.
- Preserve unowned changes. Never reset, discard, overwrite, or “clean up” work
  outside the authorized scope.

## Authority

Read-only inspection and ordinary in-scope implementation steps are allowed.
Fresh current-session operator approval for the exact action is required before:

- destructive local operations, deletion outside stated scope, history rewrite,
  force operations, or bypassing safeguards;
- dependency, lockfile, toolchain, generated-artifact, or persistent-data changes
  not explicitly requested or approved by the current-session operator;
- pushes or externally visible mutations to repositories, trackers, messages,
  releases, deployments, providers, databases, payments, or infrastructure;
- authenticated external API/provider traffic, metered model/API calls,
  paid/live probes, or prepared-environment activity not explicitly authorized
  for its target, input scope, and applicable usage, spend, or side-effect bound.

Selecting a configured host/profile through operator intent or a selected phase's
declared worker/reviewer routing authorizes that bounded workflow substep. Its
work item, profile, declared invocation count, and return condition are the bound.
Subscription-backed usage needs no separate approval or dollar cap; a metered or
API-key-backed profile still requires its applicable usage or spend bound. Extra
calls, fan-out, profile/provider changes, or unrelated paid or live activity
remain gated.

An unchanged repository-documented disposable test harness is ordinary
verification when confined to loopback/local Docker and its own test namespace.
Any target, wrapper, migration, reset, seed, ingest, or persistent-store
difference remains gated.

Ordinary public web search, public-page lookup, and official-documentation
research remain allowed unless the operator says local-only/no-web; they are not
live-source probes, authenticated API/provider traffic, paid calls, or
prepared-environment activity.

One risk-selected or operator-requested certifying review and its same-session
re-reviews are authorized substeps of the selected phase. Extra, duplicate, or
early reviews and reviewer-triggered paid activity remain gated.

Natural approval covers the stated action and bounded correction or retry within
the same risk envelope; failure does not consume it unless the operator or
governing policy made it single-use. Re-ask only if the target, scope, side
effects, provider, input scope, or cap materially changes. Ambiguous assent or
silence is not approval. For a non-gated execution choice, use applicable
instructions, repository conventions, read-only inspection, and the smallest safe
disposable observation that can settle it before asking. Proceed with the simplest
reversible in-scope choice and report the assumption. Ask when the unresolved
choice can change observable behavior, the authorized Task or risk boundary,
authority or spend, safety, or difficult-to-reverse state. Actions in the
approval-gated list and review-count gate above require approval regardless of
reversibility. Before asking, state the exact action, target, and material side
effects. Never bypass a failed hook or policy check.

When workflow guidance causes a question, pause, or unfinished requested work,
link the exact instruction and quote the relevant clause; distinguish an explicit
requirement from your interpretation. Continue independent authorized work while
the gated action or material decision waits.

Never commit secrets, credentials, private operator adapters, personal paths, or
other untracked local configuration.

## Minimum-sufficient quality

- Prefer the simplest complete repository-conventional shape. Before a plan is
  review-ready and again before implementation commits to a materially larger
  shape, compare the intended outcome, non-goals, irreducible correctness/safety
  constraints, nearest complete pattern, added responsibilities/state/artifacts,
  operator steps, reuse, and proven consumers.
- Apply the same comparison to proof code. When a harness becomes materially
  broader or owns more contract/lifecycle behavior than the product delta, stop
  and reduce it to the smallest causal boundary using existing production owners.
- Added durable machinery must trace to a current requirement, observed failure,
  established pattern, or second real consumer. When the same correction recurs
  and a repository mechanism can reliably prevent it, prefer the lowest existing
  owner—type/API boundary, runtime guard, or focused static/CI check—over more
  workflow prose; promotion beyond the authorized task remains separate work. A
  larger design remains correct when those constraints require it or it reduces
  operational complexity.
- Workflow metadata may coordinate or report work; its absence or drift does not
  invalidate previously valid output or require replay unless it protects target
  identity, approval or authority, product integrity, or a causal dependency.
  Revalidate the smallest affected behavior and continue; do not repair
  bookkeeping as a substitute for implementation or evidence.
- A planner-authored invariant is not independent authority. Before adding
  durable state or recovery for an exceptional retry or manual fallback, compare
  it with handling that exception through the existing path.
- Change only behavior the work explicitly targets; preserve other observed
  behavior and public contracts unless changing them is necessary to satisfy the
  ask. Prefer an existing owner over a parallel abstraction; keep task-local code
  limited to task-specific behavior.
- Update owning documentation only when behavior, contracts, setup, architecture,
  verification, or user/operator workflow changes.

## Verification and review floor

- Verify in proportion to changed risk at the smallest real operation boundary.
  A useful test protects durable behavior and fails when its regression returns.
- Reuse green evidence until a causal delta can invalidate it. Do not repeat broad
  gates merely because a commit, handoff, or review occurred.
- Every implementation receives one fresh inner review except a wholly
  non-generated, non-normative documentation diff that changes no executable,
  contract, setup, policy, architecture, verification, or operating behavior.
  Workflow and policy documents never qualify for that off-ramp.
- Review patches follow `REVIEW.md`'s approval-retention rule. When re-review is
  required, reuse the same reviewer; every outer-owned patch returns to its same
  outer reviewer.
- Treat summaries, receipts, and prior verdicts as claims to validate. Never claim
  verification, independence, or completion that the available host and evidence
  do not establish.

## Completion

Report the outcome, changed behavior, verification actually run, intentionally
unselected or blocked checks, documentation impact, review state, remaining
operator proof, and any real decision. Keep detailed evidence in its owner rather
than reprinting it by default.

When `HOST.local.md` configures a completion receipt store, a terminal
implementation or explicitly selected Explore, Spike, or prototype that produced
code, a durable artifact, or decision-relevant learning writes the best-effort
record in `RECEIPTS.md`; no other task creates a self-report. An explicitly
scoped follow-up may append a material sourced annotation to an existing receipt
without creating another self-report. Configuration authorizes only those bounded
local writes. Keep the durable self-report unchanged. Receipt absence, drift, or
write failure never blocks or replays work; report a skipped write once and
continue.
