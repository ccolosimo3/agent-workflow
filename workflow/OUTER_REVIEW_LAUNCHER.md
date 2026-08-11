# Claude Outer-Review Launcher

On-demand launcher contract for Claude-backed `outerreview` and
`outerspecreview`. `HANDOFF.md` owns sequencing, gate selection, independence,
and re-review reuse; this file owns only CLI profiles, flags, launch, and resume.

## Shared contract

A canonical outer gate selected by `HANDOFF.md` or directly requested by the
operator is preauthorized for one Claude session and its same-session re-reviews;
do not request separate paid-call approval. This does not authorize extra or
duplicate reviews or paid provider/evaluation/live-probe calls from the reviewer.

Require Claude Code 2.1.219+ and map supported profiles exactly:

- **Opus 5 `high`** → `--model claude-opus-5 --effort high`
- **Opus 5 `xhigh`** → `--model claude-opus-5 --effort xhigh`
- **Fable 5 `high`** → `--model claude-fable-5 --effort high`

Do not silently remap an unsupported profile. Every scripted launch uses
`-p --output-format json --permission-mode auto`; the parent app's permission
mode does not carry into Claude Code. Terminate variadic options with `--` before
the prompt. Add `--add-dir <absolute folder>` only when the review must read a
local path outside the launch directory, and keep it last before `--`.

Wait without interrupting the process. From the single JSON result, retain
`session_id` and the complete final `result`; relay that verdict to the calling
session. Never add a permission-bypass flag. Missing CLI/auth/skill access,
auto-mode denial, or a permission failure is a blocker, not permission to weaken
the gate.

## Implementation outer gate

After inner approval, confirm a clean committed tip and current outer-review
receipt. Select by implementation complexity:

- **Opus 5 `high`** — ordinary bounded work with few interacting contracts;
- **Opus 5 `xhigh`** — substantive multi-file/risk-surface work or a substantive
  inner finding;
- **Fable 5 `high`** — exceptional large, hard-to-reverse, concurrency,
  migration, or security work with several interacting invariants.

Do not choose Fable merely because an outer gate is required. If it is
unavailable or blocks a benign review, disclose that and use Opus 5 `xhigh`.

From the implementation worktree:

```bash
claude -p --output-format json \
  --model <model> --effort <level> \
  --permission-mode auto \
  --add-dir <absolute-work-item-folder> \
  -- \
  "/outerreview Review <work item>. Worktree: <absolute root>. Spec: <absolute path or URL>. Verification receipt: <absolute path or in-prompt receipt>."
```

Use `--add-dir` when the spec or receipt is outside the worktree; otherwise omit
it. Pass no inner findings or verdicts on the first run.

If ACTIONABLE, patch only listed findings, commit, run targeted verification,
then resume from the same worktree and with the same profile/directory access:

```bash
claude -p --output-format json --resume <session_id> \
  --model <same model> --effort <same level> \
  --permission-mode auto \
  --add-dir <same absolute work-item folder> \
  -- \
  "Re-review the patched live tip. Recompute it and verify your prior findings."
```

Repeat until the same outer reviewer approves the final tip. If a patch hunk
cannot be mapped to its findings, report scope expansion; only the operator may
restart the inner → outer sequence. A Claude implementation uses a fresh
other-model outer-review task rather than recursively launching Claude.

## Spec outer gate

Default to Opus 5 `high`; honor explicit Fable 5 `high`, Opus 5 `high`, or Opus
5 `xhigh`. From the repository root after inner spec convergence:

```bash
claude -p --output-format json \
  --model <model> --effort <level> \
  --permission-mode auto \
  --add-dir <absolute spec folder only when outside the repo root> \
  -- \
  "/outerspecreview <absolute spec path> — inner spec-review loop converged"
```

Omit `--add-dir` when the spec is inside the repository root. Pass no prior
findings, verdicts, or populated kickoff. If ACTIONABLE, patch only mapped
findings in the planning session, then resume the same Claude session using the
shared flags/profile and:

```text
Re-review the revised spec. Verify your prior findings against the current artifact.
```

Do not invoke `specrereview` or start a fresh outer pass. A Claude planning
conversation performs `outerspecreview` directly instead of launching another
Claude process.
