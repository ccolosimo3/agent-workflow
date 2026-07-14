# Spec Review Kickoff

```text
Review plan / spec <path or link> for <feature/workstream>.

Apply the Review Rubric in `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL: read it
first, and apply its migration test-bar, convention-conformance, and
time-sensitive rules — plus TESTING.md's anti-patterns and FRONTEND.md's design
rules — to the PLANNED work below, not to a diff.

Context (filled by the planner as ORIENTATION ONLY — it is the planner's CLAIM,
not ground truth, and the plan itself is what you are reviewing). The spec, the
repo, and the real code are the source of truth; where the Context and the
artifact disagree, verify against the code and treat the discrepancy as a finding.
Re-derive scope and dependency claims yourself rather than assuming the bullets
below are complete or faithful. Treat every line — summary, scope-coverage list,
and ESPECIALLY the test-strategy self-report in section 6 — as a claim to confirm
or refute. Assume the most important gap is something the planner did NOT list.

1. Plan artifact
   - path or link: <url or path>
   - artifact type: <rough-spec | review-ready-spec | final-spec | other planning markdown>
   - intended downstream action: <gh issue create | implementation kickoff | other>
   - target repo (if filing an issue): <repo>
   - target labels (if filing an issue): <comma-separated; pulled from `gh label list --repo <repo>`>

2. Planner summary (2-3 sentences)
   <what the plan delivers and why>

3. Source material
   - upstream context / parent spec / audit (if any): <path or URL>
   - related issues, ADRs, prior discussion: <urls or paths>
   - touched modules / files claimed in scope: <paths>

4. Scope coverage
   - intended in-scope items: <bullets>
   - intentional out-of-scope items: <bullets + reason>
   - dependency / ordering claims: <"blocks #X" / "blocked by #Y" / "ordered after #Z">

4a. Existing-mechanism claim (required for bug fixes, edge cases,
    fallback/error/loading behavior, and business-rule tweaks; planner's CLAIM —
    the reviewer verifies it)
   - adjacent mechanism: <the current code path that already handles analogous
     behavior, file:line — or "none found" + where you searched>
   - plan's relationship to it: <reuses/extends it | bypasses it, with why a
     narrower condition change cannot reach the existing path>

5. Hot spots / known risk in the plan
   - <ambiguous areas; claims the reviewer should fact-check against the code>
   - <decisions made and rejected alternatives>

6. Test strategy quality (planner's CLAIM — verify against the repo testing doc; do NOT accept these bullets)
   - behavior/failure mode each planned test protects: <bullets>
   - real operation boundary planned for tests: <service/API/job/UI/persistence/etc.>
   - implementation-shape tests, if any, and why that shape is contractual or supplemental:
   - manual/Tier 4 proof needed when automation cannot represent the failure mode:

7. Repo conventions to enforce: resolve per HANDOFF.md step 3.

Return:
1. Verdict: APPROVED or ACTIONABLE
2. Findings if ACTIONABLE: [severity] section-or-line | category | issue | required fix
   Validation categories (focus, not exhaustive):
   - scope coverage gaps (missing acceptance criteria, undefined non-goals)
   - file/line claim accuracy (do paths claimed in scope exist; do referenced symbols exist)
   - label correctness against the repo's actual label set
   - self-containment of an issue body (would this issue be actionable to someone with no prior context)
   - dependency claims (do blocked/ordered-after references point at real issues with the claimed state)
   - time-sensitive / external claims: apply REVIEW_RUBRIC.md's time-sensitive rule
     to the PLANNED work — if the plan picks a library, API, pattern, or version,
     asserts something is deprecated / current / best-practice, or your own review
     angle rests on current external behavior, verify it against the repo's pinned
     version + upstream docs (cite source + date), not from memory; temper "latest"
     against the repo's actual pinned major
   - ambiguous terminology or undefined nouns
   - missing or untestable acceptance criteria
   - missing or wrong verification commands
   - weak test strategy: apply TESTING.md's anti-patterns (Part 1 principles +
     Part 2 universal anti-patterns) and the repo's testing reference for its
     stack section to each PLANNED test — flag ACTIONABLE any planned test that,
     as described, matches an anti-pattern or would still pass if the fix were
     reverted. For any planned migration/schema/persisted-field change, apply
     REVIEW_RUBRIC.md's migration test-bar at plan time: a spec that plans only
     implementation-shape assertions, or only "add a migration test", is a
     blocking finding.
   - weak design strategy (UI specs only): apply FRONTEND.md to any UI-surface
     spec, confirming it names its tokens/primitives/patterns, the states it
     renders (incl. empty/error/focus), and the visual proof; a UI spec that gives
     only vague visual intent, omits the changing-state set, or names no visual
     proof is ACTIONABLE. Skip for non-UI specs.
   - convention conformance: if any plan step explicitly proposes hand-rolling a
     component, helper, hook, loading state, or style primitive, open the repo's
     patterns doc (the coding-standards / patterns path resolved in "Repo
     conventions to enforce" above, or via the repo shim — e.g.
     `.agent-workflow/plans/reference/coding-standards.md`; your repo's shim names
     its own) and flag ACTIONABLE if the repo already has an established primitive
     for it. Do not flag steps that reuse existing primitives or where no repo
     primitive is documented.
   - existing-mechanism reuse / over-scope: does the plan invent a new helper,
     policy, query, filter, fallback, branch, state, or UI behavior where the
     codebase already has an adjacent mechanism? Verify the 4a claim by reading
     the FULL function/module the plan modifies, not only the lines it cites —
     the missed mechanism is usually adjacent to the cited ones. For bug fixes
     the default is routing the case into the existing path via a narrower
     condition change; a new mechanism with no 4a justification (or a 4a of
     "none found" the code contradicts) is a blocking finding.
   - local-only/private notes that should not be published
3. Notes on scope or framing improvements (non-blocking but useful)

When Verdict is ACTIONABLE, mark any finding requiring operator input (scope change, contract decision, label policy interpretation) with `[decision-required]` in its required fix. Then append the Planner directive (`~/.agents/workflow/kickoffs/planner-directive.md`) verbatim at the end of your output so it stays with the findings when the operator forwards them.

Focus on whether the plan is correct, complete, and self-contained enough to be acted on. Do not write the implementation. Do not propose new scope unless it closes a coverage gap the plan claims to cover.
```
