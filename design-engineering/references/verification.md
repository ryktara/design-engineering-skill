# Visual verification loop

Implementation → run → capture → inspect → fix → repeat. Compilation, type checks, and unit tests passing are not visual success. Scale the loop to the change: a one-line style fix needs one capture; a new screen needs the matrix and the interaction pass.

## Contents
- Tool selection
- Web
- Mobile
- TV
- Desktop
- What to inspect in every capture
- Reporting

## Tool selection

Use what the environment provides, in this preference: the in-app browser pane or a browser automation tool (Playwright) for web; emulator/simulator screenshots for mobile and TV; window screenshots or computer use for desktop; the project's own visual test tooling (Storybook, screenshot tests) when present. If nothing is available, say so explicitly in the report and describe what remains unverified.

## Web

- Start the dev server with the project's script; open the route.
- Capture the responsive matrix (responsive.md) plus 200% zoom; light and dark themes if supported.
- Interaction pass: Tab through the screen and record the focus order and visibility; open every overlay and close with Escape; hover states; reduced-motion emulation (`prefers-reduced-motion`).
- Automated leads: axe/Lighthouse if installed; console errors; layout-shift observation.
- Playwright example (only if Playwright is present in the project or can be run without installing into the project):
  ```js
  await page.setViewportSize({ width: 390, height: 844 }); await page.screenshot({ path: 'phone.png', fullPage: true });
  await page.keyboard.press('Tab'); // repeat, screenshot focused element
  await page.emulateMedia({ reducedMotion: 'reduce' });
  ```

## Mobile

- iOS Simulator: `xcrun simctl io booted screenshot shot.png`; test Dynamic Type (Accessibility Inspector or Settings), VoiceOver rotor, landscape, small and large devices.
- Android emulator: `adb exec-out screencap -p > shot.png`; test font scale 200% (`adb shell settings put system font_scale 2.0`), TalkBack, gesture navigation insets, small (360 dp) and large (412+ dp) widths, foldable posture if targeted.
- Flutter/React Native: the same simulators/emulators; Flutter golden tests and RN Storybook where present.

## TV

- Android TV emulator (1080p profile) or a real device over ADB: `adb shell input keyevent KEYCODE_DPAD_RIGHT/LEFT/UP/DOWN/CENTER/BACK` to walk focus; screenshot after each move; confirm one visible focus, focus restoration on BACK, no unreachable controls, safe margins (compare against a 5% overlay), text ≥24 sp, no dropped key events while images load.
- tvOS Simulator: Siri Remote emulation; `xcrun simctl io booted screenshot`; check focus lift, parallax, and focus sections.
- Test on the weakest target hardware for focus latency; the emulator hides jank.

## Desktop

- Run the app; capture at the minimum window size and maximised; DPI 150% and 200% (Windows display scaling or `DOTNET_SYSTEM_GLOBALIZATION`-independent XAML scaling settings); light, dark, and high-contrast themes.
- Keyboard pass: Alt access keys, Tab/arrow semantics in lists/grids/trees, F6 pane cycling, Enter/Escape in dialogs; Narrator/NVDA quick pass with Accessibility Insights if available.
- Resize continuously and watch pane collapse order and text wrapping.

## What to inspect in every capture

Overflow and clipping; wrapping and truncation; alignment to the grid and shared edges; spacing on the scale; hierarchy readable at a glance; contrast (measure suspicious pairs); focus visibility and order; empty/loading/error states (force them with mocked data); long strings and RTL if applicable; imagery crops and placeholders; motion under reduced motion; platform chrome (safe areas, title bars, overscan).

## Reporting

List what was captured (matrix, devices, themes), what was found and fixed, what remains, and what could not be verified because tooling was unavailable. Attach or reference the screenshots. Never state that something "looks good" without having looked.
