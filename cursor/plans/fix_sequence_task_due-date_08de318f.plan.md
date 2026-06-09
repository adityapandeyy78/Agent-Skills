---
name: Fix sequence task due-date
overview: "Fix two bugs in the sequence task creation's due-date selection: (1) update local state so the button text changes after selecting a date, and (2) ensure day name abbreviations are i18n compatible."
todos:
  - id: fix-local-state
    content: 'Fix task-node.tsx: add updateTaskField("dueDate", date) in setSelectedDate callback so button text updates'
    status: pending
  - id: fix-day-names
    content: "Fix due-date-selection.tsx: make dayjs day abbreviations i18n compatible"
    status: pending
isProject: false
---

# Fix Sequence Task Due-Date Bugs

## Bug 1: Button text doesn't change after selecting a date

**Root cause**: In [task-node.tsx](applications/sparrow-crm/features/sequences/components/sequence-editor/nodes/task/task-node.tsx), the `setSelectedDate` callback (lines 258-266) only calls `handleUpdateTask()` for the API. It never updates the local `taskDetails.dueDate` state via `updateTaskField()`.

**Fix**: Add `updateTaskField("dueDate", date)` before the API call:

```tsx
<DueDateSelection
  selectedDate={taskDetails.dueDate}
  setSelectedDate={(date) => {
    updateTaskField("dueDate", date);
    const payload = {
      stepType: "TASK",
      taskUpdate: { setDue: date },
    };
    handleUpdateTask(payload);
  }}
/>
```

This mirrors how `PrioritySelection` works at line 271 -- it calls both `updateTaskField` and `handleUpdateTask`.

## Bug 2: Day name abbreviations not translated

**Root cause**: In [due-date-selection.tsx](applications/sparrow-crm/features/sequences/components/sequence-editor/nodes/task/due-date-selection.tsx), day abbreviations use `dayjs().format("ddd")` (lines 160, 188, 216) which always returns English ("Wed", "Sat", etc.) regardless of app locale.

**Fix**: Use `I18n.t()` with existing day-name keys, or add new translation keys for localized day formatting. The simplest approach: replace `dayjs().format("ddd")` with the full formatted date using `dayjs().format("ddd, DD MMM")` pattern but routed through a translated day name lookup, or add translation keys for short day names and use them.

- Check if there are existing day-name translation keys in the codebase
- If not, add keys like `common.dayShort.mon`, `common.dayShort.tue`, etc.
- Alternatively, use `dayjs` locale support if already configured in the project
