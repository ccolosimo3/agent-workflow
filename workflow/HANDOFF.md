# HANDOFF.md — Shared Review-Handoff Protocol

One protocol for all review/re-review handoffs — and, since the kernel points
here for it, the full ritual→skill index (which also covers the non-handoff
planning ritual). The handoff skills parameterize the protocol; in hosts
without skill support, apply it by hand from this file. Canonical
templates live in `KICKOFFS.md`; the reviewer manual is `REVIEW_RUBRIC.md`;
testing doctrine is `TESTING.md`; the handoff requirements themselves are the
kernel's "Implementation Completion Handoff".

## Ritual → skill index

The planning/build phases form a DAG (not a loop); the operator owns each
phase transition (those are the direction decisions). Review loops *within* a
phase are autonomous.

- Planning kickoff for a tracker issue (research the problem → root cause →
  spec) → `spec`
- Map & rank candidate approaches for an open question / a working-but-imperfect
  system → `explore` (hands off to `spike` if the chosen approach carries an
  unproven bet, else to `specreview`)
- Prove one chosen approach at the real boundary (GO/NO-GO) → `spike` (hands off
  to `specreview` on GO; recommends the fallback on NO-GO)
- Then: finalize spec → `specreview` / `specrereview` (autonomous loop), with an
  optional `secondspecreview` outer gate (other model) on the converged plan →
  implement → `implreview` / `implrereview` (loop) → `secondreview` outer gate
- Implementation review handoff → `implreview` (emit + spawn; emit-only mode
  for outer-gate handoffs)
- Implementation re-review after patches → `implrereview`
- Plan/spec review before promotion → `specreview`
- Plan re-review after revisions → `specrereview`
- Outer-gate second review of the operator's own implementation, run in the
  other app/model → `secondreview`
- Outer-gate second review of the operator's own converged plan/spec, run in the
  other app/model → `secondspecreview`
- Coworker PR review + calibration → `prreview` (+ `calibrate-review`)

## The protocol

1. **Template fidelity.** Read the named template section from
   `~/.agents/workflow/KICKOFFS.md` and paste it verbatim with placeholders
   filled (kernel Fidelity Rule). Never paraphrase, restructure, reorder, or
   invent a different shape — the structure is load-bearing for downstream
   agents. Do not inline `REVIEW_RUBRIC.md` into the prompt: the reviewer
   reads it itself; confirm the reviewer can reach that path.
2. **Populate honestly.** Fill every placeholder from the current session and
   the filesystem. If an OPERATOR-SUPPLIED placeholder cannot be filled
   honestly, stop and ask — never invent verification numbers, scope items,
   risks, findings, or acceptance criteria. Missing material is often exactly
   what the reviewer should flag.
3. **Repo conventions resolution** (fill from the FILESYSTEM, not operator
   memory; the stop-and-ask rule does not apply to this step). Resolve real,
   existing paths the reviewer must load:
   - testing: `~/.agents/workflow/TESTING.md` (fixed kernel path — Part 1/2
     principles + anti-patterns) plus the repo's stack section in its testing
     reference (resolve via the shim, e.g. `plans/reference/testing-philosophy.md`)
   - coding-standards / verification / checklist docs: the repo shim
     (`<root>/AGENTS.local.md` or the repo's CLAUDE/AGENTS adapter) names the
     repo's docs — resolve from it. Fallback when no shim names them: search
     `<root>/.agent-workflow/plans/reference/` and repo-root convention docs.
   - automated review: if `<root>/.coderabbit.yaml` exists, list its
     path-exclusion globs — excluded surfaces get NO automated coverage and
     the agent reviewer is the sole automated check there.
   - Write `none found` for a doc category only after checking.
4. **Hand off the populated prompt.**
   - If the skill SPAWNS a subagent reviewer: pass the full populated kickoff to
     the subagent and announce a one-line handoff in chat (what is being reviewed
     + the range/spec). Do NOT emit the full prompt verbatim — the operator opens
     the subagent to inspect it. Emit the full prompt in chat ONLY when the host
     has no subagent capability, then tell the operator to launch it manually.
   - If the skill IS the reviewer (the conversation itself — the outer gates):
     emit the populated kickoff verbatim in chat under a `## <Template-name>
     Prompt` heading as the record of what was reviewed (there is no subagent to
     inspect).
5. **Exactly one reviewer.** Spawn (or, for an outer gate, run) exactly one
   fresh-context reviewer; never a second unless the operator explicitly asks.
6. **The second review is operator-owned** — see sequencing below.

## Sequencing — inner loop, then outer gate

- **Inner loop** (implementer's app): `implreview` → patch → `implrereview`,
  repeat until APPROVED. Fast, same-app subagents; iterate freely.
- **Outer gate** (the other app/model): ONE fresh-context review of the FINAL
  tip — via `secondreview`, or via a pasted emit-only kickoff. A different
  model decorrelates blind spots; this review certifies the candidate that
  will actually be PR'd.
- Do not run the outer gate in parallel with the inner loop by default: a
  verdict on a pre-patch tip cannot certify the final tip, so parallel runs
  guarantee stale findings or a repeat review. Deliberate exception: for
  big/risky changes an early outside review may run for directional signal —
  it does NOT count as the certifying second verdict.
- Outer-gate findings: paste the verdict into the implementer session, patch,
  and run `implrereview` quoting those findings verbatim. The kernel's
  two-verdicts gate is met when both lenses have approved the final tip;
  patches landed after any approval get a re-review.

## Spec review loop (specreview → specrereview)

Spec review is autonomous and has NO operator-owned outer gate (unlike the
implementation flow above). `specreview` spawns one reviewer; the planning agent
resolves the autonomous findings by tightening the spec and re-runs
`specrereview` (a fresh reviewer per cycle), looping until APPROVED. It STOPS for
the operator only on a plan-DIRECTION finding (`[decision-required]`, or any the
planner cannot resolve without choosing an approach / scope / tradeoff / policy —
applied as a self-filter, not just the reviewer's tag) or after a 3-cycle cap.
Full disposition lives in the `specreview` skill.

## Freshness

A kickoff is stale the moment its tip SHA is no longer HEAD. Never hand a
reviewer a stale kickoff — re-populate and re-emit (`implreview` emit-only), or
use `secondreview`, which computes its own range at invocation time.

## Independence seal

The outer-gate reviewer must not see prior findings: `secondreview` never
reads `reviews.md` or prior verdicts/kickoff prompts, and the operator should
not paste inner-loop findings into the outer-gate conversation. Re-reviews are
the deliberate opposite: they REQUIRE the prior findings, quoted verbatim.

## Shared failure modes

- Paraphrasing the template — downstream agents depend on the exact shape.
- Inventing placeholder content instead of stopping to ask.
- Spawning without announcing the handoff; or, for an outer gate, not emitting
  the record of what was reviewed.
- Spawning more than one reviewer from a single skill invocation.
- Handing off a kickoff whose SHAs the tree has since moved past.
