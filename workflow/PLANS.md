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
  intact when the PR merges or the issue closes. Local historical record until
  the operator explicitly externalizes selected folders; never delete archived
  work solely because it is old.
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

Keep review findings and verdicts only in `reviews.md`; implementation receipts
and other artifacts may record implementation and verification evidence, but
must not duplicate review history.

Specs for implementation work should include a test strategy per
`~/.agents/workflow/TESTING.md` (behavior/boundary, supplemental-shape, Tier-4
proof), not just a list of commands.

Do not create a parallel `-issue-draft` file unless the final public tracker
issue must be split, redacted, or substantially reshaped from the reviewed
spec.

## Large Work-Item Subfolders

Default work-item folders should stay small. For large issues, keep the root
focused and move task-specific docs into `slices/` (specs for implementation
slices) and `spikes/` (bounded proof specs and writeups); add other subfolders
only if a project actually needs them.

Do not fold every slice back into `README.md` — update it only when the durable
feature contract changes. Command results go in `verification.md`, reviewer
outcomes in `reviews.md`.

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

## Periodic external archive cleanup

Use `/plan-cleanup` when completed folders have accumulated enough to distract
ordinary agent searches — and run it at each main-project completion, not only
when clutter is noticed. This is separate from cleanup on land: work first
moves intact to the local `archive/`, then becomes eligible for externalization
when its frontmatter is terminal (`implemented`, `closed`, or `deferred`) and
either its `landed:` date (falling back to `updated:`) is at least 30 days old
or its parent project/umbrella is complete — a completed main project's
folders may be externalized immediately with operator-approved scope.

The `plan-cleanup` skill owns the sync/prune safety envelope (audit scope,
bundled approval, manifests, fresh-clone verification, retrieval pointers). Two
things worth knowing before you invoke it: a periodic audit reads only the local
`archive/` — `active/`, `backlog/`, and `reference/` are never automatic
candidates — and a private Git host is off-device storage, not encryption and
not an independent disaster-recovery copy.
