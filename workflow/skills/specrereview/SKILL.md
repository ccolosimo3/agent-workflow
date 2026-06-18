---
name: specrereview
description: Hand off a revised plan or spec for a follow-up
  review after the planner has addressed findings from a prior ACTIONABLE
  spec review. Reads the canonical Spec Re-Review Kickoff template from
  ~/.agents/workflow/KICKOFFS.md, populates it with the prior findings and
  the revisions applied, emits it verbatim in chat, and spawns one
  fresh-context reviewer subagent. Use when the operator says
  /specrereview, "re-review this spec", or after revisions land in
  response to a prior spec review.
---

# specrereview

Follow-up review handoff after the planner revised a plan in response to
ACTIONABLE findings. Companion to [[specreview]]. Shared mechanics live in
`~/.agents/workflow/HANDOFF.md` — apply that protocol with the parameters
below; this file adds only the plan-re-review specifics.

## Protocol parameters

- Template: `## Spec Re-Review Kickoff` in `~/.agents/workflow/KICKOFFS.md`
- Emitted heading: `## Spec Re-Review Kickoff Prompt`
- Announce: `spawning one plan re-reviewer`
- Spawns: yes — one fresh-context reviewer

## Plan-re-review specifics

1. **Locate the prior findings** in chat context (operator-pasted verdict or
   this session's reviewer return). If absent, stop and ask; quote them
   verbatim — never invent or paraphrase.
2. **Identify the revised artifact**: confirm the plan/spec path. If
   version-controlled, base = the state the prior reviewer saw, tip = current
   state; if not, ask the operator for a revision summary or before/after
   snippet.
3. **Gather the revision context**: `git diff <base>..HEAD -- <artifact
   path>` when version-controlled, plus any per-finding resolution summary
   already posted in chat.
4. **Populate**: artifact path; prior verdict + source kickoff pointer;
   findings verbatim; revisions mapped to findings; diff or before/after
   snippet.

## After the verdict

This re-review is one cycle of specreview's autonomous loop. Apply the same
disposition to its result: **APPROVED** ends the loop (report + changelog); a
**direction / `[decision-required]`** finding stops it (return the decision to
the operator — do not pick it); other **autonomous** findings get resolved by
tightening the spec, then re-run through `specrereview` — until APPROVED or the
3-cycle cap (counted from the original specreview). See specreview "After the
verdict (autonomous loop)".

## Failure modes

The shared ones in HANDOFF.md, plus: running without prior findings;
paraphrasing them; asking for a fresh broad review — the scope is "did the
revisions address the findings, and did they introduce any new issues?", not
a from-scratch spec review.
