# Townchest Review Overlay

Repository match: `townchest/townchest`

Personal, additive navigation for reviews in Townchest. Repo/company rules and
the portable review rubric remain authoritative. Load only the sections and
specialists relevant to the touched surfaces.

## Always route

- Read tracked `AGENTS.md` and local `AGENTS.local.md`; use `dev` as the normal
  integration base unless the live work item or PR says otherwise.
- Read `.agents/skills/collaborative-pr-review/SKILL.md` for Townchest's
  full-file, caller/consumer, sibling-boundary, and operator-discussion
  expectations. Keep canonical severity, verdict, independence, and approval
  rules from `~/.agents/workflow/REVIEW_RUBRIC.md`.
- Read `docs/agent-rubrics/pr-review.md` and only the triggered sections of
  `docs/agent-rubrics/domain-risks.md`.
- Read `docs/agent-rubrics/review-feedback.yml` for demonstrated misses and
  noise controls. Treat it as learned evidence, not a severity authority.
- For verification, read `.agent-workflow/plans/reference/verification.md`:
  always `## Universal routing`, `### Review-nit / false-confidence checklist`,
  and `## PR handoff checklist`, plus only the touched-surface section.
- For conventions, read `.agent-workflow/plans/reference/coding-standards.md`:
  always `## Repo-wide (monorepo)` and `## Tests (mechanics only)`, plus only the
  touched-surface section. Open questions are not enforceable conventions.

## Surface routes

- Vendure, resolver, plugin, custom-field, worker, or Mirakl changes: also read
  `.agents/skills/sme-vendure/SKILL.md`; trace service/resolver behavior through
  GraphQL schema and every tc-app consumer.
- GraphQL or codegen changes: identify the authoritative source, check both
  commerce and app consumers, and treat unexpected generated semantic deltas as
  blockers to investigate. Never suggest hand-editing generated output.
- Stripe, checkout, refund, payment, order, or webhook changes: also read
  `.agents/skills/stripe-best-practices/SKILL.md`; check idempotency, replay,
  legal state transitions, totals, partial failure, and side-effect ordering.
- tc-app UI changes: apply `~/.agents/workflow/FRONTEND.md` plus the tc-app
  coding-standard section and the design-system routes named in
  `AGENTS.local.md`. Check loading, error, empty, disabled, retry, keyboard,
  responsive, and reduced-motion behavior only where the diff touches them.
- Schema, Supabase, SQL, RLS, or migration changes: check tenant isolation,
  populated upgrades, fresh schema, rollback/partial failure, indexes for new
  access paths, and every caller's nullability assumptions. Review generated or
  automated-review-excluded artifacts manually.
- CI, deploy, workflow, provider, smoke, or server-bundling changes: read
  `docs/deployment/developer-agent-ops.md`; verify active domains/branches and
  do not treat a successful build as proof of server runtime compatibility.

## Townchest-specific seam checks

- Keep generated authority, emitted schema/types, commerce runtime, and tc-app
  consumption in one lane or name the seam explicitly between lanes.
- Trace shared package/export changes at the actual consuming app's build or
  runtime boundary, not merely an internal import or typecheck.
- Inspect adjacent comments and docs after build/tooling/codegen changes; stale
  behavior descriptions are a demonstrated Townchest miss.

## Safety and noise controls

- `docs/agent-rubrics/local-verification.md` is advisory command context only.
  Its automatic `pnpm install` setup instruction conflicts with the operator's
  approval policy: never install dependencies without fresh approval.
- Never run setup, seed, migration, reset, hosted-provider, deploy, or other
  approval-gated commands during review without explicit authorization. Report
  the exact blocked boundary and continue the read-only investigation.
- Do not post, approve, request changes, or mutate Linear/GitHub unless the
  operator separately requests and approves that action.
- Prefer concrete failure modes and repo-backed convention findings. Do not turn
  optional patterns, open questions, legacy debt, or subjective taste into
  review findings.
