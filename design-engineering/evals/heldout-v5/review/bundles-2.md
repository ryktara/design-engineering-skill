### hv5-g01-089
**Prompt:** Something's wrong with focus order on the payment form, tab jumps around.

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Web: reserve space, load fonts and images without shift** — width/height or aspect-ratio on every media element, font-display: swap with size-adjust or a metric-compatible fallback, preload the display font and LCP image, skeletons match final dimensions, sticky elements don't push content. Target CLS < 0.1, LCP < 2.5 s. _(covers: no layout shift, image sizing and formats)_
- [OPTIONAL NOTES] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g01-090
**Prompt:** The player profile page shows stale stats after a match ends.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-091
**Prompt:** Fix the export button, it triggers twice if you double click by accident.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_

### hv5-g01-092
**Prompt:** The member profile card cuts off long names instead of wrapping.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [OPTIONAL NOTES] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g01-093
**Prompt:** On the shop floor screen the alarm banner never clears even after the fix is logged.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Interruptive upsells and promo banners** — Never block a task with a promotion; place promos in reserved space so content does not shift; make them dismissible with a persistent memory of the dismissal; keep them out of the DPAD/keyboard path on TV and desktop (not the first focus); never mimic system dialogs or error styling; cap frequency. On shared or public screens keep promotional copy non-personal. _(covers: no interruptive upsells, no layout shift)_

### hv5-g01-094
**Prompt:** The comparison chart on the energy dashboard mislabels the axes after a resize.

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g01-095
**Prompt:** From the sofa, the remote control app lags a full second behind button presses.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_
- [OPTIONAL NOTES] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g01-096
**Prompt:** The event log screen truncates entries instead of scrolling.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-097
**Prompt:** The claim form loses everything typed if you rotate the phone.

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_

### hv5-g01-098
**Prompt:** Fix the confirmation modal, it closes itself before the user can read it.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g01-099
**Prompt:** Warehouse staff say scanning a code sometimes adds the item twice.

_System declined (out of scope): not a UI design task: data work (warehouse) without a UI design, interaction or accessibility requirement_

### hv5-g01-100
**Prompt:** The poster-sized print preview shows the wrong bleed margins.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-101
**Prompt:** The badge kiosk print queue jams if two visitors check in within a second.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-102
**Prompt:** Fix the focus ring color on the primary button, it's invisible on dark mode.

_Detected: mode ['accessibility', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **TV: dark-first colour with restrained saturation** — Dark tinted canvas, text at 87–92% white, accent used for focus and primary only, semantic colours checked at ≥4.5:1 on dark, gradients dithered or avoided (banding on 8-bit panels), test in 'Standard' picture mode on a real panel. _(covers: dark-first TV palette, high contrast)_

### hv5-g01-103
**Prompt:** The itinerary screen reorders days wrong when you drag past the last item.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g01-104
**Prompt:** Students say the quiz timer keeps running after they submit.

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g01-105
**Prompt:** Fix the one label on the delete confirmation, it says 'Confirm' instead of what it deletes.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g01-106
**Prompt:** The loyalty tier comparison screen shows last month's points, not current.

_Detected: mode ['brand', 'audit'], platform UNKNOWN_

- [CORE] **Progress to target → bullet / progress bar, not gauge** — Bullet graph: measure bar, target tick, qualitative bands in greys; label the value and target numerically; multiple bullets align for comparison; progress bars must show the numeric value and the whole. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CRITICAL GUARDRAILS] **Semantic colour tokens, not raw hex in components** — Three layers: primitive palette → semantic roles (bg.canvas, text.primary, action.primary, border.default, focus.ring, feedback.error…) → component tokens where needed. Every theme (light, dark, high-contrast, each brand) redefines only the semantic layer. Validate with tokens.py validate. _(covers: semantic token layers per theme)_
- [CRITICAL GUARDRAILS] **Brands that differ only by logo, primary colour, and font** — Run fingerprint.py compare on the candidate brand systems; a COSMETIC-ONLY verdict fails differentiation. Vary at least two structural axes (navigation model, layout topology, density, surface strategy, image strategy, metadata density, CTA strategy) per brand, then cosmetics. _(covers: structural, not cosmetic, brand differentiation)_

### hv5-g01-107
**Prompt:** Something's wrong with the split billing screen, rounding leaves a cent unaccounted.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-108
**Prompt:** The dispatch board loses the driver's assigned zone after a refresh.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-109
**Prompt:** Fix the button order on the save dialog, cancel and confirm are swapped from usual.

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g01-110
**Prompt:** The pharmacy interaction alert dismisses on tap instead of requiring acknowledgment.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Exceptions first: surface what needs attention in lists and tables** — Compute the status in the model and show it as a column or badge with a word plus icon plus colour; sort or group exceptions first (or offer a one-tap 'only overdue' filter); show a count in the header/status bar; keep the row otherwise unchanged so scanning stays fast; state the rule that makes an item an exception (e.g. '> 90 days since service'). _(covers: exceptions and anomalies first, no colour alone for status, glanceable status, tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g01-111
**Prompt:** The clinic intake form validates the phone field wrong for international numbers.

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g01-112
**Prompt:** Fix the spacing value between the price and the strike-through price, they're touching.

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g01-113
**Prompt:** The tab for shipment history shows the wrong carrier icon sometimes.

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_

### hv5-g01-114
**Prompt:** In the van, the delivery confirmation screen doesn't save signatures offline.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_

### hv5-g01-115
**Prompt:** The overlay for the tutorial won't dismiss on some devices, blocks the whole app.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-116
**Prompt:** Fix the one color on the low-stock badge, it's the same red as the error state.

_Detected: mode ['polish', 'refactor'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g01-117
**Prompt:** The seating plan tool for teachers doesn't save if you switch classes mid-edit.

_System declined (out of scope): UI design / interaction task_

### hv5-g01-118
**Prompt:** Something's broken in the recipe screen, the serving size stepper goes negative.

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_

### hv5-g01-119
**Prompt:** The card reader terminal screen shows approved before the transaction actually clears.

_Detected: mode ['polish', 'audit'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [OPTIONAL NOTES] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_

### hv5-g01-120
**Prompt:** Fix the screen reader label on the mute icon, it just says 'button'.

_Detected: mode ['accessibility', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g02-001
**Prompt:** the totals never line up once you scroll past ten rows

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_

### hv5-g02-002
**Prompt:** tapping the tab twice sometimes opens two button row

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_

### hv5-g02-003
**Prompt:** the tab key skips over the tab labeled recent

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g02-004
**Prompt:** should this single label be bold or regular

_System declined (out of scope): UI design / interaction task_

### hv5-g02-005
**Prompt:** the confirm dialog is unreadable behind the counter

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-006
**Prompt:** our tab bar keeps showing stale data after the sync finishes

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g02-007
**Prompt:** the search box eats the first keystroke, users are complaining

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_

### hv5-g02-008
**Prompt:** the landscape view in React freezes when the list has more than a few hundred rows

_Detected: mode ['responsive', 'audit'], platform ['web']_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CORE] **List rows** — Row height from the density token (48–72 dp), whole row tappable with one accessible name, trailing chevron only when it navigates, swipe actions mirrored by a visible menu.
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_

### hv5-g02-009
**Prompt:** the back button sometimes lands on the wrong tab

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g02-010
**Prompt:** the settings screen doesn't collapse right after you delete the last row

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_

### hv5-g02-011
**Prompt:** the price updates but the total below it doesn't, until you tap away

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-012
**Prompt:** the card overlaps the legend on some builds and not others

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g02-013
**Prompt:** the loading overlay stays up even after the player overlay closes

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g02-014
**Prompt:** the sort order resets itself after you filter

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g02-015
**Prompt:** the notification badge count is off by one, always one

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_

### hv5-g02-016
**Prompt:** the modal traps focus but the close button is unreachable at the bedside

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g02-017
**Prompt:** the card component flickers before settling into place

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_

### hv5-g02-018
**Prompt:** the pagination breaks when there's exactly one page of results

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g02-019
**Prompt:** the drag handle only works on the second try

_Detected: mode ['refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g02-020
**Prompt:** the timestamp shows the wrong timezone for half our users

_System declined (out of scope): UI design / interaction task_

### hv5-g02-021
**Prompt:** the header silently drops the last edit if you navigate away too fast

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-022
**Prompt:** our React list view re-renders the whole screen on every keystroke

_Detected: mode ['audit', 'refactor'], platform ['web']_

- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g02-023
**Prompt:** the empty state shows even when there's data, just for a flash

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g02-024
**Prompt:** the form keeps its old label after the underlying record is renamed

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_

### hv5-g02-025
**Prompt:** the airport terminal map and the terminal window layout use the same green

_Detected: mode ['responsive', 'audit'], platform ['kiosk']_

- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g02-026
**Prompt:** what's the right corner radius for just this one card

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Flat tiles** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Pills for everything** — Pick one corner language for controls (small/medium radius) and reserve full-round for chips/badges; ≤2 badges per item; buttons and inputs share a radius; if everything is a pill, nothing reads as a tag. _(covers: one corner language for controls)_

### hv5-g02-027
**Prompt:** the card layout needs to show the payment card number masked

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_

### hv5-g02-028
**Prompt:** should the modal text be left or center aligned

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [OPTIONAL NOTES] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-029
**Prompt:** the landscape orientation cuts off the landscape photo thumbnail

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Mobile: image sizing, overdraw, and effect cost** — Request images at the rendered size (Coil/Glide/SDWebImage/expo-image with sizing), remove redundant opaque backgrounds (overdraw), keep list item composables/cells cheap and keyed, prefer opacity/transform animations, measure with the platform profiler (Perfetto, Instruments, Flipper). _(covers: image sizing and formats)_

### hv5-g02-030
**Prompt:** the status indicator in the profile page scrolls independently and it's disorienting

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_

### hv5-g02-031
**Prompt:** the member profile card doesn't match the gym membership card design

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_

### hv5-g02-032
**Prompt:** the toggle looks on but the setting underneath says off

_System declined (out of scope): UI design / interaction task_

### hv5-g02-033
**Prompt:** the tab bar state gets shared between two unrelated tabs somehow

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Mobile: follow the platform navigation grammar** — iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions. _(covers: platform navigation grammar)_

### hv5-g02-034
**Prompt:** the row height jumps around as data streams in

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Web: reserve space, load fonts and images without shift** — width/height or aspect-ratio on every media element, font-display: swap with size-adjust or a metric-compatible fallback, preload the display font and LCP image, skeletons match final dimensions, sticky elements don't push content. Target CLS < 0.1, LCP < 2.5 s. _(covers: no layout shift, image sizing and formats)_

### hv5-g02-035
**Prompt:** the terminal display ignores the last character typed before submit

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-036
**Prompt:** resizing the window breaks the terminal display layout permanently until reload

_System declined (out of scope): UI design / interaction task_

### hv5-g02-037
**Prompt:** the event log shows the previous user's data for a split second after switching accounts

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-038
**Prompt:** the progress bar reaches 100% and then jumps back to 40%

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-039
**Prompt:** the comparison chart label truncates mid-word instead of at a space

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g02-040
**Prompt:** what should the focus ring look like on the card

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Visible focus ring (web/desktop)** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element. _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g02-041
**Prompt:** the filter panel doesn't remember the last selected filter between sessions

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g02-042
**Prompt:** what color should the error label be

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Neutral canvas + one accent** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g02-043
**Prompt:** the dropdown on the settings screen sometimes shows two decimal points, sometimes none

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_

### hv5-g02-044
**Prompt:** the swipe-to-delete gesture triggers on a plain scroll in the control room

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_

### hv5-g02-045
**Prompt:** the user guide link is buried under the on-screen channel guide

_Detected: mode ['audit', 'refactor'], platform ['tv']_

- [CORE] **EPG / programme guide** — See the EPG grid pattern for structure; component specifics: cell shows title + time with ellipsis, minimum cell width so 5-minute programmes stay focusable (with a time label on focus), current programme highlighted and the 'now' line updates every minute, channel column sticky with logo + number, day picker above the grid, focus moves by programme not by pixel, long press or a key opens programme detail with record/remind actions, jump-to-now shortcut, mini preview of the focused channel optional. _(covers: pinned channel column and now marker, virtualization of long collections, D-pad focus reachability, live channel switching and mini guide, time navigation in the guide: now marker, jump by time and day)_
- [CORE] **Broadcast guide (TV)** — Top tabs (Live, Guide, Catch-up, Search), a fast EPG grid with a now-line and channel logos, landscape channel cards with live badges, condensed titles with tabular times, flat tonal surfaces so text stays legible over 200 channels, focus border + scale (no glow needed), mini-player while browsing. Identity via the guide's colour coding of genres and the channel-card treatment.
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **TV: exactly one visible focus at all times** — Set initial focus deterministically (first actionable content or Play on detail), restore focus to the previously focused item when returning, keep focus on screen (scroll into view), move focus to a sensible neighbour when the focused item is removed, and never rely on colour tint alone for the focused state. _(covers: focus restoration, visible focus, details screen with Play as default focus)_
- [CRITICAL GUARDRAILS] **TV: overscan-safe margins** — Keep interactive and text content ≥5% from edges: at the 960×540 dp design frame that is 48 dp horizontal and 27 dp vertical (Android guidance: up to 58/28 dp for maximum safety; tvOS: 60 pt sides, 60 pt top/bottom on the 1920×1080 frame). Let rails scroll under the margin so partial cards hint at more content. _(covers: TV safe margins)_
- [CRITICAL GUARDRAILS] **TV: 10-foot typography** — Body ≥24 sp (Android) / ≥29 pt (tvOS) at 1080p design scale, captions ≥20 sp, titles 32–48, display 57–72; sans with large x-height and open counters; short strings (titles ≤2 lines, synopsis ≤3 lines with expansion); avoid thin weights (<400) and light text on busy imagery; line height ≥1.3. _(covers: 10-foot typography, readable at distance)_

### hv5-g02-046
**Prompt:** why does closing the sidebar sometimes also close the checkout page behind it

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g02-047
**Prompt:** the input field accepts letters in a field that should be numeric only

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Placeholder as the only label** — Visible persistent label (above or floating with a real label element), placeholder only for format hints, placeholder contrast ≥4.5:1. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [OPTIONAL NOTES] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g02-048
**Prompt:** the card component shows duplicate icons after switching Vue themes

_Detected: mode ['polish', 'audit'], platform ['web']_

- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g02-049
**Prompt:** the event log screen and the calendar event log the same icon

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-050
**Prompt:** the settings screen keeps expanding every time you click it instead of toggling

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_

### hv5-g02-051
**Prompt:** the spacing between the tab and the footer feels cramped

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g02-052
**Prompt:** the headings on this screen all look the same weight, hard to tell what matters

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g02-053
**Prompt:** the comparison chart sits a few pixels off from the icon set above it

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g02-054
**Prompt:** line height on the body text feels too tight on the classroom projector

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-055
**Prompt:** the buttons on the report view are all different heights

_System declined (out of scope): UI design / interaction task_

### hv5-g02-056
**Prompt:** can you tighten up the alignment on the settings screen row

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
