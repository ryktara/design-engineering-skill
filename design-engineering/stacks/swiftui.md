# SwiftUI (iOS, iPadOS, macOS, tvOS)

## Conventions to detect and respect
- App structure (`App`/`Scene`), navigation (`NavigationStack`/`NavigationSplitView`, `TabView`), state (`@Observable`/`@State`/`@Environment`), existing design system (`Theme`, colour assets with light/dark variants, `Font` extensions), asset catalogs, SF Symbols usage, UIKit interop (`UIViewRepresentable`), targets (iOS/macOS/tvOS) in the project.

## iOS / iPadOS
- Use system components: `TabView` (3–5 tabs with `Label`), `NavigationStack` with `.navigationTitle`, `.sheet` with `.presentationDetents`, `.confirmationDialog`, `List` with `.swipeActions`/`Section`, `Form` for settings, `.searchable`, `.contextMenu`, `.toolbar` placements.
- Text: Dynamic Type styles (`.font(.body)`), custom fonts via `Font.custom(_, size:, relativeTo:)`; never fixed sizes for body; test at AX sizes; `.lineLimit` with expansion paths.
- Colour: semantic system colours or asset colours with dark variants; `.tint` for the accent; validate with `tokens.py`.
- Layout: `safeAreaInset` for sticky actions; `.ignoresSafeArea` only for backgrounds; `ViewThatFits`/size classes for iPad two-pane; `ScrollViewReader` for restoration.
- Accessibility: `accessibilityLabel/Value/Hint`, `.accessibilityAddTraits(.isButton/.isHeader)`, `.accessibilityElement(children: .combine)` for cards, `AccessibilityNotification.Announcement`, Reduce Motion (`accessibilityReduceMotion`), Increase Contrast.
- Motion: `.animation(.spring)`/`.snappy`, `matchedGeometryEffect`, `NavigationTransition.zoom` (iOS 18+); gesture-driven and interruptible; no launch choreography.

## macOS
- `NavigationSplitView` with sidebar/inspector, `.toolbar` with customisation, menu commands via `Commands`, keyboard shortcuts (`.keyboardShortcut`), `Table` with sorting/selection, `.contextMenu`, Full Keyboard Access, system font; window sizing (`.defaultSize`, `.windowResizability`).

## tvOS
- Focus: views become focusable via `Button`/`.focusable()`; `@FocusState` + `.focused()` for initial focus (Play on detail) and restoration; `.focusSection()` to group rails/nav so LEFT/RIGHT/UP/DOWN reach the right group; `.prefersDefaultFocus` in a `.focusScope`; `.onMoveCommand`/`.onExitCommand` (Menu/back) to unwind layers.
- Layout: `TabView` (`.tabViewStyle(.sidebarAdaptable)` for a system sidebar) or top tabs; horizontal `ScrollView` + `LazyHStack` rails with `.scrollTargetLayout()`/`.scrollTargetBehavior(.viewAligned)` and `.focusSection()`; card focus lift via `.hoverEffect(.lift)`/`.cardButtonStyle`; `.scrollClipDisabled()` so scaled cards are not clipped; safe margins 60 pt at 1920×1080.
- Type: tvOS default styles are already large (`.body` ≈ 29 pt); keep weights ≥ regular; contrast ≥7:1 body target.
- Playback: `AVPlayerViewController` via representable for system transport controls, Siri Remote gestures, captions; customise only if brand requires.
- Search: `.searchable` provides the system search screen; Top Shelf via extension where relevant.

## Verification
Simulators per target: iPhone small/large, iPad split view, Mac window resize, Apple TV with remote emulation; screenshots via `xcrun simctl io booted screenshot`; Accessibility Inspector audit; Dynamic Type max; Reduce Motion.
