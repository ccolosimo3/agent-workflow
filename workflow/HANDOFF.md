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
   subagents. When re-reviewing against findings the reviewer did NOT author
   (outer-gate findings routed back per Sequencing), reuse the thread but hand it
   those findings verbatim. Reuse ≠ rubber-stamp: still apply `REVIEW_RUBRIC.md`
   "Re-review mode" — confirm the fix actually works (the reverse-tautology check),
   not just that your suggestion was applied. Independence is already secured by the
   fresh FIRST review and the fresh, different-model OUTER gate; the inner re-review
   need not re-earn it. An outer follow-up re-review also reuses its original
   conversation when the operator asks it to verify patches from its own verdict;
   only the first outer pass must begin fresh and blind.
7. **Required outer review is autonomous; waivers are operator-owned** — see
   sequencing below.

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
- **Outer gate** (the other app/model): ONE fresh-context review of the FINAL
  tip. After the inner loop converges, a non-Claude implementer launches
  `outerreview` in Claude Code per "Automated Claude outer gate" below. If
  Claude implemented the work, use a fresh other-model task instead.
- Do not run the outer gate in parallel with the inner loop by default: a
  verdict on a pre-patch tip cannot certify the final tip, so parallel runs
  guarantee stale findings or a repeat review. Deliberate exception: for
  big/risky changes an early outside review may run for directional signal —
  it does NOT count as the certifying second verdict.
- Outer-gate findings: patch in the implementer session, run `implrereview`
  quoting those findings verbatim, then resume the same outer-review
  conversation against the patched live tip. The kernel's two-verdicts gate is
  met when both lenses have approved the final tip; patches landed after any
  approval get a re-review.

## Automated Claude outer gate

For a required gate after inner approval, require Claude Code 2.1.219+, confirm
a clean committed tip and current Outer-review verification receipt, then
announce the selected review profile:

- **Opus 5 `high`** (`--model claude-opus-5 --effort high`) — bounded,
  ordinary work with few interacting contracts;
- **Opus 5 `xhigh`** (`--model claude-opus-5 --effort xhigh`) — substantive
  multi-file/risk-surface work or a substantive inner finding (default for
  complex implementation);
- **Fable 5 `high`** (`--model claude-fable-5 --effort high`) — exceptional
  large, hard-to-reverse, concurrency, migration, or security work with several
  interacting invariants. This is the escalation profile; do not choose it
  merely because an outer gate is required.

From the implementation worktree, run:

```bash
claude -p --output-format stream-json --verbose \
  --model <model> --effort <level> \
  --permission-mode auto \
  --add-dir <absolute-work-item-folder> \
  -- \
  "/outerreview Review <work item>. Worktree: <absolute root>. Spec: <absolute path or URL>. Verification receipt: <absolute path or in-prompt receipt>."
```

`--add-dir` is required when the local spec or receipt lives outside the
implementation worktree; omit it only when no external local path is needed.
Because the flag accepts multiple directories, keep it last and use the
explicit `--` terminator so it cannot consume the review prompt. The parent
app's permission mode does not carry into Claude Code: pass `auto` explicitly
so routine review actions run unattended behind Claude's safety classifier.

Monitor the event stream without interrupting it and provide concise progress
updates. Keep the `system/init` event's `session_id` and the final `result`
message. Pass no inner findings or verdicts on the first run. If ACTIONABLE,
patch, commit, run targeted verification, converge `implrereview`, then resume
from the same worktree:

```bash
claude -p --output-format stream-json --verbose --resume <session_id> \
  --model <same model> --effort <same level> \
  --permission-mode auto \
  --add-dir <same absolute work-item folder> \
  -- \
  "Re-review the patched live tip. Recompute it and verify your prior findings."
```

Repeat until both reviewers approve the same final tip. Honor normal Claude
permissions; never add a bypass flag. Auto-mode denial, missing CLI/auth/skill
access, or a permission failure is a blocker to report, not a reason to weaken
the gate. If Fable is unavailable or its safeguards block the benign review,
disclose that and use Opus 5 `xhigh`; never substitute silently.

## Outer-gate waivability

Except for the documentation-only off-ramp above, the inner review loop is not
skippable (kernel review floor). The outer gate (`outerreview`) is REQUIRED
whenever the diff touches a canonical risk-surface
(migration/schema/persisted-state (any change to stored data or a state-machine),
auth, contract/API, data-loss, security, provider boundary (Stripe, AvaTax, other
external services), dependency, toolchain) OR the inner review returned ACTIONABLE
on any substantive finding at any point in the loop. It is operator-waivable ONLY
when ALL of:

- (a) the diff touches NONE of the canonical risk-surface list above;
- (b) the inner review was APPROVED on the FIRST pass with zero substantive
  findings (no ACTIONABLE cycle at all — a patched-then-clean loop does NOT
  qualify);
- (c) the diff is mechanically trivial — NO logic or control-flow change (copy,
  comment, pure rename, or a purely non-behavioral config value; a config value
  that changes runtime behavior — a threshold, retry count, rate limit — IS a
  logic change and does NOT qualify).

The implementer states `outer gate: required | waivable — <one-line why>` at
handoff. Required gates launch autonomously after inner convergence; the OPERATOR
makes the final waive call on a waivable gate. When the outer gate is mandatory,
do not trim the independence seal, live-range self-computation, or the inner
loop. (`outerspecreview` is already optional on the spec side, so this parity
holds there too.)

## Spec review loop (specreview → specrereview)

Spec review is autonomous and has no required implementation-style outer gate.
`specreview` spawns one reviewer; the planning agent
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
