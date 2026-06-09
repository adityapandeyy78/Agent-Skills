---
name: Fix useEffect dependencies
overview: Add userSettings to the useEffect dependency array so userDetails gets properly initialized when userSettings data arrives.
todos:
  - id: "1"
    content: Add userSettings to useEffect dependency array in user-profile.tsx
    status: completed
isProject: false
---

## Issue Summary

The `useEffect` hook that initializes `userDetails` state only has `[isLoading]` in its dependency array. This means when `userSettings` data arrives from the API (after loading completes), the effect doesn't re-run because `isLoading` is already `false`. As a result, `userDetails` state may not be properly synchronized with `userSettings`, causing `hasChanges()` to incorrectly return `false` when comparing values.

## Root Cause

In `user-profile.tsx` lines 140-154:

```typescript
useEffect(() => {
  if (!isLoading) {
    setUserDetails({
      language: userSettings?.LANGUAGE,
      ...
    });
  }
}, [isLoading]);  // Missing userSettings dependency
```

The comparison in `hasChanges()` compares:

- `userDetails.language.value` (from state, may be stale/undefined)
- `userSettings.LANGUAGE.value` (from API)

If `userSettings` arrives after the initial render (when `isLoading` becomes false), `userDetails` won't be updated, causing the comparison to fail.

## Fix

Add `userSettings` to the useEffect dependency array on line 154:

```typescript
}, [isLoading, userSettings]);
```

## Files to Modify

1. **applications/sparrow-crm/features/profile-settings/components/user-profile/user-profile.tsx**
   - Change line 154 from `}, [isLoading]);` to `}, [isLoading, userSettings]);`

## Verification

After the fix:

1. Load the profile settings page
2. Change the language from the dropdown
3. Click "Save Changes"
4. The API should fire and save the changes successfully
