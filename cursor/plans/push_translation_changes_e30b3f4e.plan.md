---
name: Push Translation Changes
overview: "Push translation changes requires a two-step process: first commit and push in the translation submodule, then update the submodule reference in the parent repo."
todos: []
isProject: false
---

# Push Translation Changes

The `translation` folder is a **git submodule** (separate repository). Pushing changes requires two steps:

## Current State

**Translation submodule** (`applications/sparrow-crm/translation`):

- Branch: `feature/translation-contacts-and-automation`
- Modified files:
  - `.gitignore`
  - `sparrow-crm/en/common.ts`
  - `sparrow-crm/en/contacts.ts`

**Parent repo** (`crm-client`):

- Branch: `feature/translation-contantc-sequences`
- Shows translation submodule as `(new commits, modified content)`

## Steps to Push

### Step 1: Commit and push in the translation submodule

```bash
cd applications/sparrow-crm/translation
git add .
git commit -m "Add translation keys for contacts feature"
git push origin feature/translation-contacts-and-automation
```

### Step 2: Update submodule reference in parent repo

After pushing the submodule, go back to the parent repo and commit the updated submodule reference:

```bash
cd /Users/aditya.pandey/Codes/crm-client
git add applications/sparrow-crm/translation
git commit -m "Update translation submodule reference"
git push origin feature/translation-contantc-sequences
```

## Important Notes

- The `+` prefix in `git submodule status` output indicates the submodule has local changes not yet committed to the parent repo
- You must push the submodule first, otherwise the parent repo will reference a commit that doesn't exist on the remote
- Other modified files in the parent repo (component files) should be committed separately or together with the submodule reference update
