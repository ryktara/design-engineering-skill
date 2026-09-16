# Flutter (mobile, desktop, web; TV via focus APIs)

## Conventions to detect and respect
- `ThemeData` (`ColorScheme.fromSeed`, `TextTheme`, component themes), Material 3 flag, `Cupertino` usage, routing (`go_router`/Navigator 2), state (Riverpod/Bloc/Provider), widget library folders (`lib/widgets`, `lib/ui`), image handling (`cached_network_image`), platform targets in `pubspec`/folders.

## Implementation rules
- Tokens: everything through `Theme.of(context)` (`colorScheme.*`, `textTheme.*`, `extensions` for custom semantic roles via `ThemeExtension`); no `Colors.*`/`TextStyle(fontSize:)` in widgets; light and dark `ThemeData` both defined and validated.
- Components: `NavigationBar`/`NavigationRail` by width (`LayoutBuilder`/`MediaQuery.sizeOf`), `Scaffold` + `SafeArea`, `ListView.builder`/`SliverList` with keys, `ListTile`, `Dismissible`/`flutter_slidable` with menu equivalents, `showModalBottomSheet`, `AlertDialog`, `FilterChip`, `TextFormField` with `keyboardType`/`textInputAction`/`autofillHints`, `SearchAnchor`.
- Typography: `TextTheme` roles; `MediaQuery.textScalerOf` respected (never `textScaleFactor: 1`); test at 2.0.
- Accessibility: `Semantics`/`MergeSemantics`, `ExcludeSemantics` for decorative, `SemanticsService.announce`, `Focus`/`FocusTraversalGroup` for keyboard/TV, `MediaQuery.disableAnimations`/`highContrast` respected; `flutter_test` semantics checks.
- Motion: implicit animations (`AnimatedContainer`, `AnimatedSwitcher`), `Hero` for shared elements, `PageTransitionsTheme` per platform; gate with `disableAnimations`.
- Performance: `const` widgets, `RepaintBoundary` for heavy items, `ListView.builder` with `itemExtent` when possible, `cacheWidth/Height` on images, avoid `Opacity`/blur in lists, DevTools profiling.
- TV (Android TV via Flutter): `Focus`/`FocusNode`/`FocusTraversalGroup` with `Shortcuts`/`Actions` for DPAD, visible focus decoration (scale + border), `Scrollable.ensureVisible` for pivots, no touch assumptions; consider `flutter_tv`-style helpers already in the project.

## Verification
Emulators/simulators per target; `flutter run` screenshots; text scale 2.0; TalkBack/VoiceOver; golden tests if present; desktop/web window resizing when targeted.
