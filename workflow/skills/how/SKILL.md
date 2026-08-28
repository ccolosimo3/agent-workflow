---
name: how
description: Explain how an existing codebase subsystem works by tracing its real entrypoints, runtime or data flow, ownership, boundaries, and verification route. Use for code walkthroughs and current placement or ownership questions; not for designing a replacement, routine symbol lookup, or historical rationale.
metadata:
  opencode/autoinvoke: true
  workflow/kind: expert-guidance
---

# How

Build a working mental model from the repository's actual owners. This skill is
read-only advisory guidance: it does not select a workflow phase, widen scope,
edit code, require an artifact, dispatch mandatory helpers, or certify a design.

## Trace the system

1. Resolve the question from the current conversation and repository
   instructions. For minor ambiguity, state the narrow interpretation and
   proceed; ask only when materially different targets would produce different
   answers.
2. Find the public entrypoint or trigger and the observable result. Follow the
   real call, control, or data path between them rather than inferring behavior
   from names or directory shape.
3. Identify the owners of state, validation, persistence, configuration, and
   lifecycle. Call out generated, native, external, asynchronous, or
   cross-service seams only when they affect the requested flow.
4. Locate the smallest repository verification owner that exercises the
   behavior. Do not run gated or destructive proof merely to explain it.
5. Check surprising mechanics against nearby tests, documentation, and concrete
   callers. Separate verified behavior from material inference and unresolved
   edges.

Work directly by default. Do not fan out merely because a subsystem spans
several files; use bounded delegation only when the operator requests it or the
active workflow independently authorizes it for genuinely separate evidence.

## Explain for use

Return the smallest structure that makes the answer clear:

- a concise overview and the main concepts;
- the trigger-to-result flow with specific source links;
- where state and responsibilities live;
- the important boundary, lifecycle, or verification seams;
- gotchas and unresolved facts that could affect the user's next action.

Use a small diagram when it materially reduces explanation cost. Do not turn a
mechanics question into architectural critique or a replacement proposal. If
the user asks why the current shape exists, investigate rationale with `why`;
if they ask what should replace it and credible options remain open, that is a
separately selected design activity.
