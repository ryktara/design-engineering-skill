# Multi-brand differentiation

Several brands on one application or backend must be *structurally* different, not skins. Changing logo, primary colour, and font is a theme, not a brand system. This file defines the workflow and the deterministic check.

## Contents
- What can vary between brands
- Workflow
- Fingerprints and the similarity check
- Implementing brands on one codebase
- Verdicts and what to do

## What can vary between brands

Structural axes (heavily weighted): navigation model, layout topology, content density, grid behaviour, card geometry, surface strategy, image strategy, metadata density, CTA strategy.
Cosmetic axes (lightly weighted): corner language, typography character, colour strategy, icon strategy, motion character, focus strategy.

Other levers: page composition and section architecture, content grouping, hierarchy order, spacing rhythm, iconography language, image treatment (crop, scrim, grain), focus behaviour on TV, background treatment, animation vocabulary, metadata treatment, content discovery model (rails vs. grid vs. search-first), copy voice.

## Workflow

1. For each brand, gather its own signals: audience, tone, content type, artwork quality, primary tasks, platforms, and any existing brand assets. These are KNOWN inputs; do not invent them.
2. Run a direction per brand, feeding the brand-specific signals:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/advise.py" direction "<brand A description + product + platform>" --brand "A" --out brand-a.json
   python "${CLAUDE_SKILL_DIR}/scripts/advise.py" direction "<brand B description + product + platform>" --brand "B" --out brand-b.json
   ```
   If the descriptions are near-identical, the directions will be too; that is the signal to go back and find what actually differs between the brands (or to accept that they are one product with a skin and say so).
3. Adjust the fingerprints by hand where the direction should differ (edit the JSON); every axis value must come from the allowed lists (`fingerprint.py init` prints them).
4. Compare:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/fingerprint.py" compare brand-a.json brand-b.json [brand-c.json …]
   ```
   COSMETIC-ONLY or NEAR-DUPLICATE fails the check. Change at least two structural axes for the failing pair (navigation model, layout topology, density, surface, imagery, metadata, CTA) and compare again.
5. Implement each brand as a configuration of the shared component system (below), then verify each brand visually side by side on the same screens.

## Fingerprints and the similarity check

A fingerprint is 15 enumerated axes. Similarity is the weighted fraction of equal axes, computed separately for structural and cosmetic groups. Threshold 0.7 on structural similarity marks "the same layout architecture". The check is deterministic and explainable: the report lists the shared structural axes. It does not read pixels; the fingerprint comes from the direction tool, from your inspection of a screen or screenshot, or from hand entry. When describing an existing screen, fill the fingerprint from what you observe (navigation, topology, density, cards, imagery, metadata, CTA) before comparing.

## Implementing brands on one codebase

- Tokens: one semantic token schema; each brand supplies its own values (light and dark). Validate every brand with `tokens.py validate`.
- Structure: brand configuration selects navigation model, layout variants, card geometry, metadata density, and CTA placement through composition (different screen compositions or layout components), not through CSS overrides of one layout.
- Components: shared primitives with variant props (density, geometry, emphasis); brand-specific components only where structure differs (e.g. immersive hero vs. broadcast guide on TV).
- Assets: fonts, icon sets, illustration style, image treatment per brand, loaded per brand.
- Content model: discovery (rails, grid, search-first), metadata shown, copy voice per brand.
- Guardrails: shared accessibility, focus, and platform rules are not brand-configurable.

## Verdicts and what to do

| Verdict | Meaning | Action |
|---|---|---|
| DISTINCT | structural similarity below threshold | proceed; still check cosmetic coherence per brand |
| COSMETIC-ONLY | same architecture, different paint | change ≥2 structural axes for that pair, or declare the brands as one product with a skin |
| NEAR-DUPLICATE | practically identical | one of the brands has no identity yet; gather its signals |

Report the comparison table and the axes changed. Keep `brand-*.json` files in the project's design folder if the team wants to maintain them; otherwise delete after the check.
