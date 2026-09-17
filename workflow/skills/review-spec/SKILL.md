---
name: review-spec
description: Hand a completed specification to one fresh inner reviewer and drive its same-reviewer revision loop to approval or a material operator decision. Use after spec or for an explicit spec preflight; not for code review.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Review Spec

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/PLANNING.md`, `../../references/REVIEW.md`, and
`../../references/TESTING.md` completely. If the spec has UI scope, also read
`../../references/FRONTEND.md`. Stop if a required authority cannot be resolved,
then read the repository instructions and relevant adapter.

## Initial review

Confirm the spec is review-ready and build `REVIEW.md`'s Spec initial payload
from the artifact and filesystem. Missing material remains visible; do not invent
it. Resolve the inner profile using `WORKFLOW.md`'s inheritance rule, then hand the
payload and authority paths to exactly one fresh reviewer using that host's
isolated review capability. Before handoff, resolve every relative
authority reference to a path the fresh context can open, pass those resolved
paths, and confirm their reachability. The planning context does not certify its
own spec. An unreachable authority or unavailable fresh review capability means
no verdict; report the limitation.

The reviewer applies `REVIEW.md`'s Spec method and Output contract to the entire
artifact and returns strict `APPROVED` or `ACTIONABLE`.

## Convergence

Follow `REVIEW.md`'s state machine and re-review payload: revise mechanical
findings, preserve unresolved operator choices, and resume the same reviewer
with the exact artifact delta, findings, resolutions, and affected proof. Use its
fresh fallback only when resumption is unavailable; retain the three-cycle cap.

After inner approval, apply `WORKFLOW.md`'s outer policy to this spec. Launch
`independent-spec-review` in one eligible fresh context when selected, carrying
the actual author host/profile; otherwise record the short skip reason. Outer
corrections return to that same reviewer. Return the approved spec to its author
for already-authorized continuation; approval does not itself grant execution.
