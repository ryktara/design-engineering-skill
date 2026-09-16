## design-engineering search: Photos attached to a defect report are tiny thumbnails you can't check in the field.
status=CONFIDENT modes=['audit', 'refactor'] platforms={'mobile': 'INFERRED'} inputs={'touch': 'INFERRED'} products={} density=None stacks=[] screens=[] negatives=[]
facets required=['accessibility', 'interaction', 'component', 'platform', 'anti-pattern'] unmet=['anti-pattern'] diversity=0.92
MISSING: platform: only inferred from wording (mobile); confirm before committing

### Photo capture field (take, retake, replace, remove)  `comp-photo-capture-field`  [component/form; component/platform] score 0.628 · heuristic
The field shows the thumbnails as one row of ≥ 96 dp tiles plus an 'Add photo' tile; each thumbnail is a single target that opens a sheet with Retake (camera, replaces in place), Replace from gallery, Remove (confirm only if it is the last required photo); state per photo (uploading, pending sync, failed with retry) is shown on the tile with icon + text; the camera permission is primed before the first capture and refusal leaves a way to continue; capture never loses other field values (persist the draft before opening the camera); images are downscaled for upload and the original is kept until sync succeeds; the field is announced as 'Photos, 2 of 4 added' and each tile as 'Photo 1, retake or remove'.
- use when: Forms that attach one or more photos: inspections, claims, returns, deliveries, ID capture.
- avoid when: Desktop-only forms (use a file picker with drag-and-drop) or single decorative avatars.
- why: lexical 0.667, structural 0.58 (platform mobile, input touch, mode audit)

### Field use: sunlight readability and glanceable status  `mobile-field-use`  [rule/environment; accessibility/platform] score 0.447 · heuristic
Target ≥7:1 text contrast and avoid thin weights and pale tints (glare washes them out); prefer light UI on white or very high-contrast dark, not mid-tone surfaces; make the current state glanceable (large status word plus colour plus icon, readable at arm's length in two seconds); ≥48 dp targets with ≥12 dp spacing and no precision gestures when gloves are likely; put the next action in thumb reach; large numerals for counts and readings; keep the screen usable one-handed and interruptible (state survives backgrounding).
- use when: Couriers, inspectors, technicians, warehouse and construction workers, outdoor kiosks: bright light, gloves, movement, interruptions.
- avoid when: Desk-bound indoor use.
- why: lexical 0.157, structural 0.8 (platform mobile, input touch, mode audit, environment outdoor)

### Mobile: keyboard and input types  `mobile-keyboard-ime`  [rule/forms; component/platform] score 0.381 · platform-standard
Set keyboard type and autocomplete/textContentType/autofillHints per field, return key action (Next/Done), scroll the focused field above the keyboard, keep the primary action reachable while the keyboard is open (or on the keyboard toolbar), and dismiss on tap outside for non-modal forms.
- use when: Every text field.
- avoid when: Never leave the default keyboard for emails, numbers, phone, or URLs; never let the keyboard cover the focused field or the submit button.
- why: lexical 0.103, structural 0.72 (platform mobile, input touch, mode audit)

### Mobile: gestures are shortcuts, not the only way  `mobile-gestures-discoverable`  [rule/input; interaction/platform] score 0.348 · accessibility-requirement
Every gesture action has a visible equivalent (overflow menu, button); swipe actions reveal labelled buttons; avoid horizontal swipes inside horizontally scrolling content; respect the platform back gesture; long press shows a menu, never a hidden critical action.
- use when: Swipe-to-delete, swipe between tabs, pull to refresh, long press menus, pinch zoom.
- avoid when: Never make a gesture the only path to an action; never fight system gestures (back swipe edge, home).
- why: lexical 0.043, structural 0.72 (platform mobile, input touch, mode audit)

### Mobile: safe areas and system insets  `mobile-safe-areas`  [rule/layout; layout/platform] score 0.33 · platform-standard
Content respects safe-area insets (SwiftUI safeAreaInset / .ignoresSafeArea only for backgrounds, Compose WindowInsets + edge-to-edge, RN SafeAreaView/useSafeAreaInsets, web env(safe-area-inset-*)); bottom actions sit above the home indicator/gesture bar; keyboard (IME) insets push the focused field into view.
- use when: Bottom bars, sticky CTAs, full-bleed backgrounds, top app bars, landscape.
- avoid when: Never hard-code status/nav bar heights.
- why: lexical 0.011, structural 0.72 (platform mobile, input touch, mode audit)

### Mobile: image sizing, overdraw, and effect cost  `mobile-perf-images-overdraw`  [rule/performance; performance/platform] score 0.324 · engineering-practice
Request images at the rendered size (Coil/Glide/SDWebImage/expo-image with sizing), remove redundant opaque backgrounds (overdraw), keep list item composables/cells cheap and keyed, prefer opacity/transform animations, measure with the platform profiler (Perfetto, Instruments, Flipper).
- use when: Image-heavy lists, blur/shadow effects, nested backgrounds, animations in lists.
- avoid when: Never load original-resolution images into thumbnails; never animate blur or shadow radius in scrolling lists.
- incompatible with: surface-glass
- why: lexical 0.0, structural 0.72 (platform mobile, input touch, mode audit)

### Mobile: follow the platform navigation grammar  `mobile-platform-navigation`  [rule/navigation; navigation/platform] score 0.324 · platform-standard
iOS: tab bar + navigation stack with large titles where idiomatic, sheets for secondary tasks, swipe back. Android: navigation bar, predictive back, top app bar, modal bottom sheets, up vs back. Cross-platform frameworks still map to these; state deviations as brand decisions.
- use when: Choosing tab bars, drawers, stacks, sheets, and back behaviour on iOS vs Android.
- avoid when: Do not port an iOS tab bar with iOS icons to Android unchanged or vice versa unless the product is deliberately brand-uniform; do not build custom back handling that breaks the system back.
- why: lexical 0.0, structural 0.72 (platform mobile, input touch, mode audit)

### Mobile: primary actions in thumb reach  `mobile-thumb-reach`  [rule/layout; layout/platform] score 0.324 · heuristic
Frequent actions in the bottom third; top-left/right for rare actions (back, settings); large phones make top targets a two-handed reach so provide bottom alternatives (bottom search bar, pull-down). Sheets and menus open from the bottom.
- use when: Deciding where the primary action, tab bar, search, and frequent controls go on phones.
- avoid when: Do not put destructive actions in the easiest-to-hit zone.
- why: lexical 0.0, structural 0.72 (platform mobile, input touch, mode audit)

### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.309 · engineering-practice
Design the offline state as a first-class state: show connectivity clearly but calmly (a persistent status strip, not a blocking modal), keep already-loaded content usable, queue writes locally with a visible 'pending sync' marker per item and a 'last synced' timestamp, retry automatically with backoff and let the user retry manually, never lose entered data, and resolve conflicts explicitly (show both versions or last-writer-wins with an undo). Reads: stale data is labelled with its age.
- use when: Field, travel, and public-venue apps; anything used with poor connectivity; any screen that writes data.
- avoid when: Read-only always-online desktop tools where connectivity loss is exceptional (still show an error, not a blank).
- why: lexical 0.022, structural 0.66 (platform mobile, mode audit)

### Dialog focus management  `a11y-modal-dialog`  [rule/dialog; component/platform] score 0.297 · accessibility-requirement
On open: focus the first meaningful control (or the heading), trap Tab inside, inert the background, label the dialog by its title. On close: return focus to the invoker. Escape and the visible close button both close; destructive confirmations put the safe action as default. Use <dialog>/showModal, ContentDialog, .sheet, ModalBottomSheet rather than a div overlay.
- use when: Modals, sheets, drawers, popovers, confirmations.
- avoid when: Do not use modals for content that could be inline; do not stack modals.
- why: lexical 0.0, structural 0.66 (platform mobile, mode audit)

### Native accessibility semantics (mobile/desktop)  `a11y-native-semantics`  [rule/accessibility; accessibility/platform] score 0.297 · accessibility-requirement
Use platform roles and traits (Compose semantics{role, contentDescription, heading()}, SwiftUI accessibilityLabel/.accessibilityAddTraits, RN accessibilityRole, WinUI/WPF AutomationProperties + AutomationPeer for custom controls); merge descendants so a card is one element; announce async status with live regions/announceForAccessibility. Test with TalkBack/VoiceOver/Narrator, not only by reading code.
- use when: Custom composables/views/controls, merged semantics for cards, live regions for status, headings in long screens.
- avoid when: Never build a tappable Box/View/Border without a role and name.
- why: lexical 0.0, structural 0.66 (platform mobile, mode audit)

### First-run: permission priming and feature education without blocking  `onboarding-first-run`  [rule/feedback; component/platform] score 0.297 · platform-standard
Ask for a permission only at the moment the feature needs it, preceded by a one-screen explanation of the benefit and what happens on refusal (priming), then trigger the system prompt; never chain several permission prompts on launch, and always offer a way to continue without the permission. Feature education is non-blocking: a dismissible coach mark or inline tip anchored to the real control, one at a time, never a modal tour on first launch; it can be replayed from help, is skipped for keyboard/screen-reader users unless it is accessible, and stops after it has been dismissed once. Both respect reduced motion and never cover the primary action.
- use when: Apps that need OS permissions (camera, location, notifications) or that introduce new features to returning users.
- avoid when: Strictly ordered setup where every step is mandatory (use a wizard) or products with no permissions and no new features.
- why: lexical 0.0, structural 0.66 (platform mobile, mode audit)

Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['mobile']); chart-heatmap-matrix (platform ['desktop', 'web'] not in request ['mobile']); comp-plan-comparison (platform ['desktop', 'web'] not in request ['mobile']); comp-kiosk-keypad (platform ['kiosk', 'tablet'] not in request ['mobile']); dir-analytical-console (platform ['desktop', 'web'] not in request ['mobile']); dir-public-kiosk (platform ['kiosk'] not in request ['mobile']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['mobile']); dir-product-marketing-site (platform ['web'] not in request ['mobile'])
