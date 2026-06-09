---
name: Sequences i18n cleanup
overview: "Sequence module only: remove dead duplicate option arrays in sequence constants (object-settings pattern). Touch files outside `features/sequences` only if required to keep builds/tests passing after export changes. App.tsx locale key and other app-wide fixes stay out of scope unless explicitly requested."
todos:
  - id: remove-dead-arrays
    content: In features/sequences only — remove unused English-only duplicate exports from constants/index.ts; keep *_VALUES + getters only
    status: completed
  - id: simplify-email-types
    content: Drop redundant label from SEQUENCE_SETTINGS_EMAIL_TYPES; verify types/usages
    status: completed
  - id: verify-build
    content: Run tsc/tests; grep imports of removed symbols — if any consumer lives outside features/sequences, apply minimal change there only to preserve behavior
    status: completed
  - id: optional-locale-remount
    content: Out of scope for sequence-only work — App.tsx / global i18n remount is outside features/sequences
    status: cancelled
isProject: false
---
