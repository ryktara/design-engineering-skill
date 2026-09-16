## design-engineering search: Sync status is a spinner that never says what is happening.
status=CONFIDENT modes=['audit', 'refactor'] platforms={} inputs={} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'anti-pattern'] unmet=['interaction'] diversity=0.67
MISSING: platform: audit targets differ by platform; not stated

### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.567 · engineering-practice
Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- use when: Field, travel, and public-venue apps; anything used with poor connectivity; any screen that writes data.
- avoid when: Read-only always-online desktop tools where connectivity loss is exceptional (still show an error, not a blank).
- why: lexical 0.655, structural 0.46 (mode audit)

### Desktop status bar as the persistent feedback surface, with next-error navigation  `desktop-status-bar-and-error-navigation`  [rule/feedback; component/platform] score 0.427 · platform-standard
One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width.
- use when: Data-entry and workbench windows where validation, selection and sync state must be visible without dialogs or toasts.
- avoid when: Consumer apps without a persistent window chrome; mobile.
- why: lexical 0.449, structural 0.4 (mode audit)

### Never colour alone  `a11y-color-not-only`  [rule/accessibility; accessibility] score 0.419 · accessibility-requirement
Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint.
- use when: Status, validation errors, chart series, selected/active states, required fields, links inside text.
- avoid when: Never skip.
- why: lexical 0.352, structural 0.5 (mode audit)

### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.344 · heuristic
Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- use when: Status, category, or count must be scannable in lists and headers (Open/Closed, New, 3 unread).
- avoid when: As decoration on everything; when more than two badges per item appear, the design has become noisy.
- incompatible with: metadata-minimal, layout-immersive-rails
- why: lexical 0.405, structural 0.18 (secondary mode)

### Announce dynamic status changes  `a11y-live-status`  [rule/feedback; component] score 0.339 · accessibility-requirement
Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable.
- use when: Toasts, saving/saved indicators, cart counts, filter result counts, chat messages, async loading completion.
- avoid when: Do not announce every keystroke result; do not move focus for non-blocking status.
- why: lexical 0.208, structural 0.5 (mode audit)

### Saving, saved, autosave, session expiry, and permission-denied states  `states-persistence-and-session`  [rule/states; component/platform] score 0.284 · heuristic
Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry on a personal device (restore the draft after re-authentication; on shared or public screens clear it instead); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default.
- use when: Forms and editors longer than a minute, multi-step flows, authenticated sessions with timeouts, screens whose data depends on permissions.
- avoid when: Public kiosks and shared screens: there the session is cleared on idle and nothing is restored (see shared-device-privacy).
- why: lexical 0.141, structural 0.46 (mode audit)

### One clear focal point per screen  `layout-hierarchy-one-thing`  [rule/layout; layout] score 0.284 · heuristic
Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title.
- use when: Designing any screen; reviewing 'it looks busy'.
- avoid when: Never give three elements the same maximum emphasis; never make the primary content compete with chrome.
- why: lexical 0.107, structural 0.5 (mode audit)

### Choosing a visual style before understanding product, user, and platform  `anti-style-before-product`  [antipattern/process; anti-pattern] score 0.258 · heuristic
Order of decisions: task and user → environment and input → density and navigation → layout → components → then type, colour, surface, motion. Visual style is downstream of structure. Record the KNOWN/INFERRED/MISSING ledger before choosing a look.
- use when: Any request answered with 'glassmorphism + purple gradient + Inter' (or any style) before asking who uses it, where, with what input, at what density.
- avoid when: When the user explicitly specifies the style, follow it, but still check platform fit.
- why: lexical 0.06, structural 0.5 (mode audit)

### Form labels, errors, and recovery  `a11y-forms-errors`  [rule/forms; component] score 0.252 · accessibility-requirement
Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers.
- use when: Every form: visible labels, required markers in text, inline errors linked to fields, error summary for long forms, no data loss on error.
- avoid when: Never validate on every keystroke for fields the user has not finished; validate on blur and on submit.
- why: lexical 0.05, structural 0.5 (mode audit)

### Native accessibility semantics (mobile/desktop)  `a11y-native-semantics`  [rule/accessibility; accessibility/platform] score 0.241 · accessibility-requirement
Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code.
- use when: Custom composables/views/controls, merged semantics for cards, live regions for status, headings in long screens.
- avoid when: Never build a tappable Box/View/Border without a role and name.
- why: lexical 0.062, structural 0.46 (mode audit)

### Moderate metadata with a hierarchy  `metadata-moderate`  [pattern/metadata; layout] score 0.237 · heuristic
Rank facts: title, then the deciding fact (price/status), then supporting facts in a muted style; status via badge + text; align numbers; no icon per fact.
- use when: Lists and cards where 3–4 facts help the choice (price, rating, date, status) and can be typographically ranked.
- avoid when: When facts exceed four (use a table or detail) or when only one matters.
- incompatible with: metadata-minimal, metadata-rich
- why: lexical 0.075, structural 0.28 (secondary mode)

### Cards inside cards, everything in a rounded box  `anti-card-everything`  [antipattern/generic-ai; anti-pattern] score 0.234 · heuristic
Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid.
- use when: Reviewing any layout where sections, lists, forms, and even single lines are wrapped in bordered/elevated containers.
- avoid when: A card is fine when the item is a discrete tappable object or needs elevation (drag, overlay).
- why: lexical 0.017, structural 0.5 (mode audit)

Filtered out: mobile-field-use (environment ['gloves', 'outdoor'] not in request)
