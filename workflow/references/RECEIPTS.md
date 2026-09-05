# Agent Workflow V2 Completion Receipts

This file owns the optional durable receipt contract. Receipts are private
evidence metadata, not certification, acceptance, review state, or workflow
authority. Missing, stale, malformed, or unwritable receipt data never blocks
completion, invalidates product evidence, or triggers replay or repair.

## When to write

Read this file only when `HOST.local.md` names an enabled `Completion receipt
store` and either `KERNEL.md`'s self-report trigger applies or the current task
explicitly asks to append a material sourced annotation to an existing receipt.
Write one self-report when a terminal implementation or explicitly selected
evidence-producing Explore, Spike, or prototype produced code, a durable
artifact, or decision-relevant learning. An annotation-only follow-up writes no
self-report. Otherwise specs, planners, reviewers, evidence helpers, casual
questions, and status exchanges write nothing.

Reuse evidence already gathered for completion or supplied by the named
annotation source. Do not rerun commands, inspect usage, or collect more context
for the receipt. If the store is disabled, unsafe, missing, or unwritable, report
`Receipt: skipped — <reason>` once and continue. Never fall back to a product
repository or plan directory.

## Storage

Setup records a canonical absolute user-local data root outside workflow and
product repositories after previewing its containment, private permissions, and
host access. Under that root, create without overwriting:

```text
<store>/<YYYY-MM>/<receipt-id>/self-report.json
<store>/<YYYY-MM>/<receipt-id>/annotations/<annotation-id>.json
```

See `../examples/receipts/` for the localized implementation, exploratory
prototype, and sourced-annotation fixtures.

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
| `execution` | required for new self-reports: non-empty ordered array of author execution entries defined below |
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

### Execution identity and optional measurements

For each new self-report, record the actual author's host, exact model ID, and
reasoning effort separately in `execution`. Each entry contains these non-empty
safe strings:

| Field | Value |
| --- | --- |
| `host` | Host identifier, such as `codex`, `claude`, or `cursor`; `unknown` if unavailable |
| `model` | Exact model ID exposed for that run; `unknown` if unavailable |
| `reasoning_effort` | Host-native effort or variant, such as `medium` or `xhigh`; `not_applicable` only when the host exposes no such setting, otherwise `unknown` if unavailable |
| `source` | Concise reference to already available runtime metadata or the explicit launch configuration; `unknown` if neither is available |

Prefer runtime-reported values over requested launch values. When only launch
configuration is available, identify it as such in `source`; it is not proof of
the served model. Never infer an actual setting from a current default, profile
name, task difficulty, or another agent's settings. Keep reasoning effort out of
the model string, and never store reasoning content.

Use one entry when the author settings stayed the same. Preserve known changes
of author host, model, or effort in execution order, including corrections and
recovery; do not attribute the entire task to its final model. Represent a known
segment with unavailable settings using `unknown`. Do not reconstruct missing
history or inspect additional logs or usage solely to populate this field.
Reviewer execution belongs in that reviewer's sourced annotation, not the
author's self-report. Helper execution is outside this field's scope.

`telemetry` may contain nonnegative number `elapsed_seconds` and nonnegative
integers `tokens`, `helpers`, and `revisions`. Include only values the host already
exposes cheaply; never estimate them or translate subscription usage into money.
For tasks with multiple execution entries, available telemetry describes only
the task scope its source establishes; do not assign totals to the final entry
or claim full-task totals from a partial run.

This is an additive v1 writing rule. Existing receipts and annotations remain
valid and immutable without `execution`; their missing settings are unknown.
Legacy `telemetry.host` and `telemetry.model` remain readable historical fields;
new records use `execution` for identity. Do not guess, backfill, or rewrite old
records. Missing metadata never changes the receipt's non-blocking status.

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
| `execution` | required for new annotations with `source.kind` = `reviewer`: the source reviewer's execution entries using the same rules above; omit for other sources |

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
