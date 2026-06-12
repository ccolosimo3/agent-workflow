---
name: planreview
description: Hand off a plan or spec for review before promotion
  (e.g. before `gh issue create`, before implementation kickoff). Reads the
  canonical Plan Review Kickoff template from
  ~/.agents/workflow/KICKOFFS.md, populates it from the current session,
  emits the populated prompt verbatim in chat under a
  `Plan Review Kickoff Prompt` block, then spawns exactly one fresh-context
  reviewer subagent. Use when the operator says /planreview, "review this
  spec", "pre-promotion review", "review the final spec before I file the
  issue", or similar.
---

# planreview

Pre-promotion review for planning artifacts (rough specs, review-ready specs,
final specs, plan markdown) — validate scope coverage, file/line claim
accuracy, label correctness, self-containment, and dependency claims at the
cheapest possible point. The planning equivalent of [[cjcreview]]. Shared
mechanics live in `~/.agents/workflow/HANDOFF.md` — apply that protocol with
the parameters below.

## Protocol parameters

- Template: `## Plan Review Kickoff` in `~/.agents/workflow/KICKOFFS.md`
- Emitted heading: `## Plan Review Kickoff Prompt`
- Announce: `spawning one plan reviewer`
- Spawns: yes — one fresh-context reviewer

## Population specifics

- **Plan artifact**: path/link, artifact type (`rough-spec`,
  `review-ready-spec`, `final-spec`, other), intended downstream action
  (`gh issue create`, implementation kickoff, …), target repo + intended
  labels if filing an issue.
- **Planner summary**: 2-3 sentences naming what the plan delivers and why.
- **Source material**: upstream context / parent spec / audit path, related
  issues / ADRs / prior discussion, modules and files claimed in scope.
- **Scope coverage**: intended in-scope items, intentional out-of-scope items
  + reason, dependency / ordering claims.
- **Hot spots / known risk in the plan**: ambiguous areas, claims to
  fact-check against the code, decisions made and rejected alternatives.
- **Existing-mechanism claim (field 4a; fill from the FILESYSTEM, not
  memory)**: for bug fixes, edge cases, fallback/error/loading behavior, or
  business-rule tweaks, name the current code path that already handles
  analogous behavior (file:line) and whether the plan reuses or bypasses it;
  write "none found" only after searching the modules the plan touches.

Missing material is signal, not a gap to fill: if the spec lacks explicit
non-goals, file claims, or dependencies, say so in the kickoff — that is often
what the reviewer should flag.

## Failure modes

The shared ones in HANDOFF.md, plus: fabricating scope items, label sets, or
dependencies; reviewing a non-plan artifact — for implemented code, use
[[cjcreview]] instead.
