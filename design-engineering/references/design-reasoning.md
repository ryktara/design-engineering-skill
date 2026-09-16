# Design reasoning: from signals to a direction

Read this for any create, redesign, design-system, or brand task. It defines the decision order and what "enough context" means. Style lookup is the last step, not the first.

## Contents
- Decision order
- The context ledger (KNOWN / INFERRED / MISSING)
- Product and user signals
- Environment and input signals
- From signals to structure
- From structure to visual system
- Screen-level checklist
- Explaining a recommendation

## Decision order

1. Task and user: what job is done here, by whom, how often, under what pressure, with what expertise.
2. Environment and input: web/mobile/tablet/desktop/TV/kiosk; touch/pointer/keyboard/remote; viewing distance; session length; ambient light.
3. Density and navigation: how much must be visible at once; how many peer destinations; switching frequency.
4. Layout topology and components: single column, master-detail, table-first, dashboard grid, rails, EPG, form stack, feed, editorial, workbench.
5. States: empty, loading, error, partial, long content, first use, offline.
6. Then the visual system: typography roles, colour strategy, surfaces, cards, iconography, imagery, motion, focus treatment.

Reversing the order (choosing "glassmorphism + purple + Inter" first) is the primary cause of generic output, because visual style cannot fix a wrong structure and a wrong structure looks the same for every product.

## The context ledger

Before recommending, write three lists and keep them in the final report:

- KNOWN: observed in the request or the repository (framework, tokens, fonts, breakpoints, platform targets, existing navigation, brand assets, user descriptions the user gave).
- INFERRED: reasonable conclusions with the evidence named ("finance product → high density on desktop"; "Android TV manifest → remote input").
- MISSING: material context that could not be derived. Ask only when it changes the result; otherwise proceed under a stated assumption.

`advise.py classify` and `advise.py direction` produce a first draft of this ledger; the repository inspection fills most of the rest. Never invent brand guidelines, personas, device classes, or design-system rules to fill gaps.

## Product and user signals

| Signal | What it changes |
|---|---|
| Product family (SaaS, ERP, e-commerce, finance, media, healthcare, marketing, devtools, content, social, education, government, IoT) | default density, navigation model, metadata richness, tolerance for imagery and motion |
| User type (expert daily user vs. occasional public user) | density, shortcuts, discoverability, error tolerance, onboarding |
| Primary task (enter, monitor, find, compare, browse, consume, decide, configure) | layout topology and the one focal element |
| Task frequency (many times a day vs. yearly) | learnability vs. efficiency; whether to persist state and offer shortcuts |
| Complexity (fields, records, steps) | wizard vs. form, table vs. list, palette vs. menus |
| Trust requirements (money, health, legal) | restraint, confirmations, status language, no playful motion |
| Content density of the data itself (dense tables vs. media art) | typography scale, card geometry, surfaces |
| Business goal (conversion, retention, throughput, compliance) | where the CTA lives and how loud it is |

## Environment and input signals

| Environment | Consequences that cannot be skipped |
|---|---|
| Web (pointer + keyboard + touch) | responsive matrix, focus-visible rings, hover as enhancement only, container/viewport breakpoints from the codebase |
| Mobile (touch) | thumb reach, 44 pt / 48 dp targets, safe areas and IME insets, platform navigation grammar, Dynamic Type / font scale |
| Tablet | two-pane layouts at regular width, pointer + keyboard possible, split-view behaviour |
| Desktop (pointer + keyboard) | window resizing and DPI, shortcuts and access keys, context menus, 4 px grid, persisted workspace state |
| TV (remote / DPAD) | one visible focus, straight-path navigation, 10-foot type scale, overscan margins, rails, no touch/hover/scrollbars, BACK semantics |
| Kiosk (touch, public) | ≥60 px targets, reach ranges, idle timeouts, one task per screen, glare contrast |

Load the platform file for the detected environment; its rules override generic web habits.

## From signals to structure

Navigation model by destination count and switching frequency:

- ≤3 destinations, marketing/content: top bar (web) or single screen.
- 3–5 frequent destinations on phones: bottom tabs.
- 6+ peer sections, daily tools on wide screens: left rail.
- Deep hierarchies: tree + breadcrumb.
- Infrequent distinct tasks (bank, government, kiosk): hub and spoke.
- Ordered dependent steps: wizard.
- TV: side navigation (4–8 sections) or top tabs (2–5); vertical axis = sections, horizontal = items.
- Power users: add a command palette; it never replaces visible navigation.

Layout topology by primary task:

- Enter or edit one record → form stack (sections, one column).
- Work a record set → table-first (toolbar + filters + table + optional panel).
- Scan then act on one item at a time → master-detail.
- Navigate + list + inspect → three-pane workbench (desktop).
- Monitor several independent things → dashboard grid sized by importance.
- Browse by artwork → catalog grid (web/mobile) or rails (TV).
- Consume a stream → feed.
- Read → editorial column.
- Live TV schedule → EPG grid.
- Play media → canvas with transient controls.

Density is a property of the user and the platform: experts on desktop go high; the public on touch stays medium; TV and kiosk are low-to-medium by viewing distance and input precision. Achieve density by tightening spacing and control sizes coherently, never by shrinking text below the platform floor.

## From structure to visual system

Only now choose:

- Typography character (neutral sans for tools, system font for native, humanist for public services, grotesk/serif display for brand-led surfaces, condensed for broadcast, monospace accents for developer tools). See typography.md.
- Colour strategy (neutral + accent for tools, dark + accent for TV/consoles, dominant brand for marketing/consumer, duotone/multicolour when the brand or category logic demands). See color.md.
- Surface strategy (flat tonal layers by default; bordered panes for workbenches; elevated cards only for tappable objects; imagery-backed for media; glass only with a platform material and a reason).
- Card geometry (none by default; tiles, rows, posters when the item boundary means something).
- Iconography, imagery, motion, focus treatment per platform.

Each choice in the direction output names the signals that selected it and the alternatives considered. If a choice contradicts the codebase, the codebase wins unless the task is to change it.

## Screen-level checklist

For every substantial screen, decide and state: purpose; primary user action; information hierarchy with one focal point; navigation in and out; main visual anchor; secondary information; density; empty/loading/error/partial states; hover/focus/pressed/selected states for the input model; responsive or adaptive behaviour; accessibility semantics; visual identity elements that are specific to this brand and not to the template.

## Explaining a recommendation

Every important recommendation should be able to answer: why it fits (signals), what evidence supports it (KNOWN/INFERRED), what was rejected and why, and what risks remain (accessibility, performance, platform). `advise.py … --explain` exposes the machine part of this; the reasoning about the specific product is yours. Keep the explanation in the working notes and the report; do not pad the user-facing summary with it.
