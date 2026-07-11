# AGENTS.md Kernel - Portable Agentic Workflow

This is the portable operating kernel for coding agents. It is intentionally
project-agnostic. Local repo shims define stack facts, commands, and local constraints.

## Startup Adapters

Loaded as global agent guidance (Codex, Claude Code, or similar): treat as
workflow bootstrap, not repository policy.

- Tracked repo/company/security instructions are authoritative over this kernel.
- If a repo root contains `AGENTS.local.md`, read it before substantive work as
  a local-only workflow adapter.
- Local adapters are additive; on conflict with tracked repo rules, the tracked
  rule wins (see Precedence).
- Do not commit local workflow adapters, personal paths, credentials, or kernel
  symlinks unless the repo explicitly asks for them.
- Claude Code delta: also read a repo-root `CLAUDE.md` as the Claude project
  adapter; when it imports or points at `AGENTS.md` and `AGENTS.local.md`,
  compose those files in the order the adapter describes.

## Precedence

When instructions conflict, follow this order:

1. Human instruction in the current session.
2. Repo or company policy, security rules, and code owner guidance.
3. Nearest repo/subtree `AGENTS.md` or equivalent local shim.
4. This portable kernel.
5. Personal preferences and optional playbooks.

Do not use this workflow to bypass team review, CI, security controls, licensing rules,
or data-handling policies.

## Universal Quality Floor

- Keep changes surgical and scoped to the work item. Capture out-of-scope work as a follow-up rather than expanding the change.
- Preserve public contracts unless the work item explicitly changes them.
- Do not modify unrelated files.
- Do not install dependencies, change toolchains, or edit generated artifacts without clear need and approval.
- Do not commit secrets, local credentials, device identifiers, or personal paths.
- Prefer existing repo patterns over new abstractions.
- Add tests and verification proportional to risk; broader-gate selection and
  routing reporting follow the rules under Verification Tiers.
- Update docs only when behavior, contracts, setup, or user-visible workflow changes.
- If a command fails because of environment or permissions, report the blocker clearly instead of masking it.

## Test Quality Floor

Digest of `~/.agents/workflow/TESTING.md` (full doctrine there; this is also the
offline fallback REVIEW_RUBRIC.md uses when TESTING.md can't be opened).

- Tests protect behavior, contracts, failure modes, or user/system outcomes: a
  useful test fails iff the regression it guards against comes back.
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

Use the `gh` CLI for all GitHub interactions — issues, PRs, releases, comments,
reviews, and `gh api` calls. Do not use a GitHub MCP connector when both are
available.

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
- Installing/removing/upgrading/downgrading dependencies or toolchains.
- `rm -rf`, or deleting tracked files outside the work item's stated scope.
- Deleting/recreating local databases, search indexes, containers, volumes,
  caches, or worktrees (`docker compose down -v`, `docker volume rm`,
  `supabase db reset`, `git worktree remove --force`, or aliases wrapping those).

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
- For destructive local-data commands, state the exact store/volume/worktree/
  cache/container target and whether data loss is expected before asking.
- For provider/db mutations, prefer a read-only check or dry-run first when
  supported; a successful dry-run does not authorize the real mutation.
- If a pre-commit hook or CI check fails, never bypass with `--no-verify` or
  similar — stop and report.
- If unsure whether an action belongs here, default to asking.

Future mechanical enforcement and automatic verification-hook exploration is
captured in `COMMAND_GUARDRAILS_AND_VERIFICATION_HOOKS.md`.

## Startup Routing

Pick one path; switch if the session changes.

Living evidence from the first autonomous multi-task orchestration experiment is
recorded in `AUTONOMOUS_ORCHESTRATION_FIELD_NOTES.md`; it is observational, not
policy.

The proposed coordinator-owned readiness contract for fresh implementation
worktrees is recorded in `WORKTREE_ENVIRONMENT_BOOTSTRAP.md`; until it is
implemented, kickoffs should explicitly name repo commands, ignored dependency/
evidence inputs, preflight ownership, and the rule that blocked verification is
not success.

A candidate fifth startup path—end-to-end program orchestration—is drafted in
`ORCHESTRATOR_MODE.md`. It is not active policy yet; use Startup Routing A-D
until the operator reviews and ratifies that mode.

**A) Implement an existing work item** (ticket/issue/bug/explicit task):
1. Read the work item + linked PR/context; read the nearest repo/subtree shim for
   touched files.
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

**C) Review a PR or diff:** review changed behavior before style; focus on
correctness, regressions, contract drift, security, data loss, missing
verification; lead with findings by severity + file:line; return
`APPROVED`/`ACTIONABLE` per REVIEW_RUBRIC.md.

**D) Docs/architecture/pattern maintenance:** read only docs in scope; keep them
aligned with actual commands, runtime versions, and contracts.

## Kickoff Templates

Canonical kickoff prompts live one-per-file in `~/.agents/workflow/kickoffs/`;
each handoff skill reads only its own. Index: `planning.md`, `domain-pass.md`,
`final-spec-promotion.md`, `planner-directive.md` (shared — appended to the spec
reviews), `spec-review.md`, `spec-re-review.md`, `execution.md`, `review.md`,
`re-review.md`, `external-pr-review.md`, `pr-body.md`, `post-plan-grill.md`.

**Fidelity rule:** paste the matching `kickoffs/*.md` template verbatim with
placeholders filled — do not paraphrase, restructure, or invent your own shape;
it is load-bearing for downstream agents. If you cannot read it, or the kickoff
you received looks incomplete, say so and ask the operator rather than guessing.

## Work Item Model

Neutral objects (works with GitHub Issues, Jira, Linear, or a written prompt):

- **Task** — default PR-sized implementation unit. Default: one Task → one branch
  → one PR.
- **Spec** — one living planning artifact evolving rough → review-ready → final →
  promoted → implemented; a final spec should be publishable as the tracker issue
  body unless it must be split, redacted, or substantially reshaped.
- **Decision** — a short decision lock with rationale.

Split work only when it improves delivery or risk control: too large to review
safely; a contract/schema change that should land separately; hardware/manual
validation gating later software work; migration/state-machine work needing
staging; or independent parts reviewable/mergeable without coordination risk.

## Definition Of Ready

A Task is ready when:

- goal and non-goals are clear
- acceptance criteria are testable
- exact verification commands are listed
- planned tests identify the behavior/failure mode they protect, or explain why
  only manual/Tier 4 proof is meaningful
- verification tier and any escalation gates are named
- affected surfaces and owners are known
- dependencies and manual/hardware requirements are called out
- contract changes are explicit
- domain terms are resolved or open questions are named

## Definition Of Done

A Task is done when:

- implementation satisfies acceptance criteria
- selected verification passed, or blockers documented with exact failed commands
- verification routing reported (see Verification Tiers)
- tests/docs changed where risk requires it; new tests protect intended behavior,
  or implementation-shape coverage is justified as supplemental/contractual
- docs impact checked (see Docs Impact Check), or the agent stated `Docs impact: none`
- the Implementation Completion Handoff contract was met
- if a PR was opened, it satisfies PR Handoff
- follow-up work is explicitly captured, not hidden in prose

## Docs Impact Check

Every implementation makes an explicit docs-impact decision before review
handoff. Does the change affect any of: user-visible behavior or product
terminology; setup/install/build/local-iteration commands; verification
gates/coverage policy/manual-QA expectations; architecture boundaries, module
ownership, or route/path maps; board/firmware/simulator/network/API contracts;
performance-validation policy or durable evidence; release/privacy/app-store/
distribution evidence?

- If yes: update the owning tracked doc in the SAME PR — prefer the established
  authority over a new doc (root `README.md`; setup docs; verification docs;
  architecture docs; runbooks/history; ADRs only for hard-to-reverse, surprising,
  real-trade-off decisions).
- If no: state `Docs impact: none` in the summary and as the one-line PR-body
  footer (not a standalone section).

## Planning Artifact Cleanup

When the operator says an issue or PR landed, clean local planning artifacts
before moving on — the full sequence lives in `~/.agents/workflow/PLANS.md`
("Artifact cleanup on land").

## Implementation Completion Handoff

When finishing an implementation, hand off for review: a brief summary +
verification results, then spawn exactly one fresh-context reviewer (Review
Kickoff) and announce the handoff (what + range). No second reviewer unless the
operator explicitly asks this session. Mechanics — sequencing, freshness, the
independence seal, re-review reuse, and the ritual→skill index — live in
`~/.agents/workflow/HANDOFF.md`.

Two independent approved verdicts before PR handoff by default: the implementer
owns the spawned inner reviewer; the operator owns the outer gate
(`outerreview` / `outerspecreview`), which self-populates from the work-item
folder + live range and runs on the final tip after the inner loop converges.

Review floor — the inner loop (`implreview` → `implrereview` to APPROVED) is
NEVER skippable: every implementation gets ≥1 review, and nothing reaches a PR
without one. Only the outer gate is ever waived. It is REQUIRED whenever the diff
touches a canonical risk-surface — migration/schema/persisted-state · auth ·
contract/API · data-loss · security · provider boundary · dependency · toolchain
— OR the inner review was ever ACTIONABLE on a substantive finding; it is
operator-waivable ONLY for a first-pass-clean, mechanically-trivial,
zero-risk-surface change (exact a/b/c conditions in HANDOFF.md "Outer-gate
waivability"). The implementer states `outer gate: required | waivable — <why>`;
the OPERATOR makes the waive call.

## PR Handoff

When the operator asks to open/update a PR, make the review record available for
handoff without making it default public PR content — keep prompts, verdicts,
findings + resolutions, post-patch verification, deferred follow-ups, and
residual risk / Tier-4 gates local per PLANS.md.

1. Compose the PR body in the `kickoffs/pr-body.md` shape. Closing refs: GitHub
   `Fixes #<n>` only when merge fully resolves it, else `Refs`/`Part of`; Linear
   `Closes <full url>` when fully resolved, else `Part of <url>`.
2. No standalone `## Review Summary` by default; mention a review finding only
   when it materially changes reviewer context (patched edge case, deferred
   follow-up, residual risk). A separate review-record comment (starting
   `# Review Notes`) only when requested.
3. Determine labels from the source issue + local policy: carry over labels still
   describing the diff, omit stale ones, state the final list.
4. Show the PR body, any comment, the labels, repo, target branch/PR, and
   requested action before asking for one bundled approval. Create/update only
   when authorized (labels via `gh pr create` / `gh pr edit --add-label`; an
   authorized review-record comment via `gh pr comment`). All externally visible
   GitHub mutations follow the Destructive Action Policy.

## Domain Pass

Run before final-spec promotion / tracker publication when work introduces or
overloads a core noun, changes lifecycle or state meaning, crosses
app/service/provider/device boundaries, affects user-facing terminology, creates
a new module/service boundary, or is high-risk/multi-step. Output: canonical
terms; avoided synonyms (when important); unresolved decisions; an ADR/decision
record only if the decision is hard to reverse, surprising, and a real trade-off.
Skip for isolated bug fixes, visual polish, small refactors, and dependency
maintenance with stable terminology.

## Implementation Defaults

- Read code before editing.
- Prefer structured APIs/parsers over ad hoc text manipulation.
- Keep route/page/entry files thin; move orchestration to existing service/hook/module layers.
- Repositories or persistence layers own persistence details only.
- Services own policy, validation, orchestration, transactions, and side effects.
- UI state should make loading, error, empty, disabled, and retry states explicit.
- For no-contract refactors, verify parity for status/shape/error/side effects.

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
- Don't run live/provider/hardware checks from an agent unless the env is
  explicitly prepared; if sandboxing blocks services/hardware/localhost/network,
  stop after one diagnostic run and escalate or ask the operator for output.
- Final summaries must name commands run and results.

## Review Loop

- Verdict/findings semantics (`APPROVED`/`ACTIONABLE`, blocking rules) and the
  adversarial checks (its Stance section) are owned by `REVIEW_RUBRIC.md`;
  approve clean only after naming the checks run.
- Patch only listed findings unless scope expands; rerun targeted verification.
- Both default independent fresh-context reviews run the full `REVIEW_RUBRIC.md`;
  outer-gate mechanics live in `HANDOFF.md`. Automated-reviewer (CodeRabbit)
  path-exclusion handling: see REVIEW_RUBRIC.md "Automated-reviewer awareness".
- Extra review passes whenever post-review patches are non-trivial, touch
  lifecycle/state/concurrency, change acceptance behavior, or the operator asks.

Reviewer priorities + full detail: `REVIEW_RUBRIC.md`.

## Output Budget

- Be concise.
- Do not restate stable repo rules unless they matter.
- Show failed command context only when useful.
- Final summaries should include changed files, intent, verification, and known follow-ups.

## Local Repo Facts Contract

Each local repo shim should define only facts the kernel cannot know: stack and
package manager; repo layout; branch/PR/ticket conventions; verification
commands by tier; manual/hardware gates; forbidden or sensitive files; common
pitfalls; subtree-specific rules.

Shims should stay small and local-only unless the team wants them committed. Put durable
domain vocabulary in `CONTEXT.md`, not in every agent instruction file.
