# Held-out v2 — pre-registered acceptance thresholds

Written 2026-09-09 **before** any v2 case existed and before the run. These numbers are not changed after the run; if the run misses them, the miss is reported.

## Case format (structured expectations)

```json
{"id": "hv2-001", "query": "...", "category": "...",
 "expect": {"platforms": [], "modes": [], "inputs": [], "screens": [], "negatives": [], "missing": [],
            "required_concerns": [], "recommended_concerns": [], "forbidden_concerns": [],
            "concepts": ["free-form phrases"], "offtarget": ["free-form phrases"]},
 "expect_abstain": false}
```

Concern names come from the public taxonomy (structure, navigation, component, interaction, accessibility, content, data-display, adaptive, states, feedback, performance, privacy, environment, brand, motion, anti-pattern). The generator and reviewer see only the taxonomy labels and the DesignRequirements field values, never records, lexicon, or existing cases.

## Per-case acceptability (guidance bundle, `advise.py guidance` path)

A non-abstain case is **acceptable** when all hold:

1. platforms expected ⊆ platforms detected; no extra platform beyond tablet;
2. at least one expected mode is in the top two detected modes;
3. expected inputs ⊆ detected inputs; expected negatives ⊆ detected negatives;
4. every `required_concerns` entry is covered by at least one bundle record's concerns;
5. no bundle record carries a `forbidden_concerns` entry as its *only* concerns (a record that also serves a required concern is not a violation);
6. concept-phrase recall (token-level match against bundle text) ≥ 0.50;
7. off-target phrase rate ≤ 0.34;
8. bundle non-empty.

An abstain case is correct when status is ABSTAIN or AMBIGUOUS or activation is `skip`.

## Set-level thresholds (pass/fail reported, never tuned to)

| Metric | Threshold |
|---|---|
| acceptable cases | ≥ 40% |
| mean concept recall | ≥ 0.40 |
| required-concern coverage (mean ratio) | ≥ 0.85 |
| mean off-target rate | ≤ 0.20 |
| abstain correct | ≥ 80% of abstain cases |
| platform correct | ≥ 85% |
| mode correct | ≥ 75% |
| empty bundles | ≤ 2% |

Rationale: Phase 2 held-out v1 measured 10/145 acceptable and recall 0.184 with the old search path. The thresholds above are the minimum at which the guidance bundle can be called a *material* generalisation improvement rather than noise; they are deliberately not ambitious enough to be met by tuning to the development set alone.
