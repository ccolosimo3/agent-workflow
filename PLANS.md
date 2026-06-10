# PLANS.md - Plan/Spec Doc Conventions

Personal cross-project conventions for planning docs. Apply when the local repo
uses a `plans/` directory or equivalent planning workspace.

## Directory Layout

- `plans/active/` — current work-in-progress (default for new docs)
- `plans/scratch/` — brain dumps, throwaway notes
- `plans/done/` — shipped/archived when the local repo keeps a done area;
  otherwise delete completed one-off specs after implementation lands or the PR
  is closed
- `plans/setup/` — long-lived environment/onboarding reference
- `plans/roadmap/` — long-lived strategic
- `plans/workflow/` — proposed edits to local workflow files awaiting application on other machines
- `plans/<topic-slug>/` — multi-doc bodies of work (use when 2+ related docs exist)

Directory placement is an organizational hint; `status:` frontmatter is the source of truth.

## Filename Convention

`<topic-slug>-<doctype>.md`, kebab-case. Common doctypes:

- `-rough-spec`, `-spec`, `-plan`, `-summary`
- `-review-prompt`
- `-walkthrough`, `-ladder`

Default: use one evolving spec file. Do not create a parallel `-issue-draft`
file unless the final public tracker issue must be split, redacted, or
substantially reshaped from the reviewed spec.

Specs for implementation work should include a test strategy, not just a list
of commands. The strategy should name the behavior or failure mode the tests
protect, the real operation boundary they exercise, any implementation-shape
tests that are only supplemental/contractual, and any manual or Tier 4 proof
needed because automation cannot represent the meaningful failure mode.

## Frontmatter Template

Every new plan doc starts with YAML frontmatter:

```yaml
---
title: <human title>
status: rough        # rough | review-ready | final | promoted | implemented | blocked | archived
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
- When creating a new spec, set `created:` and `updated:` to today's date and `status: rough`.
- Move a spec to `status: review-ready` when it is coherent enough for fresh-context review.
- Move a spec to `status: final` only after review findings are addressed and the operator approves promotion.
- Move a spec to `status: promoted` after the tracker issue exists and add the issue URL to frontmatter or `related:`.
- When implementation lands, either delete the one-off spec or set `status: implemented` and move reusable material to the repo's reference area.
- If a file under `plans/` has no frontmatter, leave it alone (legacy doc) — do not retrofit unless the user asks.
