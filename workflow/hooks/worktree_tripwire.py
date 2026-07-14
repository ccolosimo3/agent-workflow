#!/usr/bin/env python3
"""Codex PreToolUse tripwire for destructive paths outside a Git worktree.

This is deliberately a narrow guardrail, not a shell sandbox. It allows ordinary
commands immediately and blocks recognizable destructive commands when their
mutation target cannot be proven to remain inside the current Git worktree.
"""

from __future__ import annotations

import glob
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


CONTROL_TOKENS = {";", "&&", "||", "|", "&", "(", ")"}
PRIVILEGED_COMMANDS = {"sudo", "doas", "diskutil"}
PATH_DESTRUCTIVE_COMMANDS = {"rm", "rmdir", "unlink", "shred", "mv"}
SHELL_COMMANDS = {"bash", "sh", "zsh", "dash", "ksh"}
SIMPLE_WRAPPERS = {"command", "builtin", "exec", "nohup", "time"}
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
DESTRUCTIVE_HINT_RE = re.compile(
    r"(^|[;&|()\s/])(sudo|doas|diskutil|mkfs(?:\.[A-Za-z0-9_-]+)?|"
    r"rm|rmdir|unlink|shred|mv|rsync|find)(?=$|[;&|()\s])"
)
VARIABLE_RE = re.compile(r"\$(?:([A-Za-z_][A-Za-z0-9_]*)|\{([^}]+)\})")


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str = ""


def _deny(reason: str) -> Decision:
    return Decision(False, reason)


def _git_root(cwd: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    root = result.stdout.strip()
    return Path(root).resolve(strict=False) if root else None


def _tokenize(command: str) -> list[str]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def _segments(tokens: Sequence[str]) -> Iterable[list[str]]:
    current: list[str] = []
    for token in tokens:
        if token in CONTROL_TOKENS:
            if current:
                yield current
                current = []
            continue
        current.append(token)
    if current:
        yield current


def _expand_variables(value: str, environment: Mapping[str, str]) -> str | None:
    unresolved = False

    def replace(match: re.Match[str]) -> str:
        nonlocal unresolved
        name = match.group(1) or match.group(2) or ""
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) or name not in environment:
            unresolved = True
            return match.group(0)
        return environment[name]

    expanded = VARIABLE_RE.sub(replace, value)
    if unresolved or "$" in expanded or "`" in expanded or "$(" in expanded:
        return None
    if any(character in expanded for character in ("{", "}")):
        return None
    expanded = os.path.expanduser(expanded)
    if expanded.startswith("~"):
        return None
    return expanded


def _resolved_targets(
    raw_target: str, cwd: Path, environment: Mapping[str, str]
) -> list[Path] | None:
    if not raw_target or "\x00" in raw_target:
        return None
    expanded = _expand_variables(raw_target, environment)
    if expanded is None:
        return None
    candidate = Path(expanded)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    candidate_text = str(candidate)
    if glob.has_magic(candidate_text):
        matches = glob.glob(candidate_text, recursive=True, include_hidden=True)
        if len(matches) > 10_000:
            return None
        if matches:
            return [Path(match).resolve(strict=False) for match in matches]
    return [candidate.resolve(strict=False)]


def _inside(root: Path, target: Path) -> bool:
    try:
        return os.path.commonpath((str(root), str(target))) == str(root)
    except ValueError:
        return False


def _check_targets(
    command_name: str,
    targets: Sequence[str],
    cwd: Path,
    root: Path | None,
    environment: Mapping[str, str],
) -> Decision:
    if not targets:
        return _deny(f"{command_name} has no resolvable mutation target")
    if root is None:
        return _deny(
            f"{command_name} is destructive and the current directory is not in a Git worktree"
        )
    for raw_target in targets:
        resolved = _resolved_targets(raw_target, cwd, environment)
        if resolved is None:
            return _deny(
                f"{command_name} target cannot be resolved safely: {raw_target!r}"
            )
        for target in resolved:
            if not _inside(root, target):
                return _deny(
                    f"{command_name} resolves outside the active worktree: {target} "
                    f"(worktree: {root})"
                )
    return Decision(True)


def _leading_environment(
    tokens: Sequence[str], base: Mapping[str, str]
) -> tuple[int, dict[str, str]]:
    environment = dict(base)
    index = 0
    while index < len(tokens) and ASSIGNMENT_RE.match(tokens[index]):
        name, value = tokens[index].split("=", 1)
        expanded = _expand_variables(value, environment)
        environment[name] = expanded if expanded is not None else value
        index += 1
    return index, environment


def _operands(tokens: Sequence[str], option_paths: Sequence[str] = ()) -> list[str]:
    operands: list[str] = []
    after_options = False
    for token in tokens:
        if after_options:
            operands.append(token)
        elif token == "--":
            after_options = True
        elif token.startswith("--") and "=" in token:
            option, value = token.split("=", 1)
            if option in option_paths:
                operands.append(value)
        elif token.startswith("-") and token != "-":
            continue
        else:
            operands.append(token)
    return operands


def _find_roots(arguments: Sequence[str]) -> list[str]:
    roots: list[str] = []
    index = 0
    while index < len(arguments):
        token = arguments[index]
        if token in {"-H", "-L", "-P"}:
            index += 1
            continue
        if token == "-D":
            index += 2
            continue
        if token == "--":
            index += 1
            break
        break
    while index < len(arguments):
        token = arguments[index]
        if token.startswith("-") or token in {"!", "(", ")", ","}:
            break
        roots.append(token)
        index += 1
    return roots or ["."]


def _unwrap_env(
    tokens: Sequence[str], base: Mapping[str, str]
) -> tuple[list[str], dict[str, str]]:
    environment = dict(base)
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            index += 1
            break
        if token.startswith("-"):
            index += 1
            continue
        if ASSIGNMENT_RE.match(token):
            name, value = token.split("=", 1)
            expanded = _expand_variables(value, environment)
            environment[name] = expanded if expanded is not None else value
            index += 1
            continue
        break
    return list(tokens[index:]), environment


def _unwrap_simple_wrapper(tokens: Sequence[str]) -> list[str]:
    index = 1
    while index < len(tokens):
        if tokens[index] == "--":
            index += 1
            break
        if not tokens[index].startswith("-") or tokens[index] == "-":
            break
        index += 1
    return list(tokens[index:])


def _directory_change(
    tokens: Sequence[str], cwd: Path, environment: Mapping[str, str]
) -> Path | None:
    start, local_environment = _leading_environment(tokens, environment)
    tokens = tokens[start:]
    if not tokens or Path(tokens[0]).name not in {"cd", "pushd"}:
        return cwd
    arguments = _operands(tokens[1:])
    raw_target = arguments[0] if arguments else local_environment.get("HOME")
    if not raw_target or raw_target == "-":
        return None
    targets = _resolved_targets(raw_target, cwd, local_environment)
    return targets[0] if targets is not None and len(targets) == 1 else None


def _inspect_simple_command(
    tokens: Sequence[str], cwd: Path, root: Path | None, base_environment: Mapping[str, str]
) -> Decision:
    start, environment = _leading_environment(tokens, base_environment)
    tokens = tokens[start:]
    if not tokens:
        return Decision(True)

    command_name = Path(tokens[0]).name
    arguments = list(tokens[1:])

    if command_name == "command" and any(
        argument in {"-v", "-V"} for argument in arguments
    ):
        return Decision(True)
    if command_name in SIMPLE_WRAPPERS and arguments:
        nested = _unwrap_simple_wrapper(tokens)
        return _inspect_simple_command(nested, cwd, root, environment) if nested else Decision(True)
    if command_name == "env":
        nested, nested_environment = _unwrap_env(tokens, environment)
        return (
            _inspect_simple_command(nested, cwd, root, nested_environment)
            if nested
            else Decision(True)
        )
    if command_name == "xargs":
        for index, token in enumerate(arguments):
            nested_name = Path(token).name
            if (
                nested_name in PATH_DESTRUCTIVE_COMMANDS
                or nested_name in PRIVILEGED_COMMANDS
                or nested_name in SHELL_COMMANDS
                or nested_name in SIMPLE_WRAPPERS
            ):
                return _inspect_simple_command(arguments[index:], cwd, root, environment)
        return Decision(True)

    if command_name in SHELL_COMMANDS:
        command_option = next(
            (
                index
                for index, argument in enumerate(arguments)
                if argument == "-c"
                or (
                    argument.startswith("-")
                    and not argument.startswith("--")
                    and "c" in argument[1:]
                )
            ),
            None,
        )
        if command_option is None:
            return Decision(True)
        command_index = command_option + 1
        if command_index >= len(arguments):
            return _deny(f"{command_name} -c is missing its command string")
        return inspect_command(arguments[command_index], cwd, root, environment)

    if (
        command_name in PRIVILEGED_COMMANDS
        or command_name == "mkfs"
        or command_name.startswith("mkfs.")
    ):
        return _deny(
            f"privileged or system-destructive command is not allowed: {command_name}"
        )

    if command_name in PATH_DESTRUCTIVE_COMMANDS:
        option_paths = ("--target-directory",) if command_name == "mv" else ()
        targets = _operands(arguments, option_paths)
        return _check_targets(command_name, targets, cwd, root, environment)

    if command_name == "find":
        for marker in ("-exec", "-execdir"):
            if marker in arguments:
                tail = arguments[arguments.index(marker) + 1 :]
                nested = [token for token in tail if token not in {"+", ";"}]
                nested_decision = _inspect_simple_command(
                    nested, cwd, root, environment
                )
                if not nested_decision.allowed:
                    return nested_decision
        if "-delete" in arguments:
            return _check_targets(
                "find", _find_roots(arguments), cwd, root, environment
            )
        return Decision(True)

    if command_name == "rsync":
        dry_run = any(
            argument == "--dry-run"
            or (
                argument.startswith("-")
                and not argument.startswith("--")
                and "n" in argument[1:]
            )
            for argument in arguments
        )
        if dry_run:
            return Decision(True)
        deletes_destination = any(
            argument == "--delete" or argument.startswith("--delete-")
            for argument in arguments
        )
        removes_sources = "--remove-source-files" in arguments
        if deletes_destination or removes_sources:
            operands = _operands(arguments)
            targets = operands if removes_sources else operands[-1:]
            if any(
                ":" in target and not target.startswith(("./", "../", "/"))
                for target in targets
            ):
                return _deny("rsync destructive target is remote or ambiguous")
            return _check_targets("rsync", targets, cwd, root, environment)

    return Decision(True)


def inspect_command(
    command: str,
    cwd: Path,
    root: Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> Decision:
    environment = dict(os.environ if environment is None else environment)
    if root is None:
        root = _git_root(cwd)
    try:
        tokens = _tokenize(command)
    except ValueError as error:
        if DESTRUCTIVE_HINT_RE.search(command):
            return _deny(f"destructive-looking command could not be parsed safely: {error}")
        return Decision(True)
    effective_cwd: Path | None = cwd
    directory_stack: list[Path] = []
    for segment in _segments(tokens):
        start, _ = _leading_environment(segment, environment)
        command_name = Path(segment[start]).name if start < len(segment) else ""
        if command_name in {"cd", "pushd"}:
            if effective_cwd is None:
                continue
            changed_cwd = _directory_change(segment, effective_cwd, environment)
            if command_name == "pushd" and changed_cwd is not None:
                directory_stack.append(effective_cwd)
            effective_cwd = changed_cwd
            continue
        if command_name == "popd":
            effective_cwd = directory_stack.pop() if directory_stack else None
            continue
        if effective_cwd is None and DESTRUCTIVE_HINT_RE.search(" ".join(segment)):
            return _deny("destructive target follows an unresolved directory change")
        decision = _inspect_simple_command(
            segment, effective_cwd or cwd, root, environment
        )
        if not decision.allowed:
            return decision
    return Decision(True)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload["tool_input"]["command"]
        cwd = Path(payload["cwd"]).expanduser().resolve(strict=False)
        if not isinstance(command, str) or not command.strip():
            raise ValueError("tool_input.command must be a non-empty string")
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Blocked: invalid PreToolUse payload: {error}", file=sys.stderr)
        return 2

    decision = inspect_command(command, cwd)
    if decision.allowed:
        return 0
    print(
        "Blocked by worktree tripwire: "
        f"{decision.reason}. Out-of-worktree destructive operations must be "
        "performed directly by the operator.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
