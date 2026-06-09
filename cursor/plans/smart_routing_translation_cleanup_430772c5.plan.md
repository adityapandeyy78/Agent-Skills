---
name: Smart Routing Translation Cleanup
overview: Targeted rollback of unintended logic/structure changes while preserving translation implementation patterns (getter + SNAKE_CASE + I18n.language memoization), then complete hardcoded-text and naming-convention cleanup across smart-routing.
todos:
  - id: fix-share-modal-ids
    content: Move share option IDs into existing constants file and wire `share-router-modal.tsx` to it without new files
    status: completed
  - id: simplify-create-header
    content: Perform targeted rollback/simplification in `create-header.tsx` while preserving locale-safe status/value checks
    status: completed
  - id: normalize-naming
    content: Normalize SNAKE_CASE constants and getter naming consistency in touched smart-routing constants/components
    status: completed
  - id: translation-sweep
    content: Replace remaining hardcoded user-facing strings/aria labels in high-priority modified files and align translation keys
    status: completed
  - id: final-audit-verify
    content: Run lints + logical diff audit and report reverted/kept changes with translation coverage
    status: completed
isProject: false
---

# Smart Routing Translation-Only Remediation Plan

## Goal

Align all smart-routing changes to translation-only scope: remove unnecessary logic drift, preserve existing structure conventions, keep SNAKE_CASE stable constants, and complete i18n coverage.

## Scope Decisions (confirmed)

- Use **targeted rollback** (not full feature-wide reset).
- Store share option IDs in an **existing constants file** (no new file creation).

## Workstreams

### 1) Fix structural regression in share modal (compile-safe, translation-safe)

- Update `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/common/share-router-modal.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/common/share-router-modal.tsx)` to remove undefined symbol usage.
- Add `SHARE_ROUTER_MODAL_OPTION_IDS` to an existing constants module (or colocate in an already-existing smart-routing constants file) and import it in the modal.
- Preserve translation behavior (`I18n.t`, memoized options with `[I18n.language]`) while keeping state comparisons on stable IDs.

### 2) Revert only unnecessary logic complexity in header while keeping i18n-safe behavior

- Review and simplify `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/create-header.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/create-header.tsx)`.
- Keep original structure where possible; remove extra indirection that is not required for translation.
- Retain locale-safe comparisons against stable `.value`/keys (avoid label-based logic comparisons that break with translated strings).

### 3) Naming convention normalization (SNAKE_CASE + getter pattern)

- Audit touched constants/components and normalize naming to existing project style:
  - Stable exported constants in `SNAKE_CASE`.
  - Getter functions for localized display values.
  - Component-level memoization with `[I18n.language]` where arrays/maps are built from translated labels.
  - Memoized translated outputs consumed in components must remain `SNAKE_CASE` (same pattern used in notes, sequences, and meetings modules).
- Prioritize consistency in smart-routing constants and consuming components (especially status/route-type/workflow mappings).

### 4) Hardcoded string removal sweep (focus on active smart-routing paths)

- Replace remaining hardcoded user-facing text/aria labels/placeholders in modified smart-routing files, especially:
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/editor-tools.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/editor-tools.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/assignment/node-drawer/shared/routing-rule-filter.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/assignment/node-drawer/shared/routing-rule-filter.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/assignment/node-drawer/shared/shared-assignment-options.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/assignment/node-drawer/shared/shared-assignment-options.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/form-setup/api-setup/index.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/form-setup/api-setup/index.tsx)`
  - `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/form-setup/preview/canvas/toolbar.tsx](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/features/smart-routing/components/create-smart-route/form-setup/preview/canvas/toolbar.tsx)`
- Add/align keys in `[/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/smart-routing.ts](/Users/aditya.pandey/Codes/crm-client/applications/sparrow-crm/translation/input/sparrowcrm/en/smart-routing.ts)` only as needed.

### 5) Logical-change audit gate before finalize

- Re-run diff checks and verify no unintended behavior changes remain in targeted files.
- Ensure all status/flow checks still rely on stable values, not translated labels.
- Run lints on edited files and fix introduced issues.
- Produce final audit summary: what was reverted vs kept, translation coverage achieved, and any residual low-risk gaps.

## Validation

- Compile/lint clean for touched files.
- No undefined constants/symbols.
- No newly introduced files for IDs.
- No unnecessary logic refactors beyond translation support.
- Hardcoded user-facing strings removed from targeted modified files.
