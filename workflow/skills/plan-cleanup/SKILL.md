---
name: plan-cleanup
description: >-
  Preview and safely externalize completed local plan folders to the private
  archive with scoped approval and integrity verification. Use for
  /plan-cleanup, periodic archive cleanup, or moving completed plans off-device.
  Not for ordinary cleanup immediately after one item lands.
---

# Plan Cleanup

Externalize terminal work-item folders without making archived history visible
to ordinary project searches. Keep the archive repository out of project roots
and use the bundled script for every copy, manifest, verification, and prune.

## Audit

1. Read `~/.agents/workflow/PLANS.md`, the selected repo's instructions, and its
   local plans README. Inspect both the project and planning-repo git status;
   preserve all unowned changes.
2. Locate the project's `plans/archive/` and derive a stable project slug. Do
   not scan `active/`, `backlog/`, or `reference/` as cleanup candidates.
3. Confirm the configured GitHub archive repository is `PRIVATE` and record its
   default branch with a read-only `gh repo view` query. Block on any other
   visibility; do not create or change repository settings from this skill.
4. Run the read-only audit, normally with the 30-day default:

   ```bash
   python3 ~/.agents/workflow/skills/plan-cleanup/scripts/plan_archive.py audit \
     --plans-root <absolute-plans-path> \
     --project <project-slug> \
     --older-than-days 30
   ```

5. Report eligible items, held items, blockers, sizes, and the exact proposed
   destination. A terminal status is `implemented`, `closed`, or `deferred`;
   age comes from `landed:` and falls back to `updated:`. Missing or ambiguous
   metadata stays held. Never select a folder solely because it is old.

The audit is safe for a periodic reminder or scheduled read-only check. Do not
schedule `sync`, pushes, or local pruning.

## Approve the batch

Before mutation, show the operator:

- source planning root and exact work-item folders;
- archive repository, branch, and `projects/<project>/` destination;
- whether local pruning is included;
- all preflight warnings or blockers; and
- the exact `sync` command.

Require explicit current-session approval. One approval may cover the shown
fast-forward push, recovery verification, and exact local prune. Re-ask if the
repo, items, destination, or prune scope changes. Never silently redact, skip,
or broaden the batch.

## Sync and verify

After approval, run:

```bash
python3 ~/.agents/workflow/skills/plan-cleanup/scripts/plan_archive.py sync \
  --plans-root <absolute-plans-path> \
  --project <project-slug> \
  --remote https://github.com/ccolosimo3/agent-plan-archive.git \
  --item <work-item> [--item <work-item> ...] \
  --prune
```

Omit `--prune` when the operator approved upload only. The script must complete
all of these before it removes any source folder:

1. reject non-terminal/ineligible items, unsafe paths, symlinks, oversized
   files, and likely credentials;
2. clone the private archive into a temporary directory;
3. copy normal files to `projects/<project>/<work-item>/` and write a compact
   SHA-256 manifest;
4. commit and push fast-forward to the cloned default branch;
5. confirm the remote branch points at that commit;
6. make a second fresh clone and compare every source path, byte count, and
   hash; and
7. only then prune the exact approved local folders.

Any failure before step 7 leaves local sources untouched. An identical item
already present remotely is idempotent; a same-path byte mismatch is a hard
conflict, never an overwrite.

## Record and restore

After success, update the project's small archive pointer or index with the
archive repository, commit, and subtree. Do not paste the archived inventory
back into the live index. Do not commit or push the source planning repository
unless separately requested.

Restore by cloning the archive into a disposable directory and inspecting or
copying only the requested subtree. Do not restore directly into `active/` or
make historical material current without explicit operator direction.

## Boundaries

- Keep one archive repo per ownership/confidentiality boundary.
- Store plans as ordinary files. Do not create recurring ZIP snapshots or use
  Git LFS for normal planning material.
- Treat private GitHub as an off-device operational archive, not encrypted or
  independent disaster recovery.
- Do not upload raw data, credentials, private keys, or ambiguous artifacts.
- Do not auto-externalize `reference/`; it remains durable live context unless
  the operator selects a separate, reviewed cleanup.
