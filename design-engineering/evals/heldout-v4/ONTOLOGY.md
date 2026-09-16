# Concept ontology (public ids and labels) — concept-policy/v1, Phase 5 (114 concepts)

One id = one reusable design requirement. Use these ids in `required_concepts`, `critical_concepts`, `recommended`, `forbidden`. Five ids were added in Phase 5: `media.track_selection`, `tv.time_navigation`, `interaction.selection_visible`, `data.comparison_structure`, `feedback.trust_signals`.

## a11y
- `a11y.contrast` — high contrast
- `a11y.color_not_only` — no colour alone for status
- `a11y.accessible_names` — accessible names and labels
- `a11y.text_scaling` — dynamic type / text scaling
- `a11y.reduced_motion` — reduced motion
- `a11y.semantics` — semantic structure and roles
- `a11y.live_status` — live region status announcements
- `a11y.dialog_focus` — dialog focus management

## adaptive
- `adaptive.breakpoint_matrix` — breakpoint matrix
- `adaptive.navigation_transform` — navigation transforms across widths

## anti
- `anti.interruptive_upsell` — no interruptive upsells
- `anti.decorative_gradient` — no decorative gradients or glass
- `anti.template_landing` — no template skeleton pages
- `anti.oversized_display` — no oversized display text everywhere
- `anti.scroll_animation` — no scroll-triggered animation everywhere
- `anti.platform_scaling` — no scaled desktop layout on TV or phone
- `anti.default_fonts` — no default AI font clusters

## brand
- `brand.structural_differentiation` — structural, not cosmetic, brand differentiation
- `brand.token_layers` — semantic token layers per theme
- `brand.dark_mode_redesign` — dark mode as a surface redesign, not inversion
- `brand.type_roles` — type roles and scale
- `brand.font_loading` — font loading, subsetting and fallback metrics
- `brand.corner_language` — one corner language for controls
- `brand.imagery_purpose` — imagery and icons with purpose

## content
- `content.readable_measure` — readable line length
- `content.i18n_expansion` — text expansion and RTL

## data
- `data.pagination_strategy` — pagination / load-more strategy
- `data.filter_chips` — applied filters as removable chips with counts
- `data.search_results` — search field and results behaviour
- `data.chart_by_question` — chart form chosen from the analytical question
- `data.accessible_chart_alternative` — accessible chart summary and table alternative
- `data.kpi_comparison` — KPI with comparison and precision
- `data.realtime_window` — real-time rolling window and thresholds
- `data.exception_first` — exceptions and anomalies first
- `data.drilldown` — drill-down from summary to detail
- `data.refresh_timestamp` — last-updated / refresh state
- `data.comparison_structure` — aligned comparison structure with one recommended choice

## desktop
- `desktop.spacing_grid` — desktop 4 px grid and control heights
- `desktop.persist_workspace` — persisted workspace and selection
- `desktop.fluent_materials` — Fluent system resources and materials

## env
- `env.outdoor_readability` — high contrast outdoors / sunlight readability
- `env.glanceable_status` — glanceable status

## feedback
- `feedback.trust_signals` — trust and cost transparency before commitment
- `feedback.validation_errors` — inline validation messages and error recovery
- `feedback.confirmation_destructive` — confirmation of destructive or high-risk actions
- `feedback.progress_indicator` — progress indicator

## form
- `form.autofill_attributes` — autofill / input-type attributes per field

## interaction
- `interaction.focus_visible` — visible focus
- `interaction.focus_restore` — focus restoration
- `interaction.keyboard_navigation` — keyboard navigation and focus order
- `interaction.dpad_reachability` — D-pad focus reachability
- `interaction.back_semantics` — BACK behaviour
- `interaction.hover_independence` — no hover dependence
- `interaction.shortcuts` — keyboard shortcuts / accelerators
- `interaction.menu_semantics` — menu keyboard semantics and focus return
- `interaction.tabs_roving` — tabs with roving focus
- `interaction.tree_semantics` — tree view semantics
- `interaction.command_palette` — command palette semantics
- `interaction.drawer_focus` — drawer / side panel focus in and out
- `interaction.selection_visible` — selected state visible and distinct from focus and hover

## layout
- `layout.one_primary_action` — one primary action per view
- `layout.spacing_scale` — consistent spacing scale
- `layout.focal_hierarchy` — visual hierarchy with one focal point
- `layout.no_nested_cards` — no nested cards
- `layout.settings_grouping` — settings grouped with visible current values
- `layout.hero_thesis` — hero as a specific thesis with real proof
- `layout.media_card` — media card with one focus target and one status overlay

## media
- `media.resume_playback` — continue watching / resume playback
- `media.details_play_first` — details screen with Play as default focus
- `media.watchlist` — watchlist / save for later
- `media.search_tv` — TV search with system keyboard or voice
- `media.live_channel_switching` — live channel switching and mini guide
- `media.track_selection` — subtitle and audio track selection reachable from the player

## navigation
- `navigation.orientation_and_back` — current location marked; back restores state
- `navigation.platform_grammar` — platform navigation grammar
- `navigation.rail_semantics` — rail / sidebar grouping, active indicator, collapse
- `navigation.deep_link_state` — URL / route reflects state

## onboarding
- `onboarding.setup_checklist` — optional setup checklist
- `onboarding.linear_wizard` — linear multi-step wizard
- `onboarding.permission_priming` — permission priming before the system prompt
- `onboarding.feature_education` — non-blocking feature education

## perf
- `perf.image_sizing` — image sizing and formats
- `perf.layout_shift` — no layout shift
- `perf.focus_latency` — focus latency
- `perf.js_budget` — JS cost of UI decisions

## privacy
- `privacy.shared_device` — privacy of on-screen data on shared devices
- `privacy.sensitive_masking` — masking of sensitive values with explicit reveal

## process
- `process.decision_order` — structure before style decision order
- `process.reuse_first` — reuse → extend → compose → new
- `process.safe_modification` — safe modification of existing code
- `process.render_verify` — render and inspect before claiming done

## state
- `state.loading_empty_error` — loading, empty and error states
- `state.offline_sync` — offline and sync states
- `state.saving_conflict` — saving, saved and conflict states
- `state.session_expiry` — session expiry and idle reset
- `state.unsaved_changes_guard` — unsaved-changes guard

## table
- `table.tabular_figures` — tabular figures and numeric alignment
- `table.column_priority` — column priority on narrow widths
- `table.selection_bulk` — selection state and bulk actions
- `table.inline_edit` — inline editing
- `table.virtualization` — virtualization of long collections

## touch
- `touch.minimum_target` — large touch targets (≥44–48 px)
- `touch.thumb_reach` — thumb reach
- `touch.gestures_discoverable` — discoverable gestures
- `touch.ime_keyboard` — on-screen keyboard (IME) aware layout
- `touch.safe_areas` — safe areas and notches

## tv
- `tv.ten_foot_typography` — 10-foot typography, readable at distance
- `tv.safe_margins` — TV safe margins
- `tv.player_autohide` — auto-hide timing of player controls
- `tv.epg_pinned_channels` — pinned channel column and now marker
- `tv.dark_first` — dark-first TV palette
- `tv.no_touch_hover` — no touch or hover assumptions on TV
- `tv.sign_in_code` — activation-code sign-in
- `tv.time_navigation` — time navigation in the guide: now marker, jump by time and day
