# AGENTS.md Kernel - Portable Agentic Workflow

This is the portable operating kernel for coding agents. It is intentionally
project-agnostic. Local repo shims define stack facts, commands, and local constraints.

## Startup Adapters

When this file is loaded as global agent guidance (Codex, Claude Code, or a
similar host), treat it as workflow bootstrap, not repository policy.

- Tracked repo/company/security instructions are authoritative over this kernel.
- If a repo root contains `AGENTS.local.md`, read it before substantive work as
  a local-only workflow adapter.
- Treat local adapters as additive; on conflict with tracked repo rules, the
  tracked rule wins (see Precedence).
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

- Keep changes surgical and scoped to the work item. If you discover work outside the stated scope, capture it as a follow-up rather than expand the change.
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

- Tests protect behavior, contracts, failure modes, or user/system outcomes. A
  useful test would fail iff the regression it protects against came back.
- Before adding or changing a test, identify: the behavior or contract
  protected, the original or plausible failure mode to catch, the real
  operation boundary exercised (service method, API route, job, import/export
  flow, UI interaction, persistence reload, integration boundary, CLI command),
  and any manual/provider/hardware/local-stack/database proof needed when the
  meaningful failure mode cannot be represented in the automated harness.
- Prefer running the real operation the product or system depends on. For
  persistence, save and reload through the relevant repository/ORM/service/
  API/UI boundary before asserting; for integrations, use the smallest
  deterministic boundary that still exercises the integration logic.
- Avoid tests whose only value is implementation shape (a config constant's
  value, generated SQL text, file/class/migration existence, mock call order,
  a snapshot without a behavioral assertion, a private helper's return) unless
  that shape is itself the contract or the test is clearly supplemental to a
  behavior-level test or a documented Tier 4 proof.
- Do not add automated tests just to increase apparent coverage. If no
  meaningful automated test is practical, say so and document the
  manual/provider/local-stack verification instead of inventing weak coverage.

Full doctrine lives in `~/.agents/workflow/TESTING.md`; this digest is the
offline fallback (REVIEW_RUBRIC.md falls back to it when TESTING.md cannot be
opened).

## GitHub CLI

Use the `gh` CLI for all GitHub interactions — issues, PRs, releases, comments,
reviews, and `gh api` calls. Do not use a GitHub MCP connector when both are
available.

## Destructive Action Policy

Every instance of an action below requires fresh, in-session operator approval.

Hard-to-reverse local/repo state:

- `git push`, including `--force` and `--force-with-lease`
- `git reset --hard`, `git checkout --`, `git restore --`, `git clean -f`
- `git branch -D`, deleting branches local or remote
- `git commit --amend` on pushed commits, `git rebase` rewriting pushed history
- `git tag` create/delete, pushing tags
- Flags that skip hooks or signing: `--no-verify`, `--no-gpg-sign`,
  `-c commit.gpgsign=false`
- Editing `.git/`, lockfiles, or `.git/info/exclude`
- Installing, removing, upgrading, or downgrading dependencies or toolchains
- `rm -rf`, deleting tracked files outside the work item's stated scope
- Deleting or recreating local databases, search indexes, containers, volumes,
  caches, or worktrees, including commands like `docker compose down -v`,
  `docker volume rm`, `supabase db reset`, `git worktree remove --force`, or
  repo aliases that wrap those operations

Shared-state and externally visible actions:

- `gh pr create` / `edit` / `merge` / `close` / `review`
- `gh issue create` / `close` / `comment` / `edit`
- `gh release create` / `delete`, `gh repo edit`
- `gh api` calls using `POST`, `PATCH`, `PUT`, or `DELETE`
- Mutating issue tracker objects through Linear, Jira, or similar CLIs,
  connectors, MCP tools, or APIs
- Sending messages to Slack, email, webhooks, or external services
- Modifying CI/CD configuration, secrets, or branch-protection rules
- Mutating cloud, deployment, database, payment, DNS, monitoring, or
  infrastructure providers with CLIs, SDKs, MCP tools, or APIs, including
  commands like `aws`, `gcloud`, `kubectl`, `terraform`, `pulumi`, `sst`,
  `vercel`, `supabase`, `stripe`, `fly`, and `railway` when they create,
  update, delete, deploy, migrate, promote, reindex, change secrets, or touch
  staging/production data
- Running migrations, backfills, imports, reindexes, seed loads, or data repair
  commands against any non-local environment

Operating rules:

- One explicit in-session approval — "yes" / "approved" / "go ahead" / "open
  the PR" / any natural equivalent — authorizes the action; then state the exact
  command and run it (stating it IS the announcement, not a second ask). One
  approval covers that action AND its natural sub-steps: creating a PR includes
  applying the labels you showed and posting a comment that was part of the plan;
  opening an issue includes its labels — one approval, not three. Re-ask only if
  the command materially diverges from what was approved — a different repo or
  target, broader scope, an unstated mutation, or a body/label/comment the
  operator has not seen. "ok" / silence is not yes.
- For destructive local data commands, state the exact data store, volume,
  worktree, cache, or container target and whether data loss is expected before
  asking for approval.
- For provider or database mutations, prefer a read-only check or dry-run first
  when the tool supports it. A successful dry-run does not authorize the real
  mutation.
- If a pre-commit hook or CI check fails, never bypass with `--no-verify` or
  similar. Stop and report the failure.
- If unsure whether an action belongs here, default to asking.

## Startup Routing

Choose one path. If the session changes, switch paths.

### A) Implement Existing Work Item

Use this when a ticket, issue, bug, or explicit task already exists.

1. Read the work item and any linked PR/context first.
2. Read the nearest repo/subtree shim for touched files.
3. Restate goal, non-goals, acceptance criteria, and verification.
4. Identify files in scope and explicitly risky/out-of-scope areas.
5. Check current git status before branching or editing; never discard unowned
   changes.
5b. Before editing, spot-check the spec's load-bearing source claims (cited
   file:line wiring points and referenced symbols) against the current tree; if
   a claimed path has moved or the code contradicts a spec assumption, surface
   the conflict and adjust scope instead of coding against the stale claim.
6. Create or switch to the team-standard branch when edits are expected.
7. Implement minimally.
8. Select and run tiered verification based on changed surface and risk. Use the
   local repo shim for exact commands. Run broader local gates such as build,
   contract, e2e, visual/manual QA, or local-stack QA when the task touches the
   matching surface or the operator asks for extra confidence; report routing
   (gates run / not selected / blocked) per the Verification Tiers rules.
9. Hand off for review per "Implementation Completion Handoff"; patch actionable
   findings in scope and rerun targeted verification per the Review Loop before
   continuing.
10. Open/update PR or push only when authorized by the user/team flow.
11. When a PR is opened, keep detailed review evidence local by default. Include
    review findings in the PR body only when they materially help the reviewer
    understand the change, residual risk, or follow-up work. Post a separate
    review-record comment only when the operator requests it.

### B) Plan Work

Use this for feature shaping, final-spec preparation, task splitting, or unclear scope.

1. Read relevant product/docs/code context.
2. Run a Domain Pass when terminology, lifecycle state, or cross-boundary behavior changes.
3. Produce a reviewable spec that can evolve into the final tracker issue body:
   self-contained scope, non-goals, acceptance criteria, exact verification
   commands, labels/branch guidance when relevant, and any approval-gated work.
4. Do not make code changes during planning unless explicitly asked.

### C) Review PR or Diff

Use this when asked for review.

1. Review changed behavior first, not style first.
2. Focus on correctness, regressions, contract drift, security, data loss, and missing verification.
3. Lead with findings ordered by severity and file/line.
4. Return `APPROVED` / `ACTIONABLE` per the verdict and blocking semantics owned
   by REVIEW_RUBRIC.md.

### D) Docs, Architecture, or Pattern Maintenance

Read only docs relevant to the requested scope. Keep docs aligned with actual commands,
runtime versions, and contracts.

## Kickoff Templates

Canonical kickoff prompts live in `~/.agents/workflow/KICKOFFS.md`: Planning,
Domain Pass, Final Spec Promotion, Spec Review, Spec Re-Review,
Execution/Implementation, Review, Re-Review, External PR Review,
PR Body / Optional Review Notes, Post-Plan Grill.

**Fidelity rule:** When asked to hand off a kickoff to the operator or another
agent, paste the matching section from KICKOFFS.md verbatim with placeholders
filled. Do not paraphrase, summarize, restructure, or invent your own shape.
The structure is load-bearing for downstream agents. If you cannot read
KICKOFFS.md in this environment, say so and ask the operator to provide the
template.

If the kickoff you received looks incomplete or malformed, consult that file
for the canonical shape and ask the operator to fill the gaps before starting.

## Work Item Model

Use neutral objects so the workflow works with GitHub Issues, Jira, Linear, or a written
prompt.

- **Task**: default PR-sized implementation unit.
- **Spec**: one living planning artifact that evolves from rough to
  review-ready to final to promoted to implemented. A final spec should be
  publishable as the tracker issue body unless it must be split, redacted, or
  substantially reshaped.
- **Decision**: short decision lock with rationale.

Default: one Task -> one branch -> one PR.

Split work only when it improves delivery or risk control:

- too large to review safely
- contract or schema change should land separately
- hardware/manual validation gates later software work
- migration or state-machine work needs staging
- independent parts can be reviewed and merged without coordination risk

Parallel worktree execution is optional and deferred. Do not make it part of the core
workflow until it is used often enough to justify the extra surface area.

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
- selected verification passed or blockers are documented with exact failed
  commands
- verification routing is reported per the explicit verification-routing rule
  under Verification Tiers
- tests/docs changed where risk requires it; new tests protect the intended
  behavior rather than only implementation shape, or the implementation-shape
  coverage is justified as supplemental/contractual
- docs impact was checked; authoritative docs were updated when behavior,
  contracts, setup, verification, or user-visible workflow changed, or the
  agent stated `Docs impact: none`
- the Implementation Completion Handoff contract was met
- if a PR was opened, the PR body captures the change, validation, and any
  material residual risk; when a separate review-record comment was requested,
  it is posted or the blocker is documented
- follow-up work is explicitly captured, not hidden in prose

## Docs Impact Check

Every implementation must make an explicit docs-impact decision before review
handoff.

Check whether the change affects:

- user-visible behavior or product terminology
- setup, install, build, or local iteration commands
- verification gates, coverage policy, or manual QA expectations
- app architecture boundaries, module ownership, or route/path maps
- board, firmware, simulator, network, or API contracts
- performance validation policy or durable performance evidence
- release, privacy, app-store, or distribution evidence

If yes, update the owning tracked doc in the same PR. Prefer the established
authority instead of creating a new doc or repeating content:

- root `README.md` for repo front door and documentation map
- setup docs for onboarding and daily commands
- verification docs for test, build, coverage, and manual gates
- architecture docs for app maps and cross-boundary contracts
- runbooks/history docs for repeatable validation and durable evidence
- ADRs only for decisions that are hard to reverse, surprising without
  context, and the result of a real trade-off

If no, state `Docs impact: none` in the implementation summary and as the
one-line PR-body footer (not a standalone section).
Do not add documentation just to appear thorough. Prefer concise updates that
reduce future confusion, remove stale text, or point readers to the existing
authority.

## Planning Artifact Cleanup

When the operator says an issue or PR has landed, planning agents must clean
local planning artifacts before moving on.

Required:

- Confirm the issue or PR state with the tracker.
- Delete obsolete local issue drafts, PR body drafts, review-note drafts,
  kickoff prompts, and one-off review prompts now represented by the tracker or
  PR.
- After issue creation, advance the same living spec through its lifecycle
  instead of deleting it by default — lifecycle statuses and the
  plans-directory layout live in `~/.agents/workflow/PLANS.md`. Delete only
  transient split/redaction issue drafts or prompts at that point.
- Archive only durable context: reusable specs, verification reports, audit
  reports, ADR-like rationale, or cross-issue policy decisions.
- Move still-actionable future work to backlog, or keep it active only when it
  has a real next action.
- Update the planning index/dashboard and active workstream README when they
  exist.
- Report what was deleted, archived, and left active.

Do not leave completed issue/PR drafting artifacts in active planning folders.
Prefer one evolving spec over parallel rough-spec and issue-draft files.

## Implementation Completion Handoff

When finishing an implementation, the agent hands the implementation off for
review by spawning the implementer's reviewer.

Required shape:

1. Brief implementation summary.
2. Verification run and results.
3. Spawn exactly one fresh-context reviewer, populated from the current session
   using the canonical Review Kickoff template, and announce the handoff (what is
   being reviewed + the range). The populated prompt goes to the subagent — the
   operator opens it to inspect, or it is emitted in chat only when the host
   cannot spawn a subagent. Do not spawn a second reviewer unless the operator
   explicitly asks in the current session.
4. The second independent review is operator-owned by default and self-populates
   from the work-item folder + live range (`secondreview` / `secondspecreview`) —
   it does NOT reuse this prompt.

Obtain two independent approved review verdicts before PR handoff by default:
the implementer owns the one spawned reviewer, and the operator owns the second
reviewer unless they explicitly ask the implementer to spawn both. The second
review runs on the final tip after the implementer's review/re-review loop
converges, with a freshly populated prompt whenever patches have landed since
emission. Shared handoff mechanics — sequencing, freshness, the independence
seal, and the ritual→skill index — live in `~/.agents/workflow/HANDOFF.md`.

Review floor — the inner review loop (`implreview` → `implrereview` to
APPROVED) is NEVER skippable; every implementation gets at least one review, and
nothing reaches a PR without one. The ONLY thing ever waived is the second /
outer-gate review (`secondreview`). The outer gate is REQUIRED whenever the diff
touches ANY canonical risk-surface —

> migration / schema / persisted-state (any change to stored data or a
> state-machine) · auth · contract / API surface · data-loss paths · security ·
> provider boundary (Stripe, AvaTax, other external services) · dependency ·
> toolchain

— OR when the inner review returned ACTIONABLE on any substantive finding at any
point in the loop. It is operator-waivable ONLY when ALL of:

- (a) the diff touches NONE of the canonical risk-surface list above;
- (b) the inner review was APPROVED on the FIRST pass with zero substantive
  findings (no ACTIONABLE cycle at all — a patched-then-clean loop does NOT
  qualify);
- (c) the diff is mechanically trivial — NO logic or control-flow change (copy,
  comment, pure rename, or a purely non-behavioral config value; a config value
  that changes runtime behavior — a threshold, retry count, rate limit — IS a
  logic change and does NOT qualify).

The implementer states `outer gate: required | waivable — <one-line why>` at
handoff; the OPERATOR makes the final waive call. When the outer gate is
mandatory, do not trim the independence seal, live-range self-computation, or
the inner loop. (`secondspecreview` is already optional on the spec side, so
this parity holds there too.)

## PR Handoff

When the operator asks to open or update a PR for an implemented work item, make
the review record available for handoff without making it default public PR
content.

Keep this review material available locally:

- populated Review Kickoff prompt(s)
- reviewer verdict(s)
- actionable findings and how each was resolved
- verification run after patching findings
- deferred follow-ups, with issue links when filed
- residual risk or Tier 4 gates that remain

Flow:

1. Prepare a PR body file in the locked shape owned by the "PR Body / Optional
   Review Notes" template in KICKOFFS.md. Keep the closing-reference semantics:
   GitHub `Fixes #<issue>` only when merge fully resolves it, else `Refs
   #<issue>` / `Part of #<issue>`; Linear `Closes <full url>` when fully
   resolved, else `Part of <url>`.
2. Do not include a standalone `## Review Summary` section by default. Keep
   review prompts, transcripts, and detailed verdicts in local planning
   artifacts. Mention a review finding in the PR body only when it materially
   changes reviewer context, such as a patched edge case, deferred follow-up, or
   residual risk.
3. Prepare a separate PR review-record comment file only when the operator
   requests one. When used, start it with `# Review Notes`.
4. Determine the PR labels from the source issue and local label policy. Carry
   over labels that still describe the PR diff, omit stale status or subsystem
   labels that no longer apply, and state the final label list.
5. Show the PR body, any optional review-record comment artifact, the intended
   PR label list, repo, target branch for create or target PR for edit/update,
   and requested PR action before asking for one bundled approval.
6. Create/update the PR only when authorized, applying the selected labels
   during `gh pr create` or immediately after with `gh pr edit --add-label`.
   Approval semantics follow the Destructive Action Policy.
7. If a separate review-record comment was prepared and authorized, post it
   under the PR with `gh pr comment` once the PR number or URL exists.

All externally visible GitHub mutations in this flow — including the PR label
command and any optional PR comment command — follow the Destructive Action
Policy.

## Domain Pass

Run before final-spec promotion or tracker publication when work:

- introduces or overloads a core noun
- changes lifecycle or state meaning
- crosses app/service/provider/device boundaries
- affects user-facing terminology
- creates a new module or service boundary
- is high-risk or multi-step

Output:

- canonical terms
- avoided synonyms, when important
- unresolved decisions
- ADR/decision-record need, only if the decision is hard to reverse, surprising, and has a real trade-off

Skip Domain Pass for isolated bug fixes, visual polish, small refactors, and dependency
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

- Prefer repo-provided verify commands.
- Before implementation handoff and PR handoff, make verification routing
  explicit: commands run, gates intentionally not selected (each with a short
  reason — no self-judged "only if a reviewer would ask"), gates blocked, and
  any Tier 4/operator work remaining.
- When broader local gates are available, choose intentionally whether to run
  them based on the changed surface and risk; do not skip or run them only
  because they are or are not in the default PR CI path.
- Do not treat optional, nightly-only, or CI-only-by-policy gates as impossible
  to run locally. If the repo exposes a local command and the environment is
  prepared, agents may run it when the task risk justifies it.
- For user-facing UI, run targeted automated coverage and visual/manual QA.
  Escalate to e2e-smoke or full e2e when the change touches routing, auth,
  checkout, multi-page workflows, real data integration, or a regression-prone
  path.
- For API/schema/data/integration changes, consider contract tests, builds,
  local-stack verification, and service e2e in addition to package tests.
- Do not run live/provider/hardware checks from an agent unless the environment is explicitly prepared.
- If sandboxing blocks services, hardware, localhost, or network, stop after one diagnostic run and escalate or ask the operator for output.
- Final summaries must name commands run and results.

## Review Loop

Default review pass:

- verdict and findings semantics (`APPROVED` / `ACTIONABLE`, blocking rules)
  are owned by REVIEW_RUBRIC.md
- review adversarially and approve clean only after naming the checks run —
  the Stance section of REVIEW_RUBRIC.md owns the adversarial checks
- patch only listed findings unless scope expands
- rerun targeted verification
- the default two independent fresh-context reviews both run the full
  `REVIEW_RUBRIC.md`; the outer-gate review is a fresh independent pass, and its
  mechanics live in `~/.agents/workflow/HANDOFF.md`
- automated PR reviewer (e.g. CodeRabbit) path-exclusion handling: see
  "Automated-reviewer awareness" in REVIEW_RUBRIC.md
- additional review passes are allowed whenever patches after review are
  non-trivial, touch lifecycle/state/concurrency, change acceptance behavior, or
  the operator asks for another pass

Reviewer priorities:

1. correctness/regression
2. contract/API/schema drift
3. state and failure-path behavior
4. security/privacy/data loss
5. test quality: missing tests, false confidence, or tests that only assert
   implementation shape instead of the protected behavior
6. missing docs
7. maintainability issues that affect future changes

## Output Budget

- Be concise.
- Do not restate stable repo rules unless they matter.
- Show failed command context only when useful.
- Final summaries should include changed files, intent, verification, and known follow-ups.

## Local Repo Facts Contract

Each local repo shim should define only facts the kernel cannot know:

- stack and package manager
- repo layout
- branch/PR/ticket conventions
- verification commands by tier
- manual/hardware gates
- forbidden or sensitive files
- common pitfalls
- subtree-specific rules

Shims should stay small and local-only unless the team wants them committed. Put durable
domain vocabulary in `CONTEXT.md`, not in every agent instruction file.
