# Workflow Sync And Transfer

Use the private workflow repo as the normal way to sync portable workflow files
between machines. Use a zip transfer only as a fallback for repo-local shims or
when GitHub access is unavailable.

Preferred repo:

```text
https://github.com/odysian/agent-workflow
```

## GitHub Sync

The repo root is `%USERPROFILE%\.agents` (re-rooted from
`%USERPROFILE%\.agents\workflow` on 2026-06-10). It tracks portable
agent/workflow files only, such as:

- `%USERPROFILE%\.agents\workflow\AGENTS.md`
- `%USERPROFILE%\.agents\workflow\KICKOFFS.md`
- `%USERPROFILE%\.agents\workflow\skills\` (workflow trigger skills)
- workflow templates and transfer instructions

Installer-managed top-level state (`.skill-lock.json`, top-level `skills\`)
and OS junk are ignored by the root `.gitignore`. Add new top-level
directories deliberately, not by default.

Do not put repo-local `AGENTS.md`, `CLAUDE.md`, `COMMANDS.md`, or
`CONTEXT.md` files in this portable workflow repo. Those are local shims and
domain notes for a specific checkout. Keep them in the project checkout, ignore
them with `.git/info/exclude`, and sync them manually only when needed.

Common sync commands:

```powershell
cd $env:USERPROFILE\.agents
git pull --ff-only
git status --short
git add workflow
git commit -m "Update agent workflow"
git push
```

Before pushing, scan changes for secrets, local credentials, device
identifiers, and personal paths.

### One-Time Migration For Old Clones

A machine still cloned at `%USERPROFILE%\.agents\workflow` must NOT plain
`git pull` after the re-root — it would nest a second `workflow\` inside the
old checkout. Migrate once instead:

```powershell
cd $env:USERPROFILE\.agents\workflow
git status --short        # must be clean; commit or stash local changes first
git fetch origin
Move-Item .git ..\.git
cd ..
git reset --hard origin/main
```

`git reset --hard` is safe here only because the tree was confirmed clean
before moving `.git`; it follows the destructive-action approval rules.
Alternatively, delete the old clone and re-clone into
`%USERPROFILE%\.agents`, then restore any ignored local state.

## Zip Transfer Fallback

## What To Package

Package local-only agent and workflow files, not generated project output.

Include:

- `%USERPROFILE%\.agents\`
- repo-local `AGENTS.md`, `CLAUDE.md`, `COMMANDS.md`, and `CONTEXT.md` if present
- repo `.git/info/exclude` contents, saved as a text file for merging
- top-level local planning/workflow docs when the operator asks for plans to
  move with the workflow

Exclude:

- `%USERPROFILE%\.agents\.git\` — the repo syncs via GitHub; do not zip it
- `.codex/` app state unless the operator explicitly asks for it
- `node_modules/`, `.expo/`, Gradle/CMake caches, build output, and logs
- nested `.git/` directories inside local planning folders
- secrets, tokens, credentials, device identifiers, and machine-specific cache
  files

## Pack Workflow

1. Ask the operator which repo-local docs should travel with the portable
   workflow if the scope is unclear.
2. Stage files under a timestamped folder such as
   `tmp/agent-workflow-transfer-YYYY-MM-DD/`.
3. Preserve the target layout inside the package:
   - `home/.agents/...`
   - `repos/<repo-name>/AGENTS.md`
   - `repos/<repo-name>/CLAUDE.md`
   - `repos/<repo-name>/COMMANDS.md`
   - `repos/<repo-name>/git-info-exclude.txt`
4. Add a `MANIFEST.md` describing contents, omissions, and install notes.
5. Create a zip only after the operator confirms the staged contents are ready.

## Unpack Workflow

1. Copy `home/.agents/` into `%USERPROFILE%\.agents\` on the target machine.
2. Copy files under `repos/<repo-name>/` into that repo checkout.
3. Merge `repos/<repo-name>/git-info-exclude.txt` into the target checkout's
   `.git/info/exclude`.
4. Do not overwrite machine-specific command paths blindly. If paths differ,
   update the repo-local shim and command docs after unpacking.
5. Verify with:

```powershell
Test-Path $env:USERPROFILE\.agents\workflow\AGENTS.md
Test-Path $env:USERPROFILE\.agents\workflow\KICKOFFS.md
Test-Path .\AGENTS.md
git check-ignore -v AGENTS.md
```

## Workflow Update Reminder

When this package is refreshed after workflow changes, update this file first
so the sync/transfer instructions travel with the package.
