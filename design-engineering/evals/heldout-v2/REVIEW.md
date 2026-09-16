# heldout-v2 blind review

Reviewer worked blind: read only `cases-draft.json`; did not open any skill, lexicon, script, doc, research or other eval file.

- Cases before: 214
- Cases after: 212
- Removed: 2
- Cases edited (any rule): 186

## Edits per rule (number of cases touched)

- Rule 1 (labels from allowed sets): 0
- Rule 2 (platforms implied by wording): 20
- Rule 3 (modes vs problem statement / build verb): 18
- Rule 4 (inputs follow from platform): 27
- Rule 5 (negatives only when explicit): 2
- Rule 6 (required 2-5 / recommended / forbidden off-target): 152
- Rule 7 (concepts 3-8 short concrete phrases): 116
- Rule 8 (offtarget must not be legitimately mentionable): 11
- Rule 9 (expect_abstain only for non-UI work): 0
- Rule 10 (duplicates / unjustifiable cases removed): 2

## Removed cases

- hv2-159: rule 10: too vague to justify expectations (e.g. 'password requirements shown upfront' not derivable from 'make the signup form less annoying'); near-duplicate of hv2-031
- hv2-179: rule 10: near-duplicate of hv2-012 (settings page with ~60 controls to restructure)

## Policies applied

- Rule 2: a bare stack word (React, Vue, Compose, SwiftUI) was not treated as a platform. Web was accepted when the wording had a web cue (page, site, browser, SEO, 404, ctrl+k, mouse, axe, Tailwind, Recharts, Bootstrap, z-index/CSS) or a web-bound stack (Next.js, Nuxt, Astro, Svelte, Angular, htmx, plain HTML/CSS). Mobile was accepted for Flutter/React Native, and for Compose/SwiftUI only with a device cue (phone, tap, bottom sheet, tab bar, FAB, Dynamic Type, TalkBack, 48dp, biometric/OTP, permission prompts, App Store paywall). Otherwise platforms=[] and `platform` added to `missing`, inputs cleared.
- Rule 4: web inputs set to pointer+keyboard; touch kept only when phones/mobile/tablet/touch appear in the wording. Kiosk=touch, tv=remote, mobile=touch, desktop=keyboard/pointer (plus touch where a touchscreen is named).
- Rule 3: create removed from problem statements (e.g. 'redo', 'make it usable', 'is painful'); kept where a build/design verb is present.
- Rule 6: required trimmed to what any competent answer must cover; doubtful ones moved to recommended. Forbidden entries dropped where a good answer could legitimately touch the concern (e.g. motion on low-end devices, privacy at a payment kiosk, navigation when the constraint is 'do not change navigation').
- Rule 7: concept phrases normalised to 2-4 words; meta phrases ('ask which platform', 'clarify platform') and query restatements removed.
- Rule 8: offtarget entries removed where a good answer would naturally name the thing it avoids (e.g. 'guilt-trip copy', 'countdown timers', 'dark patterns', 'long tutorial').
- Rule 5: negatives removed where the query only implied a constraint (hv2-170 'muscle memory', hv2-207 no explicit 'no libraries').
- Rule 9: all 21 abstain cases checked; each is backend/DB/infra/CI/auth-token/build-tooling work. hv2-195/202/206 (CSS layout breakage) correctly kept as design work.
