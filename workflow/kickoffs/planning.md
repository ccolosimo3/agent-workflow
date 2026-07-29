# Planning Kickoff

```text
Run planning kickoff for <feature/workstream> from <source>.

No code changes.

Deliver:
1. problem framing
2. goal and non-goals
3. risks and edge cases
4. 3-5 ordered implementation steps for the current Task; if the broader
   outcome needs multiple Tasks, sketch the sequence separately and fully
   specify only the next independently reviewable slice
5. testable acceptance criteria
6. exact verification plan by tier, including any broader local gates selected
   or intentionally not selected
7. review-ready spec markdown that can become the final tracker issue body
8. decision brief: chosen approach, one rejected alternative, tradeoff, assumptions
9. claim grounding: confirm each load-bearing code claim (where to wire a change,
   what a file already does, what a contract exempts, "follows pattern X") against
   current source, citing the file:line you checked; mark any claim you could not
   confirm as an open question instead of asserting it from memory. Scale to risk —
   a trivial single-surface fix can ground inline.
10. Domain Pass decision (one line): per the AGENTS.md "## Domain Pass" triggers,
    state whether this plan needs a Domain Pass and why or why not; if yes, run it
    or flag it as required before the spec goes review-ready.
11. Slicing decision (one line): state why this work is proportionate as one
    Task or where it should split; every proposed slice must remain valid if
    later slices never land, and avoid shape-only or prematurely generalized
    slices.
12. UI only: declare `Visual profile: standard | composition-heavy — <reason>`
    using `~/.agents/workflow/FRONTEND.md`. For `composition-heavy`, separate the
    locked product contract, design intent, and implementer discretion envelope,
    and name the early wide/narrow render plus final rendered proof.
```
