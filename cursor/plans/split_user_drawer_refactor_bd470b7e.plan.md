---
name: Split User Drawer Refactor
overview: Reduce drawer.tsx size by moving copy to constants, pure logic to helpers, and UI into subcomponents, following patterns already used in this codebase (account-settings constants, contacts helpers/validation, add-user-modal helpers).
todos: []
isProject: false
---

# Split User Drawer (drawer.tsx) Refactor Plan

## Current state

- [drawer.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/drawer.tsx) is ~1255 lines: one component with ~20 state values, validators, handlers, and a large JSX tree (header, profile block, 6 field rows, footer).
- **Codebase patterns:** Account-settings uses [constants/index.ts](applications/sparrow-crm/features/account-settings/constants/index.ts) for feature constants; contacts use `features/contacts/helpers/` for validation and record helpers; [add-user-modal.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/add-user-modal.tsx) keeps small helpers (e.g. `tokenizeEmails`, `validateSingleEmail`) in the same file.

---

## 1. Constants: copy and validation messages

**Where:** Extend [features/account-settings/constants/index.ts](applications/sparrow-crm/features/account-settings/constants/index.ts) (or add a dedicated `user-drawer.constants.ts` in the same folder and re-export from `index.ts` if you prefer to keep drawer copy grouped).

**What to move:**

- **Validation messages:** `"Name must be at least 3 characters"`, `"Name must be less than 63 characters"`, `"Please select a country code"`, `"Phone number must be at least 6 digits"`, `"Phone number must be less than 15 digits"`.
- **Toast messages:** success/error/warning titles (e.g. `"User updated successfully."`, `"Failed to update user."`, `"You have unsaved changes. Click Save to keep them."`, file upload errors).
- **Field copy:** placeholders like `"Add Name"`, `"Add Phone Number"`, `"Add Team"`, `"Assign Role"`, `"Enter name"`, `"Select Team"`, `"Select Role"`.

**Pattern:** Export a single object (e.g. `USER_DRAWER_MESSAGES` or split `USER_DRAWER_VALIDATION`, `USER_DRAWER_TOASTS`, `USER_DRAWER_PLACEHOLDERS`) and use it in the drawer and in helpers that return error strings. This matches how other features keep UI/validation copy in constants (e.g. [object-settings/constants](applications/sparrow-crm/features/object-settings/constants/index.ts), [contacts validation](applications/sparrow-crm/features/contacts/components/record/attributes-details/attributes-types/validation.ts) using constants for error text).

---

## 2. Helpers: pure logic and validation

**Where:** Add a helper module next to the drawer. Two options consistent with the repo:

- **Option A (recommended):** `features/account-settings/components/user-permission/user-drawer-helpers.ts` — keeps drawer-specific logic colocated with the component (similar to [contacts](applications/sparrow-crm/features/contacts/helpers/record/index.ts) and [validation-helpers](applications/sparrow-crm/features/contacts/helpers/filter/validation-helpers.ts) living under the feature).
- **Option B:** `features/account-settings/helpers/user-drawer.ts` — only if you introduce a top-level `helpers/` folder for account-settings and want to reuse these functions outside user-permission.

**What to extract:**

- **Validation (pure, take value/state and return string | null):**
  - `validateName(value: string): string | null` — use constants for messages.
  - `validatePhoneNumber(phoneNumber: string, currentCountry: CountryData | null): string | null` — use constants for messages.
- **Phone parsing (pure):**
  - `applyPhoneStateFromUser(user: { phone?: string } | null, getDefaultCountry: () => CountryData | null): { country: CountryData | null; number: string }` — returns derived country + number so the drawer only calls `setCurrentCountry` / `setPhoneNumber`. Keeps `country-codes-list` usage in one place.
- **Payload / change detection (optional but useful):**
  - `buildUserUpdatePayload(...)` — given current form state and `selectedUser`, return the update payload and/or whether there are changes. This can stay in the drawer if you prefer fewer files; extracting it makes `handleUpdateUser` shorter and testable.

**What stays in the component:** State, refs, `useEffect`/`useMemo` that depend on state, and handlers that call `setState` or APIs (e.g. `onProfilePicChange`, `handleUpdateUser`, `handleCloseDrawer`, `handleFieldName`) — they can call the helpers but remain in the drawer (or in a custom hook in step 4).

---

## 3. Subcomponents: split the JSX

**Where:** New files under `features/account-settings/components/user-permission/`, e.g.:

- `user-drawer-header.tsx` — Close button, "User Details" title, dropdown (Activate/Deactivate).
- `user-drawer-profile.tsx` — Avatar, FileUpload overlay, display name, email.
- `user-drawer-fields.tsx` — Single component that renders the 6 rows (Name, Email, Phone, Created on, Team, Role) and receives all needed state and callbacks (e.g. `userDetails`, `onfieldclicked`, `editingName`, `setEditingName`, `nameError`, `setNameError`, `handleFieldName`, refs, team/role options, etc.). This avoids 6 separate files and keeps field logic together.
- `user-drawer-footer.tsx` — Save button and disabled logic.

**Data flow:** Parent (drawer) keeps all state and refs; pass props and callbacks down. No new context unless you later introduce a `useUserDrawer` hook and want to avoid prop drilling.

**Re-export:** In `drawer.tsx`, import these components and compose them so the main file becomes mostly composition + the hook (if you add one). This matches how the codebase splits large UIs (e.g. object-settings configurations, contacts record) into domain subcomponents while keeping state in a parent or hook.

---

## 4. Optional: custom hook for state and handlers

**Where:** `features/account-settings/components/user-permission/use-user-drawer.ts` (or `hooks/use-user-drawer.ts` under the same feature).

**What to move:** All `useState`, `useRef`, `useEffect`, `useMemo`, `useCallback`, and handler implementations from the drawer (e.g. `applyPhoneStateFromUser`, `onProfilePicChange`, `handleUpdateUser`, `handleCloseDrawer`, `handleFieldName`, `hasChanges`, `hasErrors`). The hook would take `selectedUser`, `isDrawerOpen`, `setIsDrawerOpen`, `handleDeactiveUser`, and return state + handlers + derived values.

**Benefit:** `drawer.tsx` becomes a thin presentational shell that calls `useUserDrawer(...)` and renders header, profile, fields, footer. This follows the project’s custom-hooks convention (e.g. [team-members-modal](applications/sparrow-crm/features/account-settings/components/user-permission/team-members-modal.tsx) with `useDefaultUserOptions`) and keeps the file under the cognitive complexity limit.

**Order:** Do this after constants + helpers + subcomponents so the hook only composes existing logic and doesn’t duplicate it.

---

## Recommended order of work

```mermaid
flowchart LR
  A[Constants] --> B[Helpers]
  B --> C[Subcomponents]
  C --> D[Optional hook]
```

1. **Constants** — Add drawer messages/placeholders to [constants/index.ts](applications/sparrow-crm/features/account-settings/constants/index.ts) (or `user-drawer.constants.ts`), then replace hardcoded strings in the drawer (and in helpers once added).
2. **Helpers** — Create `user-drawer-helpers.ts` with `validateName`, `validatePhoneNumber`, and optionally `applyPhoneStateFromUser` + payload builder; use constants for error strings; wire drawer to these functions.
3. **Subcomponents** — Extract header, profile, fields (one component), and footer into separate files; drawer imports and composes them with props/callbacks.
4. **Optional hook** — Move state and handlers into `useUserDrawer`, leave drawer as composition only.

---

## Summary

| Approach          | Where                                    | What                                                                       |
| ----------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| **Constants**     | `account-settings/constants`             | Validation messages, toasts, placeholders/labels                           |
| **Helpers**       | `user-permission/user-drawer-helpers.ts` | validateName, validatePhoneNumber, phone parsing, optional payload builder |
| **Subcomponents** | `user-permission/user-drawer-*.tsx`      | Header, profile, fields (one component), footer                            |
| **Optional hook** | `user-permission/use-user-drawer.ts`     | All state, effects, and handlers                                           |

This keeps the drawer maintainable, aligns with existing feature structure and conventions, and avoids a single 1200-line file without over-splitting (e.g. one component per field row is unnecessary; one “fields” component is enough).
