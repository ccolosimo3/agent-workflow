# Frontend / Design — Principles & Anti-Patterns

Owns the cross-repo design *principles*; a repo's actual tokens / primitives /
patterns live in its own design doc. Review *process* lives in REVIEW_RUBRIC.md.

---

## The oracle

Backend behavior is right or wrong — a passing test is a free oracle, so "when X,
return Y" is specifiable. Frontend has none until the repo builds one: a **design
system** (tokens, a few primitives, named patterns). "Make it look good" is
unspecifiable; "these tokens, this primitive, these states" is as checkable as a
backend contract. Lacking one, spec against whatever system already exists — a
curated design doc, or the tokens/theme in code; a missing doc is not a missing
system. That system is the oracle.

The **screenshot** (or device/simulator capture) is frontend's "run the test" —
render the changed states and capture them as the visual proof; where the repo
wires a visual-regression baseline, diff against it. But a resting screenshot is
**blind** to keyboard operability, accessible name/role, contrast, and layout
shift: a broken-a11y or jumping screen looks correct in a still image. The
Accessibility and Layout rules
below exist to cover exactly what the screenshot misses — that is why they are
rules and not polish.

## Spec a UI work item

Concrete when it names three things: the **tokens/primitives/patterns** it uses,
the **states it renders**, and the **visual proof** (which screenshot or story
shows it correct).

## Design values come from tokens

- Every color, font, and brand-spacing value comes from tokens — never a raw
  literal (`#a3a3a3`, a magic size) or a value living outside the system. Layout
  utilities (flex, padding, gap) arrange; they never carry design values.
- Reuse the system's primitives; don't hand-roll one it provides (no bespoke
  shimmer where there's a Skeleton, no custom button).
- A token guarantees a value *exists*, not that your *choice* is right.
  Independently: never convey meaning by color alone (red-only error, hue-only
  link, gray-on-gray disabled), and meet contrast minimums (text 4.5:1; large
  text / UI / icons / focus rings 3:1).

## Cover the states that change

Build and prove every state that changes what renders, not just the happy path:
**default / hover / focus / active / disabled / loading / empty / error**. The
empty/no-data state is the one that ships broken, because no one rendered it.
**Focus** must carry a visible indicator — never remove the platform's focus
affordance (web `outline`, native focus ring) without replacing it.

## Accessibility is a contract

Every interactive control is **keyboard-operable** and exposes a programmatic
**name + role + state** — a native `<button>`/`<a>`, the correct aria/`role`, or
RN `accessibilityRole`/`accessibilityLabel`/`accessibilityState`. Defects,
not nits: an icon-only button with no label, a clickable `<div>`, a custom
dropdown with no keyboard path, a meaningful `<img>` with no alt (decorative
images take `alt=""`). Honor `prefers-reduced-motion`.

## Layout must not jump

Reserve space before async content arrives: explicit dimensions or a fixed aspect
ratio for images/media, skeletons sized to the real final layout, and don't shift
what the user is currently reading when content loads in above it (anchor the
scroll position). A component owns the spacing **inside** itself; the **parent**
owns the gap **between** children — prefer a `gap`/spacing container over outer
margins on the child, so spacing lives in one place and composes predictably.

---

## Your repo's design system

The concrete tokens, primitives, patterns, and visual identity live in the repo's
own design system — resolve it via the repo shim (a `DESIGN.md`, or the
tokens/theme + design docs the shim names). On the specifics the repo's system
wins; on the principle, this doc wins.
