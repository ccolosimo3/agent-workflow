---
name: prreview
description: Review someone else's PR end to end. Populates the External PR
  Review Kickoff from the PR and its linked issue, spawns one fresh-context
  reviewer (announcing the handoff) that runs the strict rubric pass with local
  verification, then calibrates the returned findings via the calibrate-review
  skill into an operator action brief (patch myself / raise with author /
  discuss / defer). Use when the operator says /prreview, asks to review a
  numbered PR for them, or wants a coworker-PR review with calibrated
  takeaways. Do not use for the operator's own implementation handoff — that
  is implreview.
---

# prreview

One-command pipeline for a coworker's PR: strict fresh-context review pass,
then an operator-facing action brief. This skill is a thin orchestrator — the
canonical content lives in:

- `~/.agents/workflow/KICKOFFS.md` — "External PR Review Kickoff" template
- `~/.agents/workflow/REVIEW_RUBRIC.md` — reviewer manual, read by the spawned
  reviewer itself
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
   - review range: fetch refs without checking out
     (`git fetch origin <baseRefName>` and `git fetch origin pull/<n>/head`),
     then base = `git merge-base` of the PR head with the target branch, tip =
     PR head SHA. Do NOT check out the PR branch in this session — the spawned
     reviewer does the checkout per the kickoff.

3. **Populate the External PR Review Kickoff** from KICKOFFS.md. Apply the
   AGENTS.md Fidelity Rule: verbatim shape, placeholders filled from the PR,
   the linked issue, and the filesystem (repo convention paths resolved by
   checking they exist). Where something genuinely cannot be fetched (e.g. no
   issue linked), use the fallback wording the template itself specifies — do
   not invent acceptance criteria, check results, or intent.

4. **Announce the handoff** (the PR + range being reviewed) and pass the full
   populated External PR Review Kickoff to the subagent — the operator opens the
   subagent to inspect it. Emit the full prompt in chat under a `## External PR
   Review Kickoff Prompt` heading only when the host cannot spawn a subagent (for
   manual launch).

5. **Spawn exactly one fresh-context reviewer** with that prompt verbatim,
   using whatever subagent mechanism the host agent provides. Announce
   `spawning one reviewer`. The reviewer checks out the PR branch, runs the
   kickoff's local gates, and returns the rubric output plus the Verified-clean
   record. Do not edit files in this session while it runs — the working tree
   is shared.

6. **Calibrate.** Apply the calibrate-review skill to the reviewer's findings,
   the Verified-clean record, existing posted comments, and the PR context.
   Calibration happens in this session, not in the reviewer's, because it needs
   operator/team context the fresh reviewer must not see.

7. **Return to the operator, in order:**
   - the Action Brief (calibrate-review's output contract)
   - a compact appendix: the reviewer's verdict line, raw findings, and the
     Verified-clean record — operator-facing only, never pasted into the PR
   - branch restore: if the reviewer switched the working tree, state and run
     the plain checkout back to the recorded branch.

## Guardrails

- GitHub stays read-only end to end: no comments, reviews, approvals, labels,
  or any `gh` mutation. Posting anything to the PR, or committing/pushing a
  touch-up to the author's branch, requires a separate operator request and
  fresh approval under the Destructive Action Policy.
- The output is not an implementation-loop verdict. It does not count toward
  the two-approved-verdicts rule for the operator's own work.
- If the reviewer cannot complete (blocked environment, gates fail to run),
  report the exact blocker and stop. Do not substitute a fresh review of your
  own — that is the reviewer's job, in fresh context.

## Failure modes to avoid

- Paraphrasing the kickoff template instead of copying its shape verbatim.
- Inlining the rubric or the calibration rules into prompts — the reviewer
  reads the rubric itself; calibration is applied from its own skill file.
- Dumping the full kickoff inline instead of just announcing the handoff (the
  subagent carries the prompt; only the no-subagent fallback emits it).
- Spawning more than one reviewer.
- Returning raw `ACTIONABLE` findings as the final answer with no calibration
  stage.
- Checking out the PR branch in the main session, or over a dirty tree.
- Letting calibration concerns leak into the reviewer's prompt — the strict
  pass must not know its findings will be softened.
