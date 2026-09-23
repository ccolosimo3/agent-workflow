# Setup and host configuration

Agent Workflow V2 uses one canonical local checkout with shared references.
Installations register entrypoints through host discovery or configured package
paths; do not maintain copied skill trees. Before replacing an existing
workflow, stage and validate this package without changing active discovery.

The recommended path is to give an existing agent this package and invoke
`setup-workflow`. It gathers preferences, checks installed capabilities without making
a model call, previews changes, and writes the user-level adapter only after
approval.

First-time setup gives a three-sentence introduction, then proposes a configuration
using supplied preferences and the current confirmed host/model profile. It asks
only for missing choices needed for the preview. Defaults are on-demand for a
trial, selective outer review after inner approval, and the same profile in fresh
review contexts. Always-on is recommended for requested daily use. Each setting
gets one short explanation in the concrete approval preview; advanced options
wait until requested or needed. Helpers and receipts start disabled unless
explicitly selected. Existing installations keep their configured choices.
Setup ends with a concise summary, one example request, and any restart instruction.

## Activation

- **On-demand** is the recommended trial mode. Register the same skills,
  including automatic advisory and user-facing discovery, but leave
  each host's global kernel owner untouched. V2 loads only when a matching skill
  is selected by clear ordinary language or explicit invocation; unrelated tasks
  use the host's existing behavior.
- **Always-on** is the daily-driver mode. It uses the same package and
  entrypoints, plus one persistent host route to `references/KERNEL.md`.

Changing modes adds or removes only V2-owned persistent routes and updates the
matching activation/kernel records in `HOST.local.md`. It does not reinstall the
package, change other preferences, or alter repository adapters.

## Shared configuration

The adapter lives beside that checkout and is ignored by Git:

```text
<workflow-package>/HOST.local.md
```

It contains no credentials. It records activation mode, enabled hosts, confirmed
command shapes, named model/reasoning profiles, workload preferences by active
host, and outer-gate routing by actual author when hosts need different eligibility.
It may also enable one completion receipt store or record it
as `disabled`.
Repository adapters remain project-specific and do not copy these preferences.

Completion receipts are off by default and enabled only by explicit opt-in.
They are local evidence, not workflow state or certification. Disabled receipts
create no records or routine completion messages. When enabled, setup recommends
the platform's normal private user-data location (for example, Application Support
on macOS, `%LOCALAPPDATA%` on Windows, or `$XDG_DATA_HOME`/`~/.local/share` on Unix),
resolves and previews one canonical absolute directory outside the package and
product repositories,
checks private permissions and every enabled host's access, then creates only
that root after approval. Setup records the store as enabled only after this
succeeds. It never falls back to repository-local storage.

The default package path is `$HOME/.agents/workflow`; the adapter records the
absolute resolved location. A replacement cutover may use a stable staging path
until the active installation is ready to switch.

## Host registration

Before writing, scan every selected host's discovery roots for all release skill
IDs and legacy V2 Cursor command/plugin registrations. An existing skill link
that resolves to this exact canonical package is reusable. Every legacy V2
Cursor command/plugin registration and any other match blocks ordinary
installation rather than being left to shadow an entrypoint; removal or
replacement requires the separately approved cutover path.

Register user-facing entrypoints and advisory skills for automatic discovery,
and control-plane skills for explicit or declared internal invocation, through
the host's current supported mechanism. Discovery may recognize a clear
ordinary-language request, but `references/WORKFLOW.md` prevents relevance alone
from selecting or chaining a phase, creating artifacts, dispatching work,
granting authority, or claiming fresh-context independence. In always-on mode,
also register one persistent route to the central `references/KERNEL.md`.
Preserve unrelated existing user instructions and confirm only the selected
surfaces locally.

- **Codex:** link each package skill into `~/.agents/skills/`. In always-on mode,
  resolve `CODEX_HOME` and its active global instruction owner:
  non-empty `AGENTS.override.md` takes precedence over `AGENTS.md`. Point that
  exact owner at the central kernel when V2 owns it, or add a thin instruction
  to read the kernel without replacing unrelated guidance; block if it cannot
  be composed safely. On-demand mode leaves that owner unchanged. `codex exec
  --json` provides JSONL; `--model`, `--profile`, and `-c key=value`
  provide invocation overrides.
- **Claude Code:** link the package skills into `~/.claude/skills/`. In
  always-on mode, import the central kernel from `~/.claude/CLAUDE.md`, or point
  that file at the kernel when V2 owns it; on-demand mode leaves it unchanged.
  Non-interactive runs use `claude -p --output-format json` (or
  `stream-json`), with `--model`, `--effort`, and `--resume` when
  supported.
- **Cursor:** use the same canonical `~/.agents/skills/` links. Current Cursor
  discovers those skills automatically and exposes them for manual
  `/skill-name` invocation; do not also install command shims for the same IDs.
  Cursor has no verified name-only control, so control-plane skills remain
  discoverable under their narrow descriptions (see the classes below). In
  always-on mode, setup additionally renders the packaged kernel-rule template
  into the user's Cursor rules directory with the absolute package path;
  on-demand mode omits that rule. Check for the direct `cursor-agent` binary
  before using Cursor Desktop's `cursor agent` wrapper, which may install it;
  installation and login remain separately approved. Headless runs use
  `cursor-agent --print --output-format json`; confirm model options from the
  installed CLI.
- **OpenCode:** use the same `~/.agents/skills/` links, or register the package
  `skills/` directory through `skills.paths` in its configuration. In always-on
  mode, resolve its config directory with `opencode debug paths`, then add the
  canonical absolute `references/KERNEL.md` path once to `instructions` in the
  existing global `opencode.json` or `opencode.jsonc` (normally under
  `~/.config/opencode/`). Preserve other entries, agent settings, and unrelated
  `AGENTS.md` guidance. A textual instruction to read the kernel is not a host
  import: OpenCode does not automatically expand file references in `AGENTS.md`.
  Replace an old V2 read-pointer with this native route; avoid a second kernel
  copy or import. On-demand installation leaves global instructions unchanged.
  Non-interactive runs use `opencode run --format json`, with `--model`,
  `--variant`, and `--session` when supported.

OpenCode exposes a skill catalog, then loads each full skill through its `skill`
tool when needed. A skill body absent from initial context is expected, not a
discovery failure. Check `opencode debug skill` for canonical locations and
content, and the selected agent's effective skill-tool settings and permissions
for access; do not preload every skill into `instructions`.

In always-on mode, a fresh ordinary session must receive the kernel without
invoking a phase. In on-demand mode it must not. In both modes, a phase command
must resolve its canonical skill and shared authorities. Setup records the
activation mode, each entrypoint scope, and any kernel owner, then verifies the
selected surfaces before declaring a host ready.

Invocation has three classes across hosts:

- `typescript-engineering`, `technical-writing`, `blast-radius`, `how`, `why`,
  and `show-me` are automatic advisory guidance under their narrow descriptions.
- `explore`, `spike`, `spec`, `implement`, `review-pr`, and `project-lead` are
  automatic only when ordinary language clearly selects that user-facing work.
- `bro` is an explicit operator utility. Codex uses `agents/openai.yaml`; its
  `disable-model-invocation: true` frontmatter makes Claude Code and Cursor
  operator-only, and Claude Code also sets it to `user-invocable-only` in
  `skillOverrides`.
- `setup-workflow`, `review-change`, `review-spec`, `independent-review`, and
  `independent-spec-review` are explicit/internal control-plane skills: the
  operator or an owning phase that names one may invoke it, but description
  matching must not select it. Codex uses `agents/openai.yaml`; Claude Code sets
  these IDs to `name-only` in `skillOverrides`, which lists the name without its
  description. Never package these with `disable-model-invocation: true` or set
  them to `user-invocable-only` or `off`: Claude Code and Cursor then refuse the
  owning phase's invocation, so its required review or setup step cannot run.
  Cursor has no verified name-only control, and OpenCode's packaged
  `metadata.opencode/autoinvoke` expresses intent but is not a documented native
  invocation control. On both, the explicit/internal boundary relies on skill
  descriptions and `WORKFLOW.md`; record the lack of host enforcement as a
  capability gap unless the installed version provides a verified supported
  control.

Setup must distinguish these intended classes from host-enforced controls and
record any enforcement gaps before declaring registration complete.
Owning spec and implementation phases invoke their required review children by
name, in their own task or in a fresh task's initial prompt; the operator does
not need to invoke those review loops separately. Setup therefore verifies that
each control-plane skill stays invocable by name on every registered host, not
only that description matching cannot select it.

Desktop skill discovery does not prove headless slash-command expansion. For
Cursor CLI automation, confirm the installed version's behavior or name the
canonical `SKILL.md` path directly in the prompt and expose the package root
with the supported workspace/additional-directory option.

These registrations point to the central package rather than copying kernel or
skill bodies. Updating the central checkout updates all hosts. If links are
unavailable on Windows, use directory junctions or the host's configured package
path; setup must not fall back to maintained copies.
Replacing an existing registration is permitted only in a separately approved
cutover.

Do not bake permission bypasses into V2. The setup agent records the user's
existing safe mode or asks which documented mode they want; it does not enable a
more permissive mode implicitly.

## Repository setup

Defer repository storage choices until onboarding is requested or durable planning
needs a location.

Keep project facts in one tracked repository adapter, normally the repo's
`AGENTS.md` when its hosts support it. Add only a thin native pointer/import for a
host that does not read that owner directly. Do not copy V2 policy or host/model
preferences into the repository. The setup agent verifies the selected hosts can
reach both the repository adapter and central V2 package before declaring setup
complete.

For durable plans, the default is a private `.agent-workflow/plans/` inside the
repository, excluded through `.git/info/exclude` and declared in its local
adapter. Setup previews those writes before approval. A user may instead select a
tracked or custom path, an existing plan owner, or no durable storage. New private
stores start with only `active/` and `archive/`; `INDEX.md` appears when multiple
work items need coordination. No nested Git repository is created by default.

## macOS and Windows

On macOS, use the installed host CLI and normal `$HOME` paths. On Windows, use
the environment supported by that host—native paths, Git Bash, or WSL—and keep
the package and adapter in the same environment from which the host runs.
OpenCode recommends WSL for its fullest Windows compatibility. The setup agent
must show resolved paths before creating links or configuration.

## Outer-review choices

Inner review is the first fresh independent check of a formal spec or
implementation. Outer review adds a second fresh independent check when selected.
The author handles corrections and follow-up reviews; both reviewers may use the
same model.

Choose one policy; it controls frequency, independently of reviewer models:

| Policy | When outer review runs |
| --- | --- |
| `broad` | Most formal specs and implementations; skips clearly small, well-defined work with straightforward proof and no material risk. Borderline work gets reviewed. |
| `selective` (default) | Material risk under `WORKFLOW.md`, or an explicit request. |
| `by-request` | Only on an explicit request, at any risk level. |

An explicit request works in every mode. Apply the policy separately to spec and
implementation; their fresh inner reviews remain required. Existing
`risk-selected` maps to `selective`; `operator-invoked` and `disabled` map to
`by-request`. Updating the package does not silently change an existing choice.

Timing is separate: `Outer timing: after-inner` is the default; `concurrent`
starts both reviews on the same unchanged candidate and requires the outer's
final convergence check under `REVIEW.md`. This optional `HOST.local.md` setting
may apply globally or to an explicitly named route.

`Inner review: inherit` keeps the actual author's host and profile in a fresh
context. Record the host's native isolated-agent launch, or its same-host fresh
CLI fallback. A coordinator's host and a saved coworker-review recipe do not
override that choice.

Both passes use the same review standards. Outer review adds a blind assessment
and certifies the converged candidate; it must not inherit the author's or inner
reviewer's conversation. A fresh native subagent can perform either pass when
the host supports that isolation. A separate model or subscription is optional.

For one available host/profile, recommend this configuration using that user's
selected profile; no extra routing setting is needed:

```text
Policy: selective
Reviewer choice: ordered
Ordered outer-review profiles: <available host/profile>
Same-host fresh-context fallback: allowed
```

The outer profile may be exactly the same as the author's and inner reviewer's.
Each initial review still launches separately; choose `broad` for more frequent
outer review or `by-request` for manual selection.
With multiple available hosts, offer `prefer-different-host` as a preference,
or keep an ordered profile list. Author-specific lists and exclusions can impose
stricter host or model-family choices when the user wants them; never copy
another user's restrictions into a new installation or silently relax existing
ones. Apply them before ordering or fallback. The author is the agent that
produced the artifact, even when a different host coordinated the work.
`WORKFLOW.md` owns resolution and unavailable/unknown-origin rules. Confirm the
actual review model; a prior smoke probe does not prove that a later run avoided
substitution. Direct operator instructions override stored preferences for that
invocation.

## Verification and optional smoke test

Setup verifies executable/version, non-secret auth status, skill discovery and
access, shared-reference reachability, the configured activation route, and
documented structured-output flags without a model call. For OpenCode, check
`opencode debug config` for the resolved kernel entry and confirm that its file
is readable. Configuration and discovery checks do not prove what a model
received or followed. Restart OpenCode and use a fresh session to check runtime
loading; a model smoke test is optional and separately approval-gated because it
may consume paid usage. Report it as unrun when only local diagnostics were used.

## Release cutover

When replacing an existing workflow, setup previews one cutover: install the
release at `~/.agents/workflow`, register the release skill names, open fresh
host sessions to verify discovery, and then remove superseded registrations and
staging files. Do not leave two kernels active.

Before replacement, inventory non-release personal skills or scripts stored
inside the superseded package. Move each retained utility to the user's normal
skill root, update its canonical references, validate it, and repoint its host
registrations before removing the old tree. Do not silently drop or absorb
personal utilities into the portable release.

Before final removal, a failed cutover may restore the previously active links.
After cutover is validated and finalized, rollback installs a selected released
workflow revision; it does not retain the superseded workflow as a compatibility
layer.

## Uninstall

Run `setup-workflow` and request uninstall. It previews the exact V2 skill
registrations/links, legacy V2 Cursor command/plugin registrations, kernel
owners/scopes, and host adapter it will remove. After approval it removes only
those V2-created surfaces. It preserves the canonical checkout unless the
operator separately asks to delete it, and never removes host applications,
credentials, repositories, unrelated skills/configuration, or completion
receipt data unless that data deletion is separately requested.

To pause V2's always-on kernel routing without uninstalling its skills, switch to
on-demand mode. Setup previews and removes only V2's persistent kernel routes,
updates the matching host-adapter records, and leaves automatic and explicit
skill entrypoints plus the canonical checkout available. Removing skill
discovery requires uninstalling those host registrations.

## Current host references

- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Cursor plugins and rules](https://cursor.com/docs/reference/plugins)
- [Cursor CLI output formats](https://cursor.com/docs/cli/reference/output-format)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [OpenCode rules and instruction files](https://opencode.ai/docs/rules/#referencing-external-files)
- [OpenCode CLI](https://opencode.ai/docs/cli)
