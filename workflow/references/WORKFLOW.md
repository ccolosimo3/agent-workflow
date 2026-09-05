# Agent Workflow V2 Routing

This file owns phase selection, planner coordination, and shared handoff
semantics. Phase skills own only their phase-specific work.

## Available graph

```text
plan
  -> explore, when the approach is genuinely open
  -> spike, when one load-bearing bet can be falsified cheaply
  -> spec
  -> inner spec review <-> revision
  -> outer spec review <-> revision, when enabled and selected by risk
  -> implementation
  -> inner implementation review <-> patch
  -> outer implementation review <-> patch, when enabled and selected by risk
  -> complete
```

Skill discovery is not phase selection. A clear operator request in ordinary
language may select the matching user-facing phase; relevance alone may not
start, expand, or chain a phase, create its artifacts, dispatch work, grant
authority, or claim fresh-context independence. Only a selected phase's
declared handoff may start its review child.

The graph is not a mandatory pipeline. Without a clear end-to-end grant, the
operator selects each substantive phase: explore, spike, spec, or implementation.
A clear request to implement or own one named work item end-to-end selects the
minimum necessary route through required preparation, formal spec and its
declared reviews when the route requires them, implementation, and implementation
review. It does not select another work item, manufacture explore or spike
without a positive trigger, authorize a gated action or external publication,
expand scope, or transfer a product-direction choice to the agent. Broad
completion language selects this route only when current context identifies one
work item and completion responsibility; otherwise resolve the context before
chaining phases.

Selecting formal spec or implementation includes its required inner review as
that phase's completion gate; do not pause merely to ask whether to start it.
Once a review gate starts, its same-reviewer correction loop continues
autonomously until approved, blocked by a material decision, or its bounded retry
limit is exhausted.

## Routes

- **Fast:** outcome and shape are clear, the change is local and reversible, no
  consequential outer-gate surface is touched, and one focused proof can falsify
  it. Skip formal explore/spec; implement and use the inner review floor.
- **Standard:** the work needs a durable implementation plan but no unresolved
  architecture bet. Use spec, inner spec review, implementation, and inner
  implementation review.
- **Assured:** consequential risk is present. Use explore or spike only for real
  uncertainty, then inner and risk-selected outer reviews around spec and
  implementation.

“More review might help” is not a route trigger.

Use Fast when its conditions hold unless the operator selected a formal spec.
Choose spec and implementation outer gates separately, naming the material risk
or unanswered boundary question in the existing handoff. A spec outer gate neither
automatically selects nor discharges an implementation outer gate. Do not reopen
valid completed gates merely because routing guidance changed.

## Host and outer-gate policy

Read `HOST.local.md` from the canonical V2 package root when present. It owns
available hosts, named model profiles, workload preferences, and outer routing;
repository adapters do not.
Without one, treat outer gates as `operator-invoked` and use the current host's
capabilities without inventing cross-host launch or model selection.

Resolve workload preferences for the host doing the selected phase, not a
coordinator that dispatched it. When dispatch exposes model choice, follow the
applicable fixed profile or choose the lowest sufficient profile from its allowed
range. Resolve an explicit role preference (such as coordination or Explore/Spec)
before the host's general workload preference. Select the worker independently
of the coordinator, pass its resolved model/effort through supported launch
controls, and include the profile and a short task-specific reason in the existing
handoff. Profile selection does not select a phase, authorize another worker, or
change review gates. A current-session operator choice wins. If a host cannot
select or confirm a required profile, report that limitation; inherit a host
default only when the applicable preference permits it.

Reassess the implementation profile when a new boundary appears or two correction
attempts fail on the same unresolved mechanism. Diagnose first: environment,
tooling, or authority failures do not justify a stronger model. Escalate only
within the permitted profiles and when the diagnosis warrants it; explicit fixed
choices still win. Preserve the candidate and evidence, confirm the old writer is
inactive before any replacement, and hand off once instead of starting parallel
attempts. An already-selected reviewer and its profile remain unchanged.

An explicit inner-review mapping from the actual author's profile takes precedence
over `inherit`; it selects one fresh reviewer, not an additional review round.
`Inner review: inherit` means the actual spec author or implementer's host and
model/effort profile in a fresh context. Prefer that host's native isolated agent;
use its same-host fresh CLI context when needed. Coworker PR challenger recipes,
outer-review lists, and coordinator defaults do not select an inner reviewer.
Cross-host inner review requires an explicit inner profile or operator choice.

- `risk-selected`: apply the positive outer selectors below.
- `operator-invoked`: run an outer gate only on a direct operator request.
- `disabled`: omit outer gates from normal completion. A direct operator request
  may override this preference for that invocation.

For a selected outer gate, first resolve the eligible profiles for the actual
authoring/implementation host and applicable complexity tier. An author-specific
list replaces the global list; exclusions apply before ordering or fallback.
`prefer-different-host` chooses the first eligible profile on another host, then
follows the eligible order. `ordered` follows that order directly. Same-host fresh
review remains independent, but is permitted only when both eligible and allowed.
Never broaden an eligible list because a host is unavailable. If origin is unknown,
use an explicitly configured unknown-origin list or an unconditioned global list;
otherwise report the missing origin without guessing.

Use exactly one reviewer, without child reviewers or helper fan-out unless the
operator separately authorizes it. Check the actual run's reported model and any
substitution/reroute notice before accepting a verdict. A substituted model or
unconfirmed required profile cannot certify the gate. A successful preliminary
probe does not establish the later run's identity; probes are optional capability
diagnosis, not a prerequisite for every review. If a required gate has no permitted
fresh context, report the missing capability rather than weakening or duplicating
it. Same-reviewer correction loops keep their selected profile.

## Positive phase triggers

- **Explore:** multiple credible approaches or an unowned boundary whose evidence
  changes the design.
- **Spike:** one named uncertainty can reject or materially reshape the design and
  can be proved safely with disposable work.
- **Spec:** the operator requests a formal implementation-ready plan or downstream
  execution needs durable acceptance and verification scope.
- **Outer spec review:** hard-to-reverse architecture/product policy; a material
  contract/API/schema change; material persisted-lifecycle, migration, or
  data-loss risk; auth/security/identity; provider/dependency/toolchain strategy;
  cross-system rollout/cutover; a material unproven bet; or an operator request.
- **Outer implementation review:** a diff or inner-review patch materially
  changing a contract/API/schema, persisted lifecycle/migration/data-loss
  behavior, auth/security/identity, provider boundary, dependency/toolchain, or
  cross-system rollout/cutover; a finding or proof gap exposing one of those
  material risks; or an operator request. An ordinary bounded correctness or
  test-quality finding requires correction and same-reviewer re-review, not an
  automatic outer gate. Reassess the actual risk of its resolution.

A named surface selects an outer gate only when the work creates or materially
revises its external, persisted, or security invariant, authority,
failure/recovery behavior, provider/toolchain behavior, or rollout. Proximity,
code volume, or “more review might help” is insufficient; otherwise skip with a
one-line reason and do not ask for a waiver.

When required source reviews are complete and only later runtime or operator
evidence remains to be reviewed, use `REVIEW.md`'s evidence-only completion mode
if its admission conditions hold. It cannot replace a selected full source gate
or an explicit full-review request. Use the existing gate's reviewer routing and
same-reviewer correction rules; this mode does not add another review round.

## Planner ownership and delegation

When a named main planner is active, it alone owns shared program/index state,
scope, sequencing, dependencies, and operator-facing decisions. Workers update
only their work-item artifact and return reconciliation facts. Otherwise, the
task completing work owns the normal state update.

Plan directly by default. When the host adapter configures an evidence-helper
profile, the planner may delegate a bounded, independently answerable evidence
question with a named stop condition; otherwise it works serially. Helpers return
sourced observations and uncertainty, not judgments or decisions; they do not
implement, mutate shared state, or delegate. Do short lookups directly; delegate
only when the separate question justifies another context. Use one helper when
delegation is warranted; a second requires a separate question or adversarial
purpose. The planner checks
load-bearing claims and alone turns the evidence into plans, phase choices, and
operator-facing recommendations.

Initial implementations and certifying reviews use fresh contexts when required
and available; re-review reuses the original reviewer. If the selected route
cannot provide fresh context, isolation, configured model selection, or
resumption, report the exact limitation instead of claiming the capability.

## Shared handoff envelope

```text
Work item: stable ID, human-readable name, source, repository
Goal / non-goals: observable outcome and deliberate exclusions
Scope: exact branch, base/tip or files, checkout/worktree owner and isolation state
Author: actual phase author/implementer host and profile, or unknown; coordinator host separately when different
Acceptance: behaviors that must hold
Evidence: exact commands/results and the revision, counts, hashes, or artifacts proved
Risk / remaining checks: blocked, stale, operator-only, or intentionally unselected
Phase / stop: selected workflow phase and exact return condition
```

The receiver validates the envelope independently. Narrative status and prior
verdicts are not proof. Phase payloads may add required facts but must not restate
kernel policy or create a second envelope.

Re-review carries only the prior findings, resolution mapping, changed range,
invalidated evidence, and current tip.

## Pause and recovery

Continue through research, drafting, safe proof, review patching, and same-reviewer
re-review. Pause only for a decision that changes observable product behavior,
authority or spend, a safety boundary, irreversible scope, or the currently
authorized task.

Park a decision or blocked proof that affects one branch while independent
authorized work continues. Batch genuine operator questions with the recommended
default and consequence; yield early only when every useful path depends on an
answer or an agreed checkpoint requires it.

When the operator says `keep going`, `finish`, `do not stop`, or `run until
<result>`, the active owner states one checkable exit predicate and continues
within the existing authority envelope. Status updates and an unproductive
approach do not end the run. Do not repeat an unchanged attempt without new
evidence; distinguish a product defect from a false premise, harness/setup
failure, or environmental limitation, and change approach when evidence
invalidates the current one. Stop when the predicate holds, a material gate
blocks every useful path, no credible safe in-scope approach remains, or the
operator stops the run.

Do not replace a worker on transcript silence alone or while an active writer
cannot be ruled out. Inspect the named task and checkout state. A blocked live or
operator proof returns the exact missing capability or authorization and is not
retried until that condition changes.
