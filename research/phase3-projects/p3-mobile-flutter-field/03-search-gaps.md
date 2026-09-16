######## checklist with pass fail status per item
status=CONFIDENT modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.722 · heuristic
### Setup / progress checklist  `comp-setup-checklist`  [component/wizard; component/platform] score 0.552 · heuristic
### Desktop screen shrunk to a phone  `anti-mobile-desktop-shrunk`  [antipattern/platform; anti-pattern/platform] score 0.462 · platform-standard
### Bottom tab bar  `nav-bottom-tabs`  [pattern/navigation; navigation/platform] score 0.392 · platform-standard
######## photo capture camera attachment in a form
status=CONFIDENT modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=['form'] negatives=[]
### Form stack with sections  `layout-form-stack`  [pattern/layout; layout] score 0.493 · heuristic
### Form  `comp-form`  [component/form; component] score 0.48 · heuristic
### No decorative imagery  `imagery-none`  [pattern/imagery; visual] score 0.459 · heuristic
### Single column, one task  `layout-single-column`  [pattern/layout; layout/platform] score 0.434 · heuristic
######## offline banner status strip
status=AMBIGUOUS modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.773 · engineering-practice
### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.585 · heuristic
### Announce dynamic status changes  `a11y-live-status`  [rule/feedback; component] score 0.414 · accessibility-requirement
### Toast / snackbar / banner  `comp-toast-notification`  [component/notification; component] score 0.411 · platform-standard
######## segmented button severity selector
status=CONFIDENT modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Floating action button (Material)  `cta-fab`  [pattern/cta; layout/platform] score 0.519 · platform-standard
### Target size by platform  `a11y-target-size`  [rule/input; interaction] score 0.516 · accessibility-requirement
### Accessible names for every control and image  `a11y-labels-names`  [rule/accessibility; accessibility] score 0.464 · accessibility-requirement
### Tabs  `comp-tabs`  [component/tabs; component] score 0.452 · platform-standard
######## empty loading error states
status=AMBIGUOUS modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Design empty, loading, error, and partial states  `layout-states-empty-loading-error`  [rule/feedback; component] score 0.793 · heuristic
### Only the happy state was designed  `anti-no-states`  [antipattern/craft; anti-pattern] score 0.676 · heuristic
### Empty / zero state  `comp-empty-state`  [component/empty-state; component] score 0.433 · heuristic
### Bottom tab bar  `nav-bottom-tabs`  [pattern/navigation; navigation/platform] score 0.377 · platform-standard
######## keyboard open submit reachable IME inset
status=CONFIDENT modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'keyboard': 'KNOWN', 'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Mobile: keyboard and input types  `mobile-keyboard-ime`  [rule/forms; component/platform] score 0.714 · platform-standard
### Mobile: safe areas and system insets  `mobile-safe-areas`  [rule/layout; layout/platform] score 0.713 · platform-standard
### Inline badges and status chips  `metadata-inline-badges`  [pattern/metadata; layout/platform] score 0.399 · heuristic
### Bottom tab bar  `nav-bottom-tabs`  [pattern/navigation; navigation/platform] score 0.377 · platform-standard
######## sync queue pending items list
status=AMBIGUOUS modes=['create'] platforms={'mobile': 'KNOWN'} inputs={'touch': 'INFERRED'} products={'erp': 'KNOWN'} density=medium stacks=['flutter'] screens=[] negatives=[]
### Offline, sync, and connectivity states  `states-offline-and-sync`  [rule/states; component/platform] score 0.789 · engineering-practice
### List rows  `card-list-row`  [pattern/cards; layout/platform] score 0.564 · platform-standard
### Mobile list and swipe actions  `comp-list-row-mobile`  [component/list; component/platform] score 0.524 · platform-standard
### Mobile: image sizing, overdraw, and effect cost  `mobile-perf-images-overdraw`  [rule/performance; performance/platform] score 0.424 · engineering-practice
