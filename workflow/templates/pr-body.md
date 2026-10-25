# V2 Pull Request Body

Write for a teammate who understands the product and repository but has not read
private plans. Lead with observable behavior and motivation. Keep technical names,
paths, and commands only when they improve precision. Omit workflow tiers, private
plan codes, review mechanics, local paths, agent jargon, and process history.

Use the repository's required closing reference first when one exists. Always
include `## Summary` and `## Verification`. Include optional sections only when
they carry information a reviewer needs; omit empty headings.

```text
<closing reference, when applicable>

## Summary
<one sentence: observable change and why>
- <concrete behavior or contract change>
- <concrete behavior or contract change>

## Root cause
<optional: why the defect or need existed>

## Impact
<optional: what now works or which risk is reduced>

## Scope boundary
- <optional adjacent behavior deliberately unchanged and why>

## Screenshots
<optional visual proof; layout and upload in "Visual proof" below>

## Verification
<affected local gate summary using only checks that actually passed>
- <focused behavior proof> — <result>
- <blocked, manual, visual, or operator check> — <status, when relevant>

## Docs impact
- <optional tracked owner path> — <what changed>

## Risks
<optional remaining risk>

## Follow-ups
- <optional operator-approved or already-filed follow-up with shared link>

## Notes
- <optional non-obvious migration, rollback, or reviewer-relevant tradeoff>
```

Use an outcome-first sentence-case title. Report only observed results that apply
to the candidate. Evidence from an earlier revision may be reused when no change
to relevant code, configuration, dependencies, or environment can invalidate it;
identify the tested revision and briefly explain why the evidence still applies.
Never imply a reused check was rerun. Keep exhaustive commands, findings, verdicts,
and rerun history in the existing evidence owner rather than the PR body. Omit
`## Docs impact` when tracked docs did not change.

## Visual proof

Add `## Screenshots` only when the change is visible and `FRONTEND.md` calls for
rendered proof. Capture synthetic or test data only, with no real personal data
or secrets, and never retouch a capture. Start the section with one line naming
the tested revision, the devices or browsers and their OS versions, and that the
data is synthetic. Then put the images in a collapsed block, three across, each
under a bold caption naming the claim it proves:

```html
<details>
<summary>N screenshots (click to expand)</summary>

<table>
<tr><td width="33%" valign="top"><b>Claim it proves</b> (platform)<br><img src="./01-claim-platform.jpg" width="260" alt="Short description"></td>…</tr>
</table>

</details>
```

At width 260 a phone screen stays readable without long scrolling, and GitHub
opens the full-size image on click. Name files `NN-claim-platform` in display
order. Don't put more than three images in a row.

Upload with GitHub CLI 2.99 or later; `KERNEL.md` approval applies to each edit:

1. Show the operator the final body, with local paths where the image URLs will
   go. That one approval covers both edits below, for the same PR, body and
   images; swapping in the uploaded URLs is mechanical.
2. Upload from the image folder: `gh pr edit <n> -R <owner>/<repo> --body-file
   <upload-body> --attach ./01-claim-platform.jpg …`. In the upload body, replace
   the HTML table with plain Markdown, one caption line and one
   `![alt](./01-claim-platform.jpg)` line per image, outside any HTML. gh
   rewrites only Markdown image references; ones inside raw HTML get appended
   instead.
3. Read the uploads back: `gh pr view <n> -R <owner>/<repo> --json body --jq
   .body`, since `gh pr edit` prints only the PR URL. Map each file to its
   `user-attachments` URL. A partial upload still updates the PR and exits
   nonzero, so stop if any image lacks a URL, and upload only the missing files.
4. Once every image has a URL, apply the approved table with a second
   `gh pr edit --body-file`, putting the URLs in place of the local paths. Check
   that the live body holds every image and matches the approved text.

Always pass `-R`. From any other checkout, such as a private plans repository,
gh would otherwise target the repository the current directory belongs to.
