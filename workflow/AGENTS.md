# AGENTS.md Kernel - Portable Agentic Workflow

This is the portable operating kernel for coding agents. It is intentionally
project-agnostic. Local repo shims define stack facts, commands, and local constraints.

## Startup Adapters

Loaded as global agent guidance (Codex, Claude Code, or similar): treat as
workflow bootstrap, not repository policy.

- If a repo root contains `AGENTS.local.md`, read it before substantive work as
  a local-only workflow adapter — additive only; on conflict the tracked repo
  rule wins. Claude Code delta: also read a repo-root `CLAUDE.md`, composing the
  files in the order that adapter describes.

## Precedence

On conflict: (1) human instruction in the current session, (2) repo/company
policy, security rules, and code owner guidance, (3) the nearest repo/subtree
shim, (4) this kernel, (5) personal preferences and optional playbooks.

Do not use this workflow to bypass team review, CI, security controls, licensing rules,
or data-handling policies.

## Universal Quality Floor

- Prefer the simplest complete, repo-conventional solution that satisfies the
  current requirements and preserves correctness, safety, and maintainability.
  Added complexity must trace to a current requirement, observed failure, or
  established repo pattern; defer hypothetical future needs as follow-ups.
- Preserve public contracts unless the work item explicitly changes them.
- Do not modify unrelated files.
- Do not install dependencies, change toolchains, or edit generated artifacts
  without clear need and approval, except the isolated-worktree lockfile restore
  preauthorized below.
- Do not commit secrets, local credentials, device identifiers, personal paths,
  local workflow adapters, or kernel symlinks.
- Prefer existing repo patterns over new abstractions. Keep route/page/entry
  files thin: persistence layers own persistence, services own policy,
  validation, orchestration, transactions, and side effects.
- Add tests and verification proportional to risk; broader-gate selection and
  routing reporting follow the rules under Verification Tiers.
- Update docs only when behavior, contracts, setup, or user-visible workflow changes.
- If a command fails because of environment or permissions, report the blocker clearly instead of masking it.

## Test Quality Floor

Digest of `~/.agents/workflow/TESTING.md` (full doctrine there; this is also the
offline fallback REVIEW_RUBRIC.md uses when TESTING.md can't be opened).

- Tests protect behavior, contracts, failure modes, or user/system outcomes: a
  useful test fails iff the regression it guards against comes back.
- Sensitivity alone is insufficient: that recurrence must be a durable defect.
  When intentionally removing pure copy/markup/presentation, delete or relax only
  the obsolete assertion rather than invert it into absence coverage unless
  a raw ask, owning contract, or concrete continuing risk makes absence durably
  functional, safety/security/privacy/legal/compliance, accessibility,
  operational/forbidden-output/policy, or public-contract relevant. Classify by
  consequence, preserve every other durable assertion, and route ambiguity for
  decision.
- Before adding/changing a test, identify the behavior or contract protected, the
  original or plausible failure mode to catch, the real operation boundary
  exercised (service method,
  API route, job, import/export flow, UI interaction, persistence reload,
  integration boundary, CLI command), and any manual/provider/hardware/
  local-stack/database proof needed when that failure mode cannot be represented
  in the automated harness.
- Prefer running the real operation the product depends on: for persistence, save
  and reload through the relevant repository/ORM/service/API/UI boundary before
  asserting; for integrations, use the smallest deterministic boundary that still
  exercises the integration logic.
- Avoid tests whose only value is implementation shape (a config constant's value,
  generated SQL text, file/class/migration existence, mock call order, a snapshot
  without a behavioral assertion, a private helper's return) unless that shape is
  itself the contract or the test is clearly supplemental to a behavior-level test
  or a documented Tier-4 proof.
- Do not add automated tests just to increase apparent coverage. If no meaningful
  automated test is practical, say so and document the manual/provider/local-stack
  verification instead of inventing weak coverage.

## GitHub CLI

Use the `gh` CLI for all GitHub interactions. Do not use a GitHub MCP connector
when both are available.

## Destructive Action Policy

Every instance of an action below needs fresh, in-session operator approval.

Hard-to-reverse local/repo state:

- `git push` (incl. `--force`/`--force-with-lease`); `git reset --hard`,
  `checkout --`, `restore --`, `clean -f`; `git branch -D` / deleting branches;
  `commit --amend` or `rebase` rewriting pushed history; `git tag` create/delete
  + pushing tags.
- Hook/signing bypass flags: `--no-verify`, `--no-gpg-sign`,
  `-c commit.gpgsign=false`.
- Editing `.git/`, lockfiles, or `.git/info/exclude`.
- Installing/removing/upgrading/downgrading dependencies or toolchains, except
  the isolated-worktree lockfile restore preauthorization below.
- `rm -rf` against any target, or deleting tracked files outside the work item's
  stated scope.
- Deleting/recreating local databases, search indexes, containers, volumes,
  caches, or worktrees (`docker compose down -v`, `docker volume rm`,
  `supabase db reset`, `git worktree remove --force`, or aliases wrapping those).
  Exception: a repo-documented disposable DB test harness needs no per-run
  approval when its unchanged command is constrained to loopback/local Docker
  and a harness-owned test namespace. Any command, target, wrapper, namespace,
  migration, reset, ingest, or persistent-database difference remains gated.

Shared-state and externally visible actions:

- `gh pr` create/edit/merge/close/review; `gh issue` create/close/comment/edit;
  `gh release` create/delete; `gh repo edit`; `gh api` POST/PATCH/PUT/DELETE.
- Mutating tracker objects (Linear, Jira, …) via any CLI/connector/MCP/API.
- Messages to Slack, email, webhooks, or external services.
- CI/CD config, secrets, or branch-protection changes.
- Mutating cloud/deploy/db/payment/DNS/monitoring/infra providers (`aws`,
  `gcloud`, `kubectl`, `terraform`, `pulumi`, `sst`, `vercel`, `supabase`,
  `stripe`, `fly`, `railway`) — create/update/delete/deploy/migrate/promote/
  reindex/secret-change or touching staging/prod data.
- Migrations, backfills, imports, reindexes, seed loads, or data-repair against
  any non-local environment.

Operating rules:

- One explicit in-session approval ("yes"/"approved"/"go ahead"/"open the PR"/
  any natural equivalent) authorizes the action; then state the exact command and
  run it (stating it IS the announcement, not a second ask). One approval covers
  that action AND its natural sub-steps: a PR includes applying the labels you
  showed + posting a comment that was part of the plan; an issue includes its
  labels — one approval, not three. Re-ask only if the command materially
  diverges — a different repo/target, broader scope, an unstated mutation, or a
  body/label/comment the operator has not seen. "ok"/silence is not yes.
- **Isolated-worktree bootstrap is preauthorized.** In a newly created,
  task-specific git worktree, before substantive work: if the worktree lacks
  `AGENTS.local.md` but the source checkout has one, copy it into the worktree
  root, read it, and never stage it. Then announce and run the repository's
  existing immutable lockfile install without asking again: for example,
  `pnpm install --frozen-lockfile`, `npm ci`, `yarn install --immutable`,
  `bun install --frozen-lockfile`, or the exact repo-documented equivalent.
  This applies only when the dependency manifests and lockfile already match
  the worktree's checked-out commit. Confirm afterward that the command did not
  modify them. It does not authorize adding/upgrading/removing packages, a
  non-immutable install, global installation, or installing/changing the package
  manager or toolchain; those still require fresh approval.
- For destructive local-data commands, state the exact store/volume/worktree/
  cache/container target and whether data loss is expected before asking.
- For provider/db mutations, prefer a read-only check or dry-run first when
  supported; a successful dry-run does not authorize the real mutation.
- If a pre-commit hook or CI check fails, never bypass with `--no-verify` or
  similar — stop and report.
- If unsure whether an action belongs here, default to asking.

## Startup Routing

Pick one path; switch if the session changes.

**A) Implement an existing work item** (ticket/issue/bug/explicit task):
1. Read the work item + linked PR/context; read the nearest repo/subtree shim for
   touched files. Reopen any named spec after compaction/resume and before
   handoff; compaction never broadens scope or authority.
2. Restate goal, non-goals, acceptance criteria, verification; name in-scope
   files and risky/out-of-scope areas.
3. `git status` before branching/editing; never discard unowned changes.
4. Spot-check the spec's load-bearing source claims (cited file:line wiring
   points, referenced symbols) against the tree; if a path moved or the code
   contradicts an assumption, surface it and adjust scope — don't code against a
   stale claim.
5. Switch to the team-standard branch when edits are expected; implement
   minimally.
6. Select + run tiered verification (Verification Tiers; commands from the shim)
   and report routing.
7. Hand off per Implementation Completion Handoff; patch findings + rerun per the
   Review Loop.
8. Open/update PR or push only when authorized; on PR open keep review evidence
   local per PR Handoff.

**B) Plan work** (feature shaping, final-spec prep, task splitting, unclear
scope): read product/docs/code context; run a Domain Pass when
terminology/lifecycle/cross-boundary behavior changes; produce a reviewable spec
(self-contained scope, non-goals, acceptance criteria, exact verification
commands, labels/branch when relevant, any approval-gated work). No code changes
unless explicitly asked.

**C) Review a PR or diff:** per `REVIEW_RUBRIC.md`.

**D) Docs/architecture/pattern maintenance:** read only docs in scope; keep them
aligned with actual commands, runtime versions, and contracts.

## Kickoff Templates

Canonical kickoff prompts live one-per-file in `~/.agents/workflow/kickoffs/`;
each handoff skill reads only its own. `planner-directive.md` is shared —
appended to the spec reviews.

**Fidelity rule:** paste the matching `kickoffs/*.md` template verbatim with
placeholders filled — do not paraphrase, restructure, or invent your own shape;
it is load-bearing for downstream agents. If you cannot read it, or the kickoff
you received looks incomplete, say so and ask the operator rather than guessing.

## Work Item Model

- **Task** — default PR-sized implementation unit. Default: one Task → one branch
  → one PR.

Plan the broader destination when needed, but keep the current Task
proportionate: one independently reviewable outcome and risk boundary that
leaves a valid state if later work never lands. Split only when concerns can be
reviewed or proven independently; keep them together when splitting would
create an invalid intermediate state or shape-only ceremony. Downstream Tasks
may be sketched, but re-ground them against merged predecessors before
implementation.

## Docs Impact Check

Every implementation makes an explicit docs-impact decision before review
handoff. Does the change affect user-visible behavior or product terminology;
setup/build/local-iteration commands; verification gates, coverage policy, or
manual-QA expectations; architecture boundaries, module ownership, or route/path
maps; board/firmware/simulator/network/API contracts; or release/privacy/
distribution evidence?

- If yes: update the owning tracked doc in the SAME PR — prefer the established
  authority over a new doc (ADRs only for hard-to-reverse, surprising,
  real-trade-off decisions) — and include a `## Docs impact` PR-body section
  naming what changed.
- If no: record that decision in the review handoff, but omit docs impact from
  the PR body entirely.

## Planning Artifact Cleanup

When the operator says an issue or PR landed, clean local planning artifacts
before moving on — the full sequence lives in `~/.agents/workflow/PLANS.md`
("Artifact cleanup on land").

## Implementation Completion Handoff

When finishing an implementation, hand off for review: a brief summary +
verification results, then spawn exactly one fresh-context reviewer (Review
Kickoff) and announce the handoff (what + range), unless the entire diff
qualifies for the documentation-only off-ramp in `~/.agents/workflow/HANDOFF.md`.
No second inner reviewer unless the operator explicitly asks this session.
Mechanics — sequencing, freshness, the independence seal, re-review reuse, the
automated Claude outer gate, and the ritual→skill index — live in
`~/.agents/workflow/HANDOFF.md`.

Two independent approved verdicts before PR handoff by default: the implementer
owns the spawned inner reviewer and launches a required `outerreview` in a fresh
Claude Code session after the inner loop converges. The operator owns any waiver
and the other-app fallback when Claude performed the implementation.

Review floor — every implementation gets ≥1 inner review unless the entire diff
qualifies for the narrow documentation-only self-check in HANDOFF.md. Nothing
reaches a PR without either an APPROVED inner review or that recorded off-ramp.
The outer gate is REQUIRED whenever the diff touches a canonical risk-surface
(list owned by HANDOFF.md "Outer-gate waivability") OR the inner review was
ever ACTIONABLE on a substantive finding; it is operator-waivable ONLY per the
exact conditions there. The implementer states
`outer gate: required | waivable — <why>`; required gates proceed autonomously,
while the OPERATOR makes any waive call.

## PR Handoff

When the operator asks to open/update a PR, make the review record available for
handoff without making it default public PR content — keep prompts, verdicts,
findings + resolutions, post-patch verification, deferred follow-ups, and
residual risk / Tier-4 gates local per PLANS.md.

Compose the PR body in the `kickoffs/pr-body.md` shape, which owns the section
order, closing-ref rules, review-summary policy, and teammate-readable language
for PR titles, bodies, and public comments. Determine labels from the source
issue + local policy: carry over labels still describing the diff, omit stale
ones, state the final list. All externally visible GitHub mutations follow the
Destructive Action Policy.

## Domain Pass

Run before final-spec promotion / tracker publication when work introduces or
overloads a core noun, changes lifecycle or state meaning, crosses
app/service/provider/device boundaries, affects user-facing terminology, creates
a new module/service boundary, or is high-risk/multi-step. Output: canonical
terms; avoided synonyms (when important); unresolved decisions; an ADR/decision
record only if the decision is hard to reverse, surprising, and a real trade-off.
Skip for isolated bug fixes, visual polish, small refactors, and dependency
maintenance with stable terminology.

## Verification Tiers

- **Tier 1 - Loop**: smallest local checks proving changed behavior, such as a
  focused unit/component test, story/play test, lint/typecheck for the touched
  package, or a narrow manual repro.
- **Tier 2 - Patch**: targeted reruns after review findings or non-trivial
  patches.
- **Tier 3 - Gate**: broader repo or surface verification before final/PR, such
  as affected lint/typecheck/test, coverage-producing suites, build, boundary,
  contract, e2e-smoke, full e2e, or other repo-provided PR-parity gates selected
  for the changed surface.
- **Tier 4 - Operator**: manual, hardware, live-provider, destructive,
  local-data-reset, expensive, or environment-sensitive checks that need an
  operator-prepared environment or fresh approval.

Rules:

- Prefer repo-provided verify commands. Before implementation + PR handoff, make
  routing explicit: commands run; gates intentionally not selected (each with a
  short reason — not a self-judged "only if a reviewer would ask"); gates blocked;
  remaining Tier-4/operator work.
- Verification validity follows causal impact, not commit freshness. Run every
  repository-required gate for behavior the delta changes or could plausibly
  affect once before first review. After it is green for the current
  task/worktree, a new commit, review patch, final-tip handoff, or PR handoff
  does not by itself invalidate it. Account for every intervening delta and
  rerun only checks that could fail because of them; for composite gates, use
  affected constituent checks through the repository's documented
  standalone/public entry points. Rerun the full gate only when the delta spans
  surfaces, touches shared/build/test infrastructure, makes prior evidence
  suspect, or no valid broad evidence remains. If repository policy does not
  require a rerun and you cannot name a plausible failure path from the delta to
  the gate, do not rerun it. Report reused evidence with its evidence point and
  causal rationale; never claim the composite command ran at the current tip
  unless it did.
- Choose broader local gates by changed surface + risk — not by whether they sit
  in the default PR CI path. Don't treat optional/nightly/CI-only gates as
  impossible to run locally; run them when task risk justifies and the env is
  prepared.
- When a change creates/moves/changes a shared package/module/export for another
  app or package to consume, verification must prove the exact public import path
  at that consumer's real build/runtime boundary — a sibling export, internal
  import, or typecheck-only proof does not count unless that IS the consumer
  boundary.
- User-facing UI: run targeted automated coverage + visual/manual QA; apply
  FRONTEND.md, and for visual-design work capture the surface to verify (per
  FRONTEND.md's oracle). Escalate to e2e-smoke/full-e2e when the change touches
  routing, auth, checkout, multi-page workflows, real-data integration, or a
  regression-prone path.
- API/schema/data/integration: consider contract tests, builds, local-stack
  verification, and service e2e in addition to package tests.
- For no-contract refactors, verify parity for status/shape/error/side effects.
- Don't run live/provider/hardware checks from an agent unless the env is
  explicitly prepared; if sandboxing blocks services/hardware/localhost/network,
  stop after one diagnostic run and escalate or ask the operator for output.
- Final summaries must name commands run and results.

## Review Loop

- `REVIEW_RUBRIC.md` is the reviewer's manual (verdict semantics, stance, blocking
  rules); `HANDOFF.md` owns outer-gate mechanics. Approve clean only after naming
  the checks run.
- Patch only listed findings unless scope expands; rerun targeted verification.
- Extra review passes whenever post-review patches are non-trivial, touch
  lifecycle/state/concurrency, change acceptance behavior, rewrite or add a
  test for a test-quality finding, or the operator asks; skip only for a truly
  trivial stated patch (e.g. a corrected import path in one file). This does
  not reopen an inner reviewer for an outer-owned implementation or spec patch;
  HANDOFF.md routes those patches directly back to the same outer reviewer.

## Output Budget

- Do not restate stable repo rules unless they matter.
- Final summaries should include changed files, intent, verification, and known follow-ups.

## Local Repo Facts Contract

Each local repo shim defines only facts the kernel cannot know: stack, package
manager, repo layout, branch/PR/ticket conventions, verification commands by
tier, manual/hardware gates, sensitive files, pitfalls, subtree rules. Shims stay
small and local-only unless the team wants them committed. Put durable domain
vocabulary in `CONTEXT.md`, not in every agent instruction file.
