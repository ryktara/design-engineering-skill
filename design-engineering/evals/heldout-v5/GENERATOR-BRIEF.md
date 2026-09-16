# Held-out v5 — generator brief (prompts only)

You write **prompts only**. You must not read anything under `design-engineering/scripts`, `design-engineering/data`, `design-engineering/evals/development`, `design-engineering/evals/regression`, `design-engineering/evals/heldout*/cases.json`, or any earlier held-out set. You do not know how the skill classifies things, and you must not try to guess or game it.

Write what real developers type to an AI coding assistant about user interfaces: observations ("the totals never line up"), half-sentences, questions, typos, product jargon, device idioms instead of platform names ("from the sofa", "on the ward", "in the van", "on the shop floor screen", "the machine in the lobby"), mentions of stacks (Compose, SwiftUI, WPF, WinUI, Avalonia, Flutter, React, Svelte, Vue, Tizen, webOS, Electron). At least 40 % of prompts give the platform only situationally (no platform name), at least 20 % name none at all, and half carry **no mode verb** (no "fix / add / build / redesign / audit / review / polish").

Categories (target counts; write the number you are assigned):
- `create` — new screen/feature/product (70)
- `refactor-fix` — an existing screen has a defect or friction (100)
- `polish` — spacing, alignment, hierarchy, typography, motion on existing UI (60)
- `audit-review` — review/inspect/score an existing screen or flow (50)
- `accessibility` — keyboard, screen reader, contrast, focus, motion, target size (45)
- `responsive` — breakpoints, orientation, window sizes, split view (40)
- `tv-media` — living-room / remote / EPG / player / rails (35)
- `desktop-native` — WPF / WinUI / Avalonia / macOS / Electron windows, menus, grids, shortcuts (30)
- `mobile-native` — phones / tablets, gestures, keyboards, safe areas, offline (30)
- `kiosk-public` — public terminals, walk-up, timeouts, gloves, sunlight, languages (25)
- `adversarial` — out-of-scope (backend, data, infra, build tooling), UI-adjacent technical questions, deliberately ambiguous or contradictory requests, prompts that look like UI but are not (40)

Stress tags (set `stress` on ~25 % of prompts overall, spread across categories):
- `wrong-screen` — the prompt names one screen/component but contains a word that also names another screen or component in a different sense (e.g. "tab" the key vs tabs, "card" the payment card vs a card component, "overlay" a loading overlay vs a player overlay, "compare two files" vs a comparison chart, "landscape" the orientation, "remote" the office, "terminal" the airport building, "guide" a user guide, "poster-sized print", "member profile", "event log").
- `generic-guardrail` — a narrow one-element task where general best-practice advice would be filler (one label, one colour, one focus ring, one button order, one spacing value).

Output: a JSON file `{"generator": "<model family>", "prompts": [{"id": "hv5-gXX-NNN", "prompt": "...", "category": "...", "stress": "none|wrong-screen|generic-guardrail"}]}`. No expectations, no platform field, no concept ids — those are set by a separate reviewer who never sees your reasoning. Vary sentence length (4–40 words), voice, and domain (banking, health, retail, logistics, media, education, government, industrial, games, developer tools). Never reuse a sentence pattern more than three times.
