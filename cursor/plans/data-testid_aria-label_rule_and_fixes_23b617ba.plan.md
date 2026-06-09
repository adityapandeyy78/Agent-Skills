---
name: data-testid aria-label rule and fixes
overview: Add a temporary Cursor rule and a clear plan so the agent applies data-testid and aria-label correctly (Radix asChild, Twigs, uniqueness, disabled state, Playwright E2E), and document what else must be fixed beyond the PR feedback.
todos: []
isProject: false
---

# data-testid and aria-label: Rule, Edge Cases, and Fix Plan

## Execution protocol (agent must abide)

- **The agent must abide by this plan and the rules below.** Work **feature by feature**; do not mix features.
- **Before starting each feature:** Read and apply the rules (Section 1 checklist, asChild rule, uniqueness, disabled state, Twigs). Confirm the list of files for that feature.
- **While working:** Put `data-testid` and `aria-label` only on the **child** for Radix asChild; never duplicate on trigger and child; use unique testids in lists; add `aria-disabled` only when truly required for production SaaS.
- **After completing each feature:** Confirm that changes comply with the rules (no testid/aria on triggers when asChild; one label per control; unique testids where needed). Then proceed to the **next feature**.
- **Feature order:** Account settings → (then Tasks, Table, Smart routing, etc. as per the plan’s fix list).

---

## 1. Agent rule (temporary – add to [.cursor/rules/twigs-rule.mdc](.cursor/rules/twigs-rule.mdc) or a new rule file)

Add a **dedicated rule** the agent must follow so the same mistakes are not repeated:

**Radix `asChild` (PopoverTrigger, DropdownMenuTrigger, HoverCardTrigger, DialogClose, AlertDialogCancel, AlertDialogAction):**

- Put **one** `data-testid` and **one** `aria-label` on the **child** only. Omit both from the trigger.
- Use a **single** aria-label (e.g. "Select assignee" or "Open assignee selection"); do not set different labels on trigger and child.
- Do not duplicate `data-testid` or `aria-label` on both trigger and child.
- **Popover + Calendar/DatePicker:** The trigger that opens the calendar follows the same rule (child only). The Calendar inside PopoverContent is not a trigger; give it one `data-testid` (and optional `aria-label`) for the grid.

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
- **Disabled state:** Keep `data-testid` and `aria-label` on the control in all states. Native: `disabled` prop only. Custom: `tabIndex={-1}` + visual cues. **No `aria-disabled` anywhere in this codebase.**
- **DropdownMenuContent / PopoverContent:** Omit `data-testid` and `aria-label` if every child item already has its own. Only add content testid if tests need to scope or wait for the panel explicitly.
- **Twigs components:** For Twigs Switch, Checkbox, Select, Drawer, Input: ensure one `data-testid` and one `aria-label` (or associated label) per interactive control. When unsure about Twigs a11y props, use MCP get_twigs_guidelines / get_twigs_component_docs.

---

## 2. Uniqueness and edge cases (testing + code quality)

**Already broken (must fix):**

- **[sorting.tsx](applications/sparrow-crm/features/tasks/components/my-task/sorting.tsx):** Two elements with `data-testid="add-sort"` (lines 298 and 336). Use distinct ids (e.g. `add-sort-from-toolbar` and `add-sort-from-list`) or a single source of truth.
- **[create-template-modal.tsx](applications/sparrow-crm/features/notes/components/templates/create-template-modal.tsx):** Two `data-testid="template-share-trigger"` (lines 560 and 591). Make unique per context (e.g. include step or section).
- **[audit-log.tsx](applications/sparrow-crm/features/account-settings/components/audit-log/audit-log.tsx):** Both `Tabs` and `TabsList` use `data-testid="audit-log-tabs"`. Use different testids (e.g. `audit-log-tabs-root` and `audit-log-tabs-list`).

**Edge cases to keep in mind:**

- **Same component, multiple instances on one page:** e.g. "Open filter" in a toolbar vs in a filter pill – use different testids or include context (`add-filter-trigger` vs `filter-pill-trigger-${filter.id}`).
- **Disabled state:** see subsection below (native vs custom).
- **Dynamic content (e.g. modals that open with different data):** Modal root can have one testid; use testids inside for key actions (e.g. `confirm-delete-${id}`) if you need to target a specific instance.
- **Nested triggers:** e.g. Popover inside a row – trigger testid should be unique per row (e.g. `url-cell-trigger-${column.id}` or row id) so tests can target the correct cell.

**Disabled state: native vs custom components**

- **Native components (Button, IconButton from Twigs):**
  - **Keep** `data-testid` and `aria-label` when the control is disabled. Do not remove or conditionally omit them.
  - Use **only** the component’s `disabled` prop (e.g. `disabled={isLoading}`). The native `disabled` attribute is applied and is exposed to assistive tech. **Do not add `aria-disabled**` on native buttons — it is redundant and can cause double announcement in screen readers.
  - Tests can still query the element and assert disabled state; screen readers get the control name and disabled state from the native attribute.
- **Custom components (Flex, Box, or other non-semantic elements with `role="button"`, `tabIndex`, `onClick`):**
  - **Keep** `data-testid` and `aria-label` when the control is disabled. Do not remove or conditionally omit them.
  - **Add aria-disabled only when truly required for production-grade SaaS:** Set `aria-disabled="true"` when disabled so assistive tech can announce the state (only when truly required for production SaaS) (custom elements don’t support the native `disabled` attribute).
  - Use `tabIndex={-1}` when disabled so the control is removed from the tab order. When enabled, use `tabIndex={0}`.
  - Use visual cues (e.g. `cursor: "not-allowed"`, reduced opacity) as needed.
  - When the trigger is Radix with `asChild` and the **child** is a custom element (e.g. Flex) and disabled, set `aria-disabled={true}` on that child only when truly required for production a11y.
- **Summary:** **Never remove** `data-testid` or `aria-label` when disabled. **Native:** use `disabled` prop only; do not add aria-disabled. **Custom:** add `aria-disabled="true"` and `tabIndex={-1}` **only when truly required** for production-grade SaaS (custom element is disabled and must be announced to assistive tech).
- **Important:** `aria-label` and `data-testid` are always on the interactive control (enabled or disabled). **aria-disabled:** add **only when truly required** for production-grade SaaS — custom control + disabled state.

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

- **DropdownMenuContent / PopoverContent:** Do **not** add `data-testid` or `aria-label` on the content wrapper if every `DropdownMenuItem` / child already has its own `data-testid` and `aria-label`. The items are the controls tests and screen readers need. The content testid is only useful if tests need to explicitly scope or wait for the panel itself; otherwise omit it and target items directly.
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

**F. Twigs documentation and other Twigs components**

- **Twigs docs:** The project uses Twigs via MCP (see [twigs-mcp-ai.mdc](.cursor/rules/twigs-mcp-ai.mdc)). When adding or auditing Twigs components, run **get_twigs_guidelines** and **get_twigs_component_docs** (MCP) to confirm which props Twigs exposes for a11y and testing (e.g. `aria-label`, `data-testid`). Do not assume; Twigs may already provide roles/labels for some components.
- **Switch (Twigs):** Every `Switch` that is a meaningful control should have one `data-testid` and one `aria-label`. Audit and add where missing (e.g. [ai-autofill.tsx](applications/sparrow-crm/features/object-settings/components/configurations/fields/ai-autofill.tsx) Switch has neither).
- **Checkbox (Twigs):** Same rule: one `data-testid` and one `aria-label` per Checkbox. Fix duplicate **id** where present (e.g. [task-setting.tsx](applications/sparrow-crm/features/profile-settings/components/task/task-setting.tsx) uses `id="accept-terms"` on multiple Checkboxes — ids must be unique; use unique testids and aria-labels instead). Audit [list-filter.tsx](applications/sparrow-crm/features/object-settings/components/list-filter.tsx) Checkbox (`list-filter-object-${id}`) and [location-field.tsx](applications/sparrow-crm/features/object-settings/components/configurations/fields/location-field.tsx) for missing aria-label.
- **Select (Twigs):** Most Selects already have data-testid + aria-label. When adding new Selects, always add both. If Twigs Select uses an internal trigger (e.g. asChild), apply the same rule: testid/aria on the actual control, not on a wrapper.
- **Drawer (Twigs):** Ensure the root `Drawer` has a `data-testid` (and optional `aria-label` for the panel) so Playwright can target it. Add where missing (e.g. [assignment node-drawer index.tsx](applications/sparrow-crm/features/smart-routing/components/create-smart-route/assignment/node-drawer/index.tsx) has `id` but no `data-testid`).
- **Input / FormInput (Twigs):** For key form fields that tests need to target, ensure either an associated `<label>` (preferred) or `aria-label` plus `data-testid`. Avoid duplicate or redundant labels.

---

## 4.5 Other components to keep in mind (thorough list)

**PopoverTrigger (including Calendar / DatePicker):**

- Any **Popover** that wraps a **Calendar** or **DatePicker** uses `PopoverTrigger asChild`. The same rule applies: put **one** `data-testid` and **one** `aria-label` on the **child** of the trigger only; omit from `PopoverTrigger`.
- The **Calendar** component inside `PopoverContent` is separate: it can have its own `data-testid` (e.g. `date-picker-calendar`, `select-cell-date-calendar`) and optional `aria-label` for the grid (e.g. "Select date") for tests and a11y. That is not a trigger, so one testid/aria on the Calendar is fine.
- **Files:** [due-date-selection.tsx](applications/sparrow-crm/features/tasks/components/my-task/due-date-selection.tsx) (PopoverTrigger + Calendar in content), [out-of-office.tsx](applications/sparrow-crm/features/profile-settings/components/user-profile/out-of-office.tsx) (two PopoverTriggers for start/end date – move testid/aria to child Flex), [all-components-preview.tsx](applications/sparrow-crm/features/smart-routing/components/create-smart-route/form-setup/preview/all-components-preview.tsx) (DatePickerPreview: PopoverTrigger asChild wraps FormInput; duplicate "trigger-date-picker" and "open-date-picker" – remove from trigger and inner Flex; one set on the actual control only), [date-cell.tsx](applications/sparrow-crm/features/table/components/row-cell/date-cell.tsx) (Calendar in RowPopover content – Calendar already has testid/aria; RowPopover’s trigger follows PopoverTrigger rule in [row-popover.tsx](applications/sparrow-crm/features/table/components/row-cell/row-popover.tsx)).

**DialogClose / AlertDialogCancel / AlertDialogAction (asChild):**

- Same as other Radix triggers with `asChild`: **only the child** (Button or IconButton) gets `data-testid` and `aria-label`. Do **not** put them on `DialogClose`, `AlertDialogCancel`, or `AlertDialogAction`.
- **Files:** reset-password-modal, enable-2fa-modal, logout-modal, delete-modal, email-signature-modal, create-email-alie-modal, next-action-modal, remind-recommendation-modal, team-members-modal, add-user-modal, add-role-modal, sso-modal, sso-exampt-email-modal, sso-diable-modal. In these, the child Button/IconButton already has testid/aria in some places; ensure the trigger component itself never has duplicate testid/aria.

**TabsTrigger:**

- In this codebase **TabsTrigger** is not used with `asChild`; it renders the tab button. So putting `data-testid` and `aria-label` on **TabsTrigger** is correct (they land on the real element). Only avoid **duplicate** testids (e.g. [audit-log.tsx](applications/sparrow-crm/features/account-settings/components/audit-log/audit-log.tsx): `Tabs` and `TabsList` both had `data-testid="audit-log-tabs"` – use different testids).

**Tooltip:**

- There is no `TooltipTrigger asChild` in the codebase. **Tooltip** wraps content (e.g. a PopoverTrigger or IconButton). If the wrapped content is a Radix trigger with asChild, the **trigger’s child** gets testid/aria per the PopoverTrigger/DropdownMenuTrigger rule. Do not add testid/aria on the Tooltip component itself; the interactive element inside is the one that needs them.

**RowPopover / cell triggers:**

- [row-popover.tsx](applications/sparrow-crm/features/table/components/row-cell/row-popover.tsx) uses `PopoverTrigger asChild` and receives `triggerComponents` as children. So the **passed trigger content** (e.g. Flex in date-cell, url-cell, email-cell) must carry the **one** `data-testid` and **one** `aria-label`; `PopoverTrigger` should not. Any cell that uses RowPopover (date-cell, url-cell, etc.) should ensure the trigger element they pass has testid/aria and that RowPopover does not add them on the trigger wrapper.

**Calendar (Twigs) when used as content:**

- When **Calendar** is used inside a Popover (e.g. due-date-selection, out-of-office, all-components-preview, date-cell’s contentComponent), the Calendar is the **content**, not a trigger. One `data-testid` (e.g. `select-cell-date-calendar`, `date-picker-calendar`) and one `aria-label` (e.g. "Select date") on the **Calendar** component are appropriate for testing and a11y. No asChild rule for Calendar itself.

**Summary table:**

| Component                                           | asChild?              | Where to put data-testid + aria-label                                          |
| --------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------ |
| PopoverTrigger                                      | Yes (when used)       | Child only; omit from trigger                                                  |
| DropdownMenuTrigger                                 | Yes (when used)       | Child only; omit from trigger                                                  |
| HoverCardTrigger                                    | Yes (when used)       | Child only; omit from trigger                                                  |
| DialogClose / AlertDialogCancel / AlertDialogAction | Yes                   | Child (Button/IconButton) only                                                 |
| Popover + Calendar/DatePicker                       | Trigger uses asChild  | Trigger: child only; Calendar in content: one testid/aria on Calendar          |
| TabsTrigger                                         | No (in this codebase) | On TabsTrigger (actual element)                                                |
| Tabs / TabsList                                     | No                    | One testid each; keep unique (e.g. audit-log-tabs-root vs audit-log-tabs-list) |
| AccordionContent / AccordionTrigger                 | N/A                   | No redundant aria-label; data-testid OK                                        |
| Tooltip                                             | N/A                   | On the interactive child inside, not on Tooltip                                |
| Calendar (as content)                               | N/A                   | One data-testid (+ optional aria-label) on Calendar                            |

---

## 5. Testing optimization: Playwright and our codebase

**Test stack: Playwright** (E2E). The plan is aligned with Playwright’s recommended selectors and supports both semantic and stable queries.

**Why this approach works well with Playwright:**

1. **Playwright recommends role and label first.** Locators like `page.getByRole('button', { name: 'Select assignee' })` or `page.getByLabel('Select assignee')` are preferred because they match how users and assistive tech find elements. Our rule (one `aria-label` on the real control) gives every interactive element an **accessible name**, so Playwright can use `getByRole(role, { name })` or `getByLabel()` when the control is unique.
2. **We keep both aria-label and data-testid on the same element.** So you get: **Semantic:** `page.getByRole('button', { name: 'Select assignee' })` — resilient to DOM/class changes. **Stable:** `page.getByTestId('assignee-trigger')` — Playwright’s built-in `data-testid` selector. **Lists:** `page.getByTestId(\`options-task-${task.id})` for a unique row. Unique testids in lists + consistent aria-labels = optimized Playwright tests.
3. **Recommended Playwright authoring:** **Single instance:** Prefer `page.getByRole('button', { name: 'Select assignee' })` or `page.getByLabel(...)`. **Lists:** Use `page.getByTestId(\`options-task-${id})`to target a specific row. **Fallback:**`page.getByTestId('...')` when role/name are ambiguous or when you need a stable selector.
4. **No testid-only trap.** We require both **aria-label** and **data-testid**. That lets Playwright prefer role/label and use `getByTestId` when needed (e.g. list disambiguation, dynamic content).

**Codebase fit:** Playwright’s `getByRole` / `getByLabel` use the same accessibility tree as screen readers. Putting testid and aria on the **child** (one DOM node) means both `getByRole` and `getByTestId` resolve to the same element. This setup is optimal for Playwright: prefer role/name where possible, use testid for lists and stable selectors.

---

## 6. Code quality and test authoring

**For tests (future or existing):**

- Use **unique** testids for list rows/actions so you can target "options for task 3" vs "options for task 5" (e.g. `options-task-${task.id}`).
- Use **stable** testids for single-instance controls (e.g. "assignee-trigger", "filter-trigger") so tests don’t depend on implementation details.
- Avoid duplicate testids. **Playwright:** Prefer `page.getByRole(role, { name })` or `page.getByLabel()` when the control is unique; use `page.getByTestId(...)` for list items or when you need a stable selector.

**Code quality:**

- One control → one focusable element → one `data-testid` and one `aria-label` where needed.
- Naming: prefer action-oriented labels ("Select assignee", "Open task options") and consistent testid naming (e.g. `*-trigger`, `*-menu`, `*-content`).
- When adding new Radix triggers with asChild, apply the rule from day one: only the child gets testid and aria-label.

---

## 7. Summary: what you were missing

- **Uniqueness:** testids must be unique when multiple instances exist on the same page (lists, repeated buttons); several duplicates exist today.
- **Twigs:** AccordionContent (and sometimes TabsContent/AccordionTrigger) don’t need extra aria-labels; testids are still useful for testing.
- **Single source of truth:** With asChild, only the child is in the DOM for the trigger – so only the child should have testid and aria-label; the PR feedback is correct.
- **Explicit rule:** A written rule (and checklist) prevents the agent from re-applying testid/aria-label on both trigger and child and from introducing duplicate testids.
- **Edge cases:** Disabled controls, nested triggers, and dynamic modals need unique or scoped testids so tests and a11y stay clear and stable.

Implementing the temporary rule first, then fixing duplicate testids and asChild usages, then cleaning redundant Twigs aria-labels will bring the codebase to a consistent, test-friendly, and a11y-correct state.
