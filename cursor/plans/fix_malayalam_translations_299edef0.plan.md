---
name: Fix Malayalam translations
overview: Add missing sequences.ts and table.ts files to the Malayalam (ml) translation output folder to fix language switching errors.
todos:
  - id: "1"
    content: Create sequences.ts with Malayalam translations in output/ml/
    status: pending
  - id: "2"
    content: Create table.ts with Malayalam translations in output/ml/
    status: pending
  - id: "3"
    content: Update ml/index.ts to export sequences and table modules
    status: pending
  - id: "4"
    content: Verify fix by checking file count matches other languages
    status: pending
isProject: false
---

## Issue Summary

The Malayalam (ml) translation folder is missing `sequences.ts` and `table.ts` files compared to other languages. This causes language switching to fail with "Failed to save changes" / "Unexpected error occurred" errors.

## Files to Modify

1. **Create** `applications/sparrow-crm/translation/output/ml/sequences.ts`
   - Copy structure from existing translation (e.g., ar/sequences.ts)
   - Include Malayalam translations for all sequence-related strings
   - Must export `sequences` constant matching the filename

2. **Create** `applications/sparrow-crm/translation/output/ml/table.ts`
   - Copy structure from existing translation (e.g., ar/table.ts)
   - Include Malayalam translations for all table-related strings
   - Must export `table` constant matching the filename

3. **Update** `applications/sparrow-crm/translation/output/ml/index.ts`
   - Add exports for the new modules:
     - `export * from "./sequences";`
     - `export * from "./table";`
   - Ensure file naming convention matches existing exports (no `.ts` extension)

## Verification Steps

After making changes:

1. Verify `ml` folder now has 17 files (same as other languages)
2. Verify `ml/index.ts` exports match the pattern in `ar/index.ts`
3. Test language switching to Malayalam from profile settings

## Reference Files

- Source structure: `applications/sparrow-crm/translation/input/sparrowcrm/en/sequences.ts` and `table.ts`
- Working example: `applications/sparrow-crm/translation/output/ar/sequences.ts` and `table.ts`
- Current broken index: `applications/sparrow-crm/translation/output/ml/index.ts`
