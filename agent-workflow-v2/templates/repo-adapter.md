# Repository Adapter Template

Keep this adapter short. It contains project facts the portable kernel cannot
know; it does not copy workflow policy.

## Project identity and sources of truth

- Project purpose and repository root
- Primary contributor/startup document
- Architecture or code-owner map
- Current-status and roadmap owners, when they exist

## Layout and conventions

- Workspaces, services, and generated surfaces
- Integration branch and branch/PR conventions
- Durable plan location and visibility (`private/excluded`, `tracked`, or none)
- Tracker and issue conventions, when applicable

## Verification routes

- Smallest focused commands by changed surface
- Cross-project or composite gate and its selection rule
- Local service, database, browser, hardware, or manual prerequisites
- Live, paid, destructive, or prepared-environment checks requiring approval

## Sensitive boundaries and known pitfalls

- Security, privacy, data, provider, migration, or release constraints
- Non-obvious ownership or ordering rules demonstrated by the repository
- Existing owners that task-specific implementations must reuse

## Local execution facts

- Checkout/worktree constraints specific to this repository
- Repository-specific access or tooling needed for verification

User host/model/reviewer preferences belong in the V2 host adapter, not here.
State unavailable repository capabilities plainly. This adapter may require
stricter behavior but cannot widen the V2 kernel's authority or review rules.
