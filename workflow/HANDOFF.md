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
- Then: finalize spec → `specreview` / `specrereview` (autonomous loop), with an
  optional `outerspecreview` outer gate (other model) on the converged plan →
  implement → `implreview` / `implrereview` (loop) → adaptive `outerreview` or
  explicit coordinated `large-pr-review` outer gate
- Implementation review handoff → `implreview` (announce + spawn; emit-only mode
  for outer-gate handoffs)
- Implementation re-review after patches → `implrereview`
- Plan/spec review before promotion → `specreview`
- Plan re-review after revisions → `specrereview`
- Outer-gate second review of the operator's own implementation, run in the
  other app/model → `outerreview` (adaptive serial/coordinated routing)
- Explicit always-coordinated implementation outer gate for a broad PR/branch →
  `large-pr-review`
- Outer-gate second review of the operator's own converged plan/spec, run in the
  other app/model → `outerspecreview`
- Coworker PR review + calibration → `prreview` (+ `calibrate-review`)

## The protocol

1. **Template fidelity.** Read the named `~/.agents/workflow/kickoffs/<name>.md`
   template file and paste it verbatim with placeholders
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
   - If the skill REUSES the original reviewer (a re-review, per §6): resume its
     session and hand it only the patch/revision summary + any findings it did not
     author — do NOT re-pass the full kickoff or re-populate. The full-kickoff
     spawn is the fallback.
   - If the skill IS the reviewer (the conversation itself — the outer gates):
     follow the "Outer-gate protocol" below — self-populate the kickoff as
     INTERNAL orientation and do NOT print it back in chat; the verdict return
     (not the kickoff) is the record of what was reviewed.
5. **Exactly one verdict owner.** Spawn (or, for an outer gate, run) exactly one
   fresh-context reviewer — except a re-review, which REUSES the original per §6.
   Coordinated implementation outer-review mode may give bounded lanes to direct,
   read-only evidence scouts; they never issue verdicts and do not count as extra
   reviewers. Never add a second verdict owner unless the operator explicitly asks.
6. **Re-reviews reuse, don't re-spawn.** A re-review (`implrereview` /
   `specrereview`) is a narrow delta check — "were the findings addressed, and did
   the patch break anything else?" — so leave the ORIGINAL reviewer's session open
   and hand it the patch/revision summary; it already holds the diff, the rubric,
   its own findings, and the reasoning, so reuse it (resume that reviewer thread the
   way your host does — e.g. send it a follow-up message rather than starting a new
   one) with NO reload of the diff, rubric, or findings. Fall back to a fresh
   re-reviewer (full populated Re-Review Kickoff) ONLY when the original can't be
   resumed — a later session, a compacted context, or a host that can't resume
   subagents. When re-reviewing against findings the reviewer did NOT author
   (outer-gate findings routed back per Sequencing), reuse the thread but hand it
   those findings verbatim. Reuse ≠ rubber-stamp: still apply `REVIEW_RUBRIC.md`
   "Re-review mode" — confirm the fix actually works (the reverse-tautology check),
   not just that your suggestion was applied. Independence is already secured by the
   fresh FIRST review and the fresh, different-model OUTER gate; the inner re-review
   need not re-earn it. The outer gate NEVER reuses: it independently derives a full
   review from current first-party sources.
7. **The second review is operator-owned** — see sequencing below.

## Sequencing — inner loop, then outer gate

- **Inner loop** (implementer's app): `implreview` → patch → `implrereview`,
  repeat until APPROVED. Fast, same-app subagents; iterate freely.
- **Outer gate** (the other app/model): ONE fresh-context verdict on the FINAL
  tip — via adaptive `outerreview`, explicit coordinated `large-pr-review`, or a
  pasted emit-only kickoff. A different model decorrelates blind spots; this
  review certifies the candidate that will actually be PR'd.
- Do not run the outer gate in parallel with the inner loop by default: a
  verdict on a pre-patch tip cannot certify the final tip, so parallel runs
  guarantee stale findings or a repeat review. Deliberate exception: for
  big/risky changes an early outside review may run for directional signal —
  it does NOT count as the certifying second verdict.
- Outer-gate findings: paste the verdict into the implementer session, patch,
  and run `implrereview` quoting those findings verbatim. The kernel's
  two-verdicts gate is met when both lenses have approved the final tip;
  patches landed after any approval get a re-review — except a nit-only patch (naming,
  comment, dead code, copy) that changes no logic, contract, or behavior: it keeps the
  approval and is just noted at handoff. Anything beyond a nit takes the normal
  re-review path. The carve-out exists so low findings aren't silently dropped to
  protect a certified tip.

## Outer-gate waivability

The inner review loop is never skippable (kernel review floor). The outer gate —
satisfied by adaptive `outerreview` or explicit `large-pr-review` — is REQUIRED
whenever the diff touches any item on the canonical risk-surface list in the
kernel's Implementation Completion Handoff (its single owner; there
migration/schema/persisted-state covers any change to stored data or a
state-machine, and provider boundary covers Stripe, AvaTax, and other external
services) OR the inner review returned ACTIONABLE on any substantive finding at
any point in the loop. It is operator-waivable ONLY when ALL of:

- (a) the diff touches NONE of the canonical risk-surface list above;
- (b) the inner review was APPROVED on the FIRST pass with zero substantive
  findings (no ACTIONABLE cycle at all — a patched-then-clean loop does NOT
  qualify);
- (c) the diff is mechanically trivial — NO logic or control-flow change (copy,
  comment, pure rename, or a purely non-behavioral config value; a config value
  that changes runtime behavior — a threshold, retry count, rate limit — IS a
  logic change and does NOT qualify).

The implementer states `outer gate: required | waivable — <one-line why>` at
handoff; the OPERATOR makes the final waive call. When the outer gate is
mandatory, do not trim the independence seal, live-range self-computation, or the
inner loop. (`outerspecreview` is already optional on the spec side, so this
parity holds there too.)

## Outer-gate protocol

The shared procedure the outer-gate skills (`outerreview`, `large-pr-review`, and
`outerspecreview`) run. An outer gate is not a handoff — the conversation itself
owns the review — so it diverges from the spawn/emit protocol above:

1. **The conversation IS the verdict owner.** Review here per
   `REVIEW_RUBRIC.md` (and, for `outerspecreview`, the Spec Review Kickoff
   validation categories). Serial `outerreview` and `outerspecreview` do not
   spawn. Coordinated code-review mode may spawn only the bounded, read-only
   evidence scouts defined by `large-pr-review`; the lead validates their claims
   and issues the sole verdict.
2. **Self-populate, never from a paste.** Build the kickoff from the filesystem
   (the work-item folder / spec file) + the live git range computed at invocation
   time — NEVER from a prompt pasted by the operator or a prior session. A stale
   tip is the failure mode: a paste can encode a SHA the tree has moved past, and
   an outer gate must certify the actual final tip.
3. **Independence seal.** Do not intentionally seek or rely on prior findings,
   verdicts, kickoff prompts, or `reviews.md`; the operator must not paste them in.
   Accidental exposure is recoverable, not a stop condition: stop reading that
   material, quarantine its claims, continue the full review from first-party
   sources, independently prove any overlapping finding, and disclose the exposure
   in the verdict.
4. **The populated kickoff is INTERNAL orientation.** Do NOT print it back to the
   operator or pass it to scouts; coordinated scouts receive only their canonical
   lane kickoff. The lead's verdict return — not the kickoff — is the record of
   what was reviewed.
5. **Carry-back return shape.** Return, for the operator to paste into the
   implementer/planning session: the strict verdict line; the exact range (or spec
   section) reviewed; the findings; and a verified-clean record naming the checks
   actually run.
6. **Strict verdict.** Emit a strict `APPROVED`/`ACTIONABLE` verdict; do NOT
   soften it into a calibrate-review-style advisory brief. An early or directional
   read (the Sequencing deliberate exception) never counts as the certifying
   verdict.

## Spec review loop (specreview → specrereview)

Spec review is autonomous and has NO operator-owned outer gate (unlike the
implementation flow above). `specreview` spawns one reviewer; the planning agent
resolves the autonomous findings by tightening the spec and re-runs
`specrereview` (reusing the original reviewer across cycles per §6, fresh only as
fallback), looping until APPROVED. It STOPS for
the operator only on a plan-DIRECTION finding (`[decision-required]`, or any the
planner cannot resolve without choosing an approach / scope / tradeoff / policy —
applied as a self-filter, not just the reviewer's tag) or after a 3-cycle cap.
Full disposition lives in the `specreview` skill.

## Freshness

A kickoff is stale the moment its tip SHA is no longer HEAD. Never hand a
reviewer a stale kickoff — re-populate and re-emit (`implreview` emit-only), or
use `outerreview` / `large-pr-review`, which compute their own range at invocation
time.

## Independence seal

The outer-gate reviewer independently derives its verdict from current source,
tests, spec, and live range. It does not intentionally seek or rely on prior
findings, verdicts, kickoff prompts, or `reviews.md`, and the operator should not
paste them into the outer-gate conversation. Accidental exposure does not
invalidate the gate or require a fresh task; apply the recovery rule above and
continue. A pristine blind rerun happens only when the operator explicitly asks
for one. Re-reviews are the deliberate opposite: they REQUIRE the prior findings,
quoted verbatim.

## Shared failure modes

- Inventing placeholder content instead of stopping to ask.
- Spawning without announcing the handoff; or, for an outer gate, not emitting
  the record of what was reviewed.
- Spawning more than one verdict owner, or allowing an evidence scout to issue or
  determine the verdict.
- Handing off a kickoff whose SHAs the tree has since moved past.
