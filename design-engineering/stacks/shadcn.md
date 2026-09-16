# shadcn/ui (React + Tailwind + Radix/Base UI)

## Conventions to detect and respect
- `components.json` (style, base colour, `cssVariables`, aliases), `components/ui/*` owned source, `lib/utils.ts` `cn()`, `cva` variants, CSS variables in `globals.css` (`--background`, `--foreground`, `--primary`, `--ring`, `--radius`, sidebar/chart variables).
- The registry components are the project's design system: extend by adding variants/sizes to `cva` definitions or composing, not by forking a parallel component set.

## Implementation rules
- Tokens: the `--background/--foreground` pairs are semantic roles; add roles (e.g. `--surface`, `--success`) in both `:root` and `.dark`, register in `@theme`/config, validate with `tokens.py`.
- Component choice by task: `Dialog` (decision), `AlertDialog` (destructive confirm), `Sheet` (side panel), `Drawer` (mobile bottom), `Popover` (light context), `DropdownMenu`/`ContextMenu` (actions), `Command` (palette/combobox), `Tabs` (peer views, URL-synced), `Sidebar` (rail; one instance), `DataTable` recipe with TanStack for tables (+ virtualisation beyond ~200 rows), `Form` wrappers for label/description/error ids, `Sonner` for toasts, `Skeleton` at final sizes.
- Variants: `cva` for size/emphasis/density; keep `default/secondary/outline/ghost/destructive` semantics; do not add a `gradient` variant without a brand reason.
- Radius: `--radius` is a single token; do not mix arbitrary `rounded-*` values.
- Icons: Lucide, imported individually, sized 16/20/24 via tokens, `aria-hidden` when decorative, labelled when alone.
- Charts: `chart` components (Recharts) use `--chart-1..5`; align with the categorical palette and provide a table alternative.
- Focus: keep the `ring` tokens; never remove `focus-visible:ring` styles from primitives.

## Verification
Browser pane at the project's breakpoints; dark/light; Tab through dialogs/menus/command palette; check `Sidebar` collapse states.
