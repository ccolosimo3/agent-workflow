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

Follow-up review handoff after the implementer has patched findings from a
prior ACTIONABLE verdict. Companion to [[cjcreview]] — same fidelity rules,
different focus (verify each prior finding addressed + check for regressions
or new issues introduced by the patches).

## When invoked

1. **Locate the prior reviewer findings.** They should be present in the
   chat context (the operator typically pastes the reviewer verdict, or the
   prior reviewer subagent returned them in this session). If they are not
   present, **stop and ask the operator** for them before continuing. Do
   not invent or paraphrase prior findings.

2. **Confirm the patch range.**
   - Identify the **base** commit: the state the prior reviewer saw.
     Usually the commit at the time the prior `Review Kickoff Prompt` was
     emitted, or the commit the reviewer's verdict references.
   - **Tip** is the current `HEAD` of the branch.
   - If the base is ambiguous, ask the operator to confirm before running
     git commands. Do not guess.

3. **Gather the patch context:**
   - `git log --oneline <base>..HEAD` — commits since the review
   - `git diff --stat <base>..HEAD` — files changed and churn
   - Any patch summary the implementer already posted in chat (per-finding
     resolutions)

4. **Read the canonical template** from
   `~/.agents/workflow/KICKOFFS.md`, `## Re-Review Kickoff` section. Apply
   the AGENTS.md **Fidelity Rule**: paste the section verbatim with
   placeholders filled — do not paraphrase, restructure, or invent a
   different shape. The Re-Review Kickoff is short and points the reviewer at
   `~/.agents/workflow/REVIEW_RUBRIC.md` ("Re-review mode"); do NOT inline the
   rubric — the spawned re-reviewer reads it itself.

5. **Populate every placeholder** from steps 1-3:
   - Work item link, PR link, branch, base
   - Prior review verdict, source kickoff pointer
   - Prior findings (quote verbatim)
   - Base/tip commit shas, commit list, diff stat
   - Implementer notes if available
   - **Repo conventions to enforce (fill from the FILESYSTEM, not operator
     memory)**: detect the repo root and resolve the real, existing paths the
     re-reviewer must load — testing (`~/.agents/workflow/TESTING.md`, fixed),
     coding-standards
     (`<root>/.agent-workflow/plans/reference/coding-standards.md`, else
     `<root>/mobile/CLAUDE.md`), and whether `<root>/.coderabbit.yaml` excludes
     any touched surface (e.g. migrations). Write `none found` only after
     checking. The re-reviewer needs these to confirm a rewritten test actually
     satisfies the repo's anti-pattern table, not just the literal prior finding.

   If any OPERATOR-SUPPLIED placeholder cannot be filled honestly, stop and ask
   the operator.

6. **Emit the populated prompt verbatim in chat** under a `## Re-Review
   Kickoff Prompt` heading, in a ```text fenced block. This must appear in
   chat **before** any reviewer subagent is spawned.

7. **Spawn exactly one fresh-context reviewer subagent** with that prompt
   verbatim. Use whichever subagent mechanism the host agent has available
   (Agent tool, subagent invocation, etc.). Announce `spawning one
   re-reviewer` so the operator sees the handoff. If the host environment
   has no subagent capability, emit the prompt and explicitly tell the
   operator to launch the re-reviewer manually.

8. **Tell the operator** that the same prompt is in the chat block above
   for their second independent re-reviewer if they want one. Do not spawn
   a second reviewer unless explicitly asked.

## Failure modes to avoid

- **Running without prior findings in context.** The re-review is only
  meaningful against a specific set of findings.
- **Paraphrasing the prior findings.** Quote them as the reviewer wrote
  them, severity and path:line included.
- **Asking for a full re-review from scratch.** The scope is "did the
  patches address the findings, and did they break anything else?" — not
  a broad walk of the diff.
- **Spawning more than one reviewer.** Second review is operator-owned.
