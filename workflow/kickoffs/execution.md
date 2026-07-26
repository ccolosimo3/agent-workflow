# Execution Kickoff / Implementation Kickoff

```text
Run execution kickoff for existing work item <id/link>.

Execute Startup Routing A ("Implement Existing Work Item") in AGENTS.md end to end.
Do NOT restate the rules AGENTS.md already owns — follow them: Verification Tiers,
the Destructive Action Policy (identify every approval-gated command before running
it), the Review Loop, and PR Handoff (PR body in the locked shape below, labels).

Enforce these forcing functions ON TOP of Routing A:

- Scope control: before adding a material mechanism not named by the work item
  (public abstraction, dependency/tool, configuration or persisted state,
  fallback/retry/recovery/compatibility path, or cross-package change), name the
  current requirement, observed failure, or established repo pattern requiring
  it. If it changes scope, contracts, acceptance behavior, or proof strength,
  stop at a clean checkpoint and return to the operator/planning task. Before
  handoff, compare the diff to the ask/spec and remove or disclose anything that
  cannot be traced back. Do not future-proof for hypothetical needs.
- Surface-tied verification: if the diff touches a surface the repo's verification
  doc names a gate for, that gate is REQUIRED — "Tier 1 sufficient" is not a valid
  final-candidate record. Run it before the first implementation review; after a
  patch, apply the patch-loop rule below rather than automatically repeating it.
  Name the surface you changed, or why no surface-triggered gate applies.
- Patch-loop verification is proportional, not cumulative: after a patch, run the
  narrowest Tier 2 check that proves the changed behavior. Reuse prior green Tier 3
  evidence when the inspected delta cannot invalidate it. Rerun the broader gate
  only when the patch touches its risk surface, changes shared test setup/fixtures/
  config/infrastructure, makes the earlier result suspect, or no valid broad
  evidence remains. A single isolated test correction normally reruns that test,
  not the entire suite.
- Honest verification reporting: claim a gate passed only if it actually ran this
  session/branch; report each as a real result/number; mark un-run gates as not-run
  (reason/blocker or CI-owned), never as passing.
- Commit discipline: commit after implementation and each patch round as real
  commits (no push, no amend); record the `<base>..<tip>` range so reviewers and
  re-reviewers diff a precise range. Commit freely on the branch; do NOT locally
  squash/rewrite/force-push — rely on GitHub squash-merge for one mainline commit
  per PR (townchest's squash body concatenates commit messages, so keep subjects
  presentable).
- Re-review trigger: on an ACTIONABLE verdict, patch + rerun targeted verification +
  re-review (implrereview) when the patch is non-trivial, touches lifecycle/state/
  concurrency, changes acceptance behavior, or rewrites/adds a test for a
  test-quality finding; skip only for a truly trivial patch, stated (e.g. a
  corrected import path or renamed variable in one file, stated as trivial, needs
  no re-review).
- One-off verification tests (a static-asset/config/data repair proof with no ongoing
  regression surface) → pocket to the work-item `artifacts/`, don't commit to the
  suite; disclose in the Review Kickoff.
- Composition-heavy UI: follow the opt-in profile in
  `~/.agents/workflow/FRONTEND.md`. Prefer the live route; before completing the
  full behavior/state pass or broad gates, record one wide/narrow structural
  render and self-critique; after behavior is complete, run one final
  critique/patch/recapture loop. Hand off only a compact visual-evidence pointer
  and confirm temporary fixture/tooling residue is zero.
```
