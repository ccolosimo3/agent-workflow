# Native Windows + Git Bash bootstrap

This kit wires a checkout of the private `agent-workflow` repository into
Codex and Claude Code on native Windows. It uses Git Bash as the shell and
keeps the repository itself as the single source of truth.

It deliberately does **not** copy authentication state, project trust records,
plugin caches, MCP runtime paths, secrets, or machine-specific safety hooks.
It also does not weaken either app's approval or sandbox defaults.

## Expected layout

Run these commands in Git Bash:

```bash
gh auth status
gh repo clone ccolosimo3/agent-workflow "$HOME/.agents"
cd "$HOME/.agents"
```

The wiring scripts default to:

- workflow source: `$HOME/.agents`
- Codex home: `$HOME/.codex`
- Claude home: `$HOME/.claude`

Override those locations for a nonstandard setup with `AGENTS_HOME`,
`CODEX_HOME`, or `CLAUDE_HOME`.

## Prerequisites

1. Install current Git for Windows, GitHub CLI, Codex, and Claude Code.
2. Turn on Windows Developer Mode. File symbolic links otherwise usually need
   an elevated shell.
3. Configure the ChatGPT/Codex desktop integrated terminal to use Git Bash.
4. Tell Claude Code where Git Bash lives, using the path actually present on
   the machine:

   ```bash
   cmd.exe /d /s /c 'setx CLAUDE_CODE_GIT_BASH_PATH "C:\Program Files\Git\bin\bash.exe"'
   ```

   Restart Claude Code after setting it. If Git is installed elsewhere, do not
   use the example path blindly.

Official references:

- Codex Windows: <https://developers.openai.com/codex/windows>
- Codex configuration: <https://developers.openai.com/codex/config-basic>
- Claude Code setup: <https://code.claude.com/docs/en/setup>
- Claude Code settings: <https://code.claude.com/docs/en/settings>

## Wire the kernel and skills

Preview first:

```bash
bash workflow/bootstrap/windows-git-bash/wire-workflow.sh
```

Apply after inspecting the preview:

```bash
bash workflow/bootstrap/windows-git-bash/wire-workflow.sh --apply
bash workflow/bootstrap/windows-git-bash/verify-workflow.sh
```

The script creates:

- `$HOME/.codex/AGENTS.md` -> the portable kernel
- `$HOME/.claude/CLAUDE.md` -> the portable kernel
- one directory junction per private workflow/personal skill under both apps'
  `skills/` directories

It never removes or overwrites an existing path. A collision stops the run and
must be inspected manually. Rerunning an already-correct setup is safe.

## Apply portable preferences

The adjacent configuration fragments are references, not replacement files:

- merge `codex-config.fragment.toml` into `$HOME/.codex/config.toml`
- merge `claude-settings.fragment.json` into `$HOME/.claude/settings.json`

Do not overwrite an app-generated configuration file. Sign in and authorize
plugins/connectors independently on the Windows machine. Those records are
machine state, not workflow source.

The Codex fragment intentionally omits `approval_policy` and `sandbox_mode`.
Start with the app defaults on this machine; the out-of-worktree tripwire is
outside this bootstrap's scope.

## App smoke test

After restarting both apps, open a disposable local repository and ask each
app:

> Identify the loaded portable kernel and list the private workflow skills you
> can discover. Do not modify any files.

Then invoke `/bro` or `/plan-next` in an appropriate project. Filesystem
verification proves the links; this smoke test proves app discovery.
