# HANDOFF.md — Shared Review-Handoff Protocol

One protocol for all review/re-review handoffs — and, since the kernel points
here for it, the full ritual→skill index (which also covers the non-handoff
planning ritual). The handoff skills parameterize the protocol; in hosts
without skill support, apply it by hand from this file. Canonical
templates live one-per-file in `kickoffs/`; the reviewer manual is `REVIEW_RUBRIC.md`;
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
- Then: finalize spec → `specreview` / `specrereview` (autonomous loop), with a
  risk-routed `outerspecreview` outer gate (other model) on the converged plan →
  implement → `implreview` / `implrereview` (loop) → `outerreview` outer gate
- Coworker PR review + calibration → `prreview` (+ `calibrate-review`)

## The protocol

1. **Template fidelity.** Read the named `~/.agents/workflow/kickoffs/<name>.md`
   template file and populate it verbatim with placeholders filled (kernel
   Fidelity Rule). Emit or pass it only as step 4 directs. Never paraphrase,
   restructure, reorder, or invent a different shape — the structure is
   load-bearing for downstream agents. Do not inline `REVIEW_RUBRIC.md` into
   the prompt: the reviewer reads it itself; confirm the reviewer can reach that
   path.
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
   - If the skill REUSES the original reviewer (a re-review, per §6): resume its
     session and hand it only the patch/revision summary + any findings it did not
     author — do NOT re-pass the full kickoff or re-populate. The full-kickoff
     spawn is the fallback.
   - If the skill IS the reviewer (the conversation itself — the outer gates):
     assemble the populated kickoff as internal orientation and do NOT emit it
     in chat. The outer gate's verdict and verified-clean summary are the concise
     record of what was reviewed.
5. **Exactly one reviewer.** Spawn (or, for an outer gate, run) exactly one
   fresh-context reviewer — except a re-review, which REUSES the original per §6.
   Never a second reviewer unless the operator explicitly asks.
6. **Re-reviews reuse, don't re-spawn.** A re-review (`implrereview` /
   `specrereview`) is a narrow delta check — "were the findings addressed, and did
   the patch break anything else?" — so leave the ORIGINAL reviewer's session open
   and hand it the patch/revision summary; it already holds the diff, the rubric,
   its own findings, and the reasoning, so reuse it (resume that reviewer thread the
   way your host does — e.g. send it a follow-up message rather than starting a new
   one) with NO reload of the diff, rubric, or findings. Fall back to a fresh
   re-reviewer (full populated Re-Review Kickoff) ONLY when the original can't be
   resumed — a later session, a compacted context, or a host that can't resume
   subagents. Re-review findings with the reviewer that authored them:
   outer-owned patches return only to the original outer conversation per
   Sequencing; do not route them through `implrereview` or `specrereview`.
   Reuse ≠ rubber-stamp:
   still apply `REVIEW_RUBRIC.md` "Re-review mode" — confirm the fix actually
   works (the reverse-tautology check), not just that your suggestion was
   applied. Only the first outer pass must begin fresh and blind.
7. **Required outer review is autonomous; otherwise skip it unless requested**
   — see sequencing below.

## Documentation-only off-ramp

Skip both review loops only when the entire diff contains non-generated,
non-normative documentation that records established facts, corrects prose, or
updates links/indexes. It must change no code, config, generated artifact,
contract, setup/command, verification or security policy, architecture, or
operating procedure, and must not be bundled with implementation changes.

Before PR handoff, check source fidelity, links/formatting, secrets/private-data
safety, and `git diff --check`, then record:
`review: skipped — docs-only self-check; no normative behavior or workflow changed`.
If any condition is uncertain, use the normal inner loop. Kernel/workflow policy
docs never qualify.

## Sequencing — inner loop, then outer gate

- **Inner loop** (implementer's app): `implreview` → patch → `implrereview`,
  repeat until APPROVED. Fast, same-app subagents; iterate freely.
- **Required outer gate** (the other app/model): ONE fresh-context review of the
  FINAL tip. When "Outer-gate requirements" selects it, a non-Claude implementer
  launches `outerreview` per `OUTER_REVIEW_LAUNCHER.md`. If Claude implemented
  the work, use a fresh other-model task instead.
- Do not run the outer gate in parallel with the inner loop by default: a
  verdict on a pre-patch tip cannot certify the final tip, so parallel runs
  guarantee stale findings or a repeat review. Deliberate exception: for
  big/risky changes an early outside review may run for directional signal —
  it does NOT count as the certifying second verdict.
- Outer-gate findings: patch only changes directly required by the listed
  findings, run targeted verification, then resume the same outer-review
  conversation. Do not invoke `implrereview`. If any required patch hunk cannot
  be mapped to a listed outer finding, report scope expansion; only the operator
  may restart the inner → outer sequence. The inner approval certifies the
  implementation entering the gate; the outer follow-up certifies the final tip.

Operator-facing completion starts with what changed, why it matters,
readiness/blocker, and any decision. Put detailed verification/review evidence
after that in the existing receipt or local owner, only when required or useful.

## Claude outer-review launcher

For a Claude-backed implementation or spec outer gate, read
`~/.agents/workflow/OUTER_REVIEW_LAUNCHER.md` in full. It owns supported
model/effort profiles, CLI flags, directory access, JSON/session handling,
launch syntax, failure behavior, and same-session resume. This file continues
to own whether and when the gate runs, independence, and patch routing.

## Outer-gate requirements

Except for the documentation-only off-ramp above, the inner review loop is not
skippable (kernel review floor). The outer gate (`outerreview`) is REQUIRED when:

- the diff touches migration/schema/persisted state (including a state-machine),
  auth, contract/API, data-loss, security, a provider boundary (Stripe, AvaTax,
  other external services), dependency, or toolchain; or
- an inner finding establishes a production-correctness, public/contract,
  persistence, security, or data-loss defect; or
- a test-quality finding requires a production behavior/contract patch because
  that behavior was not previously proven.

A receipt, documentation, assertion-only, redundant-test, or process finding
does not trigger the outer gate unless the diff independently touches a
canonical risk surface above. Otherwise skip the outer gate automatically; do
not stop for a waiver decision. The implementer states `outer gate: required |
skipped — <one-line why>` at handoff. The operator may still request an outer
review. When required, preserve the independence seal, live-range
self-computation, and inner loop.

## Spec review loop (specreview → specrereview)

Spec review is autonomous. `specreview` spawns one reviewer; the planning agent
resolves the autonomous findings by tightening the spec and re-runs
`specrereview` (reusing the original reviewer across cycles per §6, fresh only as
fallback), looping until APPROVED. It STOPS for
the operator only on a plan-DIRECTION finding (`[decision-required]`, or any the
planner cannot resolve without choosing an approach / scope / tradeoff / policy —
applied as a self-filter, not just the reviewer's tag) or after a 3-cycle cap.
Full disposition lives in the `specreview` skill.

After inner convergence (APPROVED or the documented minor-only off-ramp), require
`outerspecreview` only when the plan adds or changes architecture/product policy,
a contract/API/schema, persisted-state/lifecycle/migration, auth/security, a
provider/dependency/toolchain boundary, cross-system rollout/cutover, or a
material unproven bet. Otherwise skip automatically without asking for a waiver;
the operator may still request it. Report `outer spec gate: required | skipped —
<one-line reason>`.

## Freshness

A kickoff is stale the moment its tip SHA is no longer HEAD. Never hand a
reviewer a stale kickoff — re-populate and re-emit (`implreview` emit-only), or
use `outerreview`, which computes its own range at invocation time.

## Independence seal

The first outer-gate pass must not see prior findings: `outerreview` does not
read `reviews.md` or prior verdicts/kickoff prompts, and the caller must not pass
inner-loop findings into that first run. A follow-up in the same outer
conversation deliberately retains its own findings and re-reviews the patched
tip; it must not demand a fresh task. Other re-reviews likewise REQUIRE the
prior findings, quoted verbatim.

## Shared failure modes

- Paraphrasing the template — downstream agents depend on the exact shape.
- Inventing placeholder content instead of stopping to ask.
- Spawning without announcing the handoff; or, for an outer gate, not returning
  the verdict and concise verified-clean record.
- Spawning more than one reviewer from a single skill invocation.
- Handing off a kickoff whose SHAs the tree has since moved past.
