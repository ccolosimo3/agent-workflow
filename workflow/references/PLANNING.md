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
- A living work-item document is a decision/evidence index, not a transcript,
  status diary, or review log.
- Required verification evidence belongs in the work item or its existing evidence
  owner. Capture exact commands and results there during execution. The optional
  completion receipt may summarize or point to that evidence; its formatting,
  schema, availability, or exhaustive contents must not become Task acceptance.

## Plan storage

Use the repository's declared plan location. When durable planning is first
needed and none is configured, offer one-time initialization of the private,
repo-local default `.agent-workflow/plans/`, excluded through the repository's
local Git configuration. The operator may instead choose a tracked or custom
location, or no durable storage. Preview the directory, exclusion, and adapter
change before writing; never create or track a plan area silently.

Record the resolved location and visibility in the repository adapter and reuse
it without asking again. Keep one living Markdown work item under
`active/<short-name>/README.md`, move terminal work to `archive/`, and add an
`INDEX.md` or other buckets only when real coordination needs them. Casual work
does not trigger storage setup.

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

Right-size the proof with the implementation: apply `TESTING.md` to proposed
cases, reuse existing coverage, and justify heavier harnesses by the distinct
behavior only that boundary can prove. A spec must not turn a list of internal
permutations into required tests. Keep unavailable real-boundary proof explicit
instead of declaring a substitute harness or shape assertion sufficient.

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

For Explore and Spike, distinguish the exact proposition the evidence supports
from the stronger behavior that remains unproved. Carry those limits into the
next Task: feasibility of an underlying tool does not qualify an unexercised
production wrapper, lifecycle, or platform.

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
direction choice is hidden, and consequential behavior choices are settled by
the request, established requirements, or an explicit operator decision.
Acceptance is behaviorally testable, the Task is
right-sized and independently valid, verification can falsify the change, and
approval-gated actions are explicit. Review-ready does not mean approved or
authorized for implementation.
