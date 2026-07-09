---
name: specreview
description: Hand off a plan or spec for review before promotion
  (e.g. before `gh issue create`, before implementation kickoff). Reads the
  canonical Spec Review Kickoff template from
  ~/.agents/workflow/kickoffs/spec-review.md, populates it from the current session, then
  spawns exactly one fresh-context reviewer subagent (announcing the handoff;
  the prompt is emitted in chat only as a no-subagent fallback). Use when the
  operator says /specreview, "review this
  spec", "pre-promotion review", "review the final spec before I file the
  issue", or similar.
---

# specreview

Pre-promotion review for planning artifacts (rough specs, review-ready specs,
final specs, plan markdown) — validate scope coverage, file/line claim
accuracy, label correctness, self-containment, and dependency claims at the
cheapest possible point. The planning equivalent of [[implreview]]. Shared
mechanics live in `~/.agents/workflow/HANDOFF.md` — apply that protocol with
the parameters below.

## Protocol parameters

- Template: `## Spec Review Kickoff` in `~/.agents/workflow/kickoffs/spec-review.md`
- Emitted heading (no-subagent fallback): `## Spec Review Kickoff Prompt`
- Announce: `spawning one spec reviewer`
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

## After the verdict (autonomous loop)

specreview is the first pass of an autonomous review→revise→re-review loop, not
a one-shot. When the spawned reviewer returns:

- **APPROVED** → report to the operator with a one-line-per-pass changelog; the
  plan is review-clean.
- **ACTIONABLE** → split the findings:
  - **Direction findings** — anything tagged `[decision-required]`, plus
    anything you cannot resolve without choosing an approach, changing scope,
    weighing a no-clear-winner tradeoff, or making a product/policy/naming call.
    Apply this filter yourself; do not trust the tag alone. STOP on these:
    summarize each as a crisp decision for the operator and return. Never pick
    the direction.
  - **Autonomous findings** — wrong file:line claims, untestable/unclear
    acceptance criteria, missing non-goals or verification commands, weak test
    strategy, convention / existing-mechanism gaps. Resolve each by tightening
    the spec's correctness/clarity — never by deleting the flagged element or
    weakening a criterion to dodge it. Then decide whether to re-review:
    - **Minor-only off-ramp.** If the ENTIRE remaining batch was mechanical and
      self-evidently correct on inspection — a corrected file:line citation, a
      typo/wording fix, a missing verification command / non-goal / acceptance
      criterion added verbatim as the finding specified, a label correction —
      such that a fresh reviewer would have nothing to add, do NOT re-review:
      patch, break the loop, and report (below). The bar is whole-batch — one
      substantive finding (a change to approach / scope / a criterion's meaning,
      a test-strategy rework, or any fix that could be wrong, debatable, or
      cascades into the rest of the plan) and you re-review instead.
    - Otherwise invoke `specrereview` on the revised spec.
- Loop ACTIONABLE→revise→`specrereview` until APPROVED, a direction finding
  stops it, or a minor-only round breaks it. **Cap at 3 revise→re-review
  cycles**; if still ACTIONABLE after 3, stop and surface the remaining findings.
  On every stop or APPROVED, give the operator a one-line-per-pass changelog of
  what changed. A minor-only off-ramp is YOUR call, not an independent APPROVED:
  report each patched finding and why it was mechanical, say that no fresh
  reviewer re-confirmed, and note the operator can run `/specrereview` or rely on
  `/secondspecreview` as the outer gate.

## Failure modes

The shared ones in HANDOFF.md, plus: fabricating scope items, label sets, or
dependencies; reviewing a non-plan artifact — for implemented code, use
[[implreview]] instead.
