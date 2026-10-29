# Agent Workflow V2 Frontend Authority

Load this file only when the work changes a UI surface. Repository design systems
own tokens and primitives; this file owns portable review and proof principles.

## Design oracle and scope

Use the repository's existing tokens, primitives, and visual patterns as the
oracle. Reuse them rather than introducing raw design values or parallel controls.
If no design document exists, inspect the actual theme and nearest complete
surface; absence of a document is not permission to invent a new system.

Distinguish visual-design work from incidental UI changes. Building or materially
recomposing a surface requires rendered inspection at representative wide and
narrow sizes, relevant themes and states, and hostile data. A copy, prop, or
layout-preserving behavior edit does not require screenshot ceremony; identify
the affected screen and run the smallest behavioral or operator proof.

## Changed states and interaction

Build and prove every state the change affects: default, hover, focus, active,
disabled, loading, empty, and error as applicable. Exercise real interaction;
a resting image cannot prove keyboard behavior, accessible semantics, or layout
stability.

## Accessibility contract

Interactive controls must be keyboard-operable and expose a programmatic name,
role, and state. Use native controls where possible. Preserve visible focus,
meaningful image alternatives, non-color-only meaning, adequate contrast and
reduced-motion behavior. Normal text needs 4.5:1 contrast; large text, UI,
icons, and focus indicators need 3:1. Pointer/touch targets are roughly 24×24px
or have equivalent spacing; inline text links are exempt. These are correctness
defects, not visual preference.

## Layout and composition

Reserve space for asynchronous content and media so the current reading position
does not jump. Parents own spacing between children; components own their internal
spacing.

Judge the rendered surface, not only its tokens:

- hierarchy makes the primary task and information order obvious;
- related content groups and scans with consistent density and alignment;
- long strings, missing media, large values, and larger row counts behave safely;
- the hierarchy and actions survive narrow and wide layouts without collision,
  overflow, or incoherent reflow;
- a local spacing or width correction is checked against sibling elements and the
  whole composition.

Record conclusions and any remaining uncertainty concisely. Temporary fixtures
are exceptional, must not ship, and are used only for a required state that the
live route cannot safely reach.

## Visual evidence

When implementing a change to what a user sees or does, show useful captures in
the completion report without waiting to be asked. Capture while verifying the
affected surface and reuse required verification captures: a short captioned
selection for visual-design work, or one capture for an incidental change when
it helps. Skip captures that add nothing. For incidental changes, don't start an
environment solely for a capture; don't add tooling or an exhaustive gallery just
for presentation. Use ordered screenshots for interactions and a short recording
when timing or motion matters. Add a before view when already available or cheap
to obtain without rebuilding the base solely for it.

Capture the actual implementation with synthetic or test data only, never real
personal data or secrets, and don't retouch captures. Inspect every capture you
cite. Caption the state shown and name the tested revision, environment and any
forced state or temporary fixture. Refresh captures when later changes invalidate
what they show. Keep selected captures with the work item's retained evidence,
outside product commits; they are not disposable scratch. Show them inline when
supported, otherwise as accessible file links. A delegated implementer returns
paths and captions for its lead to relay.

For an authorized PR, use the [PR body template](../templates/pr-body.md#visual-proof)
for layout and upload. If useful evidence cannot be captured or published, state
the concrete limitation and what remains unobserved or available only locally in
the normal completion. This presentation guidance adds no separate approval pause
or completion gate and does not waive required behavioral or rendered proof.
