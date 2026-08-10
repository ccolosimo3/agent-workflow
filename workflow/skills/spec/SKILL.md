---
name: spec
description: >-
  Research one selected tracker issue and produce its formal implementation-ready
  living spec, serially by default and without code or tracker mutation. Use only
  for /spec or an explicit formal-spec request. Do not trigger from a pasted
  issue, assignment, status question, or casual options discussion; not review.
---

# spec

This session IS the planning agent (kernel "Startup Routing" path B). The
output contract is the `## Planning Kickoff` template in
`~/.agents/workflow/kickoffs/planning.md`, self-applied with the issue as `<source>` —
its deliverables define what done looks like.

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
   If the repo adapter points to a planning-only reference, read it now; do not
   load such references in unrelated implementation/review sessions.

2. **Investigate — stay proportional.** Decompose the unknowns into
   independent questions: reproduction path, root-cause candidates, blast
   radius, existing repo patterns to reuse, prior art in git history and
   merged PRs — and, for bug fixes and edge cases, the adjacent-mechanism
   question: what existing code path already handles analogous behavior (read
   the FULL function/module being modified, not just the lines the issue
   points at), and can the case be routed into it with a narrower condition
   change before any new helper/filter/policy/state is proposed? Investigate
   serially by default. Spawn read-only subagents only when there are at least
   two genuinely independent, material unknowns and parallel work will shorten
   the pass; use at most two, each scoped to one question with a structured,
   file:line-cited return. When model selection is available, use GPT-5.6 Terra
   `high` for these bounded evidence investigators; reserve the parent/stronger
   model for load-bearing synthesis. Use web
   search freely for framework/provider/library behavior,
   known upstream issues, and changelogs (prefer primary docs; note the
   source when a decision rests on one), and any repo-connected docs MCP
   (e.g. a Vendure docs server) when relevant. Every load-bearing claim is
   verified against the current tree with a file:line citation; anything
   unconfirmed becomes an open question, not an assertion (Planning Kickoff
   item 9).

3. **Synthesize.** Root cause (or, for feature work, the governing design
   constraints) with evidence; two or three candidate approaches with
   tradeoffs — when an adjacent mechanism exists, the minimal
   route-into-the-existing-path option MUST be one of them; one recommendation
   plus a rejected alternative (the decision brief); the one-line Domain Pass
   decision per the kernel's triggers. Recommend the simplest complete,
   repo-conventional approach. Tie every added abstraction, configuration/state
   surface, tool, compatibility path, or cross-surface mechanism to a current
   requirement, observed failure, or established repo pattern; defer
   hypothetical hardening.
   When the destination exceeds one Task, map the sequence but fully specify
   only the next independently reviewable slice. Each slice must leave a valid
   state if later work never lands; split independently provable risks, but do
   not manufacture shape-only scaffolding or coordination ceremony.

4. **Write the living spec.** Create or reuse the work-item folder per the
   repo's planning conventions (e.g.
   `.agent-workflow/plans/active/<ISSUE-ID>-<short-kebab-title>/README.md`)
   with PLANS.md frontmatter, `status: rough`. The spec carries the
   Planning Kickoff deliverables plus: a test strategy per
   `~/.agents/workflow/TESTING.md` (behavior protected, failure mode, real
   operation boundary); for UI work, a design strategy per
   `~/.agents/workflow/FRONTEND.md` (the tokens/primitives/patterns it uses,
   the states it renders, and the visual proof); exact verification commands by
   touched surface from the repo's verification doc; the proposed branch name per the shim's
   branch rule; and open questions / `[decision-required]` items the operator
   must settle. Scale the plan to the change's size/risk — a trivial
   single-surface fix gets a compact plan (skip the two-or-three-approach
   synthesis), not the full treatment.
   If a named main planner is active, update only this work-item folder and
   return a concise reconciliation note; that planner owns shared `INDEX.md` and
   umbrella state. Otherwise perform the repo's normal shared-state update.

5. **Advance to review.** If no worthwhile direction decision remains, move the
   spec to `review-ready`, report its path/status, and invoke `/specreview`
   yourself in the same session; follow its autonomous revise→re-review loop.
   After convergence, apply HANDOFF.md's positive outer-spec risk selector:
   launch `/outerspecreview` when required, otherwise report the skip.
   Pause only for a real approach, scope, product/policy/naming, or
   no-clear-winner tradeoff decision. If the direction is still open or rests
   on an unproven architectural bet, recommend `/explore` or `/spike` and wait
   instead of forcing a single-path spec. Do not promote to `final` or mutate
   the tracker without the operator.

## Failure modes to avoid

- Editing code "just to test a fix" — propose patches inside the spec; even a
  throwaway spike needs an explicit operator ask.
- Mutating the tracker, or creating a branch during planning.
- Asserting a root cause without file:line evidence from the current tree.
- Investigator sprawl: serial is the default; never exceed two subagents or
  delegate routine orientation. Don't re-run what a subagent already answered.
- Skipping the repo shim's read-first docs and rediscovering known sharp edges.
- Drafting straight to `final` — rough → review-ready → `/specreview` is the
  path.
- Pausing before `/specreview` when no direction decision remains.
- Pausing to ask whether to run a required outer spec gate, or running one when
  no positive outer-spec risk trigger applies.
- Treating a broad destination as one implementation Task, or over-slicing it
  into pieces with no meaningful standalone behavior or proof.
