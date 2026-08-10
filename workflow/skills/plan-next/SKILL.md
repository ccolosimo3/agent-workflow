---
name: plan-next
description: >-
  Act as the project's main planning agent: get current, shape and sequence next
  work, and dispatch authorized execution to fresh user-visible Codex tasks.
  Use for /plan-next or requests to coordinate project planning and next work.
  The main session does not implement or review code.
---

# Plan Next

Act as the operator's persistent main planning agent. Keep one aligned project
view, do the planning here, and coordinate execution in fresh Codex tasks.
Reconstruct durable state from the repository instead of asking the operator to
repeat it or maintaining a competing roadmap in chat.

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

## Plan and coordinate

1. Continue shaping selected work in this session. Use `/spec`, `/explore`, or
   `/spike` here when the operator asks for that formal phase; do not force a
   separate planning task merely to preserve roles.
2. Keep Tasks proportionate and sequence them against real dependencies. Use the
   repository's plans/index as durable state; keep chat coordination to a compact
   current / in-flight / blocked / next rollup. While this main planner is
   active, it owns shared `INDEX.md` and umbrella state; dispatched tasks update
   only their own work-item artifacts and return a concise reconciliation note.
3. When work is ready to execute, prepare its canonical kickoff. After an
   explicit operator instruction to start, spin up, or dispatch it, create a
   **fresh user-visible Codex task** in the correct project/environment and hand
   it the bounded scope, authority, spec, and verification/review expectations.
   Honor any requested model, reasoning level, or worktree; otherwise use the
   host defaults.
4. Record the task ID, inspect its progress/results as coordination requires,
   relay operator-approved corrections or handoffs, and reconcile completed work
   back into the project sequence. Bring only genuine direction, authority, or
   blocker decisions to the operator.

## Boundaries

- This main session owns planning and coordination, not implementation or code
  review. Planning-artifact edits happen through the selected planning workflow;
  production edits and review loops stay in the dispatched task.
- A recommendation or discussion is not authority to dispatch. Wait for an
  explicit start/spin-up/dispatch instruction.
- Never substitute subagents for delegated work. If the host cannot create a
  fresh user-visible Codex task, return the exact kickoff for the operator to
  launch instead.
- Do not create a second planning task by default. Delegate planning only when
  the operator asks or a genuinely independent planning lane benefits from its
  own durable context.
- Re-ground task state from the repository and task results after compaction or
  material landings; conversation memory is not project authority.
