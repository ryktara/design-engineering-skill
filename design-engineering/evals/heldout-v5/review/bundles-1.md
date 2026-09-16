### hv5-g01-001
**Prompt:** Need a new onboarding flow for the loan app, three steps, nothing fancy.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g01-002
**Prompt:** Building a screen from scratch where warehouse pickers confirm a scanned bin location.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Operational workbench** — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-003
**Prompt:** We want a dashboard for the ward nurses to see who's due for meds next.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [OPTIONAL NOTES] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g01-004
**Prompt:** Sketch out a first-run experience for the fitness tracker, no accounts yet.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_

### hv5-g01-005
**Prompt:** Add a new tab for comparing two insurance quotes side by side.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CORE] **Rich metadata (operational)** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane. _(covers: visual hierarchy with one focal point, tabular figures and numeric alignment)_
- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-006
**Prompt:** Client wants a landing page for the new savings product, nothing built yet.

_Detected: mode ['create'], platform ['web']_

- [CORE] **Product marketing site** — Structure derived from the buyer's questions (what is it, does it work for me, proof, price), a hero that shows the real product, one display face with character, one accent, one orchestrated motion moment, everything else quiet; no icon-feature grids, no gradient blobs, no testimonial carousel by default. Identity via the hero concept and type; run the anti-template check.
- [CORE] **Editorial columns** — Primary column 60–75 characters wide, generous line height, figures can break the measure, headings carry the rhythm. A sticky table of contents on wide screens, none on narrow. Resist a hero banner unless the page is a landing page; an article starts with its title.
- [CORE] **Landing hero** — The hero is a specific thesis: show the real product or outcome, one headline that a user could repeat, one primary action (a second only if it is a genuinely different path), proof close by (not a logo wall by default), LCP image optimised, text contrast guaranteed, no autoplay video without a poster and reduced-motion handling. Structure varies by product: a demo, a live widget, a number, a photograph, or a form can be the hero. _(covers: hero as a specific thesis with real proof, one primary action per view, image sizing and formats)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g01-007
**Prompt:** Put together a checkout flow for the farmers market app, cash and card both.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g01-008
**Prompt:** We're starting from zero on a scheduling screen for the salon booking app.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g01-009
**Prompt:** Design the empty state for a brand new project workspace, first-time user.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CORE] **Windows-native tool (Fluent)** — NavigationView with grouped items, CommandBar for page commands, 4 epx grid with 32 epx controls, Segoe UI Variable ramp, system accent colour respected with a brand override, Mica backdrop and layered cards with 8/4 px radii, full keyboard/access-key support, light/dark/high-contrast from system resources. Identity via the accent, iconography weight, and pane composition, not by fighting the platform.
- [CORE] **Illustration system** — Define the style (line, flat, isometric) once, use it in ≤4 places (onboarding, empty, error, success), keep it meaningful (depicts the task), and mark decorative instances aria-hidden.

### hv5-g01-010
**Prompt:** Need a screen where drivers pick their route for the day, in the van, glanceable.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Exceptions first: surface what needs attention in lists and tables** — Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g01-011
**Prompt:** New feature: let players build a custom loadout before a match starts.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-012
**Prompt:** Product wants a whole new results page for the property search, map plus list.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Geographic values → choropleth or symbol map** — Choropleth for rates with a sequential palette and ≤7 classes; symbol map for counts with area-scaled circles; equal-area projection; hover/focus tooltip with region name and value; always provide a ranked table alternative; load map data lazily. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-013
**Prompt:** From scratch — a returns wizard for the retail site, three steps max.

_Detected: mode ['create'], platform ['web']_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g01-014
**Prompt:** On the shop floor screen we need a new panel showing live line throughput.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.

### hv5-g01-015
**Prompt:** Build a signup flow for the student portal, parents can co-sign.

_Detected: mode ['create'], platform ['web']_

- [CORE] **Learning platform** — Course tiles with progress, subject colour coding with labels, a reading/lesson view in a single measured column with a persistent progress/next control, humanist sans for long reading, illustrations only for onboarding and achievements. Identity via subject palette logic and tile anatomy. On TV, lessons become landscape cards in rails with a simple player.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g01-016
**Prompt:** Create a new comparison view for two flight itineraries.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-017
**Prompt:** We need a screen for the census workers to log a household visit offline.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_
- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_

### hv5-g01-018
**Prompt:** First cut of a settings screen for the smart thermostat companion app.

_Detected: mode ['create'], platform ['mobile']_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CORE] **Service app (mobile hub-and-spoke)** — Home as a task hub with large labelled entries and the account balance/status as the single focal element, spokes as linear flows with one primary action each, list rows for history, system type styles for Dynamic Type/font scale, calm neutral palette with one trustworthy accent, illustration only in onboarding/empty states. Identity via the hub's tile geometry, illustration style, and accent.
- [CORE] **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_

### hv5-g01-019
**Prompt:** Design a new upload flow for lab results, patient facing, mobile first.

_Detected: mode ['create'], platform ['mobile']_

- [CORE] **Service app (mobile hub-and-spoke)** — Home as a task hub with large labelled entries and the account balance/status as the single focal element, spokes as linear flows with one primary action each, list rows for history, system type styles for Dynamic Type/font scale, calm neutral palette with one trustworthy accent, illustration only in onboarding/empty states. Identity via the hub's tile geometry, illustration style, and accent.
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g01-020
**Prompt:** Nothing exists yet for the vendor invoice review, start with the list view.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-021
**Prompt:** Build a new player profile page, avatar, stats, badges.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Inline badges and status chips** — Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- [CRITICAL GUARDRAILS] **Pills for everything** — Pick one corner language for controls (small/medium radius) and reserve full-round for chips/badges; ≤2 badges per item; buttons and inputs share a radius; if everything is a pill, nothing reads as a tag. _(covers: one corner language for controls)_

### hv5-g01-022
**Prompt:** We're adding a brand new tipping screen at the end of checkout, optional.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Editorial storefront** — Photography full-bleed, asymmetric editorial grid, text-only navigation, serif or grotesk display with a quiet body, monochrome UI so product colour leads, hairline dividers instead of cards, crossfade transitions, one inline CTA per product. Identity via the grid rhythm, type pairing, and image crop language. Do not default to cream+serif+terracotta.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g01-023
**Prompt:** Need a fresh screen for the customs broker to enter shipment manifests.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-024
**Prompt:** Create a welcome tour for first-time users of the budgeting app.

_Detected: mode ['create'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **First-run: permission priming and feature education without blocking** — Ask for a permission only at the moment the feature needs it, preceded by a one-screen explanation of the benefit and what happens on refusal (priming), then trigger the system prompt; never chain several permission prompts on launch, and always offer a way to continue without the permission. Feature education is non-blocking: a dismissible coach mark or inline tip anchored to the real control, one at a time, never a modal tour on first launch; it can be replayed from help, is skipped for keyboard/screen-reader users unless it is accessible, and stops after it has been dismissed once. Both respect reduced motion and never cover the primary action. _(covers: permission priming before the system prompt, non-blocking feature education, reduced motion)_

### hv5-g01-025
**Prompt:** New EPG-style browse screen for the streaming app, rails by genre.

_Detected: mode ['create'], platform ['tv']_

- [CORE] **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp). _(covers: focus restoration, focus latency, media card with one focus target and one status overlay)_
- [CORE] **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional. _(covers: pinned channel column and now marker, virtualization of long collections, D-pad focus reachability, live channel switching and mini guide, time navigation in the guide: now marker, jump by time and day)_
- [CORE] **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g01-026
**Prompt:** Design a from-scratch cart for the b2b ordering portal, bulk quantities.

_Detected: mode ['create'], platform ['web']_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g01-027
**Prompt:** Build a new referral screen where users share a code and track rewards.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Monospace as identity for technical products** — Monospace for code, IDs, timestamps, and metrics (e.g. JetBrains Mono, IBM Plex Mono, Geist Mono, Commit Mono); a compact sans for prose and navigation. Never set paragraphs in monospace.

### hv5-g01-028
**Prompt:** We need a new intake form for the clinic's telehealth triage, first visit.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g01-029
**Prompt:** Sketch a new dashboard for plant supervisors, one screen, key alarms only.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Minimal metadata** — Title plus at most one secondary line; everything else on the detail screen. On TV, reveal one more line on focus rather than showing it always.
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g01-030
**Prompt:** Add a whole new screen for comparing two mortgage offers.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Rich metadata (operational)** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane. _(covers: visual hierarchy with one focal point, tabular figures and numeric alignment)_
- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-031
**Prompt:** Starting a new library screen for saved recipes, no filters yet.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-032
**Prompt:** Need a first version of a seating chart builder for the event app.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_

### hv5-g01-033
**Prompt:** Build a new screen from the ground up for tracking vaccine doses per child.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Contextual inline actions** — Actions are visible (not hover-only), consistently placed per item type, and grouped: at most one emphasised per item. Hover-reveal is allowed only as an addition to a visible affordance and never on touch/TV.
- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_

### hv5-g01-034
**Prompt:** We want a totally new onboarding for the trucking dispatch app, driver side.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_
- [CORE] **Single column, one task** — Content width capped for reading (~60–75 characters per line), vertical rhythm from the spacing scale, primary action reachable without scrolling on the shortest supported viewport, or sticky at the bottom.

### hv5-g01-035
**Prompt:** Design a new leaderboard screen for the trivia game, weekly and all-time.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-036
**Prompt:** Nothing here yet — build the initial screen for reporting a pothole.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-037
**Prompt:** New feature request: a screen letting teachers build a seating plan.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-038
**Prompt:** Create the first version of a claims submission flow, photos and receipts.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_

### hv5-g01-039
**Prompt:** We need a screen from scratch for pharmacists to flag drug interactions.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Functional minimal motion** — Animate transform and opacity only; durations from a 3-step token scale (fast/base/slow); no motion on hover beyond colour/underline; respect prefers-reduced-motion by removing non-essential motion, not by making it faster.

### hv5-g01-040
**Prompt:** Build a new profile setup screen with avatar cropping for the kids app.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_

### hv5-g01-041
**Prompt:** Design a brand new voting ballot review screen, accessible by default.

_Detected: mode ['accessibility', 'create'], platform UNKNOWN_

- [CORE] **Medium density** — 8 px base, 40–48 px interactive heights, 16 px body on web/mobile, 16 px inside groups and 24–32 px between groups. This is the safe default when the audience is unknown; state that it was a default.
- [CORE] **Dominant brand colour** — Brand colour on large surfaces with a verified on-colour text token; a secondary neutral for content areas; do not derive the whole palette by tinting everything with the brand hue. Interactive states need visible deltas on the brand surface.
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_

### hv5-g01-042
**Prompt:** Need a screen where museum visitors can browse an exhibit map, kiosk-ish.

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g01-043
**Prompt:** First pass at a new screen for comparing energy tariffs.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CORE] **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows. _(covers: virtualization of long collections, tabular figures and numeric alignment)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-044
**Prompt:** Build a new checkout confirmation screen with order tracking link.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Editorial storefront** — Photography full-bleed, asymmetric editorial grid, text-only navigation, serif or grotesk display with a quiet body, monochrome UI so product colour leads, hairline dividers instead of cards, crossfade transitions, one inline CTA per product. Identity via the grid rhythm, type pairing, and image crop language. Do not default to cream+serif+terracotta.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g01-045
**Prompt:** We're launching a new feature: split billing between roommates.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-046
**Prompt:** Create a screen for logging maintenance on factory equipment, offline capable.

_Detected: mode ['create'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_

### hv5-g01-047
**Prompt:** New onboarding wizard for the payroll admin, five steps.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Operational workbench** — Character comes from precision: a tight 4 px grid, tabular figures, hairline borders with real contrast, one accent used only for selection and primary commands, quiet surfaces, dense but aligned. Identity via a distinctive neutral tint, a characterful monospace for IDs/values, and a consistent status colour language. No hero, no cards-in-cards, no gradients.
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-048
**Prompt:** Design a fresh notifications center, nothing exists right now.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **EPG / program guide grid** — Two-dimensional virtualisation (channels vertical, time horizontal), sticky channel column and time header, programme cells sized by duration with a minimum width so short programmes stay focusable, current time line always visible, LEFT/RIGHT move within a channel's programmes (not by pixel), UP/DOWN keep the same time slot, long press or a shortcut jumps to now, focused cell shows full title + time in a detail strip rather than truncating inside the cell. _(covers: pinned channel column and now marker, virtualization of long collections, time navigation in the guide: now marker, jump by time and day)_

### hv5-g01-049
**Prompt:** Build a screen for the concierge desk to log guest requests, from the sofa in the lounge nearby.

_Detected: mode ['create', 'accessibility'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g01-050
**Prompt:** Need a new screen for scanning a barcode and adding stock, gloves on most of the day.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **No decorative imagery** — Remove stock photos, abstract blobs, and hero illustrations from working screens; empty states may use a small, meaningful illustration or none. Identity comes from type, colour, and structure.
- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_

### hv5-g01-051
**Prompt:** Create a first draft of a workout builder, drag exercises into a plan.

_Detected: mode ['create'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g01-052
**Prompt:** We want a new comparison screen for two candidate resumes.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Duotone identity** — Two hues with defined roles (one for surfaces/identity, one for action/emphasis), neutrals derived from the first hue, feedback colours chosen to avoid both. Test that the pair reads for colour-blind users (deuteranopia simulation) since duotones often pick red/green-adjacent pairs.
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-053
**Prompt:** Build a screen for reporting outages, used by field techs, spotty signal.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Geometric sans for product/tech brands** — Choose a face the category is not saturated with (e.g. Manrope, Outfit, Urbanist, Sora, Figtree, Plus Jakarta Sans, Albert Sans, Geist for dev tools) and verify numerals and weights. Use the display cut only for the largest role.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g01-054
**Prompt:** Design the initial screen for a subscription paywall, three tiers.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Three-pane workbench** — Resizable panes with remembered sizes, each pane a landmark/region with a heading, F6-style pane cycling on desktop, collapse order defined (inspector collapses first). Keyboard focus must be able to move between panes without tabbing through every control.

### hv5-g01-055
**Prompt:** New feature: a screen where citizens track their permit application status.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Service app (mobile hub-and-spoke)** — Home as a task hub with large labelled entries and the account balance/status as the single focal element, spokes as linear flows with one primary action each, list rows for history, system type styles for Dynamic Type/font scale, calm neutral palette with one trustworthy accent, illustration only in onboarding/empty states. Identity via the hub's tile geometry, illustration style, and accent.

### hv5-g01-056
**Prompt:** Need a from-scratch screen for pairing a new device over bluetooth.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Single column, one task** — Content width capped for reading (~60–75 characters per line), vertical rhythm from the spacing scale, primary action reachable without scrolling on the shortest supported viewport, or sticky at the bottom.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g01-057
**Prompt:** Build a new screen for comparing two shipment routes on cost and time.

_Detected: mode ['create'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-058
**Prompt:** Create a screen for the security desk badge kiosk, walk-up, no login.

_Detected: mode ['create'], platform ['kiosk']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g01-059
**Prompt:** First version of a screen letting coaches build a practice plan.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-060
**Prompt:** We need a totally new screen for donors to pick a recurring gift amount.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Expressive brand motion** — Define ≤3 named easings and ≤3 durations, one signature transition (e.g. a morph), apply to state changes and navigation, never to static decoration. Reduced motion falls back to crossfades.

### hv5-g01-061
**Prompt:** Design a screen for the machine in the lobby to print a visitor badge.

_Detected: mode ['create'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Pills for everything** — Pick one corner language for controls (small/medium radius) and reserve full-round for chips/badges; ≤2 badges per item; buttons and inputs share a radius; if everything is a pill, nothing reads as a tag. _(covers: one corner language for controls)_

### hv5-g01-062
**Prompt:** Build a new screen for comparing two loan terms side by side.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CORE] **Rich metadata (operational)** — Columns with user-controlled visibility and order, consistent formatting per type (dates, currency, IDs in monospace), status as text+colour, truncation with full value on focus/hover and in the detail pane. _(covers: visual hierarchy with one focal point, tabular figures and numeric alignment)_
- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-063
**Prompt:** Need a fresh screen for parents to request a substitute teacher day.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-064
**Prompt:** Create a new screen for tracking blood donation appointments.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Neutral workhorse sans** — One family with tabular figures and a wide weight range (e.g. IBM Plex Sans, Source Sans 3, Public Sans, Atkinson Hyperlegible, or the platform system font). Display role uses the same family at heavier weight and tighter tracking rather than a second face. If the codebase already uses a system font, keep it.
- [CORE] **Spring-based physical motion** — Use the platform spring APIs (SwiftUI .spring, Compose spring(), Motion/Framer spring on web) with one or two named presets (snappy, gentle); interruptible and gesture-tracking; never chain springs on page load.

### hv5-g01-065
**Prompt:** From nothing, build a screen for restaurant staff to mark a table dirty or clean.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows. _(covers: virtualization of long collections, tabular figures and numeric alignment)_
- [CORE] **Data graphics as the visual layer** — One chart palette and one mark style across the product, sparklines in tables for trends, no decorative charts (every chart answers a question), accessible alternatives (table or summary) for each chart.
- [CRITICAL GUARDRAILS] **Numeric tables: alignment, figures, units, precision** — Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator. _(covers: tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-066
**Prompt:** New feature: an itinerary builder for the travel app, drag to reorder days.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g01-067
**Prompt:** Design a first pass at a screen for comparing two loyalty card tiers.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Duotone identity** — Two hues with defined roles (one for surfaces/identity, one for action/emphasis), neutrals derived from the first hue, feedback colours chosen to avoid both. Test that the pair reads for colour-blind users (deuteranopia simulation) since duotones often pick red/green-adjacent pairs.
- [CORE] **Duotone icons as brand accent** — Duotone in feature/marketing contexts; in functional UI revert to a single-tone variant of the same set so navigation stays crisp. Verify the secondary tone is decorative (meaning must survive in monochrome).
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-068
**Prompt:** We need a screen for warehouse leads to assign pickers to zones.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-069
**Prompt:** Build a screen where players customize their in-game avatar before entering the lobby.

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-070
**Prompt:** Create the initial screen for a co-op grocery order splitting tool.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-071
**Prompt:** The totals never line up on the invoice summary, off by a pixel or two.

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g01-072
**Prompt:** The tab key skips over half the fields on the intake form.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g01-073
**Prompt:** Users keep missing the save button, it's below the fold on smaller windows.

_Detected: mode ['audit', 'responsive'], platform ['desktop']_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [OPTIONAL NOTES] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_

### hv5-g01-074
**Prompt:** Something's off with the loading spinner on the payments screen, it flickers.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-075
**Prompt:** The card on the checkout page doesn't update when quantity changes.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g01-076
**Prompt:** Drivers say the route screen freezes when they lose signal in the tunnel.

_System declined (out of scope): technical cause (signal) with a user-visible symptom (freezes); design-engineering contributes the UX side_

### hv5-g01-077
**Prompt:** The overlay stays visible after the video ends, blocking the controls.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_

### hv5-g01-078
**Prompt:** On the ward, the vitals chart resets the zoom every time a new reading comes in.

_Detected: mode ['create'], platform ['mobile']_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Editorial storefront** — Photography full-bleed, asymmetric editorial grid, text-only navigation, serif or grotesk display with a quiet body, monochrome UI so product colour leads, hairline dividers instead of cards, crossfade transitions, one inline CTA per product. Identity via the grid rhythm, type pairing, and image crop language. Do not default to cream+serif+terracotta.
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-079
**Prompt:** The dropdown for state selection doesn't scroll on touch, it just jumps.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_

### hv5-g01-080
**Prompt:** Compare two files feature shows the wrong diff colors half the time.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-081
**Prompt:** Fix the cart badge count, it doesn't update after a remove.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g01-082
**Prompt:** The remote screen in the WPF app throws when you resize below 800px wide.

_System declined (out of scope): not a UI design task: frontend runtime work (throws when) without a UI design, interaction or accessibility requirement_

### hv5-g01-083
**Prompt:** Something breaks the seating chart when two people drag at once.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g01-084
**Prompt:** The landscape mode on the tablet cuts off the last column of the table.

_Detected: mode ['responsive', 'audit'], platform ['tablet']_

- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_

### hv5-g01-085
**Prompt:** Nurses report the med schedule doesn't refresh unless you force close the app.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_

### hv5-g01-086
**Prompt:** The terminal at gate 12 kiosk keeps timing out mid-checkin.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-087
**Prompt:** Search results flicker and reorder themselves right after loading.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CORE] **Catalog grid** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift. _(covers: applied filters as removable chips with counts, pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g01-088
**Prompt:** The guide screen for new hires links to a page that doesn't exist anymore.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.
