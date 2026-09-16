# FleetDesk

A small vehicle-fleet dispatcher desktop app. C# / Avalonia 11 / net8.0. Used as a
research fixture: the point of this repo is that its **design language is stated
plainly below**, so a detector's output can be checked against ground truth.

## What is in it

| Path | Purpose |
|---|---|
| `FleetDesk.csproj`, `Program.cs` | net8.0 WinExe, Avalonia 11.2 + Fluent theme + DataGrid + bundled Inter font |
| `App.axaml` / `App.axaml.cs` | Requests the Light theme variant, includes `Styles/Theme.axaml`, maps view-models to views |
| `Styles/Theme.axaml` | **The design language.** Named brush palette, font family, corner radius, spacing scale, control styles |
| `Views/MainWindow.axaml` | Shell: menu bar (File / Vehicles / Dispatch / Help), toolbar under it, content area, status bar |
| `Views/VehiclesView.axaml` | DataGrid of 30 vehicles (id, plate, driver, status, odometer, last service), row selection, filter box |
| `Views/DispatchView.axaml` | Two panes: pending jobs list on the left, job detail form with Save / Cancel on the right |
| `Views/SettingsView.axaml` | Plain form: depot name, units, theme toggle (stub) |
| `ViewModels/*.cs` | MVVM with a hand-rolled `INotifyPropertyChanged` base and `RelayCommand`; no MVVM library |
| `Models/Vehicle.cs`, `Models/Job.cs` | Plain models |
| `Services/SampleData.cs` | Deterministic sample data (same 30 vehicles / 8 jobs every run) |
| `render/twin.html` | Static HTML twin of the Vehicles and Dispatch screens for Playwright screenshots (1440 x 900 per section), no .NET needed |

## Design language (ground truth)

**Navigation: menu bar + toolbar.** A classic top menu bar (`File`, `Vehicles`,
`Dispatch`, `Help`) sits above a flat toolbar of text buttons (Vehicles, Dispatch,
Settings | Refresh, Save job). There is no sidebar, no tab strip, no hamburger, no
navigation rail. A status bar runs along the bottom. Screens swap inside the single
content area.

**Theme: light, light-first.** The window canvas is a cool off-white (`#F5F6F8`),
panels are white (`#FFFFFF`), bars (toolbar, status bar, table header) are a slightly
darker grey (`#F0F2F5`). Text is near-black (`#1F2933`) with a muted grey
(`#5F6B7A`) for secondary text. The app requests `ThemeVariant.Light` and the
Settings "theme" toggle is a stub that does not switch anything.

**One accent colour.** Blue `#2563EB` (hover `#1D4ED8`, tint `#E8EFFD`). It is used
for the primary button (Save), focus ring, and row/list selection. Status colours
(green `#15803D`, amber `#B45309`, red `#B91C1C`) exist only for badges and are not
part of the brand.

**Typography: Segoe UI, Inter fallback.** `FontFamily` = `Segoe UI, Inter`
(`Avalonia.Fonts.Inter` is bundled so the fallback is always present). Body 13px,
small/labels 12px, section headings 15px semibold, page titles 20px semibold. No
display faces, no serif, no monospace.

**Surfaces: bordered and flat.** Every panel, card, grid, input and button is a flat
fill with a **1px** border in `#D9DDE3`. **No drop shadows** anywhere, no gradients,
no glass/blur, no elevation levels.

**Corner radius: 4px** on everything (panels, buttons, inputs, badges, DataGrid).
Fluent's `ControlCornerRadius` is overridden to 4 so built-in templates match.

**Spacing: 8px scale.** 8 / 16 / 24 / 32. Toolbar and status bar use 8x4 padding,
inputs 8x6, buttons 12x6, panels 16 or 24, page gutter 16, pane gap 16, row height 36.

**Density: medium.** Grid rows are 36px, inputs are 32px tall, labels sit above inputs.

## How views stay consistent

Views reference theme resources (`{StaticResource AccentBrush}`,
`{StaticResource AppCornerRadius}`, `{StaticResource Pad2}`, `Classes="surface"`,
`Classes="accent"`, and so on) rather than literal colours or sizes. If you change
`Styles/Theme.axaml`, every screen follows.

## Building / running

```
dotnet build
dotnet run
```

Requires a .NET SDK that can target `net8.0`; NuGet restore pulls Avalonia 11.2.3.
Nothing is downloaded at runtime.

## Screenshots without .NET

Open `render/twin.html` at a 1440-wide viewport. The page is two stacked 1440 x 900
sections (`#vehicles`, `#dispatch`) that mirror the Avalonia screens using the same
palette, fonts, radius and spacing, with the same sample data. Example with
Playwright:

```js
await page.setViewportSize({ width: 1440, height: 900 });
await page.goto('file:///.../render/twin.html');
await page.locator('#vehicles').screenshot({ path: 'vehicles.png' });
await page.locator('#dispatch').screenshot({ path: 'dispatch.png' });
```
