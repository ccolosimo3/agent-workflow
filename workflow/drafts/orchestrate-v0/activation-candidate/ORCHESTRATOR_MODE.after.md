---
title: Orchestrator Mode V0
status: active-v0
created: 2026-07-10
updated: 2026-07-10
owner: operator
related:
  - AGENTS.md
  - AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md
  - HANDOFF.md
  - PLANS.md
  - WORKTREE_ENVIRONMENT_BOOTSTRAP.md
  - COMMAND_GUARDRAILS_AND_VERIFICATION_HOOKS.md
---

# Orchestrator Mode V0

This is the active V0 kernel mode for explicitly authorized end-to-end program
orchestration. Startup Routing E in `AGENTS.md` and the `/orchestrate` skill
enter this mode; existing planning, execution, and review contracts remain in
force beneath it.

## Recommendation

Make orchestration a distinct kernel role layered over the existing roles:

- **Planning** owns one work item's research and converged spec.
- **Implementation** owns one bounded change and its inner review loop.
- **Review** independently evaluates a spec or implementation.
- **Orchestration** owns an end-to-end program's control plane: authority,
  dependency graph, task readiness, assignment, environment, leases, review
  convergence, integration, operator status, and retrospective.

The product shape is both:

1. a kernel mode defining durable semantics and safety boundaries; and
2. an `/orchestrate` skill or canonical kickoff that initializes the program
   ledger and runs the mode consistently.

The orchestrator should not normally implement a child task. It may maintain
planning/control artifacts, run neutral coordinator checks, and perform a
mechanical integration step when that ownership is explicit. Keeping child
implementation and review separate preserves scope and review independence.

## Trigger And Exit

Enter only on an explicit end-to-end mandate such as “orchestrate this program,”
“take this full spec to done,” or an explicit grant to coordinate multiple
tasks/sessions. Do not infer orchestration authority from an ordinary planning
or implementation request.

Before dispatch, lock:

- the goal and definition of done;
- allowed, approval-gated, and forbidden actions;
- repository, branch/PR delivery shape, and integration owner;
- concurrency, spend, traffic, and time ceilings;
- which fresh user-visible Codex desktop tasks may run, their serial-writer/
  read-only concurrency ceilings, project/environment, and model routes;
- operator-owned decisions and the stop/pause contract.

Exit or pause only when:

- the program reaches the furthest authorized definition of done;
- the next step needs operator authority, credentials, or a directional choice;
- requirements conflict or destructive ambiguity remains after safe checks;
- the operator explicitly pauses or replaces the goal; or
- a named environment/external blocker prevents meaningful progress.

A status question or documentation request does not pause the program. Answer
it, record any new direction, and resume the next safe critical-path action.

## Authority Does Not Expand

“Take it to done,” autonomy, full-access permissions, and worker concurrency do
not broaden the operator's authority grant. The kernel's Destructive Action
Policy, repo safety rules, provider/live/paid gates, review floor, and data
handling rules remain in force for the orchestrator and every worker it launches.

The orchestrator maintains one visible authority ledger:

| Action class | State | Required record |
| --- | --- | --- |
| Offline read/write/test/ordinary scoped commit | allowed or limited by kickoff | scope, owner, branch, verification |
| Live/provider/browser/hardware/paid action | ask per action unless explicitly granted | target, tier, cap/budget, stop rule, approval |
| Destructive/external mutation | ask per kernel policy | exact command/action, target, expected effect, approval |
| Forbidden action | never | reason and safe alternative |

Every worker assignment repeats the relevant delta. No worker inherits a broader
grant merely because its parent has broad filesystem or shell permissions.

## Program Control Artifacts

Use one program folder under the repo's local planning authority. Minimum
artifacts:

- `README.md` — umbrella goal, non-goals, decisions, dependency graph, delivery
  topology, definition of done, and child registry;
- `program-ledger.md` or a structured equivalent — live task state, owner,
  session, branch/worktree, base/tip, leases, verification, review, and next
  action;
- `approvals.md` — allowed/gated/forbidden actions, live/paid caps, approvals,
  attempts, and actual spend/traffic;
- `integration.md` — frozen child tips, merge order, conflicts, branch-level
  verification, review freshness, and final handoff;
- `retrospective.md` or a linked living evidence log — workflow friction,
  recoveries, operator decisions, and final measurements.

`INDEX.md` remains the roadmap authority. The program ledger is operational
state, not a second roadmap.

Each task row should contain at least:

| Field group | Required values |
| --- | --- |
| Identity | task/spec, role, owner/session, status, dependency |
| Git/environment | repo, branch, worktree, base SHA, owned paths, readiness result |
| Contract | deliverable, non-goals, verification boundary, done criteria |
| Safety | allowed actions, approval gates, forbidden actions, spend/traffic cap |
| Evidence | commands/results, review verdict/session, current tip, artifacts |
| Control | lease state, heartbeat, blocker, next action, recovery owner |

## Lifecycle

### O0 — Intake and authority lock

Read the complete goal/spec, repo shims, roadmap, and relevant workflow
authorities. Separate directional questions from discoverable facts. Write the
authority envelope and initial stop conditions before launching workers.

### O1 — Program graph

Decompose by independently reviewable deliverables, not by arbitrary file
count. Identify dependencies, integration seams, shared files/state, and which
proof belongs to a child versus integration. Do not dispatch a child that lacks
Definition of Ready.

### O2 — Spec convergence

Use the existing planning and spec-review loop per child. The orchestrator may
resolve factual and mechanical findings; it returns to the operator for scope,
policy, or trade-off decisions. A child becomes executable only when its spec,
environment, ownership, and verification contract agree.

### O3 — Environment and topology gate

Choose the safest delivery topology supported by proven environment parity:

1. **Serial prepared checkout — current default.** One implementer at a time in
   the known-good environment.
2. **Separate worktrees/branches — disabled in V0.** Use only after `worktree:prepare` and
   `worktree:doctor` or equivalent prove dependencies, local outputs, ignored
   inputs, verification, and clean-tree behavior.
3. **Shared worktree/branch — outside V0.** Requires disjoint path leases, one
   Git-index/commit lease, frozen integration-owned files, and serialized broad
   gates.

Throughput never outranks verification confidence. A missing tool, dependency,
compiled output, browser binary, or test service is an environment failure—not a
product defect and not a reason to waive verification.

### O4 — Dispatch

Every worker receives the canonical role kickoff plus an orchestration assignment
block containing:

- program/task identity and role;
- exact goal, deliverable, done criteria, and verification method;
- repo, base SHA, branch/worktree, owned and forbidden paths;
- dependencies and frozen inputs;
- commands resolved through repo tooling, never assumed global binaries;
- allowed, approval-gated, and forbidden actions;
- commit/index/provider/data leases;
- heartbeat, blocker, and terminal-report contract.

V0 uses fresh user-visible Codex desktop tasks for every worker and reviewer and
does not use subagents. Before dispatch, confirm the local project/environment,
one-writer ceiling, read-only task ceiling, and manual/auto model policy. Create
each task with explicit model/reasoning controls, record its task ID, and monitor
or continue it through the desktop task tools. Do not duplicate a task merely
because it is quiet; inspect or continue it first.

Model routes are portable intent mapped to current host IDs: `fast` (normally
Luna medium/high), `balanced` (normally Terra high, with xhigh for justified
complexity), and `deep` (normally Sol medium/high). Sol and Terra cap at xhigh;
neither defaults there. Xhigh
requires exceptional novelty, broad high-stakes coupling, or repeated
non-convergence, with a recorded justification.

### O5 — Active control

Keep the critical path moving within the concurrency ceiling. The orchestrator:

- records each transition and current evidence;
- answers operator questions without converting them into an implicit pause;
- detects stale bases, overlapping writers, lease conflicts, and blocked gates;
- distinguishes ordinary work, environment repair, and operator decisions;
- resumes the original worker/reviewer when continuity is required;
- re-plans when real evidence invalidates a load-bearing assumption.

Send a compact heartbeat during long work. The operator-facing view should show
completed, in flight, blocked/decision-needed, safety/spend, next gate, and the
critical path—not every low-value worker action.

### O6 — Verification and review

Children own slice-local verification and the mandatory inner review loop.
Integration owns cross-child contracts and branch-level gates. Never claim a
gate passed unless it ran on the exact current range in a prepared environment.

Apply `HANDOFF.md` unchanged:

- reuse the original reviewer for re-review;
- freeze or re-review any tip changed after approval;
- run the operator-owned outer gate where required;
- prevent one worker from reviewing its own implementation as the independent
  lens.

Live/provider/hardware proof remains Tier 4 and separately approved. A green
mock or offline fixture cannot be presented as proof of a boundary it does not
exercise.

### O7 — Integration and delivery

Before integration, freeze child tips and verify review freshness, dependencies,
docs ownership, and conflict posture. Integrate in the declared order, rerun
affected and program-level gates, then obtain any required final review on the
actual candidate tip.

Push, PR, deployment, tracker mutation, or other external delivery happens only
under the existing approval policy. The final handoff reports what is complete,
what was verified, remaining Tier-4 work, actual spend/traffic, deferred items,
and cleanup ownership.

### O8 — Cleanup and learning

On landing, follow `PLANS.md` cleanup rules, archive the program, release leases,
and distill reusable workflow findings. Record both outcome quality and control-
plane quality: review rework, environment failures, stalled/recovered workers,
operator interruptions, spend/traffic, integration defects, and elapsed time.

## Stall And Recovery Rules

- A worker with no visible progress is inspected before interruption or
  replacement. Silence alone is not failure.
- Allow one bounded diagnostic attempt for environment/permission failures;
  then route repair to the coordinator rather than weakening verification.
- Resume original sessions for re-review and context-sensitive recovery when
  possible. A replacement receives a complete explicit handoff and never writes
  concurrently with the original.
- If topology changes—parallel to serial, shared to isolated, or branch ownership
  changes—recheck every child spec's paths, counts, branch assumptions,
  verification ownership, and review freshness.
- An operator-declared “last pass” or pause overrides the ordinary autonomous
  patch/re-review loop. Preserve exact state and stop.

## Operator Status Contract

Use a stable compact status shape:

```text
Outcome/phase: <current program state>
Completed: <converged deliverables and evidence>
In flight: <owner, task, current gate>
Blocked/decision: <exact operator or environment need, or none>
Safety/spend: <live/proxy/provider/model/destructive attempts and actual cost>
Next: <next critical-path action and why>
Estimate: <evidence-based range, or unknown with reason>
```

Do not hide uncertainty behind a percentage. Estimates should be tied to
remaining review/gate steps and updated when evidence changes.

## Invocation Shape

An explicit `/orchestrate` invocation begins from:

```text
Run <goal/spec> as one end-to-end program to the furthest authorized done state.

Authority
- May: <ordinary scoped actions>.
- Ask: <live, paid, destructive, external, and direction gates>.
- Forbidden: <explicit boundaries>.
- Delivery: <repo, target, branch/PR shape, integration owner>.
- Ceilings: <concurrency, traffic, spend, time>.
- Desktop tasks: <project/local environment, serial writer, read-only ceiling>.
- Model routing: <manual|auto; fast/balanced/deep mappings and ceilings>.

Control
- Validate readiness, build the dependency graph, and assign independently
  verifiable tasks with owners, paths, proof, and done criteria.
- Maintain one task/approval/integration ledger; keep leases and review tips fresh.
- Persist through routine friction and informational interruptions.
- Stop only at the defined operator gate, genuine blocker, explicit pause, or done.
```

The skill should then populate the canonical planning/execution/review kickoffs;
it must not replace or paraphrase them.

## Post-V0 Follow-ups

The reviewed V0 resolved the trigger, ledger, desktop-task control, serial-writer
topology, model routing, review, recovery, and pilot questions. Continue to
investigate these non-blocking follow-ups without silently expanding V0:

1. Prove worktree readiness before enabling parallel implementation.
2. Evaluate command-rule/hook enforcement only through its separate threat model.
3. Calibrate heartbeat/stall thresholds from additional real programs.
4. Revisit the one-writer and read-only ceilings only with measured evidence.

## V0 Rollout Record

V0 was reviewed against the kernel, exercised through a serial offline pilot and
real desktop-task control pilot, patched through inner and outer review, and
promoted only through a manifest-verified activation candidate. Worktree
parallelism and command hooks remain outside V0.
