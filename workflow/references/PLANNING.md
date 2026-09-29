# Agent Workflow V2 Planning Authority

This file owns shared planning quality and artifact policy. `WORKFLOW.md` owns
phase selection and handoffs; each phase skill owns its inputs, process, and result.

## Proportional planning

- Casual questions, status checks, and compact option discussions stay in
  conversation and create no formal artifact.
- A formal explore, spike, or spec begins only after operator selection. Once
  invoked, preserve its compact result so downstream work does not recreate the
  evidence.
- A living work-item document is a decision/evidence index, not a transcript,
  status diary, or review log.
- Required verification evidence belongs in the work item or its existing evidence
  owner. Capture exact commands and results there during execution. The optional
  completion receipt may summarize or point to that evidence; its formatting,
  schema, availability, or exhaustive contents must not become Task acceptance.
- Keep raw CLI responses, stdout/stderr, and test captures in ignored task-local
  scratch storage. Retain findings, candidate and reviewer/session identity,
  resolutions, and unique required proof in the existing evidence owner. Preserve
  recovery inputs while work is open; at closeout, remove only task-owned disposable
  output after retaining required proof. Do not create separate durable files for
  every payload, result, stderr stream, or exit code by default.

## Plan storage

Follow the repository's declared planning location, owners, layout, and lifecycle,
including shared or external repositories. If durable planning needs a location
and none is configured, use `setup-workflow`'s Repository onboarding; do not create
or track a plan area silently.

### Routine plan maintenance

Local archival and index updates are ordinary planning work under `WORKFLOW.md`'s
ownership rule. Confirm terminal status from evidence or an operator decision;
age, silence, or missing bookkeeping is insufficient. Required proof/review keeps
work open. Carry continuing obligations to a named owner, retain disposition and
evidence in the existing plan, then follow its archive lifecycle. For the default
layout, move the whole folder to `archive/` and fix affected links. Coordinate
before moving a path an active worker uses. Deletion and off-device publication
follow `KERNEL.md`.

Retrieve from the current index or named active work; consult archives as needed.
Replace obsolete status in its owner, preserving decisions/evidence and marking
superseded direction. Ask only about genuinely unclear dispositions; maintenance
neither creates a report/ledger nor reopens valid verification or blocks unrelated
work.

## Grounding and scope

Start from the raw operator outcome, current repository behavior, nearest owner
and complete pattern, relevant landed work, and only the external facts that can
change the decision. Separate verified facts, repository evidence, assumptions,
and unresolved decisions.

Establish which outcomes the request intends to improve and which should remain.
For consequential workflow or contract changes, trace representative everyday
scenarios at the affected boundary and explain meaningful before/after differences
in the existing plan or conversation; do not require an exhaustive compatibility
inventory. Preserve established behavior outside the intended change by default,
but do not reject a proposed improvement merely because it changes that behavior.

When the request or established requirements leave a consequential choice
unsettled—capabilities, familiar defaults, required user steps, data treatment,
compatibility, or meaningful failure/recovery behavior—present the current and
proposed behavior, expected benefit, tradeoff, and recommendation to the operator
before committing dependent planning or implementation. A broad goal such as
"improve local development" does not settle every such tradeoff. Equivalent
internal mechanisms, ordinary fixes to a known contract, and behavior already
selected by the operator need no new direction approval; `KERNEL.md` still governs
execution permissions.

Resolve factual uncertainty through evidence. Keep remaining recommendations
distinct from operator decisions in the existing work item and handoff: neither
writing a choice into a spec nor another agent's agreement authorizes it. Workers
return these choices through the named planner, who asks the operator rather than
deciding on their behalf; without a planner, ask directly. Batch focused questions
as they become material and continue independent authorized work while awaiting
answers.

Map the broader destination when it helps sequencing, but fully authorize only
one independently reviewable risk boundary at a time. That Task must remain a
valid state if later work never lands. When one Task accumulates several
materially independent risks or operational responsibilities, split or simplify
before review-ready. Keep together work whose separation creates an invalid
intermediate state or hides the real operation boundary.

## Minimum-sufficient shape

Before review-ready promotion, apply `KERNEL.md`'s minimum-sufficient check; it
governs speculative machinery as well as plan shape.

Before expanding a spec around compatibility, recovery, durable state, or a fixed
mechanism, identify the supported contract/caller/state, explicit operator
requirement, or observed failure that makes that costly obligation necessary.
Use a concrete example when available; a supported contract or approved future
requirement remains valid without a local sample. Keep unsupported planner
assumptions visible as hypotheses and compare the existing ordinary path before
turning them into acceptance criteria. Record this reasoning in the existing
decision or tradeoff, not a separate constraint ledger.

Architecture may describe the full destination while the current Task remains
small. Do not confuse physical line count with design size; larger work is valid
when required correctness, safety, or operational simplicity earns it.

When designing verification, read `TESTING.md` and apply its proof-planning,
durable-value, and inclusion rules before making cases mandatory. Keep unavailable
real-boundary proof explicit; a substitute harness or shape assertion cannot
discharge it.

## Implementation latitude

Specify observable behavior, owned contracts, non-goals, acceptance, and proof.
Name an implementation mechanism only when repository evidence or a real
constraint makes it load-bearing. The implementer may substitute a simpler
repo-conventional mechanism that preserves those contracts; it must return to
planning before changing observable outcomes, authority, safety boundaries, or
the Task's risk boundary.

For a new or materially changed shared API, package, or service boundary,
specify representative caller usage and failure behavior before choosing internal
structure. Keep implementation-specific coordination and state with their owner;
repeated caller workarounds or inputs required only to accommodate internals are
evidence to reconsider the boundary.

## Review readiness

A spec is review-ready when load-bearing claims are grounded, no material
direction choice is hidden, and consequential behavior choices are settled by
the request, established requirements, or an explicit operator decision.
Acceptance is behaviorally testable, the Task is
right-sized and independently valid, verification can falsify the change, and
approval-gated actions are explicit. Review-ready does not mean approved or
authorized for implementation.
