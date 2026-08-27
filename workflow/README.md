# Agent Workflow V2

Agent Workflow V2 is a portable, risk-proportionate coding workflow for Codex,
Claude, Cursor, and OpenCode. It keeps one shared set of planning, testing, and
review authorities while letting each user choose their hosts, models, and outer
review policy.

The package is installed once at a stable user-level path and exposed through
each host's native kernel and skill or command discovery. Repository adapters
keep project facts separate from the portable workflow.

## Workflow

```text
plan -> explore/spike when needed -> spec -> spec review
     -> implementation -> implementation review -> complete
```

Inner review is part of formal spec and implementation completion. Outer spec
and implementation reviews are configurable as risk-selected,
operator-invoked, or disabled. Coworker PR review uses `review-pr` and the same
canonical review authority with human-facing calibration.

## Package

- `references/` — portable kernel, workflow, planning, testing, and review
  authorities;
- `skills/` — thin phase entrypoints;
- `templates/` — user host and repository adapters plus PR-body shape;
- `docs/SETUP.md` — installation, host configuration, and uninstall guidance.

Skills resolve shared files relative to this package. Keep one canonical local
checkout and expose its skills through links or configured discovery paths rather
than maintaining copied folders.

## Start

1. Put this package at one stable path; the default is
   `~/.agents/workflow`.
2. Ask an existing agent to read `skills/setup-workflow/SKILL.md` by path and run
   its read-only capability and collision audit.
3. Choose enabled hosts, model/reasoning profiles, workload preferences, and
   outer-review behavior.
4. Review and approve setup's exact kernel, discovery, adapter, and replacement
   preview.
5. Let setup verify the persistent kernel, explicit phase discovery, and shared
   references without a model call, then add a short repository adapter from
   `templates/repo-adapter.md` if wanted.
6. Open a fresh session and invoke a phase only when that phase is wanted.

See [setup and uninstall](docs/SETUP.md) for host-specific details.

An approved replacement cutover points host discovery only to the canonical
installation. Superseded workflow registrations do not remain active after the
operator validates and finalizes cutover.
