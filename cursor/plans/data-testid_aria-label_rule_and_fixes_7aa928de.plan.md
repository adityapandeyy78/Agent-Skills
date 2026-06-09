---
name: data-testid aria-label rule and fixes
overview: Add a temporary Cursor rule and a clear plan so the agent applies data-testid and aria-label correctly (Radix asChild, Twigs, uniqueness, testing edge cases), and document what else must be fixed beyond the PR feedback.
todos: []
isProject: false
---

# data-testid and aria-label: Rule, Edge Cases, and Fix Plan

## 1. Agent rule (temporary – add to [.cursor/rules/twigs-rule.mdc](.cursor/rules/twigs-rule.mdc) or a new rule file)

Add a **dedicated rule** the agent must follow so the same mistakes are not repeated:

**Radix `asChild` (PopoverTrigger, DropdownMenuTrigger, HoverCardTrigger):**

- Put **one** `data-testid` and **one** `aria-label` on the **child** only. Omit both from the trigger.
- Use a **single** aria-label (e.g. "Select assignee" or "Open assignee selection"); do not set different labels on trigger and child.
- Do not duplicate `data-testid` or `aria-label` on both trigger and child.

**Uniqueness:**

- **Lists / repeated items:** Use a **unique** testid per instance (e.g. `data-testid={\`options-task-${task.id}}`or`accordion-trigger-task-${time}`). Never use the same static testid for multiple elements that can appear together (e.g. two "add-sort" buttons).
- **Single control on page:** Static testid is fine (e.g. `assignee-trigger`, `filter-trigger`).
- **Menus/dropdowns:** Content can use one testid per menu (e.g. `options-task-menu-${task.id}`); trigger must be unique per row if in a list.

**Twigs components (Accordion, Tabs, Dialog, etc.):**

- **Do not** add redundant `aria-label` on `AccordionContent` or `AccordionTrigger` when Twigs/Radix already expose roles (e.g. `role="region"`, `aria-expanded`). Keep `data-testid` on sections/triggers for tests.
- **Tabs:** `TabsList` / `TabsTrigger` benefit from one `aria-label` on the list and optional labels on triggers; `TabsContent` does not need an aria-label for readability if the active tab trigger already provides the name. Prefer one `data-testid` per tab panel (e.g. `data-testid="data-fields-content"`) for testing.
- **Dialog/Modal:** One `data-testid` and one `aria-label` on the root dialog for tests and a11y; avoid duplicating on both wrapper and inner element.

**Buttons / IconButtons (no asChild):**

- Every `Button` and `IconButton` must have exactly one `data-testid` (or `id`) and one `aria-label`. If the button is the child of a Radix trigger with `asChild`, the button gets the testid/aria-label and the trigger gets none.

**Checklist before submitting:**

- No duplicate `data-testid` on trigger and child when using `asChild`.
- No two different `aria-label` values for the same control (trigger vs child).
- No duplicate static testids for multiple elements in the same view (e.g. two "add-sort" or two "template-share-trigger").
- List items use unique testids (e.g. include `id` or index).

---

## 2. Uniqueness and edge cases (testing + code quality)

**Already broken (must fix):**

- **[sorting.tsx](applications/sparrow-crm/features/tasks/components/my-task/sorting.tsx):** Two elements with `data-testid="add-sort"` (lines 298 and 336). Use distinct ids (e.g. `add-sort-from-toolbar` and `add-sort-from-list`) or a single source of truth.
- **[create-template-modal.tsx](applications/sparrow-crm/features/notes/components/templates/create-template-modal.tsx):** Two `data-testid="template-share-trigger"` (lines 560 and 591). Make unique per context (e.g. include step or section).
- **[audit-log.tsx](applications/sparrow-crm/features/account-settings/components/audit-log/audit-log.tsx):** Both `Tabs` and `TabsList` use `data-testid="audit-log-tabs"`. Use different testids (e.g. `audit-log-tabs-root` and `audit-log-tabs-list`).

**Edge cases to keep in mind:**

- **Same component, multiple instances on one page:** e.g. "Open filter" in a toolbar vs in a filter pill – use different testids or include context (`add-filter-trigger` vs `filter-pill-trigger-${filter.id}`).
- **Disabled state:** testid/aria-label still on the same element; do not remove when disabled. Optionally add `aria-disabled="true"` and keep the label so tests and a11y still see the control.
- **Dynamic content (e.g. modals that open with different data):** Modal root can have one testid; use testids inside for key actions (e.g. `confirm-delete-${id}`) if you need to target a specific instance.
- **Nested triggers:** e.g. Popover inside a row – trigger testid should be unique per row (e.g. `url-cell-trigger-${column.id}` or row id) so tests can target the correct cell.

---

## 3. Twigs: when testid and aria-label are needed vs redundant

**Need data-testid (for tests and stability):**

- Any **interactive** control you want to target in E2E or component tests: triggers, buttons, tab triggers, key form fields, list item actions.
- **Containers** that define a section (e.g. `list-tasks-accordion`, `filter-popover-menu`) so tests can wait for or scope within them.
- Prefer **one** testid per logical control; for lists, make it unique (e.g. `options-task-${task.id}`).

**Need aria-label (for a11y and screen readers):**

- **Icon-only buttons**, custom controls (Flex/Box with role="button"), and triggers that have no visible text. One clear label per control (e.g. "Select assignee", "Open task options").
- **Semantic buttons** with visible text: often no aria-label needed (name comes from content). Add aria-label only if it adds clarity (e.g. "Submit form" on a "Save" button) or when the same text appears multiple times with different purpose.

**Redundant / avoid:**

- **AccordionContent:** Twigs/Radix already expose region/expanded state. **Remove** custom `aria-label` from AccordionContent (and optionally from AccordionTrigger if the trigger has visible text). Keep `data-testid` for tests (e.g. `accordion-content-task-${time}`).
- **TabsContent:** Often redundant if the active tab trigger already names the panel. Keep `data-testid` for tests; add `aria-label` only when the panel’s purpose is not clear from the tab label.
- **Duplicate labels:** Never two different aria-labels for the same focusable element (e.g. trigger vs child with asChild).

---

## 4. What else to fix (beyond PR feedback)

**A. asChild: move testid + aria-label to child only (already identified in prior audit)**

- All files using `PopoverTrigger asChild`, `DropdownMenuTrigger asChild`, `HoverCardTrigger asChild` with `data-testid` or `aria-label` on the trigger: remove from trigger, keep exactly one of each on the child. Align aria-label text (one phrase, e.g. "Select assignee").

**B. Duplicate or non-unique testids**

- [sorting.tsx](applications/sparrow-crm/features/tasks/components/my-task/sorting.tsx): two "add-sort" → make unique.
- [create-template-modal.tsx](applications/sparrow-crm/features/notes/components/templates/create-template-modal.tsx): two "template-share-trigger" → make unique.
- [audit-log.tsx](applications/sparrow-crm/features/account-settings/components/audit-log/audit-log.tsx): Tabs vs TabsList same "audit-log-tabs" → different testids.

**C. Inconsistent trigger testid when both trigger and child have one**

- Example: [task-item.tsx](applications/sparrow-crm/features/tasks/components/my-task/task-item.tsx) – trigger has `options-task-item-${task.id}`, IconButton has `options-task-${task.id}`. After moving to child only, keep **one** pattern (e.g. `options-task-${task.id}` on IconButton) and remove from trigger.

**D. Redundant aria-labels on Twigs**

- Remove `aria-label` from AccordionContent (and duplicate AccordionTrigger labels) in: task-list, form-sidebar-data-fields, form-sidebar-appearance, storage-setting, notes-list, insight-card, networks, details (contacts).
- Optionally tighten TabsContent aria-labels where they don’t add value (keep testids).

**E. HoverCardTrigger without asChild**

- [create-header.tsx](applications/sparrow-crm/features/smart-routing/components/create-smart-route/create-header.tsx) line 462: `HoverCardTrigger` without asChild has testid/aria-label. Either use asChild and put them on the child, or keep a single set on the trigger (no duplicate on child).

---

## 5. Testing and code quality

**For tests (future or existing):**

- Use **unique** testids for list rows/actions so you can target "options for task 3" vs "options for task 5" (e.g. `options-task-${task.id}`).
- Use **stable** testids for single-instance controls (e.g. "assignee-trigger", "filter-trigger") so tests don’t depend on implementation details.
- Avoid relying on duplicate testids (e.g. `getByTestId("add-sort")` when there are two – use role + name or unique id).

**Code quality:**

- One control → one focusable element → one `data-testid` and one `aria-label` where needed.
- Naming: prefer action-oriented labels ("Select assignee", "Open task options") and consistent testid naming (e.g. `*-trigger`, `*-menu`, `*-content`).
- When adding new Radix triggers with asChild, apply the rule from day one: only the child gets testid and aria-label.

---

## 6. Summary: what you were missing

- **Uniqueness:** testids must be unique when multiple instances exist on the same page (lists, repeated buttons); several duplicates exist today.
- **Twigs:** AccordionContent (and sometimes TabsContent/AccordionTrigger) don’t need extra aria-labels; testids are still useful for testing.
- **Single source of truth:** With asChild, only the child is in the DOM for the trigger – so only the child should have testid and aria-label; the PR feedback is correct.
- **Explicit rule:** A written rule (and checklist) prevents the agent from re-applying testid/aria-label on both trigger and child and from introducing duplicate testids.
- **Edge cases:** Disabled controls, nested triggers, and dynamic modals need unique or scoped testids so tests and a11y stay clear and stable.

Implementing the temporary rule first, then fixing duplicate testids and asChild usages, then cleaning redundant Twigs aria-labels will bring the codebase to a consistent, test-friendly, and a11y-correct state.
