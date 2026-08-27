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

Patch every autonomous finding within scope and rerun only causally affected
proof. Stop for a `[decision-required]` item or a patch that changes intended
product behavior, scope, authority, safety, or the Task boundary. Otherwise
require the prior findings verbatim, prior reviewed tip, current tip, patch range,
resolutions per finding, and affected verification; resume the original reviewer
with only that delta. The reviewer applies `REVIEW.md`'s Re-review mode. Do not
rebuild the initial handoff or request broad rediscovery. If the original
reviewer cannot resume, disclose that limitation and give one fresh fallback the
full initial payload plus prior findings.

After approval, apply `WORKFLOW.md`'s configured outer policy and implementation
selector. Launch `independent-review` in exactly one permitted fresh context when
selected or requested; otherwise record the one-line skip reason. State the
implementation host when known so different-host preference can work without
guessing. Outer findings return only to that outer reviewer.
