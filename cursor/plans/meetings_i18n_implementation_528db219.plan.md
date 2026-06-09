---
name: Meetings i18n Implementation
overview: Comprehensive i18n implementation for the meetings module -- replacing all hardcoded user-facing strings with translation keys across ~35 component files, constants, and helpers.
todos:
  - id: extend-meetings-ts
    content: "Add all new structured translation keys to meetings.ts (organized by context: list, table, cancelModal, rescheduleModal, remindModal, teamFilter, aiRecommendations, aiTaskCards, meetingInfo, detailActions, sidebar, overview, comments, commentActions, notesModal, summaryModal, contactDetails, insights, analytics, analyticsSummary, analyticsStage, teamMeeting, nextActionModal, constants, history, helper)"
    status: completed
  - id: constants-getters
    content: "Create getter functions in constants/index.ts for: TEAM_MEETING_FILTERS, TEAM_MEETING_TEAMS, MEETING_PROGRESS_OPTIONS, MEETING_STATUS, ANALYTICS_TIME_INTERVALS_OPTIONS, SCORE_DIMENSIONS, COMPANY_DATA, ACTIVITY_LABELS, OBJECT_TYPE_LABEL_MAP, OBJECT_TYPE_SINGULAR, ENRICHMENT_SOURCE, ACTIVITY_VERBS, EVENT_TYPE_LABEL_MAP, MEETING_STATS_EMPTY_MESSAGE, SEVERITY_LEVELS"
    status: completed
  - id: update-helpers
    content: "Update helper/index.ts: getScoreLabel() and getItemTypeFromEventType() to use I18n.t(), translate duration suffixes in getEndTimeOptions()"
    status: completed
  - id: meeting-list-components
    content: "Translate ~13 meeting-list component files: pages/index.tsx, meeting-list/index.tsx, all-meetings.tsx, meeting-table.tsx, meeting-cancel-modal.tsx, reschedule-meeting-modal.tsx, remind-recommendation-modal.tsx, upcoming-meeting.tsx, past-meeting.tsx, ai-recommendations.tsx, follow-up-email-task-card.tsx, reschedule-task-card.tsx, meeting-content-handlers.tsx"
    status: completed
  - id: meeting-info-components
    content: "Translate ~12 meeting-info component files: meeting-tab-details.tsx, meeting-details.tsx, meeting-sidebar.tsx, overview.tsx, comments.tsx, comment-message.tsx, comment-reply-modal.tsx, create-notes-modal.tsx, summary-modal.tsx, contact-details.tsx, meeting-insights.tsx, history-item.tsx, profile-info-card.tsx"
    status: completed
  - id: analytics-components
    content: "Translate ~7 analytics component files: index.tsx, bar-chart.tsx, meeting-analytics-summary.tsx, meeting-feedback.tsx, meeting-over-time.tsx, meeting-score-trend.tsx, meeting-statge-summary.tsx"
    status: completed
  - id: team-meeting-components
    content: "Translate ~3 team-meeting component files: index.tsx, meeting-table.tsx, next-action-modal.tsx"
    status: completed
  - id: recheck-fix-pass
    content: "Re-read every file in the module one by one after initial translation. Find and fix any remaining hardcoded user-facing strings on the spot (add keys to meetings.ts, replace with I18n.t()). Cover: constants, helper, pages, meeting-list/*, meeting-info/*, analytics/*, team-meeting/*"
    status: completed
  - id: final-audit
    content: "Final verification sweep: confirm zero remaining hardcoded strings, no logic/CSS changes, all user-visible text translated, backend data untouched, keys properly structured"
    status: completed
isProject: false
---

# Meetings Module i18n Implementation

## Current State

- Translation file exists at [meetings.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/meetings.ts) with ~250 keys, but many component strings are still hardcoded.
- [common.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/common.ts) has reusable keys (cancel, save, delete, edit, close, etc.).
- [constants/index.ts](applications/sparrow-crm/features/meeting/constants/index.ts) has both hardcoded constants (MEETING_TABS, MEETING_LIST_TABS) and getter functions (getMeetingTabs, getMeetingListTabs) -- but components still use the hardcoded constants.
- [contacts/meetings](applications/sparrow-crm/features/contacts/components/record/tabs/meetings/) tab is already fully translated.
- The [helper/index.ts](applications/sparrow-crm/features/meeting/helper/index.ts) has `getScoreLabel()` and `getItemTypeFromEventType()` with hardcoded labels.

## Approach

### Step 1: Extend meetings.ts Translation Keys

Add new structured keys to [meetings.ts](applications/sparrow-crm/translation/input/sparrowcrm/en/meetings.ts), organized by context:

- **meetings.list** -- Meeting list UI (search placeholder, sort, filter, empty states)
- **meetings.table** -- Table headers (title, date, tags, participants), row actions (view, edit, copy link, reschedule, cancel), prep buttons
- **meetings.cancelModal** -- Cancel modal (dialog label, close, scheduled info, reason, buttons)
- **meetings.rescheduleModal** -- Reschedule modal (dialog label, current time, timezone, buttons)
- **meetings.remindModal** -- Remind recommendation modal (dialog, form labels, buttons)
- **meetings.teamFilter** -- Team filter labels (view by, all teams, filter by)
- **meetings.aiRecommendations** -- AI section (heading, no recs, checklist, add task, remind, dismiss, confirm)
- **meetings.aiTaskCards** -- Follow-up email card (summary prefix, send email, view meeting), reschedule card (accept, view in calendar)
- **meetings.meetingInfo** -- Meeting info tabs (overview, tasks, notes, activities, comments, insights), meeting detail tabs label
- **meetings.detailActions** -- Join meeting, view recording, dropdown, edit
- **meetings.sidebar** -- Back, navigate to meeting
- **meetings.overview** -- Conversation summary, attendees info, touchpoint labels (sent email, was added), no description
- **meetings.comments** -- Create/delete/update success/error toasts, no comments, add comment placeholder, delete confirmation, reply modal strings
- **meetings.commentActions** -- Options, edit, delete, reply, view replies, comment deleted
- **meetings.notesModal** -- Untitled note, create/update note toasts, expand, modal titles, close
- **meetings.summaryModal** -- Dialog label, heading, close, no summary
- **meetings.contactDetails** -- Field labels (LinkedIn, Fit Score, Company, Industry, Region, Lifecycle Stage, Decision Maker, Tags, Attendees), section headings (About the company, Company Summary, Latest Company News, Meeting Information, Tools Used)
- **meetings.insights** -- Meeting Score, Score Breakdown, Talk Ratio, Buying Intent Signals, Red Flags Detected
- **meetings.analytics** -- No analytics, meetings over time, activity trends, sentiment labels, scorecard labels, feedback section
- **meetings.analyticsSummary** -- Total meetings, avg meeting score, talk to listen ratio
- **meetings.analyticsStage** -- Meetings in deal stage, distribution of next actions, stage names, status labels
- **meetings.teamMeeting** -- Empty state, table headers (Fit Score, Meeting Score, Organiser, Meeting Sentiment, Next Actions), row actions, sentiment labels, toasts
- **meetings.nextActionModal** -- Dialog label, heading, send email, close
- **meetings.constants** -- All constant labels that need getter functions (see Step 2)
- **meetings.history** -- System user label
- **meetings.helper** -- Score labels (No Score, Great Going, Good Progress, Needs Improvement, Needs Attention), item types (comment, task, note, attribute value, file, call), duration suffixes (hr, hrs, min)

Reuse keys from common.ts where the content matches exactly (e.g., `common.cancel`, `common.edit`, `common.delete`, `common.close`, `common.title`, `common.filter`).

### Step 2: Create Getter Functions for Constants

In [constants/index.ts](applications/sparrow-crm/features/meeting/constants/index.ts), add getter functions for all constants with hardcoded labels:

- `getTeamMeetingFilters()` -- translates TEAM_MEETING_FILTERS labels
- `getTeamMeetingTeams()` -- translates TEAM_MEETING_TEAMS labels
- `getMeetingProgressOptions()` -- translates MEETING_PROGRESS_OPTIONS labels
- `getMeetingStatus()` -- translates MEETING_STATUS labels
- `getAnalyticsTimeIntervalsOptions()` -- translates ANALYTICS_TIME_INTERVALS_OPTIONS labels
- `getScoreDimensions()` -- translates SCORE_DIMENSIONS labels
- `getCompanyData()` -- translates COMPANY_DATA labels
- `getActivityLabels()` -- translates ACTIVITY_LABELS labels
- `getObjectTypeLabelMap()` -- translates OBJECT_TYPE_LABEL_MAP labels
- `getObjectTypeSingular()` -- translates OBJECT_TYPE_SINGULAR labels
- `getEnrichmentSource()` -- translates ENRICHMENT_SOURCE labels
- `getActivityVerbs()` -- translates ACTIVITY_VERBS labels
- `getEventTypeLabelMap()` -- translates EVENT_TYPE_LABEL_MAP
- `getMeetingStatsEmptyMessage()` -- translates MEETING_STATS_EMPTY_MESSAGE
- `getSeverityLevels()` -- translates SEVERITY_LEVELS

Keep the original constants for non-label usage (e.g., values, event type keys). The getter functions return translated labels using `I18n.t()`.

### Step 3: Update Helper Functions

In [helper/index.ts](applications/sparrow-crm/features/meeting/helper/index.ts):

- `getScoreLabel()` -- use `I18n.t("meetings.helper.noScore")` etc.
- `getItemTypeFromEventType()` -- use `I18n.t("meetings.helper.comment")` etc.
- Duration formatting functions (`getEndTimeOptions`) -- translate "hr", "hrs", "min" suffixes

### Step 4: Update Components (file by file)

For each component file, replace hardcoded strings with `I18n.t()` (imported from `@i18n/setup`). Do NOT use the `useTranslation()` hook -- the app already re-renders on language change at a higher level, so `I18n.t()` calls will naturally return the correct language.

**Meeting List group (~12 files):**

- [pages/index.tsx](applications/sparrow-crm/features/meeting/pages/index.tsx) -- Use getMeetingTabs() via useMemo with i18n.language dep; translate aria-labels, button text
- [meeting-list/index.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/index.tsx) -- Use getMeetingListTabs() via useMemo; translate search placeholder, aria-labels
- [meeting-list/all-meetings.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/all-meetings.tsx) -- Translate toast messages, empty state, button text
- [meeting-list/meeting-table.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/meeting-table.tsx) -- Translate table headers, row actions, toasts, aria-labels
- [meeting-list/meeting-cancel-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/meeting-cancel-modal.tsx) -- Translate modal text, toasts, placeholders
- [meeting-list/reschedule-meeting-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/reschedule-meeting-modal.tsx) -- Translate modal text, toasts, buttons
- [meeting-list/remind-recommendation-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/remind-recommendation-modal.tsx) -- Translate form labels, placeholders, buttons
- [meeting-list/upcoming-meeting.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/upcoming-meeting.tsx) -- Use getTeamMeetingFilters/getTeamMeetingTeams via useMemo; translate filter labels
- [meeting-list/past-meeting.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/past-meeting.tsx) -- Same as upcoming-meeting
- [meeting-list/ai-recommendations.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/ai-recommendations.tsx) -- Translate section heading, empty state, checklist, menu items, confirmation dialog
- [meeting-list/ai-task-cards/follow-up-email-task-card.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/ai-task-cards/follow-up-email-task-card.tsx) -- Translate button text, aria-labels
- [meeting-list/ai-task-cards/reschedule-task-card.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/ai-task-cards/reschedule-task-card.tsx) -- Translate button text, aria-labels
- [meeting-list/meeting-content-handlers.tsx](applications/sparrow-crm/features/meeting/components/meeting-list/meeting-content-handlers.tsx) -- Translate button text, aria-labels

**Meeting Info group (~15 files):**

- [meeting-info/meeting-tab-details.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/meeting-tab-details.tsx) -- Translate all tab labels, aria-labels
- [meeting-info/meeting-details.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/meeting-details.tsx) -- Translate join, recording, edit buttons
- [meeting-info/meeting-sidebar.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/meeting-sidebar.tsx) -- Translate back button, navigation aria-labels
- [meeting-info/overview.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/overview.tsx) -- Translate touchpoint labels, attendees, no description
- [meeting-info/comments.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/comments.tsx) -- Translate all toast messages, empty state, delete confirmation, buttons
- [meeting-info/comment-message.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/comment-message.tsx) -- Translate edit/delete/reply actions
- [meeting-info/comment-reply-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/comment-reply-modal.tsx) -- Translate all modal strings, toasts, actions
- [meeting-info/create-notes-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/create-notes-modal.tsx) -- Translate modal titles, toasts, buttons, placeholder
- [meeting-info/summary-modal.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/summary-modal.tsx) -- Translate heading, close, no summary
- [meeting-info/contact-details.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/contact-details.tsx) -- Translate all field labels and section headings
- [meeting-info/meeting-insights.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/meeting-insights.tsx) -- Translate section headings, use getScoreDimensions via useMemo
- [meeting-info/history-item.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/history-item.tsx) -- Translate "System" user name
- [meeting-info/profile-info-card.tsx](applications/sparrow-crm/features/meeting/components/meeting-info/profile-info-card.tsx) -- Remove "dsds" debug text

**Analytics group (~6 files):**

- [analytics/index.tsx](applications/sparrow-crm/features/meeting/components/analytics/index.tsx) -- Translate empty state
- [analytics/bar-chart.tsx](applications/sparrow-crm/features/meeting/components/analytics/bar-chart.tsx) -- Translate legend name, day labels
- [analytics/meeting-analytics-summary.tsx](applications/sparrow-crm/features/meeting/components/analytics/meeting-analytics-summary.tsx) -- Translate summary labels
- [analytics/meeting-feedback.tsx](applications/sparrow-crm/features/meeting/components/analytics/meeting-feedback.tsx) -- Translate headings, descriptions, strengths/areas labels
- [analytics/meeting-over-time.tsx](applications/sparrow-crm/features/meeting/components/analytics/meeting-over-time.tsx) -- Translate headings, time filter, sentiment, scorecard labels
- [analytics/meeting-score-trend.tsx](applications/sparrow-crm/features/meeting/components/analytics/meeting-score-trend.tsx) -- Translate heading
- [analytics/meeting-statge-summary.tsx](applications/sparrow-crm/features/meeting/components/analytics/meeting-statge-summary.tsx) -- Translate headings, stage names, status labels

**Team Meeting group (~3 files):**

- [team-meeting/index.tsx](applications/sparrow-crm/features/meeting/components/team-meeting/index.tsx) -- Translate empty state
- [team-meeting/meeting-table.tsx](applications/sparrow-crm/features/meeting/components/team-meeting/meeting-table.tsx) -- Translate table headers, actions, toasts, sentiment labels
- [team-meeting/next-action-modal.tsx](applications/sparrow-crm/features/meeting/components/team-meeting/next-action-modal.tsx) -- Translate modal strings

### Step 5: useMemo Pattern for Constants

In every component that uses getter functions for constants, wrap in useMemo with `I18n.language` dependency:

```typescript
import { I18n } from "@i18n/setup";

const meetingTabs = useMemo(() => getMeetingTabs(), [I18n.language]);
const meetingListTabs = useMemo(() => getMeetingListTabs(), [I18n.language]);
const teamFilters = useMemo(() => getTeamMeetingFilters(), [I18n.language]);
```

### Step 6: Full Re-check and Fix Pass

After all translation work is done, go through **every single file** in the meetings module again, one by one. For each file:

1. Read the file in its current (modified) state
2. Scan for ANY remaining hardcoded user-facing strings (toasts, placeholders, tooltips, aria-labels, button text, headings, labels, empty states, confirmation messages, etc.)
3. If any hardcoded text is found that satisfies the translation rules (i.e., it is user-visible and NOT backend data), fix it on the spot -- add the missing key to meetings.ts (or reuse from common.ts) and replace the hardcoded string with `I18n.t()`
4. Verify no logic or CSS was accidentally changed

File order for re-check:

- `constants/index.ts`, `helper/index.ts`
- `pages/index.tsx`
- All `meeting-list/` files
- All `meeting-info/` files
- All `analytics/` files
- All `team-meeting/` files

### Step 7: Final Audit

After the re-check pass, do a final verification sweep to confirm:

- No remaining hardcoded user-facing strings anywhere in the module
- No logical or CSS changes were introduced
- All toasts, placeholders, tooltips, aria-labels, and visible text use translation keys
- Backend data (meeting titles, descriptions, user names from API) remains untouched
- All new keys in meetings.ts are properly structured and named by local context

## Key Rules

- Use `I18n.t()` from `@i18n/setup` everywhere -- do NOT use the `useTranslation()` hook
- The app already re-renders on language change at a higher level, so `I18n.t()` calls naturally pick up the new language
- For constants consumed via getter functions, use `useMemo(() => getXxx(), [I18n.language])` so memoized values refresh on language change
- Reuse existing `common.ts` keys where content matches exactly
- Keep translation keys structured by local context for easy future content editing
- Do NOT translate backend data (names, titles from API responses)
- Do NOT change any logic or CSS
- TIME_INTERVAL labels are time format strings -- the existing `getTimeInterval()` getter handles AM/PM translation via `common.time.am`/`common.time.pm`
