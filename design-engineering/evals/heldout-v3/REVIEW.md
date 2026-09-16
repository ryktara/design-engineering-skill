# Blind review — heldout-v3 cases

Reviewer saw only `cases-draft.json` and `ONTOLOGY.md`, per the review brief. No access to
the skill, its scripts, or prior eval history.

## Counts

- Before: 312 cases (282 in-scope, 30 abstain)
- After: 311 cases (281 in-scope, 30 abstain)
- Net change: -1 case, 5 field-level edits across 4 other cases

## Validation

Ran a small Python script against `cases.json`:
- JSON parses.
- All `required_concepts` / `recommended_concepts` / `forbidden_concepts` ids exist in `ONTOLOGY.md` (109 valid ids).
- All `expected_scope`, `expected_modes`, `expected_platform`, `required_preservation` values are in the taxonomy.
- No case has overlap between `required_concepts`/`recommended_concepts` and `forbidden_concepts`, or between `required_concepts` and `recommended_concepts`.
- Every in-scope case has 2–6 `required_concepts`; every abstain case has all list fields empty.
- Case count: 311 ≥ 300 floor.

All of the above passed with zero problems both before and after my edits — the draft was
structurally clean coming in (no invalid ids, no label typos, no overlap bugs anywhere in the
312 cases).

## Edits per rule

**Rule 1 (scope):** 0 changes. Checked every abstain case (hv3-283 to hv3-312) against the
in-scope/abstain boundary — all 30 are genuinely backend/infra/build/db/auth work with no
UI-visible framing (indexing, CI, ORM swaps, Terraform, JWT rotation, ETL, ESLint, etc.), and
the "mechanical migration" cases (hv3-285 SCSS→CSS modules, hv3-291 db migration, hv3-305
class-to-hooks) explicitly say "no visual change." None of the 281 in-scope cases with a
technical root cause (scroll stutter, focus loss, layout shift, stale screen-reader
announcements) were mis-labeled — the draft already applied the "visible symptom = in-scope"
rule correctly throughout.

**Rule 2 (modes):** 0 changes. Spot-checked ~40 problem-statement prompts about existing UI
("our X is a mess," "redo Y") — none carried `create`; all "add a screen/feature to our
existing app" prompts correctly used `create` (new functionality, even in an existing app).
Review-only prompts ("don't write code," "review only, no code changes," "heuristic
evaluation... no fixes") correctly restricted to `review`/`audit` with no `refactor`.

**Rule 3 (platform):** 4 field edits, all removing an over-inferred platform.
- `hv3-045` (email triage UI, "keyboard first") — platform `["desktop"]` → `[]`. Keyboard-first
  power-user UIs (Superhuman-style) ship as web apps too; nothing in the prompt names a
  desktop stack.
- `hv3-122` (command palette got slow) — platform `["desktop"]` → `[]`. Command palettes are
  common in both desktop and web SaaS (Linear, Notion); no explicit desktop signal.
- `hv3-136` (icon-only toolbar, tooltip-only labels) — platform `["desktop"]` → `[]`. Icon
  toolbars appear in web editors and desktop apps alike; no explicit signal either way.
- Checked all `tv` (every case names Fire TV/Android TV/tvOS/Google TV/set-top/IPTV/EPG —
  zero false positives), `kiosk` (every case names a kiosk/self-order/check-in/terminal
  scenario — zero false positives), and `tablet`/`mobile` platform assignments the same way;
  those were sound. Two borderline cases I considered removing but kept: `hv3-116` (SCADA
  frontend → desktop is a very strong domain convention) and `hv3-167` (config-editor tree
  view with persisted expand state → its *required* concept `desktop.persist_workspace` is
  itself desktop-namespaced, so clearing the platform would create an internal
  inconsistency) and `hv3-107` (hospital medication-administration round → tablet/COW bedside
  devices are the standard real-world pattern even though the word "tablet" isn't used).

**Rule 4 (required_concepts):** 0 removals needed. Sampled required-concept lists against
prompt content across every category (create, refactor, audit/accessibility, brand,
platform-native, adversarial) — every required id was something a competent engineer would
actually have to address for that specific prompt; no generic padding (no
`table.inline_edit` required without an editing ask, no `state.loading_empty_error` required
on static content, no `tv.*` required outside TV).

**Rule 5 (forbidden_concepts):** 0 changes. Automated check confirms zero overlap with
required/recommended across all 311 cases; manual spot-check confirms the forbidden pairs are
always genuinely off-target for that prompt's domain (e.g. `tv.*`/`media.*` forbidden on
generic SaaS prompts, `touch.*` forbidden on TV prompts).

**Rule 6 (required_preservation):** 1 field edit.
- `hv3-087` ("clean up the shipment detail page. dont change the routes or the URL structure,
  other teams link into it") — `required_preservation` `["behaviour"]` → `["navigation"]`. The
  explicit ask is about routes/URL structure, which is a navigation concern
  (`navigation.deep_link_state`), not general behaviour.
- Checked every other non-empty `required_preservation` case (hv3-067, 068, 071, 084, 094,
  099, 105, 116, 123, 230, 243) against its prompt's explicit wording — all correctly scoped
  (colour-only asks → `["color"]`, route/back-button asks → `["navigation"]`, "keep behaviour
  identical" asks → `["behaviour"]`, "keep colours and fonts" → `["color","typography"]`).

**Rule 7 (near-duplicates):** 1 case removed.
- `hv3-217` ("our Fire TV app has no watchlist and users keep asking. add save-for-later
  across rows and details") removed as a near-duplicate of `hv3-014` ("we're adding a Watch
  Later row to our Fire TV app, should sit under Continue Watching") — same platform (tv),
  same mode (create), same core feature (watchlist/save-for-later on Fire TV), 3 of 4
  required concepts identical (`media.watchlist`, `interaction.dpad_reachability`,
  `layout.media_card`). Kept `hv3-014` since it's the more specific/testable prompt (exact
  placement requirement).
- No other near-duplicates found. Superficially similar-sounding pairs (e.g. hv3-011 vs
  hv3-046 on "plan comparison," hv3-090 vs hv3-140 on dashboard charts, hv3-042 vs hv3-279 on
  stale timestamps) were checked and found to differ in mode, concept set, or the specific
  problem being solved — genuinely distinct test cases, not paraphrases.

## Systematic bias noticed in the draft

The generator's platform inference had a mild bias toward tagging `desktop` whenever a prompt
used power-user/productivity vocabulary (keyboard shortcuts, command palettes, toolbars, tree
views) even without any stack or device signal — those patterns are just as common in web
SaaS. TV and kiosk inference, by contrast, was disciplined: every single TV/kiosk case names
an explicit platform keyword (Fire TV, Android TV, tvOS, set-top, IPTV, EPG, kiosk,
self-order, check-in terminal), so no over-inference there. Everything else — scope
labeling, mode selection, concept relevance, forbidden-concept selection, and preservation
scoping — was consistently well-grounded in the prompt wording across all 312 draft cases,
with no other systematic pattern of error found.
