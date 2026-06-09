---
name: Fix duplicate imports in axios.ts
overview: Remove duplicate JSONBigInt import and JSONBigIntParser declaration in axios.ts that's causing API calls to fail.
todos:
  - id: "1"
    content: Remove duplicate JSONBigInt import and JSONBigIntParser declaration from axios.ts
    status: pending
  - id: "2"
    content: Verify the file has no duplicate code remaining
    status: pending
isProject: false
---

## Issue Summary

The `applications/sparrow-crm/common/utils/axios.ts` file has duplicate imports and variable declarations that are causing JavaScript runtime errors, breaking the axios configuration and causing all API calls (including language switching) to fail with "Failed to save changes".

## Root Cause

Lines 6-15 contain duplicate code:

- Line 6: `import JSONBigInt from "json-bigint";`
- Lines 9-10: `const JSONBigIntParser = JSONBigInt({ storeAsString: true });`
- Line 12: `import JSONBigInt from "json-bigint";` (DUPLICATE)
- Lines 15-16: `const JSONBigIntParser = JSONBigInt({ storeAsString: true });` (DUPLICATE)

## Fix

Remove the duplicate import and declaration (lines 12-15), keeping only the first occurrence.

## Files to Modify

1. **applications/sparrow-crm/common/utils/axios.ts**
   - Remove lines 12-15 (the duplicate import and declaration)
   - Keep lines 1-10 and 17 onwards intact

## Verification

After the fix:

1. The axios.ts file should have only one `import JSONBigInt` statement
2. The axios.ts file should have only one `JSONBigIntParser` constant declaration
3. API calls should work correctly
4. Language switching should work from the profile settings
