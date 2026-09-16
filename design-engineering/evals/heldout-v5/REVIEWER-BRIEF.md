# Held-out v5 — expectation reviewer brief

You set the **expectations** for prompts you did not write. You may read only: this file, `ONTOLOGY.md` in this folder (concept ids + labels), the "Case format" and "Per-case scoring" sections of `THRESHOLDS.md`, and your assigned `gen/prompts-*.json`. You must not open anything else in the repository (no scripts, data, development cases, earlier held-out sets, docs). Judge each prompt as a senior UI engineer would from the sentence alone.

For every prompt produce one case:

```json
{"id": "<same id>", "prompt": "<verbatim>", "category": "<same>", "stress": "<same>",
 "scope": "in-scope | partial | abstain",
 "artifact_state": "new | existing | unknown",
 "acceptable_modes": ["create | refactor | polish | audit | review | accessibility | responsive | brand | design-system | reconstruct"],
 "platform": {"required": ["web|mobile|tablet|desktop|tv|kiosk"], "acceptable_inferred": [], "expect_unknown": false},
 "required_concepts": ["2-7 ontology ids that a competent engineer must address"],
 "critical_concepts": ["1-3 of those; guidance that misses one is BAD"],
 "recommended_concepts": ["0-4 nice-to-have ids"],
 "forbidden_concepts": ["0-4 ids that would be wrong or distracting for THIS prompt"],
 "preservation": ["navigation | typography | color | behaviour"],
 "acceptable_alternatives": {"<required id>": ["ids that count as equivalent"]}}
```

Rules:
- `scope`: `abstain` for backend / data / infrastructure / build tooling / pure runtime questions with no user-visible UI consequence; `partial` when a UI task is wrapped in technical work; else `in-scope`. Abstain cases need no concepts or platform.
- `platform.required`: only when the sentence itself makes the platform clear (a name, an exclusive device, a stack that implies one, a strong situational idiom such as "from the sofa with the remote"). Put weaker but reasonable inferences in `acceptable_inferred`. Set `expect_unknown: true` when a careful engineer would have to ask ("a large display", "the office dashboard", "phones and laptops" ⇒ web is acceptable_inferred, not required). Never require `tablet` alone.
- `acceptable_modes`: usually two; observations about existing UI accept `audit` and `refactor` (and `polish` for cosmetic ones, `accessibility` for a11y ones); requests for something new accept `create`.
- `critical_concepts`: the one to three things the request is *about*. For a narrow one-element task (stress `generic-guardrail`) list only that element's concept(s) and put general baselines (contrast, states, keyboard) into `forbidden_concepts` only if they would clearly be filler for that request — otherwise leave them out entirely.
- `forbidden_concepts` for `wrong-screen` prompts: the concept(s) the misleading word would pull in (e.g. `navigation.tabs`-like ids when "tab" is the key; chart ids when "compare two files"; player ids when "overlay" is a cookie overlay). Use only ids from the ontology.
- Be strict and literal; do not invent requirements the sentence does not support. Use ids exactly as written in `ONTOLOGY.md`.

Output one JSON file `{"reviewer": "<model family>", "cases": [...]}` at the path you are given. Include every prompt; do not drop or edit prompts.
