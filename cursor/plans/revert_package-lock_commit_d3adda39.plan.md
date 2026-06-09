---
name: Revert package-lock commit
overview: Revert the accidental `package-lock.json` commit (`265c40f9`) on the `data-test-id` branch by creating a revert commit and pushing it to the remote.
todos:
  - id: revert-commit
    content: Run git revert 265c40f9 --no-edit to create a revert commit
    status: pending
  - id: push-revert
    content: Push the revert commit to origin/data-test-id
    status: pending
isProject: false
---

# Revert Accidental package-lock.json Commit

## Context

- Branch: `data-test-id` (already pushed to `origin/data-test-id`)
- Offending commit: `265c40f9` — "fixed the package lock" — contains **only** `package-lock.json`
- The branch is up to date with remote, so history rewrite (rebase/reset + force push) would be disruptive

## Plan

Since the commit is already pushed and the branch may be shared, the safe approach is `git revert` — it creates a new commit that undoes `265c40f9` without rewriting history.

**Step 1 — Revert the commit**

```bash
git revert 265c40f9 --no-edit
```

This creates a new commit titled `Revert "fixed the package lock"` that removes the `package-lock.json` changes introduced by `265c40f9`.

**Step 2 — Push the revert commit**

```bash
git push origin data-test-id
```

## Result

- `package-lock.json` changes from `265c40f9` will be undone on the remote.
- No history rewrite; safe for a shared branch.
- All other commits (`188609ab`, etc.) are untouched.

## Alternative (if you are the only one on this branch)

If no one else has pulled `data-test-id`, you could instead do a hard reset + force push to completely erase the commit from history:

```bash
git reset --hard 265c40f9~1   # go back to the commit before package-lock
git push origin data-test-id --force-with-lease
```

This is cleaner but **rewrites history** — risky if others have the branch checked out.
