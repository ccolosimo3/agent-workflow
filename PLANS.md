# PLANS.md - Plan/Spec Doc Conventions

Personal cross-project conventions for planning docs. Apply when the local repo
uses a `plans/` directory or equivalent planning workspace.

## Directory Layout

- `plans/active/` — current work-in-progress (default for new docs)
- `plans/scratch/` — brain dumps, throwaway notes
- `plans/done/` — shipped/archived
- `plans/setup/` — long-lived environment/onboarding reference
- `plans/roadmap/` — long-lived strategic
- `plans/workflow/` — proposed edits to local workflow files awaiting application on other machines
- `plans/<topic-slug>/` — multi-doc bodies of work (use when 2+ related docs exist)

Directory placement is an organizational hint; `status:` frontmatter is the source of truth.

## Filename Convention

`<topic-slug>-<doctype>.md`, kebab-case. Common doctypes:

- `-rough-spec`, `-spec`, `-plan`, `-summary`
- `-review-prompt`, `-issue-draft`
- `-walkthrough`, `-ladder`

## Frontmatter Template

Every new plan doc starts with YAML frontmatter:

```yaml
---
title: <human title>
status: draft        # draft | active | blocked | done | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: <handle>
related:
  - path/to/related-plan.md
  - https://github.com/<org>/<repo>/issues/N
---
```

`related:` is optional. Omit when there are no related docs/issues.

## Update Rules

- When editing any file under `plans/`, bump `updated:` to today's date before saving.
- When creating a new plan doc, set `created:` and `updated:` to today's date and `status: draft` (or `active` if work is already underway).
- When a doc reaches done, set `status: done`, bump `updated:`, and move it to `plans/done/` (preserving topic subdirectory if useful).
- If a file under `plans/` has no frontmatter, leave it alone (legacy doc) — do not retrofit unless the user asks.
