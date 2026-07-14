---
name: outerreview
description: Run the operator-owned outer-gate second review of their OWN
  implementation, in a fresh conversation in the other app/model, after the
  implementer session's review + re-review loop has converged. Self-populates
  the Review Kickoff from the work-item folder and the live git range (never
  from a pasted prompt), deliberately ignores prior reviewer findings, performs
  the review itself in this conversation per
  ~/.agents/workflow/REVIEW_RUBRIC.md, and returns the strict verdict +
  verified-clean record for the operator to carry back. Use when the operator
  says /outerreview, "second review this branch", or names a work item or
  repo and asks for the outer-gate review. Not for coworker PRs (that is
  prreview) and not for the implementer session's own loop (implreview).
---

# outerreview

The outer gate of the two-review flow. Apply the shared
`~/.agents/workflow/HANDOFF.md` "Outer-gate protocol" for the mechanics every
outer gate shares — conversation-is-the-reviewer / no subagent (do the review
here in the main thread), self-populate from filesystem + live range (never a
paste; staleness = failure), the independence seal, the populated kickoff is
INTERNAL orientation you do NOT print, the carry-back return shape, and the
strict verdict (no softening, an early pre-convergence read never counts). This
skill keeps only the code-review specifics below. Its verdict certifies the
final tip for the kernel's two-approved-verdicts gate.

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
   verdicts.)
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
5. **Perform the review yourself** in this conversation, per
   `REVIEW_RUBRIC.md`. This is the outer-gate lens — adversarial test-quality
   + contract-drift: ignore the implementer's test-quality framing, re-derive
   each test's value from the test source, ask "what regression could come
   back and still leave this suite green?" — PLUS the shared per-test and
   swap checks, since this is the only outer review. Run the repo's
   verification gates yourself where the rubric/kickoff requires local proof;
   do not take the implementer's logged numbers as proof of anything you can
   cheaply re-run.
6. **Return** per the shared carry-back shape, with these code specifics:
   - verdict line: `APPROVED` or `ACTIONABLE` + the `base..tip` range and tip
     SHA it certifies
   - findings with severity and path:line (ACTIONABLE only)
   - the verified-clean record: what was traced, read, and re-run that came
     back clean
   - one line reminding the operator: paste this into the implementer
     session; ACTIONABLE findings go through `implrereview` there.

## Guardrails

- GitHub/Linear stay read-only; no working-tree edits, no commits, no
  branch switches. Gates you run must be non-mutating (build/test/typecheck);
  anything destructive or provider-touching is out of scope here.
- Strict-verdict / no-soften / no-early-read-counts per the shared protocol.

## Failure modes

The shared ones in HANDOFF.md "Outer-gate protocol", plus code specifics:
reviewing a mid-loop dirty tree instead of a converged committed candidate;
taking the implementer's logged gate numbers as proof instead of re-running the
cheap gates yourself.
