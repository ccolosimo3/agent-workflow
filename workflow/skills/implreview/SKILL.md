---
name: implreview
description: Hand off a completed implementation for review. Reads the canonical
  Review Kickoff template from ~/.agents/workflow/KICKOFFS.md, populates every
  placeholder from the current session, then spawns exactly one fresh-context
  reviewer subagent with it (announcing the handoff; the prompt is emitted in
  chat only as a no-subagent fallback). Use after completing an
  implementation when the operator says /implreview, "hand this off for review",
  "let's review this", or similar.
---

# implreview

The implementer session's trigger for the kernel's "Implementation Completion
Handoff". Shared mechanics live in `~/.agents/workflow/HANDOFF.md` — apply
that protocol with the parameters below; this file adds only the
implreview-specific population rules.

## Protocol parameters

- Template: `## Review Kickoff` in `~/.agents/workflow/KICKOFFS.md`
- Emitted heading (no-subagent fallback): `## Review Kickoff Prompt`
- Announce: `spawning one reviewer`
- Spawns: yes — one fresh-context reviewer (except emit-only mode below)

## Population specifics

- **Work item**: issue/spec link + acceptance criteria copied inline as
  `- [ ]` bullets, as they appear in the source issue.
- **Implementer summary**: 2-3 sentences naming what changed and why.
- **Review range**: `<base>..<tip>` SHAs (base = merge-base with the target
  branch, tip = HEAD). The implementation must be committed first.
- **Scope**: in-scope as a 1-2 sentence summary (do NOT enumerate file paths —
  the reviewer derives them from `git diff --stat`); out-of-scope items +
  reason; discovered follow-ups to capture as separate issues.
- **Verification run**: each command paired with a one-line result including a
  useful number (e.g. `<typecheck command>: 0 errors across 412 files`,
  `<test command>: 318 pass / 0 fail`), using the repo's real commands from
  its shim/verification doc.
- **Hot spots / known risk**: deviations from spec, assumptions, focus areas.
- **Tier 4 gate**: yes/no; if yes, name what and who runs it.
- **Original operator request / intent (field 2a)**: the verbatim or
  closely-paraphrased ask that triggered the work — the reviewer compares the
  diff against THIS, not only the acceptance criteria, to catch unrequested
  approach substitutions.

## Emit-only mode

When the operator says `/implreview emit-only` (or "emit the kickoff only",
"prepare the second-review prompt"): re-populate from the CURRENT state —
fresh SHAs, never a reuse of an earlier emitted prompt — and emit without
spawning. Use after the inner loop converges to hand the outer-gate reviewer a
fresh prompt (HANDOFF.md sequencing + freshness rules). Prefer the
`secondreview` skill in the other app when available — it self-populates and
needs no paste.

## Scope guard

Work absorbed silently beyond the acceptance criteria goes in "discovered
follow-ups" — do not expand the kickoff to retroactively justify it. Scope
creep includes SUBSTITUTION, not only addition: an acceptance criterion met by
swapping a component, library, primitive, algorithm, or data path the work
item did not name goes in Hot spots as "approach substitution: <old> -> <new>,
not explicitly requested", flagging any preserved identifier (testid, route,
public name) whose implementation changed underneath it.

## After convergence

Disposition is owned by the implementer directive appended to each verdict
(REVIEW_RUBRIC.md) plus the Execution Kickoff re-review trigger — not by this
skill. On an inner-loop APPROVED, report the result with a one-line-per-pass
changelog and note the loop converged. The next step is the operator-owned
`secondreview` outer gate (required unless waived per the kernel's
"Implementation Completion Handoff" off-ramp); this skill does NOT auto-invoke
it.

## Failure modes

The shared ones in HANDOFF.md, plus: inventing verification numbers, scope
items, risks, or acceptance criteria — if an operator-supplied placeholder
cannot be filled honestly from this session, stop and ask first.
