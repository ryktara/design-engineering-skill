# Angular

## Conventions to detect and respect
- Standalone components vs NgModules, signals vs RxJS state, Angular Router with lazy routes; Angular Material / CDK, PrimeNG, or a custom library; `styles.scss` with theme mixins or CSS variables; Angular CDK a11y utilities.
- Material theming (M3 `mat.theme` / `define-theme`) maps to semantic roles; extend through theme tokens, not deep selectors.

## Implementation rules
- Use CDK primitives: `cdkTrapFocus`, `LiveAnnouncer`, `FocusMonitor`, `cdk-virtual-scroll-viewport` for long lists, `CdkMenu`, `CdkDialog`, overlays with positioning; Material components carry ARIA and keyboard behaviour.
- Forms: reactive forms with `aria-describedby` error linkage and `mat-error`; `autocomplete` attributes; validation on blur/submit.
- Tables: `mat-table` with `matSort`, `matPaginator`, and virtual scroll for large sets; sticky headers.
- Animations: Angular animations or CSS; respect reduced motion (`matchMedia`) and disable non-essential animations.
- Routing state: query params for filters/tabs; `withInMemoryScrolling` for restoration; route guards for unsaved changes.
- Change detection: `OnPush`, `trackBy`/`track` in `@for`; avoid heavy pipes in templates.
- Theme: CSS variables + `prefers-color-scheme`/`data-theme`; Material system variables for light/dark; validate both.

## Verification
`ng serve` → browser pane/Playwright at the matrix; Tab pass; reduced-motion; console errors; `ng lint` a11y rules if configured.
