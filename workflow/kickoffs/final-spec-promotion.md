# Final Spec Promotion Kickoff

```text
Prepare final spec <path or link> for tracker publication in repo <repo>.

Output: update the same spec file in place so it can land verbatim as the GitHub issue body via `gh issue create`. Do not create a separate issue-draft file unless the spec must be split, redacted, or substantially reshaped for publication.

Pre-promotion review (recommended for non-trivial specs): spawn a fresh-context reviewer agent against the spec before publication. The reviewer validates scope coverage, file/line claim accuracy, label correctness against the repo's label set (`gh label list --repo <repo>`), self-containment of the final issue body, and dependency claims. Apply review feedback directly to the spec before marking it final. This catches stale paths, missed scope, mislabeled categories, and assumed-but-wrong code claims at the cheapest possible point.

Publication approval: `gh issue create` / `gh issue edit` follow the kernel's
Destructive Action Policy.

Lifecycle: advance the spec `rough` -> `review-ready` -> `final` -> `promoted`
-> `implemented` per the statuses and update rules in
`~/.agents/workflow/PLANS.md`. Move to `review-ready` only when the spec is
coherent AND its load-bearing code claims (paths, identifiers, behavior-parity
claims) have been grounded against current code with file:line evidence; log
any claim you could not ground as an open question rather than asserting it.

Structure (required unless marked optional, in this order):

# <Title Case, action-verb start, no leading [tag]; taxonomy lives in Type below>

## Metadata
- Type: <Polish / Perf / Migration / Hygiene / Verification slice / ...>
- Labels: <platform + subsystem + workstream + work-type labels from the local shim's label set>
- (optional) Priority: <P0|P1>
- Execution mode: <build paths allowed; explicit guardrails on remote/EAS builds; manual gates>
- Suggested branch: `<per the local repo shim's branch convention>`
- Source / prior context: `<paths, issue links, audits, or parent specs>`
- (optional) Parent workstream / Supersedes / Related roadmap
- (optional) Blocked by / Ordered after: <full GitHub issue URLs>

## What to build              # use "What to verify" if no source changes except a reverted-before-merge edit
<1-3 paragraphs: goal + framing; code fence for flow diagrams or contracts when useful>

## Scope
<concrete bullets, each a verb + named file/identifier; subheadings for larger issues>

## (optional) Implementation notes
<HOW guidance when non-obvious; otherwise omit>

## Non-goals
<bullets starting "Do not ..."; one per intentional exclusion>

## Acceptance criteria
<- [ ] testable conditions, mirroring Scope but checkable post-implementation>

## Verification
<Tier 1 commands in code fences with language tags;
 broader local gates selected for this task, such as build/e2e/contract/manual
 QA/local-stack QA; gates considered but not selected with short rationale;
 manual smoke as `- [ ]` checklist mapping to acceptance criteria;
 use Environment setup / Test sequence / Reporting subsections only when long>

## (optional) Blocks
<full GitHub URLs of downstream issues this gates>

## (optional) Notes
<editorial caveats, why-this-issue-exists, intentional out-of-scope edge cases>

Conventions:
- Title Case in titles, action verb first, no `[tag]` prefix
- Hand-wrap lines at ~78 chars for readability in the GitHub web view
- Backticks for identifiers, paths, commands; code fences with language tags for runnable blocks
- `- [ ]` for acceptance criteria and manual verification items; plain `-` for scope/non-goals/notes
- Cross-issue references as full GitHub URLs, not markdown links
- Pull repo-specific defaults (branch prefixes, verification commands, target device, build-path guardrails) from the local repo shim
- If a required section cannot be filled, insert `<!-- TODO: ... -->` rather than skip silently
- If the spec has local-only notes, move them under `## Planning Notes` and remove that section before publishing, or explicitly mark it as not included in the tracker body.
```
