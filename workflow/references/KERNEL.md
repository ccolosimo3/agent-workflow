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

Read-only inspection, public research, and ordinary in-scope development are
allowed. Follow documented routes to install pinned dependencies without changing
manifests or lockfiles, regenerate artifacts, and run local apps and tests.
Internal mechanism choices within authorized behavior need no direction approval.

Ordinary development includes repository-designated vendor sandbox/test/dev-tenant
calls and incidental license checks, plus creating, starting, migrating, seeding,
resetting, and removing disposable task environments. Resolve the actual target,
test namespace, and (for state changes) exclusive task ownership and known
synthetic/test-data provenance from checkout, configuration, and existing evidence;
ask only when these leave eligibility unsettled. Existing slots and manual-test
data qualify on that basis, not merely a "dev" label or idle service.
Sandbox calls stay within documented test operations, excluding shared account
changes, tenant-wide deletion, real messages, and real charges. Production,
staging, shared-app and primary-checkout data operations remain gated. Data
designations never override these protections.

Outside those bounds, get current-session operator approval before destructive
operations; dependency/lockfile/toolchain changes; handling real-data dumps or
uncertain data; pushes, publication, tracker/messages, deployments or
infrastructure mutations; other authenticated provider traffic, automated
live-source collection, and metered calls.
Preserve unrelated environments and unowned changes. History rewrite, force
operations, and safeguard bypasses require explicit approval; never bypass a
failed hook or policy check. State the exact target, scope, side effects, and
applicable spend bound before asking.

Selecting a configured host/profile through operator intent or a selected phase's
declared routing authorizes that bounded substep: work item, profile, invocation
count, and return condition. Subscription usage needs no separate approval or
dollar cap; metered/API-key usage still requires its usage or spend bound.
Required inner review and one outer selected by policy or the operator, with
their corrections and bounded unavailable-reviewer recovery under `REVIEW.md`,
are authorized substeps. Extra reviews, helper fan-out, unconfigured profile
changes, and unrelated paid activity remain gated.

Approval covers bounded corrections and retries within the same risk envelope;
failure or a changed artifact hash does not consume it unless explicitly made
single-use or revision-bound. Re-ask when target, scope, side effects, provider,
input scope, or cap materially changes. Silence or ambiguous assent is not
approval. Resolve factual uncertainty with instructions, inspection, or the
smallest safe observation;
choose the simplest reversible in-scope mechanism and report the assumption.
Ask about unsettled observable behavior, Task/risk boundaries, authority, spend,
safety, or difficult-to-reverse state. Neither reversibility nor a spec's own
reasoning grants gated authority; operator-approved conditions plus evidence can.

When workflow guidance causes a question, pause, or unfinished requested work,
link the exact instruction and quote the relevant clause; distinguish an explicit
requirement from your interpretation. Continue independent authorized work while
the gated action or material decision waits.

Never commit secrets, credentials, private operator adapters, personal paths, or
other untracked local configuration.

## Minimum-sufficient quality

- Choose the simplest complete repository-conventional shape. Before review-ready
  planning or materially expanding implementation, compare outcome and non-goals,
  correctness and safety constraints, nearest complete pattern, added
  responsibilities, state, artifacts and operator steps, reuse, and proven consumers.
- Apply that comparison to proof code. If a harness becomes materially broader or
  owns more contract/lifecycle behavior than the product delta, stop and reduce it
  to the smallest causal boundary using existing production owners.
- Added durable machinery must trace to a current requirement, observed failure,
  established pattern, or second real consumer. Prevent recurring corrections at
  the lowest reliable existing owner (type/API, runtime guard, or static/CI check)
  rather than adding workflow prose; out-of-scope promotion remains separate work.
  Larger designs are valid when required by those constraints or operationally
  simpler.
- Missing or stale workflow metadata does not invalidate valid work or force replay
  unless it protects target identity, approval, authority, product integrity, or a
  causal dependency. Revalidate only the smallest affected behavior; bookkeeping
  repair cannot replace implementation or evidence.
- Planner-authored invariants are not independent authority. Before adding durable
  state or recovery for an exceptional retry or manual fallback, compare handling
  it through the existing path.
- Preserve observed behavior and public contracts outside the intended change
  unless changing them is necessary to satisfy the ask. Reuse existing owners;
  keep task-local code limited to task-specific behavior.
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
- Review patches follow `REVIEW.md`'s approval-retention and recovery rules. Reuse
  the same reviewer; every outer-owned patch returns to its outer gate.
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
