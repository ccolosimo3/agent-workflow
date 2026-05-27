---
name: cjcreview
description: Hand off a completed implementation for review. Reads the canonical
  Review Kickoff template from ~/.agents/workflow/KICKOFFS.md, populates every
  placeholder from the current session, emits the populated prompt verbatim in
  chat under a `Review Kickoff Prompt` block, then spawns exactly one
  fresh-context reviewer subagent with that prompt. Use after completing an
  implementation when the operator says /cjcreview, "hand this off for review",
  "let's review this", or similar.
---

# cjcreview

Automate the Implementation Completion Handoff defined in
`~/.agents/workflow/AGENTS.md` ("Implementation Completion Handoff" section).
This skill is the operator's one-step trigger for that handoff.

## When invoked

1. **Read the canonical template.** Open
   `~/.agents/workflow/KICKOFFS.md` and locate the `## Review Kickoff`
   section. Apply the AGENTS.md **Fidelity Rule**: paste the section verbatim
   with placeholders filled. Do not paraphrase, restructure, reorder, or
   invent a different shape. The structure is load-bearing for downstream
   reviewer agents.

2. **Populate every placeholder** from the current session:

   - **Work item**: issue/spec link (URL or path) + acceptance criteria
     copied inline as `- [ ]` bullets, as they appear in the source issue.
   - **Implementer summary**: 2-3 sentences naming what changed and why.
   - **Scope**:
     - in scope, files touched: list of paths
     - out of scope, noticed but intentionally not touched: items + reason
     - discovered follow-ups: items to capture as separate issues
   - **Verification run**: each command paired with a one-line result
     including a useful number (e.g. `bun run typecheck: 0 errors across
     412 files`, `bun test: 318 pass / 0 fail`).
   - **Hot spots / known risk**: deviations from spec, assumptions made,
     areas where the reviewer should focus extra attention.
   - **Tier 4 gate**: required yes/no; if yes, name what (manual QA,
     hardware, live provider) and who runs it.

   If any placeholder cannot be filled honestly from this session, **stop
   and ask the operator**. Do not invent verification numbers, scope items,
   risks, or acceptance criteria.

3. **Emit the populated prompt verbatim in chat.** Use a `## Review Kickoff
   Prompt` heading immediately followed by a ```text fenced block
   containing the full populated prompt. This must appear in chat **before**
   any reviewer subagent is spawned — see the
   "Implementation Completion Handoff" section of AGENTS.md, which makes
   this a hard output contract.

4. **Spawn exactly one fresh-context reviewer subagent** with that prompt
   verbatim. Use whichever subagent mechanism the host agent has available
   (Agent tool, subagent invocation, etc.). Announce `spawning one
   reviewer` so the operator sees the handoff in chat.

5. **Tell the operator** that the same populated prompt is available in the
   chat block above for their second independent reviewer, which they can
   launch in a separate Claude or Codex session, or in another tool. Do
   **not** spawn a second reviewer in this session unless the operator
   explicitly asks.

## Failure modes to avoid

- **Paraphrasing the template.** Copy headings and sections from KICKOFFS.md
  exactly. Reviewers downstream expect that shape.
- **Inventing placeholders.** If you don't have a real verification number,
  a real scope item, or a real hot spot, ask the operator first.
- **Spawning the reviewer before emitting the prompt in chat.** The chat
  block is the operator's record and their handoff to the second reviewer.
- **Spawning more than one reviewer** from this skill. The second review is
  operator-owned by default.

## Scope guard

If, while populating, you discover work outside the original acceptance
criteria that the implementer absorbed silently, list it in the
"discovered follow-ups" line of Scope so the operator can capture it as a
separate issue. Do not expand the kickoff prompt to retroactively justify
it.
