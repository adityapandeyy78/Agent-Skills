---
name: Meetings Module i18n
overview: Implement comprehensive i18n for the entire meetings module by adding translation keys, converting all hardcoded user-facing strings to use `t()` / `I18n.t()`, creating getter functions for constants, and wrapping constant usage in `useMemo` with `i18n.language` dependency.
todos: []
isProject: false
---

# Meetings Module i18n Implementation

## Current State

- **Translation file exists** at [`meetings.ts`](applications/sparrow-crm/translation/input/sparrowcrm/en/meetings.ts) with ~250 keys
- **Constants file** at [`constants/index.ts`](applications/sparrow-crm/features/meeting/constants/index.ts) has some getter functions (`getMeetingTabs`, `getMeetingListTabs`, `getTimeInterval`, `getFallbackInsightsData`, `getMeetingRecordTabs`) but ~15 constants still have hardcoded labels
- **Components use hardcoded constants** (e.g., `MEETING_TABS.ALL_MEETINGS.label` instead of `getMeetingTabs()`)
- **~200+ hardcoded strings** remain across ~35 component files
- **Contacts meetings tab** (`contacts/components/record/tabs/meetings/`) is already fully translated

## Approach

- Reuse existing keys from `common.ts` where content matches exactly (e.g., `common.cancel`, `common.delete`, `common.close`, `common.title`, etc.)
- Name new keys by local context (e.g., `meetings.comments.postComment`, `meetings.analytics.meetingsOverTime`)
- Keep the keys structured in nested objects in `meetings.ts` by feature area
- Do NOT change any logic or CSS -- strictly translation work only
- Backend-sourced content (dynamic data, API responses) stays as-is

---

## Phase 1: Update Translation Keys File

**File:** [`meetings.ts`](applications/sparrow-crm/translation/input/sparrowcrm/en/meetings.ts)

Add new structured key sections:

- `meetings.meetingList` -- search, sort, filter labels, tab aria-labels
- `meetings.table` -- column headers (Title, Date, Tags, Participants), row actions, copy link toasts
- `meetings.cancelModal` -- dialog labels, toast messages, form fields
- `meetings.rescheduleModal` -- dialog labels, toast messages, form fields
- `meetings.remindModal` -- form labels, placeholders, button text
- `meetings.teamFilter` -- "View by", "All Teams", team filter labels
- `meetings.aiRecommendations` -- section headings, empty states, checklist, actions, dismiss confirmation
- `meetings.aiTaskCards` -- follow-up email card, reschedule card button text
- `meetings.meetingContentHandlers` -- accept, view in calendar, send email
- `meetings.meetingDetails` -- join, view recording, dropdown actions
- `meetings.meetingSidebar` -- back, navigate
- `meetings.meetingTabDetails` -- tab labels (Overview, Tasks, Notes, Activities, Comments, Insights)
- `meetings.overviewSection` -- touchpoint labels, attendees info, conversation summary, description fallback
- `meetings.commentsSection` -- toasts, empty state, delete confirmation, post/cancel buttons
- `meetings.commentMessage` -- options, edit, delete, reply, comment deleted
- `meetings.commentReplyModal` -- dialog labels, toasts, reply section
- `meetings.createNotesModal` -- dialog labels, toasts, untitled note, button text
- `meetings.emailViewModal` -- (sample data strings are demo content, may skip)
- `meetings.insights` -- section headings (Meeting Score, Score Breakdown, Talk Ratio, Buying Intent, Red Flags)
- `meetings.summaryModal` -- dialog label, heading, close, no summary
- `meetings.contactDetailsSection` -- all field labels (LinkedIn, Fit Score, Company, etc.), section headings
- `meetings.analytics` -- empty state, chart labels, summary labels, feedback section, scorecard, sentiment, stage summary
- `meetings.teamMeeting` -- empty state, table headers, toasts, row actions, sentiment labels, next actions
- `meetings.nextActionModal` -- dialog labels, button text
- `meetings.constants` -- all constant labels (filters, teams, progress options, status, score dimensions, activity labels, enrichment source, etc.)
- `meetings.helper` -- score labels, item type labels, duration labels (hr/min)

---

## Phase 2: Create Getter Functions for Constants

**File:** [`constants/index.ts`](applications/sparrow-crm/features/meeting/constants/index.ts)

Create getter functions for every constant with user-facing labels:

| Existing Constant | New Getter Function |
|---|---|
| `TEAM_MEETING_FILTERS` | `getTeamMeetingFilters()` |
| `TEAM_MEETING_TEAMS` | `getTeamMeetingTeams()` |
| `MEETING_PROGRESS_OPTIONS` | `getMeetingProgressOptions()` |
| `MEETING_STATUS` (unused export) | `getMeetingStatus()` |
| `ANALYTICS_TIME_INTERVALS_OPTIONS` | `getAnalyticsTimeIntervalsOptions()` |
| `SCORE_DIMENSIONS` | `getScoreDimensions()` |
| `COMPANY_DATA` | `getCompanyData()` |
| `ACTIVITY_LABELS` | `getActivityLabels()` |
| `ACTIVITY_VERBS` | `getActivityVerbs()` |
| `OBJECT_TYPE_LABEL_MAP` | `getObjectTypeLabelMap()` |
| `OBJECT_TYPE_SINGULAR` | `getObjectTypeSingular()` |
| `EVENT_TYPE_LABEL_MAP` | `getEventTypeLabelMap()` |
| `ENRICHMENT_SOURCE` | `getEnrichmentSource()` |
| `SEVERITY_LEVELS` | `getSeverityLevels()` |
| `MEETING_STATS_EMPTY_MESSAGE` | `getMeetingStatsEmptyMessage()` |

Each getter will use `I18n.t("meetings.constants.xxx")` to resolve labels.

**File:** [`helper/index.ts`](applications/sparrow-crm/features/meeting/helper/index.ts)

Convert `getScoreLabel()` and `getItemTypeFromEventType()` to use `I18n.t()`.

---

## Phase 3: Update Components (file by file)

For each component:
1. Import `useTranslation` (or use existing `I18n` import)
2. Replace hardcoded strings with `t("meetings.xxx")` or `I18n.t("meetings.xxx")`
3. For constants used from getters, wrap in `useMemo` with `i18n.language` as dependency
4. Reuse `common.ts` keys where content matches exactly

### Meeting List Components (~12 files)

- [`pages/index.tsx`](applications/sparrow-crm/features/meeting/pages/index.tsx) -- Replace `MEETING_TABS` with `getMeetingTabs()` via useMemo, translate aria-labels, button text, `ANALYTICS_TIME_INTERVALS_OPTIONS` via getter
- [`meeting-list/index.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/index.tsx) -- Replace `MEETING_LIST_TABS` with `getMeetingListTabs()` via useMemo, translate search placeholder, aria-labels
- [`all-meetings.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/all-meetings.tsx) -- Toast messages, empty state text, connector buttons
- [`meeting-table.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/meeting-table.tsx) -- Column headers, row actions, copy link toasts, prep meeting labels
- [`meeting-cancel-modal.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/meeting-cancel-modal.tsx) -- Toasts, dialog labels, form fields, buttons
- [`reschedule-meeting-modal.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/reschedule-meeting-modal.tsx) -- Toasts, dialog labels, form fields, buttons
- [`remind-recommendation-modal.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/remind-recommendation-modal.tsx) -- All form labels, placeholders, buttons
- [`upcoming-meeting.tsx`](applications/sparrow-crm/features/meeting/components/meeting-list/upcoming-meeting.tsx) -- Team filter dropdown, "