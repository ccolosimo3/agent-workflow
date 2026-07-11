---
name: orchestrate
description: Coordinate an explicitly authorized multi-task engineering program through planning, fresh user-visible Codex desktop task dispatch, implementation, verification, review convergence, integration, recovery, and the furthest authorized completion gate. Use only when the operator invokes /orchestrate or unmistakably asks one coordinator to drive a multi-work-item program end to end. Not for one-item planning, implementation, review, status reporting, generic parallel research, or subagent workflows.
---

# Orchestrate

Act as the program control plane over the existing kernel roles. Do not replace
planning, implementation, or review. Do not implement child work by default.

This staged V0 is noncanonical. Refuse activation/install work unless the
operator separately approves the reviewed activation candidate.

## Read First

Read completely:

- `~/.agents/workflow/AGENTS.md`
- `~/.agents/workflow/ORCHESTRATOR_MODE.md`
- `~/.agents/workflow/HANDOFF.md`
- the repo's nearest shim and planning/verification authorities
- [ledger-schema.md](references/ledger-schema.md)
- [assignment-and-status.md](references/assignment-and-status.md)

## Intake And Authority Lock

1. Confirm the explicit program goal, non-goals, done definition, repositories,
   delivery shape, and integration owner.
2. Record allowed, approval-gated, and forbidden actions. Enumerate the phase
   transitions pre-authorized by this invocation. Unlisted transitions remain
   operator gates.
3. Confirm desktop-task creation, target project/local environment, one-writer
   ceiling, read-only task ceiling, retry/time/traffic/spend limits, and stop
   conditions.
4. Inspect the current host's desktop task-creation contract. Require explicit
   `model` and `thinking` controls; never fall back to subagents.
5. Show detected exact model IDs/reasoning levels. Confirm manual or auto routing,
   quality bias, allowed routes, ceilings, pins, prohibitions, and fallback.
6. Initialize the program ledger with `scripts/init_program.py`. The coordinator
   is its sole logical writer.

## Routing

Use portable route classes mapped to detected model IDs:

- `fast`: deterministic/mechanical; Luna medium, or high for multi-step work.
- `balanced`: routine engineering; Terra high by default, xhigh when complexity or convergence evidence justifies it.
- `deep`: ambiguous/high-risk/certifying; Sol medium or high by default.

Sol and Terra cap at `xhigh`; Luna caps at `high`. Never select `xhigh` merely
because it exists. Require exceptional novelty, broad high-stakes coupling,
repeated non-convergence, or equivalent evidence and record the justification.
Never use `fast` for certifying review or security/auth/data-loss/migration/
provider work.

## Graph, Readiness, And Dispatch

1. Decompose into independently reviewable work items and integration proof.
2. Do not dispatch implementation before Definition of Ready and environment
   attestation pass.
3. Use fresh user-visible Codex desktop tasks for every worker and reviewer.
   Create them with the confirmed project/local target, populated canonical
   kickoff, exact `model`, and exact `thinking`.
4. Keep one implementation writer active. Read-only desktop tasks may run within
   the confirmed ceiling. V0 does not use implementation worktrees.
5. Record task ID, request/result, route attestation, assignment generation,
   owned paths, authority delta, leases, and terminal-report contract.
6. Monitor through task list/read operations. Steer or re-review by sending a
   follow-up to the same task ID. Archive only after durable reconciliation.

## Active Control

- Record every state-changing action through `scripts/record_event.py` with the
  expected predecessor hash and coordinator generation.
- Treat worker reports as claims until reconciled against files, git state,
  commands, and review evidence.
- Answer status or side-documentation messages, append `status_reported`, and
  immediately continue the next safe action unless the operator explicitly
  pauses/replaces the goal or opens a real gate.
- A quiet task triggers inspection, not replacement.
- On recovery: inspect → steer original task once → persist handoff → fence old
  assignment/leases → create exactly one replacement → re-run stale evidence.
- A route override increments assignment generation and fences the old route.

## Verification, Review, And Integration

- Child tasks own slice-local verification and the mandatory inner review loop.
- Create exactly one fresh reviewer Codex task for each review unit. Continue the
  same task for re-review; replace only after it is fenced and unreachable.
- Record exact base/tip, reviewer task ID, verdict, and freshness.
- A changed tip, topology, contract, or environment invalidates dependent proof.
- A combined delivery with cross-child/integration behavior is a distinct
  integrated-candidate review unit.
- The outer gate remains operator-owned and must certify the exact final tip.
- Push, PR, tracker, deployment, live/provider, paid, destructive, or external
  delivery remains separately approval-gated by the kernel/repo policy.

## Stop Contract

Stop only at the furthest authorized done state, an ungranted authority or phase
gate, a credential/directional conflict, exhausted bounded recovery with no safe
independent work, or explicit pause/replacement/cancellation. Never call blocked
work complete or treat an informational exchange as a pause.

Return operator status in the exact shape in
[assignment-and-status.md](references/assignment-and-status.md).

## Scripts

- `scripts/init_program.py`: initialize the authoritative event log.
- `scripts/record_event.py`: lock, validate, CAS, append, and materialize views.
- `scripts/validate_program.py`: detect stale views or rebuild them at startup.
- `scripts/render_status.py`: render the compact operator view.
- `scripts/validate_host_evidence.py`: reconcile desktop task operations to
  ledger events.
