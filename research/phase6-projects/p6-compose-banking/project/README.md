# NorthBank Android

Retail banking app for NorthBank customers: view accounts and balances, browse
transactions, send money to saved payees, and manage debit/credit cards.

This repository is the Android client only. It talks to the NorthBank Mobile
Gateway (`nb-mobile-gateway`) in production; a fake in-memory repository is used
in `debug` builds so the app runs without network access or credentials.

## Requirements

- Android Studio Ladybug (2024.2) or newer
- JDK 17
- Android SDK 35 (compileSdk / targetSdk), minSdk 26

## Module layout

```
app/
  src/main/java/com/northbank/app/
    MainActivity.kt          Single-activity host, edge-to-edge
    NorthBankApp.kt          Application; owns the repository instance
    data/
      model/                 Account, Transaction, Card, Payee
      AccountRepository.kt   Repository contract
      FakeAccountRepository  In-memory implementation seeded from SampleData
      SampleData.kt          Deterministic fixtures (stable dates for screenshots)
    ui/
      theme/                 Color, Type, Shape, Spacing, Theme
      components/            NbButton, NbCard, NbListRow, AmountText
      navigation/            Routes, bottom bar, NavHost
      screens/
        accounts/            AccountsScreen, AccountDetailScreen
        transfer/            TransferScreen + TransferViewModel
        cards/               CardsScreen
        more/                MoreScreen
    util/                    Money and date formatting
  src/main/res/              Strings, colours, window theme, launcher icon
```

The only module is `:app`. Feature modules were split out in the iOS client;
for Android we are keeping a single module until the payments rewrite lands.

## Running

```
./gradlew :app:installDebug
```

or open the project in Android Studio and run the `app` configuration on an
emulator (API 26+). Debug builds use `FakeAccountRepository`, so every
screen is populated immediately with sample data and no login is required.

Unit tests:

```
./gradlew :app:testDebugUnitTest
```

Compose UI tests run on a connected device or emulator:

```
./gradlew :app:connectedDebugAndroidTest
```

## Design language

- **Navigation:** bottom tabs (Accounts, Pay, Cards, More). Account detail
  pushes on top of the Accounts tab; all other tabs are single screens.
- **Theme:** light and dark, light by default. Dynamic (Material You) colour is
  disabled so the brand green is consistent across devices.
- **Surfaces:** outlined cards on a flat background, no elevation shadows.
- **Radius:** 12 dp on all cards, buttons and card art.
- **Spacing:** 4-pt grid via the `Spacing` object (4 / 8 / 12 / 16 / 24 / 32 dp).
  Screen content is inset 16 dp.
- **Typography:** Roboto (platform default) with the Material 3 type scale
  defined in `Type.kt`. Amounts use tabular figures so columns align.
- **Components:** an in-house `Nb*` set (`NbButton`, `NbCard`, `NbListRow`,
  `AmountText`) built on Material 3. Prefer these over raw Material components
  in screens so visual changes can be made in one place.

## Contributing

Branch from `develop`, open a PR against `develop`, and link the NB ticket in
the description. CI runs `ktlint`, unit tests and a screenshot diff on every PR.
