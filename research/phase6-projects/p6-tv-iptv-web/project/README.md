# Meridian TV — smart TV client

Web-based IPTV client for Samsung Tizen and LG webOS televisions. Plain HTML/CSS/JS, no build step, no framework; the same bundle is packaged for both platforms.

## Target platforms

| Platform | Minimum | Notes |
|---|---|---|
| Samsung Tizen | 5.5 (2020 models) | packaged via `config.xml`, Tizen Studio / `tizen` CLI |
| LG webOS | 5.0 | packaged via `appinfo.json`, `ares-package` |
| Desktop browser | Chromium 90+ | development only, 1920×1080 |

Layout is fixed at 1920×1080. The TV scales the viewport for 4K panels; do not add responsive breakpoints.

## Project layout

```
index.html        shell (top bar + screen container)
config.xml        Tizen widget manifest
appinfo.json      webOS app manifest
css/tokens.css    design tokens (colour, type scale, spacing, focus)
css/tv.css        layouts: home rails, guide grid, detail, player overlay, settings
js/keys.js        remote key-code mapping (Tizen / webOS / desktop) and app exit
js/data.js        deterministic channel/programme/rail data (seeded PRNG)
js/focus.js       spatial focus manager (d-pad navigation)
js/app.js         screens and routing
```

## Running locally

Open `index.html` in Chromium at a 1920×1080 window (or use the responsive device toolbar with a custom 1920×1080 preset). Serving over `http://` is not required.

Keyboard mapping for the remote:

| Remote | Keyboard |
|---|---|
| D-pad | Arrow keys |
| OK / Enter | Enter |
| Back / Return | Backspace or Escape |
| Play/Pause | MediaPlayPause (or the Play button on the Detail page) |
| Guide | not mapped on desktop; use the top bar |

On device the Back key arrives as key code `10009` (Tizen) or `461` (webOS); both are mapped in `js/keys.js`. Media keys are registered with `tizen.tvinputdevice` at start-up so the platform delivers them to the app.

## Packaging

**Tizen**

```
tizen package -t wgt -s <certificate-profile> -- .
tizen install -n MeridianTV.wgt -t <device-id>
```

**webOS**

```
ares-package .
ares-install --device <device> tv.meridian.app_1.4.2_all.ipk
ares-launch --device <device> tv.meridian.app
```

Bump `version` in both `config.xml` and `appinfo.json` before a release; they must match.

## Screens

- **Home** — four horizontal rails of 16:9 cards (Continue watching, On now, Movies tonight, For the kids). Left/Right moves along a rail, Up/Down moves between rails, Enter opens the programme.
- **Guide** — 30 channels × 6 hours in 30-minute columns with a "now" marker. Left/Right moves between programmes on a channel, Up/Down between channels; the time header follows focus.
- **Detail** — programme artwork, metadata, and Play / Record / Favourite actions.
- **Player** — full-screen playback with an overlay showing title, progress, play/pause and subtitles. On desktop the video is a stub and the progress bar advances on a timer.
- **Settings** — audio, subtitles, streaming quality, parental controls, account.

## Design language

- **Dark-first.** Background `#0E1116`, surfaces `#171C24`, text `#E8ECF1`. No light theme.
- **Amber accent** `#F2A900` for focus, progress and primary actions; red is reserved for LIVE badges.
- **Content rails.** Home is built from horizontal rails of landscape 16:9 cards with artwork bleeding to the edges and metadata over a bottom gradient.
- **10-foot type scale.** 28 / 32 / 40 / 56 / 72 px. Body copy is 32 px; nothing below 28 px should be used for readable text.
- **Amber focus ring** with a subtle scale on the focused element; focus is always visible and there is exactly one focused element per screen.
- **5% safe area** on all four edges; nothing interactive sits outside it.
- **Roboto**, falling back to the platform system font.

## Data

`js/data.js` generates the schedule from a fixed seed, so screenshots and QA runs are reproducible. The guide window starts at the half-hour preceding app launch. Replace `Data` with the EPG service client for production builds.
