---
name: Testid Aria Feature Workflow
overview: Define a feature-by-feature workflow for adding data-testid and aria-label across the codebase using lint-first correction, and enhance the Cursor guideline so both self-closing and with-children Twigs usage are covered consistently.
todos: []
isProject: false
---

# Plan: Feature-by-feature testid/aria workflow and Cursor guideline

## 1. Recommended approach: lint-first, then fix (feature-by-feature)

**Use Biome as the source of truth** — it already warns on both usages:

- **Self-closing:** `<Component ... />` (e.g. `require-checkbox-testid.grit`, `require-select-testid.grit`)
- **With children:** `<Component ...>{children}</Component>` (e.g. `require-checkbox-children-testid.grit`, `require-select-children-testid.grit`)

So the correct way is:

1. **Run lint scoped to one feature** to get a list of files and line numbers where testid/aria are missing.
2. **Fix those locations** by adding the right `data-testid` and `aria-label` (following the naming table).
3. **Re-run lint** for that feature until clean, then move to the next feature.

This avoids guessing: Biome + Grit already know every Twigs component and both JSX shapes. Proactively adding without lint would risk missing usages or duplicating effort.

**Concrete commands:**

- Lint one feature (replace `contacts` with the feature folder name):
  ```bash
  npx biome lint applications/sparrow-crm/features/contacts
  ```
- Optional: get a report grouped by feature (audit script):
  ```bash
  node scripts/audit-testids.js --feature=contacts
  ```
  Note: the audit script’s component list (TIERS) is currently a subset of what Biome checks. Aligning it with Biome (see section 3) would make `--feature=` a full checklist per feature.

**Feature boundaries** (from [scripts/audit-testids.js](scripts/audit-testids.js) and repo layout):

- Features live under `applications/sparrow-crm/features/<feature-name>/` (e.g. `contacts`, `account-settings`, `lists`, `tasks`, `table`, `object-settings`, `smart-routing`, `share-modal`, `sequences`, etc.).
- Use the top-level folder name as the `{feature}` segment in testids (e.g. `contacts-create-contact-save-button`, `account-settings-audit-log-tabs`).

---

## 2. Twigs component shapes: keep both in mind

Your Biome plugins already cover both:

| Shape         | Example                                  | Covered by                              |
| ------------- | ---------------------------------------- | --------------------------------------- |
| Self-closing  | `<Checkbox checked={x} />`               | `require-checkbox-testid.grit`          |
| With children | `<Checkbox checked={x}>Label</Checkbox>` | `require-checkbox-children-testid.grit` |

When fixing feature-by-feature:

- **Do not** assume a component is only self-closing or only with-children; run lint and fix what it reports.
- **Naming:** Use the same convention either way (e.g. `data-testid="{feature}-{label}-checkbox"`, plus `aria-label` when the rule says so).

No change to Biome plugins is required for “correct way” — only a clear workflow and Cursor guidance.

---

## 3. Align audit script with Biome (optional but recommended)

Currently [scripts/audit-testids.js](scripts/audit-testids.js) TIERS list only a subset of components (Button, IconButton, Tr, FormInput, Input, Checkbox, DropdownMenuItem, DropdownMenuTrigger, Tab). Biome has many more (Select, Switch, Tabs, TabsList, TabsTrigger, TabsContent, Accordion*, Drawer, Dialog, Popover*, etc.).

**Recommendation:** Extend the audit script’s TIERS (or add a new tier) so that every component type that has a Biome Grit plugin is also audited. That way:

- `node scripts/audit-testids.js --feature=contacts` gives a **single** feature-level report that matches what Biome will warn about.
- You can use the audit for a quick “what’s missing in this feature?” and Biome for exact line-level fixes.

Implementation would be: add the missing component names to the appropriate TIERS in `audit-testids.js` (and keep the same file/line extraction logic so it still detects missing `data-testid` for those tags). No change to Biome or Cursor rules required for this step.

---

## 4. Enhance Cursor guideline ([.cursor/rules/testid-rule.mdc](.cursor/rules/testid-rule.mdc))

Add the following so Cursor (and humans) follow the same workflow and naming.

**A. Add a “Feature-by-feature workflow” section**

- State: when adding or editing Twigs components, work in one feature at a time.
- Steps: (1) Run `npx biome lint applications/sparrow-crm/features/<feature>` for that feature. (2) Fix every reported missing `data-testid` / `aria-label`. (3) Optionally run `node scripts/audit-testids.js --feature=<feature>` to confirm. (4) Move to next feature.
- Clarify that both `<Component />` and `<Component>{children}</Component>` must have the required attributes (Biome will flag both).

**B. Add “Deriving {feature}”**

- Short rule: derive `{feature}` from the path under `features/` (e.g. `features/contacts/...` → `contacts`, `features/account-settings/...` → `account-settings`). Use kebab-case. This keeps testids consistent and predictable.

**C. Explicit “Both shapes” reminder**

- In the Rules or a new subsection: “Twigs components may be used as `<Component />` or `<Component>{children}</Component>`. Both must have the required `data-testid` (and `aria-label` where the table says).” So autocomplete and edits don’t assume one shape only.

**D. “Before committing” line**

- Add: “Before committing changes in a feature, run `npx biome lint applications/sparrow-crm/features/<feature>` and fix any testid/aria warnings.”

**E. Optional: link to feature list**

- Either list the main feature folders (contacts, account-settings, lists, tasks, etc.) in the rule or point to “run the audit script with `--feature=` to see feature names.” This keeps naming consistent across the app.

No code or logic changes in the guideline — only additions to the existing [testid-rule.mdc](.cursor/rules/testid-rule.mdc) so the “correct way” (lint-first, feature-by-feature, both component shapes) is explicit for Cursor and for developers.

---

## 5. Summary: what to do in what order

| Step | Action                                                                                                                                                                                                                                                                                    |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Enhance [.cursor/rules/testid-rule.mdc](.cursor/rules/testid-rule.mdc) with workflow, “both shapes,” “deriving feature,” and “before committing” (section 4).                                                                                                                             |
| 2    | (Optional) Extend [scripts/audit-testids.js](scripts/audit-testids.js) TIERS so `--feature=` matches Biome’s component set (section 3).                                                                                                                                                   |
| 3    | Run feature-by-feature: for each feature, `npx biome lint applications/sparrow-crm/features/<name>`, fix all testid/aria warnings, then re-run until clean. Use the naming table in the Cursor rule and [docs/twigs-testid-aria-requirements.md](docs/twigs-testid-aria-requirements.md). |

Result: a single, consistent “correct way” — **run lint (and optionally audit) per feature, then add data-testid and aria-label** — with both `<Component />` and `<Component>{children}</Component>` covered by existing Biome plugins and clearly reflected in the Cursor guideline.
