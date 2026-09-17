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

### Routine plan maintenance

Within the configured plan area, local archival and current-index maintenance
are ordinary planning work; perform clear-cut updates without a separate cleanup
approval. Follow `WORKFLOW.md`'s planner ownership rule. Deletion and off-device
archival or publication remain separate actions under `KERNEL.md`.

Confirm completion, cancellation, or supersession from the owning evidence or
operator decision, never age or silence alone. Required review or proof still
owed keeps work open. Before retiring superseded work, carry any continuing
obligations to a named current owner. Record the final disposition, evidence
links, and continuing follow-ups in the existing plan; move the whole terminal
folder to the local archive without overwriting retained history, and update the
existing index and affected links in both moved and current documents. Keep a
path in place while a worker uses it unless that worker's handoff is coordinated.

Start routine retrieval from the current index or named active plans; consult
archives when historical evidence is relevant. Replace obsolete current-status
text in its existing owner and clearly identify superseded direction while
preserving decisions and evidence. Surface genuinely unclear dispositions for
operator resolution; continue independent work. Mention completed maintenance
briefly in the normal update without creating a cleanup report, ledger, or
mandatory lesson document. Bookkeeping gaps do not reopen valid verification or
block unrelated implementation.

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
