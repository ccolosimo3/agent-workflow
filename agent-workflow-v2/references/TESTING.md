# Agent Workflow V2 Testing Authority

This file owns portable test quality. Repository verification and stack guides
own commands and concrete harnesses; they may be stricter but cannot make a
shape-only test sufficient.

## Durable proof

A useful test must satisfy all four:

1. **Regression-real:** restoring the defect makes it fail.
2. **Real boundary:** it exercises the operation that owns the behavior rather
   than a source-code or mock-call stand-in.
3. **Observable outcome:** it asserts what a user, caller, job, persisted store,
   or device observes.
4. **Durable value:** it protects a continuing product, contract, safety,
   accessibility, policy, or operational requirement.

The quick falsifier is: *if this returned, would the test go red, and would that
recurrence still be a defect?* Both answers must be yes.

Test changed branches, fallbacks, failures, persistence, contracts, and device or
integration outcomes. Pure copy, markup, static configuration, or a
framework-owned knob may use proportionate manual proof when no application
behavior changes. Removing incidental copy or presentation does not create a
permanent absence contract; remove only its obsolete assertion unless continuing
functional, safety, accessibility, legal, privacy, policy, or public-contract
authority requires absence coverage.

## Enough, then stop

Cover each distinct behavior and failure mode once at the lowest-cost boundary
that honestly proves it. Keep a heavier test only for what the heavier boundary
alone establishes, such as persistence reload, integration behavior,
cross-boundary ordering, concurrency, lifecycle, or device behavior.

Use canonical production owners and validators for behavior under test; do not
recreate their contract, lifecycle, identity, or projection logic in a harness or
oracle. For unrelated state whose setup behavior is not under test and whose
relevant contract is only exact preservation, schema-valid deterministic fixtures
are sufficient.

- Before adding coverage, name any retained test that catches the same regression
  under the same relevant conditions. Merge or omit redundant proof.
- Test what the change affects; do not backfill unrelated historical gaps into the
  work item.
- A spec's named cases are the expected ceiling. An additional case must protect a
  distinct regression.
- A one-time data, asset, or configuration repair with no recurring code path gets
  a disposable proof or operator check, not a permanent test.
- Coverage percentage is a constraint, never the behavioral target. If an
  enforced gate can be met only with a weak test, surface the conflict.

After two local or CI failures on the same proof premise without evidence of a
new product defect, stop patching the harness and return to the premise and
minimum proof shape. CI confirms a diagnosed correction; it is not the iterative
diagnosis loop.

## Inclusion disposition

Judge test quality and whether it should ship as separate questions:

- **ship:** distinct durable regression at the lowest honest boundary;
- **trim:** valid but unnecessarily heavy or brittle;
- **redundant-with-`<test>`:** retained proof catches the same regression at an
  equally faithful boundary;
- **one-off-proof:** useful once, but belongs outside the permanent suite;
- **obsolete-assertion-cleanup:** removes coverage for retired incidental behavior
  without weakening any durable contract.

The implementer may autonomously trim or remove a test first added in the current
work item when it names the retained equivalent proof. Do not silently weaken
pre-existing coverage or ambiguous durable authority; route that decision to the
operator. Report ordinary `ship` coverage by behavior family and list only
exceptions—never print a clean row for every assertion.

## Real-boundary bars

- **Persistence or schema:** exercise the real repository/service path and save
  plus reload. A generated migration needs a fresh-schema proof and, when data or
  constraints change, a populated-upgrade proof. Prove any lossy down path cannot
  silently corrupt data.
- **Integration or contract:** cross the actual producer/consumer seam and assert
  the caller-visible status, shape, error, or side effect.
- **Behavior-preserving refactor:** prove before/after parity at the same real
  boundary across every applicable status, output or data shape, error, side
  effect, persistence result, and contract. Prefer existing coverage; use a
  disposable equivalence or characterization proof when needed rather than
  turning incidental structure into a permanent test.
- **Performance claim:** compare before/after at the same representative workload,
  environment, and metric. Repeat enough to distinguish the change from normal
  variation, and confirm material cost was not merely shifted to another
  resource, stage, or tail.
- **UI:** render and interact through the real component boundary; assert visible
  or accessible behavior. Load `FRONTEND.md` for visual, state, accessibility,
  and layout proof.
- **CI workflow:** prove the job's execution context, ordering, and dependencies;
  YAML parsing and isolated tests of the called script are not enough. At
  CI-sensitive shell or command boundaries, label assertions and report the
  observed mismatch so logs identify the failed contract.
- **Unavailable real boundary:** record the exact operator/live/manual proof and
  owner rather than inventing weaker automation.

## Universal anti-patterns

Reject a test whose point is any of these unless the exact shape is itself a
documented public contract and a real-boundary proof carries the behavior:

- file, class, migration, export, route, or constant existence;
- source-text, SQL-text, class-name, style-object, or snapshot equality;
- importing a constant and asserting it equals itself;
- `toBeDefined`, assertion-free execution, or coverage-only permutations;
- “mock was called” without the observable outcome;
- reimplementing the production helper inside a mock or oracle;
- in-memory persistence behavior without reload or rehydrate;
- a story, screenshot, or fixture presented as automated behavioral proof.

A shape assertion may supplement a named behavioral proof when ordering or
structure is genuinely contractual. It cannot replace that proof.
