# V2 Pull Request Body

Write for a teammate who understands the product and repository but has not read
private plans. Lead with observable behavior and motivation. Keep technical names,
paths, and commands only when they improve precision. Omit workflow tiers, private
plan codes, review mechanics, local paths, agent jargon, and process history.

Use the repository's required closing reference first when one exists. Always
include `## Summary` and `## Verification`. Include optional sections only when
they carry information a reviewer needs; omit empty headings.

```text
<closing reference, when applicable>

## Summary
<one sentence: observable change and why>
- <concrete behavior or contract change>
- <concrete behavior or contract change>

## Root cause
<optional: why the defect or need existed>

## Impact
<optional: what now works or which risk is reduced>

## Scope boundary
- <optional adjacent behavior deliberately unchanged and why>

## Screenshots
<optional UI evidence>

## Verification
<affected local gate summary using only checks that actually passed>
- <focused behavior proof> — <result>
- <blocked, manual, visual, or operator check> — <status, when relevant>

## Docs impact
- <optional tracked owner path> — <what changed>

## Risks
<optional remaining risk>

## Follow-ups
- <optional operator-approved or already-filed follow-up with shared link>

## Notes
- <optional non-obvious migration, rollback, or reviewer-relevant tradeoff>
```

Use an outcome-first sentence-case title. Report only observed results that apply
to the candidate. Evidence from an earlier revision may be reused when no change
to relevant code, configuration, dependencies, or environment can invalidate it;
identify the tested revision and briefly explain why the evidence still applies.
Never imply a reused check was rerun. Keep exhaustive commands, findings, verdicts,
and rerun history in the existing evidence owner rather than the PR body. Omit
`## Docs impact` when tracked docs did not change.
