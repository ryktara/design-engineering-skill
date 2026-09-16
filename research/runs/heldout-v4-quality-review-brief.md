# Held-out v4 bundle-quality review (BLIND)

You judge the guidance a design tool produced for developer prompts. You see only the prompt and the guidance text (titles + guidance sentences, with their role core/guardrail) plus the tool's status line. You do NOT see the tool, its expectations, or any scoring. Do not open anything under `design-engineering/` and do not read other eval files.

For each bundle give exactly one verdict:

- `GOOD` — a competent designer would accept this as the right guidance for that prompt: the core records address the actual task, guardrails are relevant, nothing would send the implementer in a wrong direction.
- `PARTIAL` — useful but incomplete or diluted: the key point is there but padded with off-task records, or one important thing is missing.
- `BAD` — misleading or useless for the prompt: wrong platform or wrong kind of screen, mostly generic filler, contradicts what the prompt asks, or misses the one thing the prompt is about.
- `CORRECT_ABSTAIN` — the tool abstained (status ABSTAIN / OUT_OF_SCOPE note) and the prompt was indeed not a UI design task.
- `WRONG_ABSTAIN` — the tool abstained but the prompt was a UI design task.

For every `BAD` and `WRONG_ABSTAIN` add one defect category: `off-platform`, `wrong-screen`, `generic`, `missing-critical`, `contradicts-request`, `wrong-mode`, `should-abstain`, `should-not-abstain`. For `PARTIAL`, add the category of the main weakness when obvious.

Be strict and consistent. A bundle whose first core record is about a different product type (a checkout on a habit tracker, a TV rail on a desktop form) is BAD even if the guardrails are fine. A bundle that is generic accessibility boilerplate with nothing about the prompt's subject is BAD (`generic`). A bundle that nails the subject but also carries two irrelevant guardrails is PARTIAL.

Output file: `heldout-v4-quality-review-part<N>.json` in this folder: `{"part": N, "reviewer_model": "...", "verdicts": {"<id>": "GOOD|PARTIAL|BAD|CORRECT_ABSTAIN|WRONG_ABSTAIN"}, "defects": {"<id>": "<category>"}}`. Every id in the part must have a verdict. Then report counts per verdict and the top three defect categories.
