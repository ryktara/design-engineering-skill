### hv5-g02-057
**Prompt:** the color contrast between the label and the background is weak

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [OPTIONAL NOTES] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g02-058
**Prompt:** the transition when the tab bar opens feels abrupt

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

### hv5-g02-059
**Prompt:** the icons in the tab bar are inconsistent sizes

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

### hv5-g02-060
**Prompt:** there's too much whitespace above the tab bar and not enough below it

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

### hv5-g02-061
**Prompt:** the card text wraps awkwardly on longer names

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [OPTIONAL NOTES] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-062
**Prompt:** the shadow under the notification tray looks heavier than the rest of the home screen

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Flat surfaces with tonal layers** — Define three tonal steps per theme with measured contrast (each step ≥1.1:1 apart and borders ≥3:1 where they mark boundaries). Shadows reserved for transient layers (menus, dialogs, drag). Reads professional at any density and avoids the 'everything is a floating card' look.
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-063
**Prompt:** can you compare two files side by side like the comparison chart does

_Detected: mode ['review', 'audit'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g02-064
**Prompt:** what order should the two buttons go in on the poster print layout

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-065
**Prompt:** the comparison chart feels crowded next to the legend behind the counter

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_

### hv5-g02-066
**Prompt:** one spacing value: how much gap under the comparison chart

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Chart colour: categorical ≤8, colour-blind safe, plus shape/label** — One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette. _(covers: no colour alone for status)_
- [CORE] **Geographic values → choropleth or symbol map** — Choropleth for rates with a sequential palette and ≤7 classes; symbol map for counts with area-scaled circles; equal-area projection; hover/focus tooltip with region name and value; always provide a ranked table alternative; load map data lazily. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g02-067
**Prompt:** the font size jumps between the card component and the paragraph below it

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_

### hv5-g02-068
**Prompt:** margins around the report view are inconsistent from section to section

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-069
**Prompt:** the office remote team can't see the remote control screen preview

_Detected: mode ['accessibility', 'audit'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: dark-first colour with restrained saturation** — Dark tinted canvas, text at 87–92% white, accent used for focus and primary only, semantic colours checked at ≥4.5:1 on dark, gradients dithered or avoided (banding on 8-bit panels), test in 'Standard' picture mode on a real panel. _(covers: dark-first TV palette, high contrast)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g02-070
**Prompt:** the corners on the terminal display look sharper than everything else on the page

_Detected: mode ['polish', 'audit'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-071
**Prompt:** the row dividers in the event log are darker than they need to be

_System declined (out of scope): UI design / interaction task_

### hv5-g02-072
**Prompt:** the header title feels lost among the surrounding text

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Condensed display for broadcast/media** — Condensed only for titles and channel names (e.g. Barlow Condensed, Oswald, Roboto Condensed, Archivo Narrow) at heavy weights; body and metadata in a normal-width sans with tabular figures for times.
- [OPTIONAL NOTES] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-073
**Prompt:** the poster-sized print export looks nothing like the movie poster thumbnail

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV. _(covers: media card with one focus target and one status overlay, accessible names and labels)_
- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Web: reserve space, load fonts and images without shift** — width/height or aspect-ratio on every media element, font-display: swap with size-adjust or a metric-compatible fallback, preload the display font and LCP image, skeletons match final dimensions, sticky elements don't push content. Target CLS < 0.1, LCP < 2.5 s. _(covers: no layout shift, image sizing and formats)_

### hv5-g02-074
**Prompt:** the search results list button placement feels like an afterthought

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [OPTIONAL NOTES] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g02-075
**Prompt:** the loading skeleton doesn't match the real dashboard widget layout

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Web: reserve space, load fonts and images without shift** — width/height or aspect-ratio on every media element, font-display: swap with size-adjust or a metric-compatible fallback, preload the display font and LCP image, skeletons match final dimensions, sticky elements don't push content. Target CLS < 0.1, LCP < 2.5 s. _(covers: no layout shift, image sizing and formats)_
- [OPTIONAL NOTES] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-076
**Prompt:** the sidebar looks fine on Avalonia but slightly squished on smaller widths

_Detected: mode ['polish', 'audit'], platform ['desktop']_

- [CORE] **Persistent left rail / sidebar** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-077
**Prompt:** just need the right shade of gray for this one divider

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-078
**Prompt:** the tab labels in the card are centered oddly

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g02-079
**Prompt:** should the form button say Cancel or Dismiss

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_

### hv5-g02-080
**Prompt:** the empty state illustration feels too big for the space

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g02-081
**Prompt:** the card and the footer feel disconnected, too much gap between them

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_

### hv5-g02-082
**Prompt:** the highlight color on the selected filter panel clashes with the rest of the palette

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g02-083
**Prompt:** text inside the card feels vertically off-center

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Landscape media cards (16:9)** — Fixed 16:9, progress bar inside the art bottom edge with a scrim, duration/remaining badge with text, channel logo for live, 4 per row on TV at 960 dp with 20 dp gutters, title below.
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_

### hv5-g02-084
**Prompt:** the checkout summary looks cluttered once real data fills it in

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g02-085
**Prompt:** the spacing rhythm breaks down once the card wraps to two lines

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g02-086
**Prompt:** the comparison chart feels visually heavier than the action bar, even though it's less important

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_

### hv5-g02-087
**Prompt:** motion on the member profile dismiss feels too fast to register

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g02-088
**Prompt:** the form caption text is set in a slightly different font than the rest

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-089
**Prompt:** there's a stray extra gap between the checkout summary and the divider below it

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g02-090
**Prompt:** the guide overlay row height doesn't match the tooltip row height right above it

_System declined (out of scope): UI design / interaction task_

### hv5-g02-091
**Prompt:** should the toolbar icon be filled or outlined

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_

### hv5-g02-092
**Prompt:** the tab icon and text baseline don't quite align

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-093
**Prompt:** should this single label be bold or regular

_System declined (out of scope): UI design / interaction task_

### hv5-g02-094
**Prompt:** the modal looks a bit dated compared to the rest of the dashboard

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-095
**Prompt:** the primary and secondary buttons on the navigation drawer look too similar in weight

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CORE] **Drawer / side panel** — Inline (pushes content) on wide screens, overlay on narrow; width from tokens (320–480 px); heading + close; focus moves in on open and returns on close; content scrolls independently; TV: side sheet that keeps the player/content visible and traps DPAD inside until BACK. _(covers: drawer / side panel focus in and out)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g02-096
**Prompt:** what's the right corner radius for just this one card

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Flat tiles** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Pills for everything** — Pick one corner language for controls (small/medium radius) and reserve full-round for chips/badges; ≤2 badges per item; buttons and inputs share a radius; if everything is a pill, nothing reads as a tag. _(covers: one corner language for controls)_

### hv5-g02-097
**Prompt:** the card padding on the navigation drawer feels inconsistent left versus right

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g02-098
**Prompt:** should the settings screen text be left or center aligned

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [OPTIONAL NOTES] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-099
**Prompt:** what should the focus ring look like on the event log

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Visible focus ring (web/desktop)** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element. _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g02-100
**Prompt:** the section header above the dashboard widget feels too close to the content

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [OPTIONAL NOTES] **Measure, rhythm, and hierarchy by contrast of size and weight** — 45–75 characters per line for prose; vertical spacing from the spacing scale tied to line height; hierarchy from clear jumps (≥1.25×) in size or weight, not from five near-identical sizes; headings closer to the content below than to the content above. _(covers: readable line length, visual hierarchy with one focal point)_
- [OPTIONAL NOTES] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-101
**Prompt:** the comparison chart color feels slightly desaturated next to the rest of the brand palette

_Detected: mode ['brand', 'polish'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Chart colour: categorical ≤8, colour-blind safe, plus shape/label** — One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette. _(covers: no colour alone for status)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CRITICAL GUARDRAILS] **Brands that differ only by logo, primary colour, and font** — Run fingerprint.py compare on the candidate brand systems; a COSMETIC-ONLY verdict fails differentiation. Vary at least two structural axes (navigation model, layout topology, density, surface strategy, image strategy, metadata density, CTA strategy) per brand, then cosmetics. _(covers: structural, not cosmetic, brand differentiation)_
- [CRITICAL GUARDRAILS] **Semantic colour tokens, not raw hex in components** — Three layers: primitive palette → semantic roles (bg.canvas, text.primary, action.primary, border.default, focus.ring, feedback.error…) → component tokens where needed. Every theme (light, dark, high-contrast, each brand) redefines only the semantic layer. Validate with tokens.py validate. _(covers: semantic token layers per theme)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g02-102
**Prompt:** what color should the error label be

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Neutral canvas + one accent** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g02-103
**Prompt:** the modal title and subtitle feel like they're competing for attention

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g02-104
**Prompt:** the dashboard widget could use a subtle divider to separate it from the icon set

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [OPTIONAL NOTES] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-105
**Prompt:** the form feels off-grid compared to everything else on the order summary

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g02-106
**Prompt:** the payment card panel icon looks slightly larger than its neighbors in the row

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-107
**Prompt:** what order should the two buttons go in on the tab

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_
- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-108
**Prompt:** one spacing value: how much gap under the member profile

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g02-109
**Prompt:** the upload panel typography doesn't match the scale used elsewhere on the onboarding sequence

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g02-110
**Prompt:** the dashboard widget corner radius is inconsistent between the card and its buttons

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-111
**Prompt:** just need the right shade of gray for this one divider

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-112
**Prompt:** score the report view for how easy it is to use for a first-time visitor

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g02-113
**Prompt:** review the onboarding flow flow end to end and flag anything that feels off

_Detected: mode ['audit', 'polish'], platform UNKNOWN_

- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_
- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-114
**Prompt:** what would you change about this modal if you had to ship it tomorrow

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [OPTIONAL NOTES] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-115
**Prompt:** give me an honest read on the player screen before we show it to the client

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.

### hv5-g02-116
**Prompt:** walk through the navigation drawer as if you'd never seen it before, what trips you up

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-117
**Prompt:** should the event log button say Cancel or Dismiss

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Developer tool** — Command palette as the accelerator, three-pane workbench with resizable panes, bordered surfaces on a dark or light neutral canvas, monospace for values and a compact sans for chrome, syntax-style accent colours used semantically (status, diff), keyboard shortcuts shown everywhere. Identity via the monospace face, the accent, and pane framing.

### hv5-g02-118
**Prompt:** does the status indicator hold up next to competitors' versions of the same screen

_System declined (out of scope): UI design / interaction task_

### hv5-g02-119
**Prompt:** inspect the admin console and list every inconsistency you find

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows. _(covers: virtualization of long collections, tabular figures and numeric alignment)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_

### hv5-g02-120
**Prompt:** how would you rate the hierarchy on this landscape view, one to ten

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-121
**Prompt:** go through the order summary like a design reviewer would and note the rough edges

_System declined (out of scope): UI design / interaction task_

### hv5-g02-122
**Prompt:** check whether the landscape view actually communicates what it's supposed to

_System declined (out of scope): UI design / interaction task_

### hv5-g02-123
**Prompt:** review this dashboard widget for anything that would embarrass us in a demo

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [OPTIONAL NOTES] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-124
**Prompt:** take a critical pass at the profile page layout and call out what's weak

_System declined (out of scope): UI design / interaction task_

### hv5-g02-125
**Prompt:** assess whether the header matches the tone of the rest of the product

_System declined (out of scope): not a UI design task: backend work (rest) without a UI design, interaction or accessibility requirement_

### hv5-g02-126
**Prompt:** review the filter panel the way a new hire designer would, cold

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g02-127
**Prompt:** grade the dashboard on clarity, then tell me the single biggest issue

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-128
**Prompt:** look over the landscape view and tell me if the flow makes sense end to end

_System declined (out of scope): UI design / interaction task_

### hv5-g02-129
**Prompt:** does this player screen feel finished, or does something still read unpolished

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_

### hv5-g02-130
**Prompt:** review the poster print layout for anything a design lead would flag in five minutes

_System declined (out of scope): UI design / interaction task_

### hv5-g02-131
**Prompt:** audit this player screen against basic usability heuristics and report back

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_

### hv5-g02-132
**Prompt:** take a step back and evaluate whether the notification tray actually solves the problem

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_

### hv5-g02-133
**Prompt:** compare the card against the previous version and note what regressed

_Detected: mode ['review', 'audit'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g02-134
**Prompt:** review the home screen for anything that looks inconsistent across screens

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-135
**Prompt:** give a quick critique of the card component, treat it like a portfolio review

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Bordered cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g02-136
**Prompt:** should the landscape view icon be filled or outlined

_System declined (out of scope): UI design / interaction task_

### hv5-g02-137
**Prompt:** review the onboarding sequence and rank the top three things worth fixing first

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_

### hv5-g02-138
**Prompt:** should this single label be bold or regular

_System declined (out of scope): UI design / interaction task_

### hv5-g02-139
**Prompt:** audit the report view for anything that breaks the visual rhythm of the app

_System declined (out of scope): UI design / interaction task_

### hv5-g02-140
**Prompt:** review whether the player overlay actually earns its place on this dashboard

_Detected: mode ['review', 'audit'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_

### hv5-g02-141
**Prompt:** assess the tab the way a stakeholder walking by would judge it

_System declined (out of scope): UI design / interaction task_

### hv5-g02-142
**Prompt:** go over the profile page and flag anything that feels inconsistent with the brand

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-143
**Prompt:** review the checkout summary for clarity, is it obvious what to do next

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_
- [OPTIONAL NOTES] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_

### hv5-g02-144
**Prompt:** take an honest pass at the checkout page, what would a critic say

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_
