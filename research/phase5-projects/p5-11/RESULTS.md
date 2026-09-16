# p5-11 — results

## Task
"From the sofa nobody can tell which row is selected on the living-room screen." (run verbatim)

## Project / stack / platform
`research/phase3-projects/p3-tvos-swiftui/project` — Lumen, tvOS 17, SwiftUI, Swift-package layout (`Package.swift`, `Sources/LumenTV/{App,Theme,Components,Models,Search,Player,SignIn}`). Platform **tv**, input Siri Remote. Existing UI (CatalogueShell top tabs → Watch / Search; Search shows Series / Episodes rails and Topics tiles; shared `TVButtonStyle`). No new screen.

Build hash start = end = `bf034323a2b68202e8c902768e0de78cd93761b1a71670a49ee595648cd5f0d8` (skill untouched).

Render mode: **html-twin + static review** (no Xcode). The Phase 3 twin (`render/twin.css`, `search.html`, `player.html`) was copied into `p5-11/render/`, updated to mirror the Swift change, and driven with Playwright 1.63.0 / Chromium at 1920×1080 (arrows = swipe/D-pad). `first-*` screenshots come from the untouched Phase 3 twin, `final-*` from the updated copy. `measure.js` reads computed styles and pixel luminance before/after; `measure-first.json` / `measure-final.json` hold the numbers.

## What the code did before (reviewer diagnosis, written before running the skill — see `00-expectation.json`)
Focus = 4 pt white ring + lift 1.04/1.08 + black drop shadow; secondary/tile fill steps `surface #1A1F29 → surfaceRaised #242B38` = **1.16:1** between the focused and unfocused state (the ring was the only carrier). Cards: ring on the 400×225 art only. Nothing marks the **row**: every rail heading stays text.primary and unfocused rails are not dimmed. The 4 px ring is ≈2.9 arcmin at 3 m on a 55" panel — at the edge of what a viewer resolves.

## Design-context table (`01-inspect.json`)
| field | detected | status | actual (code) | correct? |
|---|---|---|---|---|
| platforms | tv | KNOWN | `.tvOS(.v17)` only | yes (Phase 3's spurious `mobile` is gone) |
| navigation | tv-rails | KNOWN | top `TabView` (Watch, Search) + horizontal rails inside Search | yes (rails are the content structure; "bottom-tabs" candidate scored 1 and was not chosen) |
| theme | dark-first | INFERRED | `.preferredColorScheme(.dark)`, `LumenColor.canvas #0F1218`, tokens comment says dark-first | yes (could be KNOWN: the code is explicit) |
| surfaces | elevated | INFERRED | flat tinted fills (`surface`, `surfaceRaised`); shadow only on the focused control | partial |
| radius | medium | INFERRED, evidence "8 (1×), others [24]" | `LumenFocus.cornerRadius = 16` on every control, 24 on the next-episode card; the 16 token was not seen | partial (right label, wrong evidence) |
| spacing | irregular | UNKNOWN | `LumenSpace` 8/16/24/40/64 + 60 safe area — a clear scale | partial (UNKNOWN when the code is clear) |
| typography | unknown, `type_scale: false` | UNKNOWN | `LumenFont` 76/48/34/29/23 with weights, system font | partial (an explicit scale exists) |
| components | unknown | UNKNOWN | `Components/TVButtonStyle.swift`, `CardRail`, `TextTileRail`, `TrackRow` | partial |
| tokens / icons / tests / i18n | [] | — | `Theme/Tokens.swift`, SF Symbols, `Tests/LumenTVTests`, `Localizable.xcstrings` | no (all missed, unchanged from Phase 3) |

## Requirements verdict (`02-requirements.json`, status CONFIDENT)
| field | value | verdict |
|---|---|---|
| platform_evidence | tv, STRONG_INFERENCE ("living-room", "from the sofa", "sofa") | correct. But `missing: platform only inferred from wording; confirm before committing` although the project inspection carries `Package.swift: tvOS target` KNOWN — project evidence is not promoting the platform; the confirm is noise and downgrades guidance to PARTIAL (exit 3). |
| intent.artifact_state | existing | correct |
| intent.operations | diagnose, modify | correct |
| intent.problem_domain | interaction | partial — the defect is visual/accessibility (focus-state contrast at distance); "interaction" only because of the word "select". This is probably why `a11y.contrast` stayed a recommended, not required, concept. |
| intent.change_scope | screen | correct |
| mode + evidence | audit, refactor ("interaction defect on existing UI", "fix follows the diagnosis") | acceptable (expected polish/accessibility/refactor); the pair is reasonable for a symptom sentence |
| scope.kind / reason | in-scope, "UI design / interaction task" | correct |
| change_budget | moderate | correct |
| intent.preserve | [] | acceptable (no explicit cue); navigation/theme preservation came from the direction's preserved slots instead |
| project_context | as in the table above | see context table |
| accessibility flags | keyboard, screen_reader, focus, reduced_motion, contrast | `keyboard: true` is wrong for a remote-only platform; the rest are right (reduced_motion and contrast flagged here, yet neither became a required concept) |

## Guidance verdict (`03-guidance.md/json`, bundle 2 core + 5 guardrails, 1199 tokens, status PARTIAL because of the platform confirm)
| record | role | verdict | note |
|---|---|---|---|
| `media-resume-and-details` | core | off-target → **generic** | Details screen, watchlist, resume rows. Picked as "highest-scoring component with lexical evidence" (words "row", "selected"). Nothing about focus visibility. Not used. |
| `layout-rails` | core | partial | Rail structure, pivot, focus memory, safe margin. Already implemented in `CardRail`; nothing about how the focused row/card should look. |
| `color-states-complete` | guardrail | partial | Its one useful line — "selected ≠ focused" — drove the `TrackRow` fix. The rest (hover/pressed state tokens, "Dark theme redefines all of them") is web/desktop framing. It is the *only* record in the bundle that carries `interaction.focus_visible`, while the base has `a11y-focus-visible` ("≥3:1 against the unfocused state; on TV obvious at 3 m — scale + border/glow"), which is the actual rule for this task, and `a11y-tv-focus-always`. |
| `tv-typography-distance` | guardrail | partial | Demanded because "from the sofa" → `tv.ten_foot_typography`. The type scale already meets it (29/23 pt); nothing to change. |
| `tv-dpad-axes` | guardrail | partial | Reachability, not visibility. Verified unchanged. |
| `tv-safe-area` | guardrail | relevant | Constrained the fix: the 6 pt ring is drawn inside the control and the lift stays 1.04 so a leading card lifts to 52 px ≥ 48 px overscan limit. |
| `web-virtualize-long-lists` | guardrail | off-target → **off-platform** | aria-rowcount / windowed rendering for the "performance" concern; `LazyHStack` already virtualises. |

Relevant 1 · partial 4 · off-target 2. Missing-critical (bundle): no record states the focus-indicator contrast requirement (`a11y-focus-visible`, `a11y-nontext-contrast`) or the TV dark-palette contrast rule (`tv-dark-first`), even though both were candidates (0.36 / 0.243 / 0.36) — they were only *recommended* concepts and fell to the cap. `comp-tv-rail` was omitted as "contamination: tv-rail-specific record with no tv-rail evidence in the request" while the project context says `navigation = tv-rails (KNOWN)` — the contamination check ignores project evidence.

### Concept recall (delivered = union of `concepts` over the 7 selected records)
Delivered: media.details_play_first, media.resume_playback, media.watchlist, interaction.focus_restore, interaction.back_semantics, a11y.color_not_only, interaction.focus_visible, interaction.selection_visible, tv.ten_foot_typography, interaction.dpad_reachability, tv.safe_margins, table.virtualization.

| expected id | delivered? | layer if missing (from `concept_trace`) |
|---|---|---|
| interaction.focus_visible (critical) | yes (`color-states-complete`) | — (but the weakest carrier; `a11y-focus-visible` 0.36, `a11y-tv-focus-always` 0.36, `focus-scale-glow` 0.359 lost to it at 0.458) |
| a11y.contrast (critical) | **no** | bundle-selection — recommended only; carriers `tv-dark-first` 0.36, `a11y-contrast-text` 0.269, `a11y-nontext-contrast` 0.243 "left out by the bundle cap or lower utility". Root cause one layer earlier: concerns never made it required. |
| tv.ten_foot_typography | yes | — |
| tv.dark_first | no | bundle-selection (recommended, `tv-dark-first` 0.36 dropped) |
| a11y.reduced_motion | no | expected-concepts (never demanded, although requirements set `accessibility.reduced_motion: true`) |
| interaction.selection_visible | yes | — |
| tv.no_touch_hover | no | bundle-selection (recommended, `tv-no-touch-hover` 0.36 dropped) |

Recall 3/7 = **0.43**; critical recall 1/2 = **0.50**. No forbidden concept was delivered. `table.virtualization` and the three `media.*` ids are noise for this task.

## Direction verdict (`04-direction.md/json`, validation OK)
| slot | choice | status | justified? |
|---|---|---|---|
| navigation | `nav-tv-side` "Preserve existing navigation: tv-rails" | preserved | wrong mapping — the existing shell is top tabs; `tv-rails` is a layout fact, and the preserved slot text describes a side drawer the app does not have. Harmless only because it says "do not replace". |
| layout | `layout-rails` | new | exists already; "new" is wrong for a KNOWN-rails project |
| density | `density-medium` (web text: "8 px base, 40–48 px heights, 16 px body") | new | not justified; wrong platform numbers |
| surface | preserve elevated | preserved | ok |
| cards | `card-poster-landscape` | new | exists already (`CardRail` 16:9); not justified as new |
| typography | `typography-grotesk-display` (Bricolage Grotesque…) | new | **not justified** — contradicts the system-font tvOS codebase and `stacks/swiftui.md`; ignored |
| color | preserve dark-first (`color-dark-accent`) | preserved | ok, and its "≥7:1 body text on TV" line is the only contrast rule the skill produced |
| motion | `motion-crossfade` | new | not justified (task has no transitions); ignored |
| focus | `focus-scale-glow` | new | the one slot that matches the task; "border 2–4 dp or glow, scale, selected ≠ focused" — but the numbers are Android dp at 960×540 (= 4–8 px at 1080p), so the app's 4 pt ring was already "in range" and still failed. Its swiftui note ("tvOS gives .focusable() views the system lift; add custom borders only when brand demands") is right in general and irrelevant here because `TVButtonStyle` replaces the system style. |
| cta | `cta-focus-selects` | new | already true; fine |
| imagery | `imagery-immersive-backdrop` | new | not justified; ignored |
| icon | `icon-filled-system` | new | already true |
| metadata | `metadata-focus-reveal` | new | not justified for a focus-visibility fix; ignored |

Preserved 3, changed 0, new 10 for a moderate-budget fix on an existing app: the direction is generated from platform+product, not from the task. Preservation metrics in the JSON: `preserved ['navigation','surface','color']`, `changed []`.

## Implementation
Files changed (copies of the originals in `before/`):
- `Theme/Tokens.swift` — `LumenColor.focusFill` (white 0.92); `LumenFocus.ringWidth` 4 → 6; `glowRadius` 28 / `glowOpacity` 0.35; `restingRowOpacity` 0.45; `rowMarkerWidth` 8. Comments carry the numbers (13.9:1 fill step, 4.3 arcmin ring, 4.8:1 floor for dimmed secondary text).
- `Components/TVButtonStyle.swift` — focused secondary/icon fill → `focusFill` with `canvas` label (was surfaceRaised, 1.16:1); white glow shadow added before the black drop shadow; ring 6 pt (drawn inside via `strokeBorder`, so the overscan budget is unchanged). Primary and card prominences keep their fill; Reduce Motion still drops only the lift.
- `Search/SearchView.swift` — `@FocusState var focusedRail: String?` in `SearchResultsView`; `railFocus(id, focused:)` modifier binds each rail container with `.focused($focusedRail, equals: id)`, injects `railFocusState` (neutral / focused / resting) into the environment, and sets opacity 0.45 on resting rails; new `RailHeading` (accent capsule marker beside the heading of the rail that holds focus, space always reserved; heading text.secondary while resting). `CardRail` / `TextTileRail` use `RailHeading`. With no rail focused (search field / keyboard) nothing dims.
- `Player/TrackPickerSheet.swift` — `TrackRow` takes `isFocused` (from the sheet's `focus` binding) and switches label + checkmark to `canvas` on the light focused fill (accent on #EBEBEB would be 1.9:1); selected stays the checkmark + accent text at rest, so selected ≠ focused holds.
- Twin: `render/twin.css`, `search.html`, `player.html` mirror the above (the twin's search field keeps the system-field treatment because in Swift it is `.searchable`, not `TVButtonStyle`).

Static-review risk (no compiler): `.focused(_:equals:)` on a non-focusable rail container is relied on to reflect focus on any descendant card (SwiftUI focus-state propagation); if a tvOS version does not propagate it, `focusedRail` would stay nil and the screen degrades to the pre-change behaviour (no dimming, no marker) — the card ring/fill/glow changes do not depend on it.

Guidance used: `tv-safe-area` (lift + ring inside the 48 px limit — verified: leading card lifted left edge 52 px); `color-states-complete` "selected ≠ focused" (TrackRow); `color-dark-accent` "≥7:1 on TV" from the direction's colour slot (dimmed secondary text kept ≥4.5:1, primary ≥7:1). Guidance ignored: `media-resume-and-details` (wrong screen), `web-virtualize-long-lists` (nothing to do), typography/motion/imagery/metadata/cards/density direction slots (contradict the existing system or the task). Not provided by the skill and supplied by me: focused-vs-unfocused contrast as the diagnosis, the ring-thickness-at-distance argument, the light-fill inversion (tvOS system convention), and the row-level cue (dim resting rails + heading marker).

## Measurements (`measure-first.json` → `measure-final.json`, Episodes rail, card 2 focused)
| metric | before | after |
|---|---|---|
| tile / secondary fill, focused vs unfocused | #242B38 vs #1A1F29 = **1.16:1** | #ECECED vs #1A1F29 = **13.98:1** |
| label on focused fill | 12.2:1 (white on surfaceRaised) | 15.9:1 (canvas on light fill) |
| ring | 4 px, 18.75:1 on canvas / 16.5:1 on surface, ≈2.9 arcmin at 3 m on 55" | 6 px, same colours, ≈4.3 arcmin, + 28 px white glow |
| resting rails | opacity 1, heading text.primary (no row cue) | opacity 0.45, heading text.secondary, accent marker on the focused rail's heading |
| pixel mean luminance, focused card box vs right neighbour | 1.33 | 1.32 (ring inset; the glow spreads outside the box) — the card-level gain is the fill/ring, not luminance |
| mean luminance, focused rail box vs brightest other rail | 1.51 | 1.54 (rails are mostly canvas; the visible change is the dimmed art/text and the marker — see `final-rows-*.png`) |
| 1/4-scale ("10-foot") card vs neighbour | 1.33 | 1.30 |
| lifted focused card vs 48 px overscan limit | ok (472/490/888/814) | ok; leading card in the first rail: left edge 52 px |
| reduced motion | lift none, ring kept, 0 rails resting | lift none, ring kept, 2 rails resting (row cue survives) |

## First-render defects → fixes → final
First render (iteration 1):
- visual 1 — row dim at 0.55 too subtle over dark artwork; the Series rail barely changed. Fix: 0.45 (kept secondary text ≥4.5:1) + accent heading marker on the focused rail (twin + Swift).
- accessibility 1 (twin only) — the twin's search field is a `.btn` and inherited the light-fill inversion, leaving grey placeholder on a light fill (~1.6:1). In Swift the field is the system `.searchable` bar and unaffected. Fix: twin keeps the system-field treatment.
- platform 1 (twin only) — the twin drew the ring outside the art (box-shadow spread), so a lifted leading card's ring edge sat at 46 px < 48 px overscan limit; Swift draws it inside (`strokeBorder`). Fix: inset ring in the twin (iteration 2).
Final defects: 0. Iterations: 2.

## Preservation
Navigation (TabView, rails, focus sections, Menu semantics) unchanged; theme tokens unchanged (one token added, ring width changed); typography unchanged; `TVButtonStyle` reused and extended rather than replaced; no route/state/test/id/accessibility change except the new `.isHeader` heading container (same trait as before) and the marker marked `accessibilityHidden`. Unjustified structural changes: 0.

## Regressions to propose
1. Query: the task sentence with a tvOS project. Expect: `a11y.contrast` and `interaction.focus_visible` **required**; carrier for focus_visible is `a11y-focus-visible` or `a11y-tv-focus-always` (TV-specific ≥3:1 / obvious at 3 m), not `color-states-complete`; `a11y.reduced_motion` at least recommended when requirements set `reduced_motion: true`; no `media-resume-and-details` core.
2. Query: any tv sentence with a project whose inspection says `tvOS target` KNOWN. Expect: no "platform: only inferred… confirm" MISSING entry; guidance status CONFIDENT.
3. Query: any rail/row sentence with `navigation = tv-rails (KNOWN)`. Expect: `comp-tv-rail` not rejected as "no tv-rail evidence in the request".
4. Direction for an existing SwiftUI tvOS app, mode audit/refactor, budget moderate. Expect: typography/cards/layout/motion slots **preserved** (system font, existing `CardRail`, existing rails), not "new"; navigation preserved text must describe the detected shell (top tabs), not `nav-tv-side`.
5. Requirements on tv platform. Expect: `accessibility.keyboard` false / `focus` true.

## Tags
`requirements-miss`, `concept-miss`, `ranking-miss`, `knowledge-gap`, `direction-mismatch`, `context-detection-miss`, `render-defect-fixed`, `tooling-limit`, `skill-neutral`, `preservation-ok`

## Knowledge gaps (no record in the base)
- Row-level focus cue on rail screens (dimming rails that do not hold focus, heading emphasis/marker) — `search` returns rail structure and focus memory only.
- Focus-fill inversion as the tvOS convention (focused control goes light, label dark) — `focus-scale-glow` mentions border/glow/scale only.
- Ring thickness vs viewing distance (px → arcmin at 3 m) — `focus-scale-glow` gives "2–4 dp" in the Android 960×540 frame with no tvOS 1080-pt translation; the app's 4 pt was "in range" and still failed the task.
- Contrast between the focused and unfocused *fill* as a measurable (the base has ≥3:1 for the indicator only, in `a11y-focus-visible`, which was not selected).
