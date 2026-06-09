---
name: pr-review
description: Generates comprehensive pull request descriptions from git diffs, commit history, and changed files. Use this skill whenever the user is creating or updating a pull request, asks to write a PR description, says "pr", "/pr", "draft a PR", "raise PR", "open PR", "PR body", or asks for help with their pull request — even if they don't explicitly request a description.
---

# PR description generator

Produce pull request descriptions that reviewers can scan quickly and trust.

## Workflow

1. Gather context (diff, commits, related files).
2. Analyze changes (what changed, why it matters, impact).
3. Generate a description using the template below.
4. Present it for approval.
5. Offer to create the PR with the GitHub CLI (`gh`) when appropriate.

## Step 1 — Gather context

Run commands appropriate to the repo (default branch may be `main` or `master`; detect with `git symbolic-ref refs/remotes/origin/HEAD` if unsure):

```bash
# Working tree vs last commit
git diff HEAD

# Branch vs default branch (example: main)
git diff main...HEAD

git log main..HEAD --oneline
git log main..HEAD --format="%B---"
```

## Step 2 — Analyze changes

For each meaningful change, capture:

- **What**: Technical change.
- **Why**: Motivation (commits, comments, tests).
- **Impact**: Features, performance, security, migrations, breaking changes.

Use commit messages, resolved TODOs, tests, and doc updates as evidence.

## Step 3 — Output template

Always output the PR description inside a fenced markdown code block so the user can copy it in one click. Structure it exactly like this:

````
```markdown
## Summary

[1–2 sentences: what this PR does and why.]

## Changes

- **[Area or component]**: [What changed]
- **[Area or component]**: [What changed]

## Affected Areas

<!-- Modules, features, or pages a reviewer should pay attention to -->
- **[Module/Feature]**: [Brief reason it may be impacted]
- **[Module/Feature]**: [Brief reason it may be impacted]

## Notes for reviewers

[Optional: risk areas, open questions, context.]
```
````

Then immediately after, output a second copyable block for the commit message:

````
```
- [short bullet 1 — what changed]
- [short bullet 2 — what changed]
- [short bullet 3 — what changed]
- [short bullet 4 — what changed]
- [short bullet 5 — what changed]
```
````

Label it clearly: **Commit Message Bullets** (pick any 5 of the most important changes, max ~8 words each).

## Quality standards

### Summary

- Lead with **why**, not only **what**.
- Prefer specific outcomes over vague labels ("Fix login timeout" not "Fix bug").
- One primary purpose per PR; if mixed, say so explicitly.

### Changes

- Group related bullets; call out breaking changes and migrations clearly.

### Affected Areas

- List modules, pages, or features a reviewer should open and verify — not just files that changed, but things that could *break* because of the change.
- Think: shared utilities, API contracts, sibling components, routes that depend on changed logic.

### Examples

**Good summary:** Add rate limiting to authentication endpoints to reduce brute-force risk (5 attempts per minute per IP, exponential backoff).

**Weak summary:** Fix auth issues.

**Good changes list:** bullets grouped by Auth, Config, Docs with concrete deltas.

**Weak changes list:** only file names with no intent.

**Good affected areas:** "Settings > Notifications module — uses the same hook that was refactored."

**Weak affected areas:** just listing the changed file paths.

## Edge cases

| Situation | Guidance |
|-----------|------------|
| Large PR | Overview section first; group by feature or area |
| Refactor | State behavior parity; describe structure and rationale |
| Bug fix | Symptom, root cause, fix |
| Dependencies | New packages and why |

## Step 4 — Offer `gh pr create`

After sharing the description, ask whether to open the PR with `gh`.

If yes:

1. Confirm upstream tracking: `git rev-parse --abbrev-ref --symbolic-full-name @{u}` (push with `git push -u origin HEAD` if missing).
2. Warn on uncommitted changes before creating the PR.
3. Create: `gh pr create --title "..." --body "..."` (add `--draft` for draft).

**Options to mention:** create ready PR, create draft, or copy description only for manual paste.

### Error handling

- **`gh` missing:** Point to https://cli.github.com/ or paste description manually.
- **Not authenticated:** Run `gh auth login`.
- **Uncommitted changes:** Warn before `gh pr create`.
