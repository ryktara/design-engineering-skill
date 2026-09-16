# Performance-aware UI decisions

Flag genuine hazards created by UI choices; do not sacrifice usability for benchmark scores.

## Web

- Layout shift: `width/height` or `aspect-ratio` on media, font fallback metrics (`size-adjust`), skeletons at final size, no injected content above existing content, sticky elements sized in advance. Target CLS < 0.1.
- LCP: preload the hero image/display font; never lazy-load the LCP image; serve responsive sources; avoid full-bleed 4K backgrounds.
- JS cost of UI choices: prefer CSS for hover/transitions/scroll-snap; server-render content; island-ise interactivity; import icons individually; lazy-load charts, editors, maps below the fold; measure bundle deltas before adopting a UI dependency; avoid client-rendering static pages.
- Rendering: virtualise long lists/tables; avoid animating layout properties; limit `backdrop-filter` and large box-shadows; use `content-visibility` for long pages; batch DOM updates.
- Fonts: subset, ≤2 families, variable fonts when smaller, `font-display: swap`.
- Images: modern formats (AVIF/WebP), correct dimensions, CDN resizing, `loading=lazy` below the fold, decode async.

## Mobile

- Images requested at rendered size with caching (Coil/Glide, SDWebImage/Nuke, expo-image); placeholders; no original-resolution thumbnails.
- Overdraw: remove redundant opaque backgrounds; avoid nested translucent layers; profile with GPU overdraw tools.
- Lists: LazyColumn/List/FlatList with stable keys and cheap items; avoid measuring-heavy layouts per item; paginate.
- Effects: blur, shadows, and large-radius clipping cost GPU; avoid animating them in lists.
- Animation: transform/opacity, hardware-accelerated; test on low-end devices; respect battery/thermal.
- Startup: defer non-critical UI work; avoid loading fonts/icons synchronously.

## TV

- Focus responsiveness: focus moves render within a frame even while images decode; never coalesce or drop key events; debounce backdrop changes (300 ms) and expensive focus side effects.
- Catalog virtualisation in both axes; rails and rows lazy; images sized to card; memory caps (1–2 GB boxes); avoid decoding backdrops larger than the panel.
- Scrolling smoothness: stable item sizes; avoid re-composition/re-render storms on focus change (hoist focus state, use keys).
- Player UI: overlay drawn without re-laying out the video surface; avoid heavy blur over video; subtitles rendered by the player.
- Test on the cheapest supported device; the emulator hides jank.

## Desktop

- Large grids and trees: UI virtualisation on (WPF `VirtualizingStackPanel`, WinUI `ItemsRepeater`/`ListView`, Avalonia `TreeDataGrid`); deferred loading (`x:Load`), incremental rendering.
- Visual trees: avoid deeply nested layouts and per-row templates with dozens of elements; use data templates with minimal chrome; freeze brushes; cache bitmaps for static effects.
- Effects: Acrylic/Mica only where designed; avoid per-item drop shadows and blur in lists.
- Binding: compiled bindings (`x:Bind`), avoid per-frame converters; throttle live updates to the UI thread.
- Startup and window ops: lazy pages, persisted layout restore without blocking.

## Charts and real-time

Canvas/WebGL beyond a few thousand points; downsampling; no per-tick transitions; fixed windows; throttle updates to the UI's frame budget; pause offscreen charts.

## When to flag

Flag when a design choice implies: a new heavy dependency, unbounded lists without virtualisation, large media without sizing/caching, blur/shadow-heavy surfaces on low-end targets, animation of layout properties, hover-heavy interactions on touch devices (double work), or TV focus effects that do work on every key press.
