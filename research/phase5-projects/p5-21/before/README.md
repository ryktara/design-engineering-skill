# Streaks

A small SwiftUI habit tracker for iPhone (iOS 17, Swift 5.9). It exists as a
research fixture: a real, readable codebase with one clearly stated design
language that tools can inspect and reproduce.

## Layout

```
Package.swift                      SwiftPM manifest (library target; see "Building")
Sources/Streaks/
  StreaksApp.swift                 @main entry; injects Store + Theme, configures UIKit bars
  Theme/AppTheme.swift             Theme struct: palette, typography, spacing, shape, shadow
  Models/Habit.swift               Habit, HabitFrequency, DailyCompletion
  Models/Store.swift               ObservableObject with deterministic sample data
  Views/RootTabView.swift          Bottom TabView: Today / Habits / Stats / Profile
  Views/TodayView.swift            Progress ring + habit cards with check-off circles
  Views/HabitsView.swift           NavigationStack list, swipe-to-archive, "+" toolbar button
  Views/AddHabitSheet.swift        Form: name, icon grid, frequency segmented, reminder time
  Views/StatsView.swift            Swift Charts weekly bar chart + 2x2 stat tile grid
  Views/ProfileView.swift          Settings-style grouped list
  Components/HabitCard.swift       Elevated card row
  Components/ProgressRing.swift    Circular progress indicator
  Components/PrimaryButton.swift   Full-width accent button
  Assets.xcassets/Colors/          Colorsets with light + dark appearances
Tests/StreaksTests/StoreTests.swift
render/twin.html                   Static HTML twin of Today + Add Habit + Stats (390x844), ?theme=dark
```

## Design language

Plainly stated so it can be checked against the code:

- **Navigation:** bottom tab bar with four tabs (Today, Habits, Stats, Profile).
  Each tab owns its own `NavigationStack`. Creation happens in a modal sheet, not a push.
- **Theme:** dual light/dark. Every colour is defined once in `Theme.Palette` via
  `Color(light:dark:)` and mirrored in `Assets.xcassets/Colors`. No view uses a literal colour.
- **Typography:** custom font **Nunito**, resolved through `Theme.Typography`. If Nunito is not
  registered in the bundle, it falls back to the system font with `.rounded` design. No view
  calls `Font.custom` or picks a family directly; SF Symbol glyph sizes use `.system(size:)`
  only for icon sizing.
- **Surfaces:** elevated cards. Content sits on white / near-black `surface` cards over a warm
  off-white / near-black `background`, with a soft shadow (`opacity 0.08, radius 16, y 6`).
- **Corner radius:** 16 everywhere (cards, buttons, sheet, tiles); 10 for icon chips.
- **Spacing:** 8-based scale, 4-pt base: `4 / 8 / 12 / 16 / 24` (`xs / sm / md / lg / xl`).
  Screen gutters are 16; section gaps are 24; card padding is 16.
- **Accent:** warm coral (`#FF6B4A` light, `#FF8A6E` dark) used for the ring, primary button,
  selected tab, check-off state and icon tints. `accentSoft` is the tinted chip/track colour.

### Palette

| Token            | Light     | Dark      |
|------------------|-----------|-----------|
| accent           | `#FF6B4A` | `#FF8A6E` |
| accentSoft       | `#FFE7E0` | `#4A2A22` |
| background       | `#F6F4F0` | `#121110` |
| surface          | `#FFFFFF` | `#1E1C1A` |
| surfaceSecondary | `#FBFAF8` | `#262421` |
| text             | `#1F1B18` | `#F4F1ED` |
| textSecondary    | `#76706A` | `#A39D96` |
| separator        | `#E8E4DE` | `#33302C` |
| success          | `#3BAF7A` | `#5CCB95` |
| chartTrack       | `#FFE7E0` | `#8E6152` |

## Building

There is intentionally no `.xcodeproj` checked in. Two options:

1. **Xcode app target:** create an iOS App target named `Streaks` (iOS 17), delete the generated
   `ContentView.swift`/`StreaksApp.swift`, and add `Sources/Streaks` to the target. Optionally add
   `Nunito-*.ttf` to the target and list them under `UIAppFonts` in Info.plist.
2. **SwiftPM (type-check only):** `swift build` on macOS with the iOS SDK selected, or open
   `Package.swift` in Xcode. `Package.swift` declares a library product because SwiftPM cannot
   produce an iOS app bundle on its own.

## Screenshot twin

`render/twin.html` reproduces the Today screen, the Add Habit sheet and the Stats screen at 390x844 using the same
palette, spacing and radii, with Nunito loaded from Google Fonts (falls back to the system
rounded stack). Open it directly or with `?theme=dark`. It is for Playwright screenshots on
machines without Xcode; the Swift sources are the source of truth.
