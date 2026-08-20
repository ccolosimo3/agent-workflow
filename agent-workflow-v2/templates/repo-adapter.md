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
- Durable plan location, when formal plans are used
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

## Host capabilities

- Fresh task/context creation and resumption
- Checkout/worktree isolation
- Independent reviewer availability
- Web research and tracker access
- Model/provider selection, if operator-controlled

State unavailable capabilities plainly. The adapter may require stricter behavior
but cannot widen the V2 kernel's authority or review requirements.
