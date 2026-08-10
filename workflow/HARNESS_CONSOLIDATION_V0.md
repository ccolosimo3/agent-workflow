---
title: Lean workflow harness consolidation V0
status: final
created: 2026-08-10
updated: 2026-08-10
owner: ccolosimo
issue: none
related:
  - workflow/AGENTS.md
  - workflow/HANDOFF.md
  - workflow/PLANS.md
  - workflow/TESTING.md
  - workflow/REVIEW_RUBRIC.md
---

# Lean workflow harness consolidation V0

## Recommendation

Consolidate the harness around a small always-loaded kernel, short repo routers,
and strong on-demand authorities. Do not roll back the workflow wholesale and
do not weaken the implementation, verification, or review standards that are
working. Apply the change in two ordered phases, with each repository producing
its own independently reviewable and reversible commit:

1. reduce always-loaded instructions and skill metadata;
2. reduce handoff, planning-artifact, and coordination ceremony.

Leave `TESTING.md`, `REVIEW_RUBRIC.md`, and `prreview`'s discovery/convergence
behavior semantically unchanged in V0. Consider deeper deduplication only after
the lighter loading model has been piloted on real work.

## Problem

The harness has accumulated useful rules in too many simultaneously active
layers. Agents spend substantial context and attention re-reading global
doctrine, tracked repo policy, local adapters, and verbose skill metadata before
reaching the task. The same safety or quality principle is then repeated in
kickoffs and handoffs, which encourages agents to perform and narrate the full
ceremony even when the risk is small.

Measured from the live files on 2026-08-10:

| Surface | Lines | Words | Bytes |
| --- | ---: | ---: | ---: |
| global `workflow/AGENTS.md` | 375 | 2,832 | 20,809 |
| Vendor Intelligence tracked + local agent files | 435 | 3,167 | 23,562 |
| Townchest tracked + local agent files | 382 | 2,857 | 22,176 |
| all workflow skill descriptions | — | — | 10,720 characters |
| `HANDOFF.md` | 309 | 2,394 | 16,708 |
| `REVIEW_RUBRIC.md` | 357 | 3,169 | 22,293 |
| `TESTING.md` | 226 | 1,934 | 13,180 |

This means an ordinary Vendor Intelligence session is directed through roughly
810 lines of global, tracked, and local agent instructions before any invoked
skill or task document. Townchest begins with roughly 757 lines.

### Structural evidence

All line citations in this subsection describe the frozen pre-change files at
workflow base `8ac50ad85327f32e8113eb22ffa6d9077d55dab7` and the adapter baselines
recorded under Task A4; they are evidence for the consolidation, not current-tip
navigation.

- The global kernel carries both a full test-quality digest and routing to the
  canonical doctrine (`workflow/AGENTS.md:46-79`), detailed review sequencing
  plus routing to `HANDOFF.md` (`workflow/AGENTS.md:250-267`), and a long
  verification implementation (`workflow/AGENTS.md:294-349`). The principles
  are valuable; the always-loaded level is too detailed.
- `HANDOFF.md` mixes durable review sequencing with approximately 110 lines of
  Claude CLI syntax and model-selection mechanics (`workflow/HANDOFF.md:128-237`).
  The latter is needed only when launching an outer gate.
- `PLANS.md` presents `PR_BODY.md`, `verification.md`, `reviews.md`, and
  `artifacts/` as the normal work-item contents (`workflow/PLANS.md:27-41`) even
  when a compact task needs only its living `README.md`.
- The formal `spec` path correctly stays serial by default, but every completed
  formal spec automatically enters review (`workflow/skills/spec/SKILL.md:40-60,
  93-102`). That is appropriate only because formal planning must now be
  explicitly invoked; casual questions and fast changes must stay outside it.
- The Vendor Intelligence local adapter is 281 lines and contains local plan
  layout, workflow modes, Linear formatting, docs classification, source-probe
  reminders, and detailed migration/tooling guidance. Existing authorities
  already own most of those subjects (`AGENTS.local.md:12-55,80-215,217-280`).
- The Townchest local adapter is 294 lines. Its tracked `AGENTS.md` now routes
  setup, verification, domain risk, codegen, migrations, and deployment to
  concise tracked owners (`/Users/ccolosimo/townchest/AGENTS.md:20-32`), while
  the local adapter still restates long destructive, Vercel, codegen, Biome,
  frontend, and E2E procedures.
- The restored `plan-next` direction already makes the main planning session the
  planner/coordinator and delegates execution to fresh Codex tasks
  (`workflow/skills/plan-next/SKILL.md:54-87`). Shared planning-state ownership
  is not yet defined clearly enough to prevent child tasks from concurrently
  rewriting `INDEX.md` and umbrella files.

### Behavioral evidence

The operator and the prior Vendor Intelligence planner task
`019fdeed-9b99-75e2-82b6-fb8711a4f1e5` observed:

- formal exploration or specification starting from simple questions;
- outer reviews and broad verification being selected without a named causal
  reason;
- completed work waiting and polling for reviewer capacity;
- separate branches being treated as blockers merely because they touched a
  shared planning or documentation file;
- very large documentation-survival ledgers and negative-control artifacts;
- multiple lanes concurrently editing `INDEX.md`, umbrellas, and lifecycle
  state;
- operator summaries led by SHAs, test counts, and review history rather than
  what the work changes and whether it is ready.

Some of these violate existing rules rather than being required by them. The
rewrite must therefore improve salience and routing instead of adding more
warnings.

## Goal

Make ordinary agents faster to orient and less likely to over-apply ceremony,
while preserving the quality, safety, and convergent review behavior that has
improved implementation and PR-review outcomes.

## Non-goals

- No relaxation of destructive, provider, paid-model, production, GitHub, or
  tracker approval boundaries.
- No weakening of behavioral test quality, causal verification selection,
  contract propagation, fresh-runner CI review, or real-boundary proof.
- No reduction in `prreview`'s lead/challenger convergence or large-PR fanout.
- No return of Orchestrator Mode, program ledgers, leases, hooks, or another
  persistent state machine.
- No project-source changes, dependency installation, tracker mutation, or
  automatic activation outside the private workflow and local adapters.
- No attempt to solve model verbosity or app progress-message behavior with
  additional doctrine.

## Invariants to preserve

The implementation must inventory every removed normative statement and show
where its authority remains. At minimum, preserve:

1. current-session human authority and repo-policy precedence;
2. dirty-worktree protection and no unrelated edits;
3. explicit approval for destructive, external, paid, provider, and shared-state
   mutations, including immutable worktree-install limits;
4. simplest complete, repo-conventional implementation with no speculative
   scope expansion;
5. proportional testing at the real behavior boundary and no coverage theater;
6. causal verification reuse and exact consumer-boundary proof;
7. one inner implementation review except the narrow documentation-only
   off-ramp;
8. positive risk-triggered implementation outer gates and same-reviewer
   re-review reuse;
9. explicit formal-planning triggers, proportional Tasks, and valid intermediate
   states;
10. `prreview`'s strict discovery first and calibrated operator-facing report
    last;
11. repo-specific hard edges such as Vendor Intelligence neutrality,
    files-as-record, bounded paid calls, and single-writer data; and Townchest
    branch naming, TARS prohibition, local-data safety, and generated-artifact
    handling.

## Decision brief

### Chosen: canonical owners plus router layers

Keep one canonical owner for each kind of rule. Automatically loaded files carry
only universal or repo-local facts that must affect nearly every task, plus
short routes to conditional owners. Skills load the deeper workflow only when
explicitly invoked or selected by a clear risk trigger.

This removes repeated context without discarding the underlying standards.

### Rejected: revert to the workflow from one or two weeks ago

A rollback would remove valuable later improvements together with the ceremony,
including causal verification reuse, durable test-value rules, positive
outer-gate routing, fresh-runner CI auditing, and the stronger external PR
review. It also would not solve duplicate local adapters.

### Rejected: line-edit every document in one pass

A big-bang rewrite would make it difficult to prove which authority owns a
removed rule and whether slower sessions improve because of loading, handoff,
or review changes. Two phases create a usable intermediate state and isolate the
largest source of context cost first; they do not combine separate repositories
into one review range.

## Canonical ownership after V0

| Concern | Canonical owner | Other surfaces do only this |
| --- | --- | --- |
| universal safety, authority, startup routing, quality floor | `workflow/AGENTS.md` | link to conditional doctrine |
| test principles and anti-patterns | `workflow/TESTING.md` | carry only a very short fallback digest |
| reviewer investigation and verdict semantics | `workflow/REVIEW_RUBRIC.md` | pass task context, not a second rubric |
| review sequencing, gate selection, reuse | `workflow/HANDOFF.md` | skills supply invocation-specific behavior |
| Claude outer-gate launcher syntax | one outer-review-only reference | `HANDOFF.md` links to it |
| planning layout and lifecycle | `workflow/PLANS.md` | repo plans README adds local layout only |
| shared project roadmap and planning state | main `plan-next` planner when active | child tasks update their own work item and report changes |
| repo facts and hard edges | tracked repo `AGENTS.md` and owning tracked docs | `AGENTS.local.md` carries only personal/local deltas and routes |
| coworker PR discovery/convergence/calibration | `prreview` + `calibrate-review` | general rubric supplies strict judging rules |

## Task A — reduce the always-loaded layer

This is the first rollout phase, not one cross-repository commit. Produce one
reviewable patch in the workflow repository and one separate patch in each
affected private planning repository. A later patch must not be required to
make an earlier repository valid.

### A1. Condense the global kernel

Edit `workflow/AGENTS.md` to retain the invariants above while replacing
procedural detail with routes:

- keep precedence, the universal quality floor, destructive-action categories,
  approval semantics, explicit fast/formal routing, the Work Item model, docs
  impact, verification tiers, review floor, and output budget;
- reduce the test digest to the smallest offline fallback that preserves
  behavior boundary, durable regression value, and anti-shape-test guidance;
- keep verification selection and causal-reuse semantics but remove examples or
  repetition owned by `TESTING.md`, `HANDOFF.md`, or repo verification docs;
- keep implementation/planning/review routes as concise contracts rather than
  step-by-step copies of their skills;
- do not move removed detail into another automatically loaded file.

Target: at least a 30% byte reduction without a missing invariant. The target is
a guardrail, not permission to compress wording until it becomes ambiguous.

### A2. Turn local adapters into routers

Edit the live symlink targets in the two nested private planning repositories as
separate repository-scoped patches; do not overwrite their existing unrelated
changes. Before editing, record that repository's `HEAD`, `git status`, and the
live hash/diff of every touched file. If an overlapping file still contains
unowned changes, preserve them and isolate the consolidation hunk; if that cannot
be reviewed independently, defer that adapter patch rather than absorbing the
dirty work.

Vendor Intelligence keeps only:

- local planning-repo identity and a route to its README/INDEX;
- the dashboard accessibility preference;
- the planning-only `PLANNING.md` route;
- concise tracker/branch/label deltas not owned elsewhere;
- reviewer convention routes;
- disposable DB authorization and any unique local migration safety delta;
- exact local-only exceptions not present in tracked policy.

Move or route the current detail as follows:

- umbrella/slice/archive mechanics → `.agent-workflow/plans/README.md`;
- Linear body formatting and plan-code rules → `.agent-workflow/PLANNING.md`;
- docs classification → tracked `docs/README.md`;
- source-probe process → tracked `docs/workflows/` owners;
- commands and verification → tracked `docs/COMMANDS.md` and
  `docs/VERIFICATION.md`.

Townchest keeps only:

- local context and private coding-standard routes;
- the Linear mutation delta and branch-name rule;
- local planning-repo route;
- TARS prohibition and unique local approval deltas;
- any short-lived local exception not appropriate for tracked policy.

Route setup, local data, migrations, GraphQL/codegen, verification, CI/deploy,
and provider rules to the tracked owners already named by Townchest
`AGENTS.md`. Keep private detailed overlays in their existing on-demand
references only where they still add information.

Target: each local adapter is no more than roughly 100 lines and the combined
global + tracked + local startup instruction bytes for each project fall by at
least 30%.

### A3. Shorten skill discovery metadata

Edit only the YAML `description` of each `workflow/skills/*/SKILL.md` during
this substep. Each description should state:

- the outcome;
- the explicit/natural-language trigger;
- the most important exclusion.

Move models, loop mechanics, fallback behavior, detailed profiles, and repeated
guardrails into the already on-demand skill body. Preserve skill selection
semantics. Target no description above roughly 650 characters and no more than
6,000 description characters total. For every description actually changed,
record one positive trigger and its principal exclusion before editing, then
confirm both in a fresh task after the application reloads the metadata. Do not
change descriptions that already meet the outcome/trigger/exclusion contract
merely to make the aggregate smaller.

### A4. Preserve the restored planner model

Treat the live uncommitted `plan-next` restoration as authorized predecessor
work, not collateral to rewrite. Its current baseline is workflow repository
`HEAD` `63658360ccc65105b4ef8ee9d24b8078500efcc6`, with live file hashes
`3493b85b5c07ff23367666e2db3a1865880cc780` (`SKILL.md`) and
`c7fdb8f050b3099246fa2fac47ec417acf4dad24`
(`agents/openai.yaml`). Land or otherwise freeze that restoration as its own
reviewable predecessor before changing skill metadata. A3 preserves the frozen
description's invocation behavior.

The current nested-repository baselines are Vendor Intelligence
`5fd4a0f28b6d929063d071152cddd41fe2ea6360` (live `AGENTS.local.md` hash
`823659f403566f785b7187a993663cdb9b09340e`; untracked `PLANNING.md` hash
`2be21de427d90f76e362e01bececf422ed81517f`) and Townchest
`052c73b4ba10c246ba58a3c2bc99c4fdff901d58` (live `AGENTS.local.md` hash
`27db2ca643b8d2147316f806aec8908496100d6d`). Re-read and re-hash them at
implementation start; any mismatch is an integration edge to reconcile, not
permission to reset or overwrite.

Operator decision (2026-08-10): the current Vendor Intelligence
`AGENTS.local.md` and `PLANNING.md` contents at the hashes above are the
authorized predecessor baseline. Freeze exactly those two files together as a
separate predecessor before Task A; this decision does not include, stage,
commit, discard, or otherwise absorb any other dirty planning-repository file.

After the predecessor is frozen, add only the ownership clarification needed
for the main planner to maintain shared roadmap/INDEX/umbrella state while
dispatched tasks maintain their own work-item artifact and report results.

### Task A acceptance criteria

- [ ] Every removed normative rule is classified as preserved, relocated to a
      named existing owner, intentionally deleted as duplicate, or deferred for
      an operator decision.
- [ ] Both project startup stacks shrink by at least 30% in bytes.
- [ ] Skill descriptions total no more than 6,000 characters and still route all
      current invocation examples correctly.
- [ ] No repo-specific hard edge listed under Invariants is lost.
- [ ] No new always-loaded document, mode, ledger, template, or mandatory
      artifact is introduced.
- [ ] The workflow and two private planning repositories each have their own
      stated baseline, diff, verification, commit, and rollback point.
- [ ] `plan-next` remains the main planning/coordinating session and fresh Codex
      tasks remain the execution boundary.
- [ ] All modified Markdown paths and skill YAML parse and resolve.

## Task B — reduce procedural ceremony

Begin only after Task A is piloted and its routing is stable.

### B1. Make planning artifacts content-driven

Update `workflow/PLANS.md` and both repo-local plans READMEs so only the living
`README.md` is expected by default. Create `PR_BODY.md`, `verification.md`,
`reviews.md`, or `artifacts/` only when they contain durable content that does
not fit the living spec or concise handoff. Preserve separation when such files
exist.

The main planner owns shared `INDEX.md` and umbrella lifecycle updates while it
is active. Child planning or implementation tasks update only their work-item
folder and return the existing completion handoff with a concise reconciliation
line—no new ledger. Update `workflow/skills/spec/SKILL.md`, `plan-next`, and the
relevant planning kickoff route so a dispatched task can distinguish a named
active main planner from standalone planning. Without a named active planner,
the finishing task performs the existing update so state cannot become
ownerless.

Batch related post-merge INDEX/umbrella cleanup when several lanes are landing,
but do not leave a completed item represented as active indefinitely.

### B2. Simplify coordination edges

Add two concise rules without a new ledger:

- **Review parking:** if reviewer capacity is unavailable, freeze the range and
  complete packet once, report it as ready, and let the coordinating session
  resume it when capacity exists; do not poll or ask unrelated tasks to release
  slots.
- **Integration edge:** unmerged work blocks only when it owns the same active
  behavioral seam or would make the current intermediate result false. Shared
  files or independent hunks are reconciliation work, not automatic blockers.

### B3. Make spec outer review positively risk-triggered

Keep one inner `specreview` for every explicitly requested implementation-ready
formal spec. Keep casual questions, `plan-next` discussion, and fast work out of
formal planning entirely.

Replace the broad “outer review unless every compact condition holds” framing
with a positive selector. Require `outerspecreview` for architecture/product
policy, contract/API/schema, persisted-state/lifecycle/migration, auth/security,
provider/dependency/toolchain, cross-system rollout/cutover, or a material
unproven bet. Otherwise skip it automatically unless the operator requests it.

This changes selection frequency, not the strictness of either review.

### B4. Separate operator summaries from receipts

User-facing completion messages lead with:

1. what changed;
2. why it matters;
3. readiness or blocker;
4. the operator decision, if any.

Keep SHAs, exhaustive counts, review history, and gate-routing evidence in the
local receipt or a collapsed evidence section unless the operator requests it.
The outer-review receipt gains no new mandatory ledger.

### B5. Move launcher mechanics off the shared path

Move `HANDOFF.md`'s Claude model mapping, flags, JSON session handling, resume
commands, and CLI failure behavior into one outer-review-only reference loaded
by `outerreview` and `outerspecreview`. Keep in `HANDOFF.md` only sequencing,
positive gate triggers, independence, re-review reuse, and a route to the
launcher.

### B6. Make review kickoffs context-first

Reduce implementation and external-PR kickoffs to task-specific facts and route
judgment to `REVIEW_RUBRIC.md`. Reduce spec-review kickoff repetition while
retaining its spec-specific checks. Do not remove any investigation duty; remove
only duplicate copies and clean per-item ledgers from visible output.

`prreview` keeps its current lead/challenger/specialist thresholds and
convergence behavior. Only duplicate clean tables and visible audit repetition
are in scope.

### Task B acceptance criteria

- [ ] A compact work item can consist only of a living `README.md`.
- [ ] Shared planning state has exactly one active owner with an ownerless
      fallback.
- [ ] Review-capacity exhaustion produces one parked packet, not polling.
- [ ] Independent overlapping branches can continue without weakening dirty-tree
      or merge-conflict safety.
- [ ] Formal specs always receive the inner review; only named positive risks
      require the outer spec gate.
- [ ] Operator-facing summaries are understandable without reading review
      receipts.
- [ ] Outer-review CLI behavior remains identical after its relocation.
- [ ] No `prreview`, test-quality, or implementation-review discovery duty is
      weakened.

## Deferred work

After at least three representative pilots, audit `TESTING.md` and
`REVIEW_RUBRIC.md` for exact duplication. Any consolidation must prove that the
removed text adds no distinct defect-catching prompt. Do not use line-count
reduction as sufficient evidence, and do not relax severity, candidate admission,
contract propagation, information-loss, fresh-runner CI, or behavior-proof
audits.

The prior planner's proposed broader approval envelope is also deferred. The
current natural-substeps rule remains authoritative. Any future change allowing
adaptive paid/provider retries under one approval changes the safety envelope
and requires a separate operator decision with explicit inputs, caps, provider,
stop rules, and side-effect boundaries.

## Behavioral fixtures

The implementation is not complete until these scenarios produce the expected
route from the written rules:

| Scenario | Expected behavior |
| --- | --- |
| “What are our options?” | serial answer; no automatic `explore` or `spec` |
| one-line copy removal | fast implementation, focused proof, normal inner review; no invented absence test |
| narrow implementation-ready issue | formal spec only when explicitly invoked; inner spec review; outer spec skipped if no positive risk |
| migration/auth/provider plan | formal spec, inner review, required outer spec gate |
| ordinary implementation | targeted loop checks, required affected gates once, one inner review; outer skipped without a named trigger |
| migration/auth/provider implementation | inner convergence then required fresh outer gate |
| coworker PR | current `prreview` discovery and convergence unchanged |
| reviewer slots full | one frozen ready packet; no polling or cross-task interruption |
| two branches touch one doc independently | continue and reconcile after landing unless the same behavior seam conflicts |
| main planner plus child tasks | planner owns shared INDEX/umbrella; each child owns only its work item |

### Task A skill-metadata fixtures

These expectations were frozen before editing discovery metadata. Each changed
description must still select on the positive prompt and reject the named
exclusion after an application reload. `plain` already meets the concise
contract and is unchanged.

| Skill | Positive trigger | Principal exclusion |
| --- | --- | --- |
| `behavior` | “Summarize the behavior of this spec.” | Do not replace `plain`, `learn`, or review. |
| `calibrate-review` | “Calibrate these coworker PR findings.” | Never auto-run after an implementation review. |
| `explore` | “Run a formal explore pass on these architecture options.” | Casual option questions stay serial. |
| `implreview` | “Hand this completed implementation off for review.” | Not spec review or coworker PR review. |
| `implrereview` | “Re-review the patches for the inner findings.” | Outer findings return to their outer reviewer. |
| `learn` | “Brief me on my current PR so I can explain it.” | Not a last-message restatement or design-options pass. |
| `outerreview` | “Run the outer review of my implementation.” | Not coworker PRs or the inner loop. |
| `outerspecreview` | “Run the outer review of this converged spec.” | Not inner spec review, code review, or coworker PRs. |
| `plan-cleanup` | “Archive and externalize completed plans.” | Not ordinary immediate cleanup after one landing. |
| `plan-next` | “Be my main planner and coordinate the next work.” | Main session does not implement or review code. |
| `prreview` | “Review coworker PR #123.” | Not the operator's own implementation handoff. |
| `spec` | “Run a formal implementation-ready spec for VEN-123.” | Pasted issues, status, or casual options do not trigger it. |
| `specreview` | “Run the inner review of this spec.” | Not implementation review. |
| `specrereview` | “Re-review revisions for the inner spec findings.” | Outer spec findings stay with the outer reviewer. |
| `spike` | “Prove this chosen architectural bet at the real boundary.” | Not mapping options or diagnosing a fresh bug. |

### Task A rule-disposition inventory

This inventory records the authority for the substantive detail removed from
the automatically loaded files. No safety or quality rule is intentionally
retired in Task A; only duplicate wording and examples are deleted.

| Removed surface | Disposition |
| --- | --- |
| Kernel test examples and test-selection detail | Preserved in `TESTING.md`; the kernel retains the real-boundary, durable-regression, anti-shape-test fallback. |
| Kernel implementation, planning, and review steps | Preserved in the named skills, `PLANS.md`, `HANDOFF.md`, and `REVIEW_RUBRIC.md`; the kernel retains route selection and floors. |
| Kernel verification examples and handoff mechanics | Preserved in repo verification owners and `HANDOFF.md`; the kernel retains tiers, causal reuse, and consumer-boundary proof. |
| Kernel provider/paid-operation approval detail | Preserved in the kernel: all provider mutations remain gated, with only the named disposable-DB harness exception; paid runs require an exact provider, scope, and cap. |
| Kernel no-contract refactor proof | Preserved compactly in the kernel as status/shape/error/side-effect parity across the changed boundary. |
| Vendor Intelligence workflow-mode list | Deleted as a duplicate of kernel startup routing. |
| Vendor Intelligence umbrella/slice/archive procedure | Relocated to `.agent-workflow/plans/README.md`. |
| Vendor Intelligence Linear body and plan-code procedure | Relocated to `.agent-workflow/PLANNING.md`. |
| Vendor Intelligence docs classification and source-probe procedure | Routed to tracked `docs/README.md` and `docs/workflows/`; tracked `AGENTS.md` retains the probe safety edges. |
| Vendor Intelligence reviewer, command, verification, and migration detail | Routed to tracked `AGENTS.md`, `docs/CODE_MAP.md`, `docs/COMMANDS.md`, and `docs/VERIFICATION.md`; unique disposable-DB, long-lived-DB, Drizzle, runtime, export, and PR-title deltas remain in the local adapter. |
| Townchest generic task, plan, review, and PR-body procedure | Deleted as duplicate or routed to the kernel, `HANDOFF.md`, local plans README, and `reference/pr-body-style.md`. |
| Townchest setup, local-data, migration, provider, CI/deploy, and codegen detail | Routed to tracked `AGENTS.md`, `docs/onboarding/SETUP.md`, `docs/agent-rubrics/domain-risks.md`, `docs/deployment/developer-agent-ops.md`, and `docs/tooling/graphql-schema-strategy.md`; unique local approval, TARS, and server-runtime/preview deltas remain in the adapter. |
| Townchest command catalog, Biome workaround, testing/frontend, and E2E detail | Routed to the section-addressed private verification/testing/coding owners and `FRONTEND.md`; the executable Biome guard plus manual a11y/layout, focus, reduced-motion, visual-baseline, and E2E exceptions remain in the adapter. |

Deferred dispositions: none in Task A.

## Verification plan

### Tier 1 — document and metadata checks

- capture before/after size with `wc -l -w -c <changed instruction files>`;
- parse every skill frontmatter with:

  ```bash
  ruby -e 'require "yaml"; Dir["workflow/skills/*/SKILL.md"].each { |p| t = File.read(p); fm = t[/\A---\n(.*?)\n---/m, 1] or abort("missing frontmatter: #{p}"); y = YAML.safe_load(fm, aliases: false); abort("invalid skill metadata: #{p}") unless y["name"] && y["description"] }'
  ```

- parse every OpenAI skill manifest with:

  ```bash
  ruby -e 'require "yaml"; ARGV.each { |p| YAML.safe_load(File.read(p), aliases: false) }' workflow/skills/*/agents/openai.yaml
  ```

- build an explicit list of every Markdown/path route added or changed and run
  `test -e <resolved-path>` for each one;
- run `git diff --check` and `git status --short --branch` in each modified
  repository;
- inspect every local-adapter deletion against the disposition inventory.

### Tier 2 — scenario routing

Before edits, create an in-spec matrix containing one positive trigger and the
principal exclusion for every skill description that will change, plus the
Behavioral fixtures and representative destructive, paid/provider, migration,
local-DB, codegen, and verification routes from each adapter. State the expected
selected skill/conditional owner and forbidden route in advance.

After edits and an application restart/reload, run each case in a fresh task so
startup and skill metadata cannot be inherited from this planning session. For
each, record which files the agent reads, which skill it selects, whether it
delegates, which review gate it chooses, and whether it pauses. A failure is a
wrong route, not a wording difference. The fixture record may live in the
living spec; do not create a separate ledger.

### Tier 3 — safe pilot

Use the revised harness on three real but non-provider tasks:

1. one fast, localized change;
2. one normal implementation with tests and inner review;
3. one substantive planning task whose risk either clearly selects or clearly
   skips the outer spec gate.

Compare with recent sessions on:

- time to first useful action;
- automatically loaded/read instruction volume;
- number of spawned investigators/reviewers;
- broad verification reruns;
- operator corrections about scope, ceremony, or current project state;
- review findings and any missed regression.

Do not claim success solely from lower token use. The pilot fails if it creates
an authority ambiguity, skips a required gate, weakens a finding, or loses a
repo hard edge.

### Tier 4 — operator assessment

No provider, production, paid-model, destructive, or external-message activity
is required. Promotion does require the operator's manual assessment after the
three already-authorized real tasks. Pass only when the operator confirms that
orientation and iteration are materially faster, scope/ceremony corrections are
lower, and no required safety, verification, or review gate was missed. A mixed
or uncertain result keeps V0 in pilot and does not authorize more project work
solely to manufacture evidence.

## Rollout and rollback

1. Freeze the authorized `plan-next` predecessor separately.
2. In Task A, commit/review the workflow repo, Vendor Intelligence planning repo,
   and Townchest planning repo separately; never use one cross-repo verdict.
3. Preserve the pre-change local-adapter versions in their private nested repos;
   do not overwrite unrelated dirty changes.
4. Pilot Task A before starting Task B.
5. Commit Task B separately from Task A and preserve the same repository
   boundaries.
6. If routing regresses, revert only the failing repository-scoped patch and retain the measured
   inventory so individual safe reductions can be reapplied.
7. Promote V0 only after all behavioral fixtures pass and the operator confirms
   that at least three real sessions feel materially faster without weaker
   outcomes.

## Proposed implementation surfaces

Task A:

- `/Users/ccolosimo/.agents/workflow/AGENTS.md`
- `/Users/ccolosimo/.agents/workflow/skills/*/SKILL.md` frontmatter only
- `/Users/ccolosimo/.agents/workflow/skills/plan-next/SKILL.md`
- `/Users/ccolosimo/vendor-intelligence/.agent-workflow/AGENTS.local.md`
- `/Users/ccolosimo/vendor-intelligence/.agent-workflow/PLANNING.md`
- `/Users/ccolosimo/vendor-intelligence/.agent-workflow/plans/README.md`
- `/Users/ccolosimo/townchest/.agent-workflow/AGENTS.local.md`
- existing local reference owners only when a disposition requires relocation

Task B:

- `/Users/ccolosimo/.agents/workflow/PLANS.md`
- `/Users/ccolosimo/.agents/workflow/HANDOFF.md`
- `/Users/ccolosimo/.agents/workflow/skills/spec/SKILL.md`
- `/Users/ccolosimo/.agents/workflow/skills/plan-next/SKILL.md`
- one new outer-review-only launcher reference
- `/Users/ccolosimo/.agents/workflow/kickoffs/review.md`
- `/Users/ccolosimo/.agents/workflow/kickoffs/spec-review.md`
- `/Users/ccolosimo/.agents/workflow/kickoffs/external-pr-review.md`
- narrowly corresponding handoff/review skill routing
- `/Users/ccolosimo/vendor-intelligence/.agent-workflow/plans/README.md`
- `/Users/ccolosimo/townchest/.agent-workflow/plans/README.md`

Deferred:

- `/Users/ccolosimo/.agents/workflow/TESTING.md`
- `/Users/ccolosimo/.agents/workflow/REVIEW_RUBRIC.md`
- `prreview` discovery/convergence behavior

## Planning decisions

- Domain Pass: not required. This consolidates existing workflow vocabulary and
  does not introduce a new product or lifecycle term.
- Dirty-baseline decision: resolved. The operator authorized the exact current
  Vendor Intelligence `AGENTS.local.md` + `PLANNING.md` pair as a separate
  predecessor and no other dirty planning-repository work.
- Slicing: two ordered phases, each split into independently reversible
  repository-scoped patches. Task A leaves a valid faster harness while all
  existing on-demand ceremonies still work. Task B can land later or never land
  without invalidating Task A.
- Proposed implementation branch: `workflow-harness-consolidation-v0`.
- No tracker issue or public artifact is required unless the operator later
  chooses to create one.
