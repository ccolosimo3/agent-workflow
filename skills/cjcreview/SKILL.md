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
   reviewer agents. The Review Kickoff is intentionally short and points the
   reviewer at `~/.agents/workflow/REVIEW_RUBRIC.md` (the standing reviewer
   manual: stance, required investigation, output contract, severity rubric).
   Do NOT inline the rubric into the emitted prompt — the spawned reviewer reads
   it itself, so confirm the reviewer subagent can reach that path.

2. **Populate every placeholder** from the current session:

   - **Work item**: issue/spec link (URL or path) + acceptance criteria
     copied inline as `- [ ]` bullets, as they appear in the source issue.
   - **Implementer summary**: 2-3 sentences naming what changed and why.
   - **Review range**: `<base>..<tip>` SHAs (base = merge-base with the target
     branch, tip = HEAD); the reviewer diffs that range from git. The
     implementation must be committed first (Execution Kickoff step 8).
   - **Scope**:
     - in scope: 1-2 sentence summary of the change (do NOT enumerate file
       paths — the reviewer derives them from `git diff --stat <base>..<tip>`)
     - out of scope, noticed but intentionally not touched: items + reason
     - discovered follow-ups: items to capture as separate issues
   - **Verification run**: each command paired with a one-line result
     including a useful number (e.g. `bun run typecheck: 0 errors across
     412 files`, `bun test: 318 pass / 0 fail`).
   - **Hot spots / known risk**: deviations from spec, assumptions made,
     areas where the reviewer should focus extra attention.
   - **Tier 4 gate**: required yes/no; if yes, name what (manual QA,
     hardware, live provider) and who runs it.
   - **Original operator request / intent (field 2a)**: the verbatim or
     closely-paraphrased ask that triggered this work (e.g. "stronger shimmer
     on the skeleton"). The reviewer compares the diff against THIS, not only
     the acceptance criteria, to catch unrequested approach substitutions.
   - **Repo conventions to enforce (fill this from the FILESYSTEM, not from
     operator memory; the stop-and-ask rule below does not apply to it)**:
     detect the repo root under review and resolve the real, existing paths the
     reviewer must load, writing `none found` for a doc only after checking:
     - testing-philosophy:
       `<root>/.agent-workflow/plans/reference/testing-philosophy.md` or
       `<root>/plans/reference/testing-philosophy.md`
     - coding-standards / patterns:
       `<root>/.agent-workflow/plans/reference/coding-standards.md`, else the
       subtree conventions doc (e.g. `<root>/mobile/CLAUDE.md`)
     - verification policy:
       `<root>/.agent-workflow/plans/reference/townchest-pr-checklist.md` or
       `<root>/mobile/VERIFICATION.md`
     - local shim: `<root>/AGENTS.local.md` or `<root>/mobile/CLAUDE.md`
     - automated review: whether `<root>/.coderabbit.yaml` exists; if so, list
       its path-exclusion globs so the reviewer knows which surfaces (e.g.
       migrations) get NO automated coverage.

   If any OPERATOR-SUPPLIED placeholder cannot be filled honestly from this
   session, **stop and ask the operator**. Do not invent verification numbers,
   scope items, risks, or acceptance criteria.

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

Scope creep includes SUBSTITUTION, not only addition: if an acceptance
criterion was met by swapping a component, library, primitive, algorithm, or
data path the work item did not name, surface it in the "Hot spots" block as
"approach substitution: <old> -> <new>, not explicitly requested", and flag any
preserved identifier (testid, route, public name) whose implementation changed
underneath it — a preserved id can mask the swap from existing tests.
