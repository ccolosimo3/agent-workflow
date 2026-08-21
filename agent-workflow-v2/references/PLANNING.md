# Agent Workflow V2 Planning Authority

This file owns durable planning quality, artifact policy, and phase inputs and
outputs. `WORKFLOW.md` owns whether a phase is selected; skills own only
phase-specific investigation.

## Proportional planning

- Casual questions, status checks, and compact option discussions stay in
  conversation and create no formal artifact.
- A formal explore, spike, or spec begins only after operator selection. Once
  invoked, preserve its compact result so downstream work does not recreate the
  evidence.
- Use the repository's declared plan location. If none exists, do not invent a
  tracked planning hierarchy; keep the result in the task until the operator
  chooses a durable location.
- A living work-item document is a decision/evidence index, not a transcript,
  status diary, or review log.

## Grounding and scope

Start from the raw operator outcome, current repository behavior, nearest owner
and complete pattern, relevant landed work, and only the external facts that can
change the decision. Separate verified facts, repository evidence, assumptions,
and unresolved decisions.

Map the broader destination when it helps sequencing, but fully authorize only
one independently reviewable risk boundary at a time. That Task must remain a
valid state if later work never lands. When one Task accumulates multiple
independently provable mechanisms or operational responsibilities, split or
simplify before review-ready. Keep together work whose separation creates an
invalid intermediate state or hides the real operation boundary.

## Minimum-sufficient shape

Before review-ready promotion, apply `KERNEL.md`'s minimum-sufficient check; it
governs speculative machinery as well as plan shape.

Architecture may describe the full destination while the current Task remains
small. Do not confuse physical line count with design size; larger work is valid
when required correctness, safety, or operational simplicity earns it.

## Implementation latitude

Specify observable behavior, owned contracts, non-goals, acceptance, and proof.
Name an implementation mechanism only when repository evidence or a real
constraint makes it load-bearing. The implementer may substitute a simpler
repo-conventional mechanism that preserves those contracts; it must return to
planning before changing observable outcomes, authority, safety boundaries, or
the Task's risk boundary.

## Phase inputs

Add only these facts to `WORKFLOW.md`'s shared handoff envelope:

- **Explore:** the open decision, credible options or unknown boundary, evidence
  gaps, and stop condition.
- **Spike:** the selected bet, falsifier, safe boundary, time/scope box, fallback,
  and exact approvals or prepared environment available.
- **Spec:** the raw outcome, known non-goals and decisions, current evidence and
  nearest owners/patterns, unresolved operator choice, and intended Task boundary.
- **Implementation:** selected route; converged spec or Fast ask; current Task,
  acceptance and non-goals; nearest owners/patterns; checkout/base ownership;
  named main-planner identity or none; approval state; verification routes; and
  remaining operator proof.

## Phase outputs

Use these as semantic contents, not mandatory verbose headings.

### Explore

- decision being informed and why it is open;
- evidence and source authority;
- credible options with tradeoffs and failure modes;
- recommendation and why alternatives lose;
- unresolved decision or evidence gap;
- recommended next phase, without starting it.

### Spike

- one bet, falsifier, and riskiest safe boundary;
- disposable method, time/scope box, fallback, and predeclared `GO` / `NO-GO`
  criteria;
- exact evidence produced;
- `GO`, `NO-GO`, or `BLOCKED` result and design implication;
- disposable artifacts retained or removed.

### Spec

- goal, non-goals, current behavior, and exact source-grounded evidence,
  including file:line for load-bearing repository claims;
- chosen approach, rejected alternatives and tradeoffs, design risks/edge cases,
  and real unresolved operator choices;
- one Task, its ordered implementation steps, behavioral acceptance criteria,
  affected owners/files, and valid intermediate state;
- minimum-sufficient implementation shape and permitted latitude;
- behavior/failure-mode test strategy, real operation boundaries, exact
  risk-selected verification, and remaining operator proof;
- UI strategy when a user-facing surface changes;
- approval-gated actions and documentation impact;
- downstream review and implementation handoff state, plus a concise
  tracker-ready summary when one is applicable.

Run a domain pass only when the work changes a core noun, lifecycle/state
meaning, user-facing terminology, service boundary, or cross-system contract.
Record canonical terms and real choices; do not create an architecture record for
ordinary local work.

## Review readiness

A spec is review-ready when load-bearing claims are grounded, no material
direction choice is hidden, acceptance is behaviorally testable, the Task is
right-sized and independently valid, verification can falsify the change, and
approval-gated actions are explicit. Review-ready does not mean approved or
authorized for implementation.
