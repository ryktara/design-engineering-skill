# Responsive and adaptive behaviour

## Choose the matrix from the product

Never test one viewport. Build the matrix from the codebase's breakpoints and the product's real targets; the labels below are starting points, the numbers come from the project.

| Class | Typical size | What must be checked |
|---|---|---|
| narrow phone | 320–360 css px | reflow without horizontal scroll (WCAG 1.4.10); nav collapse; sticky bars not covering focus |
| phone | 390–430 | thumb reach; bottom actions; sheets |
| tablet | 768–1024 (portrait/landscape) | two-pane or single; pointer + keyboard possibility |
| laptop | 1280–1440 | rail vs. drawer; table columns |
| desktop | 1536–1920 | max content width; multi-column |
| large | ≥2560 | scaling of fixed-width containers; wall displays |
| desktop window | 800×600 minimum → maximised | pane collapse order; DPI 150/200% |
| TV | 960×540 dp frame (1080p) and 4K scaling | safe margins; type scale; focus path |
| zoom | 200% browser zoom / max text scale | overflow, clipped labels, truncated buttons |

Also check orientation changes (mobile/tablet), foldables/split-screen (Android), Slide Over/Split View (iPadOS), and RTL locales.

## What changes across classes

- Navigation: top bar ↔ menu button; rail ↔ drawer; tabs ↔ select; bottom tabs (phone) ↔ rail (tablet).
- Layout: master-detail ↔ stacked; table ↔ list rows; dashboard grid ↔ single column ordered by importance; three-pane ↔ two-pane ↔ one.
- Overlays: dialog ↔ full-screen/sheet; side panel ↔ overlay drawer.
- Density: high on desktop pointer, medium on touch.
- Imagery: responsive sources; art direction for crops; backdrop resolution capped.
- Typography: fluid type only for display; body stays at the role size.

## Techniques

- Web: fluid widths with min/max, CSS grid `auto-fill/minmax`, container queries for components, logical properties for RTL, `env(safe-area-inset-*)`, `scroll-padding` under sticky headers, `aspect-ratio` on media.
- Compose: `WindowSizeClass`, adaptive scaffolds (`ListDetailPaneScaffold`, `NavigationSuiteScaffold`), `WindowInsets`.
- SwiftUI: size classes, `NavigationSplitView`, `ViewThatFits`, `safeAreaInset`.
- Flutter: `LayoutBuilder`, `MediaQuery.sizeOf`, adaptive scaffolds, `SafeArea`.
- React Native: `useWindowDimensions`, `SafeAreaView`, platform/TV variants.
- WinUI/WPF: `AdaptiveTrigger`/`VisualStateManager` on window width, `Grid` star sizing, `SplitView` display modes.
- Avalonia: `OnFormFactor`/`OnPlatform` and adaptive `Grid`.

## Verification (see verification.md)

Capture each class in the matrix, look for: clipping, overflow, wrapping oddities, truncated labels, tap targets, hierarchy order, data density, navigation transformation, modal/drawer behaviour, imagery crops, typography floors. Fix and re-capture. Report the matrix you actually tested.
