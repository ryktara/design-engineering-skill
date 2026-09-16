# Accessibility as a design constraint

Accessibility decisions happen while choosing structure, states, and tokens, not in a final pass. This file gives the requirements by platform and the deterministic checks that replace estimation. Standards: WCAG 2.2 for web and web-based UI; platform accessibility guidance for native. Provenance for each rule is in the knowledge records (`advise.py search "<topic>" --kind rule`).

## Contents
- Non-negotiables on every platform
- Web (WCAG 2.2 AA baseline)
- Mobile (iOS / Android / cross-platform)
- TV / remote
- Desktop (Windows / macOS)
- Kiosk
- Deterministic checks
- Audit procedure

## Non-negotiables on every platform

- Contrast: text ≥4.5:1 (large ≥3:1); non-text UI boundaries, focus indicators, meaningful icons, chart marks ≥3:1. Measure with `tokens.py contrast`.
- Colour is never the only carrier of meaning: add text, icon, pattern, weight, or underline.
- Every control has an accessible name that contains its visible label; every meaningful image has a text alternative; decorative ones are hidden.
- Every action is reachable with the platform's non-pointer input (keyboard, DPAD, switch access, screen-reader gestures).
- Focus is visible where focus exists, never obscured by sticky UI, and returns to the invoker when layers close.
- Text scales (browser zoom, Dynamic Type, font scale, Windows text scaling) without loss; containers grow.
- Motion respects reduced-motion settings; auto-rotating or timed content is pausable/extendable.
- Forms: visible labels, associated errors with recovery guidance, no data loss, autofill allowed, no re-entry of known data, no cognitive-test authentication.
- Status changes are announced (live regions / platform announcements) without stealing focus.
- Target sizes meet the platform minimum (below).

## Web (WCAG 2.2 AA baseline)

- Semantic structure: one h1, ordered headings, landmarks (`main`, `nav`, `aside`), real `button`/`a`/`table`, lists for lists, `th scope` in data tables.
- Keyboard: Tab order = visual order; composite widgets (tabs, grids, trees, menus, toolbars, listboxes) use arrow keys with a roving tabindex per the ARIA Authoring Practices; Escape closes layers; no focus traps outside modals; keyboard alternative for every drag (2.5.7).
- Focus: `:focus-visible` ring ≥2 px, ≥3:1 against adjacent colours and against the unfocused state (2.4.7, 2.4.11 not obscured, 2.4.13 AAA appearance); `scroll-padding` under sticky headers; never `outline: none` without a replacement.
- Targets: ≥24×24 CSS px minimum (2.5.8), 44×44 recommended for touch.
- Hover content: dismissible, hoverable, persistent (1.4.13); hover-revealed actions also appear on focus and have a touch path.
- Dialogs: `<dialog>`/`showModal()` or a tested library; focus moves in, background inert, focus returns.
- Live regions: `role="status"` for polite updates, assertive only for blocking errors (4.1.3).
- Reflow at 320 px without horizontal scroll (1.4.10); 200% zoom; text spacing overrides (1.4.12).
- Consistent help placement (3.2.6); redundant entry avoided (3.3.7); accessible authentication (3.3.8).
- Automated checks (axe, Lighthouse, eslint-plugin-jsx-a11y) catch ~30–40% of issues; keyboard and screen-reader passes are still required.

## Mobile (iOS / Android / cross-platform)

- Targets: iOS ≥44 pt, Android ≥48 dp with ≥8 dp spacing; extend the hit area, not the glyph.
- Semantics: SwiftUI `accessibilityLabel/Value/Hint/AddTraits`, Compose `semantics { contentDescription; role; heading() }` and `mergeDescendants`, Flutter `Semantics`, React Native `accessibilityRole/Label/State`. Custom tappable containers without a role are defects.
- Screen readers: VoiceOver/TalkBack focus order = visual order; group card contents into one element; announce async status (`UIAccessibility.post`, `announceForAccessibility`, `LiveRegionMode`).
- Text scaling: Dynamic Type text styles / `sp` units; test at the largest accessibility sizes; no fixed-height containers for text; truncation reveals the full value.
- Gestures are shortcuts: every swipe/long-press action has a visible equivalent (2.5.1); respect system back/home gestures.
- Reduced motion: `UIAccessibility.isReduceMotionEnabled`, `Settings.Global.ANIMATOR_DURATION_SCALE`, `MediaQuery.disableAnimations`, `AccessibilityInfo.isReduceMotionEnabled`.
- Keyboard and switch access: leave platform focus visuals enabled; test with a hardware keyboard on iPadOS/Android.
- Colour and contrast: same ratios as web; dark mode re-validated; "Increase Contrast" / high-contrast text settings respected.

## TV / remote

- Exactly one focused element, always on screen, deterministic initial focus, restored focus on return, focus reassigned when the focused item is removed.
- Focus indication: scale (1.05–1.1) plus border or glow ≥3:1 so it survives any artwork; never tint alone.
- Straight-path DPAD reachability for every control; no diagonal, no hidden hops; vertical = sections, horizontal = items.
- Text ≥24 sp body at the 1080p design frame, ≥20 sp captions; contrast target 7:1 for body text (viewing distance, cheap panels).
- Screen readers: Android TV TalkBack and tvOS VoiceOver read focused items; give cards a merged description (title + status); announce rail titles as headings.
- Captions/subtitles: respect system caption preferences; readable over video with a backing.
- Input: no touch, no hover, no on-screen keyboard as the primary text path; voice or system keyboard for search.
- Overscan-safe margins for all persistent UI.

## Desktop (Windows / macOS)

- Keyboard everything: shortcuts documented in menus and tooltips, access keys (Alt) on Windows, F6 pane cycling, arrow-key grids/trees/lists, Enter/Escape defaults in dialogs.
- UI Automation / accessibility API: `AutomationProperties.Name/HelpText/LiveSetting` (WinUI/WPF), `AutomationPeer` for custom controls, NSAccessibility on macOS; test with Narrator/NVDA and VoiceOver.
- Focus visuals: keep system focus visuals when retemplating (WPF `FocusVisualStyle`, WinUI `UseSystemFocusVisuals`).
- High contrast: Windows high-contrast themes must render every state (use theme resources, not hard-coded brushes).
- Text scaling 100–225% and DPI 100–300%: layouts reflow, no clipped labels.
- Targets: ≥24 epx with spacing; context menus for the selected object.

## Kiosk

- ≥60 px targets, ≥20 px text, high contrast for glare; controls within accessible reach ranges (interactive elements roughly 380–1220 mm from the floor); tactile/audio feedback on tap; idle timeout with visible countdown and session clearing; a visible cancel at every step; no hover, no precise dragging, no scrolling to reach the primary action; alternative input (headphone jack/keypad) where legally required.

## Deterministic checks

- `tokens.py contrast "#fg" "#bg"` for any pair; `tokens.py validate tokens.json --platform <p>` for the whole semantic set including states and dark theme (TV applies stricter targets).
- `tokens.py scale --platform <p>` produces role sizes that respect platform floors.
- Automated web checks: run axe (via Playwright `@axe-core/playwright`) or Lighthouse if present in the project; treat results as leads.
- Android: Accessibility Scanner / Compose semantics tests; iOS: Accessibility Inspector audit; Windows: Accessibility Insights.

## Audit procedure

1. Inspect the project for the input modes it supports and the existing accessibility mechanisms (inspect_project.py reports them).
2. Walk the primary flow with the non-pointer input (Tab/DPAD/screen reader) and record where focus goes, what is announced, and what cannot be reached.
3. Measure contrast for every text and control pair in every theme; do not estimate.
4. Check text scaling at 200% (web), largest Dynamic Type/font scale (mobile), 225% (Windows).
5. Check motion under reduced-motion and auto-rotating content controls.
6. Check forms: labels, errors, recovery, autofill.
7. Report each defect with the criterion, the element, the measured value, and the fix; rank by user impact (blocks task > degrades task > cosmetic).
