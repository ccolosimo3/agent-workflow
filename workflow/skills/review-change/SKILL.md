---
name: review-change
description: Hand a completed committed implementation to one fresh inner reviewer and drive same-reviewer patches to convergence. Use for own-work implementation review; not for specs or coworker PRs.
metadata:
  opencode/autoinvoke: false
---

# Review Change

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`; load
`../../references/FRONTEND.md` only for UI scope. Stop if an applicable authority
is unavailable, then read the repository instructions and adapter.

## Evidence-only return

Before starting a source review, check whether this is later evidence for a
source-approved candidate. If `REVIEW.md`'s evidence-only admission holds, route
directly to the reviewer assigned to that evidence gate with the candidate
identity, new artifacts, and any changed proof. Do not repeat closed inner or
outer source gates. Resume that reviewer; if it cannot resume, use the disclosed
fresh fallback rule with its retained payload and relevant prior findings. A
newly selected outer evidence gate uses one fresh `independent-review` context
under the configured routing. Apply the scoped verdict and finish this path.

## Initial review

Confirm the implementation is committed and identify the exact base/tip from the
live checkout. Build `REVIEW.md`'s Implementation initial payload from the work
item, diff, verification evidence, and filesystem. Do not invent missing results
or expand scope to justify the diff.

Resolve the inner profile using `WORKFLOW.md`'s inheritance rule. Hand the payload
and authority paths to exactly one fresh reviewer through that host's isolated
review capability. Before handoff, resolve every relative
authority reference to a path the fresh context can open, pass those resolved
paths, and confirm their reachability. An unreachable authority or unavailable
fresh review capability means no verdict; report the limitation. The reviewer
applies `REVIEW.md`'s Implementation method and Output contract.

## Convergence

Follow `REVIEW.md`'s state machine and re-review payload: the author patches
in-scope findings, commits corrections, reruns causally affected proof, and
resumes the same reviewer with the delta. Material operator choices remain open;
use its disclosed fresh fallback only when resumption is unavailable. Do not
restart broad discovery or send a second initial payload to a resumable reviewer.

Apply `WORKFLOW.md`'s outer selection policy and timing through `REVIEW.md`'s
state machine.
Launch `independent-review` in one eligible fresh context when selected, naming
full-source or evidence-only scope and the actual author host/profile. Otherwise
record the short skip reason. Outer corrections return to that same reviewer.
