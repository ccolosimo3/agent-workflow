---
name: v2-plan-next
description: Coordinate a project's current planning, sequence the next independently reviewable work, and prepare authorized execution handoffs without implementing or certifying in the planning session. Use for an ongoing main planner or a request to decide and coordinate what should happen next.
---

# V2 Plan Next

Keep one planning context aligned while later execution and certifying review use
their own phase entrypoints and contexts.

## Required authorities

Before substantive work, read these files completely relative to this skill:

- `../../references/KERNEL.md`
- `../../references/WORKFLOW.md`
- `../../references/PLANNING.md`

If any file cannot be resolved, stop and report that V2 is incomplete. Do not
fall back to partial V1 or improvised semantics.

Then read the repository's instruction chain and any declared repo adapter. Repo
facts may narrow execution but cannot widen the V2 kernel's approval or review
requirements.

## Planning role

- Get current from the repository's concise status, roadmap, active plans, recent
  landed work, and exact checkout state. Follow owner routes instead of reading
  every document.
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

## Continuation

Follow `WORKFLOW.md` for route selection, pause, recovery, and worker-liveness
rules. A status question, informational message, or completed child report does
not pause an active program; incorporate it and continue safe authorized planning.

## Handoff

Prepare the shared envelope from `WORKFLOW.md` and the phase payload from
`PLANNING.md`. Preserve approval state under `KERNEL.md`; never imply permission
that was not granted.

Keep operator updates concise: current outcome, completed work, in-flight work,
real blocker/decision, safety or spend state, and next action.
