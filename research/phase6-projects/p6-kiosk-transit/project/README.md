# MetroLink Ticket Kiosk

Front end for the MetroLink ticket vending machines (TVMs) installed at Central, Riverside and Airport stations. It is a single-page, dependency-free web app that runs full-screen in the kiosk's embedded Chromium and talks to the printer and card terminal through the local hardware bridge.

## Hardware assumptions

- **Display:** 32" portrait touch screen, 1080 × 1920, capacitive, mounted at standing height. No mouse, no physical keyboard.
- **Printer:** 80 mm thermal ticket/receipt printer below the screen.
- **Card terminal:** contactless + chip reader to the right of the screen. The bridge exposes a polled status endpoint (`idle` → `reading` → `approved` / `declined`).
- **Runtime:** Chromium 120+ in kiosk mode; no network access except the bridge on localhost.

This repo contains only the UI. The hardware bridge is stubbed in `js/app.js` (`startTerminal`) so the flow can be exercised on a laptop.

## Running

There is no build step.

```
# option 1 — just open it
open index.html

# option 2 — any static server
npx serve .
python -m http.server 8080
```

Open the page in a window sized to 1080 × 1920 (or use device emulation in dev tools) — the layout is fixed to the kiosk resolution and does not reflow.

## Structure

```
index.html        all screens as <section data-screen="…">
css/tokens.css    design tokens (colour, spacing, type, radius, touch target)
css/kiosk.css     layout and components
js/i18n.js        UI strings + t() helper
js/data.js        fare table, zones, promo codes
js/app.js         state machine, idle reset, terminal polling
data/fares.json   fare table as edited by the ops team (mirror of data.js)
assets/logo.svg   brand mark
```

### Flow

`attract → choose-ticket → quantity → review → pay → printing → done`

The header "Start over" button returns to `attract` from anywhere and clears the basket. An idle timer also returns to `attract` after 20 s without input (the printer is never interrupted). `window.__kiosk` exposes `state` and `show()` for QA scripts.

### Fares

Edit `data/fares.json`, then copy the same values into `js/data.js`. Prices are stored in pence. Promo codes are percentage discounts and are matched case-insensitively.

## Design language

- **Full-screen flow.** Every step is its own screen; there are no modals, drawers or scrolling regions.
- **One primary action per screen.** The blue filled button is the thing to press next; secondary actions are outlined.
- **72 px minimum touch target** (`--touch`), sized for a gloved finger at arm's length.
- **Colour:** transit blue `#0B4F9C` as the single primary, warm neutrals for surfaces, semantic green / amber / red for terminal states.
- **Radius:** 16 px on all cards and buttons.
- **Spacing:** 8-pt scale (8 / 16 / 24 / 32 / 48 / 64).
- **Type:** Inter with system fallback; scale 28 / 36 / 48 / 64 px. Body copy is never smaller than 28 px.
- **No dark mode.** Kiosks run in bright station lighting; a single light theme is intentional.

## Browser support

Chromium only (kiosk build). Firefox/Safari are fine for development but are not tested.
