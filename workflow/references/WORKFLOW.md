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

## Host and outer-gate policy

Read `HOST.local.md` from the canonical V2 package root when present. It owns
available hosts, named model profiles, workload preferences, and outer routing;
repository adapters do not.
Without one, treat outer gates as `operator-invoked` and use the current host's
capabilities without inventing cross-host launch or model selection.

When dispatch exposes model choice, follow the applicable fixed profile or
choose the lowest profile sufficient for the task from its allowed range; do not
default to the strongest setting. A current-session operator choice wins. If the
host cannot select or confirm the profile, inherit its default and report that
limitation rather than claiming a configured choice.

- `risk-selected`: apply the positive outer selectors below.
- `operator-invoked`: run an outer gate only on a direct operator request.
- `disabled`: omit outer gates from normal completion. A direct operator request
  may override this preference for that invocation.

When a gate is selected, use exactly one configured reviewer. A
`prefer-different-host` preference chooses the first eligible configured profile
whose host differs from the known authoring/implementation host, then follows the
configured order. If the origin host is unknown, do not guess. Use a same-host
fresh context only when configured or directly requested; it remains valid
independence. If a required risk-selected gate has no permitted fresh context,
report the missing capability rather than silently weakening or duplicating it.

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
  cross-system rollout/cutover; an inner finding establishing a
  production-correctness, public/contract, persistence, security, or data-loss
  defect; a test-quality finding requiring a production behavior/contract patch
  because that behavior was not previously proven; or an operator request.

A named surface selects an outer gate only when the work creates or materially
revises its external, persisted, or security invariant, authority,
failure/recovery behavior, provider/toolchain behavior, or rollout. Proximity,
code volume, or “more review might help” is insufficient; otherwise skip with a
one-line reason and do not ask for a waiver.

## Planner ownership and delegation

When a named main planner is active, it alone owns shared program/index state,
scope, sequencing, dependencies, and operator-facing decisions. Workers update
only their work-item artifact and return reconciliation facts. Otherwise, the
task completing work owns the normal state update.

Plan directly by default. When the host adapter configures an evidence-helper
profile, the planner may delegate a bounded, independently answerable evidence
question with a named stop condition; otherwise it works serially. Helpers return
sourced observations and uncertainty, not judgments or decisions; they do not
implement, mutate shared state, or delegate. One helper is the default; a second
requires a separate question or adversarial purpose. The planner checks
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
