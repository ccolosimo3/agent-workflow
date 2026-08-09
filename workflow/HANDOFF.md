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
  launches `outerreview` in Claude Code per "Automated Claude implementation
  outer gate" below. If Claude implemented the work, use a fresh other-model task
  instead.
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

## Shared Claude CLI review launch

Claude-backed outer reviews share one launcher contract. Require Claude Code
2.1.219+ and normalize operator profile names exactly:

- **Opus 5 `high`** → `--model claude-opus-5 --effort high`;
- **Opus 5 `xhigh`** → `--model claude-opus-5 --effort xhigh`;
- **Fable 5 `high`** → `--model claude-fable-5 --effort high`.

For `outerspecreview`, omitted profile means Opus 5 `high`; an explicit named
profile overrides it. `outerreview` still selects among these profiles by
implementation complexity below. Do not silently remap an unsupported or
unrecognized model/effort request.

All scripted launches use `-p --output-format json`, pass
`--permission-mode auto` explicitly, and terminate variadic options with `--`
before the review prompt. Add `--add-dir <absolute folder>` only when the review
must read a local path outside the launch working directory; keep it last before
`--` so it cannot consume the prompt. The parent app's permission mode does not
carry into Claude Code.

Wait for the process without interrupting it. From the single JSON result, keep
the `session_id` and final `result`, and relay the complete verdict to the
calling session/operator. Never add a permission-bypass flag.

## Automated Claude implementation outer gate

For a required `outerreview` after inner approval, apply the shared launcher
contract above, confirm a clean committed tip and current Outer-review
verification receipt, then announce the selected review profile:

- **Opus 5 `high`** — bounded, ordinary work with few interacting contracts;
- **Opus 5 `xhigh`** — substantive multi-file/risk-surface work or a substantive
  inner finding (default for complex implementation);
- **Fable 5 `high`** — exceptional
  large, hard-to-reverse, concurrency, migration, or security work with several
  interacting invariants. This is the escalation profile; do not choose it
  merely because an outer gate is required.

From the implementation worktree, run:

```bash
claude -p --output-format json \
  --model <model> --effort <level> \
  --permission-mode auto \
  --add-dir <absolute-work-item-folder> \
  -- \
  "/outerreview Review <work item>. Worktree: <absolute root>. Spec: <absolute path or URL>. Verification receipt: <absolute path or in-prompt receipt>."
```

`--add-dir` is required when the local spec or receipt lives outside the
implementation worktree; omit it only when no external local path is needed.
Pass no inner findings or verdicts on the first run. If ACTIONABLE, patch only
the listed findings, commit, run targeted verification, then resume from the
same worktree:

```bash
claude -p --output-format json --resume <session_id> \
  --model <same model> --effort <same level> \
  --permission-mode auto \
  --add-dir <same absolute work-item folder> \
  -- \
  "Re-review the patched live tip. Recompute it and verify your prior findings."
```

Repeat until the outer reviewer approves the final tip. Honor normal Claude
permissions; never add a bypass flag. Auto-mode denial, missing CLI/auth/skill
access, or a permission failure is a blocker to report, not a reason to weaken
the gate. If Fable is unavailable or its safeguards block the benign review,
disclose that and use Opus 5 `xhigh`; never substitute silently.

## Claude spec outer gate

When "Spec review loop" below requires `outerspecreview`, or the operator asks
for it explicitly, a non-Claude planning session launches a fresh Claude Code
review with the shared contract above:

- no profile named → Opus 5 `high`;
- `Fable 5 high` → Fable 5 `high`;
- `Opus 5 xhigh` → Opus 5 `xhigh`;
- `Opus 5 high` → Opus 5 `high`.

From the repository root, after the inner spec-review loop has converged, run:

```bash
claude -p --output-format json \
  --model <mapped model> --effort <mapped level> \
  --permission-mode auto \
  --add-dir <absolute spec folder only when outside the repo root> \
  -- \
  "/outerspecreview <absolute spec path> — inner spec-review loop converged"
```

Omit `--add-dir` when the spec is already inside the repository root. Pass no
prior findings, verdicts, or populated kickoff. The launched Claude conversation
performs the skill's read-only holistic review and returns its verdict.

If ACTIONABLE, resolve any operator decisions, patch only changes directly
required by the listed outer findings, then resume the same Claude session for
re-review with the same model, effort, and directory access. Do not invoke
`specrereview` or start another fresh outer pass. If a required revision cannot
be mapped to a listed finding, report scope expansion; only the operator may
restart the inner → outer sequence. The inner approval certifies the plan
entering the gate; the outer follow-up certifies the revised plan.

When the current conversation is already Claude Code/Claude, run
`outerspecreview` directly here instead of recursively launching another Claude
process. An explicit operator request to review here likewise bypasses the CLI
launcher.

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

After inner convergence (APPROVED or the documented minor-only off-ramp), run
`outerspecreview` unless **every** compact-spec off-ramp condition holds:

- one localized, repo-conventional outcome within one surface;
- no new or changed architecture/product-policy choice, contract/API/schema,
  persisted-state/lifecycle/migration, auth/security, provider, dependency, or
  toolchain boundary;
- no cross-system coordination, rollout/cutover, unproven bet, or unresolved
  direction decision; and
- acceptance criteria and exact verification are straightforward and covered by
  known repository paths.

If all hold, skip automatically; otherwise launch the outer gate automatically
without pausing for a waiver decision. Report `outer spec gate: required |
skipped — <one-line reason>`. The operator may request it even when the compact
off-ramp applies.

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
