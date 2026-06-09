---
name: User permission search fix
overview: Replace inline debounce with the shared `useDebounce` hook, derive a trimmed “effective” search for API calls (skip whitespace-only), scope tab count queries to the active tab only, fix blur/collapse behavior for invalid/whitespace input, and wrap the three table components in `React.memo` to stop unnecessary re-renders (reducing profile color flicker).
todos:
  - id: debounce-trim
    content: Switch user-permission.tsx to useDebounce; derive effectiveSearch = trim; wire tables + validation
    status: completed
  - id: count-scope
    content: Scope useGetUserCount / Team / Role to active tab + effectiveSearch
    status: completed
  - id: blur-collapse
    content: "Fix onBlur: trim, collapse+clear when empty after trim"
    status: completed
  - id: memo-tables
    content: Wrap UserTable, TeamTable, RoleTable with React.memo
    status: completed
isProject: false
---

# User permission search: debounce, counts, collapse, and memo

## Current behavior (root causes)

- **Debounce:** [`user-permission.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/user-permission.tsx) already debounces with `useEffect` + `debouncedSearchValue` (lines 94–101) — functionally same as [`useDebounce`](applications/sparrow-crm/common/hooks/use-debounce.ts) but not the shared hook you asked for.
- **“API every keystroke” / flicker:** On each keystroke, `setSearchValue` runs → **parent re-renders** → `UserTable` / `TeamTable` / `RoleTable` re-render as unmemoized default exports even though the **list** query key uses `debouncedSearchValue` and may not refetch. That re-render is enough to re-run table/avatar code and **flicker profile colors** (e.g. [`getAvatarColors`](applications/sparrow-crm/features/account-settings/components/user-permission) usage).
- **All count APIs firing:** `useGetUserCount`, `useGetTeamCount`, and `useGetRoleCount` in the same file all use the same `debouncedSearchValue` in their [query keys](applications/sparrow-crm/features/account-settings/services/user-permission.ts) (lines 250–268), so a search on the Users tab updates the key for **all three** and triggers three network calls.
- **Search bar not collapsing on blur with spaces:** `onBlur` uses `e.target.value !== ""` (line 380). A whitespace-only value is **truthy** in the sense the bar stays “open” (`"   " !== ""`), and no trim/cleanup runs.

## Implementation plan

### 1) Shared debounce + trimmed “effective” search (no API for invalid input)

- Remove `useEffect` + `setDebouncedSearchValue` and use:

  `const debouncedSearch = useDebounce(searchValue, 300)` from [`@common/hooks/use-debounce`](applications/sparrow-crm/common/hooks/use-debounce) (same pattern as [`object-setting-list.tsx`](applications/sparrow-crm/features/object-settings/components/object-setting-list.tsx)).

- Derive a single value for requests, e.g. `const effectiveSearch = debouncedSearch.trim()` (or a small helper). Use `effectiveSearch` for:
  - All three **count** hooks (see step 2).
  - The `searchValue` prop passed to `UserTable`, `TeamTable`, and `RoleTable` (replacing the current `debouncedSearchValue` prop). This keeps list requests aligned with the same “non-empty after trim” rule; existing fetchers in [`user-permission.ts`](applications/sparrow-crm/features/account-settings/services/user-permission.ts) already add params only when `trim() !== ""` in several places, but the **count** GETs use raw `search=${searchValue}` and must be fed an empty string for whitespace-only input.

**Do not** pass the live `searchValue` to tables for querying — only the debounced+trimmed value, so behavior stays request-safe.

### 2) Tab-scoped count queries (stable counts on inactive tabs)

In [`user-permission.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/user-permission.tsx), pass search into each count hook **only when that tab is active**; otherwise pass `""` so the query key stays stable while the user types on another tab.

Example shape (use existing `activeTab` + `TAB_OPTIONS`):

- `useGetUserCount(activeTab === TAB_OPTIONS.USERS ? effectiveSearch : "")`
- `useGetTeamCount(activeTab === TAB_OPTIONS.TEAMS ? effectiveSearch : "")`
- `useGetRoleCount(activeTab === TAB_OPTIONS.ROLES ? effectiveSearch : "")`

No service-layer change required unless you later want a shared `staleTime` for count queries (optional, not required for this fix).

### 3) Blur: collapse and normalize when the query is “invalid”

- Replace the current `onBlur` with logic that uses **trim**:
  - If the trimmed value is empty: `setSearchValue("")`, `setShowSearchbar(false)` (collapse and clear, including “spaces only”).
  - Else: `setSearchValue` to `trim` so trailing/leading whitespace in state does not reappear in a bad way on next focus.
- Keep the clear `IconButton` as-is; ensure `onMouseDown` preventDefault stays so close does not fight blur in an odd way.

This matches: “collapse when input is invalid” and “when inactive, clean up so cursor isn’t stuck after whitespace” (normalize on blur with trim).

### 4) `React.memo` on the three tables

- Wrap the default export of [`user-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/user-table.tsx), [`team-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/team-table.tsx), and [`role-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/role-table.tsx) with `memo()` (e.g. `const UserTable = memo(function UserTable(...) { ... })` + `export default UserTable`).

**Why it works:** After step 1, the only search-related prop that changes for network behavior is the debounced+trimmed value. Parent will still re-render on each keystroke for the controlled input, but **memo** prevents table re-renders when `effectiveSearch` and `activeTab` (and other props) are unchanged, which addresses the **profile color flicker** without over-engineering.

**Caveat:** `RoleTable` receives `setIsAddRoleModalOpen`; `TeamTable` receives several setters — all are stable from `useState` in the parent, so they do not break memo. No need for `useCallback` on the parent unless a new inline function is introduced.

### 5) Imports and small cleanup in `user-permission.tsx`

- `import { memo } from "react"` only if you choose to colocate a tiny memoized wrapper in the same file; otherwise no change at parent level (memo is only on the three child modules).
- Remove the unused `useEffect` import if it becomes unused.

## Files to touch

| File                                                                                                                       | Change                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [`user-permission.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/user-permission.tsx) | `useDebounce`, `effectiveSearch`, tab-scoped count args, `onBlur` + stop passing duplicate debounced state |
| [`user-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/user-table.tsx)           | `export default memo(UserTable)` (or inline named component)                                               |
| [`team-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/team-table.tsx)           | same                                                                                                       |
| [`role-table.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/role-table.tsx)           | same                                                                                                       |

**Out of scope (keeps the change small):** Adding `enabled: activeTab === ...` to `useGetAllUsers` inside `UserTable` to silence background fetches for hidden Radix `TabsContent` (worth a follow-up if you still see list traffic off-tab). Not required to fix the **count**-API issue you described.

## Verification (manual)

- Type quickly in the search: list + **active tab** count only refire after debounce, not on every key; **inactive** tab pill counts do not re-fetch.
- Whitespace-only input: no search/count requests with a meaningful `search` param; blur collapses the bar and clears.
- With non-empty trimmed search: counts on active tab only reflect search; switch tab: correct baseline vs searched behavior per step 2.
