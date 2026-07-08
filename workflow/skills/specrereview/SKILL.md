---
name: specrereview
description: Hand off a revised plan or spec for a follow-up
  review after the planner has addressed findings from a prior ACTIONABLE
  spec review. Reads the canonical Spec Re-Review Kickoff template from
  ~/.agents/workflow/KICKOFFS.md, populates the prior findings + revisions, and
  REUSES the original reviewer's open session for the follow-up — falling back to a
  fresh re-reviewer subagent only if it can't be resumed (announcing the handoff).
  Use when the operator says
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
- Reviewer: REUSE the original reviewer's open session per HANDOFF.md §6 — hand it
  the revision summary (it holds the spec + rubric + prior findings). Spawn a fresh
  re-reviewer with the full populated kickoff ONLY as the fallback (original not
  resumable).
- Announce: `continuing the original reviewer for re-review` (or `spawning a fresh
  re-reviewer` on the fallback)
- Emitted heading (last-resort fallback, no subagent at all): `## Spec Re-Review Kickoff Prompt`

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
4. **Populate** (fresh-fallback path; when reusing the original reviewer, hand it
   just the findings verbatim + the revisions mapped to them): artifact path; prior
   verdict + source kickoff pointer; findings verbatim; revisions mapped to
   findings; diff or before/after snippet.

## After the verdict

This re-review is one cycle of specreview's autonomous loop. Apply the same
disposition to its result: **APPROVED** ends the loop (report + changelog); a
**direction / `[decision-required]`** finding stops it (return the decision to
the operator — do not pick it); other **autonomous** findings get resolved by
tightening the spec, then re-run through `specrereview` — until APPROVED or the
3-cycle cap (counted from the original specreview). If a round's remaining
findings are ALL minor and self-evidently fixed (the minor-only off-ramp in
specreview "After the verdict"), patch and break the loop with a report instead
of re-reviewing — your call, not an APPROVED. See specreview "After the verdict
(autonomous loop)".

## Failure modes

The shared ones in HANDOFF.md, plus: running without prior findings;
paraphrasing them; asking for a fresh broad review — the scope is "did the
revisions address the findings, and did they introduce any new issues?", not
a from-scratch spec review.
