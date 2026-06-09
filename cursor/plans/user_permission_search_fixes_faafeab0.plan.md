---
name: User permission search fixes
overview: Trim + useDebounce + React Query enabled on tab counts in user-permission; Twigs MCP (component list, guidelines, component docs) for Input/IconButton/Flex/Box context during implementation.
todos:
  - id: trim-search
    content: Replace local debounce effect with useDebounce(searchValue,300); trim; pass to tables/counts
    status: completed
  - id: rq-enabled-counts
    content: Add enabled + optional URL trim in useGet*Count hooks (user-permission.ts)
    status: completed
  - id: search-ux-layout
    content: Fix onBlur (trim), minWidth wrapper for search strip; autoFocus only (no refs)
    status: completed
isProject: false
---

# User permission search: simple fixes

## Goals (mapped to minimal changes)

| Issue                                  | Simple approach                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Spaces-only still hit API              | Treat **trimmed** string as the only “real” search: after debounce, `trimmedDebounced = debouncedSearchValue.trim()` and pass **only** that into tables and count hooks. Whitespace-only becomes `""` — no new requests, stable query keys.                                                                                                                                                                                                     |
| Role/team counts while on Users tab    | Add React Query **`enabled`** to existing [`useGetUserCount` / `useGetTeamCount` / `useGetRoleCount`](applications/sparrow-crm/features/account-settings/services/user-permission.ts) (optional second arg or overload): e.g. user count only when `activeTab === TAB_OPTIONS.USERS`. Parent passes `activeTab` + trimmed search.                                                                                                               |
| Search opens focused                   | **State only, no refs:** remove the local `useEffect` debounce block and use the shared **`useDebounce(searchValue, 300)`** from [`@common/hooks/use-debounce`](applications/sparrow-crm/common/hooks/use-debounce.ts) (same import path as other features, e.g. `object-list.tsx`). Keep Twigs **`Input`** with **`autoFocus`** when `showSearchbar` is true — no `ref` / `requestAnimationFrame` unless product later proves focus is broken. |
| Blur: close if no valid input          | Replace `onBlur` logic so it closes when **`searchValue.trim() === ""`** (treat spaces as empty). Align with clear button: clear + close as today.                                                                                                                                                                                                                                                                                              |
| Avatar / table “flicker” on open/close | **No table refactor.** Likely from (a) layout jump when swapping IconButton ↔ wide Input, and/or (b) all three tab counts refetching → loading skeletons in tab list. (a) Wrap search area in a **`Flex` with `minWidth: 400`** (or match input width) so the header width stays stable when toggling. (b) fixed by **`enabled`** on count hooks so inactive tabs do not refetch.                                                               |

## Files to touch (keep scope tiny)

1. **[user-permission.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/user-permission.tsx)**
   - Remove the inline debounce `useEffect`; use **`const debouncedSearchValue = useDebounce(searchValue, 300)`** from `@common/hooks/use-debounce`, then **`const trimmedDebouncedSearch = debouncedSearchValue.trim()`** for APIs/tables.
   - Pass `trimmedDebouncedSearch` to `UserTable`, `TeamTable`, `RoleTable`.
   - Pass `activeTab` into the three count hooks (signature change below).
   - Search `Input`: `onBlur` close when trim empty; optional stable-width wrapper.
   - Tab change: still reset `searchValue`; optionally reset `showSearchbar` if you want a clean tab switch (one line if desired).

2. **[user-permission.ts](applications/sparrow-crm/features/account-settings/services/user-permission.ts)**
   - Extend count hooks to accept **`enabled?: boolean`** (default `true` for backward compatibility).
   - `useQuery({ ..., enabled })`.
   - Optionally **`trim()` inside `getUserCount` / `getTeamCount` / `getRoleCount`** before building the URL so even old callers never send `search=%20%20` — one line per function.

## Twigs MCP (during implementation)

Use the **user-twigs-ai-mcp** server for design-system context before adjusting Twigs props or layout (per [`.cursor/rules/twigs-mcp-ai.mdc`](.cursor/rules/twigs-mcp-ai.mdc), scoped to what this change touches—no Figma unless matching a file):

- **`get_twigs_components_list`** — confirm component names.
- **`get_twigs_guidelines`** — tokens, spacing, patterns.
- **`get_twigs_component_docs`** — for **`Input`**, **`IconButton`**, **`Flex`**, **`Box`** as used in the search strip.

Figma tools on that MCP are optional here; this task is behavior + layout stability, not a new Figma screen.

## What we will **not** do (keeps this simple)

- No `useMemo` / `React.memo` on whole `UserTable` or column factories unless flicker remains after the two cheap fixes above.
- No **refs** for focus (no `inputRef`, no `requestAnimationFrame`); existing **`showSearchbar` + `autoFocus`** is enough.
- No custom debounce `useEffect` in this file — use **`useDebounce`** only.
- No click-outside library: blur + trim is enough for “click outside closes empty search”.

## Verification

- Open Users → click search: input focused, table avatars stable (no full-table skeleton unless users query actually loads).
- Type only spaces → after debounce, **no** new count or list requests (network tab).
- On Users tab, change search → **only** user count refetches (team/role idle).
- Blur with empty or spaces-only → search bar closes.
