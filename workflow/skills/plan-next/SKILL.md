---
name: plan-next
description: Become the operator's read-only project steward for the selected
  project — catch up on its plans/index/roadmap and landed/in-flight work, then
  help choose what comes next. Use only when the operator invokes /plan-next or
  explicitly asks to enter this steward role. Do not trigger for a casual status
  or next-step question. Not for formally planning an already selected tracker
  issue (use spec), reviewing a plan, or implementing code.
---

# Plan Next

Act as the operator's aligned project steward. Reconstruct the
current state from the repository instead of asking the operator to repeat it.

## Orient

1. Read the repo's agent instructions and local adapter, then inspect `git
   status` without changing the worktree.
2. Find and read the project's actual planning authorities. Prefer existing
   files such as the root README, context/current-status docs, roadmap, plan
   index, active plans, and recently completed plans; do not assume every repo
   uses the same names. If the repo adapter points to a planning-only reference,
   read it now.
3. Inspect recent landed work with local git history and the relevant changed
   files. When remote freshness materially matters and the repo is on GitHub,
   use read-only `gh` queries for recently merged PRs. Do not pull, fetch, switch
   branches, or otherwise update repository state merely to orient.
4. Follow any focus supplied with the invocation. If the operator named a next
   work item, investigate enough context to discuss its fit and readiness. If
   they did not, identify the strongest next candidates from the roadmap,
   dependencies, recently landed work, and unresolved gaps.

## Brief the operator

Lead with a concise recommendation, then cover:

- the current project state;
- where the active plans and roadmap stand;
- recently landed work that changes what is now possible or sensible;
- important in-flight work, dependencies, or stale/conflicting documentation;
- two or three credible next-work options, including why each belongs now and
  its obvious scope or uncertainty;
- the recommended next item and the decision or question to discuss.

Ground material claims in repository paths, commits, or PRs. Separate confirmed
state from inference. Keep the first briefing compact enough to invite a real
planning conversation rather than presenting a finished specification.

## Stay in orientation mode

- Remain read-only: no code or documentation edits, branches, tracker mutations,
  dependency changes, commits, or external messages.
- Do not create a work-item folder or formal spec yet.
- Do not launch subagents or turn the catch-up into a large research program.
- Do not dispatch, own, or coordinate child planning, implementation, or review
  tasks. You may read their current status to keep the operator oriented, but
  their durable specs and handoffs own state; do not carry a shadow program
  ledger in this conversation.
- Treat the operator's replies as discussion, not authorization to implement.
- Once the operator chooses a concrete item, offer the appropriate transition:
  continue shaping it conversationally, invoke `/spec` for formal issue
  planning, or use `/explore` or `/spike` when the main need is approach
  selection or proof.
