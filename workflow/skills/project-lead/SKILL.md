---
name: project-lead
description: Lead a project's planning and authorized execution, continuing bounded work here or coordinating workers for a broader program. Use when established as the project lead or asked to coordinate multiple work items; not for a one-off status or advice question.
metadata:
  opencode/autoinvoke: true
---

# Project Lead

Keep scope, decisions, evidence, and current plans aligned through delivery.
Use the phase skills for work performed here or delegated under `WORKFLOW.md`.

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Before substantive work, read these files completely relative to this skill:

- `../../references/KERNEL.md`
- `../../references/WORKFLOW.md`
- `../../references/PLANNING.md`

If any file cannot be resolved, stop and report that V2 is incomplete. Do not
fall back to partial legacy or improvised semantics.

Then read the repository's instruction chain and any declared repo adapter. Repo
facts may narrow execution but cannot widen the V2 kernel's approval or review
requirements.

## Lead the work

Confirm the operator established this task as the main planner/project lead or
explicitly requested multi-item coordination; otherwise answer directly without
assuming shared program ownership or dispatching.

- Get current from the repository's concise status, roadmap, active plans, recent
  landed work, and exact checkout state. Follow owner routes instead of reading
  every document.
- Resolve `PLANNING.md`'s configured plan location before durable planning
  writes. Trigger its one-time setup only when no location exists and an artifact
  is actually needed; ordinary questions and status checks continue without it.
- Own the program map, sequencing, dependencies, and operator-facing decisions
  while this lead task is active. Maintain one current summary per
  purpose in its existing owner; other entrypoints link to it. During a material
  reconciliation, update that summary in place rather than appending another
  "current" section. Replace superseded status with links to retained decisions
  and evidence, preserving active scope, approvals, unresolved proof, and
  worker/reviewer ownership.
- Apply `PLANNING.md`'s routine plan maintenance after reconciling terminal work,
  before reporting closeout. On takeover, make a bounded pass through the
  current index or active plans for completed, cancelled, or superseded work left behind;
  during material planning updates, reconcile stale state encountered there.
  Stay within this project's planning ownership; do not rescan the archive or
  turn every status check into a cleanup sweep.
- Shape the next independently reviewable risk boundary. Map a broader
  destination only when it helps sequence work; do not fully specify speculative
  later slices.
- Apply the minimum-sufficient shape check before a plan becomes review-ready or
  implementation begins.
- For a bounded item, continue authorized planning and implementation here by
  invoking the applicable phase skill. Default to coordination for a broader
  program; delegate when `WORKFLOW.md` warrants it. Never certify your own work.
- Reconcile worker results against scope, candidate identity, required evidence,
  and the next decision. Check load-bearing claims; do not repeat the worker's
  full investigation or green checks without a concrete inconsistency or causal
  delta. Independent certifying review remains with its assigned reviewer.

## Work here or delegate

`WORKFLOW.md` owns phase selection, same-task continuation, host/profile choice,
and dispatch. Use the phase skill's input and output requirements; resolve its
entrypoint and authorities before starting. Missing capability or authority is a
specific blocker, not permission to improvise a phase or claim a launch.

Choose the profile for the remaining work: a demanding design can leave a simple
implementation. Do not dispatch merely to change phase or obtain stronger
reasoning when supported same-task controls suffice. Follow explicit operator
assignments and host capability limits.

When dispatching, pass the shared handoff facts, source artifact links, and only
phase-specific deltas. Keep one owner per checkout and confirm an existing writer
is inactive before replacing it. Reuse the worker for its correction loop; relay
changes to behavior, scope, acceptance, authority, or risk. Routine wording and
status changes need no reapproval or pause. Reviewers remain independent and
retain their own correction loops.

## Continuation

Use continuous coordination below unless the operator selects scheduled
coordination. A scheduled pass has its own yield boundary as defined below.

Follow `WORKFLOW.md` for route selection, pause, recovery, and worker-liveness
rules. Status and interim child updates do not pause an active program. Park a
declared return that needs operator input or reaches a real blocker, continue
independent ready or in-flight work, and use the host's bounded wait/monitor
capability until every declared return completes or is parked with no useful
independent path remaining. Preserve active-writer checks before retry or
replacement. Reconcile completed reports and batch genuine decisions before
yielding, or state the host limitation and exact resume boundary.
When no independent work advances the program, wait for a meaningful worker
change using the host's bounded wait capability. Prefer compact status snapshots
to transcript rereads; do not poll or replan repeatedly on unchanged state.

### Scheduled coordination

Activate only when the operator requests heartbeat or scheduled project
leadership. During setup, use the host's supported scheduler to create or update one heartbeat
in this existing planner task; reuse a matching schedule instead of duplicating
it. Preserve the requested cadence, or default to every 30 minutes. Do not create
a standalone task or polling-loop substitute when same-task scheduling is
unavailable; report the host limitation.

Before activating, check for a continuous goal on this planner. Use supported goal
controls to pause it when the operator selected this switch; if the host cannot,
ask the operator to pause it and leave activation pending. Never mark an unfinished
goal complete or blocked to stop its continuations. Preserve worker goals.

The saved prompt invokes `project-lead` in scheduled coordination mode and names
the project, existing planner, authorized scope, and agreed milestone or stop
condition. Use host workload preferences; scheduling grants no additional phase,
dispatch, review, or external-action authority. Verify the scheduler's returned
target and cadence before claiming activation.

On each wake, start with compact worker/status checks; expand only for changed
state or a load-bearing uncertainty. Reconcile results and advance ready authorized
planning or handoffs. Once only waiting or blocked paths remain, end the turn;
this is the agreed checkpoint under `WORKFLOW.md`, not a reason to wait inside the
run. Preserve active-writer checks and existing evidence/reviewer ownership.
Stay quiet on unchanged, non-actionable state; report meaningful progress,
completion, failure, or a required decision. Pause the heartbeat when its agreed
stop condition holds or the operator stops it; ordinary wakes do not repeat setup
or refresh the schedule.

## Handoff

Keep operator updates concise: current outcome, completed work, in-flight work,
real blocker/decision, safety or spend state, and next action.
