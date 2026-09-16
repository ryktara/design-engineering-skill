# Phase 6 implemented qualification round (32 tasks, 16 codebases, frozen candidate c3)

Run each sentence verbatim. Codebases: `p3-*` → `research/phase3-projects/<case>/project`; `p5-*` → `research/phase5-projects/<codebase>/project`; `p6-*` → `research/phase6-projects/<codebase>/project`. Protocol: `PROTOCOL.md` (Phase 5 steps) + `PHASE6-ADDENDUM.md`.

| task | codebase | platform | existing UI | mode word | sentence |
|---|---|---|---|---|---|
| p6-01 | p3-nextjs-saas | web | yes | no | Nobody can find the API keys section; it is buried at the bottom of the settings page. |
| p6-02 | p3-nextjs-saas | web | new screen | yes | Add a usage page showing this month's API calls against the plan quota. |
| p6-03 | p3-ecommerce-web | web | yes | no | On the product listing, shoppers cannot narrow 120 products down to what fits them. |
| p6-04 | p3-ecommerce-web | web | yes | no | The cart page: removing an item happens instantly and people do it by accident. |
| p6-05 | p3-react-dashboard-polish | web | yes | yes | Review the alerts panel against our accessibility checklist. |
| p6-06 | p5-sveltekit-clinic | web | yes | no | The patient detail billing tab shows amounts that do not line up. |
| p6-07 | p5-sveltekit-clinic | web (tablet) | yes | no | Front desk on a tablet: the appointment chips are too small to tap. |
| p6-08 | p6-vue-inventory | web | yes | no | The products table is unusable once the warehouse has 200 SKUs. |
| p6-09 | p6-vue-inventory | web | yes | no | Stock adjustment form: Save and Discard look identical and people click the wrong one. |
| p6-10 | p6-vue-inventory | web | yes | yes | Make the dashboard tell the manager which items need reordering today. |
| p6-11 | p3-mobile-flutter-field | mobile | yes | no | Inspectors in gloves keep missing the small checkbox on each defect row. |
| p6-12 | p3-mobile-flutter-field | mobile | new element | yes | Add an offline banner and retry to the report list for when the site has no signal. |
| p6-13 | p5-swiftui-habits | mobile | yes | no | The habit list has nothing to say the first time you open the app. |
| p6-14 | p5-swiftui-habits | mobile | yes | no | VoiceOver reads the streak ring as "image". |
| p6-15 | p6-compose-banking | mobile | yes | no | Typing an amount on the transfer screen brings up the letters keyboard and the Send button disappears under it. |
| p6-16 | p6-compose-banking | mobile | yes | no | Freezing a card happens the instant you touch the switch. |
| p6-17 | p6-compose-banking | mobile | yes | no | In dark mode the transaction dates are barely visible. |
| p6-18 | p3-erp-desktop-dotnet | desktop | yes | no | Purchase order screen: operators want to do the whole entry without touching the mouse. |
| p6-19 | p3-erp-desktop-dotnet | desktop | new element | yes | Add a status bar with the last sync time and any failed postings. |
| p6-20 | p3-winui-erp-audit | desktop | yes | no | The stock adjustments grid shows 3,000 rows and scrolling is janky. |
| p6-21 | p5-avalonia-fleet | desktop | yes | no | The vehicle map and the list fight for space when the window is narrow. |
| p6-22 | p5-avalonia-fleet | desktop | yes | no | Dispatchers say the job form asks for the same driver details twice. |
| p6-23 | p3-winui-erp-audit | desktop | yes | yes | Review the supplier invoice matching page for keyboard operability. |
| p6-24 | p3-android-tv-compose | tv | yes | no | Pressing back on the detail page throws you out of the app. |
| p6-25 | p3-android-tv-compose | tv | new element | yes | Add a "continue watching" row to the home screen. |
| p6-26 | p3-tvos-swiftui | tv | yes | no | Titles on the poster rows are cut off and there is no way to read the full name. |
| p6-27 | p6-tv-iptv-web | tv | yes | no | In the channel guide the time header jumps every half hour and you lose where you were. |
| p6-28 | p6-tv-iptv-web | tv | yes | no | The player controls stay on screen for the whole film. |
| p6-29 | p3-kiosk-pharmacy | kiosk | yes | no | The confirmation screen prints the receipt but never says the pick-up is complete. |
| p6-30 | p6-kiosk-transit | kiosk | yes | no | People walk away mid-purchase and the next person finds the previous ticket half bought. |
| p6-31 | p6-kiosk-transit | kiosk | yes | no | The + and − buttons for the number of tickets are fiddly for older passengers. |
| p6-32 | p6-kiosk-transit | kiosk | new element | yes | Add a Welsh language option to the ticket machine. |

Coverage: web 10 · mobile 7 · desktop 6 · TV 5 · kiosk 4 (32 tasks, 16 codebases: 12 from Phases 3/5 + 4 new: p6-compose-banking, p6-kiosk-transit, p6-tv-iptv-web, p6-vue-inventory). Existing-UI changes 27 (new screen / element on an existing codebase: p6-02, p6-12, p6-19, p6-25, p6-32). Sentences without an explicit mode word: 24 of 32.

Pre-registration lives in each task's `00-expectation.json` (written from the code before any advise command): `critical_concepts` (1–3), `expected_concepts`, `forbidden_concepts`, preservation slots.
