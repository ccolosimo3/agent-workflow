---
name: review-pr
description: Review someone else's pull request through evidence-first discovery, proportionate independent challenge, and human-facing action calibration. Use for coworker PR review; not for the operator's own implementation gate.
metadata:
  opencode/autoinvoke: true
---

# Review PR

Run the review in this conversation. The invoking agent is the lead reviewer;
independent helpers challenge evidence but do not own the verdict or final message.

## Authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`; load
`../../references/FRONTEND.md` only for UI scope. Then read repository
instructions and the applicable repo adapter. Stop if an authority is missing.

## Freeze and map

Keep GitHub read-only. Inspect the linked issue and PR claims, checks, automated
review exclusions, and exact base/head SHAs, but defer existing comment content
until independent discovery finishes. Use the clean repository-root checkout by
default; create a review worktree only when existing work or incompatible tooling
requires it. Never stash, reset, or clean user work. Freeze and confirm one
base-to-head range before local proof.

Map the behavior before/after, acceptance, material risk surfaces, changed tests,
and affected producer/consumer, contract, state/lifecycle, migration,
deployment/CI, and rollout seams. Choose the smallest review topology that fits:

- **Compact:** one cohesive low-risk behavior with no material contract,
  auth/security, persistence/migration, lifecycle/concurrency, cross-system,
  deployment-topology, or shared tooling boundary. Review directly.
- **Standard:** any non-compact cohesive PR. Use one blind challenger.
- **Large:** at least two independent material risk surfaces that need different
  traces. Use one blind challenger and only the bounded specialists justified by
  that map, never more than three helpers total.

File count alone selects nothing. If compact eligibility is uncertain, use
standard. Apply the host adapter's coworker-review profile to both the lead and
challengers.

## Discover and challenge

The lead applies `REVIEW.md`'s required investigation, shared audits, candidate
admission, and severity rules to the entire frozen diff. Open every changed file
around each change, trace affected consumers, and run only risk-selected proof.

For standard/large work, give the fresh challenger only the checkout, frozen
range, raw ask/acceptance, authority paths, and any one assigned command. Do not
expose lead candidates, clean conclusions, or prior comments. Ask it to return:

```text
Risk map and paths traced
Candidates: scenario | PR relevance | consequence | evidence/counterevidence
Important claims still needing proof
Material verified-clean conclusions
Residual checks
```

Specialists receive one bounded independent question, not the whole PR or a
shared seam. The lead alone owns checkout changes, GitHub reads, services,
dependencies, broad gates, candidate validation, and final synthesis. Unassigned
helpers stay read-only and do not issue verdicts or severity.

If the host cannot create or resume the required challenger, continue the lead
review, disclose the degraded topology, and do not claim challenger convergence.
Do not abandon useful code/history evidence or repeatedly retry the same missing
capability.

After blind discovery, give the same challenger the combined candidates and
important clean conclusions. Ask it to refute blockers, challenge one potentially
missed seam, and name the narrowest decisive proof for disagreements. Reconcile
against the code, history, and real boundary; agreement is not evidence. Continue
only while an exchange changes a material candidate, counterexample, or proof.
One unchanged exchange establishes convergence.

For an unresolved material hypothesis, the lead may create a disposable,
untracked proof with a stated oracle, including base-versus-tip comparison when
causality matters. Do not modify tracked code or dependencies, prototype a fix,
or rerun broad verification for reassurance.

Then read existing comments, deduplicate them, recheck the live PR head, and
review any head delta that can invalidate evidence. Do not repeat a broad pass
without new evidence, a changed tip, or a named unanswered question.

## Calibrate for the operator

Discovery stays as strict as own-work review. Only after evidence converges,
translate each surviving item into one action:

- **Request changes:** confirmed realistic defect, unmet acceptance, material
  security/data/migration/contract/deployment risk, or required proof whose
  absence leaves a credible material regression surface.
- **Discuss:** product, intent, or team-policy ambiguity that changes the merge
  decision; state the exact question and both outcomes.
- **Suggestion:** objective improvement when current behavior is correct and no
  applicable authority is violated.
- **Nit:** introduced, objective, low-consequence detail without behavioral or
  contract impact.
- **Reject privately:** stale, duplicate, pre-existing, unsupported,
  speculative, authorized, or personal-preference candidates.

Missing ideal tests are not automatically blocking. Name the durable regression
and consequence, credit equivalent existing or practical manual proof, and ask
for only the smallest proportionate coverage. Never downgrade a confirmed
material defect merely for diplomacy.

Return a one-screen action brief first, ordered by merge action, with evidence and
the smallest requested outcome. Close with `approve`, `comment`, `request
changes`, or `hold for <answer/proof>`. Append a compact private audit mapping
every non-clean candidate to its action/rejection, verification performed,
material verified-clean surfaces, and residual checks. Do not print full clean
acceptance or per-test ledgers.

Do not post, approve, request changes, comment, commit, push, or patch the
author's branch without a separate operator request and approval.
