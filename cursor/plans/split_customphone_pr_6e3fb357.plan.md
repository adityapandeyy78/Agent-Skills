---
name: Split CustomPhone PR
overview: On existing branch feature/custom-phone-number-input, restore the user-permission drawer phone UX to the pre–CustomPhone implementation and restore phone-number-cell.tsx to its previous implementation; keep CustomPhoneInput as a standalone addition only if you still want it in the PR.
todos:
  - id: fetch-and-checkout
    content: Fetch origin, checkout feature/custom-phone-number-input, identify merge-base vs target (e.g. main)
    status: pending
  - id: restore-drawer-and-cell
    content: Restore drawer.tsx, drawer-elements.tsx, phone-number-cell.tsx from merge-base (or main) — previous drawer phone + previous cell
    status: pending
  - id: cleanup-followups
    content: Remove orphan imports/deps (common/types CountryData, package.json react-phone-number-input) if unused; delete or keep custom-phone-input.tsx explicitly
    status: pending
  - id: verify-push
    content: lint/build, commit, push branch; PR describes drawer + cell reverted, optional standalone CustomPhoneInput
    status: pending
isProject: false
---

# feature/custom-phone-number-input — revert drawer phone + previous phone cell

## Goal (updated)

Remote branch already exists: [feature/custom-phone-number-input](https://github.com/sparrowcrm/crm-client/tree/feature/custom-phone-number-input).

On **this** branch you want:

1. **Drawer phone input** — same as **before** `CustomPhoneInput` (inline `CountryCodeDropdown` / `CountryPhoneNumberInput` + `validatePhoneNumber` / `getFieldConfig(..., currentCountry)` in [`drawer.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/drawer.tsx) and matching [`drawer-elements.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/drawer-elements.tsx)).
2. **Phone cell** — **previous** [`phone-number-cell.tsx`](applications/sparrow-crm/features/table/components/row-cell/phone-number-cell.tsx) (revert `type="tel"`, dropdown dedupe, `modal={false}`, portal/click-outside tweaks, etc.).

So the PR is **not** “wire CustomPhoneInput into the drawer + change shared cell”; it is “branch exists, but drawer and cell match the old behavior.”

## Optional: what stays on the branch

- **[`custom-phone-input.tsx`](applications/sparrow-crm/common/components/custom-phone-input.tsx)** — Either **keep** (standalone component for a follow-up / other screens) or **delete** if the PR should only be reverts. Decide before the final commit so the branch does not ship dead code unless intentional.
- **[`common/types/index.ts`](applications/sparrow-crm/common/types/index.ts)** / **[`package.json`](package.json)** — After restores, drop any additions that exist **only** for the drawer/cell/custom component (e.g. `CountryData` import with no use, `react-phone-number-input` if unused).

## Git approach (file-level restore)

Pick the **reference commit** that means “previous implementation” — usually **`origin/main`** or the **merge-base** between `feature/custom-phone-number-input` and your integration branch:

```bash
git fetch origin
git checkout feature/custom-phone-number-input
git merge-base HEAD origin/main   # note the SHA, or use origin/main directly
```

Restore the three files from that reference (example uses `origin/main`; substitute `MERGE_BASE_SHA` if you need the exact branch point):

```bash
git checkout origin/main -- \
  applications/sparrow-crm/features/account-settings/components/user-permission/drawer.tsx \
  applications/sparrow-crm/features/account-settings/components/user-permission/drawer-elements.tsx \
  applications/sparrow-crm/features/table/components/row-cell/phone-number-cell.tsx
```

Then:

- If you **remove** `custom-phone-input.tsx`, delete the file and fix any imports.
- If you **keep** it, ensure [`drawer.tsx`](applications/sparrow-crm/features/account-settings/components/user-permission/drawer.tsx) does not import it (restore above already removes that).
- Run `npm install` only if you changed `package.json`.

Commit, push:

```bash
git add -A
git commit -m "revert(user-permission): restore drawer phone and previous phone-number-cell"
git push origin feature/custom-phone-number-input
```

## Verification

- Drawer: editing phone uses the **old** country + national number flow (no `CustomPhoneInput`).
- Table / other callers: `CountryCodeDropdown` / `CountryPhoneNumberInput` behave like **pre-change** `phone-number-cell.tsx`.
- `npm run lint` / `npm run build:sparrowcrm` pass.

## Note on “only related blocks”

This workflow restores **entire files** from the reference revision. If `drawer.tsx` on the feature branch also contained **non-phone** edits you must keep, you cannot use a blind `git checkout origin/main -- drawer.tsx`; you would need to re-apply those edits or use interactive revert. Same for `phone-number-cell.tsx` if it had unrelated changes.

## Obsolete (earlier plan)

The earlier “stash phone paths onto a new branch / bugfix keeps old drawer” flow is **superseded** by: branch already created; **revert drawer + cell on that branch** as above.
