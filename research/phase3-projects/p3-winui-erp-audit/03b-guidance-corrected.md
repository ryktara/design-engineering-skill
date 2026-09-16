## guidance: Warehouse clerks say our WinUI stock adjustments page is confusing and they keep missing rows; the screen reader reads the status column as just text
status=CONFIDENT mode=['accessibility', 'audit'] platform=['desktop'] input=['keyboard', 'pointer'] product=['erp'] screen=[] stack=['winui'] density=high env=[] risk=low negatives=[]
concerns required=['accessibility', 'interaction', 'component', 'feedback', 'data-display'] covered=1.0 uncovered=[] recommended=['states', 'anti-pattern'] bundle=6 (core 2 + guardrails 4) diversity=0.83 redundancy=0.36

### Core (what to build)
- **Data table / grid** `comp-data-table` [component/data-display/structure] — Sticky header, row height by density token, zebra striping optional (prefer hover/selection highlight), column resize/reorder/visibility persisted, sort indicator with aria-sort, selection checkbox column with header select-all and a count, row actions visible on focus as well as hover, inline edit with Enter/Escape, keyboard grid navigation (arrows, Home/End, PageUp/Down), virtualised rows, loading skeleton rows, empty state inside the table body. Financial tables: see numeric rule.
  - winui: CommunityToolkit DataGrid (keyboard + UIA built in) or ItemsView; avoid ListView with a fake header row.
  - selected for: highest-scoring component with lexical evidence; lexical 0.205, structural 0.72
- **Form** `comp-form` [component/feedback/structure] — Labels above, help text below, required marked in text, field widths sized to content, grouped by section with headings, one column, inline validation on blur, error summary on submit with links to fields, primary action last (or sticky), unsaved-changes guard, autosave with status for long forms, autofill attributes. TV: one field per row, DOWN moves to next, system keyboard, minimal fields.
  - winui: TextBox Header + PlaceholderText; InfoBar for summary; ValidationErrors via Community Toolkit or manual TextBlock linked by AutomationProperties.DescribedBy.
  - selected for: highest-scoring component with lexical evidence; lexical 0.105, structural 0.4

### Guardrails (must hold)
- **Non-text contrast 3:1 for controls and focus** `a11y-nontext-contrast` [accessibility; accessibility-requirement] — Any visual that identifies a control or its state needs ≥3:1 against adjacent colours. Hairline dividers at 1.2:1 are fine as decoration but an input whose only boundary is that hairline fails.
  - selected for: required concern accessibility: accessibility mode
- **Desktop: keyboard is a first-class input** `desktop-keyboard-first` [interaction; platform-standard] — Document shortcuts in menus and tooltips; F2 edits, Delete deletes with undo, Ctrl+F finds, F6 cycles panes; grids use arrow keys and Ctrl/Shift selection; every dialog has a default and cancel button; access keys shown on Alt (Windows).
  - selected for: required concern interaction: accessibility mode: operability is part of the review
- **Accessible names for every control and image** `a11y-labels-names` [accessibility; accessibility-requirement] — Visible label for inputs (not placeholder-only), aria-label/accessibilityLabel/contentDescription/AutomationProperties.Name for icon-only controls, alt text for meaningful images and alt="" for decorative ones, link text that makes sense out of context. The accessible name must contain the visible label text (label in name).
  - selected for: required concept a11y.accessible_names
- **Saving, saved, autosave, session expiry, and permission-denied states** `states-persistence-and-session` [feedback/states; heuristic] — Show saving → saved as a quiet inline status with a timestamp (not a toast per keystroke); autosave drafts and say so; warn before a session expires with a way to extend, and never discard entered data on expiry (restore the draft after re-authentication); permission-denied is a designed state that explains what is missing and who can grant it rather than an empty screen; destructive or irreversible saves confirm once with the safe action as default.
  - selected for: recommended concern states: audits check empty/loading/error handling

Omitted (redundant): comp-data-entry-grid (same category as a core pick or incompatible with one)
Filtered out: anti-scroll-animation-everything (platform ['mobile', 'web'] not in request ['desktop']); anti-desktop-scaled-to-tv (platform ['tv'] not in request ['desktop']); anti-mobile-desktop-shrunk (platform ['mobile'] not in request ['desktop']); comp-media-card (platform ['mobile', 'tv', 'web'] not in request ['desktop']); comp-tv-rail (platform ['tv'] not in request ['desktop']); comp-epg (platform ['tablet', 'tv', 'web'] not in request ['desktop'])
