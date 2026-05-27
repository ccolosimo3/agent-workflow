---
name: planrereview
description: Hand off a revised plan, spec, or issue draft for a follow-up
  review after the planner has addressed findings from a prior ACTIONABLE
  plan review. Reads the canonical Plan Re-Review Kickoff template from
  ~/.agents/workflow/KICKOFFS.md, populates it with the prior findings and
  the revisions applied, emits it verbatim in chat, and spawns one
  fresh-context reviewer subagent. Use when the operator says
  /planrereview, "re-review this spec", or after revisions land in
  response to a prior plan review.
---

# planrereview

Follow-up review handoff after the planner has revised a plan in response
to ACTIONABLE findings. Companion to [[planreview]] — same fidelity rules,
different focus (verify each prior finding addressed + check for any new
issues introduced by the revisions).

## When invoked

1. **Locate the prior reviewer findings.** They should be present in the
   chat context (the operator typically pastes the reviewer verdict, or
   the prior reviewer subagent returned them in this session). If they
   are not present, **stop and ask the operator** for them before
   continuing. Do not invent or paraphrase prior findings.

2. **Identify the revised artifact.** Confirm the path of the plan / spec
   / issue draft being re-reviewed. If the artifact is version-controlled,
   identify the **base** commit (state the prior reviewer saw) and the
   **tip** (current state). If not version-controlled, ask the operator
   for a summary of revisions or a before/after snippet.

3. **Gather the revision context:**
   - `git diff <base>..HEAD -- <artifact path>` — full diff of the
     artifact since the prior review (if version-controlled)
   - Any revision summary the planner already posted in chat (per-finding
     resolutions)

4. **Read the canonical template** from
   `~/.agents/workflow/KICKOFFS.md`, `## Plan Re-Review Kickoff` section.
   Apply the AGENTS.md **Fidelity Rule**: paste the section verbatim with
   placeholders filled — do not paraphrase, restructure, or invent a
   different shape.

5. **Populate every placeholder** from steps 1-3:
   - Artifact path
   - Prior review verdict, source kickoff pointer
   - Prior findings (quote verbatim)
   - Summary of revisions mapped to findings
   - Diff or before/after snippet

   If any placeholder cannot be filled honestly, stop and ask the operator.

6. **Emit the populated prompt verbatim in chat** under a
   `## Plan Re-Review Kickoff Prompt` heading, in a ```text fenced block.
   This must appear in chat **before** any reviewer subagent is spawned.

7. **Spawn exactly one fresh-context reviewer subagent** with that prompt
   verbatim. Use whichever subagent mechanism the host agent has available
   (Agent tool, subagent invocation, etc.). Announce `spawning one plan
   re-reviewer`. If the host environment has no subagent capability, emit
   the prompt and explicitly tell the operator to launch the reviewer
   manually.

8. **Tell the operator** that the same prompt is in the chat block above
   for their second independent re-reviewer if they want one. Do not spawn
   a second reviewer unless explicitly asked.

## Failure modes to avoid

- **Running without prior findings in context.** The re-review is only
  meaningful against a specific set of findings.
- **Paraphrasing the prior findings.** Quote them as the reviewer wrote
  them.
- **Asking for a fresh broad re-review.** Focus is "did the revisions
  address the findings, and did they introduce any new issues?" — not a
  from-scratch plan review.
- **Spawning more than one reviewer.** Second review is operator-owned.
