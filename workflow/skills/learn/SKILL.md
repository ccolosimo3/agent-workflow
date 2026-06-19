---
name: learn
description: Brief the operator on their OWN work — a PR, commit range, branch,
  or work-item — so they can talk about it confidently. Builds a plain-language
  mental model, high-level first (say-it-first pitch, the shape, the why, and a likely
  Q&A), then drill into any piece on request. Read-only; grounds the model in the
  real diff/spec so what the operator repeats is accurate. Use when the operator
  says /learn <ref>, "help me understand this PR", "brief me on <work>", "what
  did we build here", or "I need to explain this to my boss/team". Not for
  restating the last message (that is plain) or mapping approaches before
  building (that is explore).
---

# learn

Brief the operator on their OWN work so they can talk about it confidently — the
verbalization-ready mental model, high-level first, deeper on demand. Not a
from-scratch tutorial: extract and organize what was actually built. Read-only.

## When invoked

1. **Identify the artifact** from the operator's pointer — a PR number, commit
   range, branch, or work-item folder — and read what was actually DONE, not the
   title's promise:
   - PR → `gh pr view <n>` + `gh pr diff <n>` (or the branch diff), the linked
     issue, and the work-item folder (spec / reviews / verification) if present.
   - commit range / branch → `git diff <range>` + the commit messages.
   - work-item folder → the spec README, PR_BODY, reviews.
   Ground the model in the real diff/spec: name real components and real flow,
   never architecture invented from the title. If a decision's rationale isn't
   in the artifact, say so — don't fabricate a why the operator might repeat.

2. **Brief, high-level first** — plain language, the altitude of `plain` (no
   jargon or term-of-art names the operator would stumble over):
   - **Say-it-first** — 2-4 sentences to lead with: problem → what we built →
     the shape of the approach. The line the operator can repeat verbatim.
   - **The shape** — 3-6 bullets naming the pieces and how they connect (the
     data/control flow), so the operator can point at parts by name.
   - **Why it's built this way** — the load-bearing decisions, one-line
     rationale each; name the alternative not taken when it matters.
   - **If they ask…** — a few questions a reviewer / boss / teammate would
     realistically ask, each with a crisp answer. Real questions (the sharp
     "why not X", "what happens when Y", "how does Z scale"), not softballs.
   If the operator names the audience, pitch to them — a boss wants impact and
   the gist; a reviewer / teammate wants mechanism and tradeoffs. Keep it
   skimmable; do NOT dump file-level detail here.

3. **Offer drill-down.** End by inviting "go deeper on <piece>". On request,
   expand THAT piece only — mechanics + file:line + the real decision detail,
   still plain, just more specific. High-level stays the default; depth is pull.

4. **Save on request.** Default is the in-chat briefing. If asked to keep it,
   save to the work-item folder as `LEARN.md` (`status: reference`) or the path
   the operator names.

## Guardrails

- Read-only: comprehension, not changes — no edits, branch, or tracker/PR
  mutation (read-only `gh`/`git` to gather is fine).
- Accurate over impressive: what the operator repeats must be correct — ground
  every claim in the diff/spec and flag real uncertainty instead of smoothing it
  into a confident guess.
- High-level first; never lead with exhaustive detail.

Not this skill: restating the last message → `plain`; mapping approaches before
building → `explore`; researching a fresh issue → `spec`. `learn` explains work
that already exists.
