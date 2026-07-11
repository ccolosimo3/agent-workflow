# Orchestrator V0 Ledger Schema

## Contents

1. Source of truth
2. Core entities
3. Generations and fencing
4. Event commit and recovery
5. State and freshness rules

## Source Of Truth

`events.jsonl` is the sole operational authority. `program.json`,
`approvals.json`, and `status.md` are deterministic views. Each event carries a
contiguous ID, predecessor hash, coordinator generation, topology revision, actor,
state transition, payload, invalidations, and SHA-256 hash.

## Core Entities

- Program: goal, state, done definition, authority, topology, next action.
- Work item: task state, dependencies, paths, verification, current tip.
- Assignment: assignment ID/generation, Codex task handle, model route.
- Approval: exact action, target/effect/cap/expiry, consumption state.
- Lease: kind/scope/holder/generation/state/heartbeat/expiry; acquisition must
  match the current unfenced assignment and fall within declared owned paths.
- Environment attestation: checkout/base/tip/topology/assignment generation,
  tools/ignored inputs/smoke/clean state, and freshness.
- Verification record: declared command, passed result, exact tip/environment,
  assignment/topology binding, task owner, and freshness.
- Review record: review unit and role, reviewed task, reconciled reviewer
  assignment/task handle, base/tip, verdict, and freshness.
- Integration candidate: frozen child tips, merge order, gates, review IDs.
- Recovery: old/new assignment, fencing, preserved evidence, reason.

## Generations And Fencing

- `coordinator_generation` starts at 1 and increments on coordinator replacement.
- `assignment_generation` starts at 1 and increments on replacement, ownership
  transfer, or active model/reasoning override.
- `dispatch_intent_recorded` reserves the next generation and a stable
  `idempotency_key` before desktop task creation. `assignment_started` must
  reconcile that exact key. An unresolved intent blocks another create until
  host history proves whether the earlier create was accepted.
- `model_routing.policy_revision` starts at 1 and increments whenever the
  confirmed route pool, ceilings, bias, pins, prohibitions, or fallback changes.
- Mutations/reports carrying stale generations fail closed.
- `assignment_continued` advances the generation while proving exact task-handle
  reuse; it does not create a new desktop task and therefore needs no dispatch
  intent.

## Event Commit And Recovery

Every mutating CLI acquires `.events.lock` with `fcntl.flock`, rereads and
validates the log, checks expected predecessor hash and coordinator generation,
renders the complete candidate log, fsyncs, and atomically replaces it. Views are
then rebuilt atomically. Startup rebuilds stale views from a valid log. A corrupt
log blocks; it is never reconstructed from chat or a stale view.

## State And Freshness Rules

Legal transitions are defined in `ORCHESTRATOR_V0_SPEC.md` and implemented by the
validator. Unlisted transitions fail. Exceptional states retain a nonexceptional
resume state. Terminal states do not reopen except `failed`, which requires an
explicit retry grant and non-bypassing retry anchor.

Tip, topology, acceptance-contract, environment, route-policy, or assignment-
generation changes invalidate dependent evidence. A stale review never certifies
an integration candidate. Candidate certification requires the exact declared
verification-command set for the reviewed task, passed/current records on the
candidate tip, an inner reviewer distinct from the implementation task, and—at
`outer_approved`—a second review record with a distinct outer reviewer identity.
All three derived views are compared byte-for-semantics against replayed state;
an anchored but altered JSON view or any changed `status.md` is stale.
