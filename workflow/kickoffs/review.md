# Review Kickoff

```text
Review work item <id/link> / PR <id/link> / branch <branch> against <base>.

Read and apply `~/.agents/workflow/REVIEW_RUBRIC.md` IN FULL. Its investigation,
test-quality, severity, and Output contracts are authoritative. The Context below
is the implementer's claim; the diff and repository are the source of truth.

Context:

1. Work item
   - issue/spec: <url or path>
   - range: `<base sha>..<tip sha>`; derive the authoritative file list and diff
     with `git diff --stat` and `git diff` for this range
   - acceptance criteria:
     - [ ] <AC bullet>

2. Implementer summary
   <2-3 sentences: what changed and why>

2a. Original operator request / intent
   <verbatim or close paraphrase; compare scope against this, not only the ACs>

3. Scope
   - in scope: <1-2 sentences; reviewer derives file paths from the diff>
   - intentionally out of scope: <items + reason, or none>
   - discovered follow-ups: <items, or none>

4. Evidence
   - verification run: `<command>` — <exact useful result>
   - reused evidence: <evidence point + causal reason, or none>
   - not selected or blocked: <gate + reason, or none>
   - remaining Tier 4: <check + owner, or none>

5. Conditional impact
   - docs: <owning doc updated, or none>
   - visual/UI: <profile + rendered evidence + residual checks, or not applicable>

6. Tests
   - <assertions unchanged, or grouped behaviors/failure modes and real boundaries>
   - non-ship/pocketed candidates: <list + reason, or none>

7. Risks and deviations
   - <hot spots, assumptions, spec deviations, or none>

8. Repo conventions to enforce
   <resolve from the filesystem per HANDOFF.md step 3>
```
