# Held-out v5 — bundle-quality reviewer brief

You judge guidance bundles you did not produce. You may read only: this file and your assigned `review/bundles-*.md` file (prompt + the guidance text with record ids stripped). You must not open anything else in the repository — not the records, lexicon, cases, thresholds, scripts, or other reviewers' files. Do not try to infer how the system works; judge only what an engineer would experience reading the guidance.

For each item answer one question: **would a competent engineer, following this guidance, materially improve the interface for this request without being distracted or misled?**

Verdicts:
- `GOOD` — materially helps; nothing misleading or off-topic dominates.
- `PARTIAL` — helps, but there is a real gap (the one thing the request is about is thin or missing) or a distracting record.
- `BAD` — misleads, contradicts the request, generic filler dominates, or the thing that mattered is absent.
- `CORRECT_ABSTAIN` — the system declined (out of scope) and it was right to.
- `WRONG_ABSTAIN` — the system declined but the request was a UI task it should have handled.
An **empty bundle** on a UI request is judged like any other bundle: GOOD only if nothing specific could reasonably be said; otherwise PARTIAL or BAD with `missing-critical`.

Every `PARTIAL` and `BAD` names exactly one primary defect:
`generic` (true in general, says nothing this request needed) · `wrong-screen` (guidance for a screen or component the request is not about) · `wrong-product` (another product family) · `missing-critical` (the one thing that mattered is absent) · `off-platform` · `contradicts-request` · `contradicts-codebase` (assumes a UI the request says does not exist) · `overlong` (far longer than its contribution) · `should-abstain` (a non-UI request answered) · `should-not-abstain`.

Output one JSON file at the path you are given: `{"reviewer": "<model family>", "verdicts": {"<id>": {"verdict": "...", "defect": "<category or empty>", "why": "<one short sentence>"}}}`. Include every id in your file. Be strict and consistent; a bundle with one excellent record and three irrelevant ones is PARTIAL (`generic` or `wrong-screen`), not GOOD.
