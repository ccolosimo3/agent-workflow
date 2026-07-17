---
name: large-pr-review
description: Run the explicit coordinated implementation outer gate for a large,
  generated-heavy, or cross-surface PR/branch using one lead and parallel
  read-only evidence scouts. Maps risk-coherent lanes, applies repo-aware review
  overlays, validates and deduplicates findings, coordinates verification once,
  and returns the canonical REVIEW_RUBRIC verdict for the final tip. Use when the
  operator invokes /large-pr-review or explicitly asks to force a fan-out outer
  review. This replaces adaptive outerreview for that gate; it is never an extra
  third pass and is not for coworker-PR calibration.
---

# large-pr-review

Run the explicit coordinated form of the implementation outer gate without
creating multiple verdict owners. The current
top-level task is the **lead reviewer**; spawned agents are scoped evidence
scouts. Only the lead applies the complete rubric and issues
`APPROVED`/`ACTIONABLE`.

Run this skill from a fresh top-level task after the inner loop converges; its
verdict certifies the exact final tip. An intentionally early/directional run is
allowed only when labeled non-certifying. This skill requires direct child
agents. If the host cannot spawn them, stop and route to adaptive `outerreview`;
do not silently degrade to serial review or emit disconnected manual kickoffs.

## Authorities and repo overlay

The lead reads and applies these authorities in order:

1. repo/company instructions and the source issue/spec;
2. `~/.agents/workflow/REVIEW_RUBRIC.md` in full;
3. `~/.agents/workflow/TESTING.md` and `FRONTEND.md` when applicable;
4. repo-local review guidance as an additive overlay.

Resolve and load the implementation/code-review overlay using
`~/.agents/workflow/REVIEW_RUBRIC.md` "Repository review overlay". Load it before
building lanes, then pass only the relevant routed paths and rules to each scout.
When no overlay exists, discover relevant existing files rather than hardcoding
one repo. Check, when present:

- `.agents/skills/collaborative-pr-review/SKILL.md` or the repo's equivalent;
- `docs/agent-rubrics/pr-review.md`, `review-feedback.yml`, `risk-lenses.yml`,
  and other review files routed by the repo shim;
- repo testing, coding-standard, design-system, verification, and SME skills
  relevant to the touched surfaces.

Reuse repo-specific domain risks, full-file/caller/consumer tracing, known false
positives/misses, and human discussion boundaries. The canonical rubric keeps
ownership of severity, strict verdicts, test-quality judgment, independence,
and safety. A repo overlay may strengthen those rules but never downgrade them,
require routine pauses, or authorize GitHub mutations.

## Workflow

### 1. Freeze the review target

- Run `git status --short --branch` before any checkout or branch change. Review
  committed work only; a dirty/uncommitted diff is not part of the certifiable
  range and must be committed or explicitly excluded before continuing.
- For a PR, gather live metadata with `gh pr view`, but default the review tip to
  the matching local head-branch ref so unpushed follow-up commits are included.
  Confirm the local branch corresponds to the PR's `headRefName` and compare it
  with the published `headRefOid`:
  - equal: the whole reviewed range is published;
  - local is a descendant: review local tip and record `published..local` as
    local-only commits;
  - local is behind or diverged: stop and surface the mismatch rather than omit
    commits or combine unrelated histories.
- Use the published PR head as the tip only when the operator explicitly asks
  for `published-only`, or after they confirm that no matching local branch is
  available. For a branch without a PR, resolve the integration branch from the
  repo shim and use local `HEAD`.
- Compute `base = merge-base(target branch, tip)` and record immutable
  `base..tip` SHAs plus the published/local-only split. Announce the target and
  continue.
- Ensure the clean review worktree is at that local tip before full-file reads or
  verification. In an isolated detached review worktree, updating only its
  detached pointer is allowed; never move the operator's branch or dirty tree.
- Recheck both the local branch ref and published PR head before the verdict. If
  the local tip moved, map `old tip..new tip`, rerun affected lanes and seams,
  and restart the map only when the topology changed broadly. Never certify a
  stale local tip.

### 2. Build the review map

Run `git diff --stat`, `--numstat`, `--name-status`, and the full diff. Classify
generated/vendor/lock artifacts separately from handwritten code using repo
ownership docs, `.gitattributes`, generators, and file headers.

Partition by connected behavior and risk, not directory, file count, line count,
or generic lenses across the entire diff. A lane should keep a change with its
callers, consumers, types, tests, migrations/config, and real runtime boundary.

Create a coverage map before dispatch:

`lane | primary changed files | connected unchanged files/traces | risk questions | seam owner`

Every changed file gets exactly one primary lane. Intentional overlap is allowed
at named contracts. The lead owns all cross-lane seams and any unassigned file.

Use the smallest useful fan-out:

- two or three scouts for a moderately broad PR;
- four or five for several independent surfaces, subject to host concurrency;
- waves when concurrency is limited.

This explicit gate requires at least two real coherent lanes. If the map cannot
produce them, do not invent generic lenses or duplicate coverage: stop and route
to adaptive `outerreview`, whose serial mode is the correct fit.

Include a bounded hygiene/convention lane when breadth makes low-signal misses
likely. It checks handwritten code, comments, docs, commands, dead code,
duplication, naming, and documented repo patterns—not subjective taste. Generated
output gets one provenance/semantic owner rather than dominating every lane.

### 3. Dispatch read-only scouts

Read `~/.agents/workflow/kickoffs/large-pr-review-scout.md`, populate it verbatim
for each lane, announce the lane fan-out, and spawn one direct scout per lane.
Do not give scouts prior findings, verdicts, or review comments.

Scouts:

- inspect assigned changed files in full plus connected unchanged source;
- return evidence, candidate findings, test assessment, clean checks, and seams;
- may report concrete lows/nits naturally noticed, but do not hunt taste;
- use the supplied issue/AC context; do not refetch the tracker or source issue
  unless an unresolved lane ambiguity requires it and the lead asks;
- never issue an overall verdict, edit, checkout, post, approve, or spawn agents;
- may run a narrow, non-mutating, lane-specific check when it materially helps
  validate a claim. Report its exact command and result. Do not run broad or
  expensive suites, mutating generators, provider-backed checks, or a check
  already owned by another lane; the lead coordinates shared verification and
  decides whether further confirmation is needed.

Continue the lead's own review while scouts run, then wait for every assigned
lane. Missing or incomplete scout coverage returns to the same scout once; the
lead absorbs the lane if it still cannot complete.

Keep operator updates compact. Announce the frozen target and lane map, then
consolidate later progress into material state changes or periodic summaries
while work is still running. Do not narrate every scout return or every
candidate-validation step; always surface a blocker, target movement, or scope
change promptly.

### 4. Lead integration pass

The lead remains responsible for a valid canonical review:

- re-derive intent and acceptance criteria from the original source;
- inspect the complete diff personally. The coordinated team collectively
  satisfies the rubric's full-file duty: each handwritten changed file is opened
  in full by its assigned scout or the lead, and the coverage map records the
  owner. The lead personally opens every candidate location, unassigned file,
  cross-lane seam, material generated authority, and any file needed to validate
  a scout's clean conclusion. Do not reopen every clean lane file solely to
  duplicate completed scout coverage;
- trace cross-lane contracts, state transitions, ordering, partial failure,
  authorization, generated provenance, and consumer boundaries;
- build the global AC and per-test ledgers;
- validate every scout candidate directly against current source and discard,
  correct, or merge unsupported/duplicate findings;
- follow cross-scope leads instead of assuming another lane owns them;
- coordinate verification around named review risks so each selected check runs
  once across the team, and record its exact result and owner;
- apply canonical severity and issue the only verdict.

Do not vote across scouts or concatenate their outputs. Their reports are claims
to verify, just like the implementer's summary.

For routing, change-detection, caching, or workflow-composition candidates,
reproduce the claim through the real composed entry point with its actual
upstream inputs. A helper probe with fabricated upstream state is supporting
evidence only and cannot become an ACTIONABLE finding by itself. If the real
boundary cannot be exercised or established from source, mark the claim
unverified rather than promoting it.

Before running verification, record the risk question and the smallest command
that can answer it. Prefer trustworthy green CI at the exact reviewed SHA for
broad gates already covered there, while independently rerunning cheap, narrow,
decisive boundaries when they test a live review hypothesis. Do not run a full
suite merely to reproduce implementer or CI evidence. Use a broad/full suite
when a candidate, changed risk surface, stale/missing CI, or cross-boundary
uncertainty actually requires it. Never use CI as a substitute when the review
hypothesis needs independent local proof.

### 5. Preserve independence, then collaborate

Freeze the independently derived candidate set before reading existing PR review
comments. After that seal, read posted comments/threads only to mark findings
`new`, `already raised`, `resolved`, or `still unresolved`; do not let them replace
independent evidence. If this task was already exposed to prior findings, apply
HANDOFF's quarantine/disclosure rule and continue.

Present the result for operator discussion. GitHub stays read-only; posting,
approving, requesting changes, or editing the PR needs a separate explicit
request and approval.

### 6. Return

Begin with a compact `Implementation handoff` containing the verdict and only
the new unresolved findings or decisions the implementer must act on. Give each
an explicit disposition target (`patch`, `disclose`, `file/follow-up`, or
`decline with reason`). Separate already-dispositioned findings, existing
follow-ups, and pre-existing nits from active work; never present them as needing
disposition again.

Then return the full `REVIEW_RUBRIC.md` Output contract, plus:

- the exact `base..tip` and tip SHA reviewed;
- the published PR head, local tip, and exact local-only commit range (or
  `none`);
- a compact coverage appendix:
  `lane | primary paths | connected traces | scout complete/gap | lead seam check`;
- for an open PR, the post-seal `new/already raised/resolved/unresolved` mapping;
- naturally noticed suggestions/nits under the rubric's low-severity rules;
- verification run once by the lead and any residual unverified boundary.

Use portable repo-relative `path:line` locations. Do not emit app-specific or
session-specific generated source links; the handoff must work when pasted into
another Codex or Claude task.

State that this coordinated verdict satisfies the implementation outer gate for
the exact reviewed final tip and does not require a subsequent `outerreview`. If
the operator explicitly requested an early/directional pass, state instead that
it is non-certifying and cannot satisfy the final-tip gate.

## Follow-up review

After an ACTIONABLE verdict, carry the findings back to the implementation
session and patch through `implrereview`. Certify the patched final tip with a
fresh `outerreview` or `large-pr-review` invocation; do not reuse this certifying
lead or its scouts. An explicitly early/directional pass may reuse affected scouts
for non-certifying iteration, but only a fresh final-tip outer gate counts.

## Failure modes

- Splitting files evenly or assigning one generic lens over the whole diff.
- Letting generated churn determine worker count or attention.
- Multiple verdicts, majority voting, or trusting a scout finding unverified.
- Leaving a changed file or cross-lane seam without an explicit owner.
- Every scout loading the full output contract or rerunning the same gates.
- Flooding the lead with raw logs instead of bounded evidence.
- Reading prior findings before the independent candidate set is sealed.
- Reviewing only the published PR head while a matching local branch is ahead.
- Certifying a tip that moved during the review.
- Running this explicit gate as a third pass after a valid final-tip outerreview.
