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
ordinary agent searches. This is separate from cleanup on land: work first
moves intact to the local `archive/`, then becomes eligible for externalization
only when its frontmatter is terminal (`implemented`, `closed`, or `deferred`)
and its `landed:` date (falling back to `updated:`) is at least 30 days old.

- A periodic audit may report candidates without approval. It reads only the
  local `archive/`; `active/`, `backlog/`, and `reference/` are never automatic
  candidates.
- Sync and pruning are operator-driven. Show the exact folders, private remote,
  destination, and whether pruning is included before requesting one bundled
  approval for the fast-forward push, recovery verification, and exact prune.
- Store archived plans as ordinary files under
  `projects/<project>/<work-item>/`; do not create recurring ZIP snapshots or a
  persistent archive checkout under any project root.
- Write a SHA-256 batch manifest, verify the pushed commit through a second
  fresh clone, and compare every path and byte before removing local sources.
  Any failure leaves the local copy intact; a remote path conflict blocks rather
  than overwrites.
- Leave only a compact retrieval pointer (remote, commit, subtree) in the live
  project. Restore into a disposable directory first.
- Keep separate archives for different ownership or confidentiality boundaries.
  A private Git host is off-device storage, not client-side encryption or an
  independent disaster-recovery copy.
