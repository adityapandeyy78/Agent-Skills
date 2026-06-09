---
name: minimal-bugfix-twigs
description: Guides minimal-blast bugfixes and issue resolution with the simplest viable approach, codebase-aligned patterns, and Twigs-only UI using valid props and $ theme tokens for color and dimensions. Use this skill whenever the user is bugfixing, resolving tickets, hotfixing, narrowing change scope, asks for a "small fix", "quick fix", "minimal patch", references a SCRM ticket, or wants a small production-grade patch without over-engineering — even if they don't explicitly say "minimal".
---

# Minimal bugfix and issue resolution (Twigs)

## Mindset

- Prefer the **easiest fix that correctly solves the problem** over clever or generalized solutions.
- **Do not over-engineer**: no new layers, wrappers, or abstractions unless the bug cannot be fixed without them.
- **Reuse before adding**: if the fix can use **existing refs, variables, and state** in scope, use those. **Do not** introduce new `useRef` / `useState` / derived locals unless new state is **genuinely required** for correctness and the bug cannot be fixed without it.
- If something is unclear or might be **hallucinated** (APIs, props, behavior), **ground the answer in the repo**: search for similar implementations, types, and existing Twigs usage; use Twigs MCP component docs when changing UI components.

## Blast radius and scope

- Keep changes **as small as possible**: only files and lines needed for the bug or issue.
- **Do not** refactor, rename, reformat, or "clean up" unrelated code in the same change.
- **Do not** alter behavior or contracts outside what the bug fix requires.
- The patch should be **easy to review**: obvious intent, minimal diff, production-safe (types, a11y, loading states where the codebase already requires them).

## When to ask the user first

If making the fix **production-grade and easy to understand** would require **non-trivial changes to existing code** beyond the direct bug surface (e.g., restructuring shared components, changing public APIs, or touching many call sites), **stop and ask for permission** with a short summary of options (minimal-only vs. broader cleanup) before proceeding.

## UI and Twigs (when the fix touches UI)

- Use **Twigs** components and patterns only; match how nearby code uses Twigs.
- **Props must exist** on the Twigs components in use: verify against Twigs docs (MCP) or existing in-repo usage; do not invent prop names or values.
- For **color**, **width**, and **height** (and related layout sizing where the design system exposes them), use **theme tokens with the `$` form** (e.g. `$colors$...`, spacing/sizing tokens). Prefer tokens over raw px/hex; if no token exists for a value, follow `.cursor/rules/twigs-rule.mdc` for the exception rather than inventing styles.
- Follow project rules for **a11y** (e.g. `aria-label`, `data-testid` / `id` on buttons) when adding or changing interactive UI.

## Workflow checklist

1. Reproduce or restate the bug narrowly; identify the **smallest** code path to fix.
2. **Search** the codebase (and Twigs docs if UI) for the same pattern or component usage elsewhere.
3. Implement the **minimal** change; avoid drive-by edits.
4. If a "nicer" refactor would expand scope, **ask** before doing it.
5. Sanity-check that **unrelated** flows still behave as before.

## Additional resources

- Project Twigs and UI rules: `.cursor/rules/twigs-rule.mdc`, `.cursor/rules/twigs-mcp-ai.mdc` (when translating from Figma).
- General coding standards: `.cursor/rules/general-rule.mdc`.
