# p6-26 — LumenTV (tvOS SwiftUI)

**Task sentence (verbatim):** "Titles on the poster rows are cut off and there is no way to read the full name."
**Project:** `research/phase3-projects/p3-tvos-swiftui/project` · Swift 5.9 / SwiftUI / SwiftPM · platform tv (tvOS, 1920×1080)
**Existing UI**, no new screen. Build hash start == end == `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` (candidate c3, unchanged).

## 1. Design context (`01-inspect.json`)

| field | detected | status | actual in code | correct? |
|---|---|---|---|---|
| navigation | tv-rails | KNOWN | `TabView` shell (Watch/Search) + horizontal `CardRail`/`TextTileRail` per section | yes |
| theme | dark-first | INFERRED | `.preferredColorScheme(.dark)`, canvas #0F1218 | yes |
| surfaces | elevated | INFERRED | `surface` #1A1F29 / `surfaceRaised` #242B38 + glow/shadow on focus | yes |
| radius | medium (8) | INFERRED | single radius token `LumenFocus.cornerRadius = 16` | partial (bucket right, value wrong; the 8 comes from a non-radius literal) |
| spacing | irregular | UNKNOWN | `LumenSpace` 8/16/24/40/64 + safeArea 60 — an explicit scale | partial (UNKNOWN where the code is unambiguous) |
| typography | custom | KNOWN | `LumenFont` display/title/headline/body/caption fixed-size scale | partial (`type_scale: false` although the scale is a named enum) |
| components | unknown | UNKNOWN | `Sources/LumenTV/Components/` (TVButtonStyle, QRCodeView) + shared rails | partial |
| tokens | `[]` | — | `Theme/Tokens.swift` defines colour, type, spacing and focus tokens | no |

The Swift token file is invisible to the inspector: `tokens: []`, `fonts: []`, spacing UNKNOWN. Platform, navigation and theme — the things the guidance keys off — are right.

## 2. Requirements (`02-requirements.json`)

- **platform** `tv` from project inspection — correct (`platform_evidence` is empty; the assignment came from the repo, not the sentence).
- **artifact_state** `existing`, `operations` [diagnose, modify], **problem_domain** [visual, responsive, layout], **change_scope** unknown/moderate — correct.
- **mode** `[polish, responsive, audit]`. polish and audit are right; **responsive is wrong** — tvOS is a single fixed 1920×1080 surface, and "cut off" was read as a viewport cue (`responsive: size/viewport cues with a defect`). Harmless here, but it is a mode miss.
- **scope.kind** `in-scope` ("UI design / interaction task") — correct.
- **change_budget** `low` — correct for a caption fix.
- **intent.preserve** `[]`; `constraints.preserve_existing_system: true` carried the preservation instead — acceptable.
- **project_context** as in §1.

## 3. Guidance (`03-guidance.md` / `.json`) — status PARTIAL, 8 records (core 2 + guardrails 6), ~1219 tokens, OPTIONAL layer empty

| record | layer | verdict | category | note |
|---|---|---|---|---|
| `comp-media-card` | core | relevant | — | "title below (1–2 lines, ellipsis)… one focusable element with an accessible name (title + status)" — exactly the component under repair. |
| `comp-mini-player` | core | off-target | wrong-screen | a picture-in-picture player this app does not have. Its clause "title (one line, truncated with a full title on focus)" is the right mechanism, but it arrives attached to the wrong screen. |
| `impl-reuse-before-new` | critical | partial | generic | SKILL.md §2 already says it; it consumed a bundle slot. |
| `tv-typography-distance` | critical | relevant | — | "titles ≤2 lines" set the expansion cap and confirmed 29 pt body stays. |
| `tv-dpad-axes` | critical | partial | generic | already satisfied (`.focusSection()` per rail); nothing to change. |
| `color-states-complete` | critical | off-target | generic | no colour/state work in a truncation fix. |
| `layout-spacing-scale` | critical | partial | generic | `LumenSpace` already is that scale. |
| `layout-hierarchy-one-thing` | critical | off-target | generic | screen-level hierarchy; says nothing about a caption. |
| *(bundle)* | — | — | **missing-critical** | `perf.layout_shift` absent — see below. |

**Concept recall** (pre-registered in `00-expectation.json`, written before any advise run):

| expected id | critical | delivered? | earliest wrong layer |
|---|---|---|---|
| `tv.ten_foot_typography` | yes | yes (`tv-typography-distance`) | — |
| `layout.media_card` | yes | yes (`comp-media-card`) | — |
| `perf.layout_shift` | yes | **no** | expected-concepts (never demanded; absent from the whole concept trace) |
| `content.i18n_expansion` | no | **no** | expected-concepts (never demanded) |
| `a11y.accessible_names` | no | yes (`comp-media-card`) | — |
| `tv.no_touch_hover` | no | **no** | bundle-selection (candidate `tv-no-touch-hover` existed, dropped at cap 8) |

recall 3/6 = **0.50**; critical recall 2/3 = **0.67**. The skill's own metrics report `concept_coverage_ratio 1.0` and `critical_coverage_ratio 1.0` — against its own demanded set, which never contained the one constraint that decides whether this fix is correct.

`perf.layout_shift` matters concretely: expanding a title on focus inside a horizontal rail moves the subtitle and every rail below unless the height is reserved. I hit exactly that defect at first render (§6) with no warning from the bundle.

Status PARTIAL here is not a design/engineering split — the uncovered concerns are `anti-pattern` and `performance`, i.e. coverage gaps, not out-of-scope work. Fine as a label.

## 4. Direction (`04-direction.md`) — 2 unjustified slots

11 of 13 slots preserved. Two are not:

- **cards → "Portrait poster cards (2:3)" (`card-poster-portrait`, status new)** — the codebase's rail cards are fixed `400×225` 16:9 and the file comment says `card-poster-landscape`. Reason given: "no repository evidence for this slot". At change budget `low` on an existing TV UI this is a contradicts-codebase recommendation, and the same file's fingerprint says `card_geometry: "poster-landscape"` — the direction disagrees with itself. **Ignored.**
- **imagery → "Poster art as primary recognition" (status new)** — benign, and its text ("title text below or revealed on focus") is the correct pattern, but it is still a `new` slot the task did not justify.

Also: the navigation slot is `preserved` but its prose describes a collapsed left side drawer (`nav-tv-side`) that this app does not have (it is a top `TabView`). The status is right; the attached guidance is not.

`validation: OK`, preservation metrics list navigation/layout/density/surface/typography/color/motion/focus/cta/icon/metadata preserved.

## 5. Implementation

**File changed:** `Sources/LumenTV/Search/SearchView.swift` (copy in `before/`). Nothing else touched.

- Extracted the two caption `Text`s of `CardRail` into a private `RailCardCaption` view that reads `@Environment(\.isFocused)` — the same convention `TVButtonStyle` and `TrackRow` already use.
- Resting: title `lineLimit(1)`, ellipsised. Focused: `lineLimit(2)`, which covers every title in the catalogue. On TV there is no hover and no tooltip, so the focused card is the only place a longer string can be revealed.
- The caption is one reserved block, `frame(width: 400, height: 114, alignment: .topLeading).clipped()` (2×38 body + 8 + 30 caption), so expanding on focus moves neither the subtitle nor the rail below it.
- Subtitle stays at one line: it is the synopsis / parent series, not "the full name", and a second reserved line costs 30 pt on every card. Deliberate scope call — the Series-rail synopsis is still ellipsised after the change.
- Accessibility unchanged: the card button's `accessibilityLabel` already carried the untruncated title and subtitle; the caption is now `accessibilityHidden(true)` so VoiceOver does not read it twice.

**Guidance used:** `comp-media-card` (1–2 lines + accessible name), `tv-typography-distance` (≤2 lines at 10 foot), `comp-mini-player` (the "full title on focus" mechanism, borrowed from the wrong screen).
**Guidance ignored:** `tv-dpad-axes`, `color-states-complete`, `layout-hierarchy-one-thing`, `layout-spacing-scale` (all already satisfied or not applicable), `impl-reuse-before-new` (followed, but from SKILL.md §2).

**Process guidance check:** not needed. SKILL.md §2 and §7 covered reuse-first and render-and-verify; `impl-reuse-before-new` in the bundle added nothing and cost a slot. `process_records_needed: false`.

## 6. Render (html-twin, Playwright 1.63.0, 1920×1080)

`render/twin.html` mirrors `Theme/Tokens.swift` and the `SearchView` results layout (tvOS pt == px at 1080p); `render/shoot.js` drives it. Catalogue titles are short, so the twin also renders a `?long=1` set (a longer series title, a German localisation, a subtitle-style long name) — that is where the defect the sentence describes is actually visible; `evidence-before-long-titles.png` is the pre-change state and shows the focused card's title ellipsised with nothing that can reveal it.

**First render defects (3 + 1 harness):**
- visual — title and subtitle were reserved as two separate fixed blocks (76 + 60), leaving a ~38 pt hole between them on every card (`first-01-search-rails.png`).
- visual — expanding the subtitle to two lines on focus was not worth 30 pt of permanent reserved space on every card.
- platform — the caption grew by 68 pt, pushing the Episodes rail's captions past the 1080 line and into the 60 pt bottom safe margin.
- implementation-bug (render harness, not the project) — the twin used `font: 400 29px/1.3 inherit`, an invalid shorthand, so all caption text rendered at 16px and nothing appeared truncated. Caught by comparing the caption size against the 23 pt eyebrow in the screenshot.

**Fixes (iteration 2):** one reserved caption block of 114 pt with the two texts in normal flow; subtitle back to one line always; twin CSS split into longhand properties.

**Final render:** `final-02-long-titles-focused.png` — the focused card shows "Blue Frontier: The Deep Plain Expeditions" on two lines while the unfocused neighbour stays ellipsised; the subtitle baseline is identical across focused and unfocused cards, so no rail shifts. `final-04-episodes-rail-scrolled.png` — moving focus to the Episodes rail scrolls it into view with its captions inside the safe area (the results screen is a vertical `ScrollView`; the added 38 pt only means the second rail scrolls sooner). **Final defects: 0.** Iterations: 2.

## 7. Preservation

Navigation, theme, typography tokens, focus treatment, spacing scale and the `TVButtonStyle` card style are untouched; the change is one extracted subview inside the existing `CardRail`. No structural change, no new tokens, no new files. `preservation-ok`.

## 8. Regressions to propose

1. Same sentence, tvOS project → the bundle must carry `perf.layout_shift` (reserve the expanded height so a focus change does not move the rail) and `tv.no_touch_hover` (no hover/tooltip on TV, so the focused item is the only reveal surface).
2. Same sentence → the direction must not introduce a new card geometry (`card-poster-portrait`) at change budget `low` on a TV codebase; the `cards` slot should be `preserved`, and it must not contradict its own fingerprint (`poster-landscape`).
3. "The episode name in the rail is truncated on tvOS" → no picture-in-picture / mini-player record in CORE.

## 9. Tags

`skill-helped`, `mode-miss`, `concept-miss`, `ranking-miss`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `preservation-ok`

**skill_effect: helped.** `tv-typography-distance` ("titles ≤2 lines") and `comp-media-card` ("1–2 lines, ellipsis", accessible name) fixed the expansion cap and kept me from a marquee/auto-scroll solution, and `comp-mini-player` named "full title on focus" — the TV-correct mechanism. Set against that: the bundle missed the layout-shift constraint entirely and the direction told me to change a card geometry the codebase already owns.
