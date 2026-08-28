---
name: why
description: Investigate why unusual code, behavior, compatibility, or policy exists using repository evidence and history. Use for design rationale, regressions, historical constraints, and unexplained thresholds; not for runtime walkthroughs or speculative design preference.
metadata:
  opencode/autoinvoke: true
  workflow/kind: expert-guidance
---

# Why

Recover the most defensible rationale without turning plausible history into
fact. This skill is read-only advisory guidance: it does not select a workflow
phase, widen scope, edit code, require an artifact, dispatch mandatory helpers,
or certify a future design.

## Anchor the question

Start with the exact current symbol, behavior, rule, or threshold. Establish
enough mechanics to identify its owner, but do not cite current code shape as
proof of the intent that produced it.

Search the cheapest likely rationale owners first:

1. nearby comments, tests, documentation, and explicit decision records;
2. blame for the relevant lines, the introducing commit, and related file or
   symbol history through renames;
3. linked pull requests, issues, or review references already present in local
   history;
4. additional repository or external evidence only when it can change the
   conclusion and is available under the active authority boundary.

Ordinary local Git history and public pages are sufficient for most questions.
Authenticated trackers, private documents or chat, observability, analytics,
and provider calls remain subject to the active workflow's authority; do not
query every available system by default or treat an unavailable source as a
reason to stall.

## Keep the conclusion honest

- Treat direct statements of intent as evidence, with a precise commit, path,
  issue, or URL citation.
- Label conclusions assembled from timing, code changes, tests, or surrounding
  facts as inference and explain the chain.
- Surface contradictions instead of silently choosing the neatest story.
- Do not equate temporal proximity, present-day usefulness, or code shape with
  original intent.
- Say when no rationale was found and name the material source gap without
  manufacturing a narrative.

Return the current behavior, the evidence trail, the best-supported rationale
with calibrated confidence, contradictions or gaps, and whether that rationale
still constrains the user's current decision. If the user instead needs the
runtime flow, use `how`; if they want to choose a new approach, preserve that as
a separately selected design activity.
