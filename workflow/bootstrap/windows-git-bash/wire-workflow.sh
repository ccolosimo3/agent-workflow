#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: wire-workflow.sh [--apply]

Without --apply, prints the links it would create. With --apply, creates only
missing links and refuses to overwrite or replace any existing non-matching
path.

Optional environment variables:
  AGENTS_HOME   workflow checkout (default: $HOME/.agents)
  CODEX_HOME    Codex home       (default: $HOME/.codex)
  CLAUDE_HOME   Claude home      (default: $HOME/.claude)
  LINK_BACKEND  auto|windows|posix (posix is intended for fixture testing)
EOF
}

apply=false
case "${1:-}" in
  "") ;;
  --apply) apply=true ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

agents_home="${AGENTS_HOME:-$HOME/.agents}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"
backend="${LINK_BACKEND:-auto}"

if [[ "$backend" == auto ]]; then
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) backend=windows ;;
    *) backend=posix ;;
  esac
fi

if [[ "$backend" != windows && "$backend" != posix ]]; then
  echo "ERROR: LINK_BACKEND must be auto, windows, or posix." >&2
  exit 2
fi

kernel="$agents_home/workflow/AGENTS.md"
workflow_skills="$agents_home/workflow/skills"
personal_skills="$agents_home/skills"

[[ -f "$kernel" ]] || {
  echo "ERROR: kernel not found at $kernel" >&2
  exit 1
}
[[ -d "$workflow_skills" ]] || {
  echo "ERROR: workflow skill directory not found at $workflow_skills" >&2
  exit 1
}

same_link() {
  local source=$1 target=$2
  if [[ -L "$target" ]]; then
    [[ "$(cd "$(dirname "$source")" && pwd -P)/$(basename "$source")" == "$(readlink -f "$target")" ]]
    return
  fi

  # Git Bash can expose a Windows junction as a directory rather than a POSIX
  # symlink. Accept it only when Windows confirms it is a reparse point and its
  # canonical marker file is byte-identical to the source.
  if [[ "$backend" == windows && -e "$target" ]] && command -v cygpath >/dev/null 2>&1; then
    local target_win
    target_win=$(cygpath -aw "$target")
    if MSYS2_ARG_CONV_EXCL='*' cmd.exe /d /s /c "fsutil reparsepoint query \"$target_win\"" >/dev/null 2>&1; then
      if [[ -d "$source" ]]; then
        cmp -s "$source/SKILL.md" "$target/SKILL.md"
      else
        cmp -s "$source" "$target"
      fi
      return
    fi
  fi
  return 1
}

ensure_directory() {
  local directory=$1
  if [[ -d "$directory" ]]; then
    return
  fi
  if $apply; then
    mkdir -p "$directory"
    echo "created directory: $directory"
  else
    echo "would create directory: $directory"
  fi
}

create_link() {
  local kind=$1 source=$2 target=$3

  if [[ -e "$target" || -L "$target" ]]; then
    if same_link "$source" "$target"; then
      echo "already linked: $target"
      return
    fi
    echo "ERROR: refusing to replace existing path: $target" >&2
    return 1
  fi

  if ! $apply; then
    echo "would link: $target -> $source"
    return
  fi

  if [[ "$backend" == posix ]]; then
    ln -s "$source" "$target"
  else
    command -v cygpath >/dev/null 2>&1 || {
      echo "ERROR: cygpath is required for the Windows link backend." >&2
      return 1
    }
    local source_win target_win command
    source_win=$(cygpath -aw "$source")
    target_win=$(cygpath -aw "$target")
    if [[ "$kind" == directory ]]; then
      command="mklink /J \"$target_win\" \"$source_win\""
    else
      command="mklink \"$target_win\" \"$source_win\""
    fi
    MSYS2_ARG_CONV_EXCL='*' cmd.exe /d /s /c "$command" >/dev/null
  fi
  echo "linked: $target -> $source"
}

link_skill_root() {
  local source_root=$1 app_skills=$2
  [[ -d "$source_root" ]] || return

  local skill source target
  while IFS= read -r -d '' source; do
    [[ -f "$source/SKILL.md" ]] || continue
    skill=$(basename "$source")
    target="$app_skills/$skill"
    create_link directory "$source" "$target"
  done < <(find "$source_root" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
}

ensure_directory "$codex_home"
ensure_directory "$claude_home"
ensure_directory "$codex_home/skills"
ensure_directory "$claude_home/skills"

create_link file "$kernel" "$codex_home/AGENTS.md"
create_link file "$kernel" "$claude_home/CLAUDE.md"

link_skill_root "$workflow_skills" "$codex_home/skills"
link_skill_root "$workflow_skills" "$claude_home/skills"
link_skill_root "$personal_skills" "$codex_home/skills"
link_skill_root "$personal_skills" "$claude_home/skills"

if $apply; then
  echo "Workflow wiring complete. Run verify-workflow.sh next."
else
  echo "Dry run only. Re-run with --apply after inspecting this plan."
fi
