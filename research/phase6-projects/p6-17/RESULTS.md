# p6-17 — "In dark mode the transaction dates are barely visible."

- **Project / stack / platform:** `p6-compose-banking` (NorthBank) · Kotlin + Jetpack Compose + Material3 · mobile
- **Artifact state:** existing UI (account detail screen already implemented)
- **Build hash:** start `ea8eed72…5d9947`, end `ea8eed72…5d9947` — **equal**, frozen build c3 unchanged.
- **Render mode:** `html-twin` at 390×844, `colorScheme: dark`, DPR 2 (no gradle build available). Twin created at `project/render/twin.html` (new file — nothing to copy to `before/`).
- **Concurrency rule honoured:** only `ui/theme/Color.kt` and `ui/theme/Theme.kt` were edited. `AccountDetailScreen.kt` was read but needed no change; transfer and cards screens untouched.

## Reviewer root cause (pre-registered, from the code, before any advise command)

`DarkColors.onSurfaceVariant = Grey600` (#6B6B6B) on `background`/`surface` = `Grey900` (#121212) → **3.55:1**, below WCAG AA 4.5:1 for body text. `AccountDetailScreen.TransactionRow` renders the date line as `bodySmall` (12 sp) in `onSurfaceVariant`, so the defect is dark-mode-only — light mode uses `Grey700` on white (~9:1). Correct fix is one semantic token, not a screen-level colour override.

## 1. Design-context table (`01-inspect.json`)

| Field | Detected | Status | Actual | Correct? |
|---|---|---|---|---|
| navigation | top-bar | KNOWN | Material3 `NavigationBar` shell (`BottomBar.kt`) + a per-screen `TopAppBar`; bottom-tabs scored 5 but lost to top-bar's 30 | partial |
| theme | dual-theme, default light | KNOWN | `lightColorScheme` + `darkColorScheme`, `isSystemInDarkTheme()`, dynamicColor off | yes |
| surfaces | bordered-flat | INFERRED | `NbCard` = `OutlinedCard`, 1.dp border, no elevation | yes |
| radius | small ("most common 4") | INFERRED | `CardCornerRadius = 12.dp` is documented as "every `Nb*` surface"; 4 only exists as `Shapes.extraSmall` | no |
| spacing | unknown | UNKNOWN | `Spacing.kt` is an explicit 4-pt grid (xs 4 … xxl 32, `screen = 16`) with a doc comment | no (clear in code) |
| typography | custom | KNOWN | full `Typography` scale in `Type.kt`, tabular figures detected correctly | yes |
| components | compose, material3 | KNOWN | correct | yes |
| tokens | `[]` | — | `Color.kt` (primitives) + `Theme.kt` (semantic roles) is a textbook two-layer token system | no |

The last row is the expensive one: on a task whose correct fix *is* a semantic token, the inspector reported the project as having no tokens.

## 2. Requirements verdict (`02-requirements.json`)

| Field | Value | Verdict |
|---|---|---|
| platform / `platform_evidence` | `mobile` (from project inspection; `platform_evidence: []`) | correct — no MISSING needed, project evidence was decisive |
| `intent.artifact_state` | existing | correct |
| `intent.operations` | diagnose, modify | correct |
| `intent.problem_domain` | accessibility, visual, design-system | correct, including design-system from "dark mode" |
| `intent.change_scope` | unknown (`intent.scope: moderate`) | acceptable — the sentence gives no scope word |
| mode / `mode_evidence` | `[accessibility, audit]`, "accessibility defect on existing UI" / "diagnose the reported defect" | correct, within my acceptable set |
| `scope.kind` / reason | in-scope, "UI design / interaction task" | correct |
| `change_budget` | low | correct |
| `intent.preserve` | `[]` | acceptable — `constraints.preserve_existing_system: true` carries it |
| `project_context` | as inspected | inherits the radius/spacing/token errors above |

`activation.decision` is `ambiguous` (ui_score 1.0, non_ui 0) yet `status: CONFIDENT` and scope in-scope — no practical harm here, but "barely visible" is only picked up as a ux_symptom, not as a UI term.

## 3. Guidance verdict (`03-guidance.md` / `.json`)

`status=PARTIAL`, exit code 3. Bundle = **0 core + 1 guardrail + 0 optional**.

| Record | Layer | Verdict | Category |
|---|---|---|---|
| `a11y-nontext-contrast` — "Non-text contrast 3:1 for controls and focus" | CRITICAL GUARDRAIL | partial | `generic` |
| *(bundle as a whole)* | — | — | `missing-critical` (`brand.token_layers`) |

Why `partial / generic`: the task is a **text** contrast failure. The record is explicitly about non-text contrast — "≥3:1 against adjacent colours" for controls, borders, focus rings — and it goes out of its way to say hairline dividers at 1.2:1 are acceptable. It never names 4.5:1. Implemented literally (3:1) it would have accepted a colour that still fails AA. `a11y-contrast-text` exists in `data/rules.jsonl`, carries the same `a11y.contrast` concept, was a candidate at **0.243**, and lost to `a11y-nontext-contrast` at **0.251** — the latter also carries `interaction.focus_visible`, so it presumably won on marginal concept gain rather than on fit.

`layer_review`: core `[]`, critical `[a11y-nontext-contrast]`, optional `[]` (`optional_useful` 0, `optional_noise` 0). No off-target or harmful record; the failure mode here is emptiness plus one near-miss carrier, not noise.

### Concept recall

delivered = union of `concepts` over selected records = `{a11y.contrast, interaction.focus_visible}`.

| Expected id | Critical | Delivered? | Layer if missing |
|---|---|---|---|
| `a11y.contrast` | yes | yes (wrong carrier) | — (carrier chosen at `bundle-selection`) |
| `brand.token_layers` | yes | no | `expected-concepts` |
| `brand.dark_mode_redesign` | no | no | `expected-concepts` |
| `layout.focal_hierarchy` | no | no | `expected-concepts` |
| `process.safe_modification` | no | no | `expected-concepts` |

**concept recall 1/5 = 0.20 · critical recall 1/2 = 0.50.**

None of the three missing design concepts is a knowledge gap. `search "<sentence>" -k 12` ranks, in order: `anti-dark-mode-inversion` (0.483), `color-dark-mode-rules` (0.465 — "text 87/60/38% white steps for primary/secondary/disabled; re-validate every contrast pair", i.e. literally the fix I implemented), `color-semantic-tokens` (0.364 — "every theme redefines only the semantic layer", i.e. literally where I implemented it). All three are `platform: any`, none was rejected on platform, and none appears in `omitted` or `rejected` — they were never demanded, because no expected-concept step asked for `brand.dark_mode_redesign` or `brand.token_layers` despite "dark mode" being in the sentence and `theme=dual-theme` being KNOWN in the project context. The knowledge is present and the retriever finds it; the demand layer does not ask for it.

`concerns`: required `[accessibility, interaction, component, data-display]`, uncovered `[component, data-display]` — coverage 0.5. `data-display` is arguably right to want here (a transaction list), but nothing covered it.

## 4. Direction verdict (`04-direction.md` / `.json`)

All 13 slots `preserved`, 0 `changed`, 0 `new`. **`unjustified_direction_slots` = 0** — correct for an existing UI at a low budget. `preservation` messaging and `validation: OK` are right. The one guardrail repeated in the direction is the same non-text-contrast record, and the `color` slot's prose ("neutral scale with a slight brand tint, one accent ≤10%…") is generic palette advice that neither helps nor conflicts with the task. The direction is correct and empty: it told me to change nothing, which is true of every slot except the one token the task is actually about, and it has no slot for that.

## 5. Implementation

Files changed (both copied to `before/` first):

- `app/src/main/java/com/northbank/app/ui/theme/Color.kt` — added `val Grey400 = Color(0xFFA6A6A6)` to the existing neutral ramp (slot between Grey300 and Grey500 kept in order).
- `app/src/main/java/com/northbank/app/ui/theme/Theme.kt` — `DarkColors.onSurfaceVariant`: `Grey600` → `Grey400`, with a comment recording both ratios. `LightColors` untouched.

New file: `project/render/twin.html` (HTML twin of the account detail screen; tokens/type/spacing mirror `Color.kt`/`Theme.kt`/`Type.kt`/`Spacing.kt`; `?variant=before` restores Grey600).

`AccountDetailScreen.kt` was deliberately **not** changed: the date line already uses the semantic `onSurfaceVariant` role correctly, so a per-screen colour would have been the wrong fix. `#A6A6A6` was chosen over `Grey500` (#8A8A8A, 6.1:1) because it matches the ~60%-white secondary step and leaves margin at 12 sp; it stays clearly secondary against `onSurface` = `Grey100` (17.4:1).

Measured in the twin: **3.52:1 → 7.70:1** at 12 px (Playwright-computed, plus a Pillow pixel check confirming the glyph colour moved 107 → 166).

- **Guidance used:** none.
- **Guidance ignored:** `a11y-nontext-contrast` — its 3:1 bar is for controls, not for this 12 sp text; applying it as stated would have under-fixed the defect.

### Process guidance check

`process_records_needed`: **false**. SKILL.md §2 (inspect before deciding) and §7 (verify by rendering) were enough; `impl-reuse-before-new` / `impl-safe-modification` / `verify-render-and-inspect` would have added tokens without changing what I did. The gap in this bundle was domain guidance (dark-mode token rules), not process guidance.

## 6. Render and defects

Screenshots looked at: `render/before-dark-390x844.png`, `render/first-dark-390x844.png` (= `final-dark-390x844.png`), plus 4× crops `crop-before.png` / `final-crop-dark.png`.

- **Before** render reproduces the report: the date/reference line sits at #6B6B6B on #121212 and is visibly the weakest text on the screen.
- **First render defects:** visual 0, interaction 0, accessibility 0, platform 0, existing-system-mismatch 0, implementation-bug 0. **Iterations: 1.** The fix was diagnosed from the code before rendering, so the first render was already correct; I verified it numerically rather than trusting the eye, because at 12 sp the 107→166 change is subtler in a downscaled screenshot than the ratio suggests.
- **Final defects:** all 0.
- No defect the guidance warned about was shipped.

**Adjacent defect found during render inspection, not fixed (out of the task sentence):** credit amounts use `PositiveGreen` #1B8A4C, which is **4.31:1** on the dark canvas at `bodyLarge` 16 sp — also below AA. It is not "the transaction dates", it would require a change that affects light mode too (where it passes at 4.9:1), and the budget is low, so I left it and record it here.

## 7. Preservation

Navigation, layout, density, typography, component set, spacing and both screens' structure are untouched; the only change is one semantic role in the dark scheme plus the primitive it points at. Light mode is byte-identical in behaviour. `preservation-ok`.

## 8. Miss routing (earliest layer, one per miss)

1. **`bundle-selection`** — `a11y.contrast` covered by `a11y-nontext-contrast` rather than `a11y-contrast-text`; both were compatible candidates, the wrong one won by 0.008, plausibly on the extra concept it carries.
2. **`expected-concepts`** — `brand.dark_mode_redesign` and `brand.token_layers` never demanded, despite "dark mode" in the sentence and `theme=dual-theme` KNOWN; the records exist and rank #1–#3 in `search`.
3. **`project-context`** — `tokens: []`, `spacing: UNKNOWN`, `radius: small`, `navigation: top-bar` on a project whose token layer, 4-pt grid, 12 dp corner language and bottom-tab shell are all explicit in named files.

## 9. Regressions to propose

1. Query: *"In dark mode the transaction dates are barely visible."* → expect `a11y.contrast` carried by `a11y-contrast-text` (4.5:1 for body text), not `a11y-nontext-contrast`; expect `brand.dark_mode_redesign` and `brand.token_layers` demanded and carried by `color-dark-mode-rules` and `color-semantic-tokens`.
2. Query: *"the secondary labels in the dark theme are too dim to read"* → expect `color-dark-mode-rules` in the bundle and a text-contrast record rather than a control/focus-contrast record.
3. Inspector: a Compose project with `Color.kt` primitives + `Theme.kt` `lightColorScheme`/`darkColorScheme` → expect `tokens` non-empty; a project whose shell is a Material3 `NavigationBar` → expect `navigation = bottom-tabs`.

## Tags

`concept-miss`, `ranking-miss`, `context-detection-miss`, `skill-neutral`, `preservation-ok`

**Skill effect: neutral.** Nothing in the bundle produced a change I made, and nothing in it produced a change I had to revert. The one record shipped is adjacent-but-wrong for a text-contrast task; the diagnosis, the token-layer decision and the chosen value all came from reading `Theme.kt` and from WCAG, not from the skill. The skill did get scope, platform, mode, budget and direction right — it simply had nothing to say about the thing the sentence was about.
