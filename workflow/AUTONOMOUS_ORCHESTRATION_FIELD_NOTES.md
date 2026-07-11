---
title: Autonomous Orchestration Field Notes
status: reference
created: 2026-07-09
updated: 2026-07-10
owner: operator
related:
  - AGENTS.md
  - HANDOFF.md
  - COMMAND_GUARDRAILS_AND_VERIFICATION_HOOKS.md
  - ORCHESTRATOR_MODE.md
---

# Autonomous Orchestration Field Notes

Living observations from the first program in which a planning agent was given
broad authority to plan, dispatch implementation tasks, coordinate reviews, and
prepare integration with minimal operator input. This is evidence and a design
scratchpad, not workflow policy. Update it at execution milestones and after the
final delivery result is known.

## Experiment Snapshot

Program: Vendor Intelligence source/category expansion, Wave A.

Authority envelope established in conversation:

- The orchestrator may research, write/review specs, launch Terra xhigh tasks,
  allow implementation commits on a dedicated branch, run offline/localhost
  verification, and coordinate inner review loops.
- Residential proxy, Web Unblocker, provider/browser traffic, OpenRouter/paid
  repository stages, Pets collection, push, and PR creation remain separately
  approval-gated or forbidden.
- Multiple implementers may collaborate toward one expansion PR.

Current evidence, before integration is complete:

- An umbrella, deduplicated source ledger, and reviewed child specs were produced.
- A generic runner first commit spans 21 files and about 4,000 inserted lines.
  Its inner reviewer found a real private-host policy bypass involving
  IPv4-mapped IPv6. The patch passes 11/11 focused tests and awaits re-review.
- The Michaels parser slice is edit-complete but deliberately unstaged while the
  runner's commit/review window finishes.
- No live/paid traffic, Pets collection, push, or PR action has occurred.

## What Is Working Well

1. **The safety envelope is holding.** Repeating the live/paid prohibitions in
   task assignments, keeping a central safety ledger, and making the coordinator
   own localhost checks prevented a blocked test from turning into accidental
   provider traffic.
2. **Spec review is earning its cost.** Re-review cycles forced exact decisions
   about URL synthesis, fanout, access tiers, pagination posture, and factual
   versus human-owned conclusions. Implementation started from substantially
   clearer contracts than the original exploration notes.
3. **Implementation review found a non-obvious defect.** The runner's reviewer
   caught an IPv4-mapped IPv6 escape in an otherwise well-tested host policy.
   That is strong evidence for retaining the mandatory inner loop.
4. **Explicit file ownership works.** Named edit tokens and serialized
   stage/commit windows have so far prevented two agents in one worktree from
   overwriting or committing each other's files.
5. **The integration record is useful.** One local ledger containing branch,
   task IDs, ownership, verification, review state, and safety constraints makes
   recovery and operator status reporting much easier.
6. **Operator decisions have stayed directional.** The operator chose policy and
   authority boundaries; agents handled spec corrections, routine patches, and
   review iteration autonomously.

## Snags And Friction

1. **“Full access” did not mean “no approval interruptions.”** A runner task
   stalled on a Codex approval prompt for localhost/IPC work. Other tasks could
   not bind localhost or write the shared Git index from their sandbox. Computer
   control could not clear a Codex prompt inside Codex. A recovery task and a
   coordinator-owned verification lane were needed. Global Codex defaults were
   later changed for new sessions, but mechanical destructive-command enforcement
   remains future work.
2. **A shared worktree is possible, but expensive to coordinate.** It avoids
   cherry-picks and supports one PR, yet there is one Git index, unrelated dirty
   files affect broad checks, reviewers can observe another slice's unstaged
   work, and commits must be serialized. Disjoint worktrees/branches feeding one
   integration branch may be the safer default for more than one writer.
3. **Role bootstrap was awkward.** Forked tasks inherited coordinator history and
   then needed a second, role-specific execution kickoff. Thread previews can
   therefore describe a coordinator even when the task is an implementer. A
   purpose-built orchestration assignment should establish role, base, ownership,
   permissions, and stop condition in one unambiguous handoff.
4. **Kickoffs are thorough but very long.** The canonical execution template plus
   slice-specific safety, ownership, dependency, and verification clauses can bury
   the few facts an implementer must not miss. Stable kernel rules should remain
   canonical, while an orchestration assignment block should make the delta easy
   to scan and validate.
5. **Review workers need bounded failure handling and inherited safety rules.**
   The runner reviewer spent a long interval in a blocked command/wait and had to
   be interrupted and resumed. During narrow re-review it again requested an
   elevated test even though the coordinator had supplied the exact green
   evidence. The parent task's no-escalation instruction did not reliably flow to
   its spawned/reused reviewer. The review still produced a valuable finding, but
   reviewer kickoffs should explicitly inherit the authority envelope, set
   command/time ceilings, prohibit redundant escalation, and prefer
   coordinator-supplied verification evidence when execution is not essential.
6. **Slice and integration acceptance became entangled.** Michaels could not run
   its full focused suite before the integration-owned category config existed.
   Future task graphs should distinguish slice-local proof from integration proof,
   and either land prerequisites first or provide an explicit fixture/config
   injection seam.
7. **The generic runner may be too large for one “PR-sized” task.** It combines
   schemas, policy, transport, extractors, artifact writing, CLI, docs, and tests.
   The integrated safety contract argues for cohesion, but the size increased
   implementation and review latency. Final results should determine whether it
   should have been split behind a stable internal contract.
8. **Operator visibility is still conversational.** Status can be reconstructed,
   but there is no standard compact program dashboard or heartbeat format. The
   operator should not need to open several tasks to learn state, spend, blockers,
   and the next approval gate.
9. **The parent treated conversational completion as program pause.** After
   answering status or documentation requests, the orchestrator yielded instead
   of immediately advancing the next safe dependency. No technical or operator
   gate required those pauses. In an autonomous program, an informational user
   message should be treated as an addition to the running goal unless it clearly
   overrides or pauses it. Status belongs in commentary; a final handoff should
   normally coincide with a real operator gate, blocker, or completed program.

## Hypothesis: Add An Orchestrator Mode

This hypothesis has now been extracted into `ORCHESTRATOR_MODE.md` as a rough
kernel-mode design. That draft is not policy; this file remains the evidence log
used to test and refine it.

Planning and orchestration appear to be different jobs.

- A **planning agent** researches one work item and produces a converged spec.
- An **orchestrating agent** owns the control plane for a multi-task program:
  authority envelope, dependency graph, task assignment, file/worktree leases,
  verification ownership, review convergence, recovery, integration readiness,
  operator status, and the retrospective.

The orchestrator should not normally implement a child slice. It may run neutral
coordinator checks and maintain planning/control artifacts, preserving separation
between implementation and review. It must stop at operator-owned direction,
live/paid/destructive actions, and the final outer/PR gates required by policy.

A future `/orchestrate` workflow could use this lifecycle:

1. Lock the goal, authority envelope, spend/traffic policy, delivery shape, and
   stop conditions.
2. Build the dependency graph and Definition-of-Ready check for each child spec.
3. Choose isolation strategy: separate worktrees by default; shared worktree only
   with disjoint ownership and serialized index leases.
4. Dispatch a structured assignment containing role, base SHA, owned paths,
   forbidden paths/actions, verification owner, commit window, and terminal report.
5. Maintain one machine-readable task/evidence/safety ledger and one compact
   operator-facing status view.
6. Converge inner reviews, freeze child tips, integrate, run branch-level gates,
   and prepare the operator-owned outer/PR decision.
7. Update this retrospective and clean/archive the program artifacts on landing.

## External Prompt Pattern: “One End-To-End Goal”

On 2026-07-09 the operator supplied a public prompt describing a lighter-weight
version of this experiment: give an agent one complete goal, require it to split
independent parts among parallel agents, attach deliverables/verification/done
criteria, actively schedule and reconcile the work, verify the real path, and
persist until done or genuinely blocked.

The useful core is an **outcome mandate**:

- treat the supplied plan as one program, not a sequence of disconnected chats;
- decompose only where work is independently executable and verifiable;
- give every worker a concrete result, proof method, and terminal condition;
- make the parent synthesize, resolve conflicts, and keep the critical path moving;
- require real-boundary proof where it represents the product's actual behavior;
- stop only for a named blocker, not ordinary implementation friction.

The kernel needs to qualify several phrases from the lighter prompt:

- “As many agents as it takes” becomes bounded concurrency plus explicit file,
  worktree, commit, and provider leases.
- “Verify live after every important step” becomes tiered, proportional proof.
  Live/provider/browser/hardware validation runs only when it is the meaningful
  boundary **and** its environment and per-action approval are present.
- “Whatever it takes” never expands authority or bypasses privacy, credentials,
  destructive-action, data-handling, or review policy.
- “Commit when ready” permits ordinary scoped commits inside the approved branch
  envelope; push, PR, deployment, and other external mutations remain separate.
- “Take it to done” includes mandatory inner review, required outer gates, docs
  impact, verification routing, and honest blockers—not merely code completion.

### Candidate Initial Orchestrator Prompt Shape

The eventual kickoff should combine three layers: outcome mandate, authority
envelope, and control protocol. A concise rough shape is:

```text
Run <goal/spec> as one end-to-end program. Carry planning, implementation,
verification, review, integration, and handoff to the furthest authorized done
state; do not stop for routine friction.

Authority envelope
- May: <read/write/commit/task-launch/offline-verification actions>.
- Must ask: <live, paid, destructive, external, outer/PR gates>.
- Forbidden: <credentials/state/bypass/data/provider constraints>.
- Delivery shape: <one PR, target branch, integration owner>.
- Concurrency/cost ceilings: <limits>.

Orchestrate
1. Validate the plan and surface decision blockers before execution.
2. Build the dependency graph; split only independently reviewable work.
3. Give each task: goal, base/input, owned paths, non-goals, deliverable,
   verification boundary, done criteria, dependencies, and approval limits.
4. Schedule within the concurrency ceiling; maintain leases and one state ledger.
5. Recover stalled tasks without duplicating writers or invalidating reviews.
6. Converge each inner review, freeze child tips, integrate, and run branch gates.
7. Stop only at an authority/credential/conflict blocker or the next operator gate.

Status contract
- Report: completed, in flight, blocked/decision needed, safety/spend, next gate.
- Never claim a gate passed unless it ran on the current range.

Done
- Acceptance criteria met; meaningful tests and real-boundary proof complete or
  explicitly operator-gated; docs aligned; review policy satisfied; integration
  clean; final summary and remaining approvals prepared.
```

This should be a small orchestration kickoff or skill layered over the existing
kernel, not a replacement for planning, execution, or review templates.

## More Control Versus Less Detail

Add more explicit control around:

- the initial authority envelope and approval ledger;
- task dependencies, ownership leases, and commit windows;
- worktree/branch isolation and recovery after a stalled task;
- spend/traffic counters with an always-visible zero/nonzero state;
- slice-local versus integration-level verification;
- outer-review ownership and final delivery gates;
- task timeouts, heartbeat cadence, and escalation behavior.
- persistence semantics: answer informational interruptions, then resume the
  critical path without waiting for another “continue” message.

Reduce or automate:

- repeated prose copies of stable kernel rules in every handoff;
- low-value progress narration from child tasks;
- operator involvement in autonomous spec/re-review patch loops;
- manual reconstruction of status from several task histories;
- repeated safe-command approval prompts.

## Measurements To Keep

At each checkpoint record:

- specs produced, review cycles, and operator decisions required;
- tasks launched, recovered, interrupted, or superseded;
- diff/commit size and time waiting for shared commit windows;
- verification commands, coordinator-only checks, and blocked commands;
- review findings, severity, rework, and false positives;
- live/paid/destructive attempts and actual spend/traffic;
- operator interruptions and whether each was genuinely directional;
- final PR review outcome, integration defects, and delivery time.

## Update Checkpoints

- [x] Runner inner review converged.
- [x] Michaels config plus localhost integration proof completed.
- [x] Whole Wave A offline verification completed on refreshed current-main tip;
      replacement holistic inner review is in flight.
- [ ] Required outer review completed.
- [ ] PR handoff/merge outcome known.
- [ ] Final conclusions promoted into workflow changes or explicitly rejected.

## Update Log

### 2026-07-09 — Initial mid-execution note

The experiment currently supports continuing autonomous orchestration. The
strongest evidence is the preserved safety boundary and the substantive review
finding. The largest operational weaknesses are permission-model surprises,
shared-worktree coordination cost, oversized handoffs, and the absence of a
first-class orchestrator state model. Delivery quality and total rework are not
yet known, so all structural recommendations remain provisional.

### 2026-07-09 — Runner inner-loop convergence

The initial runner review returned one high-severity finding; the patch passed
11/11 coordinator-run tests and the original reviewer approved it on re-review.
The task could edit files but could not stage them in the shared worktree, so the
orchestrator had to take a narrowly scoped index/commit window. During re-review,
the reviewer again requested elevated execution despite supplied evidence; the
parent interrupted only that tool call and resumed the same reviewer read-only.

Provisional lesson: orchestration assignments need capabilities declared per
role, not assumed from the parent task. Edit, Git-index, localhost, network, and
review-execution rights are distinct. Nested reviewers must inherit the authority
envelope explicitly, and the coordinator needs a standard narrow-commit recovery
procedure that preserves concurrent dirty work.

### 2026-07-09 — External end-to-end prompt comparison

The public prompt is directionally strong but underspecified for a controlled
engineering environment. Its best contribution is the explicit end-to-end
outcome mandate and parent responsibility for scheduling/synthesis. The kernel's
contribution is to make “parallel,” “live,” “done,” and “blocked” precise and
safe. A future orchestrator mode should preserve the public prompt's momentum
while supplying the authority and evidence control plane it omits.

### 2026-07-09 — Operator identified avoidable pauses

The operator correctly observed that the program kept stopping even when no
approval or decision was needed. The cause was the parent orchestrator yielding
after discrete status/documentation responses, not an inability to drive tasks.
The immediate correction is to keep the turn/program active, use commentary for
updates, and dispatch the next authorized dependency automatically. This should
become an explicit orchestrator-mode contract and a measurable failure condition.

### 2026-07-09 — Broad-category correction and truth reconciliation

The initial source brief named both the original broad consumer portfolio and a
newer set of gap categories. The planning artifacts over-weighted the most
concrete gap list (School, Books, Arts, Kids' Clothing) until the operator
clarified that Toys & Games, Beauty/Personal Care, and Sports & Outdoors are the
portfolio-leading lanes. Pets remains historically covered but collection-
skipped.

The correction exposed a useful orchestration rule: a detailed list of gaps must
not silently become the program's strategic ordering when a higher-level
portfolio objective exists. The orchestrator should maintain separate fields for
`primary portfolio families`, `secondary gap-fill families`, and `explicit
exclusions`, then check every child queue and approval register against them.
Here that audit found stale Faire approvals, a duplicate Toys classification,
and child-spec sequencing that had drifted toward apparel/paid-access work.

### 2026-07-09 — Wave A integration and environment-shaped verification

The Michaels inner loop returned four medium findings: one shared-verifier
regression and three missing behavior proofs. A finding-scoped patch restored
the shared contract, added default-strict/Pets-negative verification, pinned the
exact source config, and covered field/URL fallbacks. The original reviewer then
approved the patch. The integrated branch now contains five commits and the
source-truth layer reconciles Michaels, Toy Fair aliases/MYS implementation,
Ulta marketplace mode, seven Faire Beauty configs, and the no-Pets decision.

`scraper:test` passed 519/519 immediately. The first full `verify` attempts
failed because a Codex worktree does not automatically inherit the main
checkout's gitignored dashboard dependencies or evidence bundle. Missing
dependencies caused module-resolution noise; supplying dependencies alone then
caused the dashboard import to fall back to a tiny committed sample, producing
unrepresentative generated types. The final gate passed by temporarily linking
the worktree to the already-installed dashboard dependencies and the existing
read-only local evidence bundle; both links were removed automatically. Final
proof: 519 scraper tests + 70 dashboard tests, typechecks, Biome, and contract
checks all passed.

Provisional workflow improvement: implementation worktree creation should have a
documented, non-installing bootstrap for ignored dependency trees and read-only
evidence inputs. Verification records should distinguish a source failure from a
missing-worktree-input failure, and generated-data gates should name whether they
require the representative local bundle or intentionally exercise fallback
sample mode.

### 2026-07-10 — Resume, stale-review recovery, and current-main refresh

On resume, the orchestrator merged current `main` (through PR #96) into the
shared Wave A branch and reran the exact offline gate. The refreshed tip passed
520 scraper tests and 70 dashboard tests, both typechecks, Biome, and the contract
check. PR #96 removed the need for the earlier temporary evidence-bundle link;
only the already-installed dashboard dependency tree was linked for the gate and
then removed. No live, paid, provider, browser, OpenRouter, or Pets traffic ran.

The interrupted holistic reviewer remained visible by task ID and retained useful
partial reasoning, but the multi-agent runtime no longer registered it as a live
agent and the app rejected a direct follow-up to that subagent. This is a concrete
resume-semantics snag: a visible task record is not necessarily resumable. The
recovery used one explicitly named fresh Terra xhigh Codex task with the canonical
review kickoff, exact refreshed range, prior partial concern as a claim to
re-derive, and a read-only/offline authority envelope.

Provisional workflow improvements:

- Persist an explicit `resumable | record-only | superseded` state for every
  worker/reviewer rather than inferring it from task visibility.
- Store the canonical kickoff, base/tip, verification evidence, and pending
  findings in the orchestration ledger so a replacement can be launched without
  reconstructing context from chat history.
- Define a standard reviewer-replacement rule for operator interruptions: try
  exact-session reuse once; if the host rejects it, launch exactly one fresh
  reviewer, disclose the replacement, and invalidate any partial approval.
- Refresh the branch onto current target and rerun the gate before review; a
  pre-pause verdict or verification record cannot certify a post-resume tip.

### 2026-07-10 — Review specificity prevented a false fixture claim

The Toy Fair spec initially described its planned proof too broadly as an
offline fixture proof. Spec review correctly separated three boundaries: a
Toy-Fair-shaped normalization seam, an ABC-shaped full collector/artifact test,
and generic MYS pagination coverage. Re-review also caught a filesystem path
mistaken for a runtime `raw://` pointer and a suffix-only profile assertion that
could accept the wrong tenant origin.

Provisional lesson: child specs should name the exact boundary being proven and
pin tenant identity with complete URLs/pointers, not suffixes or broad “fixture-
proven” labels. Review loops are adding concrete value before implementation;
their best findings have been contract-identity mistakes, not style nits.

### 2026-07-10 — Holistic review caught cross-slice risks child review missed

Both Wave A children had converged inner reviews, and the refreshed full gate
passed, but the whole-branch reviewer still found two substantive integration
issues: a proxy-DNS/trailing-dot SSRF gap in the generic runner and a durable
Michaels report that preserved superseded URL-derivation/fanout guidance beside
the implemented explicit-only contract. Green tests and slice approvals were
therefore necessary but not sufficient.

The security finding is especially instructive. Literal IP and mapped-IPv6
guards did not cover the real resolver boundary because `got-scraping`'s proxy
agents send hostnames to the proxy. A correct patch has to bind each hop to a
validated public address before proxy dispatch while preserving Host/SNI, and it
needs injected-resolution tests for initial URLs and redirects. A cosmetic local
hostname check would have created false confidence.

Provisional lesson: retain the holistic branch review even when all child loops
converge. Its explicit job should include cross-slice authority consistency and
adversarial checks at the actual transport/provider boundary. The orchestrator
should budget time for at least one branch-level patch/re-review cycle on new
security or integration machinery.

### 2026-07-10 — Coordinator-owned verification and Git recovery repeated

The holistic security patch needed localhost proxy fixtures that the worker's
sandbox could not bind, and the worker again could not create the shared
worktree's Git index lock. The orchestrator ran the exact loopback-only suite,
returned the 15/15 evidence, then staged and committed only the six declared
runner files. The Michaels report remained unstaged until its separate commit.
This preserved ownership without treating a task-level sandbox limitation as an
operator decision or a program stop.

The exact-tip full gate initially failed because `dashboard/node_modules` was
absent from the Codex worktree. A temporary untracked symlink to the existing
main-checkout dependency tree restored the already-proven environment; the gate
then passed 524 scraper and 70 dashboard tests and the link was removed. No
dependency install or network/provider action occurred.

Provisional lessons:

- The orchestration ledger should declare which role owns localhost fixtures,
  Git-index writes, and environment bootstrap before work starts.
- A blocked worker should emit a machine-readable handoff containing owned
  paths, exact failed command, checks completed, and checks delegated to the
  coordinator. The parent should continue automatically when the operation is
  already authorized.
- Worktree bootstrap should be a first-class offline step, not rediscovered at
  the final gate. Prefer a repo command that links or validates existing ignored
  dependencies and representative read-only inputs, with cleanup recorded.
- Separate commits for disjoint review findings made the same-reviewer re-review
  easier to audit and kept shared-worktree contamination visible.

### 2026-07-10 — Worktree readiness belongs in the kickoff

The operator observed another agent reporting that typecheck could not run
because `tsc` was unavailable. In the Wave A worktree, bare-tool availability and
repo-command availability were different facts: `corepack pnpm exec tsc
--version` succeeded, while the dashboard workspace still lacked its ignored
`node_modules` tree. The first full gate therefore produced hundreds of
module-resolution/JSX errors that looked like product defects but were entirely
environment-shaped.

This should move from recovery knowledge into the kickoff contract. The
coordinator should prepare and attest the worktree before workers edit; workers
should use repo-owned commands, run one doctor check, and treat missing tools or
inputs as a handoff—not as permission to skip verification. The concise proposed
contract is recorded in `WORKTREE_ENVIRONMENT_BOOTSTRAP.md` for a later agent to
turn into the full cross-repo design.

### 2026-07-10 — Independent outer review justified its cost

After the child loops and holistic inner re-review were approved, the fresh
different-model outer gate still found two concrete runner edge cases: native
IPv6 special-use ranges were not comprehensively rejected, and a valid
64-character source ID truncated away all default run-ID timestamp/entropy. The
reviewer's in-process falsification reproduced both without external traffic.

The same outer task also reproduced the worktree-readiness failure: the scraper
and focused gates passed, while full verification stopped at dashboard typecheck
because `dashboard/node_modules` was absent. It correctly separated this from
product correctness and kept the checkout clean.

Provisional lesson: the two-lens gate is materially useful for security/new
infrastructure, but its environment should be prepared before launch. A fresh
outer lens should receive the same readiness manifest as implementers while
remaining independent of prior findings.

### 2026-07-10 — Worktrees paused as a default execution mode

The operator's review of several independently created worktree sessions showed
that dependency, tool-resolution, and verification parity are not yet seamless
or consistent. Wave A itself needed coordinator intervention for a missing
dashboard dependency tree, localhost fixture ownership, and Git-index writes.
Those recoveries preserved correctness, but they are too easy for a worker to
misread as optional verification or a product defect.

Operator direction: finish Wave A's current review cycle, then pause this
orchestration lane. Subsequent active work items should be brought to the
prepared main checkout and completed one implementer at a time. Parallel
worktrees should not become the default again until a dedicated exploration and
testing program proves bootstrap, doctor, verification, cleanup, and handoff
behavior across representative work-item shapes.

Provisional lesson: concurrency is a throughput optimization after environment
parity, not before it. The orchestrator should prefer a slower serialized mode
when it produces stronger verification confidence and less coordinator repair.

### 2026-07-10 — Readiness must preserve a clean review candidate

The first dependency bridge linked `dashboard/node_modules` as one symlink. It
made verification work, but Git reported the symlink itself as untracked because
the ignore rule matched a directory, not that symlink. That conflicts with the
outer review's clean-tree preflight. The corrected bridge creates the ignored
directory and places read-only top-level dependency symlinks inside it; Git stays
clean and dashboard typecheck passes. Cleanup remains coordinator-owned.

This detail belongs in any future `worktree:prepare` implementation: readiness
is not complete unless the environment works *and* the candidate remains clean
under the exact reviewer preflight command.

### 2026-07-10 — “Comprehensive” security rules need an external oracle

The first native-IPv6 fix correctly moved from a deny-fragment list to a
global-unicast decision, but the re-review showed that `2000::/3` alone still
included IANA-reserved `3f00`/`3ffe` space. The second patch consolidated the
reserved/documentation block as `3f00::/8` and added literal plus resolver-answer
regressions.

Provisional lesson: when a security boundary claims exhaustive address/range
coverage, the kickoff should name the authoritative registry or classification
oracle and require representative tests for each exception class. “More
complete” is not the same contract as “complete,” and a focused reviewer should
try at least one valid public address plus reserved values both inside and
outside the obvious prefix families.

### 2026-07-10 — The final worktree pass ended with a serial handoff

The operator designated one last fresh outer pass, then paused orchestration.
That reviewer found two high edge cases after the coordinator's exact-tip full
gate and holistic approval: redirected relative evidence used the original URL
as its document base, and Michaels accepted credential-bearing URL userinfo.
The findings were recorded but deliberately not routed into another patch or
review loop.

The prepared worktree passed both focused suites, but its full gate later hit a
fixed five-second timeout in an unchanged import-contract test after 526/527
scraper tests. A focused retry timed out at the same boundary. This did not
invalidate the earlier exact-tip 527-scraper/70-dashboard coordinator gate, but
it reinforced the operator's concern: even a clean, dependency-ready worktree
can produce environment-sensitive verification results that require
coordinator interpretation.

Provisional lesson: an orchestrator needs an explicit stopping contract as well
as an autonomy contract. When the operator names the last pass, preserve its
findings, exact range, verification split, and cleanup state, but do not
reflexively continue the normal patch/re-review loop. Until worktree parity is
proven, resume active items one at a time in the prepared main checkout.

### 2026-07-10 — Serializing a shared plan requires contract rewrites

While the prepared root remained occupied, the expansion queue could still be
made safer. The old Wave B children assumed one shared branch, a separate
integrator, and one coordinated final Channel Map row count. Those assumptions
became invalid when the operator changed delivery to one prepared-root item at a
time. Beauty and Sports would otherwise both add one CSV row while hard-coding
the same final count.

The serial rewrite gives every item complete test/docs/CSV ownership and makes
its count proof relative to the live merge base. It also exposed a review-state
contradiction: the Sports `reviews.md` says no review while the roadmap called
it ACTIONABLE. The safer disposition is unreviewed until evidence is recovered,
not silently choosing the more advanced status.

Provisional lesson: changing orchestration topology is a spec change, not just a
scheduling change. Recheck ownership, cross-item counts, branch names, review
provenance, and landing-order assumptions before reusing prior specs.

### 2026-07-10 — Orchestrator V0 Phase 2 deterministic core

After independent spec review converged, the operator approved a noncanonical V0
implementation and bounded desktop-task pilot. The chosen topology is fresh
user-visible Codex desktop tasks rather than subagents, with one implementation
writer and explicit model/reasoning selection on task creation.

The staged core now uses a hash-chained event log, OS writer lock, predecessor
CAS, coordinator/assignment/model-policy generations, consumable approvals,
exclusive writer leases, stale-view rebuilding, exact-tip review invalidation,
durable pre-create dispatch intents, and compact status rendering. Thirteen
CLI-boundary behavioral tests pass. A
deterministic same-scenario baseline comparison records zero orchestrated
avoidable pauses versus one baseline pause, without authority violations or
false-green evidence.

Model routing uses portable `fast`, `balanced`, and `deep` classes mapped to the
host's Luna, Terra, and Sol IDs. Luna normally uses medium/high, Terra normally
uses high with xhigh reserved for justified complexity, and Sol normally uses
medium/high. Sol and Terra cap at xhigh;
xhigh is evidence-triggered rather than a default.

The real desktop-task host pilot then confirmed that the app can create distinct
tasks with explicit model and reasoning selections, read their results, continue
the exact reviewer task with a new model/reasoning override, and archive both
tasks. It exercised Terra-medium research, Sol-high review, exceptional
Sol-xhigh adversarial analysis, and a targeted Sol-high re-review. An
informational operator question did not pause the active program.

The adversarial pass found that predecessor CAS cannot promise exactly-once host
task creation when a coordinator crashes after the host accepts create but
before the returned task ID is recorded. V0 now records a durable intent and
stable idempotency key before create, reconciles unresolved intent against host
history, and blocks a blind retry. The same reviewer task approved that patch.

The implementation review remains outstanding at this checkpoint. No mode
activation, active skill install, worktree parallelism, commit, push, provider
action, or paid repository stage has occurred.

### 2026-07-10 — Stronger affordable-route bias and operation-level remediation

The operator raised the reasoning floor for the affordable routes. Luna now uses
medium for simple deterministic work and high for multi-step mechanical work;
Terra uses high as its normal routine-engineering default and xhigh only when
complexity or convergence evidence justifies it. Sol remains medium/high with
xhigh exceptional. Complexity still selects the class; affordability changes the
within-class reasoning bias, not the authority boundary.

Implementation review also showed that a valid-looking record is not proof that
the underlying operation occurred. Remediation moved the pilot from expected
trace insertion to real task, assignment, fencing, recovery, invalidation, model
escalation, and operator-gate transitions. Host evidence now requires exact and
unique operation/event reconciliation plus terminal task and archived-handle
state.

The implementation review loop ultimately converged to `APPROVED` with
Test-quality `PASS`. Thirteen behavioral tests pass. The current host artifact
contains ten exact, one-to-one desktop-operation reconciliation records; both
route overrides are preceded by assignment fencing. The deterministic pilot ends
with terminal child tasks, a released writer lease, a stale superseded review, an
inner-approved candidate in `awaiting_outer`, and the activation approval still
`requested`. Orchestrator Mode and the skill remain inactive pending the
operator-owned outer gate and explicit activation approval.

### 2026-07-10 — Outer review exposed certification-shaped false greens

The first operator-owned outer implementation review was run in a clean detached
worktree at committed tip `71be615`. It returned `ACTIONABLE` despite the inner
loop's approval. Adversarial probes showed four load-bearing gaps: a fenced
assignment could reacquire a writer lease; review identity was not bound to a
distinct reconciled reviewer assignment; candidate verification IDs were not
validated against current exact-tip evidence; and an altered `status.md` still
reported `CURRENT`.

The remediation binds leases to current unfenced assignments, declared owned
paths, heartbeat, and expiry; binds review records to distinct worker/reviewer
tasks and reconciled task handles; requires separate inner/outer roles and
identities; requires the reviewed task's exact declared verification-command
set with current assignment/environment/topology/tip evidence; applies explicit
and topology invalidations; and compares every derived view against replayed
state. The repair suite now contains seventeen behavioral tests, including
fenced lease acquisition, self-review/duplicate outer identity, missing and
wrong-tip verification, topology invalidation, and `status.md` corruption.

Provisional lesson: an event log can be internally consistent while still
certifying the wrong authority relationship. Recovery, review independence, and
candidate promotion need adversarial tests that attempt to reuse plausible but
stale or self-authored evidence—not just happy-path replay tests.
