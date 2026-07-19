---
name: explore
description: Map and rank the candidate approaches for an open architectural
  question or a working-but-imperfect system — "is there a more correct, more
  repo-conventional, or more performant version of this?" Runs a bounded read-only
  investigation to enumerate viable approaches grounded in the real codebase (web
  search encouraged for current framework/provider/engine behavior and
  version-specific limits), adversarially verifies each one's feasibility, and
  produces a ranked
  options/decision doc with a recommended approach and the next phase (spike if
  the approach carries an unproven bet, else specreview). Read-only — no code,
  no branch, tracker untouched. Use only when the operator explicitly invokes
  /explore or asks to run a formal explore pass for an architectural question.
  Do not trigger for casual questions about options or whether a better approach
  exists; answer those serially. Not for researching a fresh bug's root cause
  (that is spec) or proving one chosen bet (that is spike).
---

# explore

The solution-space-mapping phase: you are holding an open question or a
working-but-imperfect system and want the better versions surfaced, ranked, and
de-risked before committing. Distinct from `spec` (which researches a
*problem* → one plan) — explore researches *approaches* → a ranked comparison +
a recommended bet. Read-only: no code edits, no branch, no Linear/GitHub
mutations (the Destructive Action Policy applies to any command run).

## When invoked

1. **Frame the question and the baseline.** State the open question, what exists
   today (the current/working implementation, or greenfield), and — explicitly —
   what "better" means *here*: more correct, more repo-conventional, more
   performant, simpler, less coupled. Name the **evaluation axes** up front (e.g.
   WEB-174's transport layers / exactness / coupling tax). Vague axes produce
   vague comparisons.

2. **Map the solution space — bounded fan-out, read-only.** Decompose into
   independent evidence domains and use two read-only investigators by default.
   Use three only when the question has three genuinely distinct material domains
   (for example: repo precedent, current external constraints, and performance
   evidence); never exceed three. Keep a narrow question serial when splitting it
   would duplicate reading or coordination.
   Cover: existing repo patterns/precedents that already solve this or something
   adjacent (file:line); the idiomatic approach for the stack; performance/cost
   characteristics; and the **irreducible floor** — what no approach can avoid
   (engine limits, round-trip counts, framework constraints). Explicitly test
   whether the current implementation is already the engine-canonical / idiomatic
   pattern: "no better approach exists, keep it" is a valid and common outcome —
   don't manufacture a change to justify the exploration. **Use web search
   freely** to ground approaches in CURRENT external behavior —
   framework/library/provider/engine docs, version-specific limits, the industry
   floor, known upstream issues, and changelogs; prefer primary docs and cite the
   source when a decision rests on one (an approach map is only as current as the
   external tech it is measured against). Ground every candidate in the real
   codebase and real system behavior, not memory; for a greenfield question with
   no current implementation, ground in adjacent in-repo subsystems, prior art in
   git history, and the stack's idiomatic pattern instead.

3. **Adversarially verify each candidate.** For every viable approach, try to
   *refute* its feasibility against the real stack, not just list its upsides.
   Name each one's **durable tax / failure mode** (coupling reached via `as any`,
   reindex cost, partial-data risk). "Could not refute" is the bar for calling an
   approach feasible — "sounds good" is not.

4. **Rank and recommend.** Produce a comparison (axes × approaches), a
   recommended approach with rationale, and a **Rejected / not-worth-it** list
   with the reason each was dropped (so they are never re-litigated). Make
   relationships explicit (e.g. "C1 ⊂ B2"; "A is a stepping stone to B"). Flag
   anything that is a **product/policy decision, not an engineering optimization**
   as `[decision-required]` — don't decide it.

5. **Decide the next phase (the hand-off).** For the recommended approach, state
   which is true:
   - **Proven / conventional enough** → recommend finalizing the spec and
     `/specreview`.
   - **Carries an unproven bet** (unfamiliar tech, "can this mechanism even
     work?", fragile coupling) → recommend `/spike`, naming the *exact* bet to
     prove and its GO/NO-GO question.
   Plus any operator `[decision-required]` calls (which approach, product scope).

6. **Write the options doc.** Create a reference doc in the work-item folder
   (e.g. `<TOPIC>_OPTIONS.md` or `OPTIONS.md`, `status: reference` — the
   decision-doc convention, see existing `*_OPTIONS.md` docs): the decision, the
   comparison, the rejected list with
   reasons, the next-phase recommendation, and the open `[decision-required]`
   items. It is a durable decision record, not an implementation spec.

7. **Hand back to the operator.** End with the recommended approach, the
   next-phase recommendation (spike vs specreview), and the decision(s) needed.
   Do NOT auto-invoke spike or specreview — *which approach* and *whether to
   spike* are direction decisions the operator owns.

## Guardrails

- Read-only exploration: propose, don't build. Even a throwaway probe of a
  *durable or provider-touching* boundary needs an explicit operator ask (a
  read-only source/API/local probe to ground a feasibility claim is fine).
- Ground every candidate and feasibility claim in file:line + real system
  behavior; never compare approaches from memory or assumption.
- Attack each candidate (name its tax/failure mode); a one-sided pro-list is not
  an exploration.
- The rejected list must say *why* — an unexplained rejection invites
  re-litigation.
- Separate engineering optimizations from product/policy decisions; the latter
  are `[decision-required]`, returned to the operator, not chosen here.

## Failure modes

- Listing approaches without attacking them, or without grounding them in the
  real code — a comparison only as good as its evidence.
- Recommending change for its own sake — failing to seriously rank "keep the
  current approach" when it is already the idiomatic / floor solution; "no better
  approach found" is a valid result.
- Recommending a bet without saying whether it needs a spike or can go straight
  to specreview — that next-phase call is the point of the hand-off.
- Quietly picking a product/policy direction instead of surfacing it.
- Sliding into implementation, a branch, or a tracker mutation.
- Re-running a fresh problem investigation — for a new bug's root cause use
  `spec`; for proving one chosen approach use `spike`.
