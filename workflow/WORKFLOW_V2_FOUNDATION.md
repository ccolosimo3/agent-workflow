# Agent Workflow V2 Foundation

Status: draft for operator review. This document does not activate V2 or change
the current workflow.

## Recommendation

Build V2 beside the current workflow as a portable, plugin-distributed core.
Keep the planning, proof, specification, implementation, and independent-review
loops that catch real defects. Remove their duplicated instructions, make every
optional phase enter on a positive trigger, and progressively disclose detailed
doctrine without splitting the review rubric until pilots prove that safe.

The goal is not fewer safeguards. It is fewer places describing each safeguard
and less process for work that does not need the full path.

## Local evidence behind the redesign

This evidence explains the operator's V2 decision; it is not part of the
portable runtime package.

The current workflow has already proved three important things:

1. **The loops work.** Inner and outer reviews caught real persistence,
   provenance, migration, permission, cleanup, portability, and fail-open
   defects in Townchest COM-143 and Vendor Intelligence PRs #325, #389, and the
   Lightsail work. Real-boundary spikes also prevented unsafe test deletion in
   Townchest PR #718.
2. **The same assurance is often applied too broadly.** Narrow documentation,
   deterministic replay, test-only follow-ups, and small cleanup work have
   triggered long handoffs, broad verification, or formal review artifacts.
   Vendor Intelligence's closed food-admission PR is the clearest late size/value
   failure: a roughly 3,600-line sibling was built before the workflow challenged
   whether that lifecycle was warranted.
3. **Instruction duplication is now the main harness cost.** The kernel and six
   canonical authorities are about 1,474 lines; the core phase/review skills add
   about 1,217 lines; kickoff templates add another 533. Review sequencing,
   template fidelity, test judgment, UI rules, and re-review behavior are repeated
   across several of those surfaces.

Recent task history adds four operational lessons:

- A compound planning run can spend extraordinary usage when planners delegate
  to more planners and each lane recreates orientation and review state.
- Review severity improves when a candidate must be shown reachable on a
  supported path and tied to an actual contract before it becomes blocking.
- Transcript silence is not proof a worker is dead; redispatch can create
  competing writers. Worktree state, logs, and elapsed time are better evidence.
- Exact branch, tip, counts, commands, and unresolved checks make handoffs more
  reliable than narrative status claims.

## Goals

- Preserve the current quality floor and same-reviewer convergence loops.
- Keep a deliberate route from planning through proof, specification,
  implementation, and independent review.
- Reduce default context, repeated output, task transitions, and unnecessary
  verification.
- Make the workflow understandable and installable by another engineer without
  importing one operator's paths, models, providers, or project conventions.
- Keep project facts and exceptional local policy in a small repo adapter.
- Make the strict path easy to select when risk earns it and easy to skip when it
  does not.

## Non-goals

- Weakening code, test, security, data, or review standards.
- Making every task traverse every phase.
- Replacing reviewer judgment with a score, line-count cap, or mechanical risk
  checklist.
- Hardcoding a preferred model, provider, tracker, branch, or desktop app into
  the portable core.
- Rewriting `prreview` into an ordinary implementation review. Coworker PR review
  has a different discovery and calibration job.
- Migrating or deleting V1 before a side-by-side pilot.

## V2 operating model

V2 is one state graph with optional evidence phases, not a fixed ceremony:

```text
plan
  -> explore, when the approach is genuinely open
  -> spike, when one load-bearing bet can be falsified cheaply
  -> spec
  -> inner spec review <-> revision
  -> outer spec review <-> revision, when risk selects it
  -> implementation
  -> inner implementation review <-> patch
  -> outer implementation review <-> patch, when risk selects it
  -> complete
```

This is a map of available phases, not a required linear pipeline. The operator
selects movement between phases; the inner review/revision loops proceed
autonomously once selected. Fast work may move directly from a conversation to
implementation without creating a plan artifact, while formal explore and spike
stop at their result until the next phase is selected.

The graph preserves the full workflow while allowing three proportionate routes:

| Route | Use when | Expected path |
| --- | --- | --- |
| Fast | The outcome and shape are clear, the change is local, and one focused proof can falsify it | implement -> inner review; a wholly non-generated, non-normative documentation diff that changes no code, config, contract, setup, policy, architecture, verification, or operating procedure may use the self-check off-ramp; workflow/policy docs never qualify |
| Standard | The work needs a durable implementation plan but no unresolved architecture bet | spec -> inner spec review -> implement -> inner implementation review |
| Assured | Architecture, persistence, security, identity, provider, migration, cross-system, or similarly consequential risk is present | explore/spike as needed -> spec -> inner plus risk-selected outer spec review -> implementation -> inner plus risk-selected outer implementation review |

Route changes are allowed when evidence changes the task. “More review might
help” is not a route trigger.

### Phase entry rules

- **Plan**, when a named main planner is active, keeps one aligned planning
  authority for the program. It owns shared scope, sequencing, and operator
  decisions; otherwise the finishing task owns normal state updates. It may use
  bounded investigators for independent unknowns, but does not create planners
  that create more planners: nested delegation is prohibited, and helpers return
  evidence to the owning planner.
- **Explore** starts only when there are multiple credible approaches or an
  unowned boundary whose evidence changes the design. It returns a recommendation
  and unresolved decision; it does not automatically start a spike or spec.
- **Spike** starts only for one named uncertainty whose answer could reject or
  materially reshape the proposed design. Proof code is disposable unless it
  protects durable behavior.
- **Spec** defines the next independently reviewable risk boundary, not the whole
  imagined destination. Before review-ready promotion or implementation dispatch,
  compare a materially larger proposal with the nearest complete pattern using
  the intended outcome, non-goals, added durable responsibilities and artifacts,
  operator steps, reuse, and proven consumers. If the shape is not justified or
  its value is unresolved, stop at a named shape decision or disposable spike;
  do not defer the challenge to implementation review. Once review-ready, the
  inner loop proceeds without an ordinary status pause; only a material
  operator-owned direction decision stops it.
- **Outer spec review** is selected by positive risk: hard-to-reverse architecture
  or product policy; contract, API, or schema change; persisted-state lifecycle,
  migration, or data-loss risk; auth, security, or identity; provider, dependency,
  or toolchain strategy; cross-system rollout or cutover; a material unproven bet;
  or an operator request. Small, local, reversible specs may stop after inner
  convergence.
- **Implementation** rechecks minimum-sufficient shape before committing to a
  materially larger design. It uses the nearest complete pattern and must trace
  added durable responsibilities to present requirements or observed failures.
- **Inner implementation review** remains the normal quality gate. Findings are
  patched and returned to the same reviewer.
- **Outer implementation review** is selected for the same consequential surfaces,
  an inner finding that establishes a production-correctness, public/contract,
  persistence, security, or data-loss defect, or an operator request. Outer-owned
  patches return directly to the same outer reviewer.

### Pause rules

Continue autonomously through research, drafting, focused proof, review patching,
and same-reviewer re-review. Pause only for a decision that changes observable
product behavior, authority or spend, a safety boundary, irreversible scope, or
the currently authorized task. A normal finding, status exchange, or reversible
implementation correction is not a pause.

## One owner per rule

V2 uses progressive disclosure and explicit ownership:

| Concern | Canonical owner | Other files do |
| --- | --- | --- |
| Authority, safety, route selection, universal quality floor | kernel | link only |
| Phase transitions, review selection, freshness, independence, reuse | handoff state machine | provide invocation-specific fields |
| Planning artifacts, slicing, lifecycle | planning authority | link only |
| Test value and verification doctrine | testing authority | apply it to the touched surface |
| Reviewer investigation, severity, verdict | `REVIEW_RUBRIC.md` | link only |
| UI and accessibility | frontend module | load only for UI work |
| Project commands, layout, risks, docs owners | repo adapter | stay out of portable core |
| Task creation, models, web, independent-review provider | host adapter | stay out of phase semantics |

The kernel should no longer carry a second miniature test manual. Skills should
not restate the review loop. Kickoffs should contain data, not policy.

## Lean review architecture

Phase 1 keeps `REVIEW_RUBRIC.md` intact as the single review authority. The
following is the intended universal spine, not permission to omit the rubric's
specialized checks:

1. Freeze the intended range and read every changed file in context.
2. Re-derive the acceptance criteria; treat summaries and receipts as claims.
3. Trace changed behavior through its real operation boundary and supported paths.
4. Admit a finding only with a concrete regression path, evidence, impact, and
   contract or requirement authority.
5. Calibrate severity after discovery. Uncertainty or a generic framework
   possibility is not automatically blocking.
6. Return a strict verdict, actionable findings, useful suggestions/nits,
   invalidated verification, and remaining operator checks.

For a blocking finding, state the mechanism, a reachable supported path, the
affected contract or requirement, and the material consequence. A generic
framework capability or execution-policy concern without that path is not
blocking by itself. Unknown frequency remains unknown; it neither creates nor
erases a blocker when mechanism and contract impact are proved.

After pilots, V2 may evaluate splitting specialized checks into compact modules:

- tests and verification;
- contracts, serialization, and information loss;
- persistence, schema, migration, and concurrency;
- CI, deployment, and operational workflows;
- security, permissions, identity, and secrets;
- UI, accessibility, and rendered behavior;
- provider/integration boundaries;
- performance and scale.

That split is not part of the first V2 release. It requires a disposition of every
existing rubric rule plus mandatory surface classification: load every applicable
module, use the conservative default when applicability is uncertain, and never
issue a verdict with an unclassified changed surface. Modules would supply
specialized failure modes and proof bars, not a second verdict process.

`prreview` remains a separate external-review skill. Preserve its thorough lead,
challenger, convergence, active proof, and final calibration behavior. It may
reuse the rubric, but ordinary implementation review must not inherit its fanout
or reporting ceremony. When selected for a coworker PR, it must not be silently
substituted with `implreview`; “optional” packaging means only that an installation
may omit coworker-PR review entirely.

### Review output

The operator-facing result should normally contain:

- verdict;
- exact severity and path/line findings, ordered by calibrated severity;
- a grouped test-quality summary and separate `PASS`/`FAIL` result;
- suggestions or nits worth acting on;
- verification invalidated or still required;
- unresolved operator decision, if any;
- an implementer directive when the verdict is actionable.

Clean acceptance-criteria rows, passing test ledgers, raw candidate maps, and
full command transcripts remain in local evidence when useful; they are not
reprinted by default. Failed test-quality rows, non-ship dispositions, and
`[decision-required]` items remain explicit. Test quality and same-reviewer
re-review semantics are not relaxed—only clean reporting is compressed.

## Compact handoff packet

Every handoff uses a shared semantic envelope plus the smallest phase-specific
payload required to preserve intent, artifact state, repo conventions,
independence, and test-quality context:

```text
Work item: stable ID, human-readable name, source, and repository
Goal / non-goals: observable outcome and deliberate exclusions
Scope: exact branch, base/tip or files, checkout/worktree, owner, and isolated/shared state
Acceptance: behaviors that must hold
Evidence: exact commands/results and the base/tip, counts, hashes, or artifacts they prove
Risk / remaining checks: blocked, stale, operator-only, or intentionally unselected
```

The receiver independently validates it; narrative completion or review claims
are not evidence by themselves. Reused evidence from a stale or sibling base is
not current until its causal surface is rechecked. Phase payloads may add required
fields but cannot restate policy or invent another envelope. Re-review needs only
the prior findings, resolution mapping, changed range, invalidated evidence, and
current tip.

Phase payload schemas initially mirror the applicable existing `kickoffs/*.md`
fields; no required field may be removed without a rule-disposition record.

For mutating phases, one task owns a checkout. Observers use an isolated checkout
or remain read-only. An unexpected branch, tip, or path change is a collision:
stop and re-freeze; never switch, reset, or clean a checkout owned by another
task.

## Verification without repetition

Use names rather than private codes in the portable workflow:

- **Loop proof:** smallest proof of the changed behavior.
- **Patch proof:** checks plausibly affected by a review patch.
- **Gate proof:** affected builds, tests, contracts, boundaries, or end-to-end
  paths selected by changed risk.
- **Operator proof:** live, paid, hardware, destructive, or prepared-environment
  evidence.

Preserve these rules:

- A test must protect durable behavior and fail when its regression returns.
- Prove the smallest real operation boundary: save/reload for persistence, the
  actual consumer import, and the fresh-runner job for CI.
- Green evidence stays valid until a causal delta can invalidate it.
- Do not repeat a broad gate after a narrow or tests-only patch unless shared
  infrastructure, the production path, or the proof itself changed.
- Do not create permanent tests for incidental absence, source shape, call order,
  or coverage theater unless that shape is the contract.
- Separate correctness proof from noisy performance telemetry; repeat an
  expensive benchmark only when its path or contract changed or prior evidence
  is suspect.
- When freshness or isolation is part of the claim, prove it from a clean tracked
  snapshot, exclude private/ignored inputs explicitly, and record bootstrap
  conditions; a warm operator checkout is not equivalent.
- For deterministic replay of already verified immutable inputs, use the
  repository's canonical verifier resolved through the repo adapter and the
  smallest closure that proves the changed behavior. Retain full adversarial
  closure for live/paid work, identity or external side effects, autonomous
  canonical writes, and historically silent failures.
- Do not use retries to turn suspected quiet nondeterminism green. Distinguish
  loud environmental failure from quiet flakiness and require an independent
  second execution when one green run is not trustworthy.
- A blocked operator proof returns `BLOCKED` or `NO-GO` with the exact missing
  capability, authority, or environment condition. Do not retry or redispatch
  until that condition changes; blocked is not empty, skipped, or successful.

## Planning and delegation

When a named main planner is active, it remains a useful long-lived alignment
point. V2 changes how it delegates:

- It owns the program map, next risk boundary, dependencies, and operator-facing
  decisions.
- It normally plans directly. It delegates bounded evidence questions, not whole
  duplicate planning processes.
- One investigator is the default when delegation helps; add another only for an
  independently named question or adversarial check. Nested delegation is
  prohibited; helpers return evidence to the owning planner and do not spawn
  further helpers.
- Initial implementation and certifying reviews use fresh contexts when
  independence is required; review patches return to the same reviewer. Evidence
  helpers do not issue verdicts. If a host cannot provide fresh context or
  checkout isolation, its adapter reports that limitation rather than claiming
  independence.
- Do not redispatch on transcript silence alone or while an active writer cannot
  be ruled out. Inspect the named task and checkout state; when reviewer capacity
  is unavailable, park one frozen ready handoff rather than polling or adding
  coordination machinery.

Model names and reasoning levels belong to the host/operator adapter. The portable
rule is simply to use the least expensive capable evidence helper and a strong
independent reviewer for consequential gates.

## Artifact policy

- Conversation is enough for compact work.
- Create one living work-item document when downstream implementation or review
  needs durable scope and evidence; it is a decision/evidence index, not a
  transcript.
- Once formally invoked, explore and spike retain compact durable outputs required
  by their phase contracts. Compact work avoids those artifacts by skipping the
  phase, not by erasing its result afterward.
- Keep detailed receipts local; handoffs summarize them.
- Do not create a program index for compact work unless the repo's planning
  authority requires one; preserve ownership of an existing index.
- Do not test document placement, prose location, or template shape unless a real
  consumer depends on it.

## Portable package shape

V2 should be authored once and exposed through thin integrations. The exact
layout will be validated with the Codex skill/plugin creators before scaffolding;
the Codex distribution must at least have this discoverable shape:

```text
agent-workflow-v2/
  .codex-plugin/
    plugin.json
  kernel/
    AGENTS.md               # documented install template, not auto-activated
  skills/
    plan-next/SKILL.md
    explore/SKILL.md
    spike/SKILL.md
    spec/SKILL.md
    specreview/SKILL.md
    specrereview/SKILL.md   # thin compatibility alias
    implement/SKILL.md
    implreview/SKILL.md
    implrereview/SKILL.md   # thin compatibility alias
    outerreview/SKILL.md
    outerspecreview/SKILL.md # distinct spec mode over shared behavior
    prreview/SKILL.md       # optional coworker-PR extension
  references/
    HANDOFF.md
    PLANS.md
    TESTING.md
    REVIEW_RUBRIC.md
    FRONTEND.md
  templates/
    repo-adapter.md
    handoff.md
    pr-body.md
  host-adapters/           # optional extensions, outside portable semantics
    codex.md
    claude.md
```

Compatibility aliases keep `/specrereview` and `/implrereview` discoverable but
route to shared behavior rather than owning copied policy. `/outerspecreview`
retains its holistic no-code spec contract while sharing independence, freshness,
and same-reviewer mechanics with `/outerreview`.

The Codex distribution should be a plugin containing the skills and references,
with a small documented kernel install step. Core workflow skills resolve the
bundled kernel and required references on invocation and fail closed if they are
unavailable; the installed `AGENTS.md` also applies the quality floor to ordinary
non-skill work. Only read-only/discovery utilities may claim standalone use
without that kernel. Host and repo adapters may declare capabilities or narrow
behavior, but cannot widen kernel approval, independence, or review requirements.
Provider-specific launchers, personal archive tools, personal model routing, and
project-specific shims are optional adapters or extras—not the portable core.

## Migration plan

### Phase 0 — Freeze and measure V1

- Keep V1 active and record its current instruction size, average handoff size,
  task transitions, bootstrap time, verification reruns, review findings,
  severity changes, false blockers/false greens, operator corrections, and—where
  the host exposes them—turns, tool calls, and context usage.
- Select representative completed tasks whose outcomes and escaped findings are
  known.

### Phase 1 — Build V2 beside V1

- Create the small kernel, single handoff state machine, compact packet, and
  host/repo adapter contract.
- Port skills as thin phase routers. Preserve compatibility aliases.
- Keep `REVIEW_RUBRIC.md` intact for the first V2 pilot. Consider modules only
  after every rule has an explicit disposition and the pilot validates a
  conservative surface classifier.
- Do not alter V1 symlinks or default startup files.

### Phase 2 — Shadow pilots

Replay or prospectively run V1 and V2 against the same frozen base/tip,
acceptance criteria, and available evidence inputs for a balanced set:

- a narrow documentation or copy change that should stay Fast;
- a deterministic behavior fix that needs a focused test and inner review;
- Townchest PR #718-style test-removal question where a real proof must prevent
  unsafe deletion;
- Townchest COM-143-style persistence/permission/migration change that must keep
  the full loop;
- a CI workflow change where fresh-runner viability matters;
- a Vendor Intelligence replay/admission proposal where the shape gate should
  reject a bespoke lifecycle before implementation;
- a shared compiler/provider/deployment change where strict outer review must
  continue finding real defects;
- a coworker PR review using the existing `prreview` as the quality baseline.

Include one adjudicated over-severity case and one contaminated-snapshot or
false-green case so the pilot tests calibration and evidence validity, not only
defect recall.

### Phase 3 — Coworker beta

- Package V2 as an installable Codex plugin with a short repo-adapter walkthrough.
- Give beta users only the portable defaults; do not import personal paths,
  archive tooling, or model preferences.
- Capture where users need clarification, where phases over-trigger, and where a
  safeguard was hard to discover.

### Phase 4 — Promotion

Promote V2 only when the pilot shows:

- no lost authority, safety, real-boundary testing, review independence, or
  same-reviewer convergence rule;
- the same known material defects are caught on high-risk cases;
- fewer unnecessary phase activations, task transitions, broad reruns, and
  operator corrections on compact/standard cases;
- no increase in false blockers, unsupported findings, false-green verification,
  checkout collisions, or escaped material defects;
- no loss of independent coworker-PR review or same-reviewer convergence;
- materially smaller startup instructions and handoff output;
- another engineer can install and understand the workflow without private
  context.

Rollback is disabling the V2 plugin and retaining V1; no destructive migration
is required.

## Size measurements, not policy gates

Measure the always-loaded kernel, phase/review skill prose, kickoff duplication,
and ordinary handoff size during pilots. V2 should make each materially smaller,
but no percentage or line budget authorizes deleting a safeguard, required phase
payload, or evidence. A larger canonical authority is acceptable when it is the
single owner of genuinely needed doctrine.

## Decisions before scaffolding

1. Whether `outerreview` becomes one parameterized spec/implementation engine or
   retains two thin public skills over shared references. Recommendation: retain
   both invocations for clarity, share all behavior underneath.
2. Whether the first coworker release includes `prreview` or ships it as an
   optional extension. Recommendation: include it as an optional bundled skill;
   do not let its process affect implementation review.
3. Whether V2 keeps `.agent-workflow/plans` as its default durable-plan location.
   Recommendation: make the location a repo-adapter choice and require no plan
   directory for compact work.
4. Whether the review rubric is eventually split into conditional modules.
   Recommendation: not in the first release; earn that change with a rule
   disposition, conservative classifier, and frozen-case pilot.

No decision is needed yet about model names, Claude profiles, or personal plan
archival; those are deliberately outside the portable core.
