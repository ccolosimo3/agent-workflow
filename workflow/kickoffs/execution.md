# Execution Kickoff / Implementation Kickoff

```text
Run execution kickoff for existing work item <id/link>.

Execute Startup Routing A ("Implement Existing Work Item") in AGENTS.md end to end.
Do NOT restate the rules AGENTS.md already owns — follow them: Verification Tiers,
the Destructive Action Policy (identify every approval-gated command before running
it), the Review Loop, and PR Handoff (PR body in the locked shape below, labels).

Enforce these forcing functions ON TOP of Routing A:

- Shape and scope control: apply the kernel's Minimum-sufficient shape rule
  before investing in a material mechanism. Simplify or reuse and continue when
  the outcome and approved contracts remain intact; return to the operator or
  planning task only when the correction changes approved scope, substantive
  design, a contract, or acceptance behavior. Before handoff, remove or disclose
  work that cannot be traced to the ask/spec.
- Surface-tied verification: if the diff touches a surface the repo's verification
  doc names a gate for, that gate is REQUIRED — "Tier 1 sufficient" is not a valid
  final-candidate record. Run it before the first implementation review; after a
  patch, apply the patch-loop rule below rather than automatically repeating it.
  Name the surface you changed, or why no surface-triggered gate applies.
- Patch-loop verification follows the kernel's causal-impact reuse rule
  (Verification Tiers): narrowest Tier 2 proof of the changed behavior; rerun a
  broader gate only when the patch can invalidate it.
- Honest verification reporting: claim a gate passed only if it actually ran this
  session/branch; report each as a real result/number; mark un-run gates as not-run
  (reason/blocker or CI-owned), never as passing.
- Commit discipline: commit after implementation and each patch round as real
  commits (no push, no amend); record the `<base>..<tip>` range so reviewers and
  re-reviewers diff a precise range. Commit freely on the branch; do NOT locally
  squash/rewrite/force-push — rely on GitHub squash-merge for one mainline
  commit per PR (keep subjects presentable; some repos concatenate them into
  the squash body).
- Re-review trigger: per the kernel's Review Loop. Outerreview findings return
  directly to that same outer reviewer per HANDOFF.md; do not invoke
  implrereview unless the operator explicitly restarts the inner loop.
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
