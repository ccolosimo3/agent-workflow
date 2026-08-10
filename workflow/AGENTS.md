# AGENTS.md Kernel — Portable Agent Workflow

Small, project-agnostic operating kernel for coding agents. Repo instructions
own project facts, commands, and constraints; on-demand workflow files own the
detailed procedures.

## Startup and precedence

- If the repo root has `AGENTS.local.md`, read it before substantive work as an
  additive local adapter. Claude also reads the repo-root `CLAUDE.md` in the
  order that adapter defines.
- Precedence: current-session human instruction; repo/company/security/code-owner
  policy; nearest repo/subtree instructions; this kernel; optional preferences.
- Never use this workflow to bypass team review, CI, security, licensing, or
  data-handling policy.

## Universal quality floor

- Prefer the simplest complete, repo-conventional solution. Added complexity
  must trace to a current requirement, observed failure, or established pattern;
  defer hypothetical future needs.
- Preserve public contracts unless the work item changes them. Do not modify
  unrelated files or discard unowned work.
- Prefer existing patterns over new abstractions. Route/page/entry files stay
  thin; persistence owns persistence and services own policy, validation,
  orchestration, transactions, and side effects.
- Do not install dependencies, change toolchains, or edit generated artifacts
  without clear need and approval, except the immutable worktree bootstrap below.
- Never commit secrets, credentials, device identifiers, personal paths, local
  workflow adapters, or kernel symlinks.
- Test and verify in proportion to changed risk. Update owning docs only when
  behavior, contracts, setup, architecture, or user/operator workflow changes.
- Report environmental or permission blockers; never mask them.

## Test quality fallback

`~/.agents/workflow/TESTING.md` is canonical. If it cannot be opened:

- A useful test protects a durable behavior, contract, failure mode, or outcome
  and fails when that regression returns.
- Exercise the smallest real operation boundary that proves the behavior. For
  persistence, save and reload; for integrations, cross the actual integration
  seam.
- Do not ship tests whose value is implementation shape, mock call order,
  source text, existence, or coverage percentage unless that shape is itself a
  contract or is supplemental to a named real-boundary proof.
- Removing incidental copy/markup does not create a durable absence contract.
  Relax only the obsolete assertion unless continuing functional, safety,
  accessibility, policy, legal, privacy, or public-contract authority requires
  absence coverage.
- If meaningful automation is impractical, record the manual/provider/local
  proof instead of inventing weak coverage.

## GitHub CLI

Use `gh` for GitHub interactions when available; do not substitute a GitHub MCP
connector.

## Approval boundaries

Every action below requires fresh, explicit in-session operator approval.

Hard-to-reverse local or repository state:

- `git push` (including force variants); `git reset --hard`, `checkout --`,
  `restore --`, `clean -f`; deleting branches; rewriting pushed history;
  creating/deleting or pushing tags;
- bypassing hooks/signing (`--no-verify`, `--no-gpg-sign`, or equivalents);
- editing `.git/`, lockfiles, or `.git/info/exclude`;
- adding/removing/upgrading/downgrading dependencies or toolchains;
- any `rm -rf`, or deleting tracked files outside the stated scope;
- deleting/recreating databases, indexes, containers, volumes, caches, or
  worktrees. A repo-documented disposable DB test harness is exempt only when
  its unchanged command is confined to loopback/local Docker and its own test
  namespace; any target, wrapper, migration, reset, ingest, or persistent-store
  difference remains gated.

Shared or externally visible state:

- creating/editing/merging/closing/reviewing PRs, issues, releases, repositories,
  or other mutating `gh api` calls;
- mutating tracker objects or sending Slack, email, webhook, or other external
  messages;
- changing CI/CD configuration, secrets, or branch protection;
- mutating cloud, deployment, database, payment, DNS, monitoring, or other
  provider state, including migrations, backfills, imports, reindexes, seeds,
  repairs, deploys, and promotions. Only the repo-documented disposable DB test
  harness exception above is preauthorized;
- running a paid model/API call or paid live probe unless the current request
  explicitly authorizes that exact provider, input scope, and cap.

Operating rules:

- Natural approval language such as “yes,” “approved,” “go ahead,” or “open the
  PR” authorizes the stated action and its shown natural substeps. Re-ask only
  when the repo/target, scope, side effect, body/label/comment, provider, input,
  or cap materially changes. “ok” or silence is not approval.
- Before asking, state the exact action/command, target, and relevant side
  effects; for destructive local data, say whether data loss is expected.
  Prefer read-only checks/dry-runs first; they do not authorize mutation.
- Never bypass a failed hook or CI check.
- If uncertain whether an action is gated, ask.

### Isolated-worktree bootstrap (preauthorized)

In a new task-specific worktree, if `AGENTS.local.md` exists in the source
checkout but not the worktree, copy it to the worktree root, read it, and never
stage it. Then announce and run the repo's existing immutable install (`pnpm
install --frozen-lockfile`, `npm ci`, `yarn install --immutable`, or documented
equivalent) without asking again, only when manifests and lockfile already match
the checked-out commit. Confirm they remain unchanged. This does not authorize
dependency/toolchain changes, non-immutable/global installs, or package-manager
installation.

## Choose the least sufficient workflow

Use one route and switch only if the task changes.

### Fast implementation

Use when the outcome is clear, the change is narrow/local, no architecture or
product decision remains, no canonical outer-gate risk surface is touched, and
one focused proof can falsify it. Skip formal `spec`/`explore`; implement,
verify proportionally, and use the normal inner review. A heavier route must name
the disqualifying risk—“more review might help” is not one.

### Normal implementation

1. Read the work item, linked context/spec, and nearest instructions. Restate
   goal, non-goals, acceptance criteria, scope, and verification; re-open a
   named spec after compaction.
2. Inspect `git status` before branching or editing. Spot-check load-bearing
   source claims and adjust stale assumptions rather than coding against them.
3. Use the repo-standard branch, implement minimally, and document any real
   behavior/setup/architecture impact.
4. Run risk-selected verification, then hand off through the Review Loop below.
5. Commit, push, or mutate external state only within the approval boundary.

### Formal planning

Use `spec` only when the operator explicitly invokes it or asks for a formal
implementation-ready plan. Use `explore` only when explicitly invoked for an
architectural options pass. Casual questions, status requests, and ordinary
option discussions stay serial and do not start either workflow.

A formal spec is self-contained: goal/non-goals, evidence-grounded scope,
testable acceptance criteria, exact verification, approval-gated work, and a
proportionate Task. Follow the inner spec-review loop and HANDOFF.md's current
outer-spec routing. Planning does not authorize code or tracker mutation.

### Review

- Own implementation: `implreview` / `implrereview`, then any required
  `outerreview` per `~/.agents/workflow/HANDOFF.md`.
- Coworker PR: `prreview`.
- Reviewer judgment and verdicts: `~/.agents/workflow/REVIEW_RUBRIC.md`.

## Work-item model

Default to one independently reviewable Task, branch, and PR. Map a broader
destination when useful, but fully specify only the next risk boundary. Every
slice must remain valid if later work never lands. Split independently provable
risks; keep together work whose split creates an invalid intermediate state or
shape-only ceremony. Re-ground downstream Tasks after predecessors merge.

## Domain pass

Before final-spec promotion, run a domain pass when work changes a core noun,
lifecycle/state meaning, user-facing terminology, module/service boundary, or a
cross-app/provider/device contract. Record canonical terms and real unresolved
decisions; create an ADR only for hard-to-reverse, surprising tradeoffs. Skip
isolated fixes, visual polish, small refactors, and stable dependency work.

## Documentation impact

Every implementation decides whether it changes user-visible behavior or terms;
setup/build/local iteration; verification/manual QA; architecture/ownership;
API/device/provider contracts; or release/privacy/distribution evidence.

- If yes, update the existing owning doc in the same change and include a
  `## Docs impact` PR-body section.
- If no, record that in the review handoff and omit the PR-body section.

Planning lifecycle and cleanup are owned by `~/.agents/workflow/PLANS.md`.

## Verification tiers

- **Tier 1 — Loop:** smallest local proof of changed behavior.
- **Tier 2 — Patch:** targeted reruns after non-trivial/review patches.
- **Tier 3 — Gate:** affected repo/surface builds, lint, typecheck, tests,
  contracts, boundaries, or e2e selected by changed risk.
- **Tier 4 — Operator:** manual, hardware, live-provider, destructive, expensive,
  or environment-sensitive proof requiring preparation or approval.

Rules:

- Use repo verification routes and record commands run, gates intentionally not
  selected with causal reasons, blocked gates, reused evidence, and remaining
  Tier 4 work.
- Run every required gate for behavior the delta changes or plausibly affects
  once before first review. A new commit or handoff does not invalidate green
  evidence by itself. Rerun only checks with a plausible failure path from the
  intervening delta; rerun a full composite gate when shared/build/test
  infrastructure changed, surfaces span broadly, prior evidence is suspect, or
  no valid constituent proof remains.
- Select risk-relevant optional/local gates even when CI does not require them.
- A changed shared export must be proven through the exact consumer import at
  its real build/runtime boundary; a sibling import or typecheck-only proof is
  insufficient unless that is the actual consumer boundary.
- For a no-contract refactor, prove parity for status, shape, errors, and side
  effects across the changed boundary.
- UI changes need targeted automated proof plus rendered/manual QA; API/schema/
  data/integration changes consider contracts, builds, local-stack, and e2e.
- Do not run live/provider/hardware checks unless the environment is explicitly
  prepared. After one blocked diagnostic, escalate rather than looping.

## Review loop and completion

- Every implementation gets one fresh inner review unless the entire diff meets
  HANDOFF.md's narrow non-normative documentation-only self-check. Workflow/
  policy docs never qualify. No second inner reviewer unless the operator asks.
- Patch listed findings only, rerun causally affected verification, and reuse the
  same reviewer for re-review. Extra review is required for non-trivial patches,
  lifecycle/state/concurrency, acceptance behavior, test-quality rewrites, or an
  operator request; a truly trivial stated correction may keep approval.
- Required outer gates are selected only by HANDOFF.md. Otherwise skip them
  automatically unless requested. Outer-owned patches return directly to the
  same outer reviewer, not through the inner loop.
- Completion handoff: brief outcome and verification, docs-impact decision,
  review result, `outer gate: required | skipped — <why>`, and remaining Tier 4.
  HANDOFF.md owns kickoff fidelity, freshness, independence, and reuse.

## PR handoff

Keep review prompts, findings/resolutions, detailed verification, and residual
risk local unless public context needs them. Compose the PR body from
`kickoffs/pr-body.md`, use teammate-readable language, carry only accurate issue
labels, and follow the approval boundary for every GitHub mutation.

## Output budget

Do not restate stable rules unless they affect the task. Final summaries include
changed files, intent, verification, and known follow-ups.

## Local repo facts contract

Local adapters contain only facts the kernel cannot know: stack/package manager,
layout, branch/PR/ticket conventions, verification routes, manual/hardware
gates, sensitive files, and non-obvious pitfalls. Put durable vocabulary in the
repo's context/glossary and detailed procedures in their owning docs; route to
them instead of copying them into the adapter.
