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

On `ACTIONABLE`, patch grounded mechanical findings autonomously. Stop for a
`[decision-required]` item or any correction that changes intended product
behavior, scope, policy, authority, safety, or the selected Task boundary.
Otherwise require the prior findings verbatim, exact artifact revision previously
reviewed, current artifact, resolutions per finding, and affected verification;
resume the original reviewer with only that delta. The reviewer applies
`REVIEW.md`'s Re-review mode. Do not rebuild the initial handoff or request broad
rediscovery. If the original reviewer cannot resume, disclose that limitation and
give one fresh fallback the full initial payload plus prior findings. Continue
until approved or the three-cycle cap is reached.

After approval, apply `WORKFLOW.md`'s configured outer policy and spec selector.
Launch `independent-spec-review` in exactly one permitted fresh context when
selected or requested; state the authoring host when known. Otherwise record the
one-line skip reason and finish. Do not pause merely to ask whether to run a
required review gate.
