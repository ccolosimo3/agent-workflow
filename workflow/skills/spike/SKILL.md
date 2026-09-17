---
name: spike
description: Run a disposable GO, NO-GO, or BLOCKED proof of one operator-selected design bet at its riskiest safe boundary. Use after an option is chosen but a load-bearing mechanism remains unproved; not for open-ended exploration or production implementation.
metadata:
  opencode/autoinvoke: true
---

# Spike

## Required authorities

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../references/KERNEL.md`, `../../references/WORKFLOW.md`, and
`../../references/PLANNING.md` completely. Stop if any cannot be resolved. Then
read the repository instructions and adapter relevant to the proof.

## Prove one bet

Confirm that the operator selected the spike and name the single uncertainty that
could reject or materially reshape the design. Before running anything, state the
falsifier, `GO` / `NO-GO` criteria, riskiest safely executable boundary,
time/scope box, fallback, and exact stop condition. Do not silently expand the
box when the bet does not prove out.

Use the smallest disposable proof that exercises the real uncertainty. Prefer
canonical parsers, validators, clients, and fixtures over reimplementing an
existing contract. Avoid config, global, or shared-state side effects. Disposable
scratch work within the selected proof follows `KERNEL.md`'s ordinary-action and
approval rules; calling a target disposable does not exempt a gated operation.
Proof code may live in the repository's declared plan area but does not become
production code or a permanent test merely because it was useful; remove
throwaway scaffolding by default and retain a proof artifact only when it remains
useful evidence.

Remain read-only toward production and shared external state. Live, paid,
authenticated, destructive, or prepared-environment proof requires the exact
approval in `KERNEL.md`; when unavailable, return `BLOCKED` with the missing
condition rather than substituting a weaker proof or retrying.

Preserve the bet, falsifier, safe boundary, time/scope box, fallback, declared
criteria, exact evidence, and retained/removed disposable artifacts in the
existing work item. Return `GO`, `NO-GO`, or `BLOCKED` and the design implication.
Distinguish what was proved from stronger wrapper, lifecycle, or platform claims
still unexercised, and carry those limits forward. Continue only when the
existing grant covers the next phase under `WORKFLOW.md`; an unresolved design
choice still returns to the operator. When `KERNEL.md`'s receipt trigger applies, read
`../../references/RECEIPTS.md` and write its best-effort record from evidence
already gathered.
