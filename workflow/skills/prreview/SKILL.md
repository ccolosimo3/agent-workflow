---
name: prreview
description: Review someone else's PR end to end through a proportionate,
  internally convergent process. Freeze and map the PR; review compact changes
  directly; for standard or large changes, run one blind challenger and reconcile
  evidence until material conclusions stabilize; emit a non-blocking progress
  update; then calibrate one final operator action brief. Large reviews may use up
  to two additional bounded specialists. Use when the operator says /prreview,
  asks to review a numbered coworker PR, or steers an active review with zoom out,
  drill into, shift, or challenge. Do not use for the operator's own implementation
  handoff — that is implreview.
---

# prreview

Run a coworker's PR review in this conversation: strict discovery first, then a
calibrated operator-facing result. The invoking task is already the lead reviewer;
do not spawn another agent merely for fresh context.

Read and apply these canonical owners without inlining or paraphrasing them into
prompts:

- `~/.agents/workflow/kickoffs/external-pr-review.md` — framing context;
- `~/.agents/workflow/REVIEW_RUBRIC.md` — strict discovery and evidence rules;
- `~/.agents/workflow/skills/calibrate-review/SKILL.md` — final action semantics.

Invoking this skill counts as the operator's explicit request for coworker-facing
calibration.

## Process

### 1. Preflight, freeze, and map

1. Run `git status --short --branch`; record the current branch and commit. Use the
   existing repo-root checkout by default when it is clean and available. Do not
   create a review worktree merely for isolation.
2. Gather read-only PR metadata and checks with `gh`, but do not read the content of
   existing automated or human review comments yet. Read the linked issue for the
   raw ask and acceptance criteria. Inspect automated-reviewer configuration and
   path exclusions now.
3. Fetch the target and PR refs. Freeze the exact merge-base SHA and `headRefOid`;
   use that range for every lead, challenger, and specialist trace.
4. Check out the exact frozen PR head in the existing repo-root checkout. Use a
   dedicated worktree only when the root is dirty, known to be occupied by another
   task, switching would disturb active work, or required verification needs
   dependency/tool state incompatible with the root. Never stash, reset, or clean
   user work to make the root available. Confirm `HEAD` equals the frozen
   `headRefOid` before local exploration or verification; do not merge or pull the
   PR into the current base branch.
5. Map the behavior/system flow before -> after, material risk surfaces, affected
   tests and verification routes, and shared producer/consumer, schema, state,
   transaction, deployment, and rollout seams.

Choose a profile by risk and cohesion, then record one-line evidence in the kickoff:

- **Compact/cohesive:** use only when all are true: one narrow behavior in one
  subsystem; no added/changed auth, permission, migration, persistence/data,
  public/external contract, concurrency/lifecycle/state, cross-package/service,
  deployment-topology, or shared test/build boundary; one focused check can
  falsify the change; and no material unknown remains after mapping. A repair to
  one existing CI/deployment job may qualify only when it restores one established
  prerequisite/order without changing triggers, permissions, secrets/environment,
  artifacts/outputs, cross-job flow, or deployment targets. Review directly with
  no subagent or progress checkpoint.
- **Standard:** every non-compact review that is not large. Use one blind
  challenger.
- **Large/heterogeneous:** when the map identifies at least two independent
  material risk surfaces or subsystems requiring different proof, select large
  unless one trace can cover both and record why. Use one blind challenger and at
  most two additional bounded specialists; total subagents never exceed three.

If compact eligibility is uncertain, select standard. File count alone selects
nothing. Profiles change process, never the strict review floor.

6. Populate `kickoffs/external-pr-review.md` as internal working context, verbatim
   with placeholders filled from the frozen checkout, map, and selected profile.
   Do not print it or give it to the challenger/specialists.

### 2. Blind discovery

The lead applies `REVIEW_RUBRIC.md` in full, opens every changed file plus enough
surrounding code, owns every cross-surface seam, and delays classification until
discovery and reconciliation complete.

For standard and large reviews, spawn exactly one fresh-context challenger after
freezing the range and deriving the raw ask, but before exposing the lead's map,
candidates, clean conclusions, or prior comments. The lead continues independently
while the challenger scans the complete diff, chooses its own highest-risk
hypotheses, and deeply traces likely failure paths.

Give the challenger only the absolute checkout path, frozen base/tip SHAs, raw ask
and ACs, repo-guidance and rubric paths, any explicitly assigned isolated command
(normally none), and this return contract:

```text
Independent risk map:
Highest-risk hypotheses and paths traced:
Candidate evidence: scenario/input | PR relevance | consequence/authority |
supporting and counterevidence | narrow check/result
Important claims still needing proof:
Verified-clean observations:
Residual checks:
```

The challenger uses the rubric as its discovery standard but does not reproduce
the Output contract, issue a verdict/severity, read prior comments, use `gh`,
switch branches, mutate dependencies/services, or run broad gates. An unassigned
challenger/specialist performs read-only traces only; every command has one lead-
assigned owner, and an unassigned check is reported as not run.

On a large review, add a specialist only for a bounded material question that can
be answered independently and owns neither a shared seam nor broad gate. Give it
the frozen range, raw ask/AC, one question and evidence paths, applicable rules,
and any isolated command. Require the same evidence fields as above. The lead
alone owns `gh`, checkout/restore, services/dependencies, broad verification,
candidate validation, shared seams, and the final result. Every command has one
owner.

### 3. Internal evidence loop

After the blind passes, build one working set containing all candidates, material
clean conclusions, evidence, and uncertainty. Send it to the same challenger to:

- refute proposed blockers;
- challenge important clean conclusions and identify an unexamined seam;
- reconcile its blind candidates against the lead's evidence; and
- name only the narrowest missing proof for factual disputes.

For every candidate, establish PR relevance, a concrete supported/realistic path,
observable consequence or authority, and confirming/refuting evidence at the
frozen tip. Treat a candidate or verified-clean conclusion as refuted only when
the evidence exercises the same failure boundary and relevant conditions, such as
concurrency, cardinality, ordering, or lifecycle. A narrower green path is
counterevidence, not refutation. Resolve disputes with code, history, or the
smallest decisive proof, then return the updated evidence to the challenger.
Continue only while an exchange produces a new material candidate, counterexample,
or proof. One full exchange that changes no material status establishes
convergence. Route remaining provider/access-dependent facts as exact residual
verification and intent/policy ambiguity to the operator/author. Agreement alone
is not proof.

When a material candidate remains inconclusive, you may run the smallest safe
disposable falsification proof. State the hypothesis and oracle first; use an
untracked/gitignored test, script, harness, or fixture, compare base versus tip when
causality matters, change no tracked files or dependencies, and record the exact
result. Do not repeat broad verification for reassurance.

Reuse the same challenger session. If it cannot be resumed, give one replacement
the original blind inputs first; only after its independent return may it receive
the working set and continue reconciliation. If no challenger can complete both
phases, do not claim standard/large convergence; disclose the degraded topology
and remaining independent-review gap. If an agent stalls or returns no cited
trace, take the question back; respawn only for a clear transient failure.

### 4. Synthesis, freshness, and progress update

Before final classification:

1. Review shared seams and ask what both passes could have missed.
2. Read existing automated/human comments now; deduplicate and confirm current
   status without re-litigating mechanical findings.
3. Account for every AC, affected test, material surface, and verification route.
4. Re-read `headRefOid` and thread state. If the tip moved, review the delta and
   invalidate affected evidence; restart only if the map is no longer trustworthy.

For standard/large reviews, emit this as commentary after convergence:

```text
Frozen range/tip:
Change and risk map:
Solidified findings:
Refuted candidates:
Important verified-clean conclusions:
Remaining factual unknowns or decisions:
Optional deeper areas (ranked):
Default: finalize unless the operator redirects.
```

This update is non-blocking: do not end the turn or wait for a reply. Continue to
finalization unless a genuine decision, operator-controlled access/approval,
operator steering, or explicit pause intervenes. Accept `zoom out`, `drill into
<area>`, `shift to <area>`, or `challenge <candidate>` while working; pass any new
material evidence through the same internal loop before finalizing.

### 5. Calibrate and return

Apply `calibrate-review` to the validated raw result, verified-clean record,
current comments, and PR context. Calibration may change framing or action only
with explicit evidence-based reconciliation; it may not hide a confirmed blocker
or required-proof gap.

Return, in order:

1. the one-screen Action Brief from `calibrate-review`;
2. a compact operator-only appendix with the strict result, every raw non-clean
   item mapped to its final action/rejection reason, AC/test exceptions, grouped
   clean test coverage + Test-quality verdict, verification/routing, material
   verified-clean surfaces, and residual/Tier-4 checks — never full clean AC or
   per-test ledgers; and
3. restore the recorded branch if the original checkout was switched; if a worktree
   was used, leave the original checkout untouched and report its path.

Finalize only when every material surface/seam, AC, affected test, candidate,
verification route, prior comment, and current tip is accounted for and the
standard/large internal exchange has stabilized. Another pass requires a changed
tip, new evidence, or a named unanswered question—not another broad reread.

## Guardrails

- GitHub stays read-only: no comments, reviews, approvals, labels, commits, or
  pushes without a separate operator request and fresh approval.
- This result is not an implementation-loop verdict and does not satisfy an
  own-work implementation gate.
- If an environment blocks one check, route the exact residual check; do not abandon
  the review when code/history still permit useful progress.

## Failure modes

- Creating a review worktree when the clean repo-root checkout is available and
  the review does not require incompatible dependency/tool state.
- Classifying a PR compact without satisfying and recording every eligibility
  condition, or spawning a challenger for one that does.
- Exposing the lead's map/findings or prior comments before the challenger's blind
  pass, or treating the challenger as another certifying verdict.
- Using file count as the large/fan-out trigger, treating three agents as a target,
  selecting standard after mapping independent surfaces that need different proof
  without recording why one trace covers both, or giving a specialist the whole
  PR, shared seam, or broad gate.
- Reading prior findings before independent discovery.
- Treating agreement as evidence, ending reconciliation with a material factual
  dispute still answerable locally, treating a narrower green path as refutation,
  or repeating exchanges that add no evidence.
- Ending the turn at the convergence update instead of continuing by default.
- Repeating a broad pass or broad gate without a new question or causal reason.
- Writing proof code by default or prototyping a preferred implementation instead
  of falsifying one material question.
- Treating uncertainty as severity, or missing ideal proof as blocking without a
  tracked requirement or credible fail-open material path.
- Letting calibration silently omit a confirmed defect, unmet criterion,
  required-proof gap, test-quality failure, or shared-policy violation.
