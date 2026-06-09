---
name: dayjs locale impact analysis
overview: A comprehensive analysis of the impact, pitfalls, and mitigation strategy for enabling global dayjs locale translation in the sparrow-crm codebase.
todos:
  - id: wire-dayjs-locale
    content: Add dayjs locale sync to setLocale thunk in i18n/setup.ts
    status: pending
  - id: fix-parsing-calls
    content: Add explicit 'en' locale to 3 high-risk customParseFormat parse calls
    status: pending
  - id: fix-comparison-pattern
    content: Fix AM/PM string comparison in meeting/helper/index.ts
    status: pending
  - id: cleanup-manual-helper
    content: Remove getTranslatedDayName() helper from due-date-selection.tsx, revert to dayjs().format('ddd')
    status: pending
  - id: verify-locale-mapping
    content: Verify i18n language codes match dayjs locale codes for all supported languages
    status: pending
isProject: false
---

# Global dayjs Locale Translation: Impact Analysis

## Current State

- dayjs has **no locale configured** anywhere in the codebase. It always outputs English.
- The i18n `setLocale` thunk in [`applications/sparrow-crm/i18n/setup.ts`](applications/sparrow-crm/i18n/setup.ts) updates `i18next` but never touches dayjs.
- **60+ display-only** format calls use locale-sensitive tokens (`MMM`, `ddd`, `dddd`, `MMMM`, `A`).
- **50+ API/comparison** format calls use locale-neutral tokens (`YYYY-MM-DD`, ISO strings).

## What Locale Translation Would Fix

Setting `dayjs.locale(...)` when language changes would automatically translate:

- Month abbreviations: `MMM` ("Mar" -> localized) in **30+ files**
- Day abbreviations: `ddd` ("Mon" -> localized) in **7+ files**
- Full day/month names: `dddd`, `MMMM` in a few meeting files
- AM/PM: `A` token in **25+ files**

This would **replace the manual `getTranslatedDayName()` helper** already added to [`due-date-selection.tsx`](applications/sparrow-crm/features/sequences/components/sequence-editor/nodes/task/due-date-selection.tsx) with a single global solution.

---

## Risk Assessment

### NO RISK: API Payloads (Safe)

All dates sent to the backend use locale-neutral formats. These are **completely unaffected** by locale changes:

- `format("YYYY-MM-DD")` - numeric-only, locale-independent
- `.toISOString()` / `.utc().format(...)` - always English/ISO
- Files: filter components, create-task-modal, create-field-modal, date.tsx, advanced-filter.tsx

### HIGH RISK: AM/PM Parsing with `customParseFormat`

Three files **parse** date strings using the `"h:mm A"` format token, where the input values are **hardcoded English** ("9:00 AM", "12:00 PM"):

- **[`features/meeting/helper/index.ts`](applications/sparrow-crm/features/meeting/helper/index.ts) line 77**:
  `dayjs(\`${selectedDate} ${opt.value}\`, "YYYY-MM-DD h:mm A")`
`opt.value`comes from`TIME_INTERVAL`constants, always English like`"12:00 AM"`.

- **[`features/profile-settings/helpers/index.ts`](applications/sparrow-crm/features/profile-settings/helpers/index.ts) line 13**:
  `dayjs(timeStr, "h:mm A")`
  `timeStr` comes from `getTimesOptions().value`, always English like `"9:00 AM"`.

- **[`features/meeting/components/meeting-list/create-meeting-modal.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/create-meeting-modal.tsx) lines 491-493**:
  `dayjs(\`${tempSelectedDate} ${prev.startTime.value}\`, "YYYY-MM-DD h:mm A")`

**What breaks:** If locale is set to (e.g.) French, the `A` token in the parse format expects the locale's meridiem representation, but the input is still `"AM"/"PM"` in English. The parse would produce an **Invalid Date**.

**Fix:** Force English locale on these specific parse calls:

```typescript
dayjs(`${selectedDate} ${opt.value}`, "YYYY-MM-DD h:mm A", "en");
```

dayjs's `customParseFormat` accepts a locale as the 3rd argument.

### MEDIUM RISK: AM/PM in Display-then-Compare Patterns

- **[`features/meeting/helper/index.ts`](applications/sparrow-crm/features/meeting/helper/index.ts) lines 198-202**:
  Uses `format("hh:mm A")` to compare formatted time strings. If locale changes AM/PM, the comparison with English-origin strings would fail silently.

**Fix:** Use `.locale('en').format(...)` for comparison logic, or compare with `.valueOf()` / `.isSame()` instead of string matching.

### LOW RISK: Display-Only Formatting (Desired Behavior)

All other `format("DD MMM")`, `format("ddd, D MMM")`, `format("h:mm A")` calls that are **purely display** would automatically show translated output. This is the **intended behavior** and requires no changes.

---

## Implementation Strategy

### Step 1: Wire dayjs locale into `setLocale` thunk

In [`applications/sparrow-crm/i18n/setup.ts`](applications/sparrow-crm/i18n/setup.ts), after `i18nInstance.changeLanguage()`:

```typescript
import "dayjs/locale/en"; // always available as fallback

const setLocale = createAsyncThunk("i18n/setLocale", async (languageCode) => {
  // ... existing code ...
  await i18nInstance.changeLanguage(languageCode);

  // Sync dayjs locale
  try {
    await import(`dayjs/locale/${languageCode}`);
    dayjs.locale(languageCode);
  } catch {
    dayjs.locale("en"); // fallback
  }

  return languageCode;
});
```

### Step 2: Fix the 3 high-risk parsing calls

Add explicit `'en'` locale to parse calls:

- `features/meeting/helper/index.ts`: `dayjs(..., "YYYY-MM-DD h:mm A", 'en')`
- `features/profile-settings/helpers/index.ts`: `dayjs(timeStr, "h:mm A", 'en')`
- `features/meeting/components/meeting-list/create-meeting-modal.tsx`: `dayjs(..., "YYYY-MM-DD h:mm A", 'en')`

### Step 3: Fix the medium-risk comparison pattern

In `features/meeting/helper/index.ts` lines 198-202, use `.locale('en').format(...)` or switch to time-value-based comparison.

### Step 4: Remove manual helper

Remove `getTranslatedDayName()` from `due-date-selection.tsx` and revert to `dayjs().format("ddd")` which will now auto-translate.

---

## Pitfalls and Drawbacks

- **Bundle size**: Each dayjs locale file is ~1-3 KB. Dynamic import keeps it small but adds an async load.
- **Locale mapping**: Your i18n language codes must match dayjs locale codes (e.g., `"en"` -> `"en"`, `"fr"` -> `"fr"`, `"pt-BR"` -> `"pt-br"`). Mismatches silently fall back to English.
- **SSR/initial render**: If dayjs locale loads async, the first render might flash English before switching. Mitigate by loading the locale before the app renders (in `App.tsx`).
- **Testing**: Unit tests that assert date strings like `"DD MMM"` will need locale awareness.
- **AM/PM varies by locale**: Some locales don't have AM/PM at all (they use 24h format). This means `format("h:mm A")` might produce unexpected output in some locales. You may want to use `format("HH:mm")` (24h) for those locales or keep AM/PM display explicit.

---

## Summary: Will It Break Backend Communication?

**No.** All API payloads use `YYYY-MM-DD`, ISO strings, or `.toISOString()` -- purely numeric, locale-independent formats. The backend will receive identical data regardless of the frontend locale.

The only required fixes are **3-4 specific parsing/comparison calls** that use English AM/PM strings with `customParseFormat`. These need an explicit `'en'` locale parameter -- a surgical, low-effort change.

## Scope of Changes

- **1 file** to wire up dayjs locale (i18n/setup.ts)
- **3 files** to fix high-risk parsing (meeting helper, profile-settings helper, create-meeting-modal)
- **1 file** to fix medium-risk comparison (meeting helper)
- **1 file** to clean up manual helper (due-date-selection.tsx)
- **Total: ~6 files, ~20 lines changed**
