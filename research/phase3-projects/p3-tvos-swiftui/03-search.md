## design-engineering search: tvOS documentary streaming app: sign-in with an activation code and a player with auto-hiding transport controls and a subtitle picker
status=AMBIGUOUS modes=['create'] platforms={'tv': 'KNOWN'} inputs={'remote': 'KNOWN'} products={'media': 'KNOWN'} density=medium stacks=['swiftui'] screens=['auth', 'player'] negatives=[]
facets required=['component', 'layout', 'platform', 'interaction', 'navigation', 'direction'] unmet=[] diversity=0.83
MISSING: brand: no brand assets, guideline, or character description available
CONFLICTS: platform (request kept; repository platform recorded as context)

### Player with overlay controls  `layout-split-player`  [pattern/layout; layout/platform] score 0.737 · platform-standard
Controls overlay with a scrim, show on any key/tap/mouse move, hide after ~3–5 s of inactivity but never while a control has focus or a menu is open; first focus lands on play/pause; LEFT/RIGHT seek with visible thumbnail/time; subtitles and audio selection in a side sheet that pauses the auto-hide; the progress bar is a real slider with keyboard/remote semantics and a text time readout.
- use when: Full-screen playback with transient controls (scrub, play/pause, next, subtitles, quality) that appear on input and hide on inactivity.
- avoid when: Never for non-media; for audio-only use a persistent mini-player instead.
- incompatible with: layout-table-first, layout-dashboard-grid, surface-bordered-panes
- why: lexical 0.569, structural 0.92 (platform tv, input remote (stated), mode create, product media, screen player)

### TV: transport control conventions  `tv-player-controls`  [rule/player; component/platform] score 0.726 · platform-standard
Media keys work without showing the overlay (PLAY/PAUSE, FF/RW); DPAD_CENTER on the playing video toggles play/pause or shows controls (pick one and be consistent with the platform); LEFT/RIGHT on the progress bar seek in fixed steps with preview; overlay auto-hides after 3–5 s of no input; subtitle/audio pickers are side sheets that keep playback visible; live TV adds channel UP/DOWN and a mini guide.
- use when: Video/audio playback screens.
- avoid when: Never hide controls while a control is focused; never require SELECT twice to pause.
- why: lexical 0.632, structural 0.84 (platform tv, input remote (stated), mode create, product media)

### TV sign-in: code on screen and companion device  `comp-tv-sign-in`  [component/sign-in; component/platform] score 0.724 · platform-standard
Primary path: a short activation code (6–8 chars, no ambiguous glyphs, large 10-foot type) plus a short URL or QR code, polled until the companion device completes sign-in; the TV screen shows what to do in one sentence, the code, a 'waiting' state that is obviously alive, expiry with a regenerate action, and a secondary 'type here' fallback using the system keyboard. On success land on the profile picker; on shared TVs offer a PIN for adult profiles. Focus starts on the primary fallback button so BACK/SELECT behave predictably.
- use when: Any TV app with accounts or subscriptions.
- avoid when: Never make remote-typed passwords the primary path.
- swiftui: tvOS: use system keyboard fallback with .focusable(); consider Apple TV's built-in Continuity Keyboard / passkeys where applicable.
- why: lexical 0.564, structural 0.92 (platform tv, input remote (stated), mode create, product media, screen auth)

### Player transport controls  `comp-player-controls`  [component/player; component/platform] score 0.701 · platform-standard
Play/pause, seek slider with time readout and keyboard/remote stepping, skip ±10 s, next/previous where relevant, captions and audio track selectors, quality only if user-facing, live indicator and go-to-live for live streams, volume on web/desktop only (TV uses the remote), controls overlay auto-hides except while focused/hovered; every control labelled; captions styling respects system preferences.
- use when: Video/audio playback surfaces.
- avoid when: Never custom-build when the platform control set already meets the need and the brand allows it.
- swiftui: AVPlayerViewController on tvOS gives system transport UI with Siri Remote support; customise only if brand requires.
- why: lexical 0.522, structural 0.92 (platform tv, input remote (stated), mode create, product media, screen player)

### Cinematic media (TV)  `dir-cinematic-media-tv`  [direction/direction; direction/platform] score 0.508 · internal-preference
Backdrop-driven home, side navigation, landscape rails with focus scale + glow, focus-revealed metadata, dark tinted canvas, a heavy display face for titles, filled icons at ≥32 dp, cinematic but debounced crossfades, and a player with transient controls. Identity via backdrop treatment (scrim shape, grain), display type, and the focus glow colour.
- use when: Streaming/IPTV/VOD apps on TV with strong artwork; the brand wants immersion.
- avoid when: Weak artwork, low-end boxes, catalogues where text metadata dominates (use 'Broadcast guide').
- incompatible with: nav-top-bar, layout-table-first, surface-bordered-panes, focus-ring-standard, motion-spring
- why: lexical 0.17, structural 0.92 (platform tv, input remote (stated), mode create, product media, density medium)

### Focus is the action (TV)  `cta-focus-selects`  [pattern/cta; layout/platform] score 0.494 · platform-standard
No 'button-like' cards with an inner button; the whole card is focusable and selectable. Detail screen: ≤4 actions in one row, first focus on Play/Resume, LEFT/RIGHT between them, DOWN to rails. Long press or a Menu key can open secondary actions. Never require diagonal or multi-key gestures.
- use when: TV browse/detail screens: the focused card is the call to action, SELECT opens, and detail screens expose a small row of focusable buttons (Play, Resume, Add to list) with a deterministic first focus.
- avoid when: Never on touch/pointer platforms.
- incompatible with: cta-single-primary, cta-toolbar-commands, cta-sticky-bar
- why: lexical 0.0, structural 0.92 (platform tv, input remote (stated), mode create, product media, screen player)

### TV side navigation (collapsible drawer)  `nav-tv-side`  [pattern/navigation; navigation/platform] score 0.494 · platform-standard
Collapsed icon strip on the left that expands to icons+labels when focus enters it; pressing LEFT from the first item of any rail moves focus into the drawer, RIGHT returns to the last focused content item (focus restoration is mandatory). Back from content returns to the drawer, Back from the drawer exits or goes Home. Never require UP to reach navigation from deep in a page.
- use when: TV apps with 4–8 sections (Home, Live, Movies, Series, Search, Settings) where the vertical axis is free for section switching and the horizontal axis is used for browsing rails.
- avoid when: Two or three sections (use top tabs), single-purpose players, or when content rails need the full width and the drawer would fight with left-edge focus.
- swiftui: tvOS: TabView with .tabViewStyle(.sidebarAdaptable) provides the system sidebar; do not rebuild it.
- incompatible with: nav-top-bar, nav-left-rail, nav-bottom-tabs, nav-tv-top-tabs
- why: lexical 0.0, structural 0.92 (platform tv, input remote (stated), mode create, product media, density medium)

### Focus-revealed metadata (TV)  `metadata-focus-reveal`  [pattern/metadata; layout/platform] score 0.484 · platform-standard
Reveal into reserved space (a fixed detail area above the rails or an expanded card whose height is pre-allocated) so rows never jump; keep the reveal text ≥24 sp; delay the reveal ~150 ms so quick scrubbing does not flash text.
- use when: TV rails: unfocused cards show title only (or nothing over art); the focused card or a fixed detail strip shows synopsis, year, duration, rating.
- avoid when: Never for touch/pointer; and on TV avoid when the reveal reflows the rail (use a fixed strip instead).
- incompatible with: metadata-rich, layout-table-first
- why: lexical 0.0, structural 0.92 (platform tv, input remote (stated), mode create, product media, density medium)

### Focus-driven motion (TV)  `motion-focus-scale`  [pattern/motion; platform/visual] score 0.458 · platform-standard
Focus scale 1.05–1.1 in ≤150 ms, rail scroll ≤250 ms, backdrop crossfade 300–500 ms debounced; input must never be dropped while animating (queue focus moves); test on a low-end device for dropped frames.
- use when: TV: motion exists to show where focus is and where it went; scale/glow on focus, smooth rail scrolling to the pivot, backdrop crossfade.
- avoid when: Never elsewhere; and on TV never add decorative ambient motion that competes with focus.
- incompatible with: motion-spring, motion-expressive
- why: lexical 0.0, structural 0.84 (platform tv, input remote (stated), mode create, product media)

### TV top tabs  `nav-tv-top-tabs`  [pattern/navigation; navigation/platform] score 0.454 · platform-standard
Tabs sit in the top safe area; Back from any rail jumps focus to the active tab and scrolls to top; focused tab shows the underline/pill with ≥3:1 contrast and the label stays visible. Switching tabs does not move focus into content until the user presses DOWN.
- use when: Two to five sections, when the left edge must stay free for immersive artwork or when the brand wants a browsing feel closer to a broadcast guide.
- avoid when: More than five sections, or when rows below are long (UP from deep rows must scroll back to tabs predictably; that gets slow).
- swiftui: tvOS TabView default style renders top tabs; use .focusSection() on content groups.
- incompatible with: nav-tv-side, nav-top-bar, nav-left-rail, nav-bottom-tabs
- why: lexical 0.0, structural 0.92 (platform tv, input remote (stated), mode create, product media, density medium)

### Immersive backdrop  `imagery-immersive-backdrop`  [pattern/imagery; platform/visual] score 0.408 · platform-standard
Backdrop at panel resolution max, decoded once and cached, crossfade debounced, dual scrim (left-to-right and bottom-to-top) so the text block and the rails both read; verify text contrast against the brightest backdrop in the catalogue, not the sample.
- use when: Media home/detail screens on large displays where the focused/selected item's backdrop fills the screen behind text and rails.
- avoid when: Low-end devices, inconsistent artwork, or screens where users read a lot of text.
- incompatible with: imagery-none, surface-bordered-panes, layout-table-first, density-high
- why: lexical 0.0, structural 0.84 (platform tv, input remote (stated), mode create, product media)

### Scale + glow/border focus (TV)  `focus-scale-glow`  [pattern/focus; interaction/platform] score 0.395 · platform-standard
Exactly one item focused at all times and it must be on screen; scale must not clip against neighbours (reserve padding = scale overflow); focus state includes a border (2–4 dp) or glow (2–32 dp elevation) plus scale so it survives any artwork; selected ≠ focused (a selected tab still needs a focus treatment); initial focus is deterministic on every screen.
- use when: All TV UI: focused item scales (1.05–1.1), gains a border or glow with ≥3:1 contrast, and its metadata may expand; unfocused items stay quiet.
- avoid when: Never elsewhere; and on TV never rely on colour tint alone.
- swiftui: tvOS gives .focusable() views the system lift automatically; add .hoverEffect(.lift) and custom borders only when brand demands.
- incompatible with: focus-ring-standard, focus-none-touch-only, focus-underline
- why: lexical 0.0, structural 0.7 (platform tv, input remote (stated), mode create)

Filtered out: anti-hero-template (platform ['web'] not in request ['tv']); comp-data-entry-grid (platform ['desktop', 'web'] not in request ['tv']); dir-windows-native-tool (platform ['desktop'] not in request ['tv']); dir-industrial-hmi (platform ['desktop', 'kiosk', 'tablet'] not in request ['tv']); nav-bottom-tabs (platform ['mobile'] not in request ['tv']); layout-three-pane (platform ['desktop', 'web'] not in request ['tv']); typography-serif-editorial (platform ['mobile', 'tablet', 'web'] not in request ['tv']); typography-monospace-technical (platform ['desktop', 'web'] not in request ['tv'])
