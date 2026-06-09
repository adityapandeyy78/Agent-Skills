---
name: Interactable non-semantic audit
overview: The agent implemented testid/aria for Twigs components (Button, IconButton, Dialog, etc.) but did not fully apply the rule to interactable non-semantic elements (Box, Flex, div with onClick). This plan audits account-settings for those gaps and defines additive-only fixes that do not change logic or flow.
todos: []
isProject: false
---

# Audit: Interactable non-semantic elements (Box/Flex/div) in account-settings

## Current state vs rules

**Rules** ([testid-rule.mdc](.cursor/rules/testid-rule.mdc), [a11y-rule.mdc](.cursor/rules/a11y-rule.mdc)) require that any **Box, Flex, or div** with `onClick` (or keyboard interaction) has:

- `data-testid`
- `aria-label`
- `tabIndex={0}` (so it’s focusable and keyboard-usable)

**What was done:** The agent added `data-testid` and `aria-label` to **Twigs interactive components** (Button, IconButton, Dialog, Input, Tabs, Select, etc.) across account-settings. Biome lint passes.

**What was not done:** A pass over **non-semantic interactables** was not done. Several **Flex**, **Box**, and one **AvatarGroup** (used as a clickable wrapper) in account-settings have `onClick` but are missing one or more of: `data-testid`, `aria-label`, `tabIndex`.

---

## Gaps (interactable, missing attributes)

| File                                                                                                                                 | Element                                                          | Current                                                           | Missing                                      |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------- |
| [drawer.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/drawer.tsx)                               | 3× `<Flex onClick={handleFieldClick}>` (lines 339, 346–359, 396) | No testid, no aria-label, no tabIndex                             | All three                                    |
| [role-setting-side-bar.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/role-setting-side-bar.tsx) | `<Flex onClick={...}>` per sidebar item (lines 97–128)           | No testid, no aria-label, no tabIndex                             | All three                                    |
| [add-user-modal.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/add-user-modal.tsx)               | `<Flex>` chip container (lines 377–395)                          | Has `data-testid="user-emails-chip-container"` and `tabIndex={0}` | `aria-label` only                            |
| [user-table.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/user-table.tsx)                       | `<Tr onClick={...}>` (lines 583–594)                             | Has `data-testid`, `tabIndex={0}`, `onKeyDown`                    | `aria-label` (e.g. “View user” + name/email) |
| [custom-avatar-group.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/custom-avatar-group.tsx)     | `<Box role="button" onClick={onAddClick}>` (lines 18–38)         | Has `aria-label`, `tabIndex={0}`                                  | `data-testid` only                           |
| [team-table.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/team-table.tsx)                       | `<AvatarGroup onClick={...}>` (lines 209–220)                    | Only `css` and `onClick`                                          | `data-testid`, `aria-label`, `tabIndex={0}`  |

**Already correct (no change):**

- [role-table.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/role-table.tsx): Click is on `DropdownMenuItem` (semantic); it already has `data-testid`.
- [view-members-modal.tsx](applications/sparrow-crm/features/account-settings/components/user-permission/view-members-modal.tsx): `onClick` is on an `IconButton`, which is already covered.

---

## Approach: additive-only, no logic/flow change

- **Only add** `data-testid`, `aria-label`, and/or `tabIndex={0}` where missing.
- **Do not** change:
  - Any `onClick` / `onKeyDown` handlers or their logic
  - Conditionals, structure, or control flow
  - Existing props order or behavior
- **Naming:** Use existing feature prefix and patterns (e.g. `account-settings-user-permission-...`, `account-settings-...`).

---

## Edge cases and safe application

1. **drawer.tsx — `handleFieldName` returning Flex (3 places)**
   The same helper returns different Flex UIs (empty placeholder, team list, or role name). Add attributes to each returned Flex without changing branches or handlers. Example labels: “Edit [field]” or “Select team list” / “Select role” so they stay meaningful and non-breaking.
2. **role-setting-side-bar.tsx — mapped Flex items**
   Each item is a Flex with `onClick`. Use a **dynamic** `data-testid` and `aria-label` per item (e.g. `data-testid={\`account-settings-role-setting-permission-${item}}`,` aria-label={Select permission ${item}}`) so tests and a11y stay correct and behavior is unchanged.
3. **user-table.tsx — `<Tr>**`

`Tr`is semantic (table row). Adding`aria-label`should use row data (e.g. user name or email) so screen readers get context. Only add the attribute; do not change`onClick` or row rendering logic. 4. **team-table.tsx — AvatarGroup**
Twigs `AvatarGroup` is used as a clickable control. Add `data-testid`, `aria-label` (e.g. “View team members”), and `tabIndex={0}`. If the component does not forward `onKeyDown`, adding only testid and aria-label is still an improvement; document that keyboard activation may need a follow-up if Twigs does not support it. 5. **custom-avatar-group.tsx — inner Box (line 79)**
The inner `<Box>` (avatar + icon) has `aria-label="Add member"` but no `onClick`; the **outer** Box has `onClick`. Only the outer Box needs `data-testid`. Do not change structure or event handling.

---

## Implementation checklist

- **drawer.tsx**: Add `data-testid`, `aria-label`, and `tabIndex={0}` to all three Flex elements returned by `handleFieldName` (placeholder Flex, team-list Flex, role-name Flex). Keep `handleFieldClick` and all logic unchanged.
- **role-setting-side-bar.tsx**: Add `data-testid={\`account-settings-user-permission-role-setting-permission-${item}}`,` aria-label={Select permission ${item}}`, and` tabIndex={0}`to the mapped Flex. Do not change`onClick` or scroll logic.
- **add-user-modal.tsx**: Add `aria-label` to the chip container Flex (e.g. “Email addresses”). Do not change `tabIndex`, `data-testid`, or `onClick`/`onKeyDown`.
- **user-table.tsx**: Add `aria-label` to the `Tr` using row data (e.g. “View user {name}”). Do not change `onClick`, `onKeyDown`, or row structure.
- **custom-avatar-group.tsx**: Add `data-testid` to the outer Box (e.g. `account-settings-user-permission-manage-members-trigger` or pass via props). Do not add `onClick`/handlers to the inner Box.
- **team-table.tsx**: Add `data-testid`, `aria-label` (e.g. “View team members”), and `tabIndex={0}` to the `AvatarGroup` that has `onClick`. Optionally add `onKeyDown` for Enter/Space only if the component supports it and it does not change existing behavior.
- Re-run `npx biome lint applications/sparrow-crm/features/account-settings` and fix any new warnings.
- Smoke-check: no removal or reorder of existing props; no change to handlers or flow.

---

## Summary

- The **right approach** in the rules (testid + aria + tabIndex for non-semantic interactables) is correct; the **implementation** in account-settings did not yet cover Box/Flex (and AvatarGroup used as clickable) in the listed files.
- Applying the checklist above keeps changes **additive-only**, avoids logic/flow changes, and addresses edge cases (dynamic labels, mapped items, table rows, nested Box) without breaking functionality.
