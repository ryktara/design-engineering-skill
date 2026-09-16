### hv5-g02-145
**Prompt:** what's the right corner radius for just this one card

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Flat tiles** — One surface tone step above canvas, 4–8 px radius, no border unless contrast between tile and canvas is below ~1.2:1, consistent inner padding from the spacing scale.
- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Pills for everything** — Pick one corner language for controls (small/medium radius) and reserve full-round for chips/badges; ≤2 badges per item; buttons and inputs share a radius; if everything is a pill, nothing reads as a tag. _(covers: one corner language for controls)_

### hv5-g02-146
**Prompt:** review this report view like it's someone else's work, no favoritism

_System declined (out of scope): UI design / interaction task_

### hv5-g02-147
**Prompt:** check whether the member profile still makes sense now that the footer changed

_System declined (out of scope): UI design / interaction task_

### hv5-g02-148
**Prompt:** how does the dashboard read to someone seeing it for the first time

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_

### hv5-g02-149
**Prompt:** should the settings screen text be left or center aligned

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [OPTIONAL NOTES] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g02-150
**Prompt:** what should the focus ring look like on the player overlay

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Visible focus ring (web/desktop)** — One focus token (colour + width + offset) applied globally; never outline:none without a replacement; ring must remain visible on the accent surface (use a two-tone ring or offset); composite focus in tables/lists uses a cell/row highlight plus the ring on the active element. _(covers: visible focus)_
- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g02-151
**Prompt:** what color should the error label be

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **Neutral canvas + one accent** — Neutral scale with a slight brand tint (not pure grey), one accent used for ≤10% of the screen, feedback colours distinct from the accent by hue family (error must not be the accent's hue). Charts get their own categorical palette. Validate every pair with tokens.py.
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_

### hv5-g02-152
**Prompt:** review the admin console flow and note where a user might get stuck

_Detected: mode ['audit', 'review'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_

### hv5-g02-153
**Prompt:** what order should the two buttons go in on the card component

_Detected: mode ['create'], platform UNKNOWN_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CORE] **One primary action per screen** — Exactly one filled button per view, secondaries as outlined/text, destructive actions separated and confirmed, button label is a verb phrase naming the outcome ('Save changes'), disabled only with an explanation nearby. _(covers: one primary action per view)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [OPTIONAL NOTES] **Progress for background work: what, how far, what went wrong** — State what is happening in words ('Sending 2 of 3 · Photo …'), a determinate bar when the total is known, the current item, elapsed/remaining when useful; on failure name the item and the reason with a Retry action; on completion confirm briefly ('All sent · just now'); keep a stable-phrase live region that announces start, failure and completion once per run; keep the layout stable while the state changes. _(covers: progress indicator, live region status announcements, offline and sync states)_

### hv5-g02-154
**Prompt:** give the settings screen a once-over and call out the weakest part

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_

### hv5-g02-155
**Prompt:** one spacing value: how much gap under the toolbar

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Arbitrary spacing and misaligned edges** — Snap every value to the spacing scale, align left edges of text across components, use one inset per container type, check icon/text baseline alignment, and equalise gaps in repeated structures. This single fix does more for 'looks professional' than any colour change. _(covers: consistent spacing scale)_

### hv5-g02-156
**Prompt:** just need the right shade of gray for this one divider

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g02-157
**Prompt:** does the onboarding flow pull its weight, or could it be cut entirely

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_

### hv5-g02-158
**Prompt:** should the dropdown button say Cancel or Dismiss

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Menu / dropdown / context menu** — Opens on click/Enter/Space and on Shift+F10 / right-click for context menus, arrow keys move, type-ahead, Escape closes and restores focus, items are buttons/links with icons only where meaningful, destructive items separated at the end, disabled items stay visible with a reason, positions within the viewport. Mobile: bottom sheet or platform menu. _(covers: menu keyboard semantics and focus return)_

### hv5-g02-159
**Prompt:** take a hard look at the navigation drawer, is anything here just filler

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CORE] **Drawer / side panel** — Inline (pushes content) on wide screens, overlay on narrow; width from tokens (320–480 px); heading + close; focus moves in on open and returns on close; content scrolls independently; TV: side sheet that keeps the player/content visible and traps DPAD inside until BACK. _(covers: drawer / side panel focus in and out)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g02-160
**Prompt:** review the profile page once more before release and log every rough spot

_System declined (out of scope): UI design / interaction task_

### hv5-g03-001
**Prompt:** the focus ring disappears when you tab past the third filter chip on the claims dashboard

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g03-002
**Prompt:** screen reader announces the same balance twice on the account summary card, is that the live region duplicating?

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_

### hv5-g03-003
**Prompt:** can a nurse using VoiceOver actually tell which vitals row is out of range or does it just read the number

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g03-004
**Prompt:** contrast on the shipment status pills fails against the warehouse tablet's outdoor glare mode

_Detected: mode ['accessibility', 'responsive'], platform ['tablet']_

- [CRITICAL GUARDRAILS] **Field use: sunlight readability and glanceable status** — Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding). _(covers: high contrast outdoors / sunlight readability, glanceable status, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_

### hv5-g03-005
**Prompt:** keyboard trap in the modal that confirms a wire transfer, esc does nothing

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g03-006
**Prompt:** our SwiftUI onboarding flow skips VoiceOver rotor headings entirely, need those added back

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Native accessibility semantics (mobile/desktop)** — Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code. _(covers: semantic structure and roles, accessible names and labels)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_

### hv5-g03-007
**Prompt:** teacher portal grade cells: color is the only signal for late vs missing

_System declined (out of scope): UI design / interaction task_

### hv5-g03-008
**Prompt:** does the ballot review screen at the polling place meet target size for older voters with tremor?

_Detected: mode ['accessibility', 'review'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g03-009
**Prompt:** reduce motion setting is ignored by the parallax hero on the annual report site, it still spins

_Detected: mode ['audit', 'refactor'], platform ['web']_

- [CORE] **Landing hero** — The hero is a specific thesis: show the real product or outcome, one headline that a user could repeat, one primary action (a second only if it is a genuinely different path), proof close by (not a logo wall by default), LCP image optimised, text contrast guaranteed, no autoplay video without a poster and reduced-motion handling. Structure varies by product: a demo, a live widget, a number, a photograph, or a form can be the hero. _(covers: hero as a specific thesis with real proof, one primary action per view, image sizing and formats)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Every interactive colour has hover/pressed/focus/disabled/selected** — Define state tokens per role (action.primary-hover/-pressed, bg.selected, text.disabled), keep label contrast on every state, make disabled visibly weaker but readable (≥3:1 recommended even though exempt), selected ≠ focused ≠ hovered. Dark theme redefines all of them. _(covers: visible focus, selected state visible and distinct from focus and hover)_

### hv5-g03-010
**Prompt:** audit the checkout for anyone who can't use a mouse

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_

### hv5-g03-011
**Prompt:** one label missing on the search input in the recipe app, screen reader just says edit text

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g03-012
**Prompt:** the color contrast checker flagged 47 things in our Figma library and I don't know which ones actually matter for the factory floor kiosk

_Detected: mode ['accessibility', 'reconstruct'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [OPTIONAL NOTES] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-013
**Prompt:** tab order jumps from the search bar straight to the footer, skipping the whole results grid

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [OPTIONAL NOTES] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_

### hv5-g03-014
**Prompt:** someone on the ward asked why the medication alert sound has no visual equivalent

_Detected: mode ['audit'], platform ['mobile']_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_

### hv5-g03-015
**Prompt:** is 44px enough for the delete row button on a delivery driver's gloved thumb?

_Detected: mode ['audit'], platform ['mobile']_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Mobile: primary actions in thumb reach** — Frequent actions in the bottom third; top-left/right for rare actions (back, settings); large phones make top targets a two-handed reach so provide bottom alternatives (bottom search bar, pull-down). Sheets and menus open from the bottom. _(covers: thumb reach)_

### hv5-g03-016
**Prompt:** fix the Avalonia grid so JAWS reads column headers when you arrow down

_Detected: mode ['polish', 'refactor'], platform ['desktop']_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_

### hv5-g03-017
**Prompt:** the toast that confirms a refund vanishes in two seconds and screen readers never catch it

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g03-018
**Prompt:** students using switch access can't reach the submit button on the timed exam, focus loops back to the header

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g03-019
**Prompt:** why does the price drop badge only exist as a red dot with no text

_System declined (out of scope): UI design / interaction task_

### hv5-g03-020
**Prompt:** review the shift-swap form for anyone relying on high contrast mode in Windows

_Detected: mode ['audit', 'review'], platform ['desktop']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **Windows: Fluent layering and materials, sparingly** — Use the system resources (SystemControl*, Layer/Card brushes, ControlCornerRadius) so light/dark/high-contrast themes work; Mica for the window, Acrylic only for transient surfaces; verify high-contrast mode renders every state. _(covers: Fluent system resources and materials)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-021
**Prompt:** the flight status board announces gate changes with a beep only, deaf travelers get nothing

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_

### hv5-g03-022
**Prompt:** our React table has aria-sort on the wrong element, NVDA calls every column ascending

_Detected: mode ['accessibility', 'audit'], platform ['web']_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_

### hv5-g03-023
**Prompt:** polish the focus states across the entire admin console, not just the buttons

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CORE] **Analytical console** — Charts are the imagery; one chart palette; modules sized by importance not by a uniform card grid; dark-first tonal surfaces with the accent reserved for alerts and selection; large readable numerics; small multiples over spaghetti charts. Distinctiveness via chart mark style and a signature numeric typeface.

### hv5-g03-024
**Prompt:** warehouse pick screen text is 11px and nobody asked if that's readable under fluorescent lights

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g03-025
**Prompt:** the game's difficulty prompt uses only a color swap between easy and hard, colorblind players can't tell

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Player transport controls** — Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences. _(covers: auto-hide timing of player controls, accessible names and labels, subtitle and audio track selection reachable from the player)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g03-026
**Prompt:** can dyslexic operators actually parse the alarm log or is it a wall of monospace red text

_System declined (out of scope): no UI vocabulary found; not a UI design task as written_

### hv5-g03-027
**Prompt:** one focus ring color for the whole component library, currently it's blue on blue on the primary button

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g03-028
**Prompt:** the invoice PDF preview has no alt text for the chart, finance team flagged it in the WPF app

_Detected: mode ['audit', 'refactor'], platform ['desktop']_

- [CORE] **Two categorical axes × value → heatmap / matrix** — Sequential or diverging perceptual palette (viridis/cividis-style, or a two-hue diverging with a neutral midpoint at a meaningful value), cell values on hover/focus and optionally printed when cells are large, sorted rows/columns to reveal structure, colour scale legend with units. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_
- [OPTIONAL NOTES] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g03-029
**Prompt:** somebody using a screen reader on the pharmacy counter tablet got stuck in the barcode scan step

_Detected: mode ['accessibility', 'audit'], platform ['tablet']_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_

### hv5-g03-030
**Prompt:** does the seat map on the booking flow work for keyboard-only travelers or is it mouse-drag only

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Flows between states → Sankey / alluvial** — ≤~12 nodes, link width proportional to flow, node labels with totals, hover/focus isolates a path, consistent node ordering to reduce crossings, table alternative mandatory. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Drag and drop: affordance, feedback, keyboard alternative, no layout thrash** — Show a grip or lift affordance; on lift raise the item (shadow/scale) and move it with a transform only; show a snapped drop target with the value it will take (time slot, column); write state once on drop; provide a keyboard/button alternative (arrow keys or a 'Move to…' menu) with focus kept on the moved item; announce the result in a live region; Escape cancels; respect reduced motion. _(covers: discoverable gestures, keyboard navigation and focus order, live region status announcements, no layout shift)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_

### hv5-g03-031
**Prompt:** add skip-to-content on the government benefits portal, screen reader users hit 40 nav links first

_Detected: mode ['accessibility', 'create'], platform ['web']_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g03-032
**Prompt:** the referee's tablet during the match flashes a red card overlay with no sound cue

_Detected: mode ['responsive', 'audit'], platform ['tablet']_

- [CORE] **No card containers (dividers and spacing)** — Remove nested rounded rectangles; group with whitespace and a heading; use a single hairline between rows; only wrap something in a card when it needs its own boundary for tapping, dragging, or elevation. This is the biggest single lever against generic AI layouts. _(covers: no nested cards)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_

### hv5-g03-033
**Prompt:** why is the entire settings toggle row unlabeled except for an icon nobody can identify

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_

### hv5-g03-034
**Prompt:** line height on the terms and conditions modal is too tight for anyone with low vision zoomed to 200%

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g03-035
**Prompt:** the lab results table has merged cells that break screen reader navigation entirely, patients can't hear which value is theirs

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Numeric tables: alignment, figures, units, precision** — Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator. _(covers: tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_

### hv5-g03-036
**Prompt:** check whether the checkout error summary actually gets focus after a failed submit

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CORE] **Sticky action bar** — Bottom-fixed on mobile inside the safe area, sticky footer on desktop; content gets bottom padding equal to the bar height; the bar must not obscure a focused field (WCAG 2.4.11) so scroll the field into view above it. _(covers: thumb reach, one primary action per view, safe areas and notches)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Delivery promise and returns stated next to the price** — Under the price show the delivery window as dates ('Fri 11 – Tue 15 Sep', with <time>), the cost ('Free delivery'), a order-deadline countdown ('Order within 3 h to ship today') that updates without a live region, the return terms in one line ('Free 60-day returns · prepaid label'), and stock in words; repeat the promise in the cart and at checkout unchanged. _(covers: trust and cost transparency before commitment, readable line length)_
- [OPTIONAL NOTES] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_

### hv5-g03-037
**Prompt:** our Compose app's bottom sheet has no dismiss affordance for talkback, it's trapped

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_

### hv5-g03-038
**Prompt:** on the shop floor screen the emergency stop confirmation is a tiny checkbox, that seems wrong for someone in a hurry

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.

### hv5-g03-039
**Prompt:** one contrast fix on the low-stock badge, that's it

_Detected: mode ['accessibility', 'refactor'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g03-040
**Prompt:** librarian said the catalog search results read out of order with a screen reader, titles come after ratings

_Detected: mode ['accessibility'], platform UNKNOWN_

- [CORE] **Search field and results** — Prominent field with type=search, clear button, suggestions as a listbox with keyboard support, result count announced, query in the URL, recent searches, empty-result guidance, debounce. Mobile: full-screen search with the keyboard open and results as a list. TV: a dedicated search screen, system keyboard or voice, results in rails, focus returns to the field on BACK. _(covers: search field and results behaviour, URL / route reflects state)_
- [CORE] **Catalog grid** — Responsive columns from a minimum tile width (auto-fill/minmax), consistent aspect ratio per catalog, text under the image not over it unless contrast is guaranteed, and a filter/sort bar that stays reachable. Lazy-load images with reserved aspect boxes to avoid layout shift. _(covers: applied filters as removable chips with counts, pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g03-041
**Prompt:** make sure the donation form works for someone using Dragon voice control end to end

_Detected: mode ['refactor'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Form stack with sections** — Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_

### hv5-g03-042
**Prompt:** does anyone actually test the loan calculator with a screen magnifier at 400%?

_System declined (out of scope): UI design / interaction task_

### hv5-g03-043
**Prompt:** the drone control app has gesture-only zoom, pilots with limited hand mobility have no alternative

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Full-size photo viewer** — Thumbnails at least 2-up and decoded at display size × DPR; tap opens a full-screen viewer route (system back closes it) with pinch/double-tap zoom plus an explicit zoom button, labelled previous/next, retake/remove in the bar, dark chrome with high-contrast controls, and 48 dp targets; keep the report state when returning. _(covers: image sizing and formats, discoverable gestures, BACK behaviour, large touch targets (≥44–48 px))_
- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Target size by platform** — Web: ≥24×24 CSS px minimum (WCAG 2.5.8), 44×44 recommended for touch. iOS ≥44 pt, Android ≥48 dp, kiosk ≥60 px, desktop pointer ≥24 epx with 4–8 px spacing. Extend the hit area beyond the visual glyph rather than enlarging the icon. _(covers: large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_

### hv5-g03-044
**Prompt:** audit the whole intake form for cognitive load, not just contrast

_Detected: mode ['audit', 'accessibility'], platform UNKNOWN_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Trend aesthetics at the cost of usability** — Run every aesthetic choice through contrast, target size, focus visibility, platform input model, and reading distance before keeping it. Brand character must come from choices that pass, not from breaking them. _(covers: structure before style decision order, high contrast)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_

### hv5-g03-045
**Prompt:** the countdown timer on the exam page has no pause option and no aria-live announcement, students with ADHD panic

_Detected: mode ['accessibility', 'audit'], platform UNKNOWN_

- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Bypass blocks: skip links and landmark shortcuts** — Provide a 'Skip to <region>' link as the first focusable element (visible on focus), targets with tabindex=-1 and a heading; expose landmarks (main, nav, region with aria-label) so screen-reader users can jump; keep the number of tab stops before the first control small (≤ 5) and give composite widgets a single tab stop. _(covers: semantic structure and roles, keyboard navigation and focus order)_
- [CRITICAL GUARDRAILS] **Announce dynamic status changes** — Use a polite live region (role=status / accessibilityLiveRegion=polite / LiveSetting) with a complete phrase ('12 results for shoes'), assertive only for blocking errors; toasts stay ≥5 s or until dismissed and are also logged somewhere reachable. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Text contrast 4.5:1 (3:1 large)** — Body and label text ≥4.5:1, large text (≥24 px or ≥19 px bold) ≥3:1, AAA target 7:1 for long reading and for TV. Measure with tokens.py contrast, never estimate. Placeholder text is text and must pass. _(covers: high contrast)_

### hv5-g03-046
**Prompt:** the sidebar just vanishes below 1024px, no hamburger, nothing

_Detected: mode ['audit', 'refactor'], platform UNKNOWN_

- [CORE] **Sidebar / navigation rail** — Grouped items with group labels, active item with indicator + aria-current, collapsible to icon rail with tooltips and accessible names, keyboard: Tab into the rail once then arrows, collapse state persisted, footer for account/settings, no more than two nesting levels; never a second rail for sub-navigation (use the content header). _(covers: rail / sidebar grouping, active indicator, collapse, current location marked; back restores state)_
- [CORE] **Empty / zero state** — Short heading stating the situation, one sentence of why/what next, one primary action (or none if nothing can be done), optional small meaningful illustration, same layout region as the content it replaces, and on TV a focusable action so focus is never lost. _(covers: loading, empty and error states)_

### hv5-g03-047
**Prompt:** does the claims table hold up in split view on an iPad or does it just get crushed to two columns

_Detected: mode ['audit'], platform ['tablet']_

- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [OPTIONAL NOTES] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_

### hv5-g03-048
**Prompt:** rotate the tablet at the check-in counter and the whole layout freezes mid-transition

_Detected: mode ['responsive', 'audit'], platform ['tablet']_

- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_

### hv5-g03-049
**Prompt:** the dashboard cards reflow fine until exactly 834px where two of them overlap

_Detected: mode ['refactor', 'responsive'], platform UNKNOWN_

- [CORE] **Bordered cards** — Border token with measured contrast, 6–8 px radius, header row with title and one action, body with a clear hierarchy; selectable cards (plans) use a stronger border + check mark, never colour alone.
- [CORE] **Dashboard grid of modules** — 12-column responsive grid, modules sized by importance (the primary KPI or chart spans wider), reading order = importance order (top-left first), each module a region with a heading and its own loading/empty/error states. Cards are optional: a divider grid with headings is often clearer than nested boxes.
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g03-050
**Prompt:** someone on the shop floor screen resized the browser window and the inventory grid just clipped off the right edge

_Detected: mode ['responsive', 'audit'], platform ['web']_

- [CORE] **Data table / grid** — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule. _(covers: selection state and bulk actions, inline editing, virtualization of long collections, tabular figures and numeric alignment, pagination / load-more strategy, selected state visible and distinct from focus and hover)_
- [CORE] **Utility commerce** — Search and filters dominate the header, product tiles with price and the deciding fact, comparison-friendly metadata, sticky add-to-cart on PDP, brand colour on action and header only, humanist sans for long product names and multilingual catalogues. Identity via tile geometry, price typography, and the filter chip language.
- [CRITICAL GUARDRAILS] **Numeric tables: alignment, figures, units, precision** — Right-align numbers with tabular lining figures, one precision per column, unit in the header not each cell, negative values with sign and colour (and parentheses in finance if house style), thousands separators by locale, totals visually distinct, sortable columns with an explicit sort indicator. _(covers: tabular figures and numeric alignment)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_

### hv5-g03-051
**Prompt:** what happens to the chart legend when the window gets narrower than 600px in the Electron build?

_Detected: mode ['create'], platform ['desktop']_

- [CORE] **Two categorical axes × value → heatmap / matrix** — Sequential or diverging perceptual palette (viridis/cividis-style, or a two-hue diverging with a neutral midpoint at a meaningful value), cell values on hover/focus and optionally printed when cells are large, sorted rows/columns to reveal structure, colour scale legend with units. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **Real-time streams → rolling window charts** — Fixed time window that scrolls, stable y-range with occasional stepwise rescale, no per-point animation, thresholds drawn as lines with labels, alert states via colour + icon + text, pause on hover/focus, render on canvas/WebGL beyond a few thousand points, and a 'last updated' timestamp. Wall/TV displays: larger type, fewer panels, high contrast. _(covers: real-time rolling window and thresholds, last-updated / refresh state, exceptions and anomalies first, no colour alone for status)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-052
**Prompt:** landscape mode on the gate agent's device shows the boarding list with half the rows cut off

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-053
**Prompt:** our Flutter app's grid doesn't adapt between phone and foldable, it just stretches ugly

_Detected: mode ['polish', 'audit'], platform ['mobile', 'tablet']_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_
- [OPTIONAL NOTES] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_

### hv5-g03-054
**Prompt:** test the patient chart across breakpoints, nurses use everything from a phone to a wall monitor

_Detected: mode ['responsive', 'audit'], platform ['mobile']_

- [CORE] **Part-to-whole → stacked bar, waffle, or (rarely) donut** — Prefer a single stacked horizontal bar or a waffle; a donut only with ≤4 parts, labels with percentages on or beside slices, the largest starting at 12 o'clock, colour-blind-safe palette, and never a 3D pie or exploded slices. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Sequential drop-off → funnel or step bars** — Horizontal bars per stage sorted by sequence with absolute counts and stage-to-stage conversion %, not a trapezoid whose area misleads; highlight the biggest drop; keep colours neutral with one emphasis. _(covers: chart form chosen from the analytical question, exceptions and anomalies first)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_

### hv5-g03-055
**Prompt:** the compare-two-files diff view collapses into a single column on any screen under 1400px and becomes unreadable

_Detected: mode ['review', 'accessibility'], platform UNKNOWN_

- [CORE] **Plan comparison and billing management** — Plans are a radio group of equal-width cards with the current plan marked in text (not colour only), prices with tabular figures and the billing period stated, a feature list with real text (no bare check marks without labels), and one primary action per state (Upgrade / Downgrade / Current); every card is one Tab stop with a visible focus ring, arrow keys move between plans; seat management is a data table (name, role, status, last active) with row actions reachable from the keyboard and a bulk selection state; invoice history is a table with date, amount (tabular), status text + icon and a real download link (not a hover-only icon); plan changes and seat removals confirm in a dialog that states the billing consequence and returns focus; billing settings sub-navigation is a vertical list with aria-current. _(covers: tabular figures and numeric alignment, one primary action per view, no colour alone for status, confirmation of destructive or high-risk actions, selection state and bulk actions, aligned comparison structure with one recommended choice)_
- [CORE] **Toast / snackbar / banner** — Toast: bottom (mobile) or bottom-left/top-right (desktop) consistent position, ≥5 s or until dismissed, undo where applicable, live region polite. Banner: inline at the top of the region it concerns, dismissible if non-critical. TV: brief overlay in the safe area that never steals focus. _(covers: live region status announcements)_
- [CRITICAL GUARDRAILS] **Native accessibility semantics (mobile/desktop)** — Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code. _(covers: semantic structure and roles, accessible names and labels)_
- [CRITICAL GUARDRAILS] **Desktop status bar as the persistent feedback surface, with next-error navigation** — One status bar at the bottom of the window with fixed regions (selection summary, sync/save state with timestamp, error count as a link, active filter) separated by real separators, not spaces; validation for the current row/cell is echoed there in words ('Line 50: Quantity must be greater than 0') and the error count opens a list; F8 / Shift+F8 (or the project's convention) walk to the next and previous error and move focus into the cell; error styling never paints over the value text (tint the cell background and keep ≥ 4.5:1 for the text); announce status changes with LiveSetting/UIA so screen readers hear them; the bar keeps its height at every window width. _(covers: inline validation messages and error recovery, live region status announcements, high contrast, keyboard shortcuts / accelerators, persisted workspace and selection)_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [OPTIONAL NOTES] **Respect reduced motion** — Query prefers-reduced-motion / UIAccessibility.isReduceMotionEnabled / Settings.Global.ANIMATOR_DURATION_SCALE / UISettings.AnimationsEnabled and remove non-essential motion, render final states immediately, stop auto-rotation. Never just speed animations up. _(covers: reduced motion)_

### hv5-g03-056
**Prompt:** at the airport check-in kiosk the language selector overlaps the continue button once you pick a longer language name

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Accessible names for every control and image** — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name). _(covers: accessible names and labels)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-057
**Prompt:** why does the map view refuse to shrink below its default size in split screen on the delivery app

_Detected: mode ['audit'], platform UNKNOWN_

- [CORE] **Geographic values → choropleth or symbol map** — Choropleth for rates with a sequential palette and ≤7 classes; symbol map for counts with area-scaled circles; equal-area projection; hover/focus tooltip with region name and value; always provide a ranked table alternative; load map data lazily. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_
- [CORE] **Trend over time → line / area** — Line per series with distinct style (colour + dash/marker), direct end labels instead of a legend where possible, y-axis from zero unless the domain justifies otherwise (say so), consistent time bucketing, downsample >1–2k points, hover/focus reveals values with a crosshair, area fill only for a single series or true cumulative data. _(covers: chart form chosen from the analytical question, accessible chart summary and table alternative)_

### hv5-g03-058
**Prompt:** resize the browser slowly on the pricing page and watch the columns fight each other

_Detected: mode ['responsive', 'audit'], platform ['web']_

- [CRITICAL GUARDRAILS] **Editable grids: make the current column and its unit unmistakable** — Mark the active column in the header (bar + strong text); show the unit as an affix inside the editor (EA suffix for quantities, currency prefix for money); use role-distinct formats (integers for counts, fixed decimals for money, unit in the header); bracket money columns with a stronger divider; validate implausible values (a price typed as a quantity) inline before commit. _(covers: tabular figures and numeric alignment, inline editing, inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Grids with row actions are one Tab stop** — Tab enters the grid once and leaves it once; arrow keys move between cells/rows (roving tabindex or a focus manager), Enter/Space activates the focused cell's action, Escape returns from an edited cell to navigation mode; row actions become reachable when the row or actions cell is focused and are also available from a row context/actions menu; a table with 24 rows must never produce 24 Tab stops per action column. Announce the current row/column (aria-rowindex/colindex or the platform's automation properties) and keep a visible focus indicator on the active cell. _(covers: keyboard navigation and focus order, visible focus, selection state and bulk actions, selected state visible and distinct from focus and hover)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
- [CRITICAL GUARDRAILS] **Hover reveals need a non-hover path** — Hover-revealed content must also appear on focus and be reachable by touch (persistent affordance, long-press, or an explicit menu). Tooltips: dismissible, hoverable, persistent (WCAG 1.4.13). Never put essential actions only in hover. _(covers: no hover dependence)_

### hv5-g03-059
**Prompt:** the WinUI settings pane doesn't collapse when the window is snapped to half the screen

_Detected: mode ['responsive', 'audit'], platform ['desktop']_

- [CORE] **Settings screen** — Grouped rows with clear labels and current values visible, toggles for booleans with immediate effect, pickers for enums, destructive actions at the end with confirmation, search for long settings, platform idiom (grouped lists on mobile, sections/panes on desktop, TV: vertical list with DPAD and a right-side value column). Save behaviour explicit (auto vs Save button). _(covers: settings grouped with visible current values, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_
- [CRITICAL GUARDRAILS] **Desktop: keyboard is a first-class input** — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows). _(covers: keyboard navigation and focus order, keyboard shortcuts / accelerators, visible focus)_

### hv5-g03-060
**Prompt:** does the inspection form on the tablet in the van adapt when someone props it up sideways?

_Detected: mode ['audit', 'responsive'], platform ['tablet']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CORE] **Photo capture field (take, retake, replace, remove)** — The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'. Tapping a thumbnail opens the photo full-size (zoomable, previous/next, retake/remove) so the capture can be checked before submitting. _(covers: large touch targets (≥44–48 px), offline and sync states, permission priming before the system prompt, accessible names and labels, unsaved-changes guard, image sizing and formats)_
- [CRITICAL GUARDRAILS] **Mobile: keyboard and input types** — Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms. _(covers: on-screen keyboard (IME) aware layout)_

### hv5-g03-061
**Prompt:** one spacing token change on the card grid gutter, nothing else

_Detected: mode ['polish', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **Cards inside cards, everything in a rounded box** — Justify each container: does the boundary mean something (tappable object, elevation, grouping that spacing cannot express)? If not, replace with headings, spacing, and hairline dividers. Never nest a card in a card; never wrap a single KPI number in a card just to make a grid. _(covers: no nested cards)_
- [OPTIONAL NOTES] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-062
**Prompt:** the classroom seating chart tool breaks entirely on a Chromebook's smaller viewport, buttons go off screen

_Detected: mode ['responsive', 'audit'], platform ['web']_

- [CORE] **Chart colour: categorical ≤8, colour-blind safe, plus shape/label** — One categorical palette for the product (Okabe-Ito or Tableau-10-like, ≤8), sequential for ordered, diverging with a neutral midpoint for signed; series also distinguished by line style/marker/direct label; verify with a deuteranopia simulation; dark theme variant of the palette. _(covers: no colour alone for status)_
- [CORE] **Compare categories → bar** — Horizontal bars for long labels, sorted by value unless order is meaningful, single colour (highlight one bar for emphasis), zero-based axis always, value labels at bar ends when space allows, grouped bars ≤3 groups, no 3D, no rounded bar ends that misstate length. _(covers: chart form chosen from the analytical question, KPI with comparison and precision)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_

### hv5-g03-063
**Prompt:** check the checkout flow at every standard breakpoint plus the weird 360x640 android devices

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CORE] **One-page checkout** — Order summary is visible on desktop (side column) and collapsible-but-present at the top on phones with the total always shown; guest checkout first, account optional; sections in the order contact → shipping → payment → review, each with a visible heading and inline validation on blur plus a focused error summary on submit; address fields use autocomplete attributes and correct input types/IME; the pay button states the amount, is disabled only while processing (with a visible status), and is protected against double submission; trust and cost information (shipping, tax) appears before payment, never as a surprise; progress is saved locally so a reload does not lose entries. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, confirmation of destructive or high-risk actions, saving, saved and conflict states, one primary action per view, trust and cost transparency before commitment)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_

### hv5-g03-064
**Prompt:** in the machine in the lobby, the touchscreen menu doesn't rescale when the enclosure ships with a taller panel variant

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g03-065
**Prompt:** the Svelte dashboard's charts render at a fixed pixel width regardless of container size

_Detected: mode ['audit', 'refactor'], platform ['web']_

- [CORE] **Two categorical axes × value → heatmap / matrix** — Sequential or diverging perceptual palette (viridis/cividis-style, or a two-hue diverging with a neutral midpoint at a meaningful value), cell values on hover/focus and optionally printed when cells are large, sorted rows/columns to reveal structure, colour scale legend with units. _(covers: chart form chosen from the analytical question, no colour alone for status)_
- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CRITICAL GUARDRAILS] **The default SaaS dashboard (sidebar + 4 KPI cards + chart + table)** — Start from the user's job: what decision or action happens here, how often, and what must be noticed first. Many 'dashboards' should be a table-first working screen, a queue, or a single chart with alerts. Choose navigation by section count, KPIs by decisions, charts by questions. If the result is a sidebar and four KPIs, be able to say why. _(covers: no template skeleton pages, exceptions and anomalies first, structure before style decision order)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Focus visible and not obscured** — Focus indicator ≥2 px with ≥3:1 contrast against adjacent colours and against the unfocused state; sticky UI gets scroll-padding so a focused control scrolls into clear view. On TV the indicator must be obvious at 3 m (scale + border/glow). Measure the focused-vs-unfocused state as a contrast ratio (≥ 3:1 between the two fills or a ring ≥ 3:1 against both); on TV the ring must subtend enough arc at 3 m (≥ 6 px at 1080p) and the focused fill may invert (light fill, dark label). _(covers: visible focus)_

### hv5-g03-066
**Prompt:** shrinking the window on the trading terminal makes the order book overlap the price ladder

_Detected: mode ['responsive', 'audit'], platform ['kiosk']_

- [CRITICAL GUARDRAILS] **Privacy on shared and public screens** — Assume onlookers: mask sensitive values by default with an explicit reveal (balances, medication, addresses), gate personal profiles and purchases behind a PIN on shared TVs, keep notifications and previews generic on shared screens, clear the session and screen on idle or sign-out (kiosks, waiting rooms), and never show one user's data while another profile is active. Announce masked values to assistive tech as masked, not as the value. _(covers: privacy of on-screen data on shared devices, session expiry and idle reset, masking of sensitive values with explicit reveal)_
- [CRITICAL GUARDRAILS] **One type scale with named roles** — Roles display/heading/title/body/label/caption/numeric with size, line height, weight, and letter spacing per role; body ≥16 px web/mobile, 14 desktop, 24 TV; numeric role uses tabular lining figures; headings use tighter line height (1.1–1.25) and body 1.4–1.6. Generate with tokens.py scale and map the roles to the framework's text styles. _(covers: tabular figures and numeric alignment, type roles and scale)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_
- [CRITICAL GUARDRAILS] **Spacing from one scale, grouping by proximity** — A geometric-ish scale (4/8/12/16/24/32/48/64), inside-group spacing smaller than between-group spacing (ratio ≥1.5×), alignment to a grid, consistent inset per container type, optical alignment for icons and text baselines. Inconsistent spacing is the most common 'unprofessional' signal. _(covers: consistent spacing scale)_
- [CRITICAL GUARDRAILS] **One clear focal point per screen** — Decide the screen's job and the one element that serves it; give that element the strongest size/contrast/position; demote everything else by one or two steps; navigation and chrome are quieter than content. On dashboards the focal point is the most important metric or the anomaly, not the page title. _(covers: visual hierarchy with one focal point, one primary action per view, exceptions and anomalies first)_

### hv5-g03-067
**Prompt:** how should the timeline component behave between a phone and a projector in the same conference room app?

_Detected: mode ['audit'], platform ['mobile']_

- [CORE] **Pagination vs infinite scroll vs load more** — Tables and admin lists: numbered pagination with page size and total; feeds: load-more or infinite scroll with scroll restoration and a way to link to items; catalogues: load-more; TV rails: lazy append at the rail end. Pagination is a nav landmark with aria-current on the page. _(covers: pagination / load-more strategy)_
- [CORE] **Mobile list and swipe actions** — Row ≥48 dp / 44 pt, leading avatar/icon optional, title + secondary line, trailing meta or chevron, dividers or spacing, swipe actions with labelled buttons and a menu equivalent, pull-to-refresh where data is live, sticky section headers for grouped lists, lazy lists with stable keys, selection mode via long press with a visible toolbar. _(covers: large touch targets (≥44–48 px), discoverable gestures, pagination / load-more strategy)_
- [CRITICAL GUARDRAILS] **Design empty, loading, error, and partial states** — Empty: what this is, why it is empty, one action. Loading: skeleton with final dimensions, then content; announce completion. Error: what failed, what to do, retry that works; keep entered data. Partial: show what loaded, mark what didn't. On TV, focus must land somewhere valid in each state. _(covers: loading, empty and error states)_

### hv5-g03-068
**Prompt:** the nurse call log wraps text badly once the window drops under 900px, dates get orphaned

_Detected: mode ['responsive', 'audit'], platform UNKNOWN_

- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-069
**Prompt:** on the ward the medication chart's columns don't reflow, they just get squeezed to unreadable widths

_Detected: mode ['responsive', 'accessibility'], platform ['mobile']_

- [CORE] **Chart container and interaction** — Title that states the question, unit and time range visible, legend as direct labels where possible, tooltip also keyboard-reachable (focusable points or a data table toggle), accessible summary text, consistent palette, responsive (reduce ticks, not data), empty/loading/error states, no animation beyond a single load transition and none on data refresh. Provide the data table or CSV. _(covers: no colour alone for status, chart form chosen from the analytical question, accessible chart summary and table alternative, loading, empty and error states)_
- [CORE] **KPI / stat tile** — Label, value with unit and tabular figures, comparison (vs previous period) with sign + arrow + colour, optional sparkline, consistent decimal precision, the most important KPI larger or first, no icon per tile unless it disambiguates, whole tile links to the detail. Avoid the 'four identical cards with big numbers and a gradient' default. _(covers: tabular figures and numeric alignment, KPI with comparison and precision, drill-down from summary to detail)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CRITICAL GUARDRAILS] **Mobile: density is bounded by touch** — Convert tables to list rows with the 2–3 deciding columns, put the rest in a detail screen; filters in a sheet with applied-filter chips; bulk actions via selection mode; numbers stay tabular; row height ≥48 dp. Dense on phone means fewer things, not smaller things. _(covers: column priority on narrow widths, large touch targets (≥44–48 px))_
- [CRITICAL GUARDRAILS] **Non-text contrast 3:1 for controls and focus** — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails. _(covers: high contrast, visible focus)_
- [CRITICAL GUARDRAILS] **Mobile: orientation changes and size classes** — Design for compact and regular width and for landscape height: keep the primary action and the bottom navigation on screen in both orientations (pin the action bar above the safe area, let content scroll), keep the same navigation model across orientations (tabs stay tabs, a rail may replace them only on regular width), preserve scroll position and form state on rotation, and verify with the keyboard open. _(covers: breakpoint matrix, navigation transforms across widths, safe areas and notches)_
- [CRITICAL GUARDRAILS] **Never colour alone** — Pair colour with text, icon, pattern, weight, or underline. Error fields get an icon and message; chart series get labels or line styles; links in prose get underlines; selected rows get a check or a border, not only a tint. _(covers: no colour alone for status, selected state visible and distinct from focus and hover)_
- [OPTIONAL NOTES] **Native accessibility semantics (mobile/desktop)** — Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code. _(covers: semantic structure and roles, accessible names and labels)_

### hv5-g03-070
**Prompt:** verify the onboarding wizard survives a window resize mid-step without losing form state

_Detected: mode ['responsive', 'review'], platform UNKNOWN_

- [CORE] **Wizard / stepper** — Step indicator with names and progress (list semantics, aria-current=step), Back never loses data, one primary action per step, review step before submit, resume support, each step a real page/route on web; TV: full-screen steps with default focus on the primary action. _(covers: progress indicator, saving, saved and conflict states, linear multi-step wizard)_
- [CORE] **Setup / progress checklist** — A persistent checklist with a progress summary ('3 of 6 done'), each item stating outcome, time estimate, and one action; completed items stay visible and collapsed; the list is dismissible once essentials are done and reachable again from help; items deep-link to the exact screen and return to the checklist; never block the product behind it. Announce progress changes to assistive tech; keep it out of the main content's focal position. _(covers: optional setup checklist, progress indicator)_
- [CORE] **Linear wizard / stepper** — Show step count and current step, allow going back without data loss, put one primary action per step, validate per step not at the end, and let completed steps be revisited. Save progress for flows longer than ~3 minutes. On TV, each step is a full screen with a single focused default action. _(covers: progress indicator, linear multi-step wizard)_
- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Desktop: layouts survive window resizing and DPI** — Define a minimum window size (e.g. 800×600 epx) and breakpoints (Windows: <641 small, 641–1007 medium, ≥1008 large epx); panes collapse in a documented order; use star/auto grid sizing, not absolute; test at 150% and 200% DPI; remember window size/position and pane widths per user. _(covers: breakpoint matrix, column priority on narrow widths)_

### hv5-g03-071
**Prompt:** the retail POS screen on a smaller register terminal cuts off the tender buttons entirely

_Detected: mode ['audit', 'refactor'], platform ['kiosk']_

- [CORE] **Form** — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields. _(covers: inline validation messages and error recovery, on-screen keyboard (IME) aware layout, autofill / input-type attributes per field, unsaved-changes guard)_
- [CRITICAL GUARDRAILS] **Form labels, errors, and recovery** — Label above or beside, never placeholder-only; error message next to the field, programmatically associated (aria-describedby / accessibilityHint / AutomationProperties.HelpText), with what is wrong and how to fix; move focus to the first error or the error summary on submit; keep entered data; autocomplete attributes for personal data; allow paste and password managers. _(covers: inline validation messages and error recovery)_
- [CRITICAL GUARDRAILS] **Kiosk: public, hurried, standing users** — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step. _(covers: large touch targets (≥44–48 px), privacy of on-screen data on shared devices, session expiry and idle reset)_

### hv5-g03-072
**Prompt:** our Vue storefront's filter drawer doesn't account for tablets in portrait, it renders as if it's mobile

_Detected: mode ['responsive', 'audit'], platform ['mobile', 'tablet', 'web']_

- [CORE] **Filter bar / faceted filters** — Desktop: filter row above the content with chips for applied filters; facets as popovers with checkboxes and counts; 'clear all'; results update with a count. Mobile: filter button with badge count opens a sheet; apply button; applied chips under the search field. Persist in URL. _(covers: applied filters as removable chips with counts, URL / route reflects state)_
- [CORE] **Dialog / modal** — Title as heading, one primary action, safe default for destructive confirmations, focus management per dialog rule, sized to content with max width, scroll inside the body not the page, Escape and close button, backdrop click closes only for non-destructive dialogs. Mobile: bottom sheet or full-screen; TV: full-screen with first focus on the safe action. _(covers: dialog focus management, confirmation of destructive or high-risk actions)_
- [CORE] **Drawer / side panel** — Inline (pushes content) on wide screens, overlay on narrow; width from tokens (320–480 px); heading + close; focus moves in on open and returns on close; content scrolls independently; TV: side sheet that keeps the player/content visible and traps DPAD inside until BACK. _(covers: drawer / side panel focus in and out)_
- [CRITICAL GUARDRAILS] **Search and filters: visible state and instant feedback** — Applied filters as removable chips with a 'clear all', result count announced, debounced query (≈300 ms) with a loading indicator, empty results suggest next steps, filter state in the URL/route, and on TV a search screen with a system keyboard/voice plus results as rails. _(covers: live region status announcements, applied filters as removable chips with counts, search field and results behaviour)_
- [CRITICAL GUARDRAILS] **Dialog focus management** — On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay. On TV the sheet opens with focus on the current value and BACK closes it and returns focus to the opener; on kiosks the dialog is full-width with the primary action within reach. _(covers: dialog focus management, focus restoration)_
- [CRITICAL GUARDRAILS] **Everything operable by keyboard, no traps** — Tab reaches every control in visual order; composite widgets use arrow keys with a roving tabindex so Tab is not consumed by every cell; Escape closes layers and returns focus to the invoker; nothing traps focus except a modal, and the modal itself must be escapable. Provide a keyboard alternative for every drag interaction. _(covers: keyboard navigation and focus order, no hover dependence)_
- [CRITICAL GUARDRAILS] **Web: content-driven breakpoints and a test matrix** — Use the project's breakpoints; test at least: narrowest supported (320–360), common phone (390), tablet (768–834), laptop (1280–1366), desktop (1536–1920), plus 200% zoom. Check clipping, overflow, wrapping, tap targets, hierarchy order, and that navigation and dialogs transform (drawer ↔ rail, sheet ↔ dialog). Prefer container queries for components. _(covers: breakpoint matrix, navigation transforms across widths)_
