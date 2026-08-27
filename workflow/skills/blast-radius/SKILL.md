---
name: blast-radius
description: Find and prove non-obvious downstream breakage for a suspicious, cross-boundary, or deceptively small change. Use when asked what could break or when shared contracts, persistence, wire formats, lifecycle ordering, caches, async teardown, or native boundaries make symbol search insufficient; not for every ordinary diff.
metadata:
  opencode/autoinvoke: true
  workflow/kind: expert-guidance
---

# Blast Radius

Investigate the risk that is not visible in the diff. Apply this inside an
already-selected planning, implementation, or review activity; do not create a
new phase, broaden the authorized change, or require a standalone report.

## Find the hidden reach

1. State the behavior that changed, not only the symbols that changed.
2. Trace ordinary callers, then look where symbol search stops: persisted data,
   schema and migration transitions, serialized or generated contracts, another
   language reading the same bytes, feature flags, caches, scheduled work,
   teardown ordering, native bridges, and pinned dependency behavior.
3. Separate confirmed risks from plausible but cleared paths. Cite the concrete
   owner for each claim and do not invent consumers from names alone.

## Prove the pivotal fact

Identify the one or two facts on which the change's safety materially depends.
Get each as far down this evidence ladder as is proportionate and practical:

1. source or contract evidence;
2. a traced failure path showing whether the bad case can reach the change;
3. an existing focused test or script that runs the real owner;
4. the supported operation in a disposable or running environment.

Prefer an existing repository proof owner. Do not build a permanent harness,
write a mandatory one-off script, repeat broad gates, or invoke multiple models
merely to satisfy this skill. If stronger proof needs gated data, services, or
external mutation, preserve the active approval boundary. Mark the pivotal fact
unproven rather than rounding indirect evidence up.

## Return the useful result

Report only:

- the changed behavior and its non-obvious reach;
- the pivotal safety fact and strongest evidence actually obtained;
- confirmed risks with their concrete failure path;
- important paths checked and cleared;
- the cheapest remaining proof, if any.

Stop when the evidence is proportionate to the change's real risk. The active
workflow and repository verification owners remain authoritative.
