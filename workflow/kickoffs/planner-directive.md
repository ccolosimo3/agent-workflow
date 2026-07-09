# Planner directive (shared)

The Spec Review and Spec Re-Review templates both append this verbatim. Its exact
text is load-bearing (the Fidelity Rule depends on it):

> Planner: this is an autonomous review→revise→re-review loop. Resolve every
> finding you can by tightening the plan's correctness/clarity, then re-run
> `specrereview` on the revised spec — repeat until APPROVED. STOP and return to
> the operator only for findings that decide the plan's DIRECTION: anything
> marked `[decision-required]`, plus anything you cannot resolve without choosing
> an approach, changing scope, weighing a no-clear-winner tradeoff, or making a
> product/policy/naming call — treat these as decision-required even if unmarked,
> and never pick the direction yourself. Do not resolve a finding by deleting the
> flagged element or weakening an acceptance criterion to dodge it. Minor-only
> off-ramp: if after revising the ENTIRE remaining batch was mechanical and
> self-evidently correct (a corrected citation, a typo, a verbatim-added
> verification command / non-goal / criterion, a label fix) such that a fresh
> reviewer would add nothing, do NOT re-review — patch, break the loop, and
> report it as your call (not an APPROVED), noting the operator can re-review or
> rely on the outer gate; one substantive finding and you re-review instead.
> Cap: after 3 revise→re-review cycles without APPROVED, stop and surface the
> remaining findings (non-convergence is itself a signal). On any stop or on
> APPROVED, give a one-line-per-pass changelog of what you revised.
