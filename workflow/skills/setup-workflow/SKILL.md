---
name: setup-workflow
description: Configure or audit workflow hosts, models, review routing, and repository onboarding. Use for installation, plan-storage setup, capability repair, or uninstall; not for repository implementation work.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

# Setup Workflow

Configure the package conversationally without changing its portable policy.

## Read first

Resolve this skill’s real package directory first when it was discovered through a link; relative paths below use that target, not the discovery-link directory.

Read `../../README.md`, `../../docs/SETUP.md`, and
`../../templates/host-adapter.md`. Resolve them from this skill's actual package
directory. Stop if any is unavailable; do not copy an individual skill away from
the package and silently break its shared references.

## Configure

1. Ask only for choices not already stated: activation mode (`on-demand` or
   `always-on`); hosts to enable; desired model and
   exact reasoning/variant profiles; fixed versus allowed profiles by workload;
   an optional single evidence-helper profile; outer-gate policy;
   different-host versus ordered reviewer choice; and same-host fresh-context
   fallback. Recommend on-demand for a trial and always-on only when the user
   wants V2 as their daily driver. Recommend risk-selected outer gates,
   different-host preference, and an allowed same-host fresh fallback when the
   installed hosts support them, but preserve the user's choice. Leave evidence
   helpers disabled when none is selected.
2. Inspect each selected host read-only using its executable, `--version`, local
   help, non-secret authentication/config status, model listing when locally
   available, skill discovery path, fresh launch/resume capability, and
   structured-output flags. Scan every active discovery root for all release
   skill or command IDs. Any match blocks ordinary installation; replacement
   uses only the separately approved cutover path. Never print credentials or
   make a model/provider call merely to test setup.
   For Codex, resolve `CODEX_HOME` and the active global instruction owner after
   `AGENTS.override.md` precedence. For OpenCode, resolve its config directory
   (for example, with `opencode debug paths`) and its resulting global
   `AGENTS.md`. For Cursor, inspect the selected plugin installation scope.
   For Cursor, check for the direct `cursor-agent` binary before invoking the
   Desktop `cursor agent` wrapper because the wrapper may install it.
3. Record exact confirmed commands and values in the host adapter. Do not invent
   unsupported reasoning equivalence or treat a model alias as stable when the
   host exposes an exact ID. Missing hosts stay unavailable and do not block the
   others.
4. Show the proposed package registration, activation mode, exact kernel owner
   and scope when always-on, host-adapter path, collision result, and any host
   config edits before writing.
   Preserve unrelated settings and request approval before mutating user
   configuration, installing/registering the package, or replacing an existing
   adapter. Never replace a skill outside the approved cutover. Installing a
   CLI, logging in, or running even a tiny paid smoke call is separate and
   requires explicit authorization.
5. After approval, register the package's user-facing entrypoints and advisory
   skills for automatic discovery, and its control-plane skills for explicit or
   declared internal invocation, through each selected host's supported
   mechanism. Follow `WORKFLOW.md`: discovery can recognize clear operator
   intent but cannot create intent, authority, artifacts, phase chaining, or
   fresh-context independence. In always-on mode, also
   register one persistent route to `KERNEL.md`: Codex's active global owner
   after `AGENTS.override.md` precedence, Claude Code's global `CLAUDE.md`
   import, a rendered user-level Cursor rule from the packaged template, or
   OpenCode's resolved global `AGENTS.md`. On-demand mode leaves those owners
   untouched. Preserve unrelated global instructions and block if always-on
   composition would shadow them or cannot be made safe. Preserve the packaged
   Codex and OpenCode invocation controls, set Claude Code `skillOverrides` to
   `user-invocable-only` only for the control-plane skills, and set Cursor's
   `WORKFLOW_ROOT` to the absolute package path. Leave advisory and user-facing
   entrypoints eligible for automatic invocation according to their narrow
   descriptions and host policy. Write the adapter, then verify automatic
   advisory and user-facing discovery, explicit-only control-plane entrypoints,
   shared-reference reachability, and either the active persistent route or its
   absence without a model call. Explain
   that a fresh session is required to prove loaded behavior; any such smoke
   remains separately approval-gated.

Do not infer Cursor CLI slash-command expansion from Desktop discovery. Confirm
the installed CLI behavior; otherwise invoke automation with a prompt that names
the canonical `SKILL.md` path and makes the package root readable.

The adapter is `HOST.local.md` at the canonical package root and is ignored by
Git. Host registrations point to that root; Cursor's thin command shims also
live there and load the same skill bodies. Never copy skill bodies or the adapter
into multiple maintained locations or duplicate its contents into repositories
or canonical workflow files.

## Repository onboarding

When onboarding a repository, inspect its adapter for a durable plan location.
If none exists, present `.agent-workflow/plans/` as the default private repo-local
directory excluded through `.git/info/exclude`; allow a tracked/custom location
or no durable storage when the user prefers it. Preview the exact directory,
exclusion, and adapter edit, then request approval before writing. Record private
storage in the local repository adapter and shared storage in the tracked adapter.
Initialize only `active/` and `archive/`; add `INDEX.md` when multiple work items
need coordination. Do not initialize a nested Git repository unless requested.

## Outer routing

The authoring or implementing agent reports its current host when known. For a
selected outer gate, `prefer-different-host` chooses the first configured
outer-review profile on another host; otherwise it follows the configured list.
Use the same-host fresh fallback only when allowed. Never launch more than one
outer reviewer, silently change the selected profile, or call a missing host.

## Audit and uninstall

An audit rechecks installed versions, command shapes, activation mode, any
recorded kernel owner and scope, package discovery, and adapter references, then
proposes only stale fields. Switching activation mode previews and adds or
removes only V2's persistent kernel routes and updates the matching activation
and per-host kernel records in `HOST.local.md`. Uninstall first previews and then
removes only V2-created kernel routes,
registrations, discovery links, and the V2 host adapter after approval. Preserve
the central checkout unless its deletion is separately requested, plus
repositories, credentials, unrelated host configuration and other skills/plugins.

For an approved release cutover, preview the canonical-path move, release skill
registrations, and legacy removals together. Inventory non-release personal
skills or scripts inside the old package and preserve retained utilities in the
user skill root before replacement. Switch discovery, verify the new names in
fresh host sessions, then remove superseded and staging surfaces; never leave
both kernels active. New installations skip this migration and install the
release directly.

Return a concise setup receipt: activation mode, enabled hosts and profiles,
workload and outer routing, capability gaps, files/registrations changed,
discovery checks, and any restart or optional paid smoke test remaining.
