## guidance: Pharmacy prescription pick-up kiosk flow: identify the patient, show ready prescriptions, confirm; public touch screen in the store
status=CONFIDENT mode=['create'] platform=['kiosk'] input=['touch'] product=['ecommerce', 'healthcare'] screen=[] stack=[] density=None env=['public'] risk=high negatives=[]
MISSING: brand: no brand assets, guideline, or character description available; stack: implementation stack not stated and no repository evidence
concerns required=['structure', 'states', 'interaction', 'accessibility', 'environment', 'privacy', 'feedback'] covered=1.0 uncovered=[] recommended=['navigation', 'anti-pattern', 'brand', 'performance'] bundle=6 (core 3 + guardrails 3) diversity=1.0 redundancy=0.17

### Core (what to build)
- **Public kiosk** `dir-public-kiosk` [brand/structure] — Attract screen → hub of large tiles → linear flows with one giant primary action, ≥60 px targets in the reach zone, ≥20 px text with high contrast for glare, brand colour on header and primary action, filled icons with labels, idle timeout with countdown, cancel always visible, audio/visual feedback. Identity via tile geometry, illustration, and the brand colour field.
  - selected for: highest-scoring direction with lexical evidence; lexical 0.5, structural 0.66
- **Filled icons for distance and touch** `icon-filled-system` [brand/content] — Filled or bold-weight set at ≥24 dp (≥32 dp on TV), always with a visible label in navigation, filled/outline swap allowed only to show selection.
  - selected for: highest-scoring pattern with lexical evidence; lexical 0.182, structural 0.66
- **Touch-only focus handling (mobile)** `focus-none-touch-only` [accessibility/interaction] — Pressed state within 100 ms (ripple/opacity/scale), 44 pt / 48 dp targets, screen-reader focus order = visual order, and platform focus visuals left enabled for keyboard/switch users (do not disable). Kiosks: larger targets (≥ 60 px) and no hover-dependent affordances.
  - selected for: highest-scoring pattern with lexical evidence; lexical 0.069, structural 0.66

### Guardrails (must hold)
- **Saving, saved, autosave, session expiry, and permission-denied states** `states-persistence-and-session` [feedback/states; heuristic] — Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry (restore the draft after re-authentication); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default.
  - selected for: required concern states: every screen ships empty/loading/error states
- **Kiosk: public, hurried, standing users** `kiosk-public-use` [environment/interaction/privacy; platform-standard] — Targets ≥60 px, body text ≥20 px, high contrast for glare, one task per screen, reachable-height controls (ADA reach ranges: interactive elements within 380–1220 mm), idle timeout with countdown that clears the session, attract screen as the hub, audio/visual feedback on every tap, and a visible way to cancel at every step.
  - selected for: required concern environment: public kiosk use
- **Users always know where they are and how to go back** `nav-orientation-and-back` [navigation; heuristic] — Current location marked (aria-current, selected tab, breadcrumb, page title); URL/route reflects state on web and deep-linkable screens; back returns to the previous screen with its scroll and selection; titles match the navigation label that led there.
  - selected for: recommended concern navigation: how users arrive and leave
Filtered out: anti-desktop-scaled-to-tv (platform ['tv'] not in request ['kiosk']); anti-hover-only-actions (platform ['desktop', 'web'] not in request ['kiosk']); chart-flow-sankey (platform ['desktop', 'web'] not in request ['kiosk']); comp-media-card (platform ['mobile', 'tv', 'web'] not in request ['kiosk']); comp-epg (platform ['tablet', 'tv', 'web'] not in request ['kiosk']); comp-hero-section (platform ['mobile', 'web'] not in request ['kiosk'])
