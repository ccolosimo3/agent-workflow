---
name: prreview
description: Review someone else's PR end to end. Populates the External PR
  Review Kickoff from the PR and its linked issue, performs the strict rubric
  pass with local verification directly in the invoking conversation, then
  calibrates the findings via the calibrate-review skill into an operator
  action brief (patch myself / raise with author / discuss / defer). May use
  bounded evidence subagents only for genuinely independent surfaces in a
  large PR. Use when the operator says /prreview, asks to review a numbered PR
  for them, or wants a coworker-PR review with calibrated takeaways. Do not use
  for the operator's own implementation handoff — that is implreview.
---

# prreview

One-command pipeline for a coworker's PR: strict review pass in this
conversation, then an operator-facing action brief. The invoking task is
already the fresh-context reviewer; do not spawn a subagent merely to create
another fresh context. Canonical content lives in:

- `~/.agents/workflow/kickoffs/external-pr-review.md` — "External PR Review Kickoff" template
- `~/.agents/workflow/REVIEW_RUBRIC.md` — reviewer manual
- `~/.agents/workflow/skills/calibrate-review/SKILL.md` — calibration rules and
  the Action Brief output contract

Read and apply those; do not inline or paraphrase their content here or into
prompts. Invoking this skill counts as the operator's explicit request for
coworker-facing calibration (the trigger calibrate-review requires).

## When invoked

1. **Preflight.** Run `git status --short --branch`. If the tree is dirty, stop
   and ask before anything that switches branches. Record the current branch so
   it can be restored after the review.

2. **Gather PR context (read-only).**
   - `gh pr view <n> --json title,body,author,baseRefName,headRefName,headRefOid,state,reviewDecision,statusCheckRollup,comments,reviews`
   - `gh pr checks <n>` for the rollup
   - the linked issue from the PR body (Linear or GitHub) — read it for
     acceptance criteria and the original ask
   - existing review threads, including automated reviewer comments
   - `.coderabbit.yaml` path exclusions, if the file exists
   - review range: fetch refs
     (`git fetch origin <baseRefName>` and `git fetch origin pull/<n>/head`),
     then base = `git merge-base` of the PR head with the target branch, tip =
     PR head SHA.

3. **Prepare and check out.** Populate the External PR Review Kickoff from
   `kickoffs/external-pr-review.md` as internal working context. Apply the
   AGENTS.md Fidelity Rule: verbatim shape, placeholders filled from the PR,
   linked issue, and filesystem. Where something genuinely cannot be fetched,
   use the template's fallback wording; do not invent acceptance criteria,
   results, or intent. Check out the PR branch only after the clean-tree
   preflight (use a separate clean worktree when the current checkout is
   occupied). Do not print the populated kickoff.

4. **Choose review topology.** Review serially in this conversation by default.
   Delegate only when the PR contains at least two materially independent risk
   surfaces whose deeper investigation can be partitioned without duplicating
   the whole review. File count or diff size alone is insufficient; many files
   implementing one end-to-end feature remain one surface.

   When delegation is justified, announce it and use at most two read-only
   evidence subagents unless the operator requests broader fanout. Give each
   one a single non-overlapping surface or investigation question. They return
   evidence, candidate findings, and verified-clean traces only — no verdict or
   calibration, no branch switch, and no duplicate broad verification. The
   invoking reviewer still owns the complete diff, opens every changed file,
   validates every candidate finding, and issues the final result.

5. **Review directly.** Apply `REVIEW_RUBRIC.md` in full, run proportionate
   local verification, and complete the raw rubric output plus Verified-clean
   record before calibrating. Do not soften the investigation in anticipation
   of calibration.

6. **Confirm proposed blockers.** Before classifying a finding as blocking,
   challenge it once: identify the concrete runtime failure and affected
   user/system outcome; determine whether it fails open or closed; and confirm
   it on the current PR head through code tracing or the narrowest decisive
   local check. Distinguish a demonstrated defect, a credible uncovered risk,
   missing ideal proof, and a rollout prerequisite. If no merge-time failure
   can be demonstrated and the system fails safely, route the item as a
   question or follow-up unless a tracked repo rule explicitly requires the
   missing proof. Do not rerun broad verification merely for more confidence.

7. **Calibrate.** Apply the calibrate-review skill to the raw findings,
   Verified-clean record, existing posted comments, and PR context. Calibration
   may change the recommended action or framing; it must not hide a confirmed
   blocker.

8. **Return to the operator, in order:**
   - the Action Brief (calibrate-review's output contract)
   - a compact appendix: the strict verdict line, raw findings, and the
     Verified-clean record — operator-facing only, never pasted into the PR
   - branch restore: state and run the plain checkout back to the recorded
     branch, unless the operator asked to leave the PR branch checked out.

## Guardrails

- GitHub stays read-only end to end: no comments, reviews, approvals, labels,
  or any `gh` mutation. Posting anything to the PR, or committing/pushing a
  touch-up to the author's branch, requires a separate operator request and
  fresh approval under the Destructive Action Policy.
- The output is not an implementation-loop verdict. It does not count toward
  the two-approved-verdicts rule for the operator's own work.
- If the review cannot complete (blocked environment, gates fail to run),
  report the exact blocker and stop.

## Failure modes to avoid

- Spawning a reviewer for an ordinary PR instead of reviewing directly.
- Treating file count alone as justification for delegation.
- Asking evidence subagents to review the whole PR, issue verdicts, switch the
  branch, or rerun the same broad gates.
- Skipping direct validation of a delegated candidate finding.
- Returning raw `ACTIONABLE` findings as the final answer with no calibration
  stage.
- Checking out the PR branch over a dirty tree.
- Calling a missing ideal proof a blocker without tracing the actual failure
  mode and tracked repository requirement.
- Letting calibration soften or omit a confirmed correctness or safety defect.
