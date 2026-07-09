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

The outer gate of the two-review flow (sequencing and independence rules:
`~/.agents/workflow/HANDOFF.md`). This skill runs in a FRESH conversation in
the app that did NOT implement — the conversation itself is the fresh-context
reviewer, so do the review here in the main thread; do not spawn a subagent.
Its verdict certifies the final tip for the kernel's two-approved-verdicts
gate.

## When invoked

1. **Preflight (read-only).** `git status --short --branch` in the repo root
   (operator-given, or the current working directory). Do not switch branches
   or edit the working tree — it is the implementer's checkout. If the tree
   is dirty or the branch looks like it is mid-loop, stop and ask: this skill
   reviews a converged, committed candidate.
2. **Locate the work item.** From the operator's pointer, or auto-detect: the
   branch's issue key → the repo's local plans folder (e.g.
   `<root>/.agent-workflow/plans/active/<ISSUE>-*/`). Read the spec
   (`README.md` acceptance criteria + implementation directions) and the
   folder's `verification.md` / `PR_BODY.md` if present.
3. **Independence seal (hard rule).** Do NOT read `reviews.md`, prior
   verdicts, or prior kickoff prompts — in the folder or in chat. If the
   operator pasted inner-loop findings, set them aside unread; this review
   must not be anchored by what the first lens found. (If they explicitly
   want a re-review against findings, that is `implrereview` in the
   implementer session, not this skill.)
4. **Compute the live range yourself.** base = `git merge-base` of HEAD with
   the repo's integration branch (named by the repo shim, e.g. `origin/dev`);
   tip = HEAD. Never accept SHAs from a pasted prompt — staleness is the
   failure mode this skill exists to kill. If the integration branch is
   ambiguous, ask.
5. **Populate the `## Review Kickoff` template** from
   `~/.agents/workflow/kickoffs/review.md` per the HANDOFF.md protocol (fidelity,
   honest population, repo-conventions resolution from the shim). Sources:
   the spec for acceptance criteria and field 2a (original ask), the folder's
   `verification.md` for the implementer's verification claims — marked as
   claims (`per implementer log`) — and the live git range. This is INTERNAL
   orientation — assemble the context to review against; do NOT print the
   populated kickoff back to the operator. What was reviewed is recorded
   concisely by the verdict return (step 7).
6. **Perform the review yourself** in this conversation, per
   `REVIEW_RUBRIC.md`. This is the outer-gate lens — adversarial test-quality
   + contract-drift: ignore the implementer's test-quality framing, re-derive
   each test's value from the test source, ask "what regression could come
   back and still leave this suite green?" — PLUS the shared per-test and
   swap checks, since this is the only outer review. Run the repo's
   verification gates yourself where the rubric/kickoff requires local proof;
   do not take the implementer's logged numbers as proof of anything you can
   cheaply re-run.
7. **Return, formatted for carry-back to the implementer session:**
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
- This verdict is a strict own-work review — do not soften it
  calibrate-review-style, and do not count a directional early read (run
  before the inner loop converged) as the certifying verdict.

## Failure modes

The shared ones in HANDOFF.md, plus: reading `reviews.md` or pasted prior
findings (independence seal); reviewing SHAs from a pasted prompt instead of
computing the live range; spawning a subagent (this conversation IS the fresh
context); reviewing a mid-loop dirty tree.
