# p6-27 — Meridian TV channel guide: time header jumps every half hour

**Task sentence (verbatim):** "In the channel guide the time header jumps every half hour and you lose where you were."

**Project:** `research/phase6-projects/p6-tv-iptv-web/project` — Meridian TV, plain HTML/CSS/ES5 smart-TV web app (Tizen/webOS key codes, no framework, no build). 983 LOC. **Platform:** TV (1920×1080, d-pad).
**Existing UI**, not a new screen. Concurrent task owns the player overlay — only `GuideScreen` and the `/* guide */` CSS block were touched.

**Build hash start:** `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947`
**Build hash end:** `ea8eed723aa6b2aa24cf367ef723e3289197525987d4e43311cd6073575d9947` — equal, skill untouched.

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual in code | Correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | `<header class="topbar">` with Home/Guide/Settings pill nav | yes |
| theme | dark-first | INFERRED | `--bg:#0E1116`, dark-only palette in `tokens.css` | yes |
| surfaces | bordered-flat | INFERRED | flat `--surface` fills, 1px `--line` borders, zero shadows | yes |
| radius | small | INFERRED | `--radius:8px`, cells 6px, pills 999px | partial — reported "most common radius 4 (2×)", but 4px is the *card-badge/progress* radius; the token is 8px and the guide cell is 6px. Right bucket, wrong evidence. |
| spacing | 4 | INFERRED | `--gap:24 / --gap-lg:40`, everything on a 4px multiple | yes |
| typography | unknown | UNKNOWN | `--font: "Roboto", "Segoe UI", …` **is** declared in `tokens.css`, plus a full 28/32/40/56/72 TV scale | **no** — a confident UNKNOWN on a field the code states plainly. The sub-object did detect `type_scale:true` and `tabular_numerals:true`, so the signal was read and then discarded at the family level. |
| components | unknown | UNKNOWN | no library; hand-rolled `.card`, `.guide-cell`, `.btn`, `.ctl` | partial — "no library" is true, but the project clearly has an internal component vocabulary |

Platform detection in `inspect_project.py` says `platforms: ["web"]` only. `config.xml` + `appinfo.json` (Tizen widget + webOS appinfo), `js/keys.js` with Tizen/webOS key codes, and a hard 1920×1080 body are all present and are strong TV evidence that inspection did not use. The advise layer recovered TV from the sentence wording instead.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Skill | Expected | Verdict |
|---|---|---|---|
| platform | `["tv","web"]`, tv STRONG_INFERENCE from "channel guide"/"channel"; MISSING "confirm before committing" | tv | acceptable — right platform, but from the sentence, not the repo; "web" rides along from inspection |
| artifact_state | existing | existing | yes |
| operations | diagnose, modify | diagnose + modify | yes |
| problem_domain | performance-ux | perceived-motion/orientation defect | yes |
| change_scope | screen | screen | yes |
| mode | audit + refactor ("perceived-performance defect" / "fix follows the diagnosis") | refactor / polish / audit | yes — and the sentence carries no mode word, so this was inferred correctly |
| scope.kind | in-scope (UI_INTERACTION) | in-scope | yes |
| change_budget | moderate | moderate/low | yes |
| intent.preserve | `[]` | navigation, theme, typography | miss — nothing preserved explicitly; the direction layer compensated by preserving every slot |
| status | CONFIDENT (requirements) / PARTIAL (guidance) | — | the PARTIAL comes from one uncovered required concept, not from a scope split; the design/engineering split is not at issue here |

## 3. Guidance verdict (`03-guidance.md`)

Bundle = 5 records (core 2 + guardrails 3), OPTIONAL layer empty, 840 tokens.

| Record | Layer | Verdict | Category |
|---|---|---|---|
| `layout-epg-grid` | core | **relevant** — carried the whole fix: "current time line always visible", "LEFT/RIGHT move within a channel's programmes (not by pixel)", "sticky channel column and time header", "a shortcut jumps to now" | — |
| `comp-epg` | core | **relevant** — "focus moves by programme not by pixel", "jump-to-now shortcut", "now line updates every minute" | — |
| `a11y-tv-focus-always` | critical | **relevant** — "keep focus on screen (scroll into view)" is the exact invariant the old snap violated | — |
| `tv-no-touch-hover` | critical | **partial** — true and on-platform, but the codebase already has zero hover/scrollbar affordances; nothing to do | `generic` |
| `layout-states-empty-loading-error` | critical | **off-target** — the guide is built from a synchronous seeded array; there is no loading/empty/error state and the task is not about one | `generic` |

`layer_review`: core `[layout-epg-grid, comp-epg]`, critical `[a11y-tv-focus-always, tv-no-touch-hover, layout-states-empty-loading-error]`, optional `[]`, optional_useful 0, optional_noise 0.

The two core records overlap heavily (redundancy 0.3 reported; `comp-epg` literally opens with "See the EPG grid pattern for structure"). Two near-duplicate records for a 5-record bundle is a ranking inefficiency, not a defect — I marked neither off-target because the second one did add "focus moves by programme not by pixel" as an explicit line.

### Concept recall

| Expected id | Critical | Delivered? | Layer if missing |
|---|---|---|---|
| `tv.time_navigation` | yes | yes (`layout-epg-grid`, DIRECT) | — |
| `navigation.orientation_and_back` | yes | **no** | `expected-concepts` — never demanded; it appears nowhere in the 24-entry concept trace, so no retrieval was ever attempted. This is the "you lose where you were" half of the sentence. |
| `interaction.focus_visible` | yes | yes (`a11y-tv-focus-always`) | — |
| `tv.epg_pinned_channels` | no | yes (`layout-epg-grid`, DIRECT) | — |
| `interaction.dpad_reachability` | no | yes (`comp-epg`) | — |
| `perf.focus_latency` | no | **no** | `bundle-selection` — demanded as *recommended*, candidates `tv-focus-performance`, `tv-dpad-hold-pacing`, `comp-tv-rail` existed and were dropped by the cap |

**Concept recall 4/6 = 0.67. Critical recall 2/3 = 0.67.**
(The skill's own metrics report critical_coverage 1.00, but its critical set is only `{tv.epg_pinned_channels, tv.time_navigation}` — it never promoted an orientation concept to critical.)

The skill also flagged `interaction.keyboard_navigation` as a required concept it could not cover. That one is a false requirement here — it was demanded because inspection labelled the project "web"; on a d-pad TV app `interaction.dpad_reachability` is the right concept and it *was* covered. So the PARTIAL status is an artefact of the platform mis-detection in step 1.

**Process guidance check.** `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` were **not** in the bundle and were **not** needed — SKILL.md §2/§7 was enough; the codebase has one obvious owner function (`GuideScreen`) and one CSS block, and I rendered before and after by default. `process_records_needed: false`. (`process.reuse_first` shows as an uncovered *recommended* concept; dropping it cost nothing.)

## 4. Direction verdict (`04-direction.md`)

All 13 slots `preserved`, 0 `changed`, 0 `new`. `unjustified_direction_slots: 0` — correct for an existing UI at a moderate budget on a behavioural defect.

One contradiction: **Validation: VIOLATIONS — "tv/remote: navigation 'top-bar' is a pointer/touch model"**. The direction preserves `nav-top-bar` (right call, repository evidence) and then validates it as a TV violation in the same document. The top bar here is d-pad reachable (`handleKey` routes UP from the first row into the nav, DOWN back out), so the violation is wrong on this codebase. Harmless in practice — the slot table told me to preserve it and I did — but it is an internally inconsistent output. Tagged `direction-mismatch`.

## 5. Implementation

Files changed (copies in `before/`): `js/app.js` (GuideScreen only), `css/tv.css` (guide block only). No changes to `tokens.css`, `index.html`, `focus.js`, `keys.js`, `data.js`, or any other screen.

**Root cause.** `GuideScreen` kept a single integer `headerSlot` and scrolled everything by `headerSlot * 240px`, re-snapping it to the half-hour slot containing the focused programme's *start*. Three consequences: the timeline lurched a whole half-hour column per focus move; the clamp `if (headerSlot > slots - 6) headerSlot = slots - 6` broke the keep-in-view invariant so the focused cell could sit off-screen; and there was no time reference that survived the jump.

**Changes:**
1. Replaced slot-quantised scrolling with continuous `scrollX`/`scrollY` in pixels, moved by `ensureVisibleX`/`ensureVisibleY` — the minimum distance that brings the focused cell fully into view with a 64px / one-row lead margin, clamped to the timeline extent. When the focused cell is already visible the timeline does not move at all.
2. Vertical rows moved from the same fixed `(ri - 3) * rowH` paging to the same keep-in-view rule.
3. Header restructured: a fixed **"From HH:MM" anchor** in the channel-column gutter that always names the time at the left edge of the visible window, plus a clipped label track. Previously the header had `padding-left: 260px` and translated its own children, so labels bled into the channel-column gutter; they are now clipped.
4. Half-hour labels got a 1px `--line` left tick so each label is visually bound to its column now that the scroll is continuous.
5. `now-line` hides when scrolled off *either* edge (it only checked the left before); a **`◀ HH:MM` / `HH:MM ▶` edge chip** in the header names the live time and which way it is when off-screen.
6. **Jump-to-now on the GREEN key** (`GuideScreen.onKey`), focusing the on-air cell in the current row; a green `NOW` chip in the gutter makes the key discoverable (TV has no hover to discover it any other way).

**Guidance used:** `layout-epg-grid` (now-line always visible, jump-to-now shortcut, sticky header/channel column, move by programme not pixel), `comp-epg` (jump-to-now, now-line updates), `a11y-tv-focus-always` ("keep focus on screen (scroll into view)" — this is the invariant the fix is built on).
**Guidance ignored:** `tv-no-touch-hover` (already satisfied by the codebase; nothing to change); `layout-states-empty-loading-error` (the guide has no async data — implementing loading/empty/error here would be invented work); `layout-epg-grid`'s "two-dimensional virtualisation" and "minimum cell width" (virtualisation is a perf refactor the sentence does not ask for; the shortest programme in `data.js` is 30 min = 240px, so no minimum-width problem exists); `comp-epg`'s "day picker", "detail strip", "mini preview" (new features, outside a moderate budget on a defect fix).

**skill_effect: helped.** The jump-to-now shortcut and "now line always visible" are the two things I would most plausibly have under-specified — my own reading diagnosed the snap and the keep-in-view break, but I would likely have shipped a pure scrolling fix with no recovery affordance. Those came from `layout-epg-grid` / `comp-epg`.

## 6. Render

**Render mode: native (Playwright, Chromium, 1920×1080).** Static server over `project/`, real d-pad key presses (`ArrowUp/Right/Enter` to reach the guide, then Right/Down/Left), GREEN dispatched as Tizen keyCode 403. Screenshots `render/first-*.png`, `render/final-*.png`; `render/shoot.js` is the harness. No console or page errors in either pass.

### First-render defects (2)
| # | Type | Defect |
|---|---|---|
| 1 | visual | The `NOW` edge chip was placed in `.guide-body` at the top-left and covered the first channel row's programme cells (visible in `first-03-guide-right7.png` over row 101). |
| 2 | visual | The GREEN hint was a flex sibling of the header track, so the label track was ~148px narrower than the cell area: the rightmost half-hour label rendered clipped as "05:0(" and the last ~148px of cells had no label above them. |

Neither was warned about by the guidance. Both fixed in iteration 2: the edge chip moved into the header track (absolute, bottom-aligned) and the GREEN hint moved into the anchor gutter, giving the label track the full timeline width.

### Final defects (0 blocking; 1 accepted trade-off)
`final-03-guide-right7.png` — when now is off-screen, the `◀ 23:39` chip occludes the leftmost half-hour label. Accepted rather than fixed: that label is the one already duplicated by the persistent "From 02:26" anchor two columns to its left, and the chip only exists while now is off-screen. Recorded as a trade-off, not counted as a defect.

**Iterations: 2.**

### Behavioural before/after (measured, not asserted)
Same 21-keypress d-pad script against the `before/` build and the final build, reading the actual `translateX` off `.guide-cells` after each press:

| | scroll deltas | focused cell off-screen |
|---|---|---|
| before | 720, 720, 0×11, −240, −240, −960, 0×4 — **every non-zero delta an exact multiple of 240px (30 min)** | 1 of 22 states |
| after | 392, 960, 60, 0×11, −156, −360, −896, 0×4 — arbitrary minimal pixel values | **0 of 22 states** |

The 960px delta is a 120-minute cell that is itself 960px wide — that is the minimum scroll, not a snap.

## 7. Preservation

`preservation-ok`. Top-bar navigation, the routing stack, `focus.js` scope/geometry model, all key codes, `tokens.css`, the TV type scale, the dark palette, `--focus-ring`/`--focus-scale`, the 4px spacing rhythm, `.guide-cell`/`.guide-ch` structure, programme ids, `data-focus-scope` per row and the `click` → detail handlers are all unchanged. New CSS uses existing tokens except one added green (`#3FB950` for the GREEN colour-key chip) — a colour-key chip must match the physical remote button, so a token colour would be wrong; `tabular-nums` follows the existing `.clock`/`.times` convention. Home, detail, player and settings screens untouched and re-rendered clean. 0 unjustified structural changes.

## 8. Miss routing (earliest layer, one per miss)

| # | Miss | Layer |
|---|---|---|
| 1 | `navigation.orientation_and_back` never demanded, so the "you lose where you were" half of the sentence produced no concept at all — everything delivered was about the grid and focus, nothing about keeping the user's place | `expected-concepts` |
| 2 | Typography reported UNKNOWN although `tokens.css` declares `--font` and a full TV type scale | `project-context` |
| 3 | Inspection assigns `platforms: ["web"]` and ignores `config.xml` (Tizen widget), `appinfo.json` (webOS), `js/keys.js` Tizen/webOS key codes and the fixed 1920×1080 body; TV is then recovered only from the sentence, and the spurious "web" requirement `interaction.keyboard_navigation` (which forced PARTIAL status) follows from it | `project-context` |
| 4 | `perf.focus_latency` demanded, candidates retrieved (`tv-focus-performance`, `tv-dpad-hold-pacing`), dropped by the bundle cap on a task whose whole subject is per-keypress scroll response | `bundle-selection` |
| 5 | Direction validates the very slot it preserves as a TV violation ("navigation 'top-bar' is a pointer/touch model") on a codebase whose top bar is d-pad reachable | `direction` |

## 9. Regressions to propose

| Query | Expectation |
|---|---|
| "In the channel guide the time header jumps every half hour and you lose where you were." | `navigation.orientation_and_back` demanded (and ideally critical). "lose where you were" is an orientation complaint; the bundle must carry a persistent-position / anchor concept, not only EPG structure. |
| Any TV-guide task phrased as scrolling or paging losing the user's place | `perf.focus_latency` survives the bundle cap when the complaint is per-keypress response; today it is demanded as recommended and dropped. |
| `inspect_project.py` on a project containing `config.xml` with a Tizen `<tizen:application>` widget, `appinfo.json`, or Tizen/webOS key codes | `platforms` includes `tv`, not `web` alone. Downstream, `interaction.keyboard_navigation` must not be demanded as a required concept for a d-pad-only app. |
| `inspect_project.py` on a project whose token file declares `--font` / `font-family` | `design_context.typography` is KNOWN with the declared stack, not UNKNOWN. |
| direction on a TV project whose top bar is reachable by d-pad | do not emit the "navigation 'top-bar' is a pointer/touch model" violation against a slot the same output preserves on repository evidence. |

## 10. Tags

`skill-helped`, `concept-miss`, `ranking-miss`, `context-detection-miss`, `direction-mismatch`, `render-defect-fixed`, `preservation-ok`, `partial-scope-ok`
