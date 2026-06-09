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
final specs, and plan markdown). The planning equivalent of [[cjcreview]] — same
orchestration, different subject and validation focus. Encodes the
"Spec review before tracker promotion" ritual: validate scope coverage,
file/line claim accuracy, label correctness, self-containment of the
issue body, and dependency claims at the cheapest possible point, before
the artifact gets promoted to a tracker issue or handed to an implementer.

## When invoked

1. **Read the canonical template.** Read
   `~/.agents/workflow/KICKOFFS.md` and locate the
   `## Plan Review Kickoff` section. Apply the AGENTS.md **Fidelity Rule**:
   paste the section verbatim with placeholders filled. Do not paraphrase,
   restructure, reorder, or invent a different shape. The structure is
   load-bearing for downstream reviewer agents.

2. **Populate every placeholder** from the current session:

   - **Plan artifact**: path or link to the markdown, artifact type
     (`rough-spec`, `review-ready-spec`, `final-spec`, or other), intended downstream action
     (`gh issue create`, implementation kickoff, etc.), target repo and
     intended labels if filing an issue.
   - **Planner summary**: 2-3 sentences naming what the plan delivers and
     why.
   - **Source material**: upstream context / parent spec / audit path (if
     any), related issues / ADRs / prior discussion, modules and files claimed
     in scope.
   - **Scope coverage**: intended in-scope items, intentional out-of-scope
     items + reason, dependency / ordering claims.
   - **Hot spots / known risk in the plan**: ambiguous areas, claims to
     fact-check against the code, decisions made and rejected alternatives.
   - **Repo conventions to enforce (fill from the FILESYSTEM, not operator
     memory; the stop-and-ask rule below does not apply to it)**: detect the
     repo root and resolve the real, existing paths the reviewer must load to
     judge the plan's test strategy and convention conformance —
     testing (`~/.agents/workflow/TESTING.md`, fixed) and coding-standards /
     patterns (`<root>/.agent-workflow/plans/reference/coding-standards.md`,
     else `<root>/mobile/CLAUDE.md`). Write `none found` only after checking.

   If any OPERATOR-SUPPLIED placeholder cannot be filled honestly from this
   session, **stop and ask the operator**. Do not invent scope items, label
   sets, or dependencies — missing items are often what the reviewer should
   flag.

3. **Emit the populated prompt verbatim in chat.** Use a
   `## Plan Review Kickoff Prompt` heading immediately followed by a
   ```text fenced block containing the full populated prompt. This must
   appear in chat **before** any reviewer subagent is spawned.

4. **Spawn exactly one fresh-context reviewer subagent** with that prompt
   verbatim. Use whichever subagent mechanism the host agent has available
   (Agent tool, subagent invocation, etc.). Announce `spawning one plan
   reviewer` so the operator sees the handoff. If the host environment has
   no subagent capability, emit the prompt and explicitly tell the operator
   to launch the reviewer manually.

5. **Tell the operator** that the same populated prompt is in the chat
   block above for their second independent reviewer, which they can
   launch in a separate Claude or Codex session, or in another tool. Do
   **not** spawn a second reviewer in this session unless the operator
   explicitly asks.

## Failure modes to avoid

- **Paraphrasing the template.** Copy headings and sections from
  KICKOFFS.md exactly. Reviewers downstream expect that shape.
- **Inventing placeholders.** If the spec doesn't claim specific files,
  doesn't have explicit non-goals, or doesn't list dependencies, say so —
  don't fabricate them.
- **Spawning the reviewer before emitting the prompt in chat.** The chat
  block is the operator's record and their handoff to the second reviewer.
- **Spawning more than one reviewer** from this skill. The second review
  is operator-owned by default.
- **Reviewing a non-plan artifact.** This skill is for plans and specs. For
  implemented code, use [[cjcreview]] instead.
