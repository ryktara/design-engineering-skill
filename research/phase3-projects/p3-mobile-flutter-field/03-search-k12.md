## design-engineering search: Flutter field inspection app for utility technicians working outdoors with gloves and patchy connectivity: checklist, defect report form, offline sync
status=CONFIDENT modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=['form'] negatives=[]
facets required=['component', 'layout', 'platform', 'navigation', 'direction'] unmet=['direction'] diversity=0.83
MISSING: brand: no brand assets, guideline, or character description available

### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.599 · engineering-practice
Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- use when: Field, travel, and public-venue apps; anything used with poor connectivity; any screen that writes data.
- avoid when: Read-only always-online desktop tools where connectivity loss is exceptional (still show an error, not a blank).
- why: lexical 0.516, structural 0.7 (platform mobile, mode create)

### Field use: sunlight readability and glanceable status  `mobile-field-use`  [rule/environment; accessibility/platform] score 0.598 · heuristic
Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding).
- use when: Couriers, inspectors, technicians, warehouse and construction workers, outdoor kiosks: bright light, gloves, movement, interruptions.
- avoid when: Desk-bound indoor use.
- why: lexical 0.399, structural 0.84 (platform mobile, input touch, mode create, product erp, environment gloves,outdoor)

### Form stack with sections  `layout-form-stack`  [pattern/layout; layout] score 0.42 · heuristic
Labels above fields (not placeholders), one column except for tightly related pairs (city/postcode), section headings as real headings, inline validation on blur with error text linked via aria-describedby, and the primary action at the end of the form or in a sticky footer. Field width should hint expected length.
- use when: Data entry and settings: labelled fields in one column, grouped into titled sections, with the save/submit action fixed in a predictable place.
- avoid when: Spreadsheet-style batch entry (use a data-entry grid), or tiny forms of 1–2 fields (inline them).
- incompatible with: layout-immersive-rails, layout-rails
- why: lexical 0.163, structural 0.6 (mode create, screen form, density medium)

### Mobile: keyboard and input types  `mobile-keyboard-ime`  [rule/forms; component/platform] score 0.402 · platform-standard
Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms.
- use when: Every text field.
- avoid when: Never leave the default keyboard for emails, numbers, phone, or URLs; never let the keyboard cover the focused field or the submit button.
- why: lexical 0.109, structural 0.76 (platform mobile, input touch, mode create)

### Bottom tab bar  `nav-bottom-tabs`  [pattern/navigation; navigation/platform] score 0.395 · platform-standard
3–5 items, icon + label always (no icon-only), safe-area aware, current item indicated by more than tint. Each tab keeps its own navigation stack. Don't put actions (compose, add) in the tab bar unless it is the app's primary action and it is styled as an action, not a destination.
- use when: Phone apps with 3–5 top-level destinations of similar importance that users switch between often.
- avoid when: More than five destinations, tablet/desktop widths (use a rail), single-flow apps, or when one destination dominates usage.
- flutter: NavigationBar (M3) or CupertinoTabBar; keep per-tab Navigator state.
- incompatible with: nav-left-rail, nav-top-bar, nav-tv-side, nav-tv-top-tabs
- why: lexical 0.0, structural 0.7 (platform mobile, input touch, mode create, density medium)

### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.391 · heuristic
Pill only for status/category/count; text inside the pill (never colour only); ≤2 per item; consistent colour mapping across the product; not clickable unless it is a filter.
- use when: Status, category, or count must be scannable in lists and headers (Open/Closed, New, 3 unread).
- avoid when: As decoration on everything; when more than two badges per item appear, the design has become noisy.
- incompatible with: metadata-minimal, layout-immersive-rails
- why: lexical 0.0, structural 0.78 (platform mobile, mode create, product erp, density medium)

### Single column, one task  `layout-single-column`  [pattern/layout; layout/platform] score 0.367 · heuristic
Content width capped for reading (~60–75 characters per line), vertical rhythm from the spacing scale, primary action reachable without scrolling on the shortest supported viewport, or sticky at the bottom.
- use when: Phone screens, forms, reading, onboarding, kiosks: one primary thing per screen.
- avoid when: Comparison tasks, dense data, or wide desktop windows where a single narrow column wastes the viewport and forces scrolling.
- incompatible with: layout-three-pane, layout-dashboard-grid, layout-table-first
- why: lexical 0.035, structural 0.64 (platform mobile, mode create, screen form)

### Desktop screen shrunk to a phone  `anti-mobile-desktop-shrunk`  [antipattern/platform; anti-pattern/platform] score 0.342 · platform-standard
Re-prioritise for the phone's tasks: fewer things, bigger targets, bottom-anchored actions, list rows instead of tables, sheets instead of side panels, platform navigation grammar.
- use when: Tables with horizontal scroll as the primary view, 12-px labels, sidebars turned into hamburger menus with 20 items, hover-only actions, dense toolbars.
- avoid when: Never.
- why: lexical 0.0, structural 0.76 (platform mobile, input touch, mode create, product erp)

### Mobile: gestures are shortcuts, not the only way  `mobile-gestures-discoverable`  [rule/input; interaction/platform] score 0.342 · accessibility-requirement
Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action.
- use when: Swipe-to-delete, swipe between tabs, pull to refresh, long press menus, pinch zoom.
- avoid when: Never make a gesture the only path to an action; never fight system gestures (back swipe edge, home).
- why: lexical 0.0, structural 0.76 (platform mobile, input touch, mode create)

### Mobile: image sizing, overdraw, and effect cost  `mobile-perf-images-overdraw`  [rule/performance; performance/platform] score 0.342 · engineering-practice
Request images at the rendered size (Coil/Glide/SDWebImage/expo-image with sizing), remove redundant opaque backgrounds (overdraw), keep list item composables/cells cheap and keyed, prefer opacity/transform animations, measure with the platform profiler (Perfetto, Instruments, Flipper).
- use when: Image-heavy lists, blur/shadow effects, nested backgrounds, animations in lists.
- avoid when: Never load original-resolution images into thumbnails; never animate blur or shadow radius in scrolling lists.
- incompatible with: surface-glass
- why: lexical 0.0, structural 0.76 (platform mobile, input touch, mode create)

### Mobile: follow the platform navigation grammar  `mobile-platform-navigation`  [rule/navigation; navigation/platform] score 0.342 · platform-standard
iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions.
- use when: Choosing tab bars, drawers, stacks, sheets, and back behaviour on iOS vs Android.
- avoid when: Do not port an iOS tab bar with iOS icons to Android unchanged or vice versa unless the product is deliberately brand-uniform; do not build custom back handling that breaks the system back.
- why: lexical 0.0, structural 0.76 (platform mobile, input touch, mode create)

### Form  `comp-form`  [component/form; component] score 0.341 · heuristic
Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
- use when: Any data entry: settings, checkout, applications, record editing.
- avoid when: Batch entry of many similar rows (use a data-entry grid); single toggles (inline).
- why: lexical 0.195, structural 0.52 (mode create, screen form)

Filtered out: anti-generic-sidebar-dashboard (platform ['desktop', 'web'] not in request ['mobile']); anti-desktop-scaled-to-tv (platform ['tv'] not in request ['mobile']); dir-public-kiosk (platform ['kiosk'] not in request ['mobile']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['mobile']); layout-table-first (platform ['desktop', 'web'] not in request ['mobile']); tv-dpad-axes (platform ['tv'] not in request ['mobile'])
