# Worktree Destruction Tripwire

`worktree_tripwire.py` is a low-friction Codex `PreToolUse` hook. It allows
ordinary Bash commands immediately and denies recognizable destructive commands
when their mutation targets cannot be proven to remain inside the active Git
worktree.

It covers:

- `rm`, `rmdir`, `unlink`, `shred`, and `mv`
- `find -delete` and destructive `find -exec` forms
- `rsync --delete*` and `rsync --remove-source-files`
- nested shell commands passed through `bash -c`, `sh -c`, and common shells
- obvious privileged or system-destructive commands (`sudo`, `doas`, `diskutil`,
  and `mkfs*`)

Targets are checked after resolving relative paths, `..`, known environment
variables, user-home expansion, glob matches, and symlinks. A destructive command
fails closed when its target is dynamic, ambiguous, or outside a Git worktree.
There is no approval override: an out-of-worktree destructive operation must be
performed directly by the operator.

This is a tripwire, not a sandbox. It cannot determine what arbitrary scripts,
interpreters, aliases, binaries, MCP tools, or un-intercepted execution paths will
do. Reads and ordinary writes outside the worktree are intentionally out of scope.

## Verify

```bash
python3 -m unittest discover -s "$HOME/.agents/workflow/hooks/tests" -v
```

The tests pass hook payloads to the real executable. They do not execute any of
the commands in those payloads.

## Optional Codex configuration

The hook is not activated merely by existing in this directory. To enable it,
merge the following entry into `~/.codex/hooks.json`, restart Codex, and trust the
new hook through `/hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.agents/workflow/hooks/worktree_tripwire.py\""
          }
        ]
      }
    ]
  }
}
```

Enabling the hook is a separate activation decision because a hook denial cannot
be overridden by an ordinary Codex approval.
