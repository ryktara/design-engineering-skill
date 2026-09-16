# Compose for TV (Android TV / Google TV / Fire TV) and Leanback

Read `platforms/tv.md` first; this file maps it to APIs.

## Conventions to detect and respect
- `androidx.tv:tv-material` (`androidx.tv.material3.*`: `MaterialTheme`, `Surface`, `Card`, `Button`, `NavigationDrawer`, `TabRow`, `Carousel`, `ListItem`), Compose Foundation ≥1.7 for lazy layouts with focus-aware scrolling (`TvLazyRow/Column` are deprecated; `ImmersiveList` is deprecated), Media3 for playback, Coil/Glide for images, `LEANBACK_LAUNCHER` manifest, `android.software.leanback`, `touchscreen required=false`.
- Legacy Leanback (Views): `BrowseSupportFragment`, `RowsSupportFragment`, `ListRow`/`ArrayObjectAdapter`, `Presenter`, `VerticalGridSupportFragment`, `PlaybackSupportFragment`; keep it if the app is built on it and add Compose only through `ComposeView` at screen level.
- Product flavors: mobile and TV targets may share a module; check which UI the task concerns.

## Focus
- `Modifier.focusRestorer()` on every `LazyRow`/`LazyColumn`/rail container so RIGHT/LEFT and BACK return to the last focused child; `focusGroup()` for containers; `FocusRequester` + `LaunchedEffect` for deterministic initial focus (Play on detail); `Modifier.onFocusChanged` for metadata reveal; `focusProperties { up/down/left/right = … }` to fix straight-path reachability (EPG time-slot alignment, grid edges).
- `LocalBringIntoViewSpec` (`BringIntoViewSpec.calculateScrollDistance`) to pin the focused item at a pivot (~0.2–0.3 of the container); default spec for rows that should scroll normally.
- Focused visuals through tv-material3 interaction states: `Card(scale = CardDefaults.scale(focusedScale = 1.1f), border = CardDefaults.border(focusedBorder = Border(BorderStroke(3.dp, color))), glow = …)`, `Surface`/`Button` `ScaleIndication`; never rely on colour alone; reserve padding for scale overflow (`contentPadding`).
- Key handling: `Modifier.onPreviewKeyEvent`/`onKeyEvent` for `Key.DirectionCenter`, `Key.Back`, `Key.MediaPlayPause`, `Key.MediaFastForward`, channel keys; `BackHandler` to unwind layers (player controls → player → detail → home → drawer → exit).
- Never leave a screen without a focusable element (empty/error states get a focusable action).

## Layout
- Home: `LazyColumn` of rails, each `LazyRow` with `focusRestorer()`, `contentPadding = PaddingValues(horizontal = 48.dp)` (design frame 960×540 dp), rail title ≥24 sp; optional immersive backdrop as a `Box` behind the column with `Crossfade`/`AnimatedContent` driven by a debounced `snapshotFlow` of the focused item; dual-scrim `Brush.verticalGradient/horizontalGradient` overlays.
- Navigation: `NavigationDrawer`/`ModalNavigationDrawer` (side) or `TabRow` (top) from tv-material3; drawer expands on focus; content wrapped so LEFT from index 0 enters the drawer.
- Detail: backdrop + title/metadata block + `Row` of ≤4 `Button`s with first focus on Play + related rails below.
- EPG: custom `LazyLayout` or a `LazyRow` of `LazyColumn`s sharing horizontal scroll state; cells sized by duration; `focusProperties` to keep the time slot on UP/DOWN.
- Player: Media3 `PlayerView` (`AndroidView`) or a Compose surface with an overlay composable; overlay visibility controlled by an inactivity timer that pauses while any control is focused.

## Theme and type
- `androidx.tv.material3.MaterialTheme` with a dark `colorScheme` derived from the brand seed; validate with `tokens.py validate --platform tv`; typography from tv-material3 defaults (larger than mobile) or a custom scale via `tokens.py scale --platform tv`; weights ≥400.

## Performance
- Stable `key`s, cheap item composables, image requests sized to the card (`ImageRequest.Builder.size`), backdrop capped at panel resolution and debounced, avoid re-composition on every focus change (hoist focused index to a `State` read only where needed), `LazyColumn` `beyondBoundsItemCount` for prefetch, test on a low-end device.

## Verification
Android TV emulator (1080p) or device: `adb shell input keyevent KEYCODE_DPAD_*` walks, screenshots per move, BACK unwinding, focus restoration, safe-margin overlay, TalkBack; Compose UI tests with `performKeyPress` for focus paths.
