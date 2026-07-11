# PLANS.md - Local Planning Directory Conventions

Personal cross-project conventions for the local (git-excluded) planning
workspace. The canonical shape is the one used in Townchest's
`.agent-workflow/plans/`; apply it to any repo with a local plans directory.
The repo's own `plans/README.md`, when present, wins on local specifics.

## Directory Layout

- `INDEX.md` — operational dashboard: active work table, backlog, archive
  one-liners, cleanup reminder. Keep it operational, not archival.
- `active/` — work items with a real next action (one folder per item).
- `archive/` — landed, closed, or deferred work-item folders, moved here
  intact when the PR merges or the issue closes. Local historical record;
  do not delete archived folders unless the operator asks.
- `backlog/` — scoped future work with a real trigger.
- `shelf/` — ideas that are real but not actionable yet.
- `reference/` — reusable workflow notes, checklists, verification routing,
  coding standards, durable domain lessons.
- `setup/` — local machine/account setup notes.
- `templates/` — copy-forward templates (e.g. PR body shape).

Directory placement is an organizational hint; `status:` frontmatter is the
source of truth.

## Work-Item Folders

One folder per tracker issue: `active/<ISSUE-ID>-<short-kebab-title>/`,
containing:

- `README.md` — the one living spec/plan (lifecycle statuses below; prefer one
  evolving spec over parallel draft files).
- `PR_BODY.md` — PR body draft.
- `verification.md` — commands run, manual proof, skipped gates.
- `reviews.md` — review verdicts and actionable findings.
- `artifacts/` — screenshots, exported logs, proof files when useful.

Specs for implementation work should include a test strategy, not just a list
of commands: name the behavior or failure mode the tests protect, the real
operation boundary they exercise, any implementation-shape tests that are only
supplemental/contractual, and any manual or Tier 4 proof needed because
automation cannot represent the meaningful failure mode.

Do not create a parallel `-issue-draft` file unless the final public tracker
issue must be split, redacted, or substantially reshaped from the reviewed
spec.

## Large Work-Item Subfolders

Default work-item folders should stay small. For large issues with multiple
spikes, slices, or release rehearsals, keep the root focused and move
task-specific docs into optional subfolders:

- `slices/` — concise specs for completed or in-progress implementation slices.
- `spikes/` — bounded proof specs and spike writeups.
- `release/` — rebase ledgers, merge rehearsals, final-review ledgers.
- `superseded/` — plans kept as fallback/history but not current direction.
- `future/` — follow-on design notes that are related but not yet their own
  work item.

Do not fold every slice back into `README.md`. Instead:

- update `README.md` only when the durable feature contract changes;
- record command results in `verification.md`;
- record reviewer outcomes in `reviews.md`;
- keep concise slice/spike specs standalone so agents can work from a small
  task surface.

If a `future/` item becomes actionable, promote it to its own folder under
`active/` or `backlog/`.

## Multi-Task Program Folders (Orchestrator V0 Draft)

This is inactive until Orchestrator Mode is activated. A reviewed V0 pilot may
use one umbrella work-item folder containing the living program spec plus
coordinator-owned operational state:

```text
active/<PROGRAM-ID>-<short-name>/
  README.md
  events.jsonl
  program.json
  approvals.json
  status.md
  integration.md
  verification.md
  reviews.md
  tasks/
  artifacts/
```

`INDEX.md` remains the roadmap authority and `README.md` remains the living spec.
`events.jsonl` is the operational source of truth; JSON/Markdown views are
generated and never become a second roadmap. Only the coordinator writes the
ledger. Child folders/specs retain their normal PLANS lifecycle.

## Frontmatter Template

Every new plan doc starts with YAML frontmatter:

```yaml
---
title: <human title>
status: rough        # rough | review-ready | final | promoted | implemented | reference | closed | deferred | blocked
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: <handle>
issue: <tracker URL>
pr: <PR URL or none>
landed: YYYY-MM-DD   # set when the PR merges / issue closes
related:
  - path/to/related-plan.md
---
```

`issue:`, `pr:`, `landed:`, and `related:` are included when they exist.

## Lifecycle & Update Rules

`rough -> review-ready -> final -> promoted -> implemented` (or `closed` /
`deferred`). Standalone decision/options docs that are not an evolving spec use
`status: reference`, outside that flow.

- Bump `updated:` when editing any plans file.
- `review-ready` when coherent enough for fresh-context review; `final` only
  after review findings are addressed and the operator approves promotion;
  `promoted` once the tracker issue exists (add the URL).
- Keep `pr:` frontmatter current when a PR opens — the INDEX active table
  should say which PR each folder is waiting on.
- When implementation lands: set `status: implemented` (or `closed` /
  `deferred`), set `pr:` and `landed:`, move the folder to `archive/`, refresh
  `INDEX.md`, and distill reusable lessons into `reference/`. Archived folders
  stay intact; bulky `artifacts/` may be pruned at operator discretion.
- If a file has no frontmatter, leave it alone (legacy doc) — do not retrofit
  unless the operator asks.

## Artifact cleanup on land

When the operator says an issue or PR landed, clean local planning artifacts
before moving on:

- Confirm the issue/PR state with the tracker.
- Delete obsolete local drafts now represented by the tracker or PR: issue
  drafts, PR-body drafts, review-note drafts, kickoff prompts, one-off review
  prompts.
- After issue creation, advance the same living spec through its lifecycle
  (above) rather than deleting it by default; delete only transient
  split/redaction issue drafts or prompts.
- Archive only durable context (reusable specs, verification/audit reports,
  ADR-like rationale, cross-issue policy decisions). Move still-actionable future
  work to `backlog/`, or keep it active only when it has a real next action.
- Update `INDEX.md` and any active-workstream README when they exist.
- Report what was deleted, archived, and left active. Do not leave completed
  issue/PR drafting artifacts in active folders; prefer one evolving spec over
  parallel rough-spec + issue-draft files.
