# Jetpack Compose (Android phone/tablet)

## Conventions to detect and respect
- `MaterialTheme` setup (colour scheme from seed, typography, shapes), `dynamicColor` flag, `Theme.kt`; navigation library (Navigation Compose / Navigation 3 / Voyager / Decompose); state holders (ViewModel + StateFlow), DI; existing composable library (`ui/components`), image loader (Coil/Glide), media (Media3).
- Design tokens usually live in `Color.kt`/`Type.kt`/`Shape.kt` and `MaterialTheme`; extend the scheme rather than passing raw colours.

## Implementation rules
- Use Material 3 components (`NavigationBar`, `TopAppBar`, `ModalBottomSheet`, `ListItem`, `OutlinedTextField`, `FilterChip`, `AlertDialog`, `Scaffold`) and the adaptive scaffolds (`ListDetailPaneScaffold`, `NavigationSuiteScaffold`) with `WindowSizeClass` for tablets/foldables.
- Colour roles: `MaterialTheme.colorScheme.*` container/on-container pairs; never `Color(0xFF…)` in composables; `dynamicColor = false` when brand lock is required; dark scheme defined and validated.
- Typography: `MaterialTheme.typography` roles; `sp` for text; fonts registered via `FontFamily`; test with font scale 2.0.
- Insets: `enableEdgeToEdge()` + `WindowInsets`/`contentWindowInsets` on `Scaffold`; `imePadding()` for forms; bottom actions above navigation bars.
- Lists: `LazyColumn` with stable `key`s and `contentType`; `SwipeToDismissBox` with labelled equivalents; `stickyHeader`; paging for large sets; image requests sized (`Coil` `size`).
- Semantics: `Modifier.semantics { contentDescription; role; heading() }`, `mergeDescendants` on cards, `clearAndSetSemantics` for redundant children, `LiveRegionMode` for status; `Modifier.clickable(role = Role.Button)`; TalkBack pass.
- Motion: `animate*AsState`, `AnimatedVisibility`, `SharedTransitionLayout`, springs for gestures; respect `ANIMATOR_DURATION_SCALE`/reduced motion; predictive back enabled.
- Forms: `keyboardOptions` (type, `imeAction`), `supportingText`/`isError`, `BringIntoViewRequester` for focused fields, autofill hints.
- Performance: hoist state, avoid recomposition storms (stable params, `remember`), `derivedStateOf`, baseline profiles; profile with Layout Inspector/Perfetto.

## Verification
Emulator/device: small (360 dp) and large (412+) widths, font scale 2.0, TalkBack, dark mode, gesture navigation insets; screenshots via `adb exec-out screencap`; Compose UI tests/screenshot tests if present.
