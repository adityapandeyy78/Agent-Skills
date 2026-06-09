---
name: sparrowcrm-translation
description: >
  Adds i18n translation keys to SparrowCRM feature modules. Use this skill whenever the user wants to
  translate a module, add translation keys, find hardcoded strings, wire up i18n for a settings section
  or any feature page, or says anything like "add translations for X", "translate this module", "find
  hardcoded text in X", "wire up i18n for the Y tab", "add i18n to the Z feature". This skill covers
  the full translation workflow: discovery → key reuse → key creation → replacement → verification.
  Always invoke this skill for SparrowCRM translation work — even if the user only mentions one of
  the steps (e.g. "just find hardcoded strings").
---

# SparrowCRM Translation Skill

You are adding i18n translations to a SparrowCRM feature module. The golden rule: **never change any
visible text content** — every word, letter, space, and punctuation in the UI must remain exactly the
same after your work. You are only wiring up the plumbing.

---

## Translation System Overview

- **Framework:** i18n direct instance — always use `I18n.t()`, never `useTranslation`
- **Source files:** `applications/sparrow-crm/translation/input/sparrowcrm/en/[module].ts`
- **Shared keys:** `common.ts` — always check here first before creating a new key
- **Key format:** camelCase dot-notation — `settings.userManagement.inviteUser`
- **Values:** exact UI strings, with `{{variable}}` for interpolated parts

**Always use this pattern — everywhere, including React components:**

```tsx
import { I18n } from "@i18n/setup";
I18n.t("settings.userManagement.inviteUser");
```

Never use `useTranslation`, `t()` from a hook, or any react-i18next hooks. The project standard is the `I18n` instance from `@i18n/setup`.

---

## Step 1: Understand the scope

Ask the user which module or feature file(s) to work on if not already clear. Then read:

1. The feature component files (`.tsx`, `.ts`) in the module
2. `applications/sparrow-crm/translation/input/sparrowcrm/en/common.ts` — full file
3. The module's own translation file (e.g. `en/settings.ts`) — full file

---

## Step 2: Discover all hardcoded text

Scan every file in the module for text that is:

- Hardcoded string literals passed to JSX (`<p>Save</p>`, `<Button>Cancel</Button>`)
- `placeholder="..."` attributes on inputs/textareas
- `aria-label="..."`, `aria-placeholder="..."`, `title="..."`, `alt="..."` attributes
- Error messages in `toast(...)`, `showToast(...)`, `notify(...)`, or similar calls
- Strings passed to alert/confirm dialogs, modal titles, empty state messages
- Any string that a user sees on screen — even inside a `cn(...)` conditional
- Tooltip content, dropdown option labels, badge text

**Do NOT flag:**

- Strings coming from API responses / backend data (variables, not literals)
- Internal identifiers, CSS class names, URL strings, event names
- `console.log` / debug strings
- TypeScript type strings, enum values used as keys (not displayed)
- Strings already wrapped in `t(...)` or `I18n.t(...)`

### Constants from constants.ts — ask before acting

Each module typically has a `constants.ts` (e.g. `sequences/constants.ts`) that exports SCREAMING_SNAKE_CASE values. These constants are imported and used as display text in JSX — some are good candidates for translation (user-visible labels), others should stay as-is (technical identifiers, brand names, format strings).

**Do not auto-decide.** After scanning the files, read the module's `constants.ts` and find every constant whose value appears in JSX or as a prop. Then present the user with a clear list and ask:

---

> **Constants review — please confirm which to translate**
>
> I found the following constants from `constants.ts` used as display text. Tell me which ones to translate (I'll create an `I18n.t()` key for them) and which to skip (I'll leave them as-is):
>
> | # | Constant | Value | Used as |
> |---|----------|-------|---------|
> | 1 | `SEQUENCE_STATUS_ACTIVE` | `"Active"` | Badge label |
> | 2 | `CSV_EXPORT_LABEL` | `"CSV"` | Button text |
> | 3 | `PRODUCT_NAME` | `"SurveySparrow"` | Page title |
> | 4 | `DEFAULT_STEP_NAME` | `"Untitled Step"` | Input placeholder |
>
> Reply with the numbers to **translate** (e.g. `translate: 1, 4`) and the ones to **skip** (e.g. `skip: 2, 3`). Or say `translate all` / `skip all`.

---

Wait for the user's reply before proceeding. Do not translate or modify any constant until you have explicit confirmation.

Once confirmed:
- **Translate** → create a translation key for the constant's value, then replace the constant reference in JSX with `I18n.t("module.key")`. Do not remove the constant from `constants.ts` unless it is now completely unused.
- **Skip** → leave the constant and its JSX usage completely untouched.

Build a complete inventory. For each item note: file path, the exact string, and where it appears (aria, placeholder, toast, JSX text, etc.).

---

## Step 3: Check common.ts for reuse

Before creating any new key, search `common.ts` for a key whose **value exactly matches** the string you found. If it matches, use that key — do not create a duplicate.

Then search the module's own translation file for the same match.

Only create a new key if no exact match exists in either file.

### Aria-label reuse rule

Do **not** create a separate key for an `aria-label` if its text is identical (or semantically equivalent) to a visible label that already has a key. Reuse the same key:

```tsx
// The button already has a key: settings.userManagement.inviteUser → "Invite User"

// Bad — unnecessary duplicate key
aria-label={I18n.t("settings.userManagement.inviteUserAria")}

// Good — reuse the existing key
aria-label={I18n.t("settings.userManagement.inviteUser")}
```

Only create a separate aria key when the aria text is genuinely different from any visible label — e.g., it adds context a sighted user gets from position or icon (`"Close invite user dialog"` vs the button label `"Close"`). Name it with an `Aria` suffix only in that case.

---

## Step 4: Name new keys

Follow these rules strictly:

- **camelCase** — `inviteUser`, `emailAddresses`, `audienceFilterDescription`
- **Structurally accurate** — nest under an object that reflects the UI section:
  ```ts
  settings: {
    userManagement: {
      inviteUser: "Invite User",
      pendingInvite: "Pending invite"
    }
  }
  ```
- **Max 3 levels of nesting** — `module.section.key` is the deepest you go. Never add a 4th level. If you feel you need one, flatten it by making the key name more descriptive instead:
  ```ts
  // Bad (4 levels)
  settings.userManagement.roles.adminLabel;
  // Good (3 levels, descriptive key)
  settings.userManagement.rolesAdminLabel;
  ```
- **Semantically clear** — the key name should describe the element's purpose in context, not just its text
- **Placeholders get a suffix** — `enterNamePlaceholder` or just `enterName` (either is fine, be consistent with the module)
- **Aria labels** — suffix with `Aria` only when needed to distinguish from the visible label: `closeModalAria`
- **Toasts/errors** — nest under a relevant section or use descriptive names: `deleteUserError`, `inviteSentSuccess`

Bad: `text1`, `str`, `msg`
Good: `inviteUserTitle`, `pendingEmailBadge`, `roleSelectPlaceholder`

---

## Step 5: Update the translation file

Add new keys to `applications/sparrow-crm/translation/input/sparrowcrm/en/[module].ts`.

Place them in the logically correct section. Maintain alphabetical order within a section where it already exists. Keep the structure flat or one level deep unless the module already uses deeper nesting.

**Do not change any existing keys or values.** Only append or add inside existing objects.

---

## Step 6: Replace hardcoded strings in the component

For each hardcoded string found:

1. Ensure `I18n` is imported: `import { I18n } from "@i18n/setup";`
2. Replace the string with `I18n.t("module.key")`
3. For interpolated strings like `"Hello {{name}}"`, use: `I18n.t("module.key", { name: userName })`

Keep the replacement surgically minimal — change only the string, touch nothing else on the line.

**Examples:**

```tsx
// Before
<Button>Invite User</Button>
// After
<Button>{I18n.t("settings.userManagement.inviteUser")}</Button>

// Before
<input placeholder="Enter company name" />
// After
<input placeholder={I18n.t("settings.companyNamePlaceholder")} />

// Before
aria-label="Close configuration"
// After
aria-label={I18n.t("settings.aiScoring.closeConfiguration")}

// Before
toast.error("Failed to save changes")
// After
toast.error(I18n.t("common.failedToSaveChanges"))
```

### Constant translation values with useMemo

When a translated string is used as a constant — typically to build arrays of options, column definitions, tab labels, or any data structure that doesn't need to re-evaluate on every render — wrap it in `useMemo`. Name the constant in **SNAKE_CASE**, consistent with the project convention.

```tsx
// Before
const ROLE_OPTIONS = [
  { label: "Admin", value: "admin" },
  { label: "Member", value: "member" },
];

// After
const ROLE_OPTIONS = useMemo(
  () => [
    { label: I18n.t("settings.userManagement.roleAdmin"), value: "admin" },
    { label: I18n.t("settings.userManagement.roleMember"), value: "member" },
  ],
  [I18n.language],
);

// Before
const TABLE_COLUMNS = [{ header: "Email Address" }, { header: "Status" }];

// After
const TABLE_COLUMNS = useMemo(
  () => [
    { header: I18n.t("settings.emailAddress") },
    { header: I18n.t("common.status") },
  ],
  [I18n.language],
);
```

Always include `I18n.language` in the `useMemo` dependency array whenever the memoized value contains any `I18n.t()` calls. This ensures the translated strings re-evaluate correctly if the user switches language at runtime. Without it, the memoized value would be stale after a language change.

Only introduce `useMemo` where the value is already a constant or computed once — do not add it to inline JSX strings or one-off renders. If `useMemo` is already present in the file, wrap into the existing one where it makes sense rather than adding a new one.

### Avoid nested ternaries

Never use nested ternaries to select a translation key or value. If the string depends on a condition, extract it to a variable or helper before passing to `I18n.t()`.

```tsx
// Bad — nested ternary
<span>
  {I18n.t(
    isAdmin
      ? hasRole
        ? "settings.adminRole"
        : "settings.noRole"
      : "settings.memberRole",
  )}
</span>;

// Good — resolve the key first
const roleKey = isAdmin
  ? hasRole
    ? "settings.adminRole"
    : "settings.noRole"
  : "settings.memberRole";
<span>{I18n.t(roleKey)}</span>;

// Also good — two separate keys, no nesting
const label = isAdmin
  ? I18n.t("settings.adminRole")
  : I18n.t("settings.memberRole");
```

A single ternary is fine. The moment it nests, extract.

### Singular and plural forms

When a string changes based on count, use i18next's built-in pluralization — do not manually stitch strings or use ternaries for this.

Add both forms to the translation file:

```ts
// In settings.ts
selectedUser: "{{count}} User selected",
selectedUser_other: "{{count}} Users selected",
```

Then call with the `count` option:

```tsx
I18n.t("settings.selectedUser", { count: selectedCount });
// → "1 User selected" or "3 Users selected"
```

When you spot a string that clearly has a singular/plural variant (e.g. "1 result" vs "2 results", "User" vs "Users"), always add both `_one` / `_other` keys rather than hardcoding one form or using a ternary to pick between two strings.

---

## Step 7: Content integrity verification

After all replacements are done, do a mandatory check:

For every string you replaced, verify that the value in the translation file matches the original hardcoded string **character-for-character** including:

- Capitalization
- Punctuation (commas, periods, ellipsis `...`, em dash `—`)
- Spacing
- Any `{{variable}}` placeholders matching what was in the original template

If you find any mismatch — even a single comma — fix the translation file value, not the component. The component content must never be the thing that changes.

---

## Step 8: Final sweep

After verifying, do one more pass through every file you touched:

1. Use grep or a read to check for any remaining string literals that look like UI text
2. Pay special attention to: conditional renders, ternary strings, fallback values in `I18n.t("key", "fallback")` (the fallback is fine to leave, but the key must exist in the file), tooltip props, empty-state illustrations with text
3. If you find anything missed, go back to Step 3 and handle it

Only declare the work complete when you've confirmed zero unhandled hardcoded UI strings remain in the files you touched.

---

## Step 9: Move types and interfaces to their type files

After the translation work is complete, look at every file you touched. If any file defines `interface`, `type`, or `enum` that:

- Is used by more than one file, OR
- Belongs in a type file that already exists for that module (e.g. `types.ts`, `[module].types.ts`, `interfaces.ts`)

…then move it:

1. Find the correct types file for the module. Look for `types.ts`, `*.types.ts`, or `interfaces.ts` in the same directory or a nearby `types/` folder.
2. Move the definition there (cut from source, paste into types file).
3. Add an import in the original file: `import type { MyType } from "./types";`
4. Grep for all other files that imported that type from the original location and update their imports too.

If no types file exists for the module, do not create one — only move to an already-existing file. If all usages are local to a single file, leave it in place.

Do not change the type definitions themselves — only relocate them.

---

## Step 10: Audit report

After all steps are done, produce a short audit report directly in the chat. Format it as a markdown table or grouped list. Cover:

### Changed files summary
List every file you modified and what category of change was made (translation wiring, constant extraction, type relocation, import update).

### Potential breakage risks
Flag anything that could cause a runtime or build issue:

| Risk | File | Reason |
|------|------|--------|
| `useMemo` dependency missing `I18n.language` | `SomeComponent.tsx` | Re-adding — verify it was correct |
| Type moved from component file | `settings/types.ts` | Confirm all consumers updated |
| Non-translatable constant introduced | `SomeComponent.tsx` | Was previously a string literal — verify no tests depend on exact string |
| Key reused across contexts | `common.ts` key X | Used in two different UI sections — verify both still read correctly |

Only include rows where there is a genuine non-zero chance of breakage. Do not pad with obvious safe changes. If nothing is risky, say so explicitly: "No breakage risks identified."

### Keys added
List all new translation keys created, grouped by file.

---

## What success looks like

- Zero hardcoded UI strings remain in the component files
- Product names, technical terms, and standard English constants are declared as named constants — not sent to the translation pipeline
- All aria attributes reuse existing keys where content matches; separate aria keys exist only where content differs
- All aria attributes, placeholders, toasts, and error messages are wired up
- No existing keys or values were modified in any translation file
- New keys follow the naming structure of the module
- Common keys from `common.ts` are reused where an exact match exists
- Types and interfaces that belong in a types file have been moved, and all consumer imports updated
- An audit report has been delivered listing changed files, breakage risks, and new keys
- The UI looks and reads exactly the same as before
