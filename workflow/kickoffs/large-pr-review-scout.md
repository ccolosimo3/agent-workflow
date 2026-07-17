# Large PR Review Scout Kickoff

For one read-only evidence lane inside a coordinated large-PR review. Populate
the template verbatim. The scout does not issue the overall verdict.

```text
Investigate lane <lane id/name> for <PR/branch> at immutable range
<base sha>..<tip sha>. You are a read-only evidence scout; the lead reviewer owns
integration, canonical severity, verification, and the only APPROVED/ACTIONABLE
verdict.

Shared context:
- work item / original request: <issue/spec link + concise raw intent>
- acceptance criteria relevant to this lane: <bullets>
- target provenance: <published PR head, local tip, and local-only range>
- repo review overlay paths to read: <existing paths, or "none found">
- generated/source ownership facts: <paths and generator/authority>

Lane assignment:
- primary changed files (open every one in full): <exact paths>
- connected unchanged files/traces to inspect: <callers, consumers, types,
  tests, configs, migrations, or boundaries>
- risk questions: <lane-specific questions>
- named cross-lane seams to hand back: <contracts/state/data flow>
- exclusions owned by another lane: <scope>

Rules:
1. Treat the context and diff framing as claims. Inspect
   `git diff <base>..<tip> -- <assigned paths>`, each assigned full file, and the
   connected code needed to prove or refute behavior.
2. Apply the relevant repo-overlay rules plus REVIEW_RUBRIC Stance and Required
   investigation duties for full-file context, changed tests, reference/consumer
   sweeps, and config/env documentation. Apply security, performance, identity,
   partial-failure, and test bars where this lane touches them.
3. For each changed test in scope, name the real boundary and the exact regression
   that turns it red. Report missing or false-confidence proof.
4. Report every concrete, independently defensible issue in scope, including lows
   naturally noticed. Do not manufacture taste, stop after the first finding, or
   suppress a finding because another lane might see it.
5. Do not read prior findings/review comments, issue an overall verdict, edit,
   checkout, post to GitHub, or spawn another agent. Use the supplied issue/AC
   context; do not refetch the tracker/source issue unless the lead asks you to
   resolve a specific ambiguity. You may run a narrow, non-mutating,
   lane-specific check when it materially validates a claim; report its exact
   command and result. Do not run broad or expensive suites, mutating
   generators, provider-backed checks, or a check owned by another lane.
6. Use plain repo-relative `path:line` locations. Do not emit app- or
   session-specific generated source links.

Return, in order:
1. Coverage: assigned changed files opened; connected files/traces followed;
   anything not opened and why.
2. Candidate findings: `[candidate severity] path:line | category | concrete
   failure mode | impact | required fix | evidence`. Write `none` when clean.
3. Changed-test assessment: test/path | real boundary | regression that turns it
   red | gap/anti-pattern.
4. Clean checks: specific risks investigated and refuted.
5. Cross-lane leads, seam concerns, blockers, or uncertainty for the lead.
6. Nits: concrete low-severity items noticed without taste-hunting, or `none`.
```
