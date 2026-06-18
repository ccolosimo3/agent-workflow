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
