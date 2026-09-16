# Design review rubric

Use for audits, PR design reviews, and self-review before delivery. The rubric finds defects and forces explicit judgement; scores are ordinal, not measurements. Every finding needs evidence: a screenshot region, a measured ratio, an element, or a keyboard/DPAD path.

## Dimensions (score 1–4: 1 blocks the task, 2 degrades it, 3 acceptable, 4 strong)

| Dimension | Ask | Deterministic evidence available |
|---|---|---|
| task_fit | does the screen serve the user's primary job with the right layout topology and density | ledger, direction alternatives |
| information_hierarchy | one focal point, reading order, demotion of chrome | screenshot |
| usability | affordances, feedback, error recovery, learnability, consistency with platform grammar | walkthrough |
| platform_fit | input model respected (touch/pointer/keyboard/remote), platform navigation, safe areas, window/DPI, 10-foot rules | platform file checklist |
| interaction_quality | all states present, timing, focus/hover/pressed, gestures with alternatives | state enumeration |
| visual_coherence | one spacing scale, one radius language, one icon set, aligned edges | screenshot measurements |
| brand_distinctiveness | could this belong to any product; what is specific | fingerprint, anti-generic self-check |
| accessibility | contrast, names, keyboard/DPAD, focus, text scaling, reduced motion, forms | tokens.py, walkthrough |
| responsive_behavior | matrix tested, no overflow/clipping, transformations | captures per class |
| content_density | right amount visible for user and platform | density level vs. audience |
| typography | roles, floors, measure, numerals, coverage | tokens.py scale, inspection |
| color_semantics | roles not hex, states, dark theme, status never colour-only | tokens.py validate |
| performance | CLS/LCP, virtualisation, image sizing, effect cost, TV focus latency | measurements/profiler |
| implementation_consistency | reused existing components/tokens/conventions; no parallel systems | inspect_project diff |
| generic_ai_pattern_risk | count of unjustified devices from anti-generic.md | device count |

## Procedure

1. Inspect the project (or read the PR) and establish KNOWN/INFERRED/MISSING context; a review without the platform and audience is a guess.
2. Render the screens (see verification.md) across the matrix; capture evidence.
3. Walk the primary flow with the non-pointer input.
4. Run deterministic checks (`tokens.py`, automated a11y scanner if present).
5. Score each dimension; write findings as: severity (blocks/degrades/cosmetic), dimension, element, evidence, fix, effort.
6. Rank by user impact; group by cause (one spacing-scale violation causes ten symptoms).
7. Report top findings first; keep the full table in an appendix; state what was not verified.

## Finding format

```
[blocks] accessibility — Save button label #9CA3AF on #FFFFFF = 2.5:1 (needs 4.5:1); fix: use color.text.on-action token; effort: S
[degrades] platform_fit — TV detail screen: focus starts on the back arrow (should be Play); fix: focusRequester on Play; effort: S
[cosmetic] visual_coherence — card padding 18/22/16 px across three cards; fix: inset token 16; effort: S
```

Do not present subjective taste as a standard; label heuristics and aesthetic judgements as such (the knowledge records carry provenance for each rule).
