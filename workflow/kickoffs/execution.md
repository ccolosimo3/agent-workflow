# Execution Kickoff / Implementation Kickoff

```text
Run execution kickoff for existing work item <id/link>.

Execute Startup Routing A ("Implement Existing Work Item") in AGENTS.md end to end.
Do NOT restate the rules AGENTS.md already owns — follow them: Verification Tiers,
the Destructive Action Policy (identify every approval-gated command before running
it), the Review Loop, and PR Handoff (PR body in the locked shape below, labels).

Enforce these forcing functions ON TOP of Routing A:

- Surface-tied verification: if the diff touches a surface the repo's verification
  doc names a gate for, that gate is REQUIRED — "Tier 1 sufficient" is not a valid
  record. Name the surface you changed, or why no surface-triggered gate applies.
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
```
