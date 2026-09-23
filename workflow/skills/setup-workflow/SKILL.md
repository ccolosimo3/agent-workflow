---
name: setup-workflow
description: Configure or audit workflow hosts, models, review routing, and repository onboarding. Use for installation, plan-storage setup, capability repair, or uninstall; not for repository implementation work.
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

## First-time introduction

Give at most three short sentences, about 60 words, before presenting settings.
Adapt this example; skip it for returning users and audits:

> Describe what you want; the agent plans as needed, implements, and verifies it.
> A fresh reviewer checks the work ("inner review"); higher-risk changes can get
> a second independent check ("outer review"), using the same model if needed.
> The agent handles corrections and asks you about consequential behavior or scope
> decisions.

Explain more only when requested or needed for a setup decision.

## Configure

1. Preserve existing choices; apply defaults only to new, unset preferences.
   Use supplied preferences and reliably detected host/profile facts to propose
   a configuration. Ask only for missing choices needed to make that preview
   concrete, such as the intended app/profile or trial versus daily use; do not
   turn defaults into separate questions. Recommend `on-demand` for a trial or
   `always-on` for requested daily use, the current confirmed model/reasoning
   profile, `selective` outer review, and `after-inner` timing.
   Start with the selected profile for ordinary work, `Inner review: inherit`,
   and `ordered` outer review using that profile with same-host fresh contexts
   allowed. Confirm the host can isolate both reviews. If multiple hosts are
   selected, use each host's selected profile for its own work and fresh reviews;
   record author-specific outer lists when needed to express that routing.
   Defer advanced workload routing, review timing, different-host preferences,
   exclusions, helpers, and receipts unless requested or a concrete capability
   gap needs a choice. Helpers and receipts stay disabled unless explicitly
   selected; configuring them later uses the same preview and approval process.
   Existing profiles, exclusions, helpers, and receipt settings are retained
   unless the operator asks to change them.
2. Inspect each selected host read-only using its executable, `--version`, local
   help, non-secret authentication/config status, model listing when locally
   available, skill discovery path, fresh launch/resume capability, and
   structured-output flags. Scan every active discovery root for all release
   skill IDs and legacy V2 Cursor command/plugin registrations. An existing
   skill link that resolves to this exact canonical package is reusable. Every
   legacy V2 Cursor command/plugin registration and any other match blocks
   ordinary installation; removal or replacement uses only the separately
   approved cutover path. Never print credentials or make a model/provider call
   merely to test setup.
   For Codex, resolve `CODEX_HOME` and the active global instruction owner after
   `AGENTS.override.md` precedence. For Claude Code, compare `skillOverrides`
   with the package: only explicit operator utilities may be
   `user-invocable-only`, and control-plane skills must be `name-only`. Include
   stale overrides on advisory or user-facing skills in the previewed removal,
   and any control-plane skill set to `user-invocable-only` or `off` in the
   previewed repair. Report a control-plane skill packaged with
   `disable-model-invocation: true` as package drift, fixed by updating the
   package rather than editing its installed frontmatter. For OpenCode, resolve
   its config directory with `opencode debug paths`; inspect global JSON/JSONC
   `instructions`, `AGENTS.md`, the resolved `opencode debug config`, and
   `opencode debug skill`.
   Check the selected agent's effective skill-tool settings and permissions;
   catalog discovery and on-demand body loading are separate from kernel startup.
   For Cursor, inspect native `~/.agents/skills/` discovery,
   `~/.cursor/rules/`, and any legacy V2 command/plugin registrations. Check for
   the direct `cursor-agent` binary before invoking the
   Desktop `cursor agent` wrapper because the wrapper may install it.
3. Record exact confirmed commands and values in the host adapter. Do not invent
   unsupported reasoning equivalence or treat a model alias as stable when the
   host exposes an exact ID. Missing hosts stay unavailable and do not block the
   others.
   Update existing settings in place; keep the adapter focused on current
   configuration, dated capability evidence, and unresolved limitations rather
   than superseded history or repeated portable policy.
4. Present recommended settings with one short plain-language explanation each
   in one concrete approval preview, not a separate tutorial or feature list.
   Show the proposed package registration, activation mode, exact kernel owner
   and scope when always-on, host-adapter path, completion-receipt setting,
   collision result, and any host config edits before writing. For an enabled
   receipt store, recommend the platform's private user-data area, then resolve
   symlinks and preview the selected canonical absolute user-local path outside
   the package and product repositories, its permissions, directory creation,
   and every enabled host's access. Accept another user-selected path when those
   properties hold. Leave it disabled rather than using a repository-local
   fallback when containment, privacy, or access cannot be established.
   Preserve unrelated settings and request approval before mutating user
   configuration, installing/registering the package, or replacing an existing
   adapter. Never replace a skill outside the approved cutover. Installing a
   CLI, logging in, or running even a tiny paid smoke call is separate and
   requires explicit authorization.
5. After approval, first create and verify only an enabled configured private
   receipt root; keep the adapter value disabled if that fails, and do not write
   a sample receipt or make a model call. Then register the package's user-facing
   entrypoints and advisory skills for automatic discovery, and its explicit
   utilities and control-plane skills for explicit or declared internal
   invocation, through each selected host's supported mechanism. Follow
   `WORKFLOW.md`: discovery can recognize
   clear operator intent but cannot create intent, authority, artifacts, phase
   chaining, or fresh-context independence. In always-on mode, also
   register one persistent route to `KERNEL.md`: Codex's active global owner
   after `AGENTS.override.md` precedence, Claude Code's global `CLAUDE.md`
   import, a rendered user-level Cursor rule from the packaged template, or
   an absolute kernel path in OpenCode's global JSON/JSONC `instructions` list.
   OpenCode does not import paths mentioned in `AGENTS.md`; replace an old V2
   read-pointer with the native route, preserving unrelated entries and guidance
   and avoiding duplicate kernel loads. On-demand mode leaves those owners
   untouched. Preserve unrelated global instructions and block if always-on
   composition would shadow them or cannot be made safe. Preserve packaged
   invocation metadata, but do not claim OpenCode enforces `opencode/autoinvoke`
   without verified host support; record that capability gap. Set Claude Code
   `skillOverrides` to `user-invocable-only` only for explicit operator
   utilities and to `name-only` for control-plane skills, so owning phases can
   invoke them by name.
   Cursor uses the shared `~/.agents/skills/` links for automatic discovery and manual
   slash invocation; do not install command shims for the same IDs. Leave
   advisory and user-facing entrypoints eligible for automatic invocation
   according to their narrow descriptions and host policy. Verify discovery,
   access and supported invocation controls for each class, including that no
   host control blocks an owning phase from invoking a control-plane skill by
   name, shared-reference reachability, and either the configured persistent
   route or its absence without a model call, then write the adapter with the
   verified receipt setting and any capability gaps. Do not preload skill
   bodies or equate configuration with observed model context. Explain that a
   host restart and fresh session are required to check loaded behavior; any
   model smoke remains separately
   approval-gated and must be reported as unrun when omitted.

Do not infer Cursor CLI slash-command expansion from Desktop discovery. Confirm
the installed CLI behavior; otherwise invoke automation with a prompt that names
the canonical `SKILL.md` path and makes the package root readable.

The adapter is `HOST.local.md` at the canonical package root and is ignored by
Git. Host registrations point to that root. Never copy skill bodies or the adapter
into multiple maintained locations or duplicate its contents into repositories
or canonical workflow files.

## Repository onboarding

Defer repository storage choices until repository onboarding is requested or
durable planning needs a location.

When onboarding a repository, inspect its adapter for a durable plan location
and reuse its declared planning structure under `../../references/PLANNING.md`.
If none exists, present `.agent-workflow/plans/` as the default private repo-local
directory excluded through `.git/info/exclude`; allow a tracked/custom location
or no durable storage when the user prefers it. Preview the exact directory,
exclusion, and adapter edit, then request approval before writing. Record private
storage in the local repository adapter and shared storage in the tracked adapter.
For a new default private planning area, initialize only `active/` and `archive/`;
add `INDEX.md` when multiple work items need coordination. Do not initialize a
nested Git repository unless requested.

## Outer routing

Record workload preferences by the host doing the phase and use `WORKFLOW.md`'s
inner-inheritance and outer-eligibility rules. Keep the actual author's host and
profile separate from the dispatching coordinator. Record any author-specific
outer lists, complexity tiers, and exclusions; a fallback cannot escape those
lists. Describe fresh native-agent launch and same-context resume where supported,
including whether launch inherits conversation history. Both initial review
passes require separate fresh contexts and use the same review standards; a
different model cannot compensate for inherited author or prior-review history.
Do not require another subscription or copy the installer's personal exclusions.
Preserve existing policy names through `WORKFLOW.md`'s compatibility mappings;
never change review frequency merely during an upgrade. Confirm routing with
read-only examples for the selected mode: a small clear change, a material-risk
change, an explicit request, each configured origin, a same-model outer when
allowed, and an unavailable capability. Preserve explicit
exclusions instead of silently falling back outside them. Do not launch model
smoke calls as part of this check.

## Audit and uninstall

An audit rechecks installed versions, command shapes, activation mode, receipt
store configuration/access, any recorded kernel owner and scope, package
discovery, and adapter references, then proposes only stale fields. Switching
activation mode previews and adds or removes only V2's persistent kernel routes
and updates the matching activation and per-host kernel records in
`HOST.local.md`. Uninstall first previews and then removes only V2-created kernel
routes, skill registrations and discovery links, legacy V2 Cursor command/plugin
registrations, and the V2 host adapter after approval. Preserve the receipt
store and records unless their deletion is separately requested, plus the
central checkout unless its deletion is separately requested, repositories,
credentials, unrelated host configuration, and other skills/plugins.

For an approved release cutover, preview the canonical-path move, release skill
registrations, and legacy removals together. Inventory non-release personal
skills or scripts inside the old package and preserve retained utilities in the
user skill root before replacement. Switch discovery, verify the new names in
fresh host sessions, then remove superseded and staging surfaces; never leave
both kernels active. New installations skip this migration and install the
release directly.

Return a concise setup summary: activation mode, enabled hosts and profiles,
workload and outer routing, completion-receipt setting, capability gaps,
files/registrations changed, discovery checks, and any restart or optional paid
smoke test remaining. For first-time setup, finish with one example request,
such as "Implement this fix and verify it." Do not repeat the introduction.
