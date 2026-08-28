# Agent Workflow V2

Agent Workflow V2 is a portable, risk-proportionate coding workflow for Codex,
Claude Code, Cursor, and OpenCode. The release package lives in
[`workflow/`](workflow/); the repository root also provides Cursor's local
marketplace manifest.

## Try it

1. Clone this repository to a stable user-level location.
2. Give an existing agent the path to
   [`workflow/skills/setup-workflow/SKILL.md`](workflow/skills/setup-workflow/SKILL.md)
   and ask it to run the read-only setup audit.
3. Choose **on-demand** to trial skill-triggered V2 without a persistent kernel,
   or **always-on** for a daily driver.
4. Review and approve the exact host registrations and configuration changes
   before setup writes them.
5. Open fresh host sessions and invoke the workflow phases you want to use.

The package keeps one canonical set of skills and workflow authorities while
leaving repository facts, model choices, and outer-review routing configurable.
Start with the [package overview](workflow/README.md), then use the
[setup and uninstall guide](workflow/docs/SETUP.md) for host-specific details.




https://github.com/user-attachments/assets/17d30f20-1bba-4534-b3e8-072a9b27b7de


