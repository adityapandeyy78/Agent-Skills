---
name: Complete i18n work
overview: The i18n translation work for notes and sequences modules appears complete. The remaining steps are verification, linting, and cleanup before committing.
todos:
  - id: lint-check
    content: Run linter on all 21 modified source files and fix any new errors
    status: completed
  - id: verify-no-logic-changes
    content: Spot-check key notes files (filter.tsx, create-template-modal.tsx, notes-list.tsx) for logic integrity
    status: completed
  - id: flag-task-node
    content: Confirm with user if task-node.tsx bug fix should be included in i18n commit
    status: completed
  - id: commit-changes
    content: Stage and commit all changes with proper message
    status: in_progress
isProject: false
---

# Complete Notes & Sequences i18n Translation Work

## Current Status

The i18n implementation for the notes and sequences modules is **functionally complete**:

- **Notes module**: 19 files modified, ~175 translation keys in [`notes.ts`](applications/sparrow-crm/translation/sparrow-crm/en/notes.ts), 100% coverage confirmed by audit
- **Sequences module**: 2 files modified — [`due-date-selection.tsx`](applications/sparrow-crm/features/sequences/components/sequence-editor/nodes/task/due-date-selection.tsx) (day name translation) and [`task-node.tsx`](applications/sparrow-crm/features/sequences/components/sequence-editor/nodes/task/task-node.tsx) (bug fix for dueDate update)
- **Translations generated**: `npm run translate` already ran successfully for all 9 target languages
- **Translation submodule**: dirty with new translation keys

## Remaining Steps

### 1. Lint check on all modified files

Run `ReadLints` on all 21 modified source files to catch any errors introduced by the i18n changes. Fix any new linter issues.

### 2. Verify no logic changes in notes module

Quick spot-check diffs in key files ([`filter.tsx`](applications/sparrow-crm/features/notes/components/notes/filter.tsx), [`create-template-modal.tsx`](applications/sparrow-crm/features/notes/components/templates/create-template-modal.tsx), [`notes-list.tsx`](applications/sparrow-crm/features/notes/components/notes/notes-list.tsx)) to confirm only string replacements and getter pattern changes, no logic modifications.

### 3. Flag the task-node.tsx change

Line 259 adds `updateTaskField("dueDate", date)` — this is a **bug fix** (not i18n). Confirm with user if this should be included in the commit or separated.

### 4. Stage, commit, and optionally push

- Stage all changes including the translation submodule
- Commit with a descriptive message following repo conventions
