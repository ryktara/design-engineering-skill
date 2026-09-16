### hv5-g04-011
**Prompt:** biometric unlock prompt appears before the splash finishes loading

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Only the happy state was designed** — Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_

### hv5-g04-012
**Prompt:** build a one-handed reachability mode for the transfer amount pad

_Detected: mode ['create'], platform ['mobile']_

- [CRITICAL GUARDRAILS] **Mobile: primary actions in thumb reach** — Frequent actions in the bottom third; top-left/right for rare actions (back, settings); large phones make top targets a two-handed reach so provide bottom alternatives (bottom search bar, pull-down). Sheets and menus open from the bottom. _(covers: thumb reach)_

### hv5-g04-013
**Prompt:** Flutter hot reload keeps resetting my scroll offset in the feed

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CORE] **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g04-014
**Prompt:** the barcode scanner view doesn't rotate when I flip the phone

_Detected: mode ['audit', 'refactor'], platform ['mobile']_

- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_

### hv5-g04-015
**Prompt:** offline mode banner covers the send button on the chat screen

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_
- [CRITICAL GUARDRAILS] **Only the happy state was designed** — Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_

### hv5-g04-016
**Prompt:** typing a coupon code the keyboard covers the apply button

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g04-017
**Prompt:** redesign the bottom nav for thumb reach on bigger phones

_Detected: mode ['refactor', 'create'], platform ['mobile']_

- [CORE] **Bottom tab bar** — 3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination. _(covers: platform navigation grammar)_
- [CRITICAL GUARDRAILS] **Mobile: primary actions in thumb reach** — Frequent actions in the bottom third; top-left/right for rare actions (back, settings); large phones make top targets a two-handed reach so provide bottom alternatives (bottom search bar, pull-down). Sheets and menus open from the bottom. _(covers: thumb reach)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [OPTIONAL NOTES] **Users always know where they are and how to go back** — Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there. _(covers: current location marked; back restores state, URL / route reflects state)_

### hv5-g04-018
**Prompt:** the swipe-to-approve gesture in the review app conflicts with the delete swipe

_Detected: mode ['review', 'audit'], platform ['mobile']_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g04-019
**Prompt:** audit the checkout flow for one-thumb usability on tall phones

_Detected: mode ['audit'], platform ['mobile']_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g04-020
**Prompt:** picker wheel for delivery time jumps two rows on release

_System declined (out of scope): UI design / interaction task_

### hv5-g04-021
**Prompt:** the loading spinner never stops on the nurse's handoff screen

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g04-022
**Prompt:** widget on the lock screen shows a stale balance after refresh

_System declined (out of scope): UI design / interaction task_

### hv5-g04-023
**Prompt:** the map pin cluster overlaps the search bar in portrait

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Geographic values → choropleth or symbol map** — Choropleth for rates with a sequential palette and ≤7 classes; symbol map for counts with area-scaled circles; equal-area projection; hover/focus tooltip with region name and value; always provide a ranked table alternative; load map data lazily. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g04-024
**Prompt:** polish the spacing between order rows on the tracking tab

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Tabs** — Tablist with roving tabindex (arrow keys switch, Tab moves into the panel), selected tab marked by more than colour, tab labels short, panel content lazy but state preserved, URL reflects the tab on web; TV: selection on focus with a delay or on SELECT (choose one, be consistent), DOWN enters content. _(covers: tabs with roving focus, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_

### hv5-g04-025
**Prompt:** haptic feedback fires twice when confirming the payment

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-026
**Prompt:** the app freezes on rotate during the video call screen

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Auto-rotating and timed content is controllable** — Pause/stop control, stop on focus/hover, keyboard next/previous, announce slide position; timeouts warn and allow extension; kiosks show a visible countdown before resetting. _(covers: session expiry and idle reset, reduced motion)_

### hv5-g04-027
**Prompt:** improve contrast on the low battery warning toast

_Detected: mode ['accessibility', 'refactor'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g04-028
**Prompt:** the drag-to-reorder for playlist items snaps back randomly on Android

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Mobile: gestures are shortcuts, not the only way** — Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action. _(covers: discoverable gestures)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g04-029
**Prompt:** why does the delivery app ask for location permission twice on first launch

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-030
**Prompt:** the split-bill screen rounds the last person's share wrong on small phones

_System declined (out of scope): UI design / interaction task_

### hv5-g04-031
**Prompt:** self-checkout screen times out mid-payment when a customer steps away

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-032
**Prompt:** gloves make the signature pad totally unresponsive at the loading dock kiosk

_Detected: mode ['refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_
- [OPTIONAL NOTES] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g04-033
**Prompt:** the machine in the lobby shows English only after a language reset

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-034
**Prompt:** build a walk-up directory kiosk for the hospital atrium

_Detected: mode ['create'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_

### hv5-g04-035
**Prompt:** sunlight glare washes out the queue number on the terminal in the yard

_Detected: mode ['create'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_

### hv5-g04-036
**Prompt:** add a countdown before the session resets on the ticket machine

_Detected: mode ['create'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Auto-rotating and timed content is controllable** — Pause/stop control, stop on focus/hover, keyboard next/previous, announce slide position; timeouts warn and allow extension; kiosks show a visible countdown before resetting. _(covers: session expiry and idle reset, reduced motion)_

### hv5-g04-037
**Prompt:** the parking payment kiosk keeps double-charging on slow taps

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-038
**Prompt:** redesign the self-service check-in for wheelchair users at the counter height

_Detected: mode ['refactor', 'create'], platform ['kiosk']_

- [CORE] **Public kiosk** — Attract screen → hub of large tiles → linear flows with one giant primary action, ≥60 px targets in the reach zone, ≥20 px text with high contrast for glare, brand colour on header and primary action, filled icons with labels, idle timeout with countdown, cancel always visible, audio/visual feedback. Identity via tile geometry, illustration, and the brand colour field.
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-039
**Prompt:** audit the museum info kiosk for language switching clarity

_System declined (out of scope): UI design / interaction task_

### hv5-g04-040
**Prompt:** the fare machine's card slot LED never lights up for return trips

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Bordered cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g04-041
**Prompt:** polish the idle screen animation on the lobby directory

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-042
**Prompt:** multi-language toggle on the check-in kiosk resets to default every timeout

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Internationalisation: expansion, RTL, formats** — Allow 30–50% text expansion (German, Finnish), test with pseudo-localisation, use logical CSS properties / start-end alignment, mirror navigation and progress in RTL, format dates/numbers/currency by locale, verify font coverage per script, keep tabular figures across locales. A language switch is one visible control on every screen of the flow, labelled in its own language (Español, not 'Spanish'); switching keeps the session, typed input, selection and focus, announces the change politely, and re-renders every label including error text. _(covers: text expansion and RTL)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-043
**Prompt:** the order kiosk touch targets are too small for gloved warehouse hands

_Detected: mode ['polish', 'audit'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [OPTIONAL NOTES] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_

### hv5-g04-044
**Prompt:** fix the receipt printer jam message that never clears from the screen

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g04-045
**Prompt:** the self-service scale at the returns counter freezes after a weight reading

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Public kiosk** — Attract screen → hub of large tiles → linear flows with one giant primary action, ≥60 px targets in the reach zone, ≥20 px text with high contrast for glare, brand colour on header and primary action, filled icons with labels, idle timeout with countdown, cancel always visible, audio/visual feedback. Identity via tile geometry, illustration, and the brand colour field.

### hv5-g04-046
**Prompt:** build a low-glare mode for outdoor payment terminals

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.
- [CRITICAL GUARDRAILS] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_

### hv5-g04-047
**Prompt:** the visitor badge kiosk print queue backs up during rush hour

_System declined (out of scope): UI design / interaction task_

### hv5-g04-048
**Prompt:** accessibility audit for the voting terminal's screen reader support

_Detected: mode ['accessibility', 'audit'], platform ['kiosk']_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Public kiosk** — Attract screen → hub of large tiles → linear flows with one giant primary action, ≥60 px targets in the reach zone, ≥20 px text with high contrast for glare, brand colour on header and primary action, filled icons with labels, idle timeout with countdown, cancel always visible, audio/visual feedback. Identity via tile geometry, illustration, and the brand colour field.
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [OPTIONAL NOTES] **Support text scaling and reflow** — Web: rem units, 200% zoom without loss, reflow at 320 px without horizontal scroll. iOS: Dynamic Type styles, test at AX sizes. Android: sp units, test at 200% font scale. Windows: text scaling 100–225%. Containers grow with text; truncation shows the full text on focus or in a detail. _(covers: dynamic type / text scaling)_

### hv5-g04-049
**Prompt:** the drive-through order screen font is unreadable from the car

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Trend aesthetics at the cost of usability** — Run every aesthetic choice through contrast, target size, focus visibility, platform input model, and reading distance before keeping it. Brand character must come from choices that pass, not from breaking them. _(covers: structure before style decision order, high contrast)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [OPTIONAL NOTES] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g04-050
**Prompt:** add a Braille-labeled keypad flow to the ATM screen

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **On-screen keypad / keyboard for kiosks** — Keys ≥ 64 px with ≥ 16 px gaps, one key = one accessible name ('Hyphen', 'Delete', 'Space'), the keypad is a role=group labelled by the field it edits; the value box is focusable and read back through a polite live region as it changes; a persistent format hint (not a placeholder) is tied to the field with aria-describedby and errors set aria-invalid with a specific message ('Day must be 1–31'); focus never falls to the page body after a tap (re-focus the equivalent key after a re-render); a physical keypad or scanner wedge writes into the same field (human-speed keys fill, Enter continues, bursts are treated as scans); masked entry for PINs with a visible dot per character; in accessible mode the keypad and value sit in the reach zone (lower part of the screen). _(covers: large touch targets (≥44–48 px), accessible names and labels, live region status announcements, inline validation messages and error recovery, focus restoration, masking of sensitive values with explicit reveal)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Data-entry grid (spreadsheet-like)** — Enter/Tab move predictably (configurable), F2 edits, Escape cancels, arrow keys move without editing, type-to-edit on a cell, lookup cells with a picker (F4), validation per cell with a visible marker and a summary, totals row, paste from spreadsheet, undo, row add via Enter on the last row, keyboard shortcuts documented in a help panel. _(covers: inline editing, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_

### hv5-g04-051
**Prompt:** the shop floor screen loses touch calibration after a shift change

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.

### hv5-g04-052
**Prompt:** review the timeout warning copy on the self-checkout for clarity

_Detected: mode ['audit', 'review'], platform ['kiosk']_

- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g04-053
**Prompt:** the airport terminal wayfinding map pinch-zoom doesn't work with gloves on

_Detected: mode ['accessibility', 'responsive'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-054
**Prompt:** the clinic check-in kiosk's insurance card scan step confuses walk-ins

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g04-055
**Prompt:** polish the button order on the vending machine's payment confirmation

_Detected: mode ['polish', 'audit'], platform ['kiosk']_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Only the happy state was designed** — Enumerate states per screen and per interactive component before implementation and verify each visually; test with long strings, zero items, 10k items, and slow networks. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g04-056
**Prompt:** why does our CI pipeline take 12 minutes to run the test suite

_System declined (out of scope): not a UI design task: infrastructure work (ci pipeline) without a UI design, interaction or accessibility requirement_

### hv5-g04-057
**Prompt:** the database migration for the orders table keeps timing out in staging

_System declined (out of scope): not a UI design task: data work (database, database migration, timing out) without a UI design, interaction or accessibility requirement_

### hv5-g04-058
**Prompt:** optimize the SQL query behind the dashboard's monthly report

_System declined (out of scope): not a UI design task: data work (sql) without a UI design, interaction or accessibility requirement_

### hv5-g04-059
**Prompt:** our webpack build size ballooned after the last dependency bump

_System declined (out of scope): not a UI design task: build tooling work (webpack) without a UI design, interaction or accessibility requirement_

### hv5-g04-060
**Prompt:** set up rate limiting on the checkout API

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Editorial storefront** — Photography full-bleed, asymmetric editorial grid, text-only navigation, serif or grotesk display with a quiet body, monochrome UI so product colour leads, hairline dividers instead of cards, crossfade transitions, one inline CTA per product. Identity via the grid rhythm, type pairing, and image crop language. Do not default to cream+serif+terracotta.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g04-061
**Prompt:** make the UI faster and also completely redesign it but don't change anything visible

_System declined (out of scope): UI design / interaction task_

### hv5-g04-062
**Prompt:** the load balancer keeps dropping websocket connections during deploys

_System declined (out of scope): not a UI design task: frontend runtime work (websocket) without a UI design, interaction or accessibility requirement_

### hv5-g04-063
**Prompt:** is React or Vue better for our team long term

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-064
**Prompt:** the Kubernetes pods for the reporting service keep restarting

_System declined (out of scope): not a UI design task: infrastructure work (kubernetes) without a UI design, interaction or accessibility requirement_

### hv5-g04-065
**Prompt:** write a migration script to backfill the missing user emails

_System declined (out of scope): not a UI design task: data work (migration) without a UI design, interaction or accessibility requirement_

### hv5-g04-066
**Prompt:** the redis cache invalidation logic is stale after five minutes

_System declined (out of scope): not a UI design task: frontend runtime work (cache invalidation, cache) without a UI design, interaction or accessibility requirement_

### hv5-g04-067
**Prompt:** audit our npm dependencies for known vulnerabilities

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-068
**Prompt:** the payment webhook from Stripe sometimes arrives out of order

_System declined (out of scope): not a UI design task: backend work (webhook) without a UI design, interaction or accessibility requirement_

### hv5-g04-069
**Prompt:** can you make the login screen both minimal and packed with more options

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g04-070
**Prompt:** the S3 bucket permissions are too open for the upload service

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-071
**Prompt:** review our git branching strategy for the mobile team

_Detected: mode ['audit', 'review'], platform ['mobile']_

- [CORE] **Product detail page (PDP)** — Above the fold on every viewport: product name, price (with tabular figures and any discount stated in words), primary image, variant selectors and one add-to-cart action; variant choice is a radio group with visible labels and a disabled-but-visible state for out-of-stock options; the add-to-cart button is sticky on phones without covering focused controls; shipping, returns and stock are stated next to the price, not in a tab; the gallery has fixed aspect boxes (no layout shift), keyboard-operable thumbnails and alt text per image; reviews show the distribution and a count, and stars always have a text value; secondary actions (wishlist, share, size guide) never compete visually with add-to-cart; the size guide opens as a dialog that returns focus. _(covers: one primary action per view, no layout shift, accessible names and labels, large touch targets (≥44–48 px), trust and cost transparency before commitment)_

### hv5-g04-072
**Prompt:** the GraphQL resolver for orders returns stale data intermittently

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CRITICAL GUARDRAILS] **Offline, sync, and connectivity states** — Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age. _(covers: offline and sync states, saving, saved and conflict states, last-updated / refresh state)_

### hv5-g04-073
**Prompt:** set up blue-green deployment for the checkout service

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Editorial storefront** — Photography full-bleed, asymmetric editorial grid, text-only navigation, serif or grotesk display with a quiet body, monochrome UI so product colour leads, hairline dividers instead of cards, crossfade transitions, one inline CTA per product. Identity via the grid rhythm, type pairing, and image crop language. Do not default to cream+serif+terracotta.
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g04-074
**Prompt:** the cron job that emails weekly reports silently failed last week

_System declined (out of scope): not a UI design task: backend work (cron) without a UI design, interaction or accessibility requirement_

### hv5-g04-075
**Prompt:** investigate why our Terraform apply keeps drifting from state

_System declined (out of scope): not a UI design task: infrastructure work (terraform) without a UI design, interaction or accessibility requirement_

### hv5-g04-076
**Prompt:** the analytics events aren't firing in the right order

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-077
**Prompt:** make the settings page snappy without touching any code

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_

### hv5-g04-078
**Prompt:** our OAuth token refresh logic sometimes loops forever

_System declined (out of scope): not a UI design task: backend work (token refresh, oauth) without a UI design, interaction or accessibility requirement_

### hv5-g04-079
**Prompt:** the build pipeline caches an old bundle after a hotfix

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-080
**Prompt:** is it better to use microservices or a monolith for this feature

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-081
**Prompt:** the message queue backs up when the worker pool is small

_System declined (out of scope): not a UI design task: backend work (worker) without a UI design, interaction or accessibility requirement_

### hv5-g04-082
**Prompt:** fix the bug

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-083
**Prompt:** tighten the CORS policy on the internal admin API

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Developer tool** — Command palette as the accelerator, three-pane workbench with resizable panes, bordered surfaces on a dark or light neutral canvas, monospace for values and a compact sans for chrome, syntax-style accent colours used semantically (status, diff), keyboard shortcuts shown everywhere. Identity via the monospace face, the accent, and pane framing.
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_

### hv5-g04-084
**Prompt:** the feature flag service returns different values per region

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-085
**Prompt:** rewrite the auth middleware to support multi-tenant orgs

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-086
**Prompt:** why is our Docker image so much bigger than last quarter

_System declined (out of scope): not a UI design task: infrastructure work (docker) without a UI design, interaction or accessibility requirement_

### hv5-g04-087
**Prompt:** the search index falls out of sync with the product catalog

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g04-088
**Prompt:** review our on-call rotation and alerting thresholds

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-089
**Prompt:** the same test flaked twice this week on the same assertion

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-090
**Prompt:** make it feel more premium

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-091
**Prompt:** the API rate limiter throttles legitimate retries too aggressively

_System declined (out of scope): not a UI design task: backend work (api) without a UI design, interaction or accessibility requirement_

### hv5-g04-092
**Prompt:** our logging pipeline drops half the events under load

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g04-093
**Prompt:** should we use REST or gRPC for the internal service mesh

_System declined (out of scope): not a UI design task: backend work (rest) without a UI design, interaction or accessibility requirement_

### hv5-g04-094
**Prompt:** the deploy script hardcodes a staging URL that broke prod

_System declined (out of scope): not a UI design task: infrastructure work (deploy) without a UI design, interaction or accessibility requirement_

### hv5-g04-095
**Prompt:** do the thing we talked about last time

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_
