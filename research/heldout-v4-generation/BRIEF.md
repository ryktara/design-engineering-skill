# Held-out v4 generation brief (BLIND)

You are writing evaluation prompts for a design-guidance tool that a developer invokes inside a coding assistant. You have NOT seen the tool, and you must not look for it: do not open anything under `design-engineering/`, do not read other eval sets. Your only inputs are this brief and `ONTOLOGY.md` (the public list of concept ids) in this folder.

## What a case is

A realistic thing a developer would type to an assistant while working on a codebase, plus what a careful design reviewer would expect a good response to cover. The prompt is judged on: whether the tool should engage (scope), whether the artifact is new or existing, which working modes fit, which platform is stated or safely inferable, and which ontology concepts a good answer must cover.

## Wording rules (important — this set measures generalisation)

- Write the way people actually type: fragments, lowercase, typos allowed, jargon, half-sentences, occasional long rambles. Vary sentence shapes: observations ("the X does Y"), questions, one-word-verb requests, complaints, pasted bug titles, ticket-style lines, spec-like noun phrases ("a settings screen for a …").
- At least **60% of prompts must NOT use an explicit mode verb** (avoid: create, build, add, refactor, polish, audit, review, fix, redesign, improve, make). Describe the situation instead.
- At least **50% of platform-specific prompts must NOT name the platform canonically** (avoid: "Android TV", "iOS", "desktop app", "kiosk", "mobile", "web"). Imply it through the situation: remote controls, ten-foot viewing, sofa, gloves, touch table in a lobby, tray icon, menu bar, right-click, dock, App Store review, home indicator, thumb reach, notch, back gesture, window resizing, multi-monitor, keyboard accelerators, D-pad, set-top box, hotel lobby screen, checkout lane, wayfinding, badge scanner, and so on. Some prompts should name the stack instead of the platform (SwiftUI, Compose, WPF, WinUI, Avalonia, Flutter, Tauri, Electron, MAUI, React Native, Expo, SvelteKit, Next.js, Rails views, Blazor).
- Include prompts where the platform is genuinely unknowable: then `platform.required` = [] and `acceptable_inferred` lists what may reasonably be inferred (or stays empty). A prompt that would make a reasonable reviewer say "I'd have to ask which platform" must NOT require a platform.
- Include misleading-but-clear prompts: "media browser" (not a web browser), "desktop web app", "windows in the dashboard", "mobile field team using a laptop", "tablet mounted as a kiosk", "TV listings page on our website".
- Do not reuse a wording template across cases. Do not write two prompts about the same screen with the same shape.

## Categories and counts for THIS generator

Given in the task message. Category ids: `create` (new screen or feature; about half of them on an EXISTING app, half greenfield), `refactor` (structural change to existing UI), `polish` (visual/spacing/typography refinement, no structural change), `audit-review` (assessment without change; "what is wrong with", "check against", "is this ok"), `accessibility` (a11y symptoms and requests), `responsive` (viewport / window-size / orientation / keyboard-up behaviour), `tv-media` (ten-foot UI, players, remotes, set-top), `desktop-native` (WPF/WinUI/Avalonia/mac/Electron/Tauri windows, menus, accelerators, tray), `mobile-native` (SwiftUI/Compose/Flutter/RN phones and tablets), `kiosk` (public touch terminals, lanes, lobbies, wayfinding, gloves, timeouts), `adversarial` (out-of-scope engineering prompts that MENTION UI words — endpoints, migrations, bundlers, auth tokens, CI, database tables, unit tests, crash logs — expected `scope: abstain`; plus a few `scope: partial` prompts where a technical cause has a user-visible symptom, e.g. "list stutters when 5k rows re-render on every keystroke").

## Expectation format (one JSON object per case)

```json
{
 "id": "hv4-<generator>-<nnn>",
 "prompt": "...",
 "category": "create|refactor|polish|audit-review|accessibility|responsive|tv-media|desktop-native|mobile-native|kiosk|adversarial",
 "scope": "in-scope|partial|abstain",
 "artifact_state": "new|existing|unknown",
 "acceptable_modes": ["one or more of: create, refactor, polish, audit, review, accessibility, responsive, brand, design-system, reconstruct"],
 "platform": {"required": ["web|mobile|desktop|tv|kiosk|tablet"], "acceptable_inferred": ["..."]},
 "required_concerns": ["one or more of: accessibility, adaptive, anti-pattern, brand, component, content, data-display, environment, feedback, interaction, motion, navigation, performance, privacy, states, structure"],
 "required_concepts": ["3 to 7 ontology ids a good answer MUST cover"],
 "critical_concepts": ["subset of required (1-3): missing any of these makes the answer BAD"],
 "recommended_concepts": ["0-4 ids that would be nice"],
 "forbidden_concepts": ["1-4 ids that would be clearly wrong for this prompt"],
 "preservation": ["zero or more of: navigation, typography, color, behaviour — only when the prompt says or clearly implies what must stay"],
 "acceptable_alternatives": {"<required id>": ["<alternative id that also satisfies it>"]},
 "wording": {"explicit_mode_verb": false, "canonical_platform_name": false}
}
```

Rules for expectations:
- `acceptable_modes` lists EVERY mode a reasonable reviewer would accept as primary; a fix-a-defect observation usually accepts `audit` and `refactor` (or `polish` for purely visual defects); accessibility symptoms accept `accessibility` and `audit`; viewport symptoms accept `responsive` and `refactor`.
- `platform.required` only when the prompt states or unambiguously implies the platform; `acceptable_inferred` for what a reasonable reader would infer but not insist on. Never require a platform from a single weak hint.
- `artifact_state` is `existing` whenever the prompt talks about a screen that already behaves some way, even without the word "existing"; `new` for greenfield or a new screen; `unknown` only when genuinely unclear.
- `scope: abstain` cases need only id, prompt, category, scope, and `platform`/`wording`; other fields may be empty lists.
- `scope: partial` cases need required concepts for the design side only.
- Use ONLY ids from `ONTOLOGY.md`. Prefer specific ids over generic ones; do not list more than 7 required.

## Output

Write a single JSON file `gen-<generator>.json` in this folder: `{"generator": "<generator>", "model": "<your model name>", "cases": [ ... ]}`. Then report the counts per category, the share of prompts without an explicit mode verb, and the share of platform-specific prompts without a canonical platform name. Do not write anywhere else.
