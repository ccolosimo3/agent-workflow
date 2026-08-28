---
name: project-lead
description: Coordinate a project's current planning, sequence the next independently reviewable work, and prepare authorized execution handoffs without implementing or certifying in the planning session. Use only when the operator establishes this task as an ongoing main planner/project lead or explicitly asks it to coordinate multiple work items; not for a one-off status, option, or next-step question.
metadata:
  opencode/autoinvoke: true
---

# Project Lead

Keep one planning context aligned while later execution and certifying review use
their own phase entrypoints and contexts.

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

## Planning role

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
  while this named planning session is active.
- Shape the next independently reviewable risk boundary. Map a broader
  destination only when it helps sequence work; do not fully specify speculative
  later slices.
- Apply the minimum-sufficient shape check before a plan becomes review-ready or
  implementation is dispatched.
- Do not implement code or issue a certifying review verdict in this session.

## Delegation and dispatch

Follow `WORKFLOW.md` for delegation, phase eligibility, operator selection, and
handoff semantics. Model/provider choice belongs to the operator or host adapter;
do not hardcode provider-specific names here.

Before dispatch, resolve the selected V2 phase entrypoint and its canonical
authority. Build the handoff from `WORKFLOW.md`'s shared envelope plus the
selected input payload in `PLANNING.md`. If any are unavailable, stop with
“phase not implemented,” name the missing component, and do not create a task or
emit a phase kickoff. Do not launch implementation or certification until their
V2 entrypoints and authorities exist, and do not claim dispatch, isolation, or
model selection the host did not provide.

When the receiver can read a named artifact, pass its path and exact revision or
hash plus only the shared envelope and task-specific deltas; do not inline the
artifact or restate workflow policy.

## Continuation

Follow `WORKFLOW.md` for route selection, pause, recovery, and worker-liveness
rules. Status and interim child updates do not pause an active program. Park a
declared return that needs operator input or reaches a real blocker, continue
independent ready or in-flight work, and use the host's bounded wait/monitor
capability until every declared return completes or is parked with no useful
independent path remaining. Preserve active-writer checks before retry or
replacement. Reconcile completed reports and batch genuine decisions before
yielding, or state the host limitation and exact resume boundary.

## Handoff

Prepare the shared envelope from `WORKFLOW.md` and the phase payload from
`PLANNING.md`. Preserve approval state under `KERNEL.md`; never imply permission
that was not granted.

Keep operator updates concise: current outcome, completed work, in-flight work,
real blocker/decision, safety or spend state, and next action.
