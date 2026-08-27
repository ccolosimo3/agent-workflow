# Setup and host configuration

Agent Workflow V2 uses one canonical local checkout with shared references.
Installations register entrypoints through host discovery or configured package
paths; do not maintain copied skill trees. Before replacing an existing
workflow, stage and validate this package without changing active discovery.

The recommended path is to give an existing agent this package and invoke
`setup-workflow`. It gathers preferences, checks installed capabilities without making
a model call, previews changes, and writes the user-level adapter only after
approval.

## Activation

- **On-demand** is the recommended trial mode. Register explicit skills and
  commands, but leave each host's global kernel owner untouched. Ordinary tasks
  use the host's existing behavior; invoking a V2 phase loads the complete V2
  authorities for that task.
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
command shapes, named model/reasoning profiles, workload preferences, and
outer-gate routing.
Repository adapters remain project-specific and do not copy these preferences.

The default is `$HOME/.agents/workflow`; the adapter records the absolute
resolved location. A replacement cutover may use a stable staging path until
the active installation is ready to switch.

## Host registration

Before writing, scan every selected host's discovery roots for all release skill
or command IDs. Any match blocks ordinary installation rather than replacing or
ambiguously shadowing an active entrypoint; replacement requires the separately
approved cutover path.

Always register explicit-only phase entrypoints through the host's current
official mechanism. In always-on mode, also register one persistent route to the
central `references/KERNEL.md`. Preserve unrelated existing user instructions
and confirm only the selected surfaces locally.

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
- **Cursor:** register the package as a local Cursor plugin at user/personal
  scope and configure its `WORKFLOW_ROOT` variable to the package's absolute
  path. Normal Desktop setup is **Customize → Plugins → Add Marketplace →
  Import from Disk**; select the V2 repository root, add `agent-workflow-v2` at
  user/personal scope, and set the variable once. The plugin supplies explicit
  commands while disabling direct skill registration. In always-on mode, setup
  additionally renders the packaged kernel-rule template into the user's Cursor
  rules directory with the absolute package path; on-demand mode omits that
  rule. Check for the direct `cursor-agent` binary before using Cursor Desktop's
  `cursor agent` wrapper, which may install it; installation and login remain
  separately approved. Headless runs use `cursor-agent --print --output-format
  json`; confirm model options from the installed CLI.
- **OpenCode:** use the same `~/.agents/skills/` links, or register the package
  `skills/` directory in `opencode.json`. In always-on mode, resolve its config
  directory (for example, with `opencode debug paths`) and use that directory's
  `AGENTS.md`, normally `~/.config/opencode/AGENTS.md`. Point that exact owner at
  the central kernel when V2 owns it, or add a thin instruction to read the
  kernel without replacing unrelated guidance; on-demand mode leaves it
  unchanged. Non-interactive runs use `opencode run --format json`, with
  `--model`, `--variant`, and
  `--session` when supported.

In always-on mode, a fresh ordinary session must receive the kernel without
invoking a phase. In on-demand mode it must not. In both modes, a phase command
must resolve its canonical skill and shared authorities. Setup records the
activation mode, each entrypoint scope, and any kernel owner, then verifies the
selected surfaces before declaring a host ready.

Every release skill is explicit-only through the selected host's supported
control: Codex uses each skill's `agents/openai.yaml` policy; Claude Code sets
each release ID to `user-invocable-only` in `skillOverrides`; Cursor exposes
only the package's explicit command shims; and OpenCode uses
`metadata.opencode/autoinvoke: false`. Setup must verify that state before
declaring registration complete. Owning phases start required child phases by
naming that entrypoint explicitly in the fresh task's initial prompt.

Desktop command discovery does not prove headless command expansion. For Cursor
CLI automation, confirm the installed version's behavior or name the canonical
`SKILL.md` path directly in the prompt and expose the package root with the
supported workspace/additional-directory option.

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

- `risk-selected`: V2's positive risk rules select outer gates.
- `operator-invoked`: outer gates run only when explicitly requested.
- `disabled`: outer gates are absent from normal completion.

`prefer-different-host` supports both directions: Codex work can route to Claude,
and Claude work can route to Codex. Cursor and OpenCode can participate the same
way. A same-host fresh context remains a valid fallback when the operator allows
it. Direct operator instructions override stored preferences for that invocation.

## Verification and optional smoke test

Setup verifies executable/version, non-secret auth status, skill/command
discovery, shared-reference reachability, selected activation behavior, and
documented structured-output flags without a model call. A real prompt is
optional and separately approval-gated because it may consume paid usage.

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
registrations/links, kernel owners/scopes, and host adapter it will remove.
After approval it removes only those V2-created surfaces. It preserves the
canonical checkout unless the operator separately asks to delete it, and never
removes host applications, credentials, repositories, or unrelated
skills/configuration.

To pause V2 without uninstalling it, switch to on-demand mode. Setup previews
and removes only V2's persistent kernel routes, updates the matching host-adapter
records, and leaves explicit entrypoints and the canonical checkout available.

## Current host references

- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Cursor plugins and rules](https://cursor.com/docs/reference/plugins)
- [Cursor CLI output formats](https://cursor.com/docs/cli/reference/output-format)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [OpenCode instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode CLI](https://opencode.ai/docs/cli)
