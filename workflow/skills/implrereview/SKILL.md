---
name: implrereview
description: >-
  Reuse the original inner implementation reviewer to verify patches for its
  ACTIONABLE findings. Use for /implrereview, an inner “re-review,” or after an
  inner-review patch. Do not use for outerreview findings; they return directly
  to the same outer reviewer.
---

# implrereview

Follow-up review handoff after the implementer patched findings from a prior
inner ACTIONABLE verdict, or when the operator explicitly restarts the inner
loop. Companion to [[implreview]]. Shared mechanics live in
`~/.agents/workflow/HANDOFF.md` — apply that protocol with the parameters below;
this file adds only the re-review specifics.

## Protocol parameters

- Template: `## Re-Review Kickoff` in `~/.agents/workflow/kickoffs/re-review.md`
- Reviewer: REUSE the original reviewer's open session per HANDOFF.md §6 — hand it
  the patch summary (it holds the diff + rubric + prior findings). Spawn a fresh
  re-reviewer with the full populated kickoff ONLY as the fallback (original not
  resumable).
- Announce: `continuing the original reviewer for re-review` (or `spawning a fresh
  re-reviewer` on the fallback)
- Emitted heading (last-resort fallback, no subagent at all): `## Re-Review Kickoff Prompt`

## Re-review specifics

1. **Locate the prior findings** in chat context — the operator-pasted
   verdict, this session's reviewer return, or an outer-gate `outerreview`
   verdict returned by the Claude CLI/other app when the operator explicitly
   restarted the inner loop. If absent, stop and ask; never invent or paraphrase
   prior findings. Quote them verbatim, severity and path:line included.
2. **Confirm the patch range**: base = the state the prior reviewer saw
   (the commit at prior kickoff emission, or the one the verdict references);
   tip = current HEAD. If the base is ambiguous, ask — do not guess.
3. **Gather the patch context**: `git log --oneline <base>..HEAD`,
   `git diff --stat <base>..HEAD`, and any per-finding resolution summary the
   implementer already posted in chat.
4. **Populate** (fresh-fallback path; when reusing the original reviewer, hand it
   just the findings verbatim + base/tip range + resolution notes): work item / PR
   / branch / base links; prior verdict + source kickoff pointer; findings
   verbatim; base/tip SHAs, commit list, diff stat; implementer notes if available.

## Failure modes

The shared ones in HANDOFF.md, plus: running without prior findings in
context; paraphrasing the prior findings; asking for a broad fresh review —
the scope is "did the patches address the findings, and did they break
anything else?", not a from-scratch walk of the diff; or autonomously routing
outerreview findings through the inner reviewer.
