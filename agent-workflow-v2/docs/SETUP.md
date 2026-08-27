# Setup and host configuration

Agent Workflow V2 uses one canonical local checkout with shared references.
Register skills through discovery links or host-configured paths; do not maintain
copied skill trees.

The recommended path is to give an existing agent this package and invoke
`setup-workflow`. It gathers preferences, checks installed capabilities without making
a model call, previews changes, and writes the user-level adapter only after
approval.

## Shared configuration

The adapter lives beside that checkout and is ignored by Git:

```text
<workflow-package>/HOST.local.md
```

It contains no credentials. It records enabled hosts, confirmed command shapes,
named model/reasoning profiles, workload preferences, and outer-gate routing.
Repository adapters remain project-specific and do not copy these preferences.

During beta, use any stable isolated path. The released default is
`$HOME/.agents/workflow`; the adapter records the absolute resolved location.

## Host registration

Use the host's current official mechanism and confirm it locally before writing
configuration:

- **Codex:** link each package skill into `~/.agents/skills/`. `codex exec
  --json` provides JSONL;
  `--model`, `--profile`, and `-c key=value` provide invocation overrides.
- **Claude Code:** link the same package skills into `~/.claude/skills/`.
  Non-interactive runs use `claude -p --output-format json` (or
  `stream-json`), with `--model`, `--effort`, and `--resume` when supported.
- **Cursor:** use the same `~/.agents/skills/` links as Codex, or register the
  package `skills/` directory. Headless runs use `agent --print
  --output-format json`; confirm model options from the installed CLI.
- **OpenCode:** use the same `~/.agents/skills/` links, or register the package
  `skills/` directory in `opencode.json`. Non-interactive runs use `opencode run
  --format json`, with `--model`, `--variant`, and `--session` when supported.

These are discovery links, not copies. Updating the central checkout updates all
hosts. If links are unavailable on Windows, use directory junctions or the
host's configured skills path; setup must not fall back to maintained copies.

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

Setup verifies executable/version, non-secret auth status, skill discovery,
shared-reference reachability, and documented structured-output flags without a
model call. A real prompt is optional and separately approval-gated because it
may consume paid usage.

## Release cutover

The beta directory exists only to prevent collisions while the workflow is
evaluated. After promotion is approved, setup previews one cutover: install the
release at `~/.agents/workflow`, register the release skill names, open fresh host
sessions to verify discovery, and then remove the superseded V1 and beta-only
registrations and files. Do not leave two kernels active.

Before that final removal, a failed cutover may restore the previously active
links. After cutover is validated and finalized, rollback installs a selected
released workflow revision; it does not retain V1 as a compatibility layer.

## Uninstall

Run `setup-workflow` and request uninstall. It previews the exact V2 skill
registrations/links and host adapter it will remove. After approval it removes
only those V2-created surfaces. It preserves the canonical checkout unless the
operator separately asks to delete it, and never removes host applications,
credentials, repositories, or unrelated skills/configuration.

## Current host references

- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Cursor CLI output formats](https://cursor.com/docs/cli/reference/output-format)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [OpenCode CLI](https://opencode.ai/docs/cli)
