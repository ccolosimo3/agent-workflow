# Execution Kickoff / Implementation Kickoff

```text
Run execution kickoff for existing work item <id/link>.

Execute Startup Routing A ("Implement Existing Work Item") in AGENTS.md end to end.
Do NOT restate the rules AGENTS.md already owns — follow them: Verification Tiers,
the Destructive Action Policy (identify every approval-gated command before running
it), the Review Loop, PR Handoff (PR body in the locked shape below, labels),
and Definition of Done.

Enforce these forcing functions ON TOP of Routing A:

- Surface-tied verification: if the diff touches a surface the repo's verification
  doc (named by the repo shim — e.g. a verification-routing or PR-checklist
  reference) names a gate for — migration/schema/persisted state, native config,
  routing, auth, contract —
  that gate is REQUIRED; "Tier 1 sufficient" is not a valid record. Name the surface
  you changed and why no surface-triggered gate applies.
- Visual proof (visual-design work only — building/recomposing a screen or component
  look, NOT an incidental copy/prop/behavior tweak): inspect the sibling surfaces
  first, then capture per FRONTEND.md's oracle via the host's fast tool and record it
  in your verification; where none is wired (e.g. native sim), name the gap.
  Incidental UI adds no capture ceremony.
- Honest verification reporting: claim a gate passed only if it actually ran this
  session/branch; report each as a real result/number; mark un-run gates as not-run
  (reason/blocker or CI-owned), never as passing.
- Docs impact: state `Docs impact: none` or the updated tracked-doc path in the
  summary (per the Docs Impact Check).
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
  no re-review). A test-quality finding is addressed only if the new/edited test
  exercises the real boundary and goes RED on revert.
- Scope-creep guard covers SUBSTITUTION, not only addition (the rule and masking
  check live in REVIEW_RUBRIC.md, Stance / Scope-vs-intent sections): list
  out-of-scope work as "discovered follow-ups"; disclose any unrequested swap in the
  Review Kickoff Hot spots as "approach substitution: <old> -> <new>, not requested"
  and flag any preserved identifier (testid/route/name) whose implementation changed
  underneath it.
- One-off verification tests (a static-asset/config/data repair proof with no ongoing
  regression surface) → pocket to the work-item `artifacts/`, don't commit to the
  suite; disclose in the Review Kickoff.
```
