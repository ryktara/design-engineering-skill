# Motion: purpose, tokens, platform character

Motion exists to communicate hierarchy, continuity, feedback, and state change, or to express a deliberately defined brand character. Anything else is removed.

## Purposes and defaults

| Purpose | Example | Duration | Easing |
|---|---|---|---|
| feedback | pressed state, toggle | 80–150 ms | ease-out |
| state change | expand/collapse, show/hide | 150–250 ms | ease-out in, ease-in out |
| continuity | list → detail shared element, page transition | 250–350 ms | standard/emphasised |
| focus movement (TV) | scale/glow on focus, rail scroll to pivot | ≤150 ms focus, ≤250 ms scroll | ease-out |
| attention | one toast, one badge pulse | ≤300 ms, once | ease-out |
| brand moment | launch sequence, campaign hero | ≤1.2 s total, once per session | orchestrated |

Tokens: three durations (fast/base/slow), two or three easings, one spring preset if the platform uses springs. Components reference tokens.

## Rules

- Animate transform and opacity; never width/height/top/left/blur/box-shadow in lists or on scroll.
- Exit faster than enter; interruptible; never queue-blocking (input must not be dropped, especially on TV).
- Reduced motion: remove non-essential motion and render final states immediately (`prefers-reduced-motion`, `UIAccessibility.isReduceMotionEnabled`, `ANIMATOR_DURATION_SCALE`, `UISettings.AnimationsEnabled`); crossfade may replace movement.
- No auto-playing carousels without pause/stop; no ambient motion that competes with focus or reading.
- One orchestrated reveal on a landing page is a choice; fade-ups on every section are a template marker.
- Measure: 60 fps on the lowest target device; TV boxes and old phones first.

## Platform character

- Web: CSS transitions/animations first; View Transitions API for continuity; Motion/Framer only when already present; scroll-driven animations sparingly.
- iOS: system springs (`.spring`, `.snappy`), matchedGeometryEffect / zoom transitions; sheets and navigation use system motion.
- Android: Material motion (container transform, shared axis), `SharedTransitionLayout`, spring() for gestures; predictive back animations.
- Windows: connected animations, subtle Fluent reveal; entrance animations only on first show; respect "animation effects" setting.
- TV: motion is focus: scale 1.05–1.1 and glow/border in ≤150 ms; rail scroll to pivot; backdrop crossfade 300–500 ms debounced; nothing decorative.
- Kiosk: functional only; attract loop is the one allowed ambient animation and it stops on touch.

## Vocabulary for expressive brands

If the brand is motion-led (consumer social, education), define: ≤3 named easings, ≤3 durations, one signature transition (a morph, a wipe), where it applies (navigation, state change), and a reduced-motion fallback. Keep professional/enterprise products on functional motion.
