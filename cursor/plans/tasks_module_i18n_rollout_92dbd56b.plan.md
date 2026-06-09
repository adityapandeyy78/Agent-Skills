---
name: Tasks module i18n rollout
overview: Implement comprehensive i18n coverage for the tasks module, including shared dependencies it uses, while preserving existing architecture and avoiding behavioral changes.
todos:
  - id: inventory-current-keys
    content: Inventory existing keys in `common.ts` and `tasks.ts`; identify missing keys for tasks + shared dependencies.
    status: completed
  - id: add-en-input-keys
    content: Add missing English input keys under `translation/input/sparrowcrm/en/tasks.ts` (and `common.ts` when truly shared).
    status: completed
  - id: translate-tasks-components
    content: Replace hardcoded copy in tasks components with `I18n.t(...)`, including toasts, labels, placeholders, tooltips, aria-labels.
    status: completed
  - id: translate-shared-dependencies
    content: Update shared files used by tasks (`common/constants`, `features/notes/helpers`) to remove tasks-visible hardcoded literals.
    status: completed
  - id: memoize-translated-constants
    content: Add/adjust `useMemo` in consumers with `i18n.language` dependency for translated constants/getters.
    status: completed
  - id: audit-and-verify
    content: Perform final hardcoded-text audit, verify no logic changes, and resolve lint issues in touched files.
    status: completed
isProject: false
---

# Tasks Module Translation Implementation Plan

## Scope Confirmed

- Include `features/tasks` and shared dependencies used by tasks screens.
- Update only English input translation sources (`translation/input/sparrowcrm/en/*`); do not regenerate `translation/output/*` in this task.

## Target Files

- Translation sources:
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/common.ts](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/common.ts)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/tasks.ts](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/tasks.ts)`
- Highest-priority tasks files with hardcoded copy:
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/notify-modal.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/notify-modal.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/priority-selection.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/priority-selection.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/sorting.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/sorting.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/filter.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/filter.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/assignee-selection.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/tasks/components/my-task/assignee-selection.tsx)`
- Shared dependencies used by tasks:
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/common/constants/index.ts](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/common/constants/index.ts)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/notes/helpers/index.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/notes/helpers/index.tsx)`

## Implementation Approach

1. Baseline review and key inventory

- Read existing keys in `common.ts` and `tasks.ts` and map missing keys for:
  - modal titles/descriptions/buttons
  - toast success/error text
  - aria-label fragments
  - filter connector words (like date-range separator)
  - shared object-type labels and bucket fallbacks where surfaced in tasks
- Reuse existing key naming style in `tasks.ts` (and `common.ts` only when truly shared globally).

1. Add missing i18n keys (input only)

- Add all required English keys in `translation/input/sparrowcrm/en/tasks.ts`.
- Add to `common.ts` only if a key is cross-feature and already semantically common.
- Keep key hierarchy aligned with existing architecture (no ad-hoc namespaces).

1. Refactor tasks module hardcoded strings to i18n

- Replace hardcoded user-facing literals with `I18n.t(...)` in tasks files.
- Ensure toasts, placeholders, labels, tooltips, and aria-labels are all localized.
- Preserve non-translatable runtime data (names, API payload values) and only localize surrounding static text.

1. Apply translation to shared dependencies used by tasks

- Update `common/constants/index.ts` object-type labels to translation getters instead of raw English literals when consumed in tasks UI tooltips.
- Update `features/notes/helpers/index.tsx` fallback/group-label logic so tasks-visible labels remain translation-safe (without breaking notes behavior).

1. Constants getter loading with memoization

- For tasks constants/getters consumed as option arrays, ensure usage follows your requested pattern:
  - use `useMemo` in consuming components with `i18n.language` dependency where needed to recompute translated option labels deterministically.
- Keep memoization local to UI consumers to avoid introducing global state coupling.

1. Architecture parity and no-logic-change pass

- Mirror existing i18n usage style in the codebase (`I18n.t` / current hook usage patterns).
- Avoid behavioral changes (API payloads, enum values, filter/group logic).
- Only change text sources and translation wiring.

1. Comprehensive audit and verification

- Run a final hardcoded-text audit across `features/tasks` and confirmed shared dependencies.
- Re-check all changed components for accessibility constraints (aria-labels, ids/data-testid rules already present).
- Run lints/diagnostics for touched files and fix any introduced issues.

## Validation Checklist

- No remaining hardcoded UI strings in tasks scope (including toasts/errors/placeholders/tooltips/aria labels).
- Tasks UI renders with translation keys from `translation/input/sparrowcrm/en/tasks.ts` and `common.ts`.
- No logic regressions in task actions/filtering/grouping.
- Constants/options that are translation-driven are language-reactive via memoization with `i18n.language` dependency where applicable.
