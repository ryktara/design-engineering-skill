# Field Inspect

Mobile app (Android + iOS, Flutter, Material 3) for utility field technicians who inspect
poles, transformers, meters and substations outdoors.

Context that drives the UI:
- Bright sunlight: high contrast, large glanceable status, no thin text.
- Gloves: tap targets 56 dp minimum, generous spacing, no swipe-only gestures.
- Patchy connectivity: offline-first, pending-sync queue, last-synced timestamp always visible.

Screens: inspection checklist (`/inspection/:id`), defect report form (`/inspection/:id/defect/:itemId`).
State: Riverpod. Routing: go_router. Theme: `lib/theme/app_theme.dart` (light and dark, semantic status colours via `ThemeExtension`).
