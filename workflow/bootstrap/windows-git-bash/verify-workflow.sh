#!/usr/bin/env bash
set -euo pipefail

agents_home="${AGENTS_HOME:-$HOME/.agents}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
claude_home="${CLAUDE_HOME:-$HOME/.claude}"

kernel="$agents_home/workflow/AGENTS.md"
workflow_skills="$agents_home/workflow/skills"
personal_skills="$agents_home/skills"
failures=0

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*" >&2; failures=$((failures + 1)); }

is_windows=false
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) is_windows=true ;;
esac

is_link() {
  local path=$1
  if [[ -L "$path" ]]; then
    return 0
  fi
  if $is_windows && command -v cygpath >/dev/null 2>&1; then
    local path_win
    path_win=$(cygpath -aw "$path")
    MSYS2_ARG_CONV_EXCL='*' cmd.exe /d /s /c "fsutil reparsepoint query \"$path_win\"" >/dev/null 2>&1
    return
  fi
  return 1
}

check_file_link() {
  local source=$1 target=$2
  if [[ ! -f "$target" ]]; then
    fail "missing file link: $target"
  elif ! is_link "$target"; then
    fail "path exists but is not a link: $target"
  elif ! cmp -s "$source" "$target"; then
    fail "linked file content differs: $target"
  else
    pass "$target"
  fi
}

check_skill_root() {
  local source_root=$1 app_skills=$2
  [[ -d "$source_root" ]] || return

  local source skill target
  while IFS= read -r -d '' source; do
    [[ -f "$source/SKILL.md" ]] || continue
    skill=$(basename "$source")
    target="$app_skills/$skill"
    if [[ ! -f "$target/SKILL.md" ]]; then
      fail "missing skill link: $target"
    elif ! is_link "$target"; then
      fail "skill path exists but is not a link: $target"
    elif ! cmp -s "$source/SKILL.md" "$target/SKILL.md"; then
      fail "skill content differs: $target"
    else
      pass "$target"
    fi
  done < <(find "$source_root" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
}

[[ -f "$kernel" ]] || {
  echo "ERROR: kernel not found at $kernel" >&2
  exit 1
}

check_file_link "$kernel" "$codex_home/AGENTS.md"
check_file_link "$kernel" "$claude_home/CLAUDE.md"
check_skill_root "$workflow_skills" "$codex_home/skills"
check_skill_root "$workflow_skills" "$claude_home/skills"
check_skill_root "$personal_skills" "$codex_home/skills"
check_skill_root "$personal_skills" "$claude_home/skills"

if (( failures > 0 )); then
  echo "Workflow verification failed: $failures problem(s)." >&2
  exit 1
fi

echo "Workflow filesystem verification passed. Restart both apps and run the discovery smoke test."
