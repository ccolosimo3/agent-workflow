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

The **screenshot** (or device/simulator capture) is frontend's "run the test." For
genuine **visual-design work** — building or recomposing a screen, dashboard, or a
component's look — an agent captures it **autonomously** to verify
hierarchy/states/layout read right, via the host's fast tool: **Claude Code** → the
Claude Preview MCP (boot the dev server, screenshot across viewports + dark mode,
inspect computed styles), or browser control where the surface fits that better;
**Codex** → its in-app browser (primary), or browser control where better for the
work item; **native** → a sim capture runbook. Where no capture path exists for a
surface, capture stays operator-tier — name the proof and let the operator eyeball
it, don't skip it silently. For **incidental UI** — a copy/prop/behavior tweak that
merely touches a component — don't force a capture: name which screen shows it
correct and let the operator eyeball it. But a resting screenshot is
**blind** to keyboard operability, accessible name/role, contrast, and layout
shift: a broken-a11y or jumping screen looks correct in a still image. The
Accessibility and Layout rules below exist to cover exactly what the screenshot
misses — so prove those by exercising the UI (a keyboard/interaction pass, or a
story asserting real geometry), not a still capture; that is why they are rules,
not polish.

## Spec a UI work item

Concrete when it names three things: the **tokens/primitives/patterns** it uses,
the **states it renders**, and the **visual proof** (which screenshot or story
shows it correct).

### Visual profiles

Every UI work item declares `Visual profile: standard | composition-heavy —
<reason>`.

Use `composition-heavy` only when the task materially changes hierarchy or
reading order, repeated geometry, responsive composition, progressive
disclosure/default visibility, or a substantial multi-state surface. Copy-only,
isolated styling, accessibility-only remediation, invisible refactors, and
layout-preserving behavior changes remain `standard`.

A composition-heavy spec separates:

- the **locked product contract** — facts, actions, state, accessibility,
  required visibility, reading order, responsive semantics, and non-goals;
- the **design intent** — focal task, scan/inspect/act sequence, hierarchy,
  density, alignment, and the experience that must survive across widths; and
- the **implementer discretion envelope** — reversible choices such as grid
  fractions, spacing from the existing scale, wrapping, dividers, surface
  weight, text treatment, action alignment, and close breakpoint choices.

During implementation, prefer the live route and representative data. Before
completing the full behavior/state pass or broad verification, render the
structural composition once at a primary wide and narrow width, critique it
against the design intent, and correct material issues inside the discretion
envelope. After behavior and required states are complete, run one final render
→ critique → patch → recapture loop. Variants are
optional and capped at two when materially different compositions remain
plausible; pause for the operator only when the choice changes product priority,
visibility, terminology, interaction, or scope.

Handoff carries a compact evidence pointer: widths/themes and states exercised,
three-to-five critique conclusions and corrections (zero corrections is valid),
remaining visual uncertainty, the boundary between static capture, browser
interaction, automated proof, and operator-tier proof, and confirmation that
temporary fixture/tooling residue is absent. A fixture is exceptional: use one
only for a required state the live route cannot safely reach, and never ship it.

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
images take `alt=""`), a pointer/touch target under ~24×24px with no equivalent
spacing (inline text links exempt). Honor `prefers-reduced-motion`.

## Layout must not jump

Reserve space before async content arrives: explicit dimensions or a fixed aspect
ratio for images/media, skeletons sized to the real final layout, and don't shift
what the user is currently reading when content loads in above it (anchor the
scroll position). A component owns the spacing **inside** itself; the **parent**
owns the gap **between** children — prefer a `gap`/spacing container over outer
margins on the child, so spacing lives in one place and composes predictably.

## Composition, not just correctness

Every state/token/a11y/contrast/layout rule can pass and the screen still read
clumsy. Judge composition against the rendered surface (capture it to see) — don't
just assert it:
- **Hierarchy** — one focal point per view; size/weight/color/position track
  importance. Everything emphasized reads as nothing emphasized.
- **Scannability / density** — group related, separate unrelated, hold one rhythm;
  neither a wall of equal-weight rows nor whitespace islands.
- **Grid & alignment** — shared edges, consistent gutters, a predictable column
  structure; nothing floats one-off.
- **Hostile data** — design the long string, huge number, missing image, 3× the
  rows, the overflow — not the demo-perfect row; truncate, wrap, or clamp on purpose.
- **Responsive invariants** — the hierarchy holds narrow and wide; nothing
  overflows, collides, or reflows into nonsense.
- **Systemic, not symptom-local** — a width/padding/spacing change is never local:
  re-check the whole surface and its siblings after, because the nudge that fixes
  one card usually breaks its neighbors. Never tweak one number in isolation.

---

## Your repo's design system

The concrete tokens, primitives, patterns, and visual identity live in the repo's
own design system — resolve it via the repo shim (a `DESIGN.md`, or the
tokens/theme + design docs the shim names). On the specifics the repo's system
wins; on the principle, this doc wins.
