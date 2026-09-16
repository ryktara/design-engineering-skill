# Mobile (iOS, Android, cross-platform) and tablet

Touch-first, one-handed, interrupted use on small screens with strong platform grammars. Load for phone/tablet work in SwiftUI, Compose, Flutter, React Native, or mobile web.

## Contents
- Input and ergonomics
- Platform grammar
- Layout and density
- Components that change on mobile
- Keyboard, forms, and text
- Motion and feedback
- Tablets and large screens
- Performance
- Accessibility
- Checklist

## Input and ergonomics

- Targets ≥44 pt (iOS) / ≥48 dp (Android) with ≥8 spacing; extend hit areas beyond glyphs.
- Thumb zone: frequent and primary actions in the bottom third; rare actions (back, settings) at the top; large phones need bottom alternatives (bottom search, pull-down, sheets from the bottom).
- Gestures are shortcuts: swipe/long-press/pull-to-refresh always have a visible equivalent; never fight system gestures (edge back swipe, home indicator).
- Pressed feedback within ~100 ms (ripple, opacity, scale); no hover-dependent affordances; loading state on the tapped control.

## Platform grammar

- iOS: tab bar (3–5, icon + label), navigation stack with large titles where idiomatic, sheets for secondary tasks (detents), swipe back, context menus on long press, SF Symbols, Dynamic Type styles, system materials for bars/sheets, alerts sparingly.
- Android: navigation bar (3–5, icon + label always), top app bar, predictive back, modal bottom sheets, FAB for one dominant creative action (labelled/extended where space allows), Material Symbols, Material 3 tonal colour, edge-to-edge with insets.
- Cross-platform (Flutter/RN): still map to the host grammar; deviations are brand decisions to state explicitly, not defaults.
- Hub-and-spoke for service apps (banking, government, health): a task hub with large labelled entries and one focal element (balance/status), spokes as linear flows with a single primary action each.

## Layout and density

- Single column by default; two columns only for tightly related pairs; density medium (8 dp base, 40–48 dp controls, 16 sp body); dense products become "fewer things, bigger targets", never smaller text.
- Safe areas and insets: status bar, notch/Dynamic Island, home indicator/gesture bar, IME; bottom actions sit above the home indicator; backgrounds may bleed, content may not.
- Tables become list rows with the 2–3 deciding columns and a detail screen; filters open in a sheet with applied-filter chips; bulk actions via selection mode with a contextual toolbar.
- Sticky primary action (Add to cart, Continue) in the safe area with content padding so it never covers a focused field.
- Empty/loading/error states occupy the content region with one action; skeletons at final size.

## Components that change on mobile

| Desktop/web | Mobile |
|---|---|
| dialog | bottom sheet or full-screen modal with a close/back |
| dropdown/context menu | bottom sheet menu / platform menu / long-press context menu |
| sidebar | bottom tabs (+ drawer only for rare sections) |
| data table | list rows + detail; horizontal scroll only for secondary data |
| hover tooltip | help text or info button |
| inline row actions | swipe actions with labelled buttons + overflow menu |
| pagination | load more / infinite with scroll restoration |
| side panel | push to a new screen |

## Keyboard, forms, and text

Keyboard type and autofill hints per field (email, phone, number, URL, one-time code), return key action (Next/Done), the focused field scrolled above the keyboard, primary action reachable while the keyboard is open, labels above fields (never placeholder-only), inline errors on blur, error summary for long forms, sections with headings, progress saved for long flows, passwords manager-friendly.

## Motion and feedback

System springs for gesture-driven UI (sheets, swipes) that track the finger and are interruptible; shared-element transitions for list → detail; 150–300 ms for state changes; reduced-motion respected; haptics for confirmations and destructive actions (sparingly); no launch animations that delay first interaction.

## Tablets and large screens

Regular width → two-pane (NavigationSplitView / ListDetailPaneScaffold), rail instead of bottom tabs, pointer and keyboard support (iPadOS pointer hover effects, hardware keyboards, Android desktop mode), multitasking widths (Split View, foldable postures); do not stretch a phone layout.

## Performance

Images at rendered size with caching; overdraw reduction; lazy lists with stable keys; transform/opacity animations only; avoid blur/shadow animation in lists; profile on low-end devices; startup work deferred.

## Accessibility

VoiceOver/TalkBack focus order = visual order; merged semantics for cards and rows; roles and labels on every custom control; Dynamic Type/font scale up to 200% (AX sizes on iOS) without clipping; contrast ratios as web; reduced motion; Increase Contrast / high-contrast text; switch access and hardware keyboard focus visuals left enabled; live announcements for async status.

## Checklist

- [ ] Targets ≥44 pt/48 dp; primary actions in thumb reach; gestures have visible equivalents
- [ ] Platform navigation grammar (tabs/bar, stack, sheets, predictive back/swipe back) respected or deliberately deviated
- [ ] Safe areas and IME insets handled; sticky actions never cover focused fields
- [ ] Lists not tables; filters in sheets; density medium
- [ ] Keyboard types, autofill, return keys, labels above fields, inline errors
- [ ] Dynamic Type / font scale tested at max; VoiceOver/TalkBack pass
- [ ] Reduced motion; spring/shared-element only where they serve continuity
- [ ] Screens verified on a small and a large device, both orientations if supported
