# PR Body / Optional Review Notes

```text
Compose PR handoff text for work item <id/link> / PR <id/link>.

# Locked PR body shape

Required core, always present: `## Summary` and `## Verification`. Optional
sections appear ONLY when they carry real content, in the order shown below —
omit an optional section entirely rather than writing "None". One shape serves
human and agent reviewers alike (both want stable headings, claims tied to
verifiable specifics, the intent, and the noise cut); do not split formats.

Closing reference — the FIRST line of the body, above `## Summary`:
- GitHub issue (e.g. clearsnake): `Fixes #<n>` when merge fully resolves it;
  `Refs #<n>` or `Part of #<n>` for partial / phase / validation-only work.
- Linear (e.g. townchest): `Closes <full https://linear.app/...> URL` when fully
  resolved; `Part of <url>` for partial. GitHub keywords do NOT close a Linear
  issue; the `issue.gitBranchName` branch also auto-links it. Never use a prose
  "Source issue: <url>" line to close — it does not auto-close.

Layout (annotations are not part of the output):

  <closing reference>                 # top line, per above

  ## Summary            (required)
  <one sentence: what changed + why, in user-facing/product terms>
  - <concrete change bullet>
  - <concrete change bullet>

  ## Root Cause         (optional — bug or non-obvious change)
  <why it broke / why this is needed; system nouns over implementation trivia>

  ## Impact             (optional — what now works or what risk is reduced; NOT a second summary)
  <one short paragraph>

  ## Scope boundary     (optional — what this deliberately does NOT change)
  - <adjacent behavior/system left untouched, and why the in-scope work did not need it>
  # High value when the change has a tempting overreach — it is the line an agent
  # reviewer uses to catch approach/scope substitution. Omit when there is no
  # meaningful boundary to draw.

  ## Screenshots        (optional — UI; or `## Visual QA`)
  <images / before -> after>

  ## Verification       (required)
  Full local PR-parity gates green: <only the gates that ACTUALLY ran green>.
  - <focused test / behavior proof specific to THIS change> -> <result>
  - <manual / visual / Tier-4 QA, or "none needed">
  - <gate blocked / skipped / CI-owned that affects THIS change> -> <why>   # omit if N/A

  ## Docs impact        (required only when tracked docs changed)
  - <tracked-doc path> — <one line on what changed>

  ## Risks              (optional)
  <residual risk, 1-2 sentences>

  ## Follow-ups         (optional — ONLY operator-named deferrals or filed issues)
  - <deferred item> — <full issue URL if filed>

  ## Notes              (optional — reviewer-ACTIONABLE caveats only)
  - <rollback / migration / residual risk / a deliberate non-obvious tradeoff>

Constraints:
- Omit docs impact entirely when no tracked docs changed; never write
  `Docs impact: none`.
- Verification is ONE PR-parity sweep line plus only targeted proofs (the focused
  behavior test, manual/visual/Tier-4 QA). The exhaustive command log lives in the
  work item's verification.md, never the PR. Do NOT list individual gate
  invocations or flag strings, module/dependency/doc counts, tooling warnings
  irrelevant to the diff, or rerun/post-rebase process history. The sweep line
  names ONLY gates that actually ran green; a blocked or skipped gate gets its own
  explicit line (honesty rule unchanged).
- Reviewer-skip test for every line (human OR agent reviewer): if a reviewer
  skipped it, would their review be worse? If not, it is a log entry — cut it.
- Keep review verdicts OUT of the PR body by default — review evidence stays
  local. Mention a review finding only in `## Notes`, and only when it explains a
  patched edge case, residual risk, or deferred follow-up. No standalone
  `## Review Summary` section.
- Plain `path:line` and full issue URLs; no markdown file links (GitHub does not
  resolve them in PR comments).
- Factual and concise, no marketing tone; prefer "no remaining blocking issues
  found" over absolutes like "approved", "fully safe", or "all issues resolved".
- Do not mention spec review by default; accepted specs normally pass spec review
  before coding.
- Return the PR body only, no preamble like "here is the summary".

# Optional separate review-record comment (only when the operator requests one)

A separate PR comment, not the body. Start with `# Review Notes`. Include: findings
patched in this PR as a brief bullet list with `path:line`; deferred follow-ups,
each captured as a separate issue when applicable; residual risk in one or two
sentences (omit if none). Use neutral labels ("Implementation review", "Second
independent review", "Operator review") and treat it as a verification record, not
a certification.
```
