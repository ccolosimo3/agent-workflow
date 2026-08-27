---
name: typescript-engineering
description: Apply expert TypeScript type, API, and boundary design when materially reading, designing, editing, or reviewing .ts or .tsx code. Use for domain models, parsing, refactors, and correctness-sensitive TypeScript; not for generated declarations or unrelated prose.
metadata:
  opencode/autoinvoke: true
  workflow/kind: expert-guidance
---

# TypeScript Engineering

Strengthen the selected task with TypeScript-specific judgment. This skill does
not select a workflow phase, widen scope, require an artifact, or replace the
repository's instructions, compiler configuration, generated owners, or public
contracts.

## Model the domain

- Use discriminated unions when values have real variants with different valid
  fields. Do not use a bag of optional fields that admits contradictory states.
- Prefer the simplest type that keeps the required operations total. Strengthen
  an array, primitive, or object only where the looser type causes assertions,
  impossible-case throws, or repeated defensive checks.
- Brand or wrap primitives only when confusing two values is a credible defect
  and the repository has or earns a stable construction boundary.
- Derive from the authoritative schema, generated client, function signature,
  or existing domain owner before declaring a parallel interface.
- Prefer a clear local representation over clever type-level machinery that
  shifts complexity to every reader or caller.

## Keep boundaries honest

- Treat external, persisted, decoded, configuration, environment, and
  user-controlled data as untrusted until the owning boundary parses or narrows
  it into a named type. Static types do not replace runtime validation.
- Make guards verify every fact their return type promises. Prefer ordinary
  discriminant, `in`, `typeof`, or `instanceof` narrowing before a custom guard.
- Use exhaustive handling when adding a variant should force callers to make a
  decision. Keep the compiler error close to the match.
- Prefer `satisfies` when checking a value while retaining useful literal
  inference.
- Treat `any`, casts, non-null assertions, and assertion functions as evidence
  the compiler lacks a proof. Remove them when a better model or boundary check
  is practical. When a library limitation or already-proven invariant requires
  one, keep it narrow, local, and reviewable rather than pretending casts are
  universally forbidden.

## Shape usable APIs

- Design from caller usage and keep names aligned with repository vocabulary.
- Use an options object when several arguments are confusable or the call is
  likely to evolve. Keep simple positional APIs when they are clearer or a hot
  path makes allocation material.
- Preserve inference where it helps callers. Do not add annotations that merely
  repeat what the compiler already knows.
- Keep dynamic open records at genuinely dynamic boundaries. After validation,
  expose stable named contracts rather than spreading `Record<string, unknown>`.

## Verify proportionally

Follow the repository's real verification routes and the active workflow's
testing authority. Prefer a focused proof of observable behavior over tests that
only restate a type or mock the implementation. Preserve generated files and
unrelated formatting, and report any remaining runtime fact the type system
cannot establish.
