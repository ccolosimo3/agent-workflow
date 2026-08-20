---
name: v2-implreview
description: Hand a completed committed V2 implementation to one fresh inner reviewer and drive same-reviewer patches to convergence. Use for own-work implementation review; not for specs or coworker PRs.
---

# V2 Implementation Review

## Required authorities

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`,
`../../references/REVIEW.md`, and `../../references/TESTING.md`; load
`../../references/FRONTEND.md` only for UI scope. Stop if an applicable authority
is unavailable, then read the repository instructions and adapter.

## Initial review

Confirm the implementation is committed and identify the exact base/tip from the
live checkout. Build `REVIEW.md`'s Implementation initial payload from the work
item, diff, verification evidence, and filesystem. Do not invent missing results
or expand scope to justify the diff.

Hand the payload and authority paths to exactly one fresh reviewer through the
host's isolated review capability. Before handoff, resolve every relative
authority reference to a path the fresh context can open, pass those resolved
paths, and confirm their reachability. An unreachable authority or unavailable
fresh review capability means no verdict; report the limitation. The reviewer
applies `REVIEW.md`'s Implementation method and Output contract.

## Convergence

Patch every autonomous finding within scope, rerun only causally affected proof,
and use `v2-implrereview` with the original reviewer. Stop for a
`[decision-required]` item or a patch that changes intended product behavior,
scope, authority, safety, or the Task boundary.

After approval, apply `WORKFLOW.md`'s outer-implementation selector. Launch
`v2-outerreview` in a fresh context when selected or requested; otherwise record
the one-line skip reason. Outer findings return only to that outer reviewer.
