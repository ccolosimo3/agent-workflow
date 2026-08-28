# Agent Workflow V2

Agent Workflow V2 is a portable, risk-proportionate coding workflow for Codex,
Claude, Cursor, and OpenCode. It keeps one shared set of planning, testing, and
review authorities while letting each user choose their hosts, models, and outer
review policy.

The package is installed once at a stable user-level path and exposed through
each host's skill or command discovery. Users may keep it on-demand or add one
persistent kernel route for always-on use. Repository adapters keep project
facts separate from the portable workflow.

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
- `skills/` — natural-language workflow entrypoints, internal review controls,
  compact advisory guidance, and focused explanation utilities;
- `templates/` — user host and repository adapters plus PR-body shape;
- `docs/SETUP.md` — installation, host configuration, and uninstall guidance.
- `THIRD_PARTY_NOTICES.md` — attribution for adapted third-party guidance.

Skills resolve shared files relative to this package. Keep one canonical local
checkout and expose its skills through links or configured discovery paths rather
than maintaining copied folders.

Clear ordinary language can select the matching user-facing workflow entrypoint,
while setup and review-control skills remain explicit/internal. The
`typescript-engineering`, `technical-writing`, `blast-radius`, `how`, `why`, and
`show-me` may be selected automatically when their narrow descriptions match.
`bro` remains an explicit operator utility. Skill discovery cannot manufacture
operator intent, expand scope, chain phases, grant authority, or claim
fresh-context independence.

## Start

1. Put this package at one stable path; the default is
   `~/.agents/workflow`.
2. Ask an existing agent to read `skills/setup-workflow/SKILL.md` by path and run
   its read-only capability and collision audit.
3. Choose `on-demand` to trial skill-triggered V2 without a persistent kernel or
   `always-on` for a daily driver, then choose enabled hosts, model/reasoning
   profiles, workload preferences, and outer-review behavior.
4. Review and approve setup's exact activation, discovery, adapter, and
   replacement preview.
5. Let setup verify automatic advisory and user-facing discovery, explicit-only
   control-plane entrypoints, and shared references without a model call, plus
   the persistent kernel only in always-on mode; then add a short repository
   adapter from `templates/repo-adapter.md` if wanted.
6. Open a fresh session and request the wanted work naturally or invoke its
   entrypoint explicitly.

See [setup and uninstall](docs/SETUP.md) for host-specific details.

An approved replacement cutover points host discovery only to the canonical
installation. Superseded workflow registrations do not remain active after the
operator validates and finalizes cutover.

Switching modes changes only V2-owned persistent kernel routes and the matching
activation/kernel records in `HOST.local.md`. The package, explicit entrypoints,
other preferences, and repository setup remain in place.
