# Testing — Principles & Per-Stack Guide

Single source of truth for how to write and review tests across the operator's
repos. The review *process* lives in `REVIEW_RUBRIC.md`; this doc owns *what/how*
to test. **Apply Parts 1–2 always, plus the one stack section for the repo you are
in.**

Composes with each repo's coverage/verification authority (those win on conflict):
- townchest: `docs/testing/coverage-scope.md` (the 100% in-scope coverage policy).
- clearsnake-mobile: `mobile/VERIFICATION.md` (Automated Unit-Test Policy + coverage
  treatments) and `mobile/jest.config.js` (mechanical coverage authority).

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

### Is a test worth keeping? (all three, or rewrite/delete)

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

**The 10-second check:** *if this bug came back, does the test go red?* If you can't
answer yes, it isn't valuable yet.

### When to test vs skip

Test when the change **adds or alters a branch, fallback, failure path, persisted
field, contract, or device outcome.** Skip only for pure copy / markup / static
config / a framework-owned knob with no app logic — and when you skip, say so in the
PR and name the manual/Tier-4 proof that carries the confidence.

- Diff size doesn't excuse skipping a real branch; a one-line conditional that flips
  what renders, what persists, or what command is sent needs a test.
- A copy-sounding title doesn't either: if a "visual" change grows a pure helper or
  a stateful flag, test that helper/flag.
- **Per-stack defaults:** tc-commerce → test **~always**; tc-app → test when there's
  branching, failure, or persistence logic; clearsnake → Jest when there's behavior,
  a contract, a failure mode, or persistence, and a **Tier-4 device proof** for
  touch/geometry/streaming risks a unit harness can't represent.

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

The implementer pockets clear one-off proofs and ships `ship` tests. For any other
non-`ship` disposition, surface it with a recommendation and let the **operator**
make the final include/exclude call — don't silently delete a working test. (This is
worth, not weakness; it is independent of whether the test is a quality FAIL.)

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

- **Disposition reporting is a hard handoff output.** Every implementation handoff
  names, for new/changed tests: total count, each non-`ship` disposition with a
  one-line reason, and confirmation the suite was trimmed to behaviors. A handoff
  without this is incomplete.

### Reviewer quick-check (for agent output)

🚩 **Reject/rewrite** if: it's named after a migration/class/constant; asserts a
constant, SQL/source text, a className/style object/layout number, a snapshot, "mock
was called", or `toBeDefined` as the point; is a backend test with no DB reload or a
store test with no rehydrate/write-back when persistence matters; offers a Storybook
story as the test; would still pass if you reverted the fix; or a changed branch has
no test on either side.

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

## Part 3 — tc-commerce / Vendure / Mirakl (Vitest)

Boot a real Vendure test server → run the real service method → **save + reload from
the DB** → assert the reloaded entity. Mock only the external Mirakl SDK.

```ts
const variant = await app.get(ProductVariantService).findOne(ctx, variantId);
await app.get(EntityHydrator).hydrate(ctx, variant!, { relations: ['assets'] });
expect(variant!.assets[0].asset.customFields.original_url).toBe(longUrl);
```

- **Save + reload is the core.** Re-fetch via the repository/service after the
  operation; assert the reloaded entity, never the in-memory return value.
- Use real fixtures from `test-fixtures/`, mutated per case (delete a field to force
  a failure; bump ids to avoid collisions).
- Repair/persistence bugs: corrupt real state, **assert it's broken first**, run the
  operation, reload (ideally two read paths), assert it healed.
- Split pure logic (fast unit tests) from orchestration (one real save+reload
  integration test).
- **Migrations:** prove behavior via the import/service path; local-Postgres
  `migrate:run` is the **Tier-4** proof — SQL.js is supplemental. Generate via
  `pnpm --filter tc-commerce migrate:generate`, never bare `npx vendure`. A
  generated-SQL string match or "`up()`/`down()` were called" is **not** sufficient
  on its own.

**Stack anti-pattern:** generated-SQL string match as the sole proof (OK only as
clearly-supplemental to a save+reload / migrate:run proof).

**Canonical files:**
- Import + save/reload: `services/tc-commerce/src/plugins/mirakl-connector/products/tests/product-import.spec.ts`

---

## Part 4 — tc-app frontend (React Query / Jest+RTL / Next routes)

### React Query stores / hooks (Vitest)

Run the real query through `TCQueryClient`; assert resolved data **and the failure
path**.

```ts
vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401, json: ... }));
await expect(new TCQueryClient().fetchQuery(paymentMethodsBootstrapQuery('user-1')))
  .rejects.toBeInstanceOf(PaymentMethodsBootstrapUnauthorizedError);
```

- Always cover the failure path (e.g. 401 → typed redirect error).
- Test derived flags (`isPending`/`isError`/`isUnavailable`, default-vs-custom) as
  pure functions of query state.
- Don't assert the raw options object (`gcTime`, `refetchOnWindowFocus`, …) — that's
  config shape. `queryKey` may be asserted when cache isolation is a real contract.
- For stores that hit Supabase directly, prefer a real-DB test: insert fixtures with
  `SUDOsupabase`, run the query, assert, clean up in `afterAll`.

### Components (Jest + React Testing Library)

Render the real component, drive it with `userEvent`/`fireEvent`, assert
user-visible output and the **absence** of the wrong state.

```tsx
/** @jest-environment jsdom */
render(<ThemeProvider theme={theme}><Page /></ThemeProvider>);
expect(screen.getByTestId('payment-methods-bootstrap-skeleton')).toBeTruthy();
expect(screen.queryByText('Cards')).toBeNull();
```

- One render+assert per real branch; match cases to branch count, not line count.
- Cover failure/rollback explicitly (retry calls refetch; unauthorized → redirect;
  optimistic action reverts on write failure).
- Include an old-copy/regression case for display-conditional changes.
- Mock at the seam (`jest.mock` + a mutable ref reset in `beforeEach`); import real
  shared classes/helpers instead of re-declaring them in the mock.
- A Storybook story is not a test.

### Next API routes (Jest, node env)

Invoke the real handler with a real `Request`; assert status per branch and that the
persistence collaborator isn't called on the failure path.

```ts
/** @jest-environment node */
const res = await PATCH(createFormDataRequest() as NextRequest);
expect(res.status).toBe(401);
expect(mockPersist).not.toHaveBeenCalled();   // no side effect on failure
```

- Assert `response.status` for each branch (200 / 400 / 401 / 404 / 409) and the
  response body shape callers depend on.

**Canonical files:**
- React Query store (mocked-fetch + failure): `apps/tc-app/stores/tests/payment-methods-query.test.ts`
- React Query store (real-DB): `apps/tc-app/stores/tests/supporter-of-query.test.ts`
- Component RTL (branches + retry + redirect): `apps/tc-app/components/support/page/PaymentMethodsPage/__tests__/UserPaymentMethodsPage.test.tsx`
- Next route (status matrix + no-side-effect-on-fail): `apps/tc-app/app/api/user/pledged-schools-banner/dismiss/dismiss.test.ts`

---

## Part 5 — clearsnake mobile (RN / Jest+RNTL / Zustand)

### Components (React Native Testing Library)

Render the real component, query by accessibility/role/text/testID, assert behavior
and the **absence** of the wrong state. Never assert `className`,
`StyleSheet.flatten(...)`, or numeric layout props.

```tsx
import { render } from '@testing-library/react-native';

const screen = render(
  <ConnectionIndicator isConnected={false} isConnecting networkStatus="reachable" />,
);
expect(screen.getByLabelText('Connecting to camera')).toBeTruthy();
expect(screen.queryByText('OFFLINE')).toBeNull();
```

- Assert the user-facing contract: accessible label/live-region, visible label,
  state precedence, that the right callback/command fires on interaction.
- One render+assert per real branch; cover empty/disconnected/error, not just happy.
- For "does the layout stay stable", assert an **invariant** (a stable container/
  icon-slot via testID exists in every state) rather than exact `gap`/`width`/`flex`.
  If the real risk is on-device geometry, send it to Tier-4, not Jest.
- Drive a derived visual through the component, not its helper: feed `Number.NaN` /
  `Number.POSITIVE_INFINITY` through the mocked hook and assert the fallback renders.

### Stores (Zustand + AsyncStorage)

The mobile analog of save+reload: write a persisted blob, **rehydrate**, assert the
rehydrated state — and assert write-back by reading what actually persisted.

```ts
useClearsnakeStore.setState(useClearsnakeStore.getInitialState(), true);
await AsyncStorage.setItem('clearsnake-storage', JSON.stringify({ state: { ledDuty: 75 }, version: N }));
await useClearsnakeStore.persist.rehydrate();
expect(useClearsnakeStore.getState().ledDuty).toBe(75);

// write-back: act through the store, then assert the persisted projection
expect(selectPersistedClearsnakeState(useClearsnakeStore.getState())).toMatchObject({ ledDuty: 75 });
```

- Reset with `useClearsnakeStore.setState(useClearsnakeStore.getInitialState(), true)`,
  clear the AsyncStorage Jest mock, restore `console.log` spies (per `VERIFICATION.md`).
- Assert the **exact persisted keys** via `selectPersistedClearsnakeState`, not a
  whole-store snapshot.
- Legacy migrations live in `src/lib/clearsnake-store-migrations.ts` so migration
  behavior is tested without importing the production store.

### Async clients / board fetchers

Run the real fetch/parse/abort/timeout/retry path; mock only `fetch`. Assert the
parsed contract, the **error classification**, and the timeout/abort behavior.

```ts
jest.spyOn(globalThis, 'fetch').mockResolvedValue(
  createResponse({ ok: true, status: 200, body: firmwareReading }),
);
await expect(fetchBoardBattery(BATTERY_URL)).resolves.toMatchObject({ percent: 56, state: 'good' });

// failure mode is the high-value half:
jest.spyOn(globalThis, 'fetch').mockResolvedValue(createJsonRejectingResponse({ ok: true, status: 200 }));
await expect(fetchBoardBattery(BATTERY_URL)).rejects.toBeInstanceOf(BoardBatteryError);
```

- Cover the unhappy paths the board actually produces: non-200, invalid JSON,
  abort/timeout (`*_REQUEST_TIMEOUT_MS`), retry — each is a real device failure mode.

### Pure logic / selectors

Exercise the function for meaningful inputs. **Never** import a constant and assert
it equals the same constant from the same module.

- Prove behavior like production-vs-dev URL selection by toggling `__DEV__` /
  `EXPO_PUBLIC_CLEARSNAKE_INTERNAL_TOOLS` and asserting the **selected** value (see
  `board-urls.test.ts`).
- The one sanctioned constant-equality test is `board-url-defaults.test.ts`:
  release-facing default board URLs are themselves the contract.

### Native modules / parsers / transport

Assert the protocol contract and the native-event→store boundary; mock only the
native bridge edge.

- Parser/transport: assert the parsed terminal-log markers/required fields and the
  failure classification the host protocol depends on.
- Native event/status-probe/snapshot/recording: assert the event→store update, the
  native API call, media-library save/cleanup, and streaming failure modes.
- Geometry/touch-target/real-board behavior the harness can't represent → document
  Tier-4 device/manual proof; treat any incidental style assertion as supplemental.

**Stack anti-patterns:** exact `className` string assertions; `StyleSheet.flatten(...)`
/ numeric layout props (`gap`/`width`/`flex`); a direct helper-export test that
duplicates rendered behavior (make the helper private); palette/membership-only tests.

**Canonical files:**
- Component (RNTL, accessible/visible behavior): `mobile/src/components/camera-tab/__tests__/ConnectionIndicator.test.tsx`
- Store (AsyncStorage rehydrate + write-back): `mobile/src/lib/__tests__/clearsnake-store.test.ts`
- Store migrations (test without the production store): `mobile/src/lib/__tests__/clearsnake-store-migrations.test.ts`
- Async client (fetch/parse/timeout/error classification): `mobile/src/lib/__tests__/board-battery.test.ts`
- Pure selector (runtime-mode behavior, not constant-equality): `mobile/src/lib/__tests__/board-urls.test.ts`
- Documented constant-equality exception: `mobile/src/lib/__tests__/board-url-defaults.test.ts`
- Native parser/transport protocol contract: `mobile/src/lib/__tests__/native-mjpeg-perf-runner-host.test.ts`
