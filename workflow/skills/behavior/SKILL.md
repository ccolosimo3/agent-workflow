---
name: behavior
description: Give the operator a concise, source-grounded summary of the behavior
  planned in a spec or delivered by an implemented work item, including the
  load-bearing design decisions and why they were made. Use when the operator
  explicitly invokes /behavior or asks for a focused behavior summary of a
  spec, current branch, PR, commit range, or work item. Not for restating the
  last response (plain), a deep briefing with Q&A (learn), or reviewing the work.
---

# behavior

Explain what the work does and why it takes this shape. Stay at the product and
system-behavior level rather than walking through files or implementation trivia.
Remain read-only.

## Ground the summary

1. Resolve the target from the operator's pointer. If none is given, use the
   active work item or current branch when it is unambiguous; otherwise ask for
   the spec, branch, PR, range, or work-item path.
2. Determine the source of truth:
   - **Planned:** read the complete spec and its recorded decisions. Describe
     proposed behavior in future tense.
   - **Implemented:** inspect the actual diff or commit range, plus its spec when
     available. Treat delivered code as authoritative and describe current
     behavior.
3. State only rationale supported by the source or clearly evidenced by the
   constraints. Label a useful inference; never invent a polished rationale.
4. If implementation materially differs from the spec, summarize the delivered
   behavior and note the meaningful divergence in one sentence.

## Respond

Keep the default response under roughly 300 words:

- **What we're building / built** — 2–4 sentences covering the problem, the
  resulting behavior, and who or what experiences it.
- **How it behaves** — 3–5 bullets describing the important flow, including only
  the boundary or failure behavior needed to understand the feature.
- **Why this approach** — 2–4 bullets naming the load-bearing decisions and
  their concise rationale. Mention a rejected alternative only when it clarifies
  a real tradeoff.
- **Status** — one line: `Planned` or `Implemented`, plus any material
  source-of-truth limitation.

Do not include a file inventory, acceptance-criteria dump, verification log,
review history, generic benefits, speculative future work, likely Q&A, or an
invitation to drill down unless the operator asks.
