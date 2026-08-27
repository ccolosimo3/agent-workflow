# Agent Workflow V2

Agent Workflow V2 is a portable, risk-proportionate coding workflow for Codex,
Claude, Cursor, and OpenCode. It keeps one shared set of planning, testing, and
review authorities while letting each user choose their hosts, models, and outer
review policy.

V2 is currently an inactive beta. Testing this checkout does not modify an active
workflow or repository until the operator approves those actions. Its versioned
directory is temporary collision protection, not the final installation shape.

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

1. During beta, keep this package in one stable isolated path and do not register
   its release skill names in an active host profile.
2. Ask an existing agent to read `skills/setup-workflow/SKILL.md` by path and run
   its read-only capability and collision audit.
3. Choose enabled hosts, model/reasoning profiles, workload preferences, and
   outer-review behavior.
4. Test discovery only in a clean isolated host home/profile with no matching
   skill IDs; otherwise invoke beta instructions by their package paths.
5. Let setup verify the persistent kernel, explicit phase discovery, and shared
   references without a model call, then add a short repository adapter from
   `templates/repo-adapter.md` if wanted.
6. Open a new isolated session and invoke the selected skill explicitly.

See [setup and uninstall](docs/SETUP.md) for host-specific details.

At release, the package is promoted to `~/.agents/workflow` and host discovery
points only to that canonical installation. V1 and the beta-only package do not
remain installed after the operator validates and finalizes cutover.
