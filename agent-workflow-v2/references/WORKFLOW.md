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
  -> outer spec review <-> revision, when selected by risk
  -> implementation
  -> inner implementation review <-> patch
  -> outer implementation review <-> patch, when selected by risk
  -> complete
```

The graph is not a mandatory pipeline. The operator selects each substantive
phase: explore, spike, spec, or implementation. Selecting formal spec or
implementation includes its required inner review as that phase's completion
gate; do not pause merely to ask whether to start it. Once a review gate starts,
its same-reviewer correction loop continues autonomously until approved, blocked
by a material decision, or its bounded retry limit is exhausted.

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

## Positive phase triggers

- **Explore:** multiple credible approaches or an unowned boundary whose evidence
  changes the design.
- **Spike:** one named uncertainty can reject or materially reshape the design and
  can be proved safely with disposable work.
- **Spec:** the operator requests a formal implementation-ready plan or downstream
  execution needs durable acceptance and verification scope.
- **Outer spec review:** hard-to-reverse architecture/product policy; contract,
  API, or schema change; persisted lifecycle, migration, or data-loss risk;
  auth/security/identity; provider/dependency/toolchain strategy; cross-system
  rollout/cutover; a material unproven bet; or an operator request.
- **Outer implementation review:** a diff touching a contract/API/schema,
  persisted lifecycle/migration/data-loss surface, auth/security/identity,
  provider boundary, dependency/toolchain, or cross-system rollout/cutover; an
  inner finding that establishes a production-correctness, public/contract,
  persistence, security, or data-loss defect; a test-quality finding that
  requires a production behavior or contract patch because that behavior lacked
  proof; or an operator request.

## Planner ownership and delegation

When a named main planner is active, it alone owns shared program/index state,
scope, sequencing, dependencies, and operator-facing decisions. Workers update
only their work-item artifact and return reconciliation facts. Otherwise, the
task completing work owns the normal state update.

Plan directly by default. Delegate only a bounded evidence question with a named
stop condition. One helper is the default; a second requires a separate question
or adversarial purpose. Nested delegation is prohibited. Evidence helpers do not
implement, mutate shared state, recommend a phase transition or owning-phase
outcome, or issue its `GO` / `NO-GO` / review verdict.

Initial implementations and certifying reviews use fresh contexts when the host
supports them; re-review reuses the original reviewer. If the host cannot provide
fresh context, isolation, model selection, or resumption, report the limitation
instead of claiming the capability.

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

Do not replace a worker on transcript silence alone or while an active writer
cannot be ruled out. Inspect the named task and checkout state. A blocked live or
operator proof returns the exact missing capability or authorization and is not
retried until that condition changes.
