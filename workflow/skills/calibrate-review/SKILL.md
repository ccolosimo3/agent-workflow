---
name: calibrate-review
description: Use only when the operator explicitly asks to calibrate raw review
  findings for someone else's PR or work. Triage External PR Review, implreview,
  review-pr, CodeRabbit, or human findings against repo standards, team norms,
  merge risk, author effort, and review etiquette; then return a concise action
  brief telling the operator what to patch as a touch-up commit, what to raise
  with the author as blocking or as a question, and what to defer or drop. Do
  not auto-run after ordinary implementation review handoffs.
---

# calibrate-review

Convert raw review findings into a concise, evidence-grounded action brief the
operator can act on — with the reviewing agent and with the PR author.

This skill is a translation layer, not another review pass. Use it after an
External PR Review pass (`~/.agents/workflow/KICKOFFS.md`), `implreview`,
`review-pr`, CodeRabbit, or a human reviewer has already produced findings and
the operator wants help deciding what to do and say on someone else's PR.
Do not conduct a fresh review or search for unrelated issues. Read enough
context to validate and calibrate the supplied findings. If you notice a
serious new risk while doing that, label it separately as a new concern.

## Core Principle

Protect the codebase while preserving trust with the author.

Use the strict review output as private signal. Do not paste raw agent verdicts,
rubric text, exhaustive ledgers, or "ACTIONABLE" framing into a coworker's PR.
Do not hide real blockers to avoid discomfort. Translate them into concise,
grounded recommendations the operator can deliver in their own words.

If coworker diplomacy conflicts with codebase safety, codebase safety wins. The
wording should stay respectful, but real blockers remain blockers.

## Grounding

Every item in the brief is only as good as its evidence, because the operator
owns each claim the moment they relay it to the author.

- Carry an evidence basis on every item: the diff lines read, the upstream
  finding, the verified-clean record entry, or the command + result behind it.
- The upstream pass's verified-clean record (what it traced, read, and ran that
  came back clean) is a required input. If it is missing, ask for it — do not
  infer cleanliness from the absence of findings.
- Never mark an item verified unless the record, diff lines you read, or the
  operator's own stated actions support it. Mark anything else
  `unverified — check before relaying`.
- Confirm each finding still applies at the PR's current head; raw findings may
  predate a force-push or follow-up commit. Publicly flagging an already-fixed
  issue is a social cost with no benefit.
- Check what is already posted on the PR (automated reviewers, humans). Do not
  re-raise an already-posted finding as new; mark it `already-posted` and note
  agreement only when it materially changes the merge decision.

## Trigger Boundary

Run only when explicitly requested by the operator for an external/human-facing
review, such as:

- "calibrate these findings"
- "prepare a human review"
- "help me decide what to surface"
- "this is someone else's PR"
- "turn these agent findings into a coworker-friendly review"
- as the calibration stage of a `prreview` run — invoking that skill counts
  as the operator's explicit request

Do not use this skill for the operator's own implementation handoff unless they
explicitly ask for coworker-facing calibration. Normal implementation reviews
stay strict and mechanical.

This skill never replaces the strict implementation-review verdict used for the
operator's own work. Its output is not an `APPROVED` review verdict for the
implementation loop and must not be counted as one.

## Inputs

Gather only what is needed:

- raw findings from review agents, CodeRabbit, or humans
- the upstream pass's verified-clean record: the specific checks, traces, and
  commands that came back clean (ask for it if missing)
- review comments already posted on the PR, automated or human
- PR title/body and linked issue/spec, when available
- changed surface: customer UI, internal admin/operator UI, dev-only tool,
  backend service, migration, generated contract, provider/infrastructure
- CI/check status and author-stated manual verification
- repo/team standards that apply, distinguishing tracked/shared standards from
  personal local workflow preferences
- whether team norms let the operator push a touch-up commit to the author's
  branch, or prefer a suggested diff

If a finding depends on a repo standard, cite the standard if known. If the
standard is only local or personal, treat it as a question or a defer/drop item
unless the operator says the team has adopted it.

## Triage Axes

For each finding classify:

- **Confidence**: confirmed / likely / speculative
- **Basis**: tracked repo rule or CI / shared team convention / general best
  practice / local preference
- **Merge risk**: blocker / important / minor / note
- **Impact**: customer / internal operator / developer / downstream contract /
  none clear
- **Author effort**: tiny / small / moderate / large redo
- **Best action**: patch myself / raise as blocker / raise as question / defer
  to follow-up / drop

Large-redo findings need a high burden of proof. If a finding would ask the
author to rework a chosen approach, surface it as a question or manager/team
calibration point unless it clearly breaks requirements, creates real risk, or
violates an agreed standard.

## Surfacing Rules

Request changes only for:

- acceptance criteria not met
- correctness bug in a real path
- security, permission, privacy, data loss, migration, or provider risk
- API/schema/generated contract drift that will create downstream breakage or
  recurring unrelated churn
- missing verification for risk-bearing behavior with no credible automated or
  manual proof

Ask a question when:

- product scope or role behavior is ambiguous
- the finding depends on an assumption about how the team uses the feature
- the likely fix could expand the PR or require redesign
- the standard is not clearly shared by the team

Use a nit or small suggestion when:

- the issue is real but low risk
- the fix is tiny
- the PR is otherwise sound
- the author can address it without rethinking the design

Patch it in myself (touch-up commit) when:

- the fix is mechanical and tiny
- the author may appreciate unblocking help
- patching does not require taking over design ownership
- team norms allow reviewer commits on the author's branch; otherwise recommend
  handing the author a suggested diff instead

Defer or drop when:

- the finding is mostly personal preference
- the code could be nicer but is not risky
- the fix would cause large churn without a clear team-standard basis
- the issue belongs in a follow-up rather than this PR

Floor: an item triaged blocker or important must land in a raise-with-author
group (or be patched and said so) — only its framing is negotiable, never its
visibility. Defer/drop is for minor and note-level items only.

## Surface Calibration

- Public/customer UI: accessibility and UX issues are usually worth surfacing.
- Internal admin/operator UI: basic accessibility, labels, errors, and clarity
  still matter; small issues are usually nits unless they block use.
- Dev-only scripts/tests/debug tools: polish is usually defer/drop or optional
  unless the surface is reused by non-developers or affects reliability.
- Generated/API/schema surfaces: contract consistency is important even when
  the immediate PR consumer does not use the generated artifact.
- Tests: prefer asking for the smallest proof that covers the real risk. If the
  author already ran manual verification, ask them to record reproducible steps
  before demanding a new automated harness — except where a tracked repo
  standard mandates a specific proof (e.g. a migration save/reload bar); then
  cite the standard and hold that line.

Do not call an internal admin/operator feature "dev-only" merely because it is a
debug or maintenance affordance. Decide based on who can actually reach and use
the surface.

## Framing Guidance

The brief is for the operator; the words to the author are theirs. When an item
includes a suggested frame, anchor positives in evidence that exists: lead with
what the review actually confirmed works, then the few things worth checking
before merge.

Frames that land well — suggest them only when the verified-clean record or the
operator's own check backs the claim:

- "I traced X through Y and the main wiring looks good."
- "One thing I would check before merge..."
- "Is this role split real in production?"
- "Could you add the manual steps you ran to the PR body?"
- "Tiny polish: ..."

Avoid:

- agent names
- raw verdict labels such as `ACTIONABLE`
- "the rubric says"
- exhaustive private ledgers
- implying optional polish failed the review
- asking for a rewrite unless the current approach is clearly risky or outside
  scope
- verification claims nothing in the record supports

## Output: Action Brief

No paste-ready review prose. Return one concise brief the operator can read in
one screen, discuss with you, and act on with the author. One line per item:

`finding | path:line | basis | evidence | confidence`

Group items by action, ordered by merge risk within each group:

1. **Patch myself**: mechanical, tiny fixes worth a touch-up commit on the PR
   branch without taking over design ownership. Note when team norms favor a
   suggested diff over a push.
2. **Raise with author — blocking**: items meeting the request-changes bar.
   Name the rule or risk and the smallest acceptable fix.
3. **Raise with author — discuss/ask**: scope ambiguities, assumption checks,
   large-redo concerns. Give the one-sentence question to ask, not a script.
4. **Defer / drop**: nits, preferences, follow-up candidates, already-posted
   items — one-word reason each (preference / churn / follow-up /
   already-posted / stale / unverified).

Close with two lines:

- **Stance**: approve / comment / request changes / hold for operator decision,
  naming the evidence basis (e.g. "based on External PR Review pass +
  CodeRabbit; affected tests rerun locally"). A stance built on thin coverage
  must say so.
- **Manager calibration**: only when a finding exposes an unclear team policy
  or a repeated review-standard mismatch; otherwise omit.

If every item is defer/drop, say so in one line and stop — do not formalize a
routine PR.

Recommend only. Do not post, submit, approve, request changes, or comment on
the PR, and do not commit or push to the author's branch, unless the operator
separately asks and authorizes that exact action. Touch-up commits and pushes
are operator-executed and stay under the destructive-action approval rules.
