# Spec Review Kickoff

```text
Review plan/spec <path or link> for <feature/workstream>.

Treat this Context as the planner's claim. The spec, repository, and current
source are authoritative. Re-derive scope and dependencies; assume the key gap
may be something the planner omitted.

Context:

1. Artifact and downstream action
   - path: <url or path>
   - status/type: <rough | review-ready | final | promoted | other>
   - downstream action: <implementation kickoff | tracker publication | other>
   - target repo/labels: <only when publication is intended; otherwise none>

2. Summary and sources
   - planner summary: <2-3 sentences: outcome and why>
   - upstream context / related issues / ADRs: <paths or URLs, or none>

3. Scope
   - in scope: <bullets>
   - non-goals: <bullets + reason>
   - claimed modules/files: <paths>
   - dependencies/order: <claims, or none>

3a. Adjacent mechanism (for a bug, edge case, fallback/error/loading path, or
    business-rule tweak)
   - current analogous path: <file:line, or none found + search scope>
   - relationship: <reuse/extend | bypass + why a narrower condition cannot work>

4. Verification, tests, and design
   - exact verification: <commands and Tier-4/manual proof>
   - planned tests: <behavior/failure mode + real operation boundary>
   - UI only: <tokens/primitives, states, visual proof; otherwise not applicable>

5. Risks and decisions
   - <claims to fact-check, assumptions, rejected alternative, open decisions>

6. Repo conventions to enforce
   <resolve from the filesystem per HANDOFF.md step 3>

Return:
1. `APPROVED` or `ACTIONABLE`.
2. Findings: `[severity] section-or-line | category | issue | required fix`;
   mark operator-owned direction decisions `[decision-required]`.
3. Concise non-blocking framing improvements, if any.

Verify, without restating clean ledgers:
- self-contained goal, scope/non-goals, acceptance criteria, dependencies, and
  publication labels when applicable;
- every load-bearing file:line and adjacent-mechanism claim against current
  source, reading the full affected function/module and preferring reuse over an
  unjustified new mechanism;
- exact verification and behavior-level tests under
  `~/.agents/workflow/TESTING.md`, including the migration/persistence bar in
  `~/.agents/workflow/REVIEW_RUBRIC.md` when applicable;
- UI strategy under `~/.agents/workflow/FRONTEND.md` when applicable;
- current external/version claims against the pinned repo version and official
  primary sources;
- terminology, implementation latitude, minimum-sufficient design, and absence
  of private/local-only material from intended public text.

Do not write implementation or add scope beyond a claimed coverage gap. When
ACTIONABLE, append `~/.agents/workflow/kickoffs/planner-directive.md` verbatim.
```
