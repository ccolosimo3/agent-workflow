# AGENTS.md Kernel - Portable Agentic Workflow

This is the portable operating kernel for coding agents. It is intentionally
project-agnostic. Local repo shims define stack facts, commands, and local constraints.

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
- Add tests or verification proportional to risk.
- Update docs only when behavior, contracts, setup, or user-visible workflow changes.
- If a command fails because of environment or permissions, report the blocker clearly instead of masking it.

## GitHub CLI

Use the `gh` CLI for all GitHub interactions — issues, PRs, releases, comments,
reviews, and `gh api` calls. Do not use a GitHub MCP connector when both are
available. The CLI keeps commands text-visible and copyable for the operator,
keeps argument shape consistent across sessions, and the Destructive Action
Policy already enumerates `gh` commands by name — the CLI keeps that policy
enforceable.

## Destructive Action Policy

Every instance of an action below requires fresh, in-session operator approval.
There is no blanket pre-approval; approving one push, merge, or close does not
authorize the next.

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

Shared-state and externally visible actions:

- `gh pr create` / `edit` / `merge` / `close` / `review`
- `gh issue create` / `close` / `comment` / `edit`
- `gh release create` / `delete`, `gh repo edit`
- `gh api` calls using `POST`, `PATCH`, `PUT`, or `DELETE`
- Sending messages to Slack, email, webhooks, or external services
- Modifying CI/CD configuration, secrets, or branch-protection rules

Operating rules:

- State the exact command before running it.
- Wait for explicit approval in this session ("yes", "approved", "go ahead").
  Silence, "ok", or prior approvals do not authorize.
- Authorization is scoped to the exact action and target stated. A push to
  branch X does not authorize a force push, a push to a different branch, or
  a later merge.
- If a pre-commit hook or CI check fails, never bypass with `--no-verify` or
  similar. Stop and report the failure.
- If unsure whether an action belongs here, default to asking. The cost of an
  extra question is far less than the cost of an unwanted destructive action.

## Startup Routing

Choose one path. If the session changes, switch paths.

### A) Implement Existing Work Item

Use this when a ticket, issue, bug, or explicit task already exists.

1. Read the work item and any linked PR/context first.
2. Read the nearest repo/subtree shim for touched files.
3. Restate goal, non-goals, acceptance criteria, and verification.
4. Identify files in scope and explicitly risky/out-of-scope areas.
5. Check current git status before branching or editing; never discard unowned changes.
6. Create or switch to the team-standard branch when edits are expected.
7. Implement minimally.
8. Run tiered verification.
9. Hand the operator a fully populated, copy/paste-ready Review Kickoff prompt
   in chat as a dedicated completion artifact. The prompt must be visible in
   chat before any reviewer subagent is spawned.
10. After the prompt has been emitted in chat, spawn exactly one fresh-context
    reviewer from that prompt by default, and tell the operator to use the same
    prompt for the second independent review.
11. Obtain two independent approved review verdicts before PR handoff by
    default; the implementer owns one spawned reviewer, the operator owns the
    second reviewer unless they explicitly ask the implementer to spawn both.
    Patch any actionable findings in scope and rerun targeted verification
    before continuing.
12. Open/update PR or push only when authorized by the user/team flow.
13. When a PR is opened, post a review-cycle summary comment using the reviews
    that informed the implementation.

### B) Plan Work

Use this for feature shaping, issue drafting, task splitting, or unclear scope.

1. Read relevant product/docs/code context.
2. Run a Domain Pass when terminology, lifecycle state, or cross-boundary behavior changes.
3. Choose mode: `task` by default, `gated` for high-risk multi-step work, `fast` for low-risk quick fixes.
4. Produce issue-ready scope with acceptance criteria and exact verification commands.
5. Do not make code changes during planning unless explicitly asked.

### C) Review PR or Diff

Use this when asked for review.

1. Review changed behavior first, not style first.
2. Focus on correctness, regressions, contract drift, security, data loss, and missing verification.
3. Lead with findings ordered by severity and file/line.
4. Return `APPROVED` only when no blocking findings remain.
5. Return `ACTIONABLE` when concrete fixes are required.

### D) Docs, Architecture, or Pattern Maintenance

Read only docs relevant to the requested scope. Keep docs aligned with actual commands,
runtime versions, and contracts.

## Kickoff Templates

Canonical kickoff prompts live in `~/.agents/workflow/KICKOFFS.md`: Planning,
Domain Pass, Issue Draft, Execution/Implementation, Review, PR Review Comment,
Fast Fix, Post-Plan Grill.

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
- **Spec**: umbrella for multiple related tasks or high-risk work.
- **Decision**: short decision lock with rationale.
- **Fast fix**: low-risk direct change when team policy allows it.

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
- affected surfaces and owners are known
- dependencies and manual/hardware requirements are called out
- contract changes are explicit
- domain terms are resolved or open questions are named

## Definition Of Done

A Task is done when:

- implementation satisfies acceptance criteria
- verification passed or blockers are documented with exact failed commands
- tests/docs changed where risk requires it
- docs impact was checked; authoritative docs were updated when behavior,
  contracts, setup, verification, or user-visible workflow changed, or the
  agent stated `Docs impact: none`
- PR/review requirements are satisfied
- the operator received a populated Review Kickoff prompt in chat as a
  dedicated completion artifact
- if a PR was opened, the review-cycle summary comment is posted or the blocker
  is documented
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

If no, state `Docs impact: none` in the implementation summary and PR body.
Do not add documentation just to appear thorough. Prefer concise updates that
reduce future confusion, remove stale text, or point readers to the existing
authority.

## Planning Artifact Cleanup

When the operator says an issue or PR has landed, planning agents must clean
local planning artifacts before moving on.

Required:

- Confirm the issue or PR state with the tracker.
- Delete local issue drafts, PR body drafts, review summary drafts, kickoff
  prompts, and one-off review prompts now represented by the tracker or PR.
- Archive only durable context: reusable specs, verification reports, audit
  reports, ADR-like rationale, or cross-issue policy decisions.
- Move still-actionable future work to backlog, or keep it active only when it
  has a real next action.
- Update the planning index/dashboard and active workstream README when they
  exist.
- Report what was deleted, archived, and left active.

Do not leave completed issue/PR drafting artifacts in active planning folders.

## Implementation Completion Handoff

When finishing an implementation, the agent must hand the operator a review
prompt even if the agent is also spawning a reviewer itself. This is a hard
output contract: an implementation completion summary is incomplete without a
dedicated `Review Kickoff Prompt` block.

Required shape:

1. Brief implementation summary.
2. Verification run and results.
3. A fenced, copy/paste-ready `Review Kickoff Prompt` populated from the current
   session using the canonical Review Kickoff template. This must be emitted in
   chat before spawning any reviewer. Do not wait until the reviewer completes
   to show it to the operator.
4. Only after the prompt is visible in chat, spawn exactly one fresh-context
   reviewer agent from that exact prompt.
   The second independent review is operator-owned by default: the operator
   receives the prompt and may paste it into another agent. Do not spawn a
   second reviewer unless the operator explicitly asks in the current session.

If two independent reviews are expected, the same populated prompt may be used
for both the implementer-spawned reviewer and the operator-launched reviewer
unless the operator or work item needs different review focuses.

## PR Handoff

When the operator asks to open or update a PR for an implemented work item, make
the review record part of the PR handoff instead of leaving it buried in chat.

Required review material:

- populated Review Kickoff prompt(s)
- reviewer verdict(s)
- actionable findings and how each was resolved
- verification run after patching findings
- deferred follow-ups, with issue links when filed
- residual risk or Tier 4 gates that remain

Flow:

1. Prepare a PR body file with correct issue closing semantics: `Fixes
   #<issue>` only when merge fully resolves the issue; otherwise use `Refs
   #<issue>` or `Part of #<issue>`.
2. Prepare a separate PR review-summary comment file from the PR Review Comment
   kickoff template. The comment body must start with `# Review Summary`.
3. Determine the PR labels from the source issue and local label policy. Carry
   over labels that still describe the PR diff, omit stale status or subsystem
   labels that no longer apply, and state the final label list.
4. Show both artifacts and the intended PR label list before asking for
   approval.
5. Create/update the PR only when authorized, applying the selected labels
   during `gh pr create` or immediately after with `gh pr edit --add-label`.
6. Immediately post the review-cycle comment under the PR with `gh pr comment`
   once the PR number or URL exists.

All externally visible GitHub mutations in this flow still follow the
Destructive Action Policy: state the exact `gh` command(s), including the PR
label command and PR comment command, and wait for fresh in-session approval.

## Domain Pass

Run before issue drafting when work:

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

- **Tier 1 - Loop**: smallest checks proving changed behavior.
- **Tier 2 - Patch**: targeted reruns for review findings.
- **Tier 3 - Gate**: broad repo or surface verification before final/PR.
- **Tier 4 - Operator**: manual, hardware, live-provider, destructive, or expensive checks.

Rules:

- Prefer repo-provided verify commands.
- Do not run live/provider/hardware checks from an agent unless the environment is explicitly prepared.
- If sandboxing blocks services, hardware, localhost, or network, stop after one diagnostic run and escalate or ask the operator for output.
- Final summaries must name commands run and results.

## Review Loop

Default review pass:

- verdict: `APPROVED` or `ACTIONABLE`
- if `ACTIONABLE`, list only concrete findings with required fixes
- patch only listed findings unless scope expands
- rerun targeted verification
- run two independent fresh-context reviews by default before opening a PR; by
  default, the implementer spawns one reviewer and the operator launches the
  second reviewer from the provided `Review Kickoff Prompt`
- additional review passes are allowed whenever patches after review are
  non-trivial, touch lifecycle/state/concurrency, change acceptance behavior, or
  the operator asks for another pass

Reviewer priorities:

1. correctness/regression
2. contract/API/schema drift
3. state and failure-path behavior
4. security/privacy/data loss
5. missing tests or docs
6. maintainability issues that affect future changes

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
