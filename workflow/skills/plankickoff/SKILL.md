---
name: plankickoff
description: Begin planning and research for a newly assigned tracker issue
  (Linear or GitHub). The invoking session becomes the planning agent and
  orchestrator — it reads the issue and its linked context, spins up read-only
  investigation subagents to find the root cause or design constraints (web
  search encouraged for framework/provider questions), and produces the
  work-item folder and living spec per ~/.agents/workflow/PLANS.md and the
  repo shim. Planning only — no code edits, no branch creation, tracker stays
  read-only. Use when the operator says /plankickoff <issue>, "we've been
  assigned <ISSUE-KEY>", "start planning this issue", or pastes an issue URL
  asking for root cause and the best approach. Not for reviewing an existing
  spec (planreview) or implemented code (cjcreview).
---

# plankickoff

This session IS the planning agent (kernel "Startup Routing" path B). The
output contract is the `## Planning Kickoff` template in
`~/.agents/workflow/KICKOFFS.md`, self-applied with the issue as `<source>` —
its ten deliverables (problem framing through claim grounding and the Domain
Pass decision) define what done looks like. Mode defaults to `task`.

Hard role limits: no code edits, no branch creation, no Linear/GitHub
mutations (reads only; mutations stay approval-gated per the kernel and repo
shim). The Destructive Action Policy applies to any command run during
research.

## When invoked

1. **Intake.** Parse the issue key/URL. Read the issue, its parent/child
   issues, comments, labels, and linked docs (Linear read tools or
   `gh issue view` / `gh api`, read-only). Load the repo's startup context per
   its shim (e.g. `CONTEXT.md`, coding-standards). Restate the goal,
   non-goals, and acceptance criteria as currently understood, and name the
   unknowns that investigation must resolve.

2. **Investigate — orchestrate, don't wander.** Decompose the unknowns into
   independent questions: reproduction path, root-cause candidates, blast
   radius, existing repo patterns to reuse, prior art in git history and
   merged PRs. Spawn read-only subagents in parallel for independent
   questions — each scoped to one question with a structured, file:line-cited
   return. Use web search freely for framework/provider/library behavior,
   known upstream issues, and changelogs (prefer primary docs; note the
   source when a decision rests on one), and any repo-connected docs MCP
   (e.g. a Vendure docs server) when relevant. Every load-bearing claim is
   verified against the current tree with a file:line citation; anything
   unconfirmed becomes an open question, not an assertion (Planning Kickoff
   item 9).

3. **Synthesize.** Root cause (or, for feature work, the governing design
   constraints) with evidence; two or three candidate approaches with
   tradeoffs; one recommendation plus a rejected alternative (the decision
   brief); the one-line Domain Pass decision per the kernel's triggers.

4. **Write the living spec.** Create or reuse the work-item folder per the
   repo's planning conventions (e.g.
   `.agent-workflow/plans/active/<ISSUE-ID>-<short-kebab-title>/README.md`)
   with PLANS.md frontmatter, `status: rough`. The spec carries the ten
   Planning Kickoff deliverables plus: a test strategy per
   `~/.agents/workflow/TESTING.md` (behavior protected, failure mode, real
   operation boundary); exact verification commands by touched surface from
   the repo's verification doc; the proposed branch name per the shim's
   branch rule; and open questions / `[decision-required]` items the operator
   must settle. Update the plans `INDEX.md` when the repo keeps one.

5. **Hand back.** End with the spec path and status, the decision-required
   items, and the next pipeline step: operator revises → spec goes
   `review-ready` → `/planreview` (then `/planrereview` after findings).
   Do not auto-run planreview, and do not promote to `final` or to the
   tracker without the operator.

## Failure modes to avoid

- Editing code "just to test a fix" — propose patches inside the spec; even a
  throwaway spike needs an explicit operator ask.
- Mutating the tracker, or creating a branch during planning.
- Asserting a root cause without file:line evidence from the current tree.
- Investigator sprawl: a few well-scoped parallel subagents beat many vague
  ones; don't re-run what a subagent already answered.
- Skipping the repo shim's read-first docs and rediscovering known sharp edges.
- Drafting straight to `final` — rough → review-ready → `/planreview` is the
  path.
