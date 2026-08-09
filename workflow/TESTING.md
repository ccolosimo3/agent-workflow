# Testing — Principles & Universal Anti-Patterns

Single source of truth for the test PRINCIPLES and universal anti-patterns across
the operator's repos. The review *process* lives in `REVIEW_RUBRIC.md`; this doc
owns *what/how* to test at the principle level. **Apply Parts 1–2 always; the
concrete per-stack recipes, code examples, and canonical files live in the repo's
own testing reference** (see "Your repo's stack section" at the end).

Composes with each repo's coverage/verification authority, named in that repo's
testing reference (it wins on conflict).

---

## Part 1 — Principles (every stack)

### The principle

**Test the business/device outcome through the real operation — not the
implementation that delivers it today.** Schemas, migrations, field types, class
strings, style objects, helper exports, and tree shape are implementation: they
change without the behavior changing, and the behavior breaks without them
changing. So drive the service, component, hook, store, parser, client, or device
the way the app/board does, and assert the outcome a user or the board actually
depends on.

### Is a test worth keeping? (all four, or rewrite/delete)

1. **Regression-real** — fails if the actual bug comes back, not if a constant,
   class string, or style constant gets refactored.
2. **Real boundary** — runs the real operation (service/import/job, API route,
   render + interaction, hook state machine, store save+reload / rehydrate+
   write-back, parser/transport, fetch/abort client, native event→store), not code
   shape.
3. **Observable outcome** — asserts what a user/caller/board sees (persisted+
   reloaded state, HTTP status, rendered text/accessible label, parsed contract,
   classified error, thrown warning, command sent), not className / StyleSheet /
   SQL text / export shape.
4. **Durable value** — protects a continuing product, contract, safety, or
   operational requirement/risk, not an incidental preference or an acceptance
   criterion manufactured by the implementer to justify coverage.

**The 10-second check is necessary, not sufficient:** *if this came back, does the
test go red — and would that recurrence be a durable defect?* If either answer is
no, the test is not valuable yet.

### When to test vs skip

Test when the change **adds or alters a branch, fallback, failure path, persisted
field, contract, or device outcome.** Skip only for pure copy / markup / static
config / a framework-owned knob with no app logic — and when you skip, say so in the
PR and name the manual/Tier-4 proof that carries the confidence.

- Diff size doesn't excuse skipping a real branch; a one-line conditional that flips
  what renders, what persists, or what command is sent needs a test.
- A copy-sounding title doesn't either: if a "visual" change grows a pure helper or
  a stateful flag, test that helper/flag.
- Classification follows consequence, not file type or syntax. Exact text,
  markup, presence, or absence is not incidental when it carries functional,
  safety, security, privacy, legal/compliance, accessibility, operational,
  forbidden-output/policy, or public-contract meaning. A time-bounded requirement
  remains durable until its explicit retirement condition.
- Intentionally removing pure copy, markup, or presentation does not by itself
  create a continuing prohibition. Delete or relax only the obsolete assertion;
  do not invert it into absence/tombstone coverage unless the raw operator ask,
  an owning contract, or a concrete continuing risk makes absence durable. An
  implementer-authored addendum alone cannot create that authority. Preserve all
  other durable coverage; if authority is ambiguous, mark it
  `[decision-required]`. Never lower or bypass an enforced coverage gate: replace
  obsolete coverage with durable behavior proof or surface the gate-vs-quality
  conflict.
- **Per-stack defaults** (examples from this operator's repos; a repo without
  its own testing reference applies Parts 1–2 alone): tc-commerce → test
  **~always**; tc-app → test when there's branching, failure, or persistence
  logic; clearsnake → Jest when there's behavior, a contract, a failure mode,
  or persistence, and a **Tier-4 device proof** for touch/geometry/streaming
  risks a unit harness can't represent.

### How much — enough, not exhaustive

Thoroughness has a stopping point. Once a behavior is protected, another test for it
adds maintenance cost, not protection. Cover every distinct behavior and failure
mode **once**, at the **lowest-cost boundary that honestly proves it** — then stop.

- **One mechanism, one proof.** When several flows share a mechanism, prove it
  end-to-end once; assert the other call sites *fire* it at the seam level.
- **Match weight to what only that test can prove.** Reserve heavy real-client /
  integration / native tests for behavior you can *only* prove that way — cache
  isolation, persistence reload, a cross-boundary race, a native event→store path.
  Branch rendering, input mapping, and per-call-site wiring belong at the unit/seam
  level.
- **Test what *this* change changed.** Don't back-fill exhaustive coverage of
  pre-existing untested behavior; note the gap as a follow-up instead of inflating
  the diff.
- **Redundancy check.** Before adding a test: would it go red for a regression no
  existing test already catches? If another test already fails for that bug, drop or
  merge.
- **Brittleness is a cost on the ledger.** Big mock surfaces (deferred promises,
  multi-step UI, native-module mocks, fake timers) false-fail on unrelated
  refactors. Fewer, well-placed heavy tests beat a wall of them.
- **One-off repairs get proven once, not institutionalized.** A one-time
  static-asset, config, or data fix has no ongoing regression surface a normal code
  change would hit. Verify it once (a local `artifacts/` proof or a Tier-4 note),
  then keep that proof **out** of the permanent suite — a strong, passing test here
  earns its place only if the thing it guards can actually regress. Pocket it, don't
  ship it.

This is the counterweight to the coverage policy, not a contradiction: cover all the
distinct behaviors — each exactly once, at the right altitude.

### Inclusion: should this test ship? (a second axis, separate from PASS/FAIL)

A test can be a 10-second-check **PASS** and still not be worth shipping. Give each
new/changed test a disposition:

- **ship** — protects an ongoing regression surface this change introduced or
  touched (the default for real behavior tests).
- **trim** — valid but over-weight (heavy harness/dependency for trivial logic) or
  brittle; lighten it to the lowest boundary that proves the behavior.
- **redundant-with-`<test>`** — an existing/other test already goes RED for this
  regression; drop or merge.
- **one-off-proof→pocket** — a valid verification of a one-time repair with no
  ongoing regression surface; keep it as a local `artifacts/` proof or a Tier-4
  note, not permanent suite coverage.
- **obsolete-assertion-cleanup** — a deleted/relaxed assertion protected no
  durable requirement and every other durable assertion remains covered;
  expected cleanup, not a non-`ship` disposition.

The implementer pockets clear one-off proofs, ships `ship` tests, and records
`obsolete-assertion-cleanup` when the removal rule applies. For any other
non-`ship` disposition, surface it with a recommendation and let the **operator**
make the final include/exclude call — don't silently delete a working test. (This
is worth, not weakness; it is independent of whether the test is a quality FAIL.)

### Right-sizing agent output & coverage-gate interaction (hard rules)

These harden the two sections above into required behavior, because agents
systematically over-produce tests to chase a coverage number.

- **Behavior-first; coverage is a byproduct, never the target.** Write the tests
  the behavior needs; never add a test, an assertion-free execution, or a
  permutation whose only purpose is to move a coverage %. A repo's coverage gate
  (e.g. townchest `docs/testing/coverage-scope.md` + the *enforced*
  `jest.shared.cjs` allowlist) still wins as repo policy — but you satisfy it
  *with behavior tests*, and only for files the gate actually enforces. Do not
  pre-emptively exhaustively cover files the gate does not include. If a real
  branch is only reachable by a Part 2 anti-pattern, stop and surface the
  gate-vs-quality conflict to the operator rather than shipping a shape/no-assert
  test to make the number — Part 2 is not waived by a coverage target.

- **A spec's required-test list is the CEILING, not the floor.** When a plan/spec
  enumerates the tests for a change, implement those and stop. Any case beyond the
  list must name the distinct regression it protects. Don't mirror production
  permutations into test permutations.

- **Disproportionality is a stop-and-triage trigger.** A test artifact whose size
  is out of proportion to the behavior changed (heuristic: a many-hundred-line
  test file for a small/medium change) must be triaged test-by-test with the
  10-second check and the inclusion axis before handoff.

- **Trim before you split.** Splitting a big test file is not a fix for an
  oversized one. First delete redundant/implementation-shape tests, collapse
  permutations into table-driven cases, and push fixtures into factories/builders.
  Split into multiple files only if the *trimmed* suite is still large enough that
  splitting by behavior/concern aids comprehension — never to make bloat look
  smaller.

- **Disposition reporting is exception-only.** When assertions are unchanged,
  say so once. Otherwise group ordinary `ship` coverage by behavior/boundary and
  list each non-`ship` disposition with a one-line reason; do not emit a clean
  row per test. This changes reporting only — the full quality and inclusion
  audit still applies.

### Reviewer quick-check (for agent output)

🚩 **Reject/rewrite** if: it's named after a migration/class/constant; asserts a
constant, SQL/source text, a className/style object/layout number, a snapshot, "mock
was called", or `toBeDefined` as the point; is a backend test with no DB reload or a
store test with no rehydrate/write-back when persistence matters; offers a Storybook
story as the test; would still pass if you reverted the fix; protects only an
incidental detail with no durable defect/authority; deletes or relaxes unique
durable coverage without equivalent proof; or a changed branch has no test on
either side.

✅ **Accept** if: it runs the real operation, asserts an observable outcome
(persisted+reloaded state, HTTP status, accessible label / visible text, parsed
contract, classified error, command sent), covers the failure/edge path, reloads/
rehydrates for persistence, and any skip names its manual/Tier-4 proof.

✂️ **Trim/consolidate** (good test, too much) if: it re-proves a behavior another
test already catches, or uses a heavy integration/native flow to prove a wiring a
seam/unit test could assert. Cover each behavior once, at the lowest boundary.

Then apply the 10-second check and assign an inclusion disposition.

---

## Part 2 — Universal anti-patterns (delete on sight, every stack)

| Pattern | Why it's worthless |
| --- | --- |
| Test named after a migration/class/file/constant | Restates that code exists; protects no future behavior. |
| Import a constant and assert it equals itself / config-constant equals | Restates a constant; refactor-fragile, regression-blind. |
| Asserting a schema/custom-field/config value | Can fail without the objective failing, and pass while it's broken. |
| In-memory return/`setState` with no reload/rehydrate (when persistence is the point) | Tests a stand-in the runtime persists/rehydrates differently. |
| Source-text grep (`readFileSync(...).match(...)`) | Asserts code shape, not runtime behavior. |
| "Mock was called" as the point of the test | Couples to internals, not the contract. |
| Re-implementing the helper inside the mock factory | Tests a copy, not the real exported logic. |
| Export-existence / import-only / `toBeDefined()` | Not a behavior assertion. |
| Snapshot with no behavioral assertion | Rubber-stamps changes; asserts nothing meaningful. |
| A Storybook story used as the test | Visual proof only; no assertion, no guard. |

The one sanctioned constant-equality exception is a release-facing default that is
*itself* the contract (e.g. clearsnake `board-url-defaults.test.ts`, where URL drift
is the defect). Don't generalize it to other constants.

---

## Part 3 — Your repo's stack section

The concrete per-stack recipe — the real-operation pattern, code examples, stack
anti-patterns, and canonical example files — lives in the repo's own testing
reference, named by the repo shim (typically
`.agent-workflow/plans/reference/testing-philosophy.md`, or the path the shim
gives; clearsnake: `plans/reference/testing-philosophy.md`). That doc also names
the repo's coverage/verification authority, which wins on conflict. Apply
Parts 1–2 above plus that stack section for the repo you are in.
