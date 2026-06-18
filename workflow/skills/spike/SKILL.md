---
name: spike
description: Prove (or reject) one chosen architectural bet at the real boundary
  before committing to it — read-only, disposable, GO/NO-GO. Frames the single
  sharp question + go/no-go criteria up front, writes a bounded spike spec, runs
  the proof against the RISKIEST assumption at the REAL boundary (never a green
  mock standing in for the core bet), verifies falsifiably against an oracle,
  adversarially tries to refute it, and writes proof notes with a verdict that
  feeds the plan (GO → seed the implementation spec; NO-GO → recommend the
  fallback). Disposable by default — no production code, no branch, no tracker
  or provider/hosted mutation; web search encouraged. Use when the operator says
  /spike, "prove <approach> works", "can <mechanism> actually do X", "spike the
  <X> coupling", or after explore recommends proving a bet. Not for mapping
  approaches (that is explore) or researching a fresh bug (that is spec).
---

# spike

The proof phase: you are holding one chosen but **unproven** bet — an unfamiliar
mechanism, a fragile coupling, a "can this even work?" — and you prove or reject
it at the real boundary before any durable work depends on it. Distinct from
`explore` (which maps and ranks approaches) and from implementation (which is
durable): a spike is throwaway. Read-only and disposable by default; the
Destructive Action Policy applies to anything beyond that.

## When invoked

1. **Frame the bet + GO/NO-GO up front.** State the single sharp question (the
   *riskiest* assumption, not the easy plumbing), what "proven" concretely means,
   the time/scope box, and the fallback if it fails. The go/no-go criteria are
   written *before* the proof runs, so the result can't be rationalized after.

2. **Write the spike spec** (the BEFORE artifact, in the work-item folder root,
   e.g. `<TOPIC>_SPIKE.md` / `<TOPIC>_SPIKE_SPEC.md`, PLANS.md frontmatter with
   `status: rough`/`review-ready` and a `parent_spec` / `related` link back to the
   README and any `*_OPTIONS.md`). Shape, from the operator's
   proven pattern: header guardrail ("no production code, no branch, local-only
   read-only proof"); Question/Goal & Non-Goals; **Risks & Edge Cases** (the
   failure modes the proof must surface); **Existing Code Path Claims** (file:line
   grounding); a numbered **Proof Plan** naming *which boundary* each step uses;
   tight In/Out of Scope; **boundary-aware Acceptance Criteria** ("config/mock
   tests do not stand in for live proof of ordering"); a Verification Plan; and
   explicit **GO/NO-GO** ("choose X if… stay on the fallback if…").

3. **Run the proof — disposable, read-only.** Build only throwaway scaffolding and
   remove it after: `/tmp` outputs, temporary plugins/fields, local-only
   DB/index, read-only source inspection and API probes. For runtime queries,
   prefer a re-runnable local-only proof script under `artifacts/` (the repo's
   `.mjs` proof-harness pattern) that asserts every target is local *before*
   querying, fail-fast asserts, writes a JSON report beside it, and leaks no
   secrets — a re-runnable artifact beats a one-shot terminal session. Do NOT
   touch production code, create a branch, mutate the tracker, or touch
   provider/hosted state; a local-only mutation on disposable state (a local
   migrate:run/revert, a temporary local server) is done only with operator
   approval and recorded as such. **Use web search freely** to prove against
   CURRENT external behavior — engine/provider/library docs, version-specific
   limits, known issues; cite the version/source when a GO/NO-GO rests on it.

4. **Boundary honesty — prove the bet where it actually lives.** Tag every proof
   piece with its boundary: source-inspection / mocked-boundary / live-local. The
   **core bet must be proven at the real boundary**; a green mocked suite proves
   plumbing (clause construction, delegation, wiring), NOT the bet (real ordering,
   grouping, persistence, coupling under the live engine). Say which is which.

5. **Verify falsifiably, then try to refute.** The proof must be able to FAIL:
   compare against an oracle (existing behavior, the real index, a known-good
   baseline) rather than self-confirming with the same incomplete constraints. If
   the proof reconstructs a query or params, prove parity against the *existing*
   production path (or the plugin's own param builder) as the oracle — not against
   your own reconstruction with the same constraints. Then adversarially attack
   the bet — "could not refute at the real boundary" is the GO bar, not "the happy
   path returned something".

6. **Write proof notes** (the AFTER artifact, e.g.
   `artifacts/<topic>-proof-notes.md`): a **Scope** statement of what was
   deliberately *not* touched (durable code, provider state); per-piece
   **Verdicts** with their boundary ("blocked" / "adjust plan, then proceed");
   the recommended next implementation slice; and **parked contracts** — concrete
   deferred designs (a function signature, a config shape, a migration plan), not
   a vague note. Do not claim a gate proved something it skipped (a command that
   exits 0 while skipping the real work is not proof).

7. **Verdict + hand back.** GO → update/seed the implementation spec with the
   proven approach and parked contracts, and recommend `/specreview`. NO-GO →
   recommend the fallback (from `explore` or the spec) and record why. **Narrowed
   GO** — when the core bet holds at the reachable boundary but one piece couldn't
   be proven safely (e.g. the live service call needs bootstrap writes), record
   the partial verdict, name exactly what stays unproven, and make that residual
   proof the first gate of the implementation phase (a narrowed GO is honest;
   claiming source-inspection proved the live boundary is not). If the bet did not
   prove out within the box, that itself is a NO-GO/escalate signal — don't keep
   digging silently. Do NOT auto-invoke specreview or start implementation; the
   GO/NO-GO direction is the operator's to act on.

## Guardrails

- Disposable & read-only by default: throwaway scaffolding removed after; no
  production code, branch, tracker mutation, or provider/hosted state. Local-only
  mutations on disposable local state need an operator OK and a note; hosted/
  staging/prod reindex, migrate, deploy, or seed are operator-gated, never run by
  the agent.
- Local-target is not side-effect-free: even against a local stack, bootstrapping
  a service or hitting an init path can create keys, write global settings, or
  mutate local config. Confirm the path is side-effect-free or guard it before any
  runtime service call; if you can't, narrow the GO to source-proven coupling and
  defer the live service-call proof to the implementation phase.
- Prove the riskiest assumption at the real boundary; never let a green mock
  stand in for the core bet, and name each proof's boundary.
- The proof must be falsifiable against an oracle — a result that can't fail
  isn't proof.
- Honor the box: if it won't prove out in the stated time/scope, call NO-GO or
  escalate rather than expanding the spike into an implementation.

## Failure modes

- Claiming a green mocked/unit suite as proof of the core bet — it proves
  plumbing, not the live behavior. The riskiest assumption stays unproven.
- A self-confirming proof: the "oracle" uses the same incomplete constraints as
  the thing under test, so it can't fail.
- A green exit that skipped the real work — e.g. a reindex that exits 0 but never
  touched the live index, or an e2e that passed against a mock. Inspect the output
  and confirm the boundary actually ran; a zero exit code is not proof.
- Proving the easy part (delegation, clause construction) and quietly leaving the
  actual risk (live ordering, coupling, persistence) untested.
- Leaving durable changes behind: a branch, an uncommitted production edit, or
  scaffolding not removed.
- Running a hosted/provider mutation, or a local data mutation, without approval.
- Digging past the box instead of calling NO-GO; or sliding from proof into
  implementation.
- Re-mapping approaches instead of proving the chosen one — that is `explore`.
