---
name: Lists Module i18n Implementation
overview: Create a `lists.ts` translation file, register it in the barrel, and replace all hardcoded user-facing strings across 7 lists module files (+ the services file) with i18n keys, reusing existing `common.*` and `settings.*` keys where they match exactly, and adding new `lists.*` keys for list-specific strings.
todos:
  - id: create-lists-ts
    content: Create `lists.ts` translation file with all structured keys
    status: completed
  - id: register-barrel
    content: Add `export { lists }` to barrel `index.ts`
    status: completed
  - id: translate-pages-index
    content: Replace hardcoded strings in `pages/index.tsx` (~22 strings)
    status: completed
  - id: translate-create-list-modal
    content: Replace hardcoded strings in `create-list-modal.tsx` + convert DEFAULT_VIEW_TYPES to getter function (no useMemo needed)
    status: completed
  - id: translate-duplicate-list-modal
    content: Replace hardcoded strings in `duplicate-list-modal.tsx` (~12 strings)
    status: completed
  - id: translate-list-modal
    content: Replace hardcoded strings in `list-modal.tsx` (~14 strings)
    status: completed
  - id: translate-object-selection
    content: Replace hardcoded string in `object-selection.tsx` (1 string)
    status: completed
  - id: translate-pipeline-selection
    content: Replace hardcoded strings in `pipeline-selection.tsx` (2 strings)
    status: completed
  - id: translate-services
    content: Replace hardcoded strings in `services/index.ts` (2 strings)
    status: completed
  - id: translate-emoji-selector
    content: Replace hardcoded aria-label strings in `emoji-selector.tsx`
    status: completed
  - id: full-recheck
    content: Re-read every file in the lists module top-to-bottom after all edits, grep for remaining hardcoded English strings, and fix any missed ones
    status: completed
  - id: final-audit
    content: "Final audit: diff every changed file against original to confirm zero logic/CSS changes, verify every user-facing string is i18n, verify keys exist in lists.ts"
    status: completed
isProject: false
---

# Lists Module i18n Implementation

## Approach

1. Create `lists.ts` translation file with structured keys
2. Register it in the barrel `index.ts`
3. Replace hardcoded strings file-by-file using `I18n.t()` everywhere (no `useTranslation()` hook)
4. Use getter function for the `DEFAULT_VIEW_TYPES` constant (called directly in component body, no `useMemo` needed since the whole app re-renders on language change)
5. Remove the existing `useTranslation()` import in `pages/index.tsx` (replace its `t()` call with `I18n.t()`)
6. Audit all changes for completeness and correctness

**Why `I18n.t()` only**: The app fully re-renders on language change (via `i18nInstance.changeLanguage()` + `initReactI18next`), so all components get fresh renders. `I18n.t()` always reads from the current language of the singleton instance, which is already updated before the re-render. No subscription hooks or memoization are needed.

## Key Reuse from `common.ts`

These existing keys will be reused (exact content match):

- `common.cancel` = "Cancel"
- `common.notes` = "Notes" (already used)
- `common.moreOptions` = "More Options"
- `common.continue` = "Continue"
- `common.recordAddedToListSuccessfully` (already used in add-record-modal)
- `common.failedToAddRecordToList` (already used in add-record-modal)
- `common.addRecordToList` (already used)
- `common.addRecordToListDialog` (already used)
- `common.closeRecipients` (already used)
- `common.searchRecords` (already used)
- `common.selectByName` (already used)
- `common.createByName` (already used)
- `common.addLater` (already used)
- `common.addToList` (already used)
- `common.selectObject` (already used)
- `common.close` = "Close"
- `common.duplicate` = "Duplicate"
- `common.yesDelete` = "Yes, Delete" (close but not exact -- "Yes, delete" lowercase d, so new key needed)

## Key Reuse from `settings.ts`

Some keys exist in settings but their content does not always match the exact strings in the lists feature module (e.g., settings has `listGeneralSettings.deleteListConfirmDescription: "Once deleted, your list cannot be recovered. Are you sure you want to delete this list?"` vs lists page has `"Once deleted, your list cannot be recovered. Are you sure?"`). So most list-feature strings need new keys in `lists.ts`.

## New Translation File: `lists.ts`

File: [applications/sparrow-crm/translation/input/sparrowcrm/en/lists.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/lists.ts)

Structured keys (grouped by context):

```typescript
export const lists = {
  // Page-level
  shareList: "Share list",
  export: "Export",
  settings: "Settings",
  duplicateList: "Duplicate list",
  copyListId: "Copy list ID",
  deleteList: "Delete list",
  addRecord: "Add record",
  listDeletedSuccessfully: "List deleted successfully.",
  failedToDeleteList: "Failed to delete list",
  idCopiedSuccessfully: "ID copied successfully!",
  failedToCopyId: "Failed to copy ID",
  deleteListConfirmTitle: "Delete list",
  deleteListConfirmDescription:
    "Once deleted, your list cannot be recovered. Are you sure?",
  yesDelete: "Yes, delete",

  // Create list modal
  createList: "Create List",
  listTitle: "List title",
  enterListTitle: "Enter list title",
  defaultView: "Default View",
  viewName: "View name",
  enterViewName: "Enter view name",
  listCreatedSuccessfully: "List created successfully",
  failedToCreateList: "Failed to create list",
  newList: "New List",
  defaultViewName: "Default",

  // View types (used via getter)
  tableView: "Table View",
  kanbanView: "Kanban View",

  // Duplicate list modal
  duplicateListTitle: "Duplicate List",
  listName: "List name",
  duplicateViews: "Duplicate views",
  allViews: "All Views",
  countSelected: "{{count}} Selected",
  selectAll: "Select all",
  searchViews: "Search views",
  listDuplicatedSuccessfully: "List duplicated successfully",
  failedToDuplicateList: "Failed to duplicate list",

  // List modal (select list)
  selectList: "Select List",
  searchLists: "Search lists",
  useListsToTrack: "Use lists to track records intelligently",
  noListsFound: "No lists found",
  startCreatingLists:
    "Start creating lists to organize your data. Create a list to get started.",
  noListsMatchingSearch:
    "No lists found matching your search. Try a different search.",
  pleaseSelectList: "Please select a list to add record to",
  addRecordToList: "Add record to list",
  recordAddedToListSuccessfully: "Record added to list successfully",
  failedToAddRecordToList: "Failed to add record to list",

  // Object selection
  object: "Object",

  // Pipeline selection
  stageField: "Stage field",
  selectPipeline: "Select pipeline",

  // Services
  updateFailed: "Update Failed",
  failedToUpdateListRecordAttribute: "Failed to update list record attribute",

  // Aria labels
  ariaLabels: {
    shareList: "Share list",
    notes: "Notes",
    export: "Export",
    moreOptions: "More options",
    moreOptionsDropdown: "More options dropdown",
    moreOptionsDropdownTrigger: "More options dropdown trigger",
    settings: "Settings",
    duplicateList: "Duplicate list",
    copyListId: "Copy list ID",
    deleteList: "Delete list",
    addRecordToList: "Add record to list",
    closeListCreation: "Close list creation",
    listTitleInput: "List title",
    createList: "Create list",
    closeDuplicateListModal: "Close duplicate list modal",
    listTitleDuplicateInput: "List title input",
    selectViewsToDuplicate: "Select views to duplicate",
    openDuplicateViewsSelector: "Open duplicate views selector",
    selectAllViews: "Select all views",
    searchViews: "Search views",
    cancelDuplicateListModal: "Cancel duplicate list modal",
    duplicateListModal: "Duplicate list modal",
    selectListDialog: "Select list dialog",
    createNewList: "Create new list",
    closeListModal: "Close list creation",
    searchListsInput: "Search lists",
    cancelList: "Cancel",
    addToList: "Add to list",
    emojiPicker: "Emoji picker",
    openEmojiPicker: "Open emoji picker",
    selectEmoji: "Select emoji",
    emojiPickerOptions: "Emoji picker options",
    selectPipeline: "Select pipeline",
  },
};
```

## Files to Modify (in order)

### 1. Create translation file and register it

- Create [applications/sparrow-crm/translation/input/sparrowcrm/en/lists.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/lists.ts)
- Add `export { lists } from "./lists";` to [applications/sparrow-crm/translation/input/sparrowcrm/en/index.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/index.ts)

### 2. `pages/index.tsx`

[applications/sparrow-crm/features/lists/pages/index.tsx](applications/sparrow-crm/features/lists/pages/index.tsx)

- `I18n` is already imported
- Remove `useTranslation` import and `const { t } = useTranslation()` — replace its single usage `t("common.contacts")` with `I18n.t("common.contacts")`
- Replace ~22 hardcoded strings with `I18n.t("lists.*")` calls
- Reuse `common.cancel` for Cancel button text in ConfirmationModal
- Keep all logic, CSS, and data-testid attributes unchanged

### 3. `create-list-modal.tsx`

[applications/sparrow-crm/features/lists/components/create-list-modal.tsx](applications/sparrow-crm/features/lists/components/create-list-modal.tsx)

- Import `I18n` from `@i18n/setup`
- Convert `DEFAULT_VIEW_TYPES` to a getter function `getDefaultViewTypes()` that returns the array with `I18n.t()` labels
- Call `getDefaultViewTypes()` directly inside the component body (no `useMemo` needed — app fully re-renders on language change, so the component re-mounts with fresh `I18n.t()` values)
- Replace ~12 hardcoded strings
- Default state values like `"New List"` and `"Default"` will use `I18n.t("lists.newList")` and `I18n.t("lists.defaultViewName")` as initial state

### 4. `duplicate-list-modal.tsx`

[applications/sparrow-crm/features/lists/components/duplicate-list-modal.tsx](applications/sparrow-crm/features/lists/components/duplicate-list-modal.tsx)

- Import `I18n` from `@i18n/setup`
- Replace ~12 hardcoded strings using `I18n.t()`
- Use interpolation for `"{{count}} Selected"` via `I18n.t("lists.countSelected", { count: selectedViewIds.length })`

### 5. `list-modal.tsx`

[applications/sparrow-crm/features/lists/components/list-modal.tsx](applications/sparrow-crm/features/lists/components/list-modal.tsx)

- Import `I18n` from `@i18n/setup`
- Replace ~14 hardcoded strings
- Reuse `common.cancel` for Cancel button

### 6. `object-selection.tsx`

[applications/sparrow-crm/features/lists/components/object-selection.tsx](applications/sparrow-crm/features/lists/components/object-selection.tsx)

- Replace `"Object"` FormLabel with `I18n.t("lists.object")`

### 7. `pipeline-selection.tsx`

[applications/sparrow-crm/features/lists/components/pipeline-selection.tsx](applications/sparrow-crm/features/lists/components/pipeline-selection.tsx)

- Import `I18n` from `@i18n/setup`
- Replace `"Stage field"` and `"Select pipeline"` with `I18n.t("lists.*")` calls

### 8. `services/index.ts`

[applications/sparrow-crm/features/lists/services/index.ts](applications/sparrow-crm/features/lists/services/index.ts)

- Import `I18n` from `@i18n/setup`
- Replace `"Update Failed"` and `"Failed to update list record attribute"` with `I18n.t("lists.*")` calls

### 9. `emoji-selector.tsx`

[applications/sparrow-crm/features/lists/components/emoji-selector.tsx](applications/sparrow-crm/features/lists/components/emoji-selector.tsx)

- Import `I18n` from `@i18n/setup`
- Replace aria-label strings `"Emoji picker"`, `"Open emoji picker"`, `"Select emoji"`, `"Emoji picker options"` with `I18n.t("lists.ariaLabels.*")` or reuse `common.emojiPicker` where it matches

## Getter Pattern for Constants

The `DEFAULT_VIEW_TYPES` in `create-list-modal.tsx` will be converted to a getter function:

```typescript
function getDefaultViewTypes() {
  return [
    {
      value: "table",
      label: I18n.t("lists.tableView"),
      icon: <TableViewIcon size={16} color="#64748B" />,
    },
    {
      value: "kanban",
      label: I18n.t("lists.kanbanView"),
      icon: <KanbanViewIcon size={16} color="#64748B" />,
    },
  ];
}
```

Usage inside the component — called directly (no hook, no memo):

```typescript
const defaultViewTypes = getDefaultViewTypes();
```

## What NOT to change

- No CSS modifications
- No logic changes
- No changes to data-testid values
- Backend-sourced strings (e.g., `view.name`, `item.title`, `item.emoji`, `error?.response?.data?.error`) remain untouched
- `OBJECT_FIELD_LABEL` is from `@common/constants` and used across the entire app -- translating it is out of scope for the lists module task (it's also used with `I18n.t("common.createByName", { name: ... })` where the label is interpolated, so it would need a broader coordinated change)

## Post-Implementation Re-check (Step 1 — full-recheck)

After all file edits are done, re-read every single file in the lists module from top to bottom:

1. `pages/index.tsx`
2. `components/add-record-modal.tsx`
3. `components/create-list-modal.tsx`
4. `components/duplicate-list-modal.tsx`
5. `components/list-modal.tsx`
6. `components/object-selection.tsx`
7. `components/pipeline-selection.tsx`
8. `components/emoji-selector.tsx`
9. `services/index.ts`

For each file, scan for any remaining:

- Quoted English strings passed as props (tooltip `content`, `placeholder`, `aria-label`, `title`, `description`, button children, `FormLabel` children, toast `title`/`description`)
- Template literals with English text
- Hardcoded strings in JSX children

Fix any missed strings on the spot.

## Final Audit (Step 2 — final-audit)

After the re-check pass, perform a final verification:

- Diff every changed file against its original to confirm zero logic/CSS changes
- Verify every user-facing string is wrapped in `I18n.t()`
- Verify every key used in `I18n.t("lists.*")` exists in `lists.ts`
- Verify every key in `lists.ts` is actually used (no orphaned keys)
- Confirm no `useTranslation()` hook was introduced
- Confirm no `useMemo` was added
- Confirm barrel `index.ts` exports `lists`
- Confirm backend-sourced values (e.g., `view.name`, `item.title`, `error?.response?.data?.error`) were left untouched
