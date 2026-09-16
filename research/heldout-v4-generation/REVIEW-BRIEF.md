# Held-out v4 expectation review (BLIND, independent of the generator)

You are the expectation reviewer. You have NOT seen the tool under test and must not look for it: do not open anything under `design-engineering/`, and do not read other eval sets. Your inputs: `BRIEF.md` (the generator's brief — read it for the rules), `ONTOLOGY.md` (the only valid concept ids), and one `review-chunk-<n>.json`.

For every case decide whether the expectation is what a careful, fair design reviewer would demand of a good answer to that exact prompt. Fix what is wrong; leave what is right. Typical problems to look for:

- **Over-demanding platform**: `platform.required` set from a weak hint (a single word like "app", "screen", "users") — move it to `acceptable_inferred` or empty it. A prompt whose platform a reasonable reader would have to ask about must not require one.
- **Under-demanding platform**: the prompt unambiguously implies a platform (remote control, ten-foot, gloves at a checkout lane, menu bar + accelerators, home indicator) but `required` is empty — set it.
- **Wrong artifact_state**: prompts describing how a screen currently behaves are `existing`; greenfield or a new screen are `new`; `unknown` only if genuinely unclear.
- **acceptable_modes too narrow**: list every mode a fair reviewer would accept as the primary (a defect observation usually accepts `audit` and `refactor`, or `polish` for purely visual defects; accessibility symptoms accept `accessibility` and `audit`; viewport symptoms accept `responsive` and `refactor`; a new screen accepts `create`, and `refactor` when it must fit an existing app).
- **Concepts**: `required_concepts` must be things a good answer MUST cover (3–7, ids from ONTOLOGY.md only); `critical_concepts` (1–3) are the ones whose absence makes the answer BAD; `forbidden_concepts` must be clearly wrong for the prompt (not merely irrelevant). Remove padding, add glaring omissions, fix ids that do not exist in ONTOLOGY.md (one known bad id: `kiosk.env`).
- **Scope**: `abstain` only for prompts that are not design tasks at all; `partial` when a technical cause has a user-visible UX symptom; everything else `in-scope`.
- **Preservation**: only when the prompt states or clearly implies what must stay.
- **Wording flags**: check `wording.explicit_mode_verb` and `wording.canonical_platform_name` against the prompt text and correct them.
- **Duplicates / template reuse**: if two prompts are near-identical, rewrite one so it is a different situation (keep the id).

Do not soften cases to make them easy and do not make them impossible; the standard is "what a good answer must contain".

## Output

Write `reviewed-chunk-<n>.json`: `{"chunk": <n>, "reviewer_model": "<your model>", "cases": [ ...all cases, corrected... ], "changes": [{"id": "...", "field": "...", "from": ..., "to": ..., "reason": "..."}]}`. Keep every case (never drop one). Then report: number of cases changed, the most common kinds of corrections, and anything systematic you noticed about the generator.
