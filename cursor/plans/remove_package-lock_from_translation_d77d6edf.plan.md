---
name: Remove package-lock from translation
overview: Remove the accidentally pushed `package-lock.json` from the `crm-translator` submodule by creating a new commit that deletes it, then pushing to the remote branch.
todos:
  - id: rm-package-lock
    content: Run git rm package-lock.json inside the translation submodule
    status: pending
  - id: commit-removal
    content: Commit the removal in the translation submodule
    status: pending
  - id: push-translation
    content: Push the new commit to origin/feature/account-setting-profile-setting-translation
    status: pending
  - id: update-submodule-pointer
    content: Update and push the submodule pointer in crm-client
    status: pending
isProject: false
---

# Remove package-lock.json from Translation Submodule

## Context

- Submodule path: `applications/sparrow-crm/translation` → remote repo: `crm-translator.git`
- Current branch: `feature/account-setting-profile-setting-translation` (pushed to origin)
- `package-lock.json` was introduced in commit `baa1bc5` ("Added the translation of account-setting and profile-setting")
- 3 more commits sit on top of it — we should NOT rewrite history, just remove the file going forward

## Steps

**Step 1 — Enter the submodule and remove `package-lock.json` from tracking**

```bash
cd applications/sparrow-crm/translation
git rm package-lock.json
```

**Step 2 — Commit the removal**

```bash
git commit -m "chore: remove accidentally committed package-lock.json"
```

**Step 3 — Push to the translation remote**

```bash
git push origin feature/account-setting-profile-setting-translation
```

**Step 4 — Update the submodule pointer in `crm-client**`

After the above, the translation submodule will point to a new commit. Go back to the root and update the pointer:

```bash
cd /Users/aditya.pandey/Codes/crm-client
git add applications/sparrow-crm/translation
git commit -m "chore: update translation submodule (remove package-lock.json)"
git push origin data-test-id
```

## Result

- `package-lock.json` is removed from the translation repo going forward.
- No history rewrite — safe for shared branches.
- The `crm-client` submodule pointer is updated to reflect the clean state.

## Note

If you also want `package-lock.json` to never be committed again in the translation repo, add it to `.gitignore` inside the submodule in the same commit (Step 2).
