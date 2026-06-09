---
name: testid aria-label standards
overview: Definitive rules and execution protocol for data-testid and aria-label across the sparrow-crm codebase. The agent must search each feature fresh — no pre-listed files. Apply all rules to every match found.
todos:
  - id: account-settings-verify
    content: "Account settings: scan ALL files in the feature, verify prior asChild fixes, remove aria-label from all DropdownMenuContent/TabsContent, check every file for all rules"
    status: completed
  - id: content-wrapper-pass
    content: "Content wrapper pass: grep entire codebase for DropdownMenuContent/TabsContent/AccordionContent with aria-label; remove aria-label from all instances found"
    status: completed
  - id: tasks-feature
    content: "Tasks: grep ALL files in features/tasks for every rule violation; fix all found"
    status: completed
  - id: table-feature
    content: "Table: grep ALL files in features/table for every rule violation; fix all found"
    status: completed
  - id: smart-routing-feature
    content: "Smart routing: grep ALL files in features/smart-routing for every rule violation; fix all found"
    status: completed
  - id: sequences-notes-feature
    content: "Sequences + Notes: grep ALL files in both features for every rule violation; fix all found"
    status: completed
  - id: contacts-meeting-feature
    content: "Contacts + Meeting: grep ALL files in both features for every rule violation; fix all found"
    status: completed
  - id: profile-object-settings
    content: "Profile settings + Object settings: grep ALL files in both features for every rule violation; fix all found"
    status: completed
  - id: dialog-content-pass
    content: "DialogContent pass: grep entire codebase for DialogContent and AlertDialogContent missing data-testid; fix all found"
    status: completed
isProject: false
---

# data-testid and aria-label: Rules and Execution Protocol

---

## Execution Protocol — agent MUST follow this every session

1. **Read all rules below** before touching any file. State which rules apply to the current feature.
2. **Work one feature (todo) at a time.** Do not mix features.
3. **Search first, edit second.** For every feature, run a fresh grep across the entire feature directory for:

- `asChild` — find all Radix trigger violations (Rule 1)
- `DropdownMenuContent`, `TabsContent`, `AccordionContent` — find content wrapper violations (Rule 2)
- `PopoverContent`, `DialogContent`, `AlertDialogContent` — check for missing testid/aria-label (Rule 2)
- `data-testid`, `aria-label` — check for redundancy, duplicates, uniqueness (Rules 3, 5, 6)
- Do **not** rely on memory or prior lists. Always grep fresh.

1. **After finishing a feature**, run the Quick Reference Checklist on every changed file before marking the todo complete.
2. **Feature order:** Account settings → Content wrapper pass → Tasks → Table → Smart routing → Sequences → Notes → Contacts → Meeting → Profile settings → Object settings → Deals → DialogContent pass.

---

## Rule 1 — Radix asChild: child only

**Applies to:** `PopoverTrigger`, `DropdownMenuTrigger`, `HoverCardTrigger`, `DialogClose`, `AlertDialogCancel`, `AlertDialogAction` — whenever `asChild` is present.

With `asChild`, Radix renders no DOM node for the trigger itself. It merges behavior onto the single direct child. Therefore:

- **Put `data-testid` and `aria-label` on the child element only.**
- **Remove both from the trigger element itself.**
- If both trigger and child have them → remove from trigger, keep on child. Align to one consistent `aria-label` value.
- If only the trigger has them → move to child, remove from trigger.
- Never place them on both simultaneously.

---

## Rule 2 — Content wrappers: what to remove vs keep

| Component                                                             | `aria-label`                                                                                                                                  | `data-testid`                                                                 |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `DropdownMenuContent`                                                 | **REMOVE always.** Radix gives it `role="menu"`; each `DropdownMenuItem` owns its label.                                                      | **REMOVE** unless a test must explicitly scope or wait for the panel to open. |
| `TabsContent`                                                         | **REMOVE always.** Radix auto-wires `aria-labelledby` from the matching `TabsTrigger`. Adding one here overrides and confuses screen readers. | **KEEP** — useful to assert which panel is active in tests.                   |
| `AccordionContent`                                                    | **REMOVE always.** Radix auto-wires `aria-labelledby` from `AccordionTrigger`. Same reason.                                                   | **KEEP** — useful to scope test assertions within the section.                |
| `PopoverContent`                                                      | **KEEP.** Gets `role="dialog"` and needs an accessible name for screen readers.                                                               | **KEEP** — useful to scope child queries and wait for panel open.             |
| `DialogContent` / `AlertDialogContent`                                | Prefer a `DialogTitle` inside. Use `aria-label` only when no visible title exists.                                                            | **ALWAYS ADD** if missing — every dialog must have a testid.                  |
| `HoverCardContent`                                                    | Optional — informational only.                                                                                                                | **KEEP** for tests.                                                           |
| `Popover` / `DropdownMenu` / `HoverCard` / `Dialog` **root wrappers** | **REMOVE.** Root is a React context provider that renders no DOM node.                                                                        | **REMOVE.** Same reason — silently dropped.                                   |

---

## Rule 3 — Uniqueness: no duplicate testids

- **Repeated elements (lists, table rows):** `data-testid` must include a unique identifier per instance — e.g. `options-task-${task.id}`, `accordion-trigger-task-${time}`, `role-options-menu-${role.id}`.
- **Single instance on page:** a static testid is fine — `assignee-trigger`, `filter-trigger`.
- **Never** use the same static `data-testid` on two or more elements that can exist simultaneously in the same view. If found, rename to make unique or remove the redundant one.

---

## Rule 4 — Disabled state: no aria-disabled

- **Native controls (`Button`, `IconButton`):** use the component's `disabled` prop only. Do **not** add `aria-disabled` — it is redundant and can cause double-announcement.
- **Custom controls (`Flex`, `Box` with `role="button"`):** use `tabIndex={-1}` + visual cues (opacity, cursor). Do **not** add `aria-disabled` anywhere in this codebase.
- **Never remove** `data-testid` or `aria-label` from a control just because it is disabled — they must stay regardless of state.

---

## Rule 5 — aria-label: when to add vs remove

**ADD `aria-label`:**

- Icon-only `IconButton` or `Button` with no visible text.
- Custom interactive elements (`Flex`, `Box` with `role="button"`) that have no visible text.
- `PopoverContent` — the floating panel needs a name for screen readers.
- `DialogContent` / `AlertDialogContent` when no `DialogTitle` exists inside.

**REMOVE `aria-label` if present on:**

- `DropdownMenuContent`, `TabsContent`, `AccordionContent` — Radix handles naming via `aria-labelledby`.
- Any Radix trigger (`PopoverTrigger`, `DropdownMenuTrigger`, etc.) when `asChild` is used — move to child instead.
- Buttons or controls with visible text — the text content is already the accessible name; an explicit `aria-label` overrides it and can mismatch what users see.

---

## Rule 6 — data-testid: when to add vs remove

**ADD `data-testid`:**

- Every interactive control tests need to target: `Button`, `IconButton`, `TabsTrigger`, `AccordionTrigger`, inputs, checkboxes, switches, selects.
- The **child** of every Radix `asChild` trigger — this is the real DOM node.
- Content panels: `TabsContent`, `AccordionContent`, `PopoverContent`, `DialogContent`.
- List/repeated items: one unique testid per row (e.g. `options-task-${task.id}`).

**REMOVE `data-testid` if present on:**

- Any Radix trigger (`PopoverTrigger`, `DropdownMenuTrigger`, `HoverCardTrigger`, `DialogClose`, `AlertDialogCancel`, `AlertDialogAction`) when `asChild` is used — the trigger has no DOM node; testid must be on the child only.
- `Popover`, `DropdownMenu`, `HoverCard`, `Dialog` root wrappers — React context providers, render no DOM element; the testid is silently dropped and does nothing.
- `DropdownMenuContent` when every `DropdownMenuItem` already has its own unique `data-testid` — tests target the items; the wrapper testid is redundant.
- Any element that carries the same static `data-testid` as another element visible at the same time — breaks Playwright `getByTestId` uniqueness.

---

## Quick Reference Checklist — run on every changed file before marking a todo complete

**REMOVE these if present:**

- `aria-label` on `DropdownMenuContent`, `TabsContent`, `AccordionContent`
- `aria-label` or `data-testid` on a Radix trigger when `asChild` is used — child only
- `aria-label` or `data-testid` on `Popover` / `DropdownMenu` / `HoverCard` / `Dialog` root wrappers
- `data-testid` on `DropdownMenuContent` when all items already have their own
- `aria-label` on buttons/controls with visible text
- Duplicate static `data-testid` on elements visible simultaneously

**ENSURE these are present:**

- One `data-testid` + one `aria-label` on the **child** of every Radix `asChild` trigger
- `data-testid` on `TabsContent`, `AccordionContent`, `PopoverContent`, `DialogContent`
- `aria-label` on `PopoverContent`
- `aria-label` or `DialogTitle` inside `DialogContent` / `AlertDialogContent`
- Unique `data-testid` for all list/repeated items (include id or index)
- `disabled` prop only for native controls; `tabIndex={-1}` for custom. No `aria-disabled` anywhere
