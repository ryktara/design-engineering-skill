# ClinicBoard

Front-desk web app for a small medical clinic. SvelteKit 2, Svelte 5 (runes), Tailwind CSS 3. No component library; a small in-house set lives in `src/lib/components`.

```
npm install
npm run dev      # http://localhost:5173
npm run build
```

## Screens

| Route | Purpose |
| --- | --- |
| `/` | Redirects to `/appointments` |
| `/appointments` | Day view, 08:00-18:00 time grid, one column per practitioner, appointment chips, practitioner filter, "New appointment" modal |
| `/patients` | Searchable table (name, DOB, phone, last visit, balance); row click opens detail |
| `/patients/[id]` | Patient detail with Summary / Visits / Billing tabs |
| `/waiting` | Three-column board: Checked-in / With practitioner / Done |
| `/reports` | Simple daily counts |
| `/settings` | Plain settings form |

All data is deterministic sample data (`src/lib/data/sample.ts`, 40 patients, 25 appointments) held in memory via `src/lib/stores.ts`.

## Design language

- **Navigation:** a fixed 240px left rail (logo, five primary links) plus a 56px top header (clinic name, user menu). Only the content area scrolls.
- **Theme:** light only. `color-scheme: light` is set in `src/app.css`; there is no dark mode.
- **Typography:** "Source Sans 3" (Google Fonts) with a `system-ui` fallback. Sizes stay within Tailwind's default scale; body text is `text-sm`.
- **Colour:** custom palette in `tailwind.config.ts`. Primary is teal (`primary-*`), neutrals are slate (`neutral-*`), semantic tones are `success`, `warning`, `danger`. Components use these tokens only; no arbitrary hex values.
- **Surfaces:** bordered-flat. White panels with a 1px `neutral-200` border on a `neutral-50` page background. No shadows anywhere except the modal.
- **Radius:** 6px default (`rounded`); `rounded-sm` is 4px for badges and small controls.
- **Spacing:** Tailwind's default 4px-based scale (`gap-4`, `p-4`, `h-9` controls, `h-14` bars).
- **Components:** `Button`, `Card`, `Table`, `Badge`, `Tabs`, `Modal`, `Input`, `Select` in `src/lib/components`. Controls are 36px tall; tables use 44px rows with uppercase 12px column headers.

## Layout of the source

```
src/
  app.css              Tailwind layers + light-theme CSS variables
  app.html
  routes/
    +layout.svelte     Rail + header shell
    +page.ts           Redirect to /appointments
    appointments/      Day view
    patients/          List and [id] detail
    waiting/           Board
    reports/
    settings/
  lib/
    components/        Button, Card, Table, Badge, Tabs, Modal, Input, Select
    data/sample.ts     Seeded sample data
    stores.ts          Svelte stores
tailwind.config.ts     Palette, font, radius
```
