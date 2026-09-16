### hv5-g03-073
**Prompt:** the terminal at the gate has a portrait screen but our UI still assumes landscape

_System declined (out of scope): UI design / interaction task_

### hv5-g03-074
**Prompt:** why does the analytics dashboard need a horizontal scrollbar at 1280px, that's a normal laptop

_Detected: mode ['audit', 'responsive'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CRITICAL GUARDRAILS] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g03-075
**Prompt:** split view on the factory supervisor's tablet leaves the alert panel with barely any room to show text

_Detected: mode ['responsive', 'audit'], platform ['tablet']_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Exceptions first: surface what needs attention in lists and tables** — Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-076
**Prompt:** one column width fix on the export summary table

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Table-first working screen** — Table fills the viewport height with internal scrolling and sticky header, row density selectable, column widths persisted, filters as a row of chips/fields above the table (not a hidden drawer), bulk actions appear in the toolbar on selection. Numeric columns right-aligned with tabular figures. Virtualise beyond a few hundred rows. _(covers: virtualization of long collections, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_

### hv5-g03-077
**Prompt:** the itinerary card breaks its own grid when someone has a longer flight number, does it wrap or overflow?

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_

### hv5-g03-078
**Prompt:** does the loan application form actually work on a foldable phone half-open?

_Detected: mode ['audit'], platform ['mobile', 'tablet']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g03-079
**Prompt:** resizing the video call window shrinks the participant grid but the toolbar stays a fixed width and eats the space

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-080
**Prompt:** field techs on the van's mounted tablet complain the job list truncates every address after 20 characters

_Detected: mode ['responsive', 'audit'], platform ['tablet']_

- [CORE] **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g03-081
**Prompt:** audit breakpoints across the whole insurance quote flow, we've only ever tested desktop

_Detected: mode ['audit', 'responsive'], platform ['desktop']_

- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-082
**Prompt:** the museum kiosk's landscape orientation lock doesn't actually lock, rotating the stand flips the whole UI

_System declined (out of scope): UI design / interaction task_

### hv5-g03-083
**Prompt:** does the recipe scaling tool's layout survive a narrow kitchen tablet mounted under a cabinet?

_System declined (out of scope): UI design / interaction task_

### hv5-g03-084
**Prompt:** the two-pane email client collapses to one pane too early, at 1100px instead of something reasonable

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Master–detail (list + detail pane)** — List pane with selection state that is keyboard-navigable (arrow keys change selection, Enter opens), detail pane that updates in place and announces its title to assistive tech. Persist the selected item across navigation. On narrow widths collapse to a two-screen stack with Back.

### hv5-g03-085
**Prompt:** check whether the site's nav bar wraps into two rows on a 13 inch laptop with the sidebar open

_Detected: mode ['responsive', 'audit'], platform ['web']_

- [CORE] **Top bar navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible.
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g03-086
**Prompt:** from the sofa, the EPG rows scroll fine but the highlighted tile jumps two rows when you press down

_Detected: mode ['accessibility', 'audit'], platform ['tv']_

- [CORE] **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional. _(covers: pinned channel column and now marker, virtualization of long collections, D-pad focus reachability, live channel switching and mini guide, time navigation in the guide: now marker, jump by time and day)_
- [CORE] **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV. _(covers: media card with one focus target and one status overlay, accessible names and labels)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [OPTIONAL NOTES] **TV: pace held D-pad repeats on rails and grids** — First press moves immediately; while the key is held, admit repeats at a fixed pace (about 3–5 cards per second) and finish each scroll step before the next move; keep the focused card inside the viewport with a stable position; show a large title of the focused item; under reduced motion keep the same pace with instant (non-animated) moves; long lists offer a page-jump (channel up/down, letter index). _(covers: focus latency, reduced motion, visible focus)_

### hv5-g03-087
**Prompt:** the player overlay covers the scrubber and you can't tell if you're hovering the seek bar or the volume control

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_

### hv5-g03-088
**Prompt:** focus gets lost entirely when the recommendation rail finishes loading, remote just does nothing

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp). _(covers: focus restoration, focus latency, media card with one focus target and one status overlay)_
- [CORE] **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV. _(covers: media card with one focus target and one status overlay, accessible names and labels)_
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-089
**Prompt:** does the channel guide handle a ten-hour marathon block without the row scrolling forever?

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CORE] **EPG / program guide grid** — Two-dimensional virtualisation (channels vertical, time horizontal), sticky channel column and time header, programme cells sized by duration with a minimum width so short programmes stay focusable, current time line always visible, LEFT/RIGHT move within a channel's programmes (not by pixel), UP/DOWN keep the same time slot, long press or a shortcut jumps to now, focused cell shows full title + time in a detail strip rather than truncating inside the cell. _(covers: pinned channel column and now marker, virtualization of long collections, time navigation in the guide: now marker, jump by time and day)_
- [CORE] **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional. _(covers: pinned channel column and now marker, virtualization of long collections, D-pad focus reachability, live channel switching and mini guide, time navigation in the guide: now marker, jump by time and day)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g03-090
**Prompt:** the Tizen app's live tile thumbnails are blurry from ten feet away, text is unreadable on the couch

_Detected: mode ['accessibility', 'audit'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **TV: focus response and list performance** — Focus moves must render within one frame (≤16 ms at 60 Hz) even while images load; key events are never dropped or coalesced into jumps; images sized to card, cached, and loaded with placeholders; rows virtualised vertically and horizontally; heavy backdrops debounced; test on the cheapest target device (e.g. 1–2 GB RAM set-top boxes), not the emulator. _(covers: focus latency, virtualization of long collections, image sizing and formats)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g03-091
**Prompt:** pressing back on the remote during playback exits the whole app instead of showing controls

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: transport control conventions** — Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input (any key resets the timer; do not hide while a control is receiving input); subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour, live channel switching and mini guide, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: predictable BACK** — BACK closes the topmost layer (player controls → player → detail → home → nav → exit); in a rail-based home, BACK from content first moves focus to the navigation (side nav or top tabs) and scrolls to top, then exits. Deep-linked entries still unwind to the app home. Splash screens are never in the back stack. _(covers: BACK behaviour)_

### hv5-g03-092
**Prompt:** the webOS home screen's focus ring is invisible against the dark hero art

_Detected: mode ['accessibility', 'audit'], platform ['tv']_

- [CORE] **Immersive hero + rails** — Backdrop crossfades on focus change with a debounce (~300 ms) so scrubbing across a rail doesn't thrash decodes; a scrim gradient guarantees text contrast over any image; the hero text block sits in the safe area with title, one line of metadata, and a short synopsis; the first rail is partially visible so users know to press DOWN. Provide a reduced-motion path with a static backdrop. _(covers: focus restoration, media card with one focus target and one status overlay)_
- [CORE] **Media details screen, resume playback and watchlist** — Details: the primary action is Play (or Resume with the remaining time and a Start over alternative) and it takes default focus; metadata is a short scannable block (duration, year, rating, badges as text not colour), synopsis ≤3 lines with an expander, episodes as a rail or list with progress bars and the next unwatched episode preselected; secondary actions (watchlist, trailer, more like this) sit after Play in one row. Resume: a continue-watching row shows progress on each card, resumes at the saved position, and removes finished items; entering a title from the row returns focus to that card. Watchlist: one toggle with a clear on/off state and text label, works from cards and details, and is reflected immediately in the watchlist row. Everything is reachable with D-pad UP/DOWN/LEFT/RIGHT and BACK returns to the row that launched the details. _(covers: details screen with Play as default focus, continue watching / resume playback, watchlist / save for later, focus restoration, BACK behaviour, no colour alone for status)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g03-093
**Prompt:** one spacing fix between the rail tiles, they're touching

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g03-094
**Prompt:** in the break room the office remote skips two channels every time someone double presses the arrow key too fast

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.
- [CRITICAL GUARDRAILS] **TV: pace held D-pad repeats on rails and grids** — First press moves immediately; while the key is held, admit repeats at a fixed pace (about 3–5 cards per second) and finish each scroll step before the next move; keep the focused card inside the viewport with a stable position; show a large title of the focused item; under reduced motion keep the same pace with instant (non-animated) moves; long lists offer a page-jump (channel up/down, letter index). _(covers: focus latency, reduced motion, visible focus)_
- [OPTIONAL NOTES] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_

### hv5-g03-095
**Prompt:** why does the subtitle track selector require six clicks on a d-pad to reach

_Detected: mode ['audit'], platform ['tv']_

- [CORE] **TV side sheet / chooser** — A right-hand sheet (~600 dp) over a scrim; columns of radio rows; first focus lands on the current value; selected state is a fill + check + semantics distinct from the focus ring; SELECT applies immediately; BACK closes and returns focus to the button that opened it; show the current choice next to the button when closed; include an Off row and a 'no tracks' text state; player controls stay hidden while the sheet is open. _(covers: dialog focus management, selected state visible and distinct from focus and hover, focus restoration, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: pace held D-pad repeats on rails and grids** — First press moves immediately; while the key is held, admit repeats at a fixed pace (about 3–5 cards per second) and finish each scroll step before the next move; keep the focused card inside the viewport with a stable position; show a large title of the focused item; under reduced motion keep the same pace with instant (non-animated) moves; long lists offer a page-jump (channel up/down, letter index). _(covers: focus latency, reduced motion, visible focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-096
**Prompt:** the live sports overlay showing the score never updates unless you exit and re-enter the stream

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.

### hv5-g03-097
**Prompt:** audit the whole rails-and-hero home screen for anyone squinting from across the room

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp). _(covers: focus restoration, focus latency, media card with one focus target and one status overlay)_
- [CORE] **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV. _(covers: media card with one focus target and one status overlay, accessible names and labels)_
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CRITICAL GUARDRAILS] **Identical landing skeleton (hero + 3 features + testimonials + CTA)** — Derive the page structure from what convinces this product's buyer: a live demo, a calculator, a comparison table, a single case study, the actual data, a photograph of the physical thing. Cut sections that only exist because the template has them. The section order is a decision, state it. _(covers: no template skeleton pages, hero as a specific thesis with real proof)_

### hv5-g03-098
**Prompt:** does the parental control PIN pad on the set-top box work with a remote that has no numpad?

_Detected: mode ['audit'], platform ['tv']_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CRITICAL GUARDRAILS] **TV: transport control conventions** — Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input (any key resets the timer; do not hide while a control is receiving input); subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour, live channel switching and mini guide, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: no touch, no hover, no scrollbars** — Every interaction maps to DPAD + SELECT + BACK (+ optional MENU/PLAY keys); text entry is minimal and uses the system keyboard or voice; no hover-only affordances; no visible scrollbars; no small inline links; a desktop layout enlarged is not a TV layout. _(covers: no touch or hover assumptions on TV, no hover dependence)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g03-099
**Prompt:** our tvOS focus engine keeps snapping to the wrong tile when two rails are close together vertically

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CORE] **TV rail (horizontal row of cards)** — Rail title (≥24 sp) left-aligned in the safe area, cards of one aspect ratio, focused card scrolls to a fixed pivot (~10–30% from left) with LEFT at index 0 going to navigation, focus memory per rail, lazy loading of items and images, 'see all' as the last card if the rail is capped, no wrap-around, consistent card counts per width (Android: ~4 landscape / ~6 portrait at 960 dp). _(covers: focus restoration, focus latency, media card with one focus target and one status overlay)_
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-100
**Prompt:** the mini player in the corner during a phone call overlay blocks the closed captions entirely

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_

### hv5-g03-101
**Prompt:** grandma can't find the exit button on the streaming app menu from the couch, it's tucked in a corner

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CORE] **Cinematic media (TV)** — Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [OPTIONAL NOTES] **TV: predictable BACK** — BACK closes the topmost layer (player controls → player → detail → home → nav → exit); in a rail-based home, BACK from content first moves focus to the navigation (side nav or top tabs) and scrolls to top, then exits. Deep-linked entries still unwind to the app home. Splash screens are never in the back stack. _(covers: BACK behaviour)_

### hv5-g03-102
**Prompt:** the karaoke lounge's queue screen doesn't scroll with the remote, you have to use the on-screen mouse pointer mode

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: no touch, no hover, no scrollbars** — Every interaction maps to DPAD + SELECT + BACK (+ optional MENU/PLAY keys); text entry is minimal and uses the system keyboard or voice; no hover-only affordances; no visible scrollbars; no small inline links; a desktop layout enlarged is not a TV layout. _(covers: no touch or hover assumptions on TV, no hover dependence)_

### hv5-g03-103
**Prompt:** one color change on the buffering spinner, that's the whole ask

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g03-104
**Prompt:** review the whole media player chrome, buttons, captions, scrubber, everything, for ten-foot legibility

_Detected: mode ['audit', 'review'], platform ['tv', 'web']_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Player with overlay controls** — Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout. _(covers: auto-hide timing of player controls)_
- [CRITICAL GUARDRAILS] **TV: transport control conventions** — Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input (any key resets the timer; do not hide while a control is receiving input); subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour, live channel switching and mini guide, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: predictable BACK** — BACK closes the topmost layer (player controls → player → detail → home → nav → exit); in a rail-based home, BACK from content first moves focus to the navigation (side nav or top tabs) and scrolls to top, then exits. Deep-linked entries still unwind to the app home. Splash screens are never in the back stack. _(covers: BACK behaviour)_

### hv5-g03-105
**Prompt:** the news ticker overlay running along the bottom obscures the lower third graphics during breaking segments

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Chart colour: categorical ≤8, colour-blind safe, plus shape/label** — One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette. _(covers: no colour alone for status)_

### hv5-g03-106
**Prompt:** why does holding down the remote's fast forward button skip the whole episode instead of scrubbing smoothly

_Detected: mode ['audit'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: pace held D-pad repeats on rails and grids** — First press moves immediately; while the key is held, admit repeats at a fixed pace (about 3–5 cards per second) and finish each scroll step before the next move; keep the focused card inside the viewport with a stable position; show a large title of the focused item; under reduced motion keep the same pace with instant (non-animated) moves; long lists offer a page-jump (channel up/down, letter index). _(covers: focus latency, reduced motion, visible focus)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-107
**Prompt:** the gym's wall-mounted display cycles workout stats but nobody can read the small font from the treadmill

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-108
**Prompt:** does the now-playing rail actually indicate which tile has focus once you scroll past the first row?

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_

### hv5-g03-109
**Prompt:** the remote's back button behaves differently on every screen of the app, sometimes it exits, sometimes it goes up a level

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: predictable BACK** — BACK closes the topmost layer (player controls → player → detail → home → nav → exit); in a rail-based home, BACK from content first moves focus to the navigation (side nav or top tabs) and scrolls to top, then exits. Deep-linked entries still unwind to the app home. Splash screens are never in the back stack. _(covers: BACK behaviour)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-110
**Prompt:** fix the closed caption sizing so it doesn't cover the player controls when both are visible

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **TV side sheet / chooser** — A right-hand sheet (~600 dp) over a scrim; columns of radio rows; first focus lands on the current value; selected state is a fill + check + semantics distinct from the focus ring; SELECT applies immediately; BACK closes and returns focus to the button that opened it; show the current choice next to the button when closed; include an Off row and a 'no tracks' text state; player controls stay hidden while the sheet is open. _(covers: dialog focus management, selected state visible and distinct from focus and hover, focus restoration, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **TV: transport control conventions** — Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input (any key resets the timer; do not hide while a control is receiving input); subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide. _(covers: auto-hide timing of player controls, BACK behaviour, live channel switching and mini guide, subtitle and audio track selection reachable from the player)_

### hv5-g03-111
**Prompt:** the lobby's digital signage rotates ads but the transition stutters every third slide

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g03-112
**Prompt:** one contrast bump on the live badge, red on red right now

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_

### hv5-g03-113
**Prompt:** the airport departure board's font choice makes 3 and 8 nearly identical from thirty feet

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g03-114
**Prompt:** does the profile switcher on the shared living room account require typing on a d-pad keyboard, that's painful

_Detected: mode ['audit'], platform ['tv']_

- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: vertical = sections, horizontal = items** — Every focusable element must be reachable with straight UP/DOWN/LEFT/RIGHT presses; no diagonal reasoning, no hidden hops. Search and settings live at a predictable edge. Grids: LEFT at the first column may enter side navigation, RIGHT at the last column stays. Forms: one field per row, DOWN advances. _(covers: D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_

### hv5-g03-115
**Prompt:** audit the whole guide from the couch, both eyesight and remote lag

_Detected: mode ['audit'], platform ['tv']_

- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g03-116
**Prompt:** the fitness class replay rail loses your scroll position every time you back out and come back

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Media card (poster/thumbnail)** — Fixed aspect, image with placeholder + title fallback, title below (1–2 lines, ellipsis), one status overlay max (progress bar, live badge, new), whole card is one focusable/tappable element with an accessible name (title + status), TV focus = scale + border/glow, hover on web = subtle lift, touch = pressed state; no inner buttons on TV. _(covers: media card with one focus target and one status overlay, accessible names and labels)_
- [CORE] **Mini player / picture-in-picture state** — The mini player is a single focusable/tappable region anchored to a corner (TV: bottom-right inside the safe margin, never over the focused rail; mobile: bottom above the tab bar; web: bottom-right) with the title (one line, truncated with a full title on focus), live/progress indicator and exactly two actions (expand, close); on TV, SELECT expands to the full player and BACK from the full player returns to the mini state with focus restored to the element that was focused before; playback state (playing/paused/buffering/error) is shown with an icon plus text, and the audio keeps playing while the UI is navigated; the region is excluded from the rail's D-pad focus loop except through an explicit UP/RIGHT move; never autoplay audio from a mini player on page load on web. _(covers: focus restoration, BACK behaviour, loading, empty and error states, TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_

### hv5-g03-117
**Prompt:** why does pausing during a live broadcast show a frozen frame with no buffering indicator at all

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g03-118
**Prompt:** the waiting room monitor cycles a queue number list but the current-turn highlight is barely different from the rest

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Exceptions first: surface what needs attention in lists and tables** — Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-119
**Prompt:** check whether voice search on the remote actually surfaces a result you can select with d-pad afterward

_Detected: mode ['create'], platform ['tv']_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Horizontal rails (rows of content)** — Each rail has a visible title, focused item scrolls to a fixed pivot (about 20–30% from the left) rather than centring, rails remember their last focused index when returning, row heights are consistent within a rail, and off-screen items are partially visible to signal continuation. Lazy-load rails and images; never render every rail on first paint. Keep the safe margin (~5% / 48 dp horizontal, 27 dp vertical at 960×540 dp). _(covers: focus restoration)_
- [CRITICAL GUARDRAILS] **TV search: voice first, on-screen keyboard second** — Offer voice entry first, a compact keyboard grid with predictive suggestions, results updating live with focus kept in the keyboard until DOWN, recent searches as rails, and a clear focus path from keyboard to results. _(covers: TV search with system keyboard or voice, D-pad focus reachability)_
- [CRITICAL GUARDRAILS] **TV: pace held D-pad repeats on rails and grids** — First press moves immediately; while the key is held, admit repeats at a fixed pace (about 3–5 cards per second) and finish each scroll step before the next move; keep the focused card inside the viewport with a stable position; show a large title of the focused item; under reduced motion keep the same pace with instant (non-animated) moves; long lists offer a page-jump (channel up/down, letter index). _(covers: focus latency, reduced motion, visible focus)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g03-120
**Prompt:** the multi-camera angle switcher during the match overlaps the scoreboard graphic when you open it

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-121
**Prompt:** right-click context menu on the file browser doesn't match the ribbon's own commands, half of them are missing

_Detected: mode ['audit', 'refactor'], platform ['desktop']_

- [CORE] **Desktop menu bar + toolbar commands** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live.
- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_

### hv5-g03-122
**Prompt:** the WPF grid's column resize handles are two pixels wide, impossible to grab reliably

_Detected: mode ['responsive', 'audit'], platform ['desktop']_

- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_

### hv5-g03-123
**Prompt:** does the Avalonia app remember window position across restarts on a multi-monitor setup?

_Detected: mode ['audit', 'responsive'], platform ['desktop']_

- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-124
**Prompt:** our Electron app's menu bar looks native on mac but generic on windows, is that intentional

_Detected: mode ['polish', 'audit'], platform ['desktop']_

- [CORE] **Desktop menu bar + toolbar commands** — Menu bar for the complete command set with access keys and accelerators shown; toolbar/command bar for the frequent subset; context menus mirror the toolbar for the selected object. Commands must be enabled/disabled by state, never hidden, so users learn where things live.
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [OPTIONAL NOTES] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_

### hv5-g03-125
**Prompt:** keyboard shortcuts conflict between the app's own hotkeys and the OS-level ones, ctrl+n does nothing

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-126
**Prompt:** the WinUI3 title bar doesn't respect the system's dark mode toggle, it stays white

_System declined (out of scope): UI design / interaction task_

### hv5-g03-127
**Prompt:** why does dragging a row in the data grid also select text underneath it

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-128
**Prompt:** one menu item reorder in the File menu, that's it

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Top bar navigation** — Put primary destinations in a single horizontal bar; collapse to a menu button below the container width rather than hiding destinations one by one. The active item must be marked by more than colour (underline, weight, or aria-current). On narrow widths, the bar keeps the brand mark and one primary action visible.
- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_
- [OPTIONAL NOTES] **Users always know where they are and how to go back** — Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there. _(covers: current location marked; back restores state, URL / route reflects state)_

### hv5-g03-129
**Prompt:** the trading terminal's multi-window layout doesn't snap consistently between two ultrawide monitors

_Detected: mode ['responsive', 'audit'], platform ['kiosk']_

- [CORE] **Chart colour: categorical ≤8, colour-blind safe, plus shape/label** — One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette. _(covers: no colour alone for status)_
- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
- [CRITICAL GUARDRAILS] **Exceptions first: surface what needs attention in lists and tables** — Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-130
**Prompt:** audit every dialog in the app for consistent button ordering, some have OK/Cancel and some have Cancel/OK

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g03-131
**Prompt:** resizing the settings window below its minimum size just clips content instead of enforcing the minimum

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-132
**Prompt:** our macOS build's toolbar icons don't scale for retina, they look fuzzy compared to the sidebar

_Detected: mode ['create', 'audit'], platform ['desktop']_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Persistent left rail / sidebar** — Fixed-width rail (collapsible to icons with labels on hover/focus) holding grouped sections; secondary navigation lives in the content header, not as a second rail. Don't add a rail because 'apps have sidebars': justify it with section count and switching frequency. Mark active section with a visible indicator that survives collapse.
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [OPTIONAL NOTES] **Desktop: persist layout and selection state** — Restore the workspace on launch (per user, per view), offer 'reset layout', keep undo history per document, and never lose selection on data refresh (re-select by key). _(covers: persisted workspace and selection)_

### hv5-g03-133
**Prompt:** the accounting app's tab key order jumps around the form unpredictably, feels random

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Web: reserve space, load fonts and images without shift** — width/height or aspect-ratio on every media element, font-display: swap with size-adjust or a metric-compatible fallback, preload the display font and LCP image, skeletons match final dimensions, sticky elements don't push content. Target CLS < 0.1, LCP < 2.5 s. _(covers: no layout shift, image sizing and formats)_

### hv5-g03-134
**Prompt:** does alt+tab preview show a frozen thumbnail of the app or the actual last frame

_System declined (out of scope): UI design / interaction task_

### hv5-g03-135
**Prompt:** the property inspector panel in the design tool can't be undocked, it's stuck to the side

_System declined (out of scope): UI design / interaction task_

### hv5-g03-136
**Prompt:** why does closing the last document window quit the whole app instead of just closing the window

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g03-137
**Prompt:** the CAD tool's context menu for a selected object overlaps the object itself, obscuring what you're editing

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g03-138
**Prompt:** review the entire preferences window for consistency, some tabs use sliders and some use text fields for the same kind of value

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [OPTIONAL NOTES] **Users always know where they are and how to go back** — Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there. _(covers: current location marked; back restores state, URL / route reflects state)_

### hv5-g03-139
**Prompt:** the print dialog's default paper size resets every session even after the user changes it

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g03-140
**Prompt:** one label rename on the export button, currently it just says Go

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [OPTIONAL NOTES] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g03-141
**Prompt:** the Avalonia data grid doesn't show a loading state during a long filter operation, app just looks frozen

_Detected: mode ['audit', 'refactor'], platform ['desktop']_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g03-142
**Prompt:** does the app respect Windows high-DPI scaling on a 4K external monitor plugged into a laptop

_Detected: mode ['audit', 'responsive'], platform ['desktop']_

- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-143
**Prompt:** the inventory tool's toolbar buttons don't have tooltips, new hires have no idea what half of them do

_System declined (out of scope): UI design / interaction task_

### hv5-g03-144
**Prompt:** our Electron packaging ships a completely different font stack than the design spec used, everything looks off

_Detected: mode ['polish', 'audit'], platform ['desktop']_

- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-145
**Prompt:** why does the app's own scrollbar style clash with the OS scrollbar in the same window

_System declined (out of scope): UI design / interaction task_

### hv5-g03-146
**Prompt:** the WPF app's splash screen blocks input for three seconds after the window is already interactive

_Detected: mode ['audit', 'responsive'], platform ['desktop']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [OPTIONAL NOTES] **Windows: Fluent layering and materials, sparingly** — Use the system resources (SystemControl*, Layer/Card brushes, ControlCornerRadius) so light/dark/high-contrast themes work; Mica for the window, Acrylic only for transient surfaces; verify high-contrast mode renders every state. _(covers: Fluent system resources and materials)_

### hv5-g03-147
**Prompt:** check whether right-click on the taxonomy tree in the CMS admin tool offers move-here as an option or only copy

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Tree view** — Full APG tree semantics (roles tree/treeitem/group, aria-expanded, aria-level), arrow keys expand/collapse/move, type-ahead, multi-select with Shift/Ctrl where needed, lazy children with a loading indicator, virtualised for large trees, indentation lines optional but consistent, drag/drop with a keyboard alternative. _(covers: tree view semantics, virtualization of long collections)_
- [CORE] **Tree + breadcrumb for deep hierarchies** — Tree in the left pane with full keyboard semantics (arrow keys expand/collapse, type-ahead), breadcrumb above the content that mirrors the tree path and is clickable at every level. Persist expansion state per session. Virtualise beyond ~500 nodes. _(covers: tree view semantics, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_

### hv5-g03-148
**Prompt:** the multi-select in the asset manager loses selection state if you scroll too far

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Every interactive colour has hover/pressed/focus/disabled/selected** — Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them. _(covers: visible focus, selected state visible and distinct from focus and hover)_

### hv5-g03-149
**Prompt:** does the native notification for a completed export actually link back to the file location on click

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_

### hv5-g03-150
**Prompt:** audit the whole app's window chrome, menus, dialogs, and shortcuts against the platform's own HIG

_Detected: mode ['audit', 'responsive'], platform ['web']_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g04-001
**Prompt:** checkout button disappears behind the keyboard on the reorder screen

_Detected: mode ['refactor', 'audit'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g04-002
**Prompt:** SwiftUI list scroll stutters when the offline banner is visible

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_
- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_
- [CRITICAL GUARDRAILS] **Virtualise long lists and tables** — Windowed rendering with stable row heights or measured heights, keyboard focus preserved when rows unmount (roving focus by key), aria-rowcount/aria-setsize so assistive tech knows the real size, scroll restoration on back navigation. Native: LazyColumn/List/FlatList/VirtualizingStackPanel already virtualise; keep keys stable. _(covers: virtualization of long collections)_

### hv5-g04-003
**Prompt:** users on the ward keep fat-fingering the med dose stepper

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g04-004
**Prompt:** add a pull-to-refresh to the shipment tracker

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-005
**Prompt:** the safe area padding is wrong on notch phones in landscape

_Detected: mode ['responsive', 'audit'], platform ['mobile']_

- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Mobile: safe areas and system insets** — Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view. _(covers: safe areas and notches)_

### hv5-g04-006
**Prompt:** Compose recomposition tanks fps when the cart badge updates

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g04-007
**Prompt:** gesture to dismiss the bottom sheet fights with the back swipe

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [OPTIONAL NOTES] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_
- [OPTIONAL NOTES] **Mobile: primary actions in thumb reach** — Frequent actions in the bottom third; top-left/right for rare actions (back, settings); large phones make top targets a two-handed reach so provide bottom alternatives (bottom search bar, pull-down). Sheets and menus open from the bottom. _(covers: thumb reach)_

### hv5-g04-008
**Prompt:** fix the tab bar overlap with the home indicator on iPhone

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Bottom tab bar** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination. _(covers: platform navigation grammar)_
- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Mobile: safe areas and system insets** — Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view. _(covers: safe areas and notches)_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

### hv5-g04-009
**Prompt:** onboarding carousel loses swipe position after backgrounding the app

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [OPTIONAL NOTES] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_

### hv5-g04-010
**Prompt:** the loyalty card screen renders tiny text under the max Dynamic Type setting

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Support text scaling and reflow** — Web: rem units, 200% zoom without loss, reflow at 320 px without horizontal scroll. iOS: Dynamic Type styles, test at AX sizes. Android: sp units, test at 200% font scale. Windows: text scaling 100–225%. Containers grow with text; truncation shows the full text on focus or in a detail. _(covers: dynamic type / text scaling)_
