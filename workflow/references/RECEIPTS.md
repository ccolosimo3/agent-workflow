# Agent Workflow V2 Completion Receipts

This file owns the optional durable receipt contract. Receipts are private
evidence metadata, not certification, acceptance, review state, or workflow
authority. Missing, stale, malformed, or unwritable receipt data never blocks
completion, invalidates product evidence, or triggers replay or repair.

## When to write

Read this file only when `HOST.local.md` names an enabled `Completion receipt
store` and `KERNEL.md`'s completion trigger applies. Write one receipt when a
terminal implementation or explicitly selected evidence-producing Explore,
Spike, or prototype produced code, a durable artifact, or decision-relevant
learning. Specs already own their artifact; planners, reviewers, evidence
helpers, casual questions, and status exchanges write nothing.

Reuse evidence already gathered for completion. Do not rerun commands, inspect
usage, or collect more context for the receipt. If the store is disabled, unsafe,
missing, or unwritable, report `Receipt: skipped — <reason>` once and continue.
Never fall back to a product repository or plan directory.

## Storage

Setup records a canonical absolute user-local data root outside workflow and
product repositories after previewing its containment, private permissions, and
host access. Under that root, create without overwriting:

```text
<store>/<YYYY-MM>/<receipt-id>/self-report.json
<store>/<YYYY-MM>/<receipt-id>/annotations/<annotation-id>.json
```

The bucket comes only from the self-report's UTC month. Later annotations remain
under that bucket. IDs are lowercase canonical UUIDv4 values; repository and
task text never becomes a path segment. Validate complete JSON before publishing
the final no-clobber file. On collision, generate a new ID. Ignore or remove only
a task-owned partial temporary file; never overwrite or repair an existing
record.

## Self-report

`self-report.json` contains only the owning agent's claims. `completed` means the
agent reports reaching its selected task outcome; it does not mean accepted,
correct, merged, or production-proven.

| Field | Type and rule |
| --- | --- |
| `schema` | required literal `agent-workflow.receipt/v1` |
| `receipt_id` | required lowercase canonical UUIDv4 string matching the directory |
| `recorded_at` | required RFC 3339 UTC `YYYY-MM-DDTHH:MM:SSZ` string |
| `repository` | required stable display identity; strip credentials, query, fragment, and personal path |
| `task` | required object with non-empty string `id`, `title`, and `intent`; `shape` is `implementation`, `exploration`, `prototype`, or `spike` |
| `agent_state` | required `completed`, `partial`, `blocked`, or `abandoned` |
| `result` | required concise non-empty changed-or-learned outcome |
| `evidence` | required array of 1–12 evidence objects defined below |
| `uncertainty` | required array of 0–8 concise strings |
| `revision` | optional object with known safe string `branch`, `base`, and/or `tip` |
| `snags` | optional array of 0–8 snag objects defined below |
| `next_decision` | optional concise string |
| `discarded` | optional array of 0–8 concise strings |
| `telemetry` | optional cheaply exposed values defined below |

An evidence object has `kind` = `command`, `observation`, `artifact`, or
`source`; non-empty string `ref` and `result`; `quality` = `direct`, `proxy`,
`inference`, or `unverified`; and an optional safe string `revision`. A command
reference is a redacted command shape plus useful result, never raw output or
secret-bearing arguments.

Evidence quality means:

- `direct`: observed at the owning behavior boundary or in an authoritative
  current source;
- `proxy`: indirect support that does not exercise the owning boundary;
- `inference`: a conclusion derived from named direct or proxy evidence;
- `unverified`: an unresolved claim with no confirming evidence.

A `completed` report requires at least one `direct`, `proxy`, or `inference`
item; wholly `unverified` evidence cannot support that state.

A snag object has non-empty string `summary` and `recovery`, plus attribution:

- `product`: changed product behavior;
- `repository_guidance`: a repository-owned rule or route;
- `environment_bootstrap`: local setup or readiness;
- `workflow`: portable V2 policy;
- `host_tool`: agent host or tool transport;
- `model`: model execution;
- `task_shape`: ask or spec boundary;
- `operator_choice`: explicit operator direction;
- `unknown`: evidence cannot distinguish the cause.

`telemetry` may contain safe string `host` and `model`, nonnegative number
`elapsed_seconds`, and nonnegative integers `tokens`, `helpers`, and `revisions`.
Include only values the host already exposes cheaply; never estimate them or
translate subscription usage into money.

The UTF-8 self-report is at most 16 KiB. Omit unknown optional fields instead of
adding empty boilerplate.

For exploratory work, use `task.intent` for the question or hypothesis, `result`
for the artifact or learning, evidence quality for its strength, `discarded` for
an approach rejected by evidence, and `uncertainty` or `next_decision` for what
remains. Do not manufacture a binary test result.

## Sourced annotations

Never copy a reviewer or CI verdict, operator correction, post-merge defect,
independent acceptance, or externally decided abandonment into the self-report,
even when already known at receipt creation. Record only material
interpretation-changing outcomes as separate immutable annotation files, one
consolidated annotation per source/session rather than one per finding.

| Field | Type and rule |
| --- | --- |
| `schema` | required literal `agent-workflow.annotation/v1` |
| `annotation_id` | required lowercase canonical UUIDv4 matching the filename |
| `receipt_id` | required UUIDv4 matching the containing receipt |
| `recorded_at` | required RFC 3339 UTC `YYYY-MM-DDTHH:MM:SSZ` string |
| `source` | required object: `kind` = `reviewer`, `operator`, `ci`, `tracker`, `agent_followup`, or `evaluation`; non-empty safe string `ref` |
| `kind` | required `review_outcome`, `correction`, `acceptance`, `abandonment`, `defect`, or `reclassification` |
| `summary` | required concise non-empty string |
| `evidence` | optional concise safe string |
| `corrects` | required only for `correction`; literal `self_report` or an existing different annotation UUID in this receipt |

`review_outcome` summarizes one certifying review session. `correction` refutes
or changes the named self-report or annotation claim. `acceptance` and
`abandonment` record those independent owner decisions. `defect` records a later
observed failure. `reclassification` changes how an outcome is categorized
without rewriting its facts.

Each annotation is at most 4 KiB and follows the same privacy rules as the
self-report. A correction creates a new file and never edits its target. No
annotation is required for a valid receipt; no annotation means unadjudicated,
not accepted.

## Privacy and completion output

Store no raw reasoning, transcript, full log or diff, credential, secret,
environment value, raw payload, credential-bearing remote, or personal absolute
checkout path. Apply the same redaction to annotation text and references. If a
safe reference cannot be recorded, omit it or skip the receipt.

Keep the normal chat completion. Add only:

```text
Receipt: <self-report path | disabled | skipped — reason>
```
