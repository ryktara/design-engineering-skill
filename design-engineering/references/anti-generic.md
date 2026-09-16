# Anti-generic: justification, not prohibition

AI-generated interfaces converge on the same devices regardless of product. Nothing here is forbidden; each device needs a reason rooted in the product, the platform, or the brand system. If you cannot state the reason in one sentence, remove the device.

## Contents
- The default cluster to recognise
- Device-by-device justification rules
- Structural moves that do more than styling
- Self-check before delivering

## The default cluster to recognise

Recognise these as defaults, not choices: sidebar + four KPI cards + chart + table for any "dashboard"; hero with headline, gradient subtitle, two buttons and a floating screenshot for any landing page; cards inside cards; purple→pink gradients and radial blobs; frosted glass panels; pills for every control; an icon in a tinted circle beside every feature; oversized display text everywhere; Inter or Space Grotesk on every product; scroll-triggered fade-ups on every section; cream + serif + terracotta "premium" look; near-black + acid accent "tech" look; dense newspaper hairlines as "editorial" look. Any of these can be right; the failure is arriving there without a product-specific reason.

## Device-by-device justification rules

| Device | Keep when | Remove or replace when |
|---|---|---|
| Gradient | encodes depth/scrim over imagery; part of the brand's defined token set; a single signature use | decorative background, button fill, text fill, KPI tile, or "to add interest" |
| Glass / blur | a transient platform material (sheet, menu, Mica/Acrylic, iOS material) over content that must remain visible; contrast verified against worst-case backdrop; GPU cost measured | application cards, panels, nav bars, anything on TV or low-end devices |
| Card container | the item is a discrete tappable object, needs elevation (drag, overlay), or spacing cannot express the grouping | wrapping sections, forms, single lines, KPIs; nested cards; "to make a grid" |
| Pill / full radius | filters, tags, compact status, segmented controls | buttons, inputs, nav items, and tags all at once |
| Icon | disambiguates an action, state, or object type; platform set expected (tab bar, toolbar) | beside every heading or list item; emoji as icons; decorative feature-grid icons |
| Hero section | landing/campaign page where showing the real product or outcome persuades | app screens, docs, articles; the same skeleton for unrelated products |
| Shadow / elevation | transient layers (menus, dialogs, dragged items); one resting level for tappable cards | on every panel; multiple shadow recipes; "depth" for decoration |
| Animation | state change, continuity (open/close, shared element), feedback, focus movement on TV; one orchestrated brand moment | scroll-reveal on every section, parallax, ambient motion, hover bounce, every KPI counting up |
| Display-size text | the single focal element of the screen; TV scale | app headings, KPI tiles, every section title |
| Illustration | onboarding/empty/error moments in one consistent style | decoration on every card; blob-and-person stock art |
| Sidebar | 6+ peer sections and frequent switching on wide screens | three destinations; marketing; phones; TV |

## Structural moves that do more than styling

- Replace nested boxes with headings, whitespace from the spacing scale, and hairline dividers.
- Give the screen one focal element and demote everything else by one or two steps of size/contrast.
- Choose the section order of a page from the buyer's or user's questions, not from a template.
- Let the product's own material carry identity: the data (charts, tabular figures), the artwork (posters, backdrops), the photograph of the physical thing, the live demo.
- Pick typography for the brief and verify coverage/figures; if the codebase has a font, keep it.
- Encode identity in structure (navigation model, layout rhythm, card geometry, metadata treatment, focus treatment) before colour; multi-brand systems that differ only in colour fail the fingerprint check.
- Prefer platform materials and controls over hand-made imitations; they carry accessibility and theming for free.

## Self-check before delivering

Run through the screen and answer honestly:

1. Could this layout belong to any other product in the category unchanged? If yes, what one structural choice makes it this product's?
2. Count cards, pills, icons, gradients, shadows, animations. For each count above two, name the reason for each instance.
3. Is any text below the platform floor, any contrast unmeasured, any focus state missing, any hover-only action, any auto-motion without reduced-motion handling?
4. Does the hierarchy read in one glance: focal element, then supporting, then chrome?
5. Are spacing values on the scale and edges aligned?
6. Did the codebase's existing tokens, components, fonts, and navigation survive, or were they replaced without a reason?

`advise.py search "<request>" --kind antipattern` returns the specific anti-patterns that apply to a request; the review rubric turns this list into scored findings.
