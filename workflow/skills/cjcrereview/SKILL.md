---
name: cjcrereview
description: Hand off a patched implementation for a follow-up review after the
  implementer has addressed findings from a prior ACTIONABLE review verdict.
  Reads the canonical Re-Review Kickoff template from
  ~/.agents/workflow/KICKOFFS.md, populates it with the prior findings and
  patch context from the current session, emits it verbatim in chat, and
  spawns one fresh-context reviewer subagent. Use when the operator says
  /cjcrereview, "re-review this", or after patches land in response to a
  prior review.
---

# cjcrereview

Follow-up review handoff after the implementer patched findings from a prior
ACTIONABLE verdict. Companion to [[cjcreview]]. Shared mechanics live in
`~/.agents/workflow/HANDOFF.md` — apply that protocol with the parameters
below; this file adds only the re-review specifics.

## Protocol parameters

- Template: `## Re-Review Kickoff` in `~/.agents/workflow/KICKOFFS.md`
- Emitted heading: `## Re-Review Kickoff Prompt`
- Announce: `spawning one re-reviewer`
- Spawns: yes — one fresh-context reviewer

## Re-review specifics

1. **Locate the prior findings** in chat context — the operator-pasted
   verdict, this session's reviewer return, or an outer-gate `secondreview`
   verdict pasted from the other app. If absent, stop and ask; never invent
   or paraphrase prior findings. Quote them verbatim, severity and path:line
   included.
2. **Confirm the patch range**: base = the state the prior reviewer saw
   (the commit at prior kickoff emission, or the one the verdict references);
   tip = current HEAD. If the base is ambiguous, ask — do not guess.
3. **Gather the patch context**: `git log --oneline <base>..HEAD`,
   `git diff --stat <base>..HEAD`, and any per-finding resolution summary the
   implementer already posted in chat.
4. **Populate**: work item / PR / branch / base links; prior verdict + source
   kickoff pointer; findings verbatim; base/tip SHAs, commit list, diff stat;
   implementer notes if available.

## Failure modes

The shared ones in HANDOFF.md, plus: running without prior findings in
context; paraphrasing the prior findings; asking for a broad fresh review —
the scope is "did the patches address the findings, and did they break
anything else?", not a from-scratch walk of the diff.
