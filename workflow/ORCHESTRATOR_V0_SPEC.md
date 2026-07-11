---
title: Define Orchestrator Mode And Orchestrate Skill V0
status: review-ready
created: 2026-07-10
updated: 2026-07-10
owner: operator
issue: none
pr: none
related:
  - ORCHESTRATOR_MODE.md
  - AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md
  - WORKTREE_ENVIRONMENT_BOOTSTRAP.md
  - COMMAND_GUARDRAILS_AND_VERIFICATION_HOOKS.md
  - AGENTS.md
  - HANDOFF.md
  - PLANS.md
---

# Define Orchestrator Mode And Orchestrate Skill V0

## Metadata

- Type: Workflow architecture and safe offline pilot
- Activation state: draft only; not canonical policy and not an installed skill
- Spec-review freshness: APPROVED on 2026-07-10 after the operator-directed
  desktop-task/model-routing revision and one original-reviewer re-review;
  operator amendment caps both Sol and Terra at `xhigh`
- Execution mode: documentation, local validation fixtures, and an offline serial
  pilot only until the operator approves activation
- Source: the first autonomous orchestration experiment, current kernel
  contracts, and official Codex documentation checked 2026-07-10

## Recommendation

Build V0 as a small, explicit coordinator control plane over the existing
planning, implementation, and review roles. Put durable invariants in
Orchestrator Mode and invocation/ledger/dispatch mechanics in `/orchestrate`.
Use a coordinator-owned, versioned file ledger as the source of truth.

V0 defaults to fresh user-visible Codex desktop tasks with serial implementation
in one coordinator-attested prepared local checkout. Read-only desktop tasks may
run concurrently within the confirmed ceiling; only one implementation writer is
active at a time. V0 does not use subagents. Parallel implementation worktrees
and shared-worktree multi-writer execution remain disabled until a separate
readiness pilot proves environment and verification parity.

This is deliberately narrower than the current draft. The first experiment
supports the control-plane role, exact authority boundaries, review freshness,
and persistent state. It does not prove durable session resumption, transferable
approvals, crash-proof background execution, or worktree parity.

## Evidence Classification

The design uses three evidence classes. No hypothesis may be presented as a
platform guarantee.

### Verified Codex capabilities

- Long-running Goal mode accepts steering and status messages in the same task;
  starting a goal does not broaden sandbox or approval authority. Independent
  parallel tasks should not write the same source. See [Long-running
  work](https://learn.chatgpt.com/docs/long-running-work).
- Subagents are delegated agent threads whose results return to the parent.
  Codex supports spawning, follow-up routing, waiting, inspection, stopping, and
  closing. Official guidance favors read-heavy parallelism and warns about
  parallel writers. Subagents inherit the parent permission mode and tools. See
  [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- Projects organize related tasks and context; they are not a transactional
  program coordinator. See [Projects, chats, and
  tasks](https://learn.chatgpt.com/docs/projects).
- Desktop Codex supports local and worktree task environments and Local ↔
  Worktree handoff. Managed worktrees still need dependencies and tools, and
  ignored inputs require explicit handling. See [Codex
  environments](https://learn.chatgpt.com/docs/environments/modes), [Local
  environments](https://learn.chatgpt.com/docs/environments/local-environment),
  and [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees).
- Sandbox and approval policy are separate controls. A goal, skill, or
  coordinator cannot expand either. See [Sandbox](https://learn.chatgpt.com/docs/sandboxing)
  and [Agent approvals &
  security](https://learn.chatgpt.com/docs/agent-approvals-security).
- Skills package reusable workflows; `AGENTS.md` supplies durable scoped
  instructions. Canonical kickoff fidelity and reviewer reuse are local kernel
  contracts, not Codex primitives. See [Build
  skills](https://learn.chatgpt.com/docs/build-skills) and [Custom instructions
  with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Command rules are experimental prefix rules. Hooks can observe lifecycle
  events and block some tool calls, but official documentation says
  `PreToolUse` interception is incomplete. They are defense in depth, not the
  V0 safety boundary. See [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)
  and [Hooks](https://learn.chatgpt.com/docs/hooks).

### Current-host observations, not portable guarantees

On 2026-07-10 this Codex desktop session exposes tools to create, fork, list,
read, message, hand off, rename, pin, and archive user-visible tasks. The tool
contracts also say:

- creating a separate task requires an explicit user request;
- task creation accepts explicit `model` and `thinking` arguments. This host
  advertises `gpt-5.6-sol` and `gpt-5.6-terra` with low through ultra, and
  `gpt-5.6-luna` with low through max;
- follow-up messaging can preserve or explicitly override model/reasoning;
- forks copy completed history only, not an active unfinished turn;
- handoff interrupts the destination task, cannot move the caller itself, and
  does not support cloud handoff;
- no general arbitrary-task interrupt tool is exposed;
- thread heartbeats and standalone recurring jobs are distinct mechanisms.

The skill must capability-detect these operations and record their actual
result. Desktop-task creation/list/read/message plus explicit route controls are
V0 prerequisites; if absent, V0 reports unsupported and does not degrade to
subagents or advisory routing.

### Local workflow evidence

- Central safety, ownership, verification, and integration state preserved the
  authority boundary and improved recovery in the Wave A experiment
  (`AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`, “What Is Working Well”).
- Status exchanges caused avoidable pauses even though no gate existed
  (`AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`, “Operator identified avoidable
  pauses”).
- Visible task history did not imply resumability; a replacement reviewer was
  required (`AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`, “Resume, stale-review
  recovery, and current-main refresh”).
- Child review plus child tests did not replace a holistic integrated-candidate
  review (`AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`, “Holistic review caught
  cross-slice risks child review missed”).
- Fresh worktrees repeatedly lacked ignored dependencies or representative
  inputs and produced misleading failures. The operator paused worktree
  parallelism as a default (`WORKTREE_ENVIRONMENT_BOOTSTRAP.md` and
  `AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`, “Worktrees paused as a default
  execution mode”).

### Design hypotheses to test

- A versioned event ledger plus snapshots can recover a program after context
  loss without reconstructing authority or review state from chat.
- A serial-first coordinator can remove avoidable pauses without increasing
  operator repair work.
- Event-driven heartbeats are sufficient for V0; wall-clock monitoring and
  scheduled wakeups are optional topology capabilities.
- A distinct integrated-candidate review unit preserves the one-reviewer rule
  while covering cross-child behavior.

## Assessment Of The Existing Draft

### Sound

- The role split is correct: orchestration owns the program control plane, not a
  larger version of implementation.
- Explicit entry, a non-expanding authority envelope, and compact operator
  status are necessary.
- The serial prepared-checkout default matches current evidence.
- Environment failure is distinct from product failure; blocked verification is
  never success.
- Exact-tip verification, original-reviewer re-review reuse, replacement only
  after failed reuse, and outer-review independence must remain unchanged.
- Informational messages are steering/status, not an implicit pause.

### Underspecified

- The listed ledger fields do not define enumerated states, transition owners,
  invalidation, event ordering, schema versioning, or recovery.
- Approval records lack action-instance identity, exact target/effect, expiry,
  consumption, and a prohibition on reusable authority tokens.
- Leases lack acquisition, exclusivity, renewal, fencing, expiry, revocation,
  and replacement semantics.
- Session visibility and resumability are conflated.
- The proposed program folder is not reconciled with `PLANS.md`'s one-folder-per-
  work-item model.
- “Mechanical integration” does not distinguish conflict resolution, generated
  artifacts, integration bug fixes, and ordinary merges.
- Child review, integrated-candidate review, and final-tip outer review are not
  expressed as separate review units.
- Heartbeats are described as if a durable timer exists.
- Pilot success and rollback thresholds are not falsifiable.

### Conflicts With Current Kernel Contracts

- `HANDOFF.md` says the operator owns planning/build phase transitions. A broad
  end-to-end mandate may pre-authorize named transitions, but the orchestrator
  cannot infer unlisted transitions.
- The `spec` skill ends before automatic spec review or promotion. An
  orchestration caller contract must permit review convergence while preserving
  the operator-owned `final`, tracker-publication, and implementation gates.
- `PLANS.md` requires operator approval before `final`; review-clean is not the
  same as final or promoted.
- `HANDOFF.md` allows one fresh reviewer per review unit. A holistic program
  review must be declared as the review of a distinct integrated candidate, not
  silently added as a second reviewer of a child.
- `outerreview` is operator-owned and runs in a different app/model. V0 prepares
  and pauses at that gate unless the invocation explicitly includes a supported
  operator-owned route; it never self-certifies the outer gate.
- `AGENTS.md` explicitly leaves Orchestrator Mode inactive. Draft artifacts and
  pilots cannot alter that state.
- Command guardrails remain a separate future spec. V0 has procedural approval
  enforcement and audit records only.

## Domain Pass

Decision: required and completed. This work introduces a mode, authority/state
meanings, and cross-task lifecycle nouns. No ADR is warranted before the pilot
because V0 is explicitly reversible and noncanonical.

Canonical terms:

| Term | Meaning |
| --- | --- |
| Program | One explicitly authorized multi-work-item outcome with one authority envelope and done definition |
| Orchestrator | The coordinator Codex task that is the sole control-plane and ledger owner |
| Work item | A planned deliverable such as a spec or implementation slice; distinct from a Codex desktop task |
| Codex task | A user-visible desktop task created for one worker or reviewer role; tool schemas may call its identifier a thread ID |
| Assignment | One generation-fenced instruction from the orchestrator to a Codex task |
| Task handle | The recorded host/task ID and observed lifecycle state for a Codex task; replaces ambiguous “session” in new schemas |
| Route class | Portable intent: `deep`, `balanced`, or `fast` |
| Model route | Exact detected model ID plus supported reasoning level chosen for an assignment |
| Review unit | The exact spec, child implementation, patch range, or integrated candidate receiving one independent review |
| Integration candidate | Frozen child tips plus integration-owned changes and program gates proposed as one delivery candidate |
| Approval | Operator authorization for one exact workflow action instance under kernel policy |
| Permission | Host sandbox/tool/admin capability; never workflow approval |
| Awaiting operator gate | Progress can continue only after an ungranted phase, authority, or directional choice |
| Paused | Operator explicitly suspended progress; preserves a resumable prior state |
| Blocked | Bounded diagnosis/recovery is exhausted and no independent safe work remains |
| Lease | Coordinator-issued, generation-fenced ownership of a path, index, environment, integration, provider, or data surface |

Avoid in normative V0 text:

- “agent session” when `Codex task`, `task handle`, or `assignment` is meant;
- “worker” without specifying `worker task` or `work item`;
- “model” when portable `route class` versus exact `model route` matters;
- “approved” for sandbox permission, successful command execution, or a stale
  review verdict;
- “stalled” as a synonym for blocked, quiet, awaiting approval, or paused;
- “final candidate” without an exact integration candidate ID and tip.

Unresolved terminology: none. Existing files may retain historical “session” or
“thread” wording when quoting host APIs; new V0 schemas use `task_handle` and keep
the raw host `thread_id` only inside that object.

## Decision Brief

### D1 — Kernel mode versus skill

Options:

1. Put all behavior in the skill. Simple to install, but safety and role
   semantics become optional and duplicated.
2. Put all behavior in the kernel. Durable, but bloats every session and mixes
   invariants with host mechanics.
3. Split invariants and mechanics. The mode defines semantics; the skill runs
   the procedure and owns templates/scripts.

Recommendation: option 3. Mode owns entry/exit, authority non-expansion, state
invariants, review freshness, topology rules, recovery, and status semantics.
The skill owns intake, capability detection, ledger initialization/validation,
canonical kickoff composition, worker control, rendering, and pilot fixtures.

### D2 — Source of truth

Options:

1. Conversation/task status only.
2. Human-authored Markdown ledger only.
3. Versioned structured snapshots plus append-only events, with generated
   Markdown status.

Recommendation: option 3. Task/session state is advisory. The coordinator is the
sole V0 ledger writer. Use JSON for deterministic validation and portability;
render compact Markdown for the operator. Do not require a database.

### D3 — Default topology

Options:

1. Fresh worktree tasks by default.
2. Shared checkout with multiple writers and path/index leases.
3. Fresh user-visible Codex desktop tasks, with serial implementation in one
   prepared local checkout and bounded concurrent read-only tasks; worktrees
   remain capability/readiness-gated.

Recommendation: option 3. The `/orchestrate` invocation explicitly authorizes
desktop-task creation after intake confirmation. V0 rejects subagent dispatch and
multi-writer shared-checkout dispatch.

### D4 — Phase authority

Options:

1. “Take it to done” implicitly grants every phase transition.
2. Ask at every planning/build/review transition.
3. The initial envelope enumerates pre-authorized transitions; unlisted
   transitions remain gates.

Recommendation: option 3. This preserves the existing operator-owned DAG while
allowing a genuine end-to-end mandate.

### D5 — Approval representation

Options:

1. A program-wide list of approved command classes.
2. Reusable approval tokens inherited by workers.
3. Consumable approval instances tied to one exact action and bounded natural
   substeps.

Recommendation: option 3. Sandbox permission is never workflow authority. An
approval instance records the granting message/session but is not a bearer token
and is never copied to a worker as authorization.

### D6 — Review topology

Options:

1. Child inner reviews only.
2. One holistic review only after integration.
3. Child inner loops plus a distinct integrated-candidate inner review when one
   candidate combines children or includes integration-owned changes; then the
   existing final-tip outer gate.

Recommendation: option 3. It matches the experiment's cross-slice findings while
respecting exactly one reviewer per review unit. Any changed tip invalidates the
approval that named the old tip.

### D7 — Heartbeats and persistence

Options:

1. Fixed wall-clock heartbeat and automatic replacement.
2. Event-driven progress records with optional scheduled wakeups when supported.
3. No heartbeat state.

Recommendation: option 2. Silence is not failure. V0 records activity at dispatch,
tool/result, status, gate, review, and handoff boundaries. A wall-clock stale
threshold triggers inspection, never automatic replacement.

### D8 — Command enforcement

Options:

1. Treat prompts and ledgers as sufficient forever.
2. Treat rules/hooks as complete enforcement now.
3. Keep kernel approval policy authoritative; add rules/hooks later as tested
   defense in depth.

Recommendation: option 3. Official hook limitations make option 2 false.

### D9 — Model and reasoning routing

Options:

1. Inherit one model/reasoning level for every worker. Simple, but wastes either
   quality or latency/cost across different roles.
2. Require the operator to pin every assignment. Maximum control, but creates a
   recurring coordination pause.
3. Confirm one program-level routing policy at intake: `manual` role/task pins or
   `auto` selection from an operator-approved model/reasoning pool, with per-role
   overrides and ceilings.

Recommendation: option 3. Before dispatch, show the operator the detected models
and supported reasoning levels, then confirm:

- mode: `manual` or `auto`;
- allowed model pool and reasoning ceiling;
- quality bias: `quality`, `balanced`, or `economy`;
- role/task pins and prohibited combinations;
- fallback behavior when a requested route is unavailable.

The current host exposes Sol, Terra, and Luna model families. Public Codex
documentation supports per-agent model/reasoning selection and automatic
balancing, but does not establish Sol/Luna as portable public names. V0 records
detected model IDs and capability evidence instead of hard-coding availability.

Portable route classes and the recommended current-host mapping:

| Route class | Task class | Current-host mapping | Reason |
| --- | --- | --- | --- |
| `deep` | Program strategy, architecture, ambiguous root cause, security/data-loss/contract work, holistic final-tip inner review | Sol normally at `medium`–`high`; maximum `xhigh` | Depth and adversarial reasoning dominate latency |
| `balanced` | Normal implementation, focused debugging, repo investigation, behavior tests, ordinary spec/re-review | Terra normally at `high`; maximum `xhigh` | Balanced quality, speed, and cost |
| `fast` | Mechanical formatting, deterministic fixture generation, status rendering, simple inventory/lookup | Luna at `medium`, or `high` for multi-step work | Low ambiguity and a deterministic verification oracle |

Auto mode starts at the lowest reasoning level that fits the known complexity:

| Complexity | Starting route |
| --- | --- |
| Deterministic/mechanical with a strong oracle | Luna `medium`, or `high` when several files/steps are involved |
| Routine bounded engineering | Terra `high` |
| Complex but bounded implementation, debugging, or review | Terra `high` or Sol `medium`, selected by speed-versus-depth needs |
| Ambiguous, cross-system, security-sensitive, or certifying work | Sol `high` |
| Exceptional novelty, repeated non-convergence, or unusually broad/high-stakes reasoning | Terra or Sol `xhigh`, with an explicit recorded justification |

Neither Sol nor Terra defaults to `xhigh`. Auto mode raises the route or reasoning
only when evidence reveals greater ambiguity/risk, repeated failure, a substantive
review finding, or insufficient progress at the current level. It may lower a
route only before dispatch or after a completed bounded phase. Every choice and
change is logged with its complexity evidence and rationale. Auto mode may never
select `fast` for an independent certifying review,
security/auth/data-loss/migration/provider work, or an unresolved directional
decision.

## V0 Contracts

### Role boundary

The orchestrator may:

- read program, repo, tracker, and workflow context within the authority envelope;
- maintain coordinator-owned local planning/control artifacts;
- plan the dependency graph and readiness gates;
- dispatch and steer workers using a supported authorized topology;
- run neutral environment, verification, and integration checks;
- perform explicitly assigned mechanical integration;
- reconcile evidence, review freshness, and operator status.

The orchestrator does not normally implement a child. It may patch only:

- coordinator-owned control artifacts; or
- an integration defect under an explicit `integration_patch` assignment that
  becomes its own implementation and review unit.

Conflict resolution, behavior changes, generated-artifact changes with semantic
impact, and integration bug fixes are not “mechanical integration.”

### Invocation and trigger

Enter only when the operator invokes `/orchestrate` or gives an unmistakable
end-to-end, multi-task coordination mandate. An ordinary plan, build, review, or
“help me with this issue” request does not trigger the mode.

Before any dispatch, the skill must materialize and validate:

- goal, non-goals, program done definition, and source artifacts;
- allowed, approval-gated, and forbidden action classes;
- pre-authorized phase transitions;
- repo, target, delivery shape, branch/PR ownership, and integration owner;
- topology permissions: `desktop_tasks`, serial writer, bounded concurrent
  read-only tasks, and separately gated `worktrees`;
- model routing: `manual|auto`, detected/allowed pool, reasoning ceilings,
  quality bias, role pins, prohibited routes, and fallback policy;
- concurrency, time, traffic, paid-spend, and retry ceilings;
- operator-owned decisions and explicit stop/pause conditions.

Defaults when omitted:

- phase transitions: planning and spec convergence only;
- commits: not authorized;
- desktop-task project/environment: operator confirmation required before first
  creation; `/orchestrate` is the explicit task-creation mandate;
- implementation worktrees: disabled;
- concurrency: one writer, up to two bounded read-only desktop tasks;
- model routing: operator confirmation required before first worker dispatch;
- network/live/provider/paid/external/destructive: approval-gated or forbidden by
  the existing kernel/repo policy;
- final spec promotion, implementation start, outer review, push/PR/deploy/tracker
  mutation: operator gates.

The skill asks only when a missing value changes authority, safety, role
boundaries, delivery topology, or activation. It discovers ordinary repo facts
it can read safely.

### Program lifecycle

Program states:

```text
draft -> authority_locked -> graph_ready -> active -> integrating
      -> awaiting_operator_gate -> done
      -> paused
      -> blocked
      -> cancelled
```

Every nonterminal program snapshot may carry `resume_state`. Only the coordinator
emits transition events; operator messages and worker reports are evidence for a
transition, not transitions themselves. The complete legal program transition
table is:

| From | To | Owner | Guard and event | Invalidates |
| --- | --- | --- | --- | --- |
| `draft` | `authority_locked` | coordinator | Valid explicit envelope; `authority_locked` | prior graph/readiness |
| `authority_locked` | `draft` | coordinator | Operator changes goal/authority before dispatch; `authority_reopened` | graph/readiness |
| `authority_locked` | `graph_ready` | coordinator | Graph validates and every non-planning child is ready; `graph_validated` | none |
| `graph_ready` | `authority_locked` | coordinator | Graph, authority, or topology changes before dispatch; `graph_invalidated` | readiness/environment |
| `graph_ready` | `active` | coordinator | At least one authorized assignment is recorded; `program_started` | none |
| `active` | `integrating` | coordinator | Required child tips are frozen/current; `integration_started` | prior candidate reviews |
| `active` | `awaiting_operator_gate` | coordinator | Next action is an ungranted phase/action; `operator_gate_opened` | none |
| `integrating` | `active` | coordinator | Integration exposes child rework; `integration_rework_opened` | candidate verification/reviews |
| `integrating` | `awaiting_operator_gate` | coordinator | Final candidate is ready for outer/delivery gate; `operator_gate_opened` | none |
| `awaiting_operator_gate` | `active` | coordinator | Exact active-phase gate granted and state is fresh; `operator_gate_consumed` | none |
| `awaiting_operator_gate` | `integrating` | coordinator | Exact integration gate granted and state is fresh; `operator_gate_consumed` | none |
| `awaiting_operator_gate` | `done` | coordinator | Gate completes furthest authorized done definition; `program_completed` | none |
| `active` or `integrating` | `done` | coordinator | No further operator gate is required and done validates; `program_completed` | none |
| Any nonterminal except `paused`, `blocked` | `paused` | coordinator | Explicit pause/last-pass; store prior state; `program_paused` | running assignment authority |
| `paused` | stored `resume_state` | coordinator | Explicit resume and freshness reconciliation pass; `program_resumed` | records found stale during reconciliation |
| Any nonterminal except `paused`, `blocked` | `blocked` | coordinator | Blocker survives bounded diagnosis/recovery and no safe independent work remains; store prior state; `program_blocked` | blocker-dependent readiness/evidence |
| `blocked` | stored `resume_state` | coordinator | Blocker resolved and freshness reconciliation pass; `program_unblocked` | records found stale during reconciliation |
| Any nonterminal | `cancelled` | coordinator | Explicit operator cancellation/replacement; `program_cancelled` | all active leases/assignments |

`done` and `cancelled` are terminal. They have no outgoing transitions in V0.
All unlisted program transitions fail closed. `blocked` is not a substitute for
waiting on a worker, ordinary friction, or an informational status exchange.

Task states:

```text
proposed -> planning -> review_ready -> spec_review -> ready
         -> assigned -> running -> verifying -> inner_review
         -> patching -> frozen -> integrated -> complete

Exceptional: waiting_dependency | awaiting_approval | environment_blocked |
             paused | recovery | superseded | cancelled | failed
```

Only the coordinator changes task state. Worker reports are claims reconciled
against artifacts, git state, and command/review evidence.

Every exceptional nonterminal task state carries `resume_state`. The complete
legal task transition table is:

| From | To | Owner | Guard and event | Invalidates |
| --- | --- | --- | --- | --- |
| `proposed` | `planning` | coordinator | Planning assignment ready; `task_planning_started` | none |
| `planning` | `review_ready` | coordinator | Definition-of-Ready draft validates; `task_spec_ready` | prior spec reviews |
| `review_ready` | `spec_review` | coordinator | Canonical kickoff recorded; `task_spec_review_started` | none |
| `spec_review` | `planning` | coordinator | Autonomous ACTIONABLE findings; `task_spec_rework_started` | spec approval |
| `spec_review` | `ready` | coordinator | APPROVED or valid minor-only off-ramp and phase is allowed; `task_ready` | none |
| `ready` | `assigned` | coordinator | Authority, environment, dependencies, and lease guards pass; `task_assigned` | none |
| `assigned` | `running` | coordinator | Current generation starts/acknowledges; `task_started` | none |
| `running` | `verifying` | coordinator | Deliverable report reconciles; `task_verification_started` | prior verification/reviews |
| `verifying` | `running` | coordinator | Product failure requires implementation correction; `task_rework_started` | verification/reviews |
| `verifying` | `inner_review` | coordinator | Required slice gates pass on current tip; `task_inner_review_started` | none |
| `inner_review` | `patching` | coordinator | ACTIONABLE autonomous findings; `task_patch_started` | review approval and affected verification |
| `inner_review` | `frozen` | coordinator | Inner loop converges on exact tip; `task_frozen` | none |
| `patching` | `verifying` | coordinator | Patch reconciled and targeted proof is ready; `task_patch_verification_started` | prior verification/reviews |
| `frozen` | `verifying` | coordinator | Tip, contract, topology, or environment evidence is stale; `task_freeze_invalidated` | affected verification/reviews |
| `frozen` | `integrated` | coordinator | Exact frozen tip enters declared candidate; `task_integrated` | none |
| `integrated` | `verifying` | coordinator | Integration/topology change invalidates child proof; `task_integration_invalidated` | affected verification/reviews/candidate |
| `integrated` | `complete` | coordinator | Candidate/delivery definition for task validates; `task_completed` | none |
| `planning`, `review_ready`, or `ready` | `waiting_dependency` | coordinator | Named dependency not ready; store prior state; `task_waiting_dependency` | dependency-shaped readiness |
| Any nonterminal work state from `planning` through `inner_review` | `awaiting_approval` | coordinator | Exact authority/direction gate is next; store prior state; `task_awaiting_approval` | none |
| `ready`, `assigned`, `running`, `verifying`, `inner_review`, or `patching` | `environment_blocked` | coordinator | Environment attestation/gate fails; store prior state; `task_environment_blocked` | environment-dependent evidence |
| `assigned`, `running`, `verifying`, `inner_review`, or `patching` | `recovery` | coordinator | Session/assignment unreachable or bounded worker recovery begins; store prior state; `task_recovery_started` | active assignment/lease generation |
| Any nonterminal work or exceptional state except `paused`, `failed` | `paused` | coordinator | Explicit program/task pause; store prior state; `task_paused` | active assignment execution authority |
| `waiting_dependency`, `awaiting_approval`, `environment_blocked`, or `paused` | stored `resume_state` | coordinator | Named condition resolves and freshness reconciliation passes; condition-specific `task_resumed` | records found stale during reconciliation |
| `recovery` | stored `resume_state` | coordinator | Prior generation fenced, one replacement/current owner recorded, readiness reconciled; `task_recovered` | stale assignment/session evidence |
| Any nonterminal state except `proposed`, `failed` | `failed` | coordinator | Retry ceiling exhausted or non-recoverable task-local failure; exceptional states must normalize to a non-`failed` base before recording the required `retry_anchor`; `task_failed` | active leases/assignment |
| `failed` | `recovery` | coordinator | Explicit operator retry plus new bounded recovery budget; set `resume_state` to recorded `retry_anchor`; `task_retry_granted` | prior assignment/failed evidence |
| Any nonterminal state | `cancelled` | coordinator | Operator cancels task/program; `task_cancelled` | active leases/assignment |
| Any nonterminal state | `superseded` | coordinator | Graph/topology replaces task with named successors; `task_superseded` | active leases/assignment and dependent readiness |

`complete`, `cancelled`, and `superseded` are terminal. All unlisted task
transitions fail closed. Exceptional-state exits must target recorded
`resume_state`; they cannot skip required lifecycle gates. A retry from `failed`
must not set `resume_state: failed`. `proposed` cannot enter `failed`; before
planning it may only remain proposed, start planning, be cancelled, or be
superseded.

Failure events record a deterministic non-bypassing `retry_anchor`:

| Failure source | `retry_anchor` |
| --- | --- |
| `planning`, `review_ready`, or `spec_review` | `planning` |
| `ready` | `ready` |
| `assigned` | `assigned` |
| `running` | `running` |
| `verifying` | `verifying` |
| `inner_review` | `verifying` |
| `patching` | `patching` |
| `frozen` or `integrated` | `verifying` |
| `waiting_dependency`, `awaiting_approval`, `environment_blocked`, `recovery`, or `paused` | normalize the state's stored `resume_state` through this table |

The validator rejects a missing/unknown anchor, a recursive exceptional anchor,
or any retry target that would bypass a required spec, readiness, environment,
verification, or review gate.

### Persistence and folder layout

For a multi-task umbrella, use one PLANS-compatible work-item folder:

```text
active/<PROGRAM-ID>-<short-name>/
  README.md                 # living program spec and child registry
  program.json              # generated current snapshot; coordinator-owned
  events.jsonl              # authoritative append-only semantic event log
  status.md                 # generated compact operator view
  approvals.json            # generated approval view; coordinator-owned
  integration.md            # candidate tips/order/conflicts/gates
  verification.md           # program-level command evidence
  reviews.md                # review provenance and findings/resolutions
  tasks/<TASK-ID>.md         # concise child assignment/spec pointer
  artifacts/                # fixtures, pilot traces, validation output
```

`INDEX.md` remains the roadmap authority. `README.md` remains the living program
spec. `events.jsonl` is the sole operational source of truth. `program.json`,
`approvals.json`, and `status.md` are deterministic materialized views. Human
edits to generated views are overwritten.

Schema policy:

- root `schema_version`: `0` for the pilot;
- event IDs are contiguous coordinator-issued integers starting at 1;
- every snapshot records `last_event_id` and final event hash;
- events form a hash chain; duplicate IDs, gaps, malformed/truncated lines, or a
  hash mismatch fail closed;
- every mutating CLI must acquire an exclusive advisory lock on
  `<program-dir>/.events.lock` with Python `fcntl.flock`. If `fcntl` is
  unavailable, V0 fails closed as unsupported; it never substitutes an unsafe
  best-effort lock;
- while holding the lock, re-read and validate the complete log, compare the
  caller's `expected_prev_event_hash` and `coordinator_generation` to the current
  values, then commit. A mismatch returns `CAS_CONFLICT` without mutation;
- commit an accepted event by rendering the complete new log to a
  same-directory temporary file, flushing/fsyncing it, and atomically replacing
  `events.jsonl`. The log is semantically append-only even though V0 rewrites the
  small physical file to make the commit atomic;
- after the log commit, regenerate each view independently to a same-directory
  temporary file, validate/flush/fsync it, and atomically replace the view;
- a crash before log replacement leaves the old event set authoritative. A crash
  after log replacement may leave stale views; startup detects their event/hash
  mismatch and rebuilds every view from the valid log before any action;
- orphan temporary files are ignored; corruption/truncation of the committed log
  blocks the program with its exact error and is never repaired from chat or a
  stale view;
- before each desktop-task create, append `dispatch_intent_recorded` with the
  next assignment generation and a stable idempotency key. On restart, reconcile
  the intent against host task history before any create or replacement. Commit
  the returned task handle through `assignment_started` with the same key. An
  unresolved intent blocks retry because the host API does not promise
  idempotent exactly-once task creation;
- unknown fields are rejected in V0 to expose drift;
- V0 has no migration path because it is noncanonical; schema change invalidates
  the pilot and requires regenerated fixtures.

The first event establishes `coordinator_generation: 1`. Coordinator recovery or
replacement acquires the same lock, revalidates the predecessor, and appends
`coordinator_replaced` with generation +1. Every subsequent mutation must present
that generation. A resumed older coordinator is fenced even after the OS lock is
released. Locks are never deleted or stolen based only on elapsed time; a live
process holds the OS lock, while stale logical ownership is resolved only through
the replacement event and normal recovery authority.

`record_event.py` requires `--coordinator-generation` and
`--expected-prev-event-hash`. It returns exit 0 on commit, exit 5
`CAS_CONFLICT`, exit 6 `LOCK_BUSY`, exit 7 `STALE_COORDINATOR`, or exit 4
`INVALID_LOG`, with no mutation on nonzero exit.

Required event schema:

```text
schema_version, event_id, event_type, program_id, coordinator_generation,
task_id|null, assignment_generation|null,
actor: coordinator|operator|worker|reviewer|system,
actor_ref, occurred_at, prior_state|null, next_state|null,
topology_revision, payload, invalidates[], prev_event_hash|null, event_hash
```

Normative event types are the transition event names in the tables plus:

```text
approval_requested | approval_granted | approval_denied | approval_expired |
approval_consumed | approval_revoked | lease_acquired | lease_heartbeat |
lease_released | lease_expired | lease_revoked | environment_attested |
verification_recorded | review_recorded | review_invalidated |
candidate_recorded | decision_recorded | status_reported | recovery_recorded |
model_route_selected | model_route_changed | model_route_unavailable |
coordinator_replaced
```

Compute `event_hash` as SHA-256 over canonical UTF-8 JSON for every event field
except `event_hash`, with sorted keys and no insignificant whitespace.
`prev_event_hash` is null only for event 1. Approval consumption, counters,
leases, snapshots, and status are derived from events; there is no cross-file
write transaction.

### Snapshot schema

Required `program.json` fields:

```json
{
  "schema_version": 0,
  "program_id": "string",
  "title": "string",
  "state": "program-state",
  "topology_revision": 1,
  "coordinator_generation": 1,
  "last_event_id": 1,
  "last_event_hash": "sha256-hex",
  "goal": "string",
  "done_definition": ["string"],
  "authority": {
    "allowed": ["action-class"],
    "approval_gated": ["action-class"],
    "forbidden": ["action-class"],
    "phase_transitions": ["transition"],
    "topologies": ["desktop_tasks"],
    "ceilings": {
      "writers": 1,
      "read_tasks": 2,
      "paid_usd": 0,
      "live_requests": 0,
      "retries_per_blocker": 1
    }
  },
  "model_routing": {
    "policy_revision": 1,
    "mode": "manual-or-auto",
    "quality_bias": "quality-or-balanced-or-economy",
    "detected_routes": ["model-capability-object"],
    "allowed_models": ["detected-model-id"],
    "reasoning_ceiling": "detected-supported-effort",
    "route_classes": {
      "deep": {"model": "detected-sol-id", "max_reasoning": "xhigh"},
      "balanced": {"model": "detected-terra-id", "max_reasoning": "xhigh"},
      "fast": {"model": "detected-luna-id", "max_reasoning": "high"}
    },
    "role_pins": ["role-route-object"],
    "prohibited_routes": ["route-rule-object"],
    "fallback": "ask-or-approved-auto-fallback",
    "confirmed_by": "operator-message-pointer"
  },
  "repo": {
    "root": "absolute-path",
    "target_branch": "string",
    "integration_owner": "string"
  },
  "tasks": ["task-object"],
  "leases": ["lease-object"],
  "environment_attestations": ["attestation-object"],
  "verification_records": ["verification-object"],
  "review_records": ["review-object"],
  "integration_candidates": ["candidate-object"],
  "decisions": ["decision-object"],
  "recoveries": ["recovery-object"],
  "next_action": "string",
  "updated_at": "RFC3339"
}
```

Required task fields:

```text
task_id, title, role, state, dependencies, deliverable, non_goals,
done_criteria, verification_owner, verification_commands, owned_paths,
forbidden_paths, base_sha, branch, worktree, assignment_id,
assignment_generation, task_handle,
authority_delta, environment_attestation_id, lease_ids, current_tip,
review_record_ids, model_policy_revision, model_route, model_route_rationale,
blocker, next_action, updated_at
```

Tasks in exceptional states also require `resume_state`. Program snapshots in
`paused` or `blocked` require `resume_state`.

`assignment_generation` starts at 1 on first assignment and increments before
every replacement, active model-route override, or ownership transfer. Reports
with an older generation are fenced. `model_routing.policy_revision` starts at 1
after operator confirmation and increments whenever the allowed pool, ceilings,
pins, prohibitions, bias, or fallback changes; route events and task snapshots
must name the governing revision. Replay rebuilds and validates both counters.

Task handle is advisory and records:

```text
kind: coordinator | codex_task
host, thread_id, state: active | resumable | record_only |
unreachable | superseded | closed | archived, observed_at, capability_evidence
```

### Approval ledger

Each `approvals.json` record contains:

```text
approval_id, action_class, exact_action_or_command, exact_target,
expected_effect, destructive_or_external_effect, bounded_substeps,
requested_at, requested_in_session, granted_at, granting_message_pointer,
expires_at, cap, consumed_amount, state: requested | granted | denied |
expired | consumed | revoked, consumed_event_ids
```

Rules:

- An approval is one action instance, not a reusable token.
- A worker receives the action's allowed/ask/forbidden classification, not the
  granting message as authority.
- Before execution, the coordinator rechecks exact action, target, effect, cap,
  expiry, and state.
- Natural substeps are valid only when shown to the operator in the original
  approval bundle and remain within its target/effect.
- Sandbox, tool, admin, or filesystem permission never creates a ledger approval.
- A platform approval prompt does not replace the kernel's in-session approval.
- Paid/live counters are reconciled after every attempt, including failures.

### Leases and heartbeats

Lease kinds are `path`, `git_index`, `environment`, `integration`, and reserved
future `provider`/`data` leases.

Required lease fields:

```text
lease_id, kind, scope, holder_task_id, holder_assignment_id, mode,
generation, state: requested | active | released | expired | revoked,
acquired_at, last_heartbeat_at, inspect_after, expires_at,
release_or_revocation_reason
```

Rules:

- The coordinator is the only lease issuer.
- One active writer may hold path and index leases in V0. Read-only leases may
  overlap only when commands are non-mutating.
- Every reassignment increments `generation`; reports from older generations are
  fenced and cannot update task state.
- Heartbeats are event-driven, emitted at dispatch, meaningful tool/result,
  verification, review, status, and handoff boundaries.
- `inspect_after` means inspect status; it does not mean failure or replacement.
- Expiry does not authorize a second writer. Replacement requires the recovery
  sequence below and explicit revocation of the prior generation.

### Environment attestation

Before implementation dispatch, record:

```text
attestation_id, topology_revision, repo_root, checkout_kind, branch,
base_sha, git_status, runtime_versions, package_manager_versions,
repo_command_resolution, required_ignored_inputs, dependency_state,
setup_command_and_result, doctor_command_and_result,
minimal_smoke_command_and_result, verification_commands_available,
clean_tree_result, cleanup_owner, attested_at
```

The attestation is valid only for its checkout, base/environment fingerprint,
and topology revision. Setup success alone is not readiness. Missing dependencies,
ignored data, browser binaries, local services, or compiled outputs produce
`environment_blocked`; they are not product failures and never waive a gate.

For V0 serial execution, the prepared local checkout may use a documented manual
attestation. Worktree implementation dispatch is rejected unless a repo-owned
non-installing prepare/doctor contract has separately passed its pilot.

### Worker assignment and report

The skill populates the existing canonical role kickoff verbatim and appends one
canonical orchestration assignment block. It never paraphrases or replaces the
planning, execution, review, or re-review template.

Assignment block:

```text
Orchestration assignment
- program / task / assignment generation:
- role and terminal deliverable:
- base SHA / branch / checkout:
- owned paths / forbidden paths:
- dependencies and frozen inputs:
- done criteria:
- worker-owned verification / coordinator-owned verification:
- environment attestation:
- allowed / ask / forbidden delta:
- model / reasoning route, mode, rationale, and fallback:
- active leases and prohibited shared state:
- heartbeat and inspect contract:
- terminal report path and required fields:
```

Worker terminal report:

```text
Outcome: complete | blocked | approval-needed | failed
Assignment generation:
Owned-path changes:
Current tip / dirty state:
Commands and exact results:
Unrun or delegated gates:
Approval/live/paid/destructive attempts:
Review state and reviewer identity:
Blocker and one diagnostic already attempted:
Next safe action:
```

### Topology selection

Every worker and reviewer is a fresh user-visible Codex desktop task. V0 does not
dispatch subagents.

Before creation, call the desktop project-list operation and confirm the target
project plus `local` environment. Create the task with the canonical kickoff and
explicit `model`/`thinking` route. Record the returned task identifier and exact
request/result. Monitor through task list/read operations, steer or re-review by
sending follow-ups to the same task identifier, and archive only after its result
and recovery state are durably reconciled.

Use one implementation task at a time when work touches source, generated
artifacts, a Git index, local services, or integration assumptions. Read-only
investigation, source validation, and non-mutating checks may use concurrent
desktop tasks within the confirmed ceiling. Each still receives an explicit
checkout, authority delta, route, and terminal report.

Exactly-one-reviewer semantics are unchanged: create one fresh reviewer task for
the review unit and continue that same task for re-review. If it is unreachable,
fence it before creating exactly one replacement.

Use implementation worktrees only after the separate readiness pilot promotes
them. Shared-worktree multi-writer mode is out of V0.

### Model-routing procedure

Before first worker dispatch, read the callable desktop task-creation contract
exposed on the destination host. Extract its advertised model IDs and supported
reasoning values, record that schema evidence, show the result and recommended
routing table to the operator, and confirm `manual` or `auto`. Do not infer
availability from a previous program or family nicknames. If the contract cannot
enumerate and accept explicit `model` and `thinking` arguments, desktop-task V0
is unsupported on that host and fails closed before dispatch.

In manual mode, each task class or assignment must match an operator-confirmed
pin. An unavailable or unsupported pin opens an operator gate; the coordinator
does not silently substitute.

In auto mode, choose the lowest reasoning level and lowest-cost/latency route that
still meets the task's known complexity, ambiguity, risk, and independence needs
within the confirmed pool and ceiling. `xhigh` requires a concrete exceptional
trigger from the complexity table; model capability alone is not justification.
Record `model_route_selected` before dispatch with:

```text
task_id, assignment_generation, task_class, risk_class, model_id,
reasoning_effort, quality_bias, selection_rationale, capability_evidence,
fallback_used, operator_policy_revision
```

Dispatch uses the desktop task-creation operation with:

```text
prompt: populated canonical kickoff plus orchestration assignment
target: confirmed project ID and local environment
model: detected exact model ID mapped from the selected route class
thinking: detected supported reasoning value
```

Route attestation has three explicit levels:

- `schema_supported`: the pair appears in the destination task-creation contract;
- `dispatch_accepted`: the explicit create call succeeds and returns a task ID;
- `runtime_reported`: task create/read metadata reports the configured pair, when
  the host exposes it.

V0 may claim the explicit route was accepted only at level
`dispatch_accepted`; it may claim runtime observation only at
`runtime_reported`. A create error records `model_route_unavailable` and applies
the confirmed fallback. The task ID, exact arguments, result/error, host, and
attestation level are ledger evidence.

A model/reasoning change uses the desktop follow-up operation's explicit
`model`/`thinking` override, creates a new assignment generation, fences the prior
route, and records `model_route_changed`. Model routing never
changes sandbox, approvals, topology, allowed actions, review independence, or
paid/live/external authority. If no allowed route is available, fail closed at
`awaiting_approval` with `model_route_unavailable`.

### Verification and review routing

- Every child owns slice-local verification per the repo authority and its
  mandatory inner `implreview` → patch → original-reviewer `implrereview` loop.
- Re-review reuse is attempted once. If the original reviewer is unreachable,
  launch exactly one fresh replacement with the canonical re-review kickoff,
  disclose replacement, and invalidate partial approval.
- Review records contain review unit, base/tip, reviewer task identity,
  verdict, findings pointer, verification considered, and `fresh|stale`.
- A tip change, topology revision, changed acceptance contract, or changed
  environment claim invalidates affected readiness, verification, and review
  records.
- A one-PR program with cross-child contracts or integration-owned changes
  creates one distinct `integrated_candidate` review unit. It receives exactly
  one holistic inner reviewer after child tips are frozen and program gates pass.
- The operator-owned outer review runs only after the integrated inner loop
  converges and must review the exact final candidate tip in the other app/model.
  V0 prepares the handoff and pauses unless the operator explicitly performs it.
- Outer findings return verbatim to the original inner reviewer through the
  existing `implrereview` flow. Any patch after either approval makes that
  approval stale until re-review.

Integration candidate fields:

```text
candidate_id, topology_revision, target_branch, child_tips, merge_order,
integration_tip, conflict_resolutions, integration_owned_changes,
program_gate_record_ids, inner_review_record_id, outer_review_record_id,
state: assembling | verified | inner_approved | awaiting_outer |
outer_approved | stale | delivered
```

### Recovery and replacement

Recovery sequence:

1. Inspect the platform record, checkout, artifacts, lease, and last event.
2. Reconcile observable progress into the ledger without treating silence as
   failure.
3. Attempt exact-task steering/resume once when the host supports it.
4. If unreachable or still blocked, preserve kickoff, authority delta, base/tip,
   dirty state, evidence, findings, and next action in a recovery event.
5. Revoke the prior assignment/lease generation and mark its task handle
   `superseded`; prove no writer remains active.
6. Durably record a create intent with the next generation and stable idempotency
   key, reconcile any unresolved intent against host task history, then start at
   most one replacement. Never retry a create whose accepted result may have
   been lost; escalate the unresolved intent instead.
7. Re-run stale environment/readiness/verification/review steps before accepting
   completion.

A worker requiring an approval it cannot surface returns control to the
coordinator. It does not retry-loop, self-escalate, or weaken verification.

### Informational operator messages

Classify new messages as:

- `steer`: adds context or constraints; update ledger and continue;
- `status`: answer in the required status shape, record the event, then continue
  the next safe critical-path action in the same logical run;
- `side_documentation`: complete if safe and bounded, then continue;
- `pause`: only explicit “pause,” “stop after this pass,” or equivalent;
- `replace`: explicitly supersedes the goal;
- `authority_or_direction`: creates an operator gate.

Ambiguous messages do not silently cancel the program. A material scope or
authority ambiguity still stops for a decision.

### Stop, pause, escalation, and done

Stop or pause only when:

- the furthest authorized done state is reached;
- an ungranted phase/action, credential, authority, safety, or directional
  decision is next;
- requirements conflict and safe investigation cannot resolve them;
- the same blocker survives one bounded diagnostic plus the supported recovery
  attempt and no independent safe work remains;
- the operator explicitly pauses, names a last pass, replaces, or cancels the
  goal.

Do not stop for routine status, an ordinary worker completion, a single failed
test that can be diagnosed safely, or an environment failure with a known
coordinator-owned recovery path.

### Operator status

Use exactly:

```text
Outcome/phase: <program state and current candidate>
Completed: <converged tasks and exact evidence>
In flight: <owner, task, assignment generation, current gate>
Blocked/decision: <exact operator/environment need, or none>
Safety/spend: <live/paid/destructive attempts and actual amount>
Next: <next safe critical-path action and why>
Estimate: <remaining gates/review cycles, or unknown with reason>
```

## Skill Package Design

Do not scaffold until the reviewed design is approved. After approval, use the
system `skill-creator` initializer and keep the package non-installed under the
workflow draft area until activation approval.

Proposed non-discoverable staging package:

```text
drafts/orchestrate-v0/
  orchestrate/
    SKILL.md
    agents/openai.yaml
    references/
      ledger-schema.md
      assignment-and-status.md
    scripts/
      init_program.py
      validate_program.py
      render_status.py
      record_event.py
      validate_host_evidence.py
    assets/
      program-v0/
        program.json
        approvals.json
        events.jsonl
        status.md
        integration.md
  tests/
    test_event_log.py
    test_writer_lock.py
    test_transitions.py
    test_approvals.py
    test_leases.py
    test_recovery.py
    test_review_freshness.py
    test_status_and_pilot.py
  pilot/
    scenario.json
    host_scenario.json
    run_baseline.py
    run_orchestrated.py
    compare_runs.py
    host-evidence.schema.json
```

`drafts/` is outside every configured skill discovery root. Phase 2 must verify
that the staged skill is absent from the active skill catalog before forward
testing. Activation is the explicit Phase 3 move/copy of the reviewed exact
`drafts/orchestrate-v0/orchestrate/` tree into `skills/orchestrate/`, followed by
validation and a smoke invocation. No symlink or marketplace entry points from an
active root to the draft.

`SKILL.md` stays below 500 lines and contains only the trigger, role, lifecycle,
capability/topology selection, canonical kickoff routing, recovery loop, and
resource map. Detailed schemas and formats live one reference level away.
Scripts use only the Python standard library unless separately approved.

The skill description triggers only for `/orchestrate` or explicit end-to-end
multi-task program coordination. It explicitly excludes one-item planning,
implementation, review, ordinary status reporting, and generic parallel research.

## Behavioral Validation

### Deterministic fixtures

Validator tests must prove:

- invalid program/task transitions fail closed;
- concurrent mutating subprocesses serialize under the ledger lock; callers with
  the same predecessor yield one success plus one `CAS_CONFLICT`, and an explicit
  retry appends the second event without loss;
- a replaced coordinator generation fences all later writes from the old owner;
- detect-only validation reports a stale derived-view event/hash mismatch without
  mutation; startup recovery rebuilds that same stale view from a valid log;
- an approval cannot be reused after consumption, expiry, target drift, or cap
  exhaustion;
- an old assignment generation cannot report completion after replacement;
- overlapping V0 writer/path/index leases are rejected;
- status messages record an event and preserve the next action;
- environment setup success with a failed doctor/smoke remains
  `environment_blocked`;
- tip or topology changes mark dependent verification/review records stale;
- a visible but unreachable Codex task is not marked resumable;
- original-reviewer reuse is tried before one replacement;
- an integrated candidate cannot become `outer_approved` unless both final-tip
  review records name its exact tip;
- explicit last-pass/pause prevents autonomous patch continuation;
- hooks/rules absence or a simulated bypass does not alter approval requirements;
- dispatch is rejected until the operator confirms a model-routing policy;
- manual mode rejects route substitution and unsupported reasoning levels;
- auto mode chooses the expected `deep`/`balanced`/`fast` class and mapped exact
  model ID from a synthetic detected capability set;
- routine work starts at Terra `high`, complex bounded work may choose Terra
  `xhigh` or Sol `medium`/`high`, and neither Sol nor Terra selects `xhigh` without an
  exceptional trigger recorded in the route rationale;
- auto/manual routing rejects Sol or Terra reasoning above `xhigh` even when the
  host advertises `max` or `ultra`;
- auto escalation creates a new assignment generation and fences the prior route;
  prohibited `fast` risk/reviewer routes fail closed;
- an unavailable route follows the confirmed fallback or opens an operator gate
  without changing task authority.
- restart recovery succeeds when a crash is injected before log replacement and
  after log replacement but before each derived view replacement;
- a malformed, truncated, duplicate-ID, gap-ID, or hash-broken committed log
  fails closed without reconstructing state from a view or chat;
- approval grant/consumption remains correct after every injected restart.
- replay/restart preserves and validates coordinator generation, assignment
  generation, and model-policy revision.

Tests exercise scripts through their CLI boundary using temporary directories and
assert exit codes, persisted state, and rendered status. Source-text or constant-
equality tests are supplemental only; behavioral state transitions are the
contract.

The test location and runner are fixed for V0:

```text
python3 -m unittest discover \
  -s /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/tests \
  -p 'test_*.py'
```

Every test creates its own `tempfile.TemporaryDirectory`, invokes the scripts as
subprocess CLIs, and asserts persisted files plus exit status. Skill assets hold
input fixtures only; they never substitute for executable tests.

Derived-view validation has two explicit CLI paths:

```text
validate_program.py --check-views <program-dir>
  valid/current -> exit 0, CURRENT
  valid log + stale/missing view -> exit 3, STALE_VIEW, no mutation
  invalid log -> exit 4, INVALID_LOG, no mutation

validate_program.py --startup-recover <program-dir>
  valid/current -> exit 0, CURRENT
  valid log + stale/missing view -> atomically rebuild all views, exit 0, REBUILT
  invalid log -> exit 4, INVALID_LOG, no mutation
```

`test_event_log.py` and `test_recovery.py` assert all six outcomes, including the
exact exit code/result marker and before/after file hashes.

### Safe pilot

Validation has two distinct layers.

Policy-engine tests use only temporary folders and injected events. They prove
ledger transitions, fencing, selection policy, and fail-closed behavior; they do
not claim that the desktop app created, steered, resumed, or routed a real task.

The host-integration pilot runs one local, serial, two-task documentation/fixture
program through the staged skill and the real desktop task operations:

- no repo source implementation;
- preflight the desktop project list and explicit model/reasoning task-creation
  contract; stop as `host_capability_blocked` if either is absent;
- create one fresh read-only research task and one fresh reviewer task in the
  confirmed local project/environment, each with explicit model and reasoning;
- no implementation worktrees;
- no network, provider, paid call, credential, tracker mutation, commit, push, or
  external message;
- confirm an auto model-routing policy, record each selected route/rationale, and
  issue one real follow-up model/reasoning override that requires a new assignment
  generation;
- monitor both real task IDs through task read/status operations and reconcile
  their returned results into the ledger;
- continue the same reviewer task with a re-review follow-up and verify the task ID
  is unchanged;
- after results are reconciled, archive the tasks and record the archive results;
- have the operator send one status question while the pilot is active; verify the
  coordinator answers and then advances the next authorized action without a
  `continue` prompt;
- inject one environment-blocked child and recover it through the coordinator;
- inject one stale review tip and require re-review freshness;
- exercise a controlled reviewer replacement after closing the original task and
  verify generation fencing. A naturally unreachable task remains explicitly
  unproven until observed; V0 handles it fail-closed with the same replacement
  protocol and does not claim host resumability;
- end at an operator-owned outer-gate simulation without invoking the outer gate.

For every host operation, write `host-evidence.jsonl` with operation name, exact
arguments excluding secrets, returned task/operation ID, result/error, observed
status, route-attestation level, timestamp, and linked ledger event. Promotion
requires the ledger and host evidence to reconcile one-to-one.

Run a reproducible baseline first, then the orchestrated pilot. Both drivers read
the exact same immutable `pilot/scenario.json` and record its SHA-256. The
scenario contains the same two tasks, authority envelope, status interruption,
environment failure/repair fact, stale-tip event, unreachable-reviewer event, and
simulated outer gate.

`run_baseline.py` models the current serial A–D procedural workflow without an
orchestration ledger: it processes the scenario in order, yields after the
injected status exchange, requires an explicit operator-continue event, performs
the declared environment repair when prompted, and records review/replacement
steps without changing the scenario. `run_orchestrated.py` uses the proposed
ledger and transition CLIs over the same scenario. These deterministic drivers
compare policy behavior; the host-integration procedure above separately proves
the real task boundary.

Operational metric definitions:

- `avoidable_pause`: the driver yields while a pre-authorized `next_action`
  exists, no approval/direction/credential/blocker gate is open, and no worker is
  still running.
- `operator_repair`: the operator must restate persisted state, issue `continue`
  after an informational message, recover a coordinator-owned declared
  environment step, or reconstruct a kickoff/evidence record.
- `operator_request_expected`: request matches the scenario's named direction,
  authority, credential, or outer-gate event.
- `operator_request_avoidable`: any other request, including status continuation
  or ordinary friction.
- `false_green`: a gate/review is current despite an unrun/failed command, stale
  tip/topology/environment record, or invalid event chain.

Each driver writes `metrics.json`, `trace.jsonl`, and `final-status.md` in a clean
temporary output directory. `compare_runs.py` rejects different scenario hashes
or missing events.

Record baseline and pilot:

```text
elapsed time; avoidable coordinator pauses; operator decisions requested;
environment repairs; duplicate writers; stale review acceptances;
recovery attempts/success; review cycles/findings; false-green gates;
authority violations; live/paid/destructive attempts; ledger validation failures
```

Promotion thresholds:

- zero authority violations;
- zero live/paid/destructive/external attempts;
- zero false-green or stale-tip approvals;
- zero overlapping writers;
- zero dispatches without a confirmed and supported model/reasoning route;
- real task create/read/follow-up/archive operations reconcile to host evidence;
- explicit route arguments reach `dispatch_accepted`; any absent
  `runtime_reported` evidence remains labeled rather than inferred;
- every recovery preserves assignment fencing and exact evidence;
- informational status does not pause the next safe action;
- every operator request is directional, authority-bearing, or a true blocker;
- orchestrated `avoidable_pause == 0` and is lower than the baseline (the injected
  baseline status yield must make baseline `avoidable_pause >= 1`);
- orchestrated `operator_repair <= baseline operator_repair`, with zero state or
  kickoff reconstruction;
- orchestrated expected operator requests equal the scenario's named gates and
  avoidable operator requests equal zero;
- validator and pilot fixtures all pass twice from clean temporary directories;
- naturally unreachable-task resumption remains an unproven capability and is not
  represented as passed merely because controlled replacement succeeds;
- inner spec and implementation artifact review loops converge;
- operator explicitly approves activation.

Abort/rollback criteria:

- any approval reuse, writer overlap, stale review accepted as current, or false
  green;
- ledger corruption or recovery requiring chat-history reconstruction;
- more operator repair work than the serial baseline;
- a platform capability is required but not capability-detected/fallback-safe.

Rollback is deletion/archival of the uninstalled draft skill and removal of the
inactive startup-route proposal. Existing A–D routing and review skills remain
unchanged throughout the pilot.

## Rollout

1. Converge this spec through one fresh `specreview` and original-reviewer
   `specrereview` loop.
2. Obtain operator approval for artifact implementation, not activation.
3. Revise `ORCHESTRATOR_MODE.md` as the normative draft and add the noncanonical
   kickoff/templates/schemas/scripts/fixtures.
4. Scaffold `drafts/orchestrate-v0/orchestrate/` with `skill-creator`, validate
   it in place, confirm it is absent from active skill discovery, and forward-test
   it against the offline fixture without installing it.
5. Run the safe serial desktop-task pilot and append measured evidence to
   `AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`.
6. Run the mandatory implementation `implreview` → `implrereview` loop on the
   artifact diff, then the mandatory `outerreview` because the artifact defines a
   workflow state machine and authority contract.
7. Assemble a non-discoverable activation candidate containing the exact staged
   skill bytes, SHA-256 manifest, rendered `AGENTS.md` Routing E patch, activation
   script, rollback script, and explicit-path activation smoke evidence. Treat it
   as a distinct review unit: run `implreview` → any `implrereview`, then mandatory
   final-tip `outerreview` on that exact candidate.
8. Present the reviewed activation candidate for the final operator decision:
   activate, revise/re-pilot, or reject.
9. Only after explicit activation approval, copy the manifest-identical skill into
   `skills/orchestrate/` and apply the reviewed `AGENTS.md` patch. Verify installed
   hashes and run the reviewed post-install smoke immediately. Any byte/patch
   difference or smoke failure triggers rollback; any corrective patch creates a
   new candidate and invalidates both reviews.

## Proposed File-Level Change Plan

Phase 1 — reviewed design, current assignment:

- `ORCHESTRATOR_V0_SPEC.md`: living evidence, decisions, normative V0 contract,
  validation, rollout, and file plan.
- No canonical behavior changes.

Phase 2 — artifact implementation after operator approval:

- `ORCHESTRATOR_MODE.md`: replace rough prose with the reviewed semantic contract;
  remain `status: draft` until activation.
- `kickoffs/orchestration.md`: canonical intake/authority lock.
- `kickoffs/orchestration-assignment.md`: append-only block used after existing
  role kickoffs.
- `drafts/orchestrate-v0/orchestrate/**`: non-discoverable staged skill package,
  deterministic scripts, and versioned ledger/status assets.
- `drafts/orchestrate-v0/tests/**`: fixed standard-library `unittest` behavioral
  suite covering the state and recovery contracts.
- `drafts/orchestrate-v0/pilot/**`: shared scenario, baseline/orchestrated drivers,
  comparison script, and generated evidence ignored or pocketed under artifacts.
- `PLANS.md`: narrowly add umbrella-program folder composition and generated
  operational artifacts.
- `HANDOFF.md`: clarify integrated candidate as a distinct review unit and preserve
  exactly-one-reviewer/final-tip rules.
- `AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`: append pilot evidence; do not rewrite
  historical observations.
- `AGENTS.md`: no activation edit in Phase 2. Keep the candidate route inactive.

Phase 3 — activation only after explicit approval:

- `drafts/orchestrate-v0/activation-candidate/**`: reviewed exact skill manifest,
  candidate `AGENTS.md` patch, activation/rollback scripts, and explicit-path
  smoke evidence; remains outside discovery through inner and outer review.
- After final operator approval only, `AGENTS.md`: apply the exact reviewed
  Startup Routing E patch and remove inactive-candidate wording.
- After final operator approval only, `skills/orchestrate/**`: copy the exact
  manifest-reviewed staged artifact into discovery, verify hashes, and run the
  reviewed post-install smoke with rollback on any mismatch/failure.

Deferred separate specs:

- worktree prepare/doctor/cleanup implementation and multi-worktree pilot;
- complete command-rule/hook threat model and enforcement rollout;
- cross-host/cloud user-visible task orchestration;
- scheduled heartbeat/SLA behavior;
- shared-worktree multi-writer mode.

## Acceptance Criteria

- [ ] Assessment clearly separates verified platform capabilities, local evidence,
  and hypotheses.
- [ ] Mode/skill responsibilities and role boundaries are non-overlapping.
- [ ] Entry requires explicit multi-task orchestration authority and enumerates
  pre-authorized phase transitions.
- [ ] Intake confirms manual or auto model/reasoning routing; auto choices are
  capability-detected, bounded, explainable, and fail closed when unavailable.
- [ ] Every worker/reviewer is a fresh user-visible desktop task created with an
  explicit accepted model/reasoning route; policy simulations are not represented
  as host-operation proof.
- [ ] Every destructive/external/live/paid action remains subject to current
  kernel/repo approval policy.
- [ ] Ledger schemas define states, transition authority, event ordering,
  approvals, leases, task handles, environment, verification, review, integration,
  and recovery.
- [ ] V0 has one writer and serial implementation by default; unsupported
  topologies fail closed.
- [ ] Environment attestation proves the actual destination commands and clean
  state before dispatch.
- [ ] Review records certify exact tips; stale approvals cannot certify a changed
  candidate.
- [ ] Original reviewers are reused for re-review when reachable; replacement is
  single, explicit, and fenced.
- [ ] Status/side-documentation messages do not pause authorized critical-path
  work.
- [ ] Stop, pause, escalation, last-pass, recovery, and replacement conditions are
  testable.
- [ ] Rules/hooks are described only as future defense in depth.
- [ ] Safe pilot and promotion/rollback thresholds are falsifiable.
- [ ] No mode activation or skill installation occurs before reviewed-design and
  operator-activation approvals.

## Verification Plan

Current planning phase:

```text
Read every named kernel/draft/reference/kickoff/analogous skill completely.
Check current Codex behavior against official OpenAI documentation.
Run canonical specreview, patch autonomous findings, and reuse the reviewer for
specrereview until APPROVED or the three-cycle/directional-decision stop.
Confirm git status in the active repo remains untouched.
```

Artifact implementation phase after approval:

```text
python3 /Users/ccolosimo/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/orchestrate
python3 -m unittest discover \
  -s /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/tests \
  -p 'test_*.py'
python3 /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/pilot/run_baseline.py \
  --scenario /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/pilot/scenario.json \
  --output <clean-baseline-dir>
python3 /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/pilot/run_orchestrated.py \
  --scenario /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/pilot/scenario.json \
  --output <clean-orchestrated-dir>
python3 /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/pilot/compare_runs.py \
  --baseline <clean-baseline-dir> --orchestrated <clean-orchestrated-dir>
python3 /Users/ccolosimo/.agents/workflow/drafts/orchestrate-v0/orchestrate/scripts/validate_host_evidence.py \
  --program <pilot-program-dir> --evidence <pilot-program-dir>/host-evidence.jsonl
```

The test and pilot paths are fixed for V0. The test runners create their clean
temporary directories; the placeholders above are their printed output paths or
explicit `mktemp` directories created for a manual repeat.

Gates intentionally not selected now:

- Skill scaffold validation: blocked by operator design approval.
- Artifact implementation review: no artifact implementation exists yet.
- Worktree parity: separately deferred and not implied by V0.
- Rules/hooks enforcement: separately deferred.
- Live/provider/network/paid/external verification: forbidden for this program.

## Non-Goals

- Do not activate Startup Routing E.
- Do not install or promote an active skill.
- Do not promise crash-proof background persistence or universal session resumption.
- Do not use subagents or make implementation worktrees mandatory for V0;
  user-visible desktop tasks are the required worker/reviewer topology.
- Do not transfer approvals between Codex tasks or treat sandbox permission as authority.
- Do not replace planning, execution, review, re-review, or outer-review skills.
- Do not mechanically enforce every destructive command in this work item.
- Do not create a workflow database, daemon, hosted service, or dependency.
- Do not weaken review, test-quality, verification, or docs-impact contracts for
  throughput.

## Open Decisions Requiring Operator Direction

No direction decision blocks spec review. The recommended defaults are explicit.
Activation, artifact implementation after review, and any future expansion to
implementation worktrees or cross-host/cloud tasks remain operator gates.
