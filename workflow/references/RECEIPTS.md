# Agent Workflow V2 Completion Receipts

Receipts are optional private learning records, not acceptance or certification.
When disabled or unconfigured, write nothing and add no receipt-status message.
When enabled in `HOST.local.md`, write only for `KERNEL.md`'s completion trigger
or an explicitly scoped later annotation. Specs, reviewers, helpers, casual
questions, and status checks do not create self-reports.

Use evidence already gathered. Never rerun proof, inspect usage/logs, or recover
history just to fill a receipt. Missing, malformed, or unwritable metadata never
blocks or replays work. Report `Receipt: skipped — <reason>` once if needed.

## Storage and privacy

Use the configured canonical private user-data root outside workflow and product
repositories; never fall back to a repository or plan directory. Create without
overwriting:

```text
<store>/<YYYY-MM>/<receipt-id>/self-report.json
<store>/<YYYY-MM>/<receipt-id>/annotations/<annotation-id>.json
```

Use lowercase canonical UUIDv4 IDs and the self-report's UTC month for both paths.
Validate JSON before publishing with no-clobber creation; regenerate a colliding
ID. Remove only task-owned partial files. Existing records are immutable,
including v1 records: read their recorded fields as historical data, never migrate,
backfill, or rewrite them. `../examples/receipts/` includes v1 history and a v2
writing example.

Store no credentials, environment values, personal absolute checkout paths,
raw payloads, reasoning, transcripts, full logs, or diffs. Redact references too;
if a required reference cannot be made safe, skip the record. Limit self-reports
to 16 KiB and annotations to 4 KiB. Do not create telemetry or evidence taxonomies.

## New self-reports: v2

All fields below are required unless marked optional. Use concise text.
`completed` reports the selected task outcome, not merge, acceptance, or production
proof. Attributed review outcomes remain the reviewers' claims.

| Field | Shape |
| --- | --- |
| `schema` | `agent-workflow.receipt/v2` |
| `receipt_id` | UUIDv4 matching the directory |
| `recorded_at` | UTC `YYYY-MM-DDTHH:MM:SSZ` |
| `repository` | `owner/name` when known, otherwise stable display name; no personal path |
| `task` | Object: non-empty `id`, `title`, `intent`; `shape`: `implementation`, `exploration`, `prototype`, or `spike` |
| `agent_state` | `completed`, `partial`, `blocked`, or `abandoned` |
| `result` | Short changed-or-learned outcome |
| `verification` | One string: what ran or was observed, boundary and result; `none` when none ran |
| `uncertainty` | List of remaining limits or questions; empty when none |
| `authors` | Non-empty ordered list of author profiles: `host`, `model`, `reasoning_effort` |
| `reviews` | List of completed review sessions, defined below; empty when none |
| `snags` | Optional list of objects: `summary`, `recovery`, and `attribution` (plain description or `unknown`) |
| `revision` | Optional object with known safe `branch`, `base`, and/or `tip` |
| `next_decision` | Optional short string |

Author and reviewer profile values mean **as launched**, not independently proved
runtime identity. Use `unknown` for unavailable values; never guess from defaults
or investigate to fill them. Preserve known author changes in order without
reconstructing missing history.

Each `reviews` entry contains `role` (`inner`, `outer`, or another named role),
`host`, `model`, `reasoning_effort`, a safe `source` session/reference,
`initial_verdict`, `final_verdict`, and `findings` (a material summary or `none`).
For a disclosed replacement, use a separate entry and identify recovery in
`source`; do not attribute another session's work to its replacement. Put reviews
completed before this receipt inline, without duplicate review annotations.
An unfinished review belongs in `uncertainty`, not a claimed final verdict.

## Later annotations

Append only material later outcomes—review, CI/PR-bot defect, operator correction,
acceptance, abandonment, or post-merge defect—when explicitly scoped. One record
per source/session suffices; do not write one per finding or edit the self-report.

New annotations use `schema: agent-workflow.annotation/v2`, UUIDv4 `annotation_id`
and `receipt_id`, UTC `recorded_at`, `source` (object with `kind` and safe `ref`),
`kind` (outcome type), and concise `summary`. Optional `evidence` is a short safe
reference. Corrections require `corrects: self_report` or the existing annotation
ID they correct. A review outcome includes a `review` object using the inline
review fields above. No annotation means no recorded later adjudication.

Keep the ordinary chat completion; add only `Receipt: <self-report path>` after
an applicable successful write, or the skipped-write message above.
