# Lexicon gaps (observed, 2026-09-08)

Vocabulary the deterministic classifier failed to recognise, taken only from observed failures (development runs, the independent activation set, the frozen held-out run). Synonyms are not added speculatively.

## Added in Phase 2 (each with a regression or development case)

| Phrase(s) | Label | Evidence | Case |
|---|---|---|---|
| refresh the look / refresh the visual / visual style / restyle / facelift / visual refresh / freshen up / modern look | mode polish | dev `req-keep-navigation` classified as create | `regression/requirements: reg-polish-vocabulary` |
| epg / programme guide / program guide / channel guide | screen list | dev `req-tv-epg-compose` | `reg-epg-is-list-screen` |
| site / web page / webpage / web site / homepage / microsite / intranet | platform web | held-out run 1 ho-002 ("council site") had no platform and retrieved a TV anti-pattern | `reg-site-is-web` |
| framework-runtime vocabulary: redirect loop, not updating, build fails, duplicate class, gradle, canexecute, re-evaluate, shard(ing), soft-delete, purge(d), production build, remote domain, not configured, throws, exception, api caching, revalidate, @state, @published, background thread, doesn't/does not/not re-render(ing), postgres, the query, orders/users table, add a column, migrate the, hot reload, hmr, webpack, vite, bundler, tree shaking, source map, wrong values after, data update, stale data, cache invalidation | non-UI vocabulary (activation proxy) | activation run 1: 13 false positives, all framework-runtime prompts mentioning UI technologies | `regression/activation` (7 cases) |
| progress indicator / stepper / step indicator / how far along / readability / line length / legend | UI vocabulary (activation proxy) | activation run 1 false negatives act-059, act-042, act-168 | `reg-act-kiosk-progress-positive` |
| stack words removed from platform lists (react, compose, winui, swiftui …) | correction | "Build an Android TV EPG in Compose" produced platform mobile KNOWN and an AMBIGUOUS status | `reg-stack-word-not-platform`, `reg-react-implies-web-only-inferred` |

Note on independence: the activation set was used as the evidence for the non-UI vocabulary above, so activation proxy numbers after that change (0.987 precision) are no longer a blind measurement; run 1 (0.849) is the blind number. The held-out set was not tuned against beyond the single "site" defect, which was fixed through a regression case; both held-out runs are archived in `research/runs/`.

## Observed but NOT added (recorded for Phase 3, needs its own cases)

Mode detection defaults to `create` when the request states a *problem* rather than a verb. Held-out run: 47 mode misses, almost all of this shape:

- "customers keep missing where to …", "users don't know how far along", "gets lost among", "selection state is confusing", "numbers misalign", "feels off", "disappear too fast", "loses focus when you come back", "looks different on every screen", "layout shifts", "errors only on submit", "users are confused by" → expected refactor/polish/audit.
- Proposed rule for the lexicon: a `problem_statement` phrase group ("keep missing", "don't know", "gets lost", "confusing", "misalign", "feels off", "too fast", "loses focus", "look different", "shifts", "hard to", "can't find") that maps to `polish`+`audit` as secondary modes and demotes the `create` default. Requires development cases first.

Platform inference the generator expected but the system deliberately does not make: "SaaS", "admin", "checkout page", "booking site", "email template" → web (24 misses). The current policy (do not infer web from product words; see `req-audit-checkout`) was kept because it prevents silent assumptions; a middle ground (web as INFERRED with an explicit reason when the product is SaaS/admin and no native stack is present) is a candidate for Phase 3 with the KNOWN/INFERRED distinction preserved.

Other single observations: "big wall display" (→ tv/desktop), "32 inch", "1080p landscape" (kiosk display size cues), "iPad" already mapped, "macOS app" already mapped, "Outlook" (email client rendering is out of scope).
