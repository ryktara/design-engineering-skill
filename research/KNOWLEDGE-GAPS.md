# Knowledge gaps (from the frozen held-out run, 2026-09-08)

Source: `evals/heldout/cases.json` (145 independent cases) scored in `research/runs/heldout-run2-release-token-matching.json`. For every expected concept the analysis asked: does *any* record in the knowledge base contain the concept's tokens? If yes and it was not retrieved, it is a **ranking miss**; if no record contains it, it is a **knowledge gap**. Records are added only for repeated or important gaps; nothing was added during Phase 2 (the held-out set is frozen and was not tuned against).

## Headline

| Class | Concept misses |
|---|---|
| ranking miss (concept exists, not in top 5) | 478 |
| knowledge gap (concept absent from all records) | 192 |
| concept hits | 148 |

Ranking misses dominate. The single largest cause is that universal interaction/accessibility rules are not a *required facet* for create-mode requests on touch platforms (the interaction facet is required only when an input is stated or the platform is TV/desktop/kiosk), so "large touch targets" (11 misses), "tabular figures" (8), "high contrast" (5), "keyboard navigation" (5), "focus order" (4) are present in the base but not surfaced for mobile/web create requests. This is a follow-up for Phase 3 (change the facet policy, add a regression case first), not a data problem.

## Proposed records (repeated or important gaps only)

| Missing concept | Failing case ids | Why existing references cannot cover it | Proposed record kind |
|---|---|---|---|
| 10-foot typography as a named concept | 5 held-out TV cases (ho-0xx tvos/android-tv) | `tv-typography-distance` exists but uses "TV: 10-foot typography" only in the title; the guidance text says "distance". Not a new record: add "10-foot typography", "10 foot" to its keywords (lexical hook), after a regression case. | keyword addition to existing rule |
| Glanceable status / at-a-glance state for field, courier and utility apps | ho-005, ho-008, +1 | No rule about glanceability (large state, colour+icon+text, minimal reading) for outdoor/field use. | rule: `mobile-glanceable-status` (platform mobile/tablet, input touch) |
| Column priority for responsive tables (which columns survive on phones) | 3 cases (tables/responsive) | `mobile-density-touch` says "2–3 deciding columns" but has no keyword hooks for "column priority"/"hide columns"; still a rule rather than a gap: extend keywords. | keyword addition |
| Outdoor high-contrast / sunlight readability | ho-001, ho-008 | Contrast rule is WCAG-only; no environmental (glare, sunlight, gloves) guidance for field and outdoor apps. Kiosk file covers glare for kiosks only. | rule: `mobile-outdoor-readability` |
| Pinned channel column in EPG | 2 cases | `layout-epg-grid` guidance says "sticky channel column" — vocabulary mismatch ("pinned"). | keyword addition |
| Player auto-hide timing | 2 cases (tvos) | `tv-player-controls` covers auto-hide 3–5 s; concept phrase "auto hide timing" did not token-match "auto-hides". Tokeniser treats "auto-hides" as one token. | keyword addition ("auto hide", "auto-hide timing") |
| Activation code / QR sign-in / companion device for TV | 2 cases | `platforms/tv.md` mentions code-on-screen sign-in, but no record exists; TV sign-in is a common screen. | component: `comp-tv-sign-in` |
| Privacy of on-screen data on shared devices (TV, kiosk) | 2 cases | Kiosk rule covers session clearing; TV has nothing about shared-household privacy (profile PINs, hiding balances). | rule: `shared-device-privacy` |
| Offline-first, sync status, progress saved locally | ho-005, ho-008, +1 | No offline/connectivity state guidance anywhere; `layout-states-empty-loading-error` covers loading/error only. | rule: `states-offline-and-sync` |
| Dismissable upsell / promo banners | 2 cases | Anti-pattern set has no entry for interruptive promos; `comp-toast-notification` is about status. | antipattern: `anti-interruptive-upsell` |
| Progress checklist / setup checklist (onboarding) | 2 cases | `comp-wizard-stepper` is linear; a persistent checklist for multi-session setup is a different component. | component: `comp-setup-checklist` |

Single-occurrence gaps (address search, print stylesheet, low bandwidth, photo upload, semantic table markup, progressive enhancement, session timeout warning, QR sign-in, resource dictionary, SettingsCard/expander groups, abnormal-value highlight) are recorded here but not proposed: one independent case each; several are content-specific rather than design knowledge.

## By category (concept hits / ranking misses / knowledge gaps)

winui 1/21/2, settings 1/20/3, flutter 2/19/3, negative-constraint 3/19/2, mobile 2/17/5, brand 3/17/4, accessibility 6/16/2, avalonia 5/16/3, compose 5/16/3, polish 5/16/3, android-tv 6/15/2, finance 4/15/5, saas 3/15/6, swiftui 4/15/5, tvos 5/14/5, erp 3/14/7, media 7/14/3, onboarding 2/14/8, screenshot 2/14/8, forms 5/13/6, nextjs 5/13/6, tables 5/13/6, wpf 4/13/7, dashboards 6/12/6, healthcare 6/11/7, search 9/11/4, react 9/10/5, kiosk 10/10/4, web 2/10/12, responsive 5/9/10, ecommerce 7/9/8, adversarial 10/37/32.

Reading: desktop-native categories (winui, wpf, avalonia) and settings miss on ranking, not knowledge; web/responsive/onboarding/screenshot carry the most genuine gaps.

## Process

Each proposed addition requires: (1) a regression or development case that fails today, (2) the record with provenance and keywords, (3) `validate_skill.py` clean, (4) development + regression green. The held-out set stays frozen; a future held-out set (v2) would measure whether the additions generalise.
