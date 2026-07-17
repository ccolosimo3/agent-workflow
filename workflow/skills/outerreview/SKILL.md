---
name: outerreview
description: Run the operator-owned outer-gate second review of their OWN
  implementation, in a fresh conversation in the other app/model, after the
  implementer session's review + re-review loop has converged. Self-populates
  the Review Kickoff and live range, then adaptively performs a serial review or
  coordinates bounded read-only evidence scouts when the diff has multiple
  coherent risk lanes. The current conversation remains the sole verdict owner
  and returns the strict REVIEW_RUBRIC verdict. Use when the operator says
  /outerreview, "second review this branch", or asks for the implementation
  outer gate. Not for coworker PRs (prreview) or the inner loop (implreview).
---

# outerreview

The outer gate of the two-review flow. Apply the shared
`~/.agents/workflow/HANDOFF.md` "Outer-gate protocol" for the mechanics every
outer gate shares — one verdict-owning lead, self-populate from filesystem + live
range (never a paste; staleness = failure), the independence seal, the populated
kickoff is INTERNAL orientation you do NOT print, the carry-back return shape,
and the strict verdict. This skill keeps only the code-review specifics below.
Its verdict certifies the final tip for the kernel's two-approved-verdicts gate.

## When invoked

Everything the outer gates share (independence seal, self-populate-never-paste,
kickoff-is-internal, carry-back shape, strict verdict) is in HANDOFF.md
"Outer-gate protocol"; the steps below are only the code-review specifics.

1. **Preflight (read-only).** `git status --short --branch` in the repo root
   (operator-given, or the current working directory). Do not switch branches
   or edit the working tree — it is the implementer's checkout. If the tree
   is dirty or the branch looks like it is mid-loop, stop and ask: this skill
   reviews a converged, committed candidate.
2. **Auto-detect the work item.** From the operator's pointer, or the branch's
   issue key → the repo's local plans folder (e.g.
   `<root>/.agent-workflow/plans/active/<ISSUE>-*/`). Read the spec
   (`README.md` acceptance criteria + implementation directions) and the
   folder's `verification.md` / `PR_BODY.md` if present. (The shared
   independence seal still applies — do not open `reviews.md` or prior
   verdicts. Do not use review-bearing receipt sections as verification logs.)
3. **Compute the live range yourself** (self-populate, never a paste — see the
   shared protocol). base = `git merge-base` of HEAD with the repo's
   integration branch (named by the repo shim, e.g. `origin/dev`); tip = HEAD.
   If the integration branch is ambiguous, ask.
4. **Populate the `## Review Kickoff` template** from
   `~/.agents/workflow/kickoffs/review.md` as INTERNAL orientation per the
   shared protocol — do NOT print it back. Sources: the spec for acceptance
   criteria and field 2a (original ask), the folder's `verification.md` for the
   implementer's verification claims — marked as claims (`per implementer log`)
   — and the live git range.
5. **Route by review topology.** Run `git diff --stat`, `--numstat`, and
   `--name-status`, then inspect enough of the full diff to group connected
   behavior and risk. Use coordinated mode when at least two coherent lanes
   exist and separate contexts materially reduce attention loss — common signals
   are multiple app/service/provider boundaries, a source/generated/consumer
   chain, or a canonical risk surface spanning layers. File count alone is never
   the trigger. Otherwise use serial mode.
   - **Coordinated:** if direct child agents are available, read
     `~/.agents/workflow/skills/large-pr-review/SKILL.md` in full and follow its
     Authorities plus Workflow steps 2-6 against the already-frozen range. This
     is this outer gate's execution mode, not another review pass.
   - **Serial:** perform the full review in this conversation. If coordinated
     mode would help but direct children are unavailable, continue serially and
     disclose that coverage constraint; do not emit disconnected scout prompts
     and pretend they form one verdict.
6. **Perform the outer lens** per `REVIEW_RUBRIC.md`. In either mode, the current
   conversation owns the lead integration and sole verdict: adversarial test-quality
   + contract-drift: ignore the implementer's test-quality framing, re-derive
   each test's value from the test source, ask "what regression could come
   back and still leave this suite green?" — PLUS the shared per-test and
   swap checks, since this is the only outer review. Run the repo's
   verification gates yourself where the rubric/kickoff requires local proof;
   do not take the implementer's logged numbers as proof of anything you can
   cheaply re-run.
7. **Return** per the shared carry-back shape, with these code specifics:
   - verdict line: `APPROVED` or `ACTIONABLE` + the `base..tip` range and tip
     SHA it certifies
   - findings with severity and path:line (ACTIONABLE only)
   - the verified-clean record: what was traced, read, and re-run that came
     back clean, plus any accidental prior-review exposure and its quarantine
   - one line reminding the operator: paste this into the implementer
     session; ACTIONABLE findings go through `implrereview` there.

## Guardrails

- GitHub/Linear stay read-only; no working-tree edits, no commits, no
  branch switches. Gates you run must be non-mutating (build/test/typecheck);
  anything destructive or provider-touching is out of scope here.
- Accidental prior-review exposure is not a stop condition: apply HANDOFF's
  quarantine rule, disclose it, and still return the strict verdict.
- Evidence scouts are read-only and never receive prior findings, the populated
  lead kickoff, or authority to issue a verdict.
- Strict-verdict / no-soften / no-early-read-counts per the shared protocol.

## Failure modes

The shared ones in HANDOFF.md "Outer-gate protocol", plus code specifics:
reviewing a mid-loop dirty tree instead of a converged committed candidate;
taking the implementer's logged gate numbers as proof instead of re-running the
cheap gates yourself; routing by file count alone; or inventing artificial lanes
to justify fan-out.
