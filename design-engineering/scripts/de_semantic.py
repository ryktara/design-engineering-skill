#!/usr/bin/env python3
"""design-engineering semantic layer (Phase 4): concept ontology, scope model, task-intent model,
expected-concept derivation. Stdlib only, deterministic. Versioned as concept-policy/v1.

Pipeline position:  prompt -> scope -> intent/mode -> requirements -> concerns -> EXPECTED CONCEPTS
                    -> candidate retrieval -> bundle selection -> direction -> project adaptation
"""

from __future__ import annotations

import re

CONCEPT_POLICY_VERSION = "concept-policy/v1"

# ---------------------------------------------------------------------------
# Concept ontology: id -> (human label, primary concern). One id = one reusable design requirement.
# Namespaces: a11y interaction navigation layout state form table data adaptive touch tv desktop
#             privacy env perf content brand motion onboarding media anti process feedback
# ---------------------------------------------------------------------------
CONCEPT_META: dict[str, tuple[str, str]] = {
    # interaction
    "interaction.focus_visible": ("visible focus", "interaction"),
    "interaction.focus_restore": ("focus restoration", "interaction"),
    "interaction.keyboard_navigation": ("keyboard navigation and focus order", "interaction"),
    "interaction.dpad_reachability": ("D-pad focus reachability", "interaction"),
    "interaction.back_semantics": ("BACK behaviour", "interaction"),
    "interaction.hover_independence": ("no hover dependence", "interaction"),
    "interaction.shortcuts": ("keyboard shortcuts / accelerators", "interaction"),
    "interaction.menu_semantics": ("menu keyboard semantics and focus return", "interaction"),
    "interaction.tabs_roving": ("tabs with roving focus", "interaction"),
    "interaction.tree_semantics": ("tree view semantics", "interaction"),
    "interaction.command_palette": ("command palette semantics", "interaction"),
    "interaction.drawer_focus": ("drawer / side panel focus in and out", "interaction"),
    # touch / mobile
    "touch.minimum_target": ("large touch targets (≥44–48 px)", "interaction"),
    "touch.thumb_reach": ("thumb reach", "interaction"),
    "touch.gestures_discoverable": ("discoverable gestures", "interaction"),
    "touch.ime_keyboard": ("on-screen keyboard (IME) aware layout", "interaction"),
    "touch.safe_areas": ("safe areas and notches", "adaptive"),
    # accessibility
    "a11y.contrast": ("high contrast", "accessibility"),
    "a11y.color_not_only": ("no colour alone for status", "accessibility"),
    "a11y.accessible_names": ("accessible names and labels", "accessibility"),
    "a11y.text_scaling": ("dynamic type / text scaling", "accessibility"),
    "a11y.reduced_motion": ("reduced motion", "accessibility"),
    "a11y.semantics": ("semantic structure and roles", "accessibility"),
    "a11y.live_status": ("live region status announcements", "accessibility"),
    "a11y.dialog_focus": ("dialog focus management", "accessibility"),
    # tables / data
    "table.tabular_figures": ("tabular figures and numeric alignment", "data-display"),
    "table.column_priority": ("column priority on narrow widths", "data-display"),
    "table.selection_bulk": ("selection state and bulk actions", "data-display"),
    "table.inline_edit": ("inline editing", "data-display"),
    "table.virtualization": ("virtualization of long collections", "performance"),
    "data.pagination_strategy": ("pagination / load-more strategy", "data-display"),
    "data.filter_chips": ("applied filters as removable chips with counts", "data-display"),
    "data.search_results": ("search field and results behaviour", "component"),
    "data.chart_by_question": ("chart form chosen from the analytical question", "data-display"),
    "data.accessible_chart_alternative": ("accessible chart summary and table alternative", "accessibility"),
    "data.kpi_comparison": ("KPI with comparison and precision", "data-display"),
    "data.realtime_window": ("real-time rolling window and thresholds", "data-display"),
    "data.exception_first": ("exceptions and anomalies first", "data-display"),
    "data.drilldown": ("drill-down from summary to detail", "navigation"),
    "data.refresh_timestamp": ("last-updated / refresh state", "states"),
    # tv
    "tv.ten_foot_typography": ("10-foot typography, readable at distance", "content"),
    "tv.safe_margins": ("TV safe margins", "structure"),
    "tv.player_autohide": ("auto-hide timing of player controls", "interaction"),
    "tv.epg_pinned_channels": ("pinned channel column and now marker", "data-display"),
    "tv.dark_first": ("dark-first TV palette", "brand"),
    "tv.no_touch_hover": ("no touch or hover assumptions on TV", "interaction"),
    "tv.sign_in_code": ("activation-code sign-in", "component"),
    # media jobs
    "media.resume_playback": ("continue watching / resume playback", "component"),
    "media.details_play_first": ("details screen with Play as default focus", "component"),
    "media.watchlist": ("watchlist / save for later", "component"),
    "media.search_tv": ("TV search with system keyboard or voice", "component"),
    "media.live_channel_switching": ("live channel switching and mini guide", "component"),
    "media.track_selection": ("subtitle and audio track selection reachable from the player", "component"),
    "tv.time_navigation": ("time navigation in the guide: now marker, jump by time and day", "navigation"),
    "interaction.selection_visible": ("selected state visible and distinct from focus and hover", "interaction"),
    "data.comparison_structure": ("aligned comparison structure with one recommended choice", "data-display"),
    "feedback.trust_signals": ("trust and cost transparency before commitment", "feedback"),
    # states
    "state.loading_empty_error": ("loading, empty and error states", "states"),
    "state.offline_sync": ("offline and sync states", "states"),
    "state.saving_conflict": ("saving, saved and conflict states", "states"),
    "state.session_expiry": ("session expiry and idle reset", "states"),
    "state.unsaved_changes_guard": ("unsaved-changes guard", "states"),
    # layout / structure
    "layout.one_primary_action": ("one primary action per view", "structure"),
    "layout.spacing_scale": ("consistent spacing scale", "structure"),
    "layout.focal_hierarchy": ("visual hierarchy with one focal point", "structure"),
    "layout.no_nested_cards": ("no nested cards", "structure"),
    "layout.settings_grouping": ("settings grouped with visible current values", "structure"),
    "layout.hero_thesis": ("hero as a specific thesis with real proof", "content"),
    "layout.media_card": ("media card with one focus target and one status overlay", "component"),
    # navigation
    "navigation.orientation_and_back": ("current location marked; back restores state", "navigation"),
    "navigation.platform_grammar": ("platform navigation grammar", "navigation"),
    "navigation.rail_semantics": ("rail / sidebar grouping, active indicator, collapse", "navigation"),
    "navigation.deep_link_state": ("URL / route reflects state", "navigation"),
    # forms / feedback
    "feedback.validation_errors": ("inline validation messages and error recovery", "feedback"),
    "feedback.confirmation_destructive": ("confirmation of destructive or high-risk actions", "feedback"),
    "feedback.progress_indicator": ("progress indicator", "feedback"),
    "form.autofill_attributes": ("autofill / input-type attributes per field", "feedback"),
    # onboarding
    "onboarding.setup_checklist": ("optional setup checklist", "feedback"),
    "onboarding.linear_wizard": ("linear multi-step wizard", "feedback"),
    "onboarding.permission_priming": ("permission priming before the system prompt", "feedback"),
    "onboarding.feature_education": ("non-blocking feature education", "feedback"),
    # privacy / environment
    "privacy.shared_device": ("privacy of on-screen data on shared devices", "privacy"),
    "privacy.sensitive_masking": ("masking of sensitive values with explicit reveal", "privacy"),
    "env.outdoor_readability": ("high contrast outdoors / sunlight readability", "environment"),
    "env.glanceable_status": ("glanceable status", "environment"),
    # performance
    "perf.image_sizing": ("image sizing and formats", "performance"),
    "perf.layout_shift": ("no layout shift", "performance"),
    "perf.focus_latency": ("focus latency", "performance"),
    "perf.js_budget": ("JS cost of UI decisions", "performance"),
    # adaptive / content
    "adaptive.breakpoint_matrix": ("breakpoint matrix", "adaptive"),
    "adaptive.navigation_transform": ("navigation transforms across widths", "adaptive"),
    "content.readable_measure": ("readable line length", "content"),
    "content.i18n_expansion": ("text expansion and RTL", "content"),
    # desktop
    "desktop.spacing_grid": ("desktop 4 px grid and control heights", "structure"),
    "desktop.persist_workspace": ("persisted workspace and selection", "states"),
    "desktop.fluent_materials": ("Fluent system resources and materials", "brand"),
    # brand / tokens
    "brand.structural_differentiation": ("structural, not cosmetic, brand differentiation", "brand"),
    "brand.token_layers": ("semantic token layers per theme", "brand"),
    "brand.dark_mode_redesign": ("dark mode as a surface redesign, not inversion", "brand"),
    "brand.type_roles": ("type roles and scale", "content"),
    "brand.font_loading": ("font loading, subsetting and fallback metrics", "performance"),
    "brand.corner_language": ("one corner language for controls", "brand"),
    "brand.imagery_purpose": ("imagery and icons with purpose", "brand"),
    # anti / process
    "anti.interruptive_upsell": ("no interruptive upsells", "anti-pattern"),
    "anti.decorative_gradient": ("no decorative gradients or glass", "anti-pattern"),
    "anti.template_landing": ("no template skeleton pages", "anti-pattern"),
    "anti.oversized_display": ("no oversized display text everywhere", "anti-pattern"),
    "anti.scroll_animation": ("no scroll-triggered animation everywhere", "anti-pattern"),
    "anti.platform_scaling": ("no scaled desktop layout on TV or phone", "anti-pattern"),
    "anti.default_fonts": ("no default AI font clusters", "anti-pattern"),
    "process.decision_order": ("structure before style decision order", "anti-pattern"),
    "process.reuse_first": ("reuse → extend → compose → new", "structure"),
    "process.safe_modification": ("safe modification of existing code", "structure"),
    "process.render_verify": ("render and inspect before claiming done", "structure"),
}
CONCEPTS = set(CONCEPT_META)
CONCEPT_LABELS = {k: v[0] for k, v in CONCEPT_META.items()}
CONCEPT_CONCERN = {k: v[1] for k, v in CONCEPT_META.items()}

# Relationships that materially help derivation/retrieval. `requires` closes over required concepts
# (a required concept's requirements become required); `related` widens recommended coverage;
# `conflicts` removes a concept when the other is required.
RELATIONS: dict[str, dict[str, list[str]]] = {
    "table.inline_edit": {"requires": ["interaction.keyboard_navigation", "interaction.focus_visible", "feedback.validation_errors"], "related": ["state.saving_conflict"]},
    "table.selection_bulk": {"requires": ["a11y.color_not_only"], "related": ["interaction.keyboard_navigation"]},
    "interaction.dpad_reachability": {"requires": ["interaction.focus_visible"], "related": ["interaction.focus_restore"]},
    "tv.player_autohide": {"requires": ["interaction.back_semantics"]},
    "data.drilldown": {"requires": ["navigation.orientation_and_back"]},
    "data.realtime_window": {"requires": ["data.refresh_timestamp"], "related": ["data.exception_first"]},
    "data.exception_first": {"related": ["a11y.color_not_only", "layout.focal_hierarchy"]},
    "onboarding.linear_wizard": {"requires": ["feedback.progress_indicator"], "related": ["state.unsaved_changes_guard"]},
    "media.resume_playback": {"requires": ["interaction.focus_restore"]},
    "media.details_play_first": {"requires": ["interaction.focus_visible"], "related": ["media.watchlist"]},
    "media.live_channel_switching": {"related": ["tv.epg_pinned_channels", "tv.player_autohide"]},
    "a11y.dialog_focus": {"requires": ["interaction.focus_restore"]},
    "state.offline_sync": {"related": ["data.refresh_timestamp", "state.saving_conflict"]},
    "interaction.keyboard_navigation": {"related": ["interaction.shortcuts", "interaction.focus_visible"]},
    "interaction.selection_visible": {"requires": ["a11y.color_not_only"], "related": ["interaction.focus_visible"]},
    "data.comparison_structure": {"related": ["layout.one_primary_action", "table.tabular_figures"]},
    "tv.time_navigation": {"requires": ["interaction.dpad_reachability"], "related": ["tv.epg_pinned_channels"]},
    "media.track_selection": {"requires": ["interaction.back_semantics"]},
    "a11y.contrast": {"related": ["a11y.color_not_only"]},
    "feedback.validation_errors": {"related": ["form.autofill_attributes", "a11y.live_status"]},
    "tv.no_touch_hover": {"conflicts": ["touch.gestures_discoverable", "touch.thumb_reach"]},
    "touch.minimum_target": {"related": ["touch.thumb_reach"]},
    "brand.dark_mode_redesign": {"requires": ["a11y.contrast", "brand.token_layers"]},
    "brand.structural_differentiation": {"related": ["process.decision_order"]},
    "data.chart_by_question": {"requires": ["data.accessible_chart_alternative"], "related": ["a11y.color_not_only"]},
    "layout.hero_thesis": {"related": ["perf.image_sizing", "layout.one_primary_action"]},
}


def requires_closure(ids: list[str]) -> list[str]:
    """Deterministic closure over `requires` (cycle-safe, insertion ordered)."""
    out: list[str] = []
    stack = list(ids)
    while stack:
        c = stack.pop(0)
        if c in out:
            continue
        out.append(c)
        for r in RELATIONS.get(c, {}).get("requires", []):
            if r not in out:
                stack.append(r)
    return out


def relation_cycles() -> list[list[str]]:
    """Cycles in `requires` (validator check)."""
    cycles = []
    for start in RELATIONS:
        seen, node, path = set(), start, [start]
        while True:
            nxt = RELATIONS.get(node, {}).get("requires", [])
            if not nxt:
                break
            node = nxt[0]
            if node in seen or node == start:
                if node == start:
                    cycles.append(path + [node])
                break
            seen.add(node); path.append(node)
    return cycles


# ---------------------------------------------------------------------------
# Platform evidence model (Phase 5). Evidence is typed and graded; platforms are resolved from candidates.
# Types: explicit · stack · form-factor · modality · os · environment · product · repository.
# Strengths: DIRECT (names the platform or an exclusive device) · STRONG_INFERENCE (a form factor,
# environment or modality that implies one platform) · WEAK_INFERENCE (compatible with several).
# WEAK evidence alone never assigns a platform: the contract says UNKNOWN + MISSING confirm.
# ---------------------------------------------------------------------------
PLATFORM_EVIDENCE = {
    "tv": {
        "DIRECT": [("explicit", ["tv", "television", "android tv", "google tv", "apple tv", "tvos", "fire tv", "fire stick", "firestick", "smart tv", "smart-tv", "roku", "tizen", "webos", "set-top", "set top box", "settop", "cable box", "leanback", "iptv", "10-foot ui", "ten-foot ui", "channel app"])],
        "STRONG_INFERENCE": [("environment", ["living room", "living-room", "from the couch", "on the couch", "from the sofa", "sofa", "ten feet away", "10 feet away", "ten-foot", "10-foot", "10 ft"]),
                             ("modality", ["remote control", "with the remote", "on their remote", "their remote", "remote's down arrow", "remote's up arrow", "remote's left arrow", "remote's right arrow", "remote's arrow", "remote's ok", "remote's back", "holding the remote", "arrow on the remote", "controller-driven", "controller driven", "with a controller", "arrow keys on the remote", "d-pad", "dpad"]),
                             ("product", ["channel guide", "programme guide", "program guide", "epg", "linear channels", "channel lineup", "media browser for remote"])],
        "WEAK_INFERENCE": [("form-factor", ["big screen", "big-screen", "big-screen version", "large screen", "wall display", "wall-mounted", "large display", "bedside screen", "bedside", "streaming box", "the big screen"]),
                           ("modality", ["remote", "the remote", "a remote", "arrow keys on a remote", "direction pad", "directional pad", "directional buttons", "direction buttons", "up/down buttons", "ok button", "arrow buttons", "the remote's", "remote's", "without a keyboard", "no keyboard"]),
                           ("environment", ["couch", "the sofa", "lounge", "across the room", "armchair", "foot of the bed", "lean back", "lean-back", "family members", "viewers", "hotel guests", "hotel room"]),
                           ("distance", ["from across the room", "at ten feet", "ten feet", "from a distance", "readable from the", "sit back"]),
                           ("product", ["trailer", "episodes", "episode", "programme", "programmes", "channel", "channels", "captions button", "now-playing bar", "activation code", "sign-in code", "cartoon rows", "camera angles", "player controls", "media app", "the film", "a film"])],
    },
    "mobile": {
        "DIRECT": [("explicit", ["mobile", "phone", "phones", "smartphone", "iphone", "ios", "android phone", "android app", "handset", "handsets", "app store", "play store", "maui app", "watch face"])],
        "STRONG_INFERENCE": [("modality", ["one-handed", "one handed", "one thumb", "thumb", "thumb-reachable", "thumb reachable", "with one hand", "swipe", "swiping", "swipe-to-dismiss", "pull-to-refresh", "edge swipe", "back gesture", "haptic", "face id", "touch id"]),
                             ("environment", ["on the bus", "on the go", "on-the-go", "walking between", "while walking", "in the field", "pocket", "pocket-sized", "in people's pockets", "crowded bus", "on the train", "on the ward", "mid-run", "handlebar", "between stops", "in the queue at"]),
                             ("form-factor", ["home indicator", "notch", "share sheet", "bottom tab bar", "on-screen keyboard covers", "home screen widget", "widget on the home screen"]),
                             ("stack", ["flutter", "reactnative", "expo app", "expo", "compose screen for the", "jetpack compose"]),
                             ("product", ["courier app", "driver app", "rider app", "field app", "field-service app", "field service app", "technician app", "companion app", "android widget", "home-screen widget"])],
        "WEAK_INFERENCE": [("os", ["android", "swiftui", "compose", "kotlin app"]),
                           ("form-factor", ["handheld", "hand-held", "carry it", "carried", "carrying", "carry", "held in the hand", "handset-sized"]),
                           ("product", ["scanner app", "stock counts", "photos", "attach them", "take photos"]),
                           ("modality", ["tap", "taps", "tapping", "scan with the camera", "camera", "barcode", "scan a barcode", "gloves on"]),
                           ("environment", ["outdoors", "outdoor", "on site", "sunlight", "warehouse aisles", "aisles", "in the back room", "runners", "couriers", "delivery riders", "riders", "nurses", "inspectors", "field engineers", "technicians on site", "shoppers scan"])],
    },
    "tablet": {
        "DIRECT": [("explicit", ["tablet", "tablets", "ipad", "surface tablet", "surface tablets", "surface pro", "android tablet", "galaxy tab", "foldable"])],
        "STRONG_INFERENCE": [("form-factor", ["12-inch slate", "slate our", "10-inch", "11-inch", "two-hand", "two hands", "large phone"])],
        "WEAK_INFERENCE": [],
    },
    "desktop": {
        "DIRECT": [("explicit", ["desktop", "on desktop", "desktop app", "desktop application", "desktop client", "desktop inventory client", "desktop tool", "native desktop", "windows app", "windows application", "win32", "macos", "mac app", "menu-bar app", "menu bar app", "electron", "wpf", "winui", "avalonia", "uno platform", "tauri", "system tray", "in the tray", "on macs", "on a mac", "macbook", "on the mac", "for mac"])],
        "STRONG_INFERENCE": [("form-factor", ["workstation", "workstations", "multi-monitor", "multiple monitors", "4k monitor", "operator console", "dispatchers keep open", "trading floor", "windows program", "system tray", "tray icon", "tray flyout", "menu bar has", "the menu bar", "dock icon", "title bar", "second monitor", "two-screen", "torn off into its own window", "own window", "native window", "installer"]),
                             ("os", ["windows", "macos", "linux desktop", "windows and mac", "on windows"]),
                             ("modality", ["keyboard and mouse", "mouse and keyboard", "alt-plus tab", "numeric keypad", "keypad at their desks"])],
        "WEAK_INFERENCE": [("modality", ["right-click", "right click", "context menus", "keyboard accelerators", "accelerators", "laptop", "laptops", "arrow keys", "keyboard shortcut", "keyboard shortcuts", "drag a file", "mouse", "ctrl-plus", "cmd-plus", "alt-plus", "shift-plus"]),
                           ("form-factor", ["window", "the window", "resize the window", "resizing the window", "monitor", "monitors", "panel disappears", "explorer", "desktops", "at their desks", "at the desk"]),
                           ("environment", ["analysts", "traders", "dispatchers", "clerks", "accountants", "support agents", "photographers cull"]),
                           ("product", ["program", "order-entry program", "spreadsheet", "installer", "inspector panel", "second one"])],
    },
    "kiosk": {
        "DIRECT": [("explicit", ["kiosk", "kiosks", "self-service terminal", "self-checkout", "self checkout", "point of sale", "point-of-sale", "pos terminal", "pos screen", "vending", "public display", "digital signage", "ticket machine", "check-in terminal", "check in terminal", "wayfinding"])],
        "STRONG_INFERENCE": [("form-factor", ["fixed touch screen", "fixed touchscreen", "standing terminal", "counter screen", "customer-facing screen", "wall-mounted panel", "self-service screen", "public sign-in station", "sign-in station", "visitor terminal", "ticket terminal", "check-in screen", "unattended touch display", "public catalogue terminal", "pay station", "ticket machine at"]),
                             ("environment", ["in the lobby", "clinic lobby", "hotel lobby", "at the station", "in the store", "in-store", "shopping centre", "shopping center", "public terminal", "public check-in", "visitor sign-in", "bolted to the wall", "factory floor", "hmi panel", "hmi", "check-in display", "check in display"]),
                             ("form-factor", ["terminal", "32-inch", "touch-screen windows", "touchscreen windows", "touch terminal"])],
        "WEAK_INFERENCE": [("environment", ["large wall display", "wall display", "with gloves", "gloves", "warehouse terminal", "rugged terminal", "reception", "at reception", "foyer", "at the counter", "at the till", "the till", "queue builds", "the queue", "queue at", "car park", "museum", "walk up to", "at the stop", "by the door", "unattended", "in the mail room", "mail room", "at the gate", "lane", "lanes", "lobby", "checkout counter", "checkout counters", "checkout lane", "vehicle-display"]),
                           ("product", ["self-service", "check in", "check-in", "checks in", "ticket", "tickets", "badge", "locker pickup", "loyalty number", "customer-facing", "for the next person", "next person", "everyone shares", "shared touch screen", "print their badge", "buy a ticket", "vending-style", "pickup"]),
                           ("modality", ["tap their order", "tap an exhibit", "touch screen", "touchscreen", "touch display", "keypad"]),
                           ("form-factor", ["machine", "terminal", "screen at the", "screen by the", "screen at", "panel with gloves", "the screen in the"])],
    },
    "web": {
        "DIRECT": [("explicit", ["web", "website", "web app", "webapp", "web application", "browser", "browsers", "chrome", "safari", "firefox", "edge browser", "html", "css", "dom", "spa", "pwa", "progressive web app", "webview", "web view", "landing page", "marketing site", "intranet", "site"])],
        "STRONG_INFERENCE": [("stack", ["react", "next.js", "nextjs", "vue", "nuxt", "svelte", "angular", "astro", "tailwind", "shadcn", "htmx"]),
                             ("product", ["portal", "customer portal", "storefront", "online store", "web store", "blog", "chromebook", "embeddable widget", "partner sites", "saas admin", "admin panel", "admin dashboard", "back office", "backoffice", "reporting tool", "intranet page"])],
        "WEAK_INFERENCE": [("product", ["saas", "b2b saas", "dashboard for", "admin", "laptop", "laptops", "the link", "link from the email", "url", "share link", "search engines", "cookie banner", "print", "printed"]),
                           ("runtime", ["browser tab", "new tab", "the page", "page jumps", "anchor target", "sticky header", "sidebar squeezes", "zooming to 200%", "200% zoom", "back button in the", "embeddable", "partners drop into"]),
                           ("form-factor", ["laptops and", "smaller phone screens", "phones and laptops", "laptops and phones", "small screens", "phones and desktops", "desktop and phone", "desktop and mobile", "mobile and desktop"]),
                           ("product", ["banner", "a link", "follow a link", "the email", "newsletter"])],
    },
}
STRENGTH_ORDER = {"DIRECT": 3, "STRONG_INFERENCE": 2, "WEAK_INFERENCE": 1, "NONE": 0}
# an exclusive device platform wins over a framework/OS-derived one
DEVICE_TYPES = {"explicit", "environment", "form-factor", "modality", "product"}
FRAMEWORK_TYPES = {"stack", "os"}
INPUT_EVIDENCE = {"touch": ["touch input", "touch screen", "touchscreen", "touch-screen", "with gloves", "gloves", "tap", "swipe", "one thumb", "thumb"],
                  "remote": ["remote", "d-pad", "dpad", "controller", "arrow keys on the remote", "leanback", "focus traversal"],
                  "keyboard": ["keyboard", "shortcuts", "accelerators", "hotkeys"], "pointer": ["mouse", "trackpad", "right-click", "hover"]}
_PLATFORM_NEGATIONS = ["no mobile support", "not mobile", "desktop browser only", "no phone support", "not for phones"]
_NOT_A_BROWSER = ["media browser", "file browser", "photo browser", "content browser", "catalogue browser", "catalog browser", "asset browser", "product browser"]


_PLATFORM_TRAPS = [
    (r"\bremote(?:ly)?[- ](?:office|offices|team|teams|work|working|workers|worker|employees|staff|branch|branches|config\w*|access|desktop|server|servers|session|sessions|support|debugging|login|logins|colleagues|first)\b", " telework "),
    (r"\bremote into\b|\bremotes? in(?:to)?\b", " telework "), (r"\bcontrol[- ]room\b", " operations-room "),
    (r"\bterminal (?:output|window|emulator|session|command|commands|log|logs)\b|\bin the terminal\b|\bcommand[- ]line\b|\bshell\b", " console "),
    (r"\bkiosk mode\b", " fullscreen mode "), (r"\btablets? of\b|\btablets? (?:per|a day|daily)\b", " pills of "),
    (r"\bcouch[- ]to[- ]5k\b|\bcouch potato\b", " running-plan "), (r"\bphone (?:number|numbers|call|calls|line|lines|book)\b|\btelephone\b", " telephone-number "),
    (r"\bwindows? (?:in|of|on) the (?:dashboard|layout|app|page|screen|editor)\b", " panes in the layout "), (r"\bwindow (?:function|functions|of time)\b", " period "),
    (r"\bbig screen or small\b|\bsmall screen or big\b", " any size "), (r"\bsmart fridge\b|\bfridge screen\b", " appliance screen "),
    (r"\bmobile (?:safari|chrome|browser|emulation|viewport)\b", " narrow-browser "), (r"\bin-flight\b|\bseatback\b", " seat-display "),
    (r"\bcar dashboard\b|\bin-car\b|\binfotainment\b", " vehicle-display "),
    (r"\bmedia browser\b|\bfile browser\b|\bphoto browser\b|\basset browser\b", " media explorer "),
    (r"\bon[- ]site\b|\bsite visits?\b|\bconstruction site\b|\bjob site\b|\bcustomer site\b|\bthe site has\b|\bsite has no\b|\bat the site\b|\bwhen the site\b|\bsite (?:engineer|manager|crew|team)s?\b", " premises "),
    (r"\btv (?:listings?|guide page|programmes?|programs?|shows?|schedule|channels? page|section|news)\b", " televisioncontent "),
    (r"\bdesktop (?:layout|breakpoint|viewport|version|view|size|width|widths|grid)\b", " wide-layout "),
    (r"\b(ctrl|cmd|alt|shift|command|option)\+", r"\1-plus "),
]


def neutralize_platform_traps(text: str) -> str:
    """Words that look like platform evidence but are not (remote work, shell terminals, kiosk mode, pills, couch-to-5k...)."""
    for pat, repl in _PLATFORM_TRAPS:
        text = re.sub(pat, repl, text)
    return text


# evidence families: clues in the same family are one clue (sofa / couch / living room), clues from different
# independent families combine (Phase 6 compound inference)
EVIDENCE_FAMILY = {"explicit": "explicit", "stack": "runtime", "os": "runtime", "environment": "environment", "modality": "input",
                   "form-factor": "form-factor", "product": "product", "distance": "distance", "repository": "repository"}


def _evidence_families(evidence: list[dict]) -> set[str]:
    """Distinct evidence families, counting one clue once: phrases that share a stem (gloves / with gloves on)
    or contain one another are the same clue and only keep their first family."""
    seen_stems: dict[str, str] = {}
    fams: set[str] = set()
    for e in evidence:
        stem = re.sub(r"[^a-z]", "", e["phrase"].split()[-1] if e["phrase"].split() else e["phrase"])[:5]
        fam = EVIDENCE_FAMILY.get(e["type"], e["type"])
        if stem in seen_stems and seen_stems[stem] != fam:
            continue
        seen_stems.setdefault(stem, fam)
        fams.add(fam)
    return fams


def resolve_platform(query: str, project_platforms: list[str] | None = None) -> dict:
    """Typed, graded platform evidence -> candidates -> resolution. Returns
    {"candidates": [...], "resolved": {platform: {"status": KNOWN|INFERRED, "strength", "reason"}}, "unknown": bool,
     "weak_only": [...], "inputs": {...}, "negated": [...]}"""
    text = " " + query.lower().replace("_", " ") + " "
    text = neutralize_platform_traps(text)
    for phrase in _NOT_A_BROWSER:
        text = text.replace(phrase, phrase.replace("browser", "explorer"))
    text = re.sub(r"react[- ]native", "reactnative", text)
    desktop_web = bool(re.search(r"desktop (?:web|browser|site|version of the site)", text))
    if desktop_web:
        text = re.sub(r"\bdesktop (?=web|browser|site|version)", "wide-screen ", text)
    cands: dict[str, dict] = {}
    for plat, groups in PLATFORM_EVIDENCE.items():
        for strength, entries in groups.items():
            for etype, phrases in entries:
                hits = _count(text, phrases)
                if not hits:
                    continue
                c = cands.setdefault(plat, {"platform": plat, "evidence": [], "strength": "NONE"})
                for h in hits:
                    c["evidence"].append({"type": etype, "phrase": h, "strength": strength})
                if STRENGTH_ORDER[strength] > STRENGTH_ORDER[c["strength"]]:
                    c["strength"] = strength
    if _count(text, ["companion app", "companion phone app", "remote control app", "second-screen app", "second screen app"]):
        for plat in list(cands):
            if plat != "mobile" and not _count(text, ["on phones", "on the phone", "and phones"] if plat == "web" else []):
                cands.pop(plat, None) if plat in ("kiosk", "tv", "desktop") else None
    multi_device = _count(text, ["phones and laptops", "laptops and phones", "laptops and smaller", "smaller phone screens", "phone screens", "phones and desktops", "desktop and phone", "desktop and mobile", "mobile and desktop", "from laptops", "on laptops and"])
    if multi_device and "mobile" in cands and all(e["phrase"] in ("phone", "phones", "mobile", "smartphone", "smartphones") for e in cands["mobile"]["evidence"] if e["strength"] == "DIRECT"):
        cands["mobile"]["strength"] = "WEAK_INFERENCE"
        for e in cands["mobile"]["evidence"]:
            e["strength"] = "WEAK_INFERENCE"
        w = cands.setdefault("web", {"platform": "web", "evidence": [], "strength": "NONE"})
        w["evidence"].append({"type": "form-factor", "phrase": multi_device[0], "strength": "STRONG_INFERENCE"})
        if STRENGTH_ORDER["STRONG_INFERENCE"] > STRENGTH_ORDER[w["strength"]]:
            w["strength"] = "STRONG_INFERENCE"
    negated = _count(text, _PLATFORM_NEGATIONS)
    if negated:
        for plat in ("mobile",):
            if plat in cands and all(e["type"] in ("explicit",) and e["phrase"] in ("phone", "phones", "mobile") for e in cands[plat]["evidence"]):
                cands.pop(plat)
    # device platforms named directly suppress framework/OS-only candidates of other platforms
    device_direct = {p_ for p_, c in cands.items() if any(e["strength"] == "DIRECT" and e["type"] in DEVICE_TYPES for e in c["evidence"])}
    strong_device = {p_ for p_, c in cands.items() if any(e["strength"] == "STRONG_INFERENCE" and e["type"] in ("environment", "form-factor", "modality") for e in c["evidence"])}
    resolved: dict[str, dict] = {}
    weak_only: list[str] = []
    for plat, c in cands.items():
        best = c["strength"]
        types = {e["type"] for e in c["evidence"] if e["strength"] == best}
        if best == "DIRECT":
            # "android app for a television": explicit OS-app wording loses to an explicit device platform
            if plat == "mobile" and (device_direct - {"mobile"}) & {"tv", "kiosk", "desktop"} and all(e["phrase"] in ("android app", "android phone", "ios", "mobile") for e in c["evidence"] if e["strength"] == "DIRECT") and not _count(text, ["on phones", "and phones", "phones and", "on the phone"]):
                weak_only.append(plat); continue
            if plat == "web" and (device_direct - {"web"}) & {"tv", "kiosk"} and types <= {"stack"}:
                weak_only.append(plat); continue
            resolved[plat] = {"status": "KNOWN", "strength": best, "reason": "request: " + ", ".join(dict.fromkeys(e["phrase"] for e in c["evidence"] if e["strength"] == best))}
        elif best == "STRONG_INFERENCE":
            if types <= FRAMEWORK_TYPES and ((device_direct | strong_device) - {plat}):
                weak_only.append(plat); continue  # framework evidence is not enough when a device platform is evident
            resolved[plat] = {"status": "INFERRED", "strength": best, "reason": "inferred (" + ", ".join(sorted(types)) + "): " + ", ".join(dict.fromkeys(e["phrase"] for e in c["evidence"] if e["strength"] == best))}
        else:
            families = _evidence_families(c["evidence"])
            competing = {p_ for p_, o in cands.items() if p_ != plat and STRENGTH_ORDER[o["strength"]] >= STRENGTH_ORDER["STRONG_INFERENCE"]}
            if plat in ("kiosk", "tv"):
                competing -= {"web"}   # web technology is the substrate of a kiosk / TV screen
            weak_rivals = {p_ for p_, o in cands.items() if p_ != plat and o["strength"] == "WEAK_INFERENCE" and len(_evidence_families(o["evidence"])) >= 2}
            if len(families) >= 2 and not competing and not weak_rivals and plat not in ("tablet",):
                c["strength"] = "STRONG_INFERENCE"; c["compound"] = sorted(families)
                resolved[plat] = {"status": "INFERRED", "strength": "STRONG_INFERENCE", "compound": sorted(families),
                                  "reason": "compound inference (" + ", ".join(sorted(families)) + "): " + ", ".join(dict.fromkeys(e["phrase"] for e in c["evidence"]))}
            else:
                weak_only.append(plat)
    if "desktop" in resolved and _count(text, ["electron", "tauri", "webview", "web view", "wrapped for the desktop"]) and "web" in cands and "web" not in resolved:
        resolved["web"] = {"status": "INFERRED", "strength": "STRONG_INFERENCE", "reason": "web technology inside a desktop shell (" + ", ".join(dict.fromkeys(e["phrase"] for e in cands["web"]["evidence"])) + ")"}
        weak_only = [w for w in weak_only if w != "web"]
    # a WEAK candidate alone stays unknown; with a resolved platform present, weak candidates are dropped
    unknown = not resolved and not (project_platforms or [])
    inputs = {i: _count(text, ph) for i, ph in INPUT_EVIDENCE.items()}
    return {"candidates": [{"platform": p_, "strength": c["strength"], "evidence": c["evidence"][:6]} for p_, c in sorted(cands.items(), key=lambda kv: -STRENGTH_ORDER[kv[1]["strength"]])],
            "resolved": resolved, "unknown": unknown, "weak_only": [w for w in weak_only if w not in resolved], "inputs": {k: v for k, v in inputs.items() if v}, "negated": negated}


# ---------------------------------------------------------------------------
# Scope / domain model (deterministic). Activation is a separate, frozen proxy; this is internal scope.
# ---------------------------------------------------------------------------
DOMAINS = ["UI_DESIGN", "UI_INTERACTION", "UI_ACCESSIBILITY", "UI_IMPLEMENTATION", "FRONTEND_RUNTIME",
           "BACKEND", "DATA", "INFRASTRUCTURE", "BUILD_TOOLING", "UNKNOWN"]

_TECH = {
    "FRONTEND_RUNTIME": ["re-render*", "rerender*", "usestate", "throws an exception", "throws on", "throws when", "useeffect", "usememo", "hook", "hooks", "state update", "state management",
                         "redux", "zustand", "signal", "hydration", "hydration mismatch", "hydrate", "mutation", "api call", "promise", "async", "race condition", "memory leak",
                         "exception", "undefined is not", "null reference", "crash", "stack trace", "event loop", "websocket", "polling", "cache invalidation", "query key"],
    "BACKEND": ["endpoint", "api", "rest", "graphql", "returns 500", "500", "404", "server error", "controller", "service layer", "jwt", "token refresh", "refresh the jwt",
                "oauth", "session cookie", "auth server", "rate limit", "webhook", "microservice", "backend", "server-side", "cron", "queue worker", "payments service", "api keys", "rotate"],
    "DATA": ["database", "sql", "postgres", "mysql", "sqlite", "add an index", "database index", "sql index", "query plan", "db migration", "database migration", "schema", "prisma", "orm", "etl", "data pipeline", "etl pipeline", "warehouse", "data model", "table schema", "timing out", "query stops"],
    "INFRASTRUCTURE": ["deploy", "deployment", "kubernetes", "k8s", "docker", "terraform", "aws", "azure", "gcp", "cdn config", "dns", "ssl", "certificate", "play console", "app store connect", "upload the apk", "sign the apk", "apk", "aab", "ipa", "app bundle", "signing", "signing key", "provisioning", "release pipeline", "testflight"],
    "BUILD_TOOLING": ["webpack", "vite", "rollup", "esbuild", "turbopack", "bundle size", "tree-shake", "tree shake", "treeshake", "purge", "purgecss", "css build", "build is slow", "build time",
                      "storybook", "eslint", "prettier", "stylelint", "lint", "type error", "typescript error", "tsconfig", "babel", "postcss", "sass compile", "compile", "css modules",
                      "monorepo", "turborepo", "nx", "jest", "vitest", "playwright tests", "flaky", "in ci", "ci pipeline", "github actions", "pipeline fails", "source map", "hot reload", "hmr", "dependency upgrade", "webpack upgrade", "gradle sync", "pod install", "package", "fails to start", "production build", "in production"],
}
# symptoms that are UX-visible even when the cause is technical: the skill has something to contribute
_UX_SYMPTOMS = ["freezes", "freeze", "janky", "jank", "stutter*", "feels slow", "slow to use", "laggy", "lag when", "scroll", "scrolling", "layout shift", "cls", "lcp", "jumps",
                "flicker", "flash of", "loses focus", "lose focus", "focus", "screen reader", "voiceover", "talkback", "narrator", "announces", "announce", "keyboard",
                "loading state", "loading-state", "skeleton", "spinner", "empty state", "session expires", "lose the form", "lose their", "lose your", "lose an unsaved", "unsaved", "users", "customers", "clipped", "overflow", "breaks at", "responsive",
                "nothing tells", "never says", "can't tell", "cannot tell", "barely visible", "hard to see", "can't see", "cannot see", "too fast to", "flies past", "tiny thumbnail*", "can't get to", "cannot get to",
                "what is happening", "what's happening", "see which", "at a glance", "without opening each", "how long each", "keep typing", "keeps typing", "wrong column", "time out", "times out", "before they finish",
                "stands out", "same weight", "hard to find", "can't find", "cannot find", "drop off", "gives no sign", "no sign", "no indication", "nothing happens", "cropped", "cut off", "too wide", "off screen", "off-screen",
                "trapped", "cannot be dismissed", "flush together", "look identical", "looks identical", "indistinguishable", "queasy", "throws the changes away", "throws away", "loses everything", "loses", "lost", "no way back", "no way to",
                "confusing", "don't know what", "unsure which", "takes forever", "presses before", "too small", "tiny", "too heavy", "misaligned", "wrap", "wraps", "spinning circle", "spinning", "runs for a minute", "pick one", "people on the", "customers at the",
                "readable", "unreadable", "hard to read", "cannot read", "can't read", "can't tell", "cannot tell", "hidden behind", "covers", "overlaps", "off the edge", "cut in half", "squeezes", "cannot be turned on", "can't be turned on", "hard to edit", "scroll past", "in one wall", "one wall", "walks through", "autoplays", "with sound"]
_UI_WORDS = ["ui", "ux", "screen*", "page*", "layout*", "design*", "button*", "modal*", "dialog*", "form", "forms", "table*", "grid*", "list", "lists", "card*", "hero", "navigation", "nav", "menu*", "tab", "tabs", "icon*",
             "board", "front desk", "chip", "chips", "spinner", "thumbnail*", "photo*", "sheet", "chooser", "picker", "toolbar", "sync status", "language switch", "summary card", "status bar", "banner", "badge*", "tile*",
             "overview", "pricing", "plan*", "field*", "row*", "column*", "header*", "footer", "sidebar", "panel*", "pane*", "avatar*", "shadow*", "corner*", "font*", "typeface", "heading*", "label*", "tooltip*", "toast*", "overlay*", "modal*", "dialog*", "widget*", "filter*", "step*", "wizard", "export button", "the app", "our app", "the site",
             "subtitle*", "caption*", "line item*", "editor", "the cast", "attract loop", "promo", "workspace", "billing", "members", "usage page", "quota",
             "colour*", "color*", "theme*", "dark mode", "typography", "font*", "spacing", "contrast", "focus*", "accessib*", "a11y", "wcag", "responsive", "breakpoint*", "viewport",
             "component*", "toast*", "banner*", "dashboard*", "checkout", "onboarding", "settings", "player", "rail*", "epg", "kiosk*", "loading", "empty state", "visual*", "css grid", "css", "screenshot*", "mockup*", "wireframe*",
             "flow", "flows", "wizard*", "sidebar*", "drawer*", "tooltip*", "chart*", "kpi*", "widget*", "label*", "placeholder*", "keyboard", "d-pad", "dpad", "remote", "touch", "gesture*", "scroll*", "hover", "animation*", "motion", "brand*", "logo*", "hierarchy", "readab*", "legib*", "cluttered", "cramped",
             "panel*", "tree", "row", "rows", "column*", "report*", "numbers", "view", "section*", "cell*", "field*", "control*", "badge*", "strip", "header*", "footer*", "guide", "rail", "tile*", "picker*", "dropdown*", "checkbox*", "toggle*", "slider*", "spinner*", "skeleton*", "highlight*", "selection", "selected", "step*", "onboarding", "search*", "filter*", "sort*", "pagination", "infinite scroll", "spacing", "alignment", "aligned", "font*", "icon*", "image*", "photo*", "thumbnail*", "poster*"]
_NO_VISUAL = ["no visual changes", "no visual change", "mechanically", "without changing the ui", "no ui changes", "purely technical"]
_DECISIVE_TECH = {
    "DATA": ["sql", "database", "postgres", "prisma", "db migration", "database migration", "migration", "migrations", "shard", "sharding", "multi-tenancy"],
    "BACKEND": ["endpoint", "returns 500", "returns 404", "500 error", "jwt", "rotate the api keys", "api key rotation", "worker", "cron", "nightly job", "lock is not released"],
    "INFRASTRUCTURE": ["kubernetes", "docker", "terraform", "ci pipeline", "github actions"],
    "BUILD_TOOLING": ["webpack", "vite config", "tree-shake", "tree shake", "eslint", "bundle size", "npm audit", "dependency upgrade", "play console", "app store connect", "apk"],
    "FRONTEND_RUNTIME": ["hydration mismatch", "throws an exception", "throws on", "throws when", "throws null", "exception", "null reference", "null collection", "stack trace", "segfault", "memory leak", "unit test*", "mock the"],
}
_A11Y = ["accessib*", "a11y", "wcag", "screen reader", "voiceover", "talkback", "narrator", "aria", "contrast", "keyboard users", "focus order", "reduced motion", "labels"]
_INTERACTION = ["focus", "keyboard", "tap", "click", "gesture", "swipe", "drag", "hover", "d-pad", "dpad", "remote", "scroll", "loses", "lose", "miss", "respond", "shortcut", "select", "feels slow", "slow to", "waiting", "wait for", "laggy"]
_IMPLEMENTATION = ["css", "grid breaks", "breaks at", "px", "virtualize", "virtualise", "component", "render", "implement", "markup", "html", "tailwind", "styles", "stylesheet", "cls", "lcp", "layout shift"]


def _count(text: str, phrases) -> list[str]:
    """Word-bounded phrase hits; a trailing '*' allows any suffix (accessib* matches accessibility)."""
    hits = []
    for p in phrases:
        if p.endswith("*"):
            pat = r"(?<![a-z0-9])" + re.escape(p[:-1])
        else:
            pat = r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])"
        if re.search(pat, text):
            hits.append(p.rstrip("*"))
    return hits


def classify_scope(query: str, ui_signal: int = 0, has_project: bool = False) -> dict:
    """Domain + in-scope decision with a reason. `ui_signal` = count of lexicon UI evidence (modes,
    components, screens, platforms, problems) computed by the requirements layer."""
    text = " " + query.lower() + " "
    tech = {d: _count(text, ph) for d, ph in _TECH.items()}
    ui_hits = list(dict.fromkeys(h.rstrip("*") for h in _count(text.replace("-", "+"), _UI_WORDS))) + [f"concept:{c}" for c in alias_concepts(query)][:3]
    decisive = []
    for dom, ph in _DECISIVE_TECH.items():
        hits = _count(text, ph)
        if hits:
            decisive += hits
            tech.setdefault(dom, []).extend(h for h in hits if h not in tech.get(dom, []))
    ux = _count(text, _UX_SYMPTOMS)
    no_visual = _count(text, _NO_VISUAL)
    eng = _count(text, ["virtualize", "virtualise", "virtualized", "memoize", "memoise", "debounce", "throttle", "lazy-load", "lazy load", "code-split", "code split", "cache", "caching", "profile", "profiling", "render pipeline", "reflow", "repaint", "gpu"])
    if eng:
        tech.setdefault("FRONTEND_RUNTIME", []).extend(eng)
    tech_best = max(tech, key=lambda d: (len(tech[d]), -DOMAINS.index(d)))
    tech_score = sum(len(v) for v in tech.values())
    ui_score = len(ui_hits) + ui_signal
    reason, nearest, kind = "", None, "in-scope"
    if no_visual:
        domain, in_scope = ("BUILD_TOOLING" if tech_score else "UI_IMPLEMENTATION"), False
        reason = "explicitly non-visual / mechanical change"
        nearest = "visual verification after the migration"
    elif tech_score and not ux and (decisive or (tech_score >= ui_score and (ui_score <= 1 or tech_score >= 2))):
        domain, in_scope = tech_best, False
        reason = f"not a UI design task: {tech_best.lower().replace('_', ' ')} work ({', '.join(tech[tech_best][:3])}) without a UI design, interaction or accessibility requirement"
        nearest = {"FRONTEND_RUNTIME": "the UI states and feedback around this behaviour", "BACKEND": "the screen that consumes this endpoint",
                   "DATA": "the table or dashboard that shows this data", "INFRASTRUCTURE": "none", "BUILD_TOOLING": "visual verification after the tooling change"}[tech_best]
    elif tech_score and ux:
        # technical cause, UX-visible symptom: the skill contributes the UX side (PARTIAL scope)
        domain = "UI_ACCESSIBILITY" if _count(text, _A11Y) else ("UI_INTERACTION" if _count(text, _INTERACTION) else "UI_IMPLEMENTATION")
        in_scope = True
        kind = "partial"
        reason = f"technical cause ({', '.join(tech[tech_best][:2])}) with a user-visible symptom ({', '.join(ux[:2])}); design-engineering contributes the UX side"
        nearest = f"design-engineering contribution: the user-facing states, responsiveness and feedback around '{ux[0]}'; non-design portion: {tech_best.lower().replace('_', ' ')} work ({', '.join(tech[tech_best][:2])}) belongs to the engineering side"
    elif ui_score == 0 and not ux and has_project and not tech_score:
        domain, in_scope = "UI_DESIGN", True
        reason = "repository context: no technical vocabulary, so the request concerns the project's user interface"
    elif ui_score == 0 and not ux:
        domain, in_scope, reason = "UNKNOWN", False, "no UI vocabulary found; not a UI design task as written"
        nearest = "describe the screen, component, or user-facing problem"
    else:
        in_scope = True
        if _count(text, _A11Y):
            domain = "UI_ACCESSIBILITY"
        elif _count(text, _INTERACTION):
            domain = "UI_INTERACTION"
        elif _count(text, _IMPLEMENTATION) and not _count(text, ["design", "look", "layout", "hierarchy", "brand", "polish"]):
            domain = "UI_IMPLEMENTATION"
        else:
            domain = "UI_DESIGN"
        reason = "UI design / interaction task"
    if not in_scope:
        kind = "abstain"
    return {"domain": domain, "in_scope": in_scope, "kind": kind, "reason": reason, "nearest_ui_task": nearest,
            "evidence": {"ui": ui_hits[:6], "ux_symptoms": ux[:4], "technical": {d: h[:4] for d, h in tech.items() if h}, "non_visual": no_visual}}


# ---------------------------------------------------------------------------
# Task-intent model: what the user says -> what operation is needed. Cues work in combination.
# ---------------------------------------------------------------------------
_EXISTING = ["our", "this", "these", "current", "currently", "existing", "keeps", "keep", "keeping", "still", "when", "after", "sometimes", "again", "the selected", "the layout", "the sidebar",
             "users", "customers", "clerks", "people", "already", "we have", "we've got", "in production", "on the", "of the", "without changing", "without redesigning", "matching the", "consistent with", "in its", "its existing", "the app's"]
_PROBLEM = ["hard to", "cannot", "can't", "cant", "can not", "confusing", "confused", "misaligned", "lost", "lose", "loses", "losing", "clipped", "clip", "overflows", "overflow", "doesn't", "does not", "don't",
            "fails", "fail", "failing", "too dense", "too slow", "too small", "too big", "too many", "tiring", "cluttered", "cramped", "miss", "misses", "missing", "abandon", "skips", "skip",
            "wrong", "broken", "breaks", "break", "invisible", "unreadable", "hard to read", "twice", "complain", "complaints", "hate", "annoying", "inconsistent", "shifts", "jumps",
            "doesn't respond", "not respond", "unresponsive", "what is wrong", "whats wrong", "what's wrong", "feels", "looks off", "looks wrong", "looks generic", "looks dated", "abandons"]
_CHANGE = ["fix", "improve", "refactor", "simplify", "polish", "clean up", "cleanup", "tighten", "make this", "make the", "make our", "make it", "streamline", "declutter", "rework", "restructure", "reorganise", "reorganize", "modernise", "modernize", "less tiring", "easier to"]
_CREATE = ["create", "build", "design a", "design an", "design the", "new screen", "new page", "new component", "new flow", "implement", "add a", "add an", "add screen", "add page", "scaffold", "prototype", "from scratch", "greenfield", "mock up", "mockup", "wireframe"]
_ADD_TO_EXISTING = ["add", "adding", "extend", "introduce", "include"]
_DIAGNOSE = ["review", "audit", "assess", "evaluate", "critique", "what is wrong", "what's wrong", "find problems", "find issues", "check this", "check the", "check our", "check whether", "score this", "rate this"]
_NO_CHANGE = ["don't change code", "do not change code", "without changing code", "no code changes", "don't change anything", "without modifying", "review only", "just review", "only review", "report only"]
_REDESIGN = ["redesign", "from scratch", "rebuild", "reimagine", "overhaul", "start over", "new information architecture", "redesign the information architecture"]
_LOOKFEEL = ["look", "looks", "feel", "feels", "premium", "professional", "cluttered", "cramped", "spacing", "visual", "polish", "tiring to scan", "generic", "dated", "inconsistent", "alignment", "aligned", "colour", "color", "typography", "font"]
_STRUCTURAL = ["simplify", "restructure", "reorganise", "reorganize", "rework", "consolidate", "refactor", "information architecture", "navigation", "layout", "flow", "hierarchy", "streamline", "declutter", "shortcuts", "shortcut"]
_RESPONSIVE = ["resize", "resized", "below", "px", "breakpoint", "viewport", "window", "narrow window", "narrow screen", "narrower", "small screen", "mobile layout", "clipped", "overflow", "reflow", "orientation", "landscape", "portrait", "on phones", "on a phone", "tablet"]
_PRESERVE = ["keep the existing", "keep existing", "keep our", "keeping the", "keeping our", "keeping its", "keeping", "without changing", "without redesigning", "don't change", "do not change", "preserve", "leave the", "keep the", "keep its",
             "matching the existing", "consistent with the existing", "consistent with the rest", "in its existing style", "in the existing style", "in the app's existing", "existing style", "same style as", "without touching"]
_PRESERVE_TARGETS = {"navigation": ["navigation", "nav", "sidebar", "menu", "tabs", "top bar", "topbar", "rail", "home layout", "flow", "pick-up flow", "shell"], "typography": ["typography", "font", "fonts", "type"],
                     "color": ["colour", "color", "theme", "palette", "light theme", "dark theme", "brand colours", "brand colors"],
                     "layout": ["layout"], "behaviour": ["how it works", "behaviour", "behavior", "functionality", "code", "flow"],
                     "system": ["style", "styling", "look", "design language", "design system", "pages", "rest of the", "existing pages", "existing screens", "the rest"]}
_PRESERVE_WORDS = r"(?:keep(?:ing)?(?: the)?(?: existing| our| current| its| the app's)?|without (?:changing|redesigning|touching)(?: the| its| our)?|don't change(?: the| its)?|do not change(?: the| its)?|preserve(?: the)?|leave the|matching the(?: existing)?|consistent with the(?: existing| rest of the)?|in (?:its|the)(?: app's)? existing|same style as)"
_A11Y_FACET = ["screen reader", "voiceover", "talkback", "narrator", "accessib", "a11y", "wcag", "aria", "contrast", "keyboard users", "reads", "announce", "skips the"]
_INTERACTION_FACET = ["focus", "keyboard", "button", "click", "tap", "select", "selected", "respond", "miss", "misses", "continue", "dialog", "modal", "shortcut", "gesture", "swipe", "scroll", "drag"]


ARTIFACT_STATES = {"new", "existing", "unknown"}
OPERATIONS = ["create", "inspect", "diagnose", "modify", "polish", "restructure", "redesign", "compare", "review", "validate"]
PROBLEM_DOMAINS = ["accessibility", "interaction", "navigation", "responsive", "performance-ux", "layout", "visual", "brand", "design-system", "content"]
CHANGE_SCOPES = ["local", "screen", "flow", "system", "unknown"]

_DOMAIN_CUES = {
    "accessibility": ["screen reader*", "voiceover", "talkback", "narrator", "accessib*", "a11y", "wcag", "aria", "colour-blind", "color-blind", "colourblind", "colorblind", "keyboard user*", "keyboard-only", "keyboard only", "focus order", "reduced motion", "200% zoom", "zoom", "contrast", "announce*", "required marker*", "assistive", "tab stops", "barely visible", "hard to see", "can't see", "cannot see", "invisible", "before they finish", "older customers", "older users", "elderly", "from the sofa", "from a distance"],
    "interaction": ["focus*", "select*", "tap*", "click*", "keyboard", "button*", "respond*", "trapped", "stuck", "drag*", "back button", "controls", "gesture*", "swipe*", "scroll*", "highlight*", "hover", "dialog*", "modal*", "picker", "menu*", "toggle*", "input*", "save takes", "takes three taps", "times out", "keypad", "shortcut*", "remote", "forget*", "what you typed", "typed", "typing", "keep typing", "wrong column", "go back", "goes back", "undo", "state is lost", "unsaved", "lose an unsaved", "lose their edits", "lose your edits", "clicking another", "drag*", "chooser", "sheet"],
    "navigation": ["find*", "way back", "breadcrumb*", "menus deep", "navigat*", "lost", "lose their place", "which section", "export option", "next step", "what to do next", "route*", "back out", "deep", "sitemap"],
    "visual": ["visible", "invisible", "look*", "noisy", "colour*", "color*", "contrast", "alignment", "align*", "line up", "sizes", "shout*", "identical", "indistinguishable", "muddy", "faint", "blend*", "highlight*", "read*", "unreadable", "template", "polish", "tidy", "tidy-up", "spacing", "typograph*", "font*", "icon*", "cramped", "cluttered", "noisy", "premium", "dated", "generic"],
    "layout": ["equal importance", "scan*", "hierarchy", "layout*", "below the fold", "covers", "cover", "buried", "too much", "sections", "arrangement", "density", "dense", "sparse", "structure", "restructure", "break*", "overflow*", "stack up", "pushes", "takes over", "hides the", "cut off", "clipped", "collide*", "overlap*", "far away", "far from", "appear far"],
    "responsive": ["on phones", "on the phone", "on a phone", "narrow window*", "narrow screen*", "narrower", "small screen*", "small window*", "smaller screen*", "resize*", "squeezed", "zoom", "tablet*", "two hands", "horizontal scroll*", "breakpoint*", "viewport*", "window*", "laptop*", "clipped", "overflow*", "mobile version", "responsive", "orientation", "landscape", "portrait"],
    "performance-ux": ["slow*", "blank", "jump*", "loading", "spinner*", "shift*", "second*", "freez*", "stutter*", "lag*", "load*", "wait*"],
    "brand": ["brand*", "identity", "identical apart from", "tier*", "reseller", "white-label", "white label", "skin"],
    "design-system": ["token*", "theme*", "dark mode", "dark variant", "different sizes", "nine different", "inconsistent", "mean different things", "every page", "across the app", "design system", "type scale", "primary button changes", "components library", "icons mean"],
    "content": ["label*", "copy", "wording", "message*", "text", "instructions", "microcopy", "empty cart page", "error page", "placeholder*", "language", "spanish", "french", "german", "arabic", "translation*", "translate*", "locale*", "localis*", "localiz*", "multilingual", "wording", "copy"],
}
_EXISTING_CUES = ["our", "this", "these", "the existing", "existing", "current", "currently", "legacy", "old", "keeps", "keep", "keeping", "still", "again", "already", "in production", "the app's", "its", "we have", "we've got",
                  "to the", "to our", "into the", "into our", "in our", "in the app", "the app", "the tv app", "the site", "the portal", "the tool", "the grid", "the table", "the page", "the screen", "the dashboard", "the checkout", "the player", "the kiosk",
                  "without changing", "without redesigning", "matching the", "consistent with", "in its", "the way it", "as it is", "today", "right now", "at the moment", "users", "customers", "people", "clerks", "viewers", "guests", "staff", "nurses", "couriers", "operators", "visitors", "nobody", "everyone", "shoppers"]
_NEW_CUES = ["new", "brand-new", "brand new", "first version", "green-field", "greenfield", "from scratch", "from the ground up", "entirely new", "a first", "initial version", "v1 of", "prototype", "mvp", "sketch"]
_DEFECT_PATTERNS = [r"\b(?:is|are|looks?|feels?|gets?|seems?|remains?|stays?)\b[^.]*\b(?:hard|difficult|impossible|barely|almost|invisible|too|not|never|wrong|confusing|noisy|cramped|cluttered|unreadable|muddy|identical|indistinguishable|buried|hidden|broken|cut off|clipped|missing|inconsistent|slow|blank|equal|far|different|just|only|squeezed|squashed|tiny|huge|everywhere|deep|awkward|unusable|unclear|off)\b",
                    r"\b(?:can'?t|cannot|can not|don'?t|doesn'?t|never|nobody|no one|keep|keeps|lose|loses|losing|miss|misses|missing|abandon|abandons|get stuck|gets stuck|get trapped|trapped|break|breaks|disappear|disappears|vanish|vanishes|drift|drifts|cover|covers|hide|hides|jump|jumps|stack up|block|blocks|shout|blend|blends|exits|forgets|only show|takes three|times out)\b",
                    r"\b(?:too many|too much|too small|too big|too close|hard to|difficult to|impossible to|far away|out of reach|three menus deep|out of sight)\b"]
_QUESTION_PATTERNS = [r"^\s*(?:why|how|is|are|does|do|should|what'?s wrong|what is wrong|which|can|could|would|where)\b", r"\?\s*$"]
_OP_CUES = {
    "create": ["create", "build", "design a", "design an", "design the", "new screen", "new page", "new component", "new flow", "implement", "add", "add a", "add an", "add screen", "add page", "scaffold", "prototype", "mock up", "mockup", "wireframe", "introduce", "sketch", "first version", "set up", "a first"],
    "inspect": ["inspect", "look at", "have a look", "take a look", "examine"],
    "diagnose": ["why", "what's wrong", "what is wrong", "find problems", "find issues", "audit", "diagnose", "assess", "evaluate", "figure out", "investigate"],
    "modify": ["fix", "improve", "make", "change", "update", "adjust", "correct", "resolve", "repair", "enable", "support", "handle", "ensure", "let ", "allow"],
    "polish": ["polish", "tighten", "refine", "tidy", "tidy-up", "clean up", "cleanup", "refresh the look", "freshen", "modernise the look", "modernize the look", "make it look", "look more", "feel more", "premium", "less tiring", "easier to scan", "less noisy", "visual pass", "spacing", "alignment", "padding", "margins", "align the"],
    "restructure": ["restructure", "reorganise", "reorganize", "rework", "simplify", "streamline", "declutter", "consolidate", "rethink", "regroup", "re-platform", "reflow", "rearrange", "reorder", "move the", "put the", "comes first", "end to end"],
    "redesign": ["redesign", "rebuild", "reimagine", "overhaul", "from scratch", "from the ground up", "start over", "entirely new", "new information architecture", "new look", "revamp"],
    "compare": ["compare", "side by side", "versus", "vs.", "which is clearer", "which hierarchy", "which one", "variants"],
    "review": ["review", "critique", "rate this", "score this", "assess", "sign off", "second opinion", "feedback on", "tell me which", "tell me whether"],
    "validate": ["validate", "check against", "verify", "does this meet", "still work", "good enough", "conform", "compliant", "meets"],
}
_NO_CHANGE = ["don't change code", "do not change code", "without changing code", "no code changes", "don't change anything", "without modifying", "review only", "just review", "only review", "report only", "no changes yet", "no changes", "not change code"]
_SCOPE_CUES = {"system": ["whole product", "entire product", "all three apps", "all apps", "across the app", "across the product", "every page", "every screen", "design tokens", "design system", "token*", "brand*", "architecture", "sitewide", "site-wide", "app-wide", "global", "platform-wide", "everywhere"],
               "flow": ["flow", "journey", "funnel", "end to end", "end-to-end", "onboarding", "checkout", "wizard", "steps", "process"],
               "screen": ["screen", "page", "view", "window", "dashboard", "settings", "home", "list", "detail*", "table", "grid", "guide", "player"],
               "local": ["button*", "tile*", "spacing", "alignment", "label*", "icon*", "badge*", "toast*", "tooltip*", "marker*", "strip", "banner", "row selection", "selected row", "highlight", "keypad", "picker", "control*", "column header*", "breadcrumb", "one field", "a field"]}
_PRESERVE = ["keep the existing", "keep existing", "keep our", "keeping the", "keeping our", "keeping its", "keeping", "without changing", "without redesigning", "don't change", "do not change", "preserve", "leave the", "keep the", "keep its",
             "matching the existing", "consistent with the existing", "consistent with the rest", "in its existing style", "in the existing style", "in the app's existing", "existing style", "same style as", "without touching", "without touching its", "no changes to the"]
_PRESERVE_TARGETS = {"navigation": ["navigation", "nav", "sidebar", "menu", "tabs", "top bar", "topbar", "rail", "home layout", "flow", "pick-up flow", "shell", "workflow"], "typography": ["typography", "font", "fonts", "type"],
                     "color": ["colour", "color", "theme", "palette", "light theme", "dark theme", "brand colours", "brand colors"],
                     "layout": ["layout"], "behaviour": ["how it works", "behaviour", "behavior", "functionality", "code", "flow", "workflow"],
                     "system": ["style", "styling", "look", "design language", "design system", "pages", "rest of the", "existing pages", "existing screens", "the rest"]}
_PRESERVE_WORDS = r"(?:keep(?:ing)?(?: the)?(?: existing| our| current| its| the app's)?|without (?:changing|redesigning|touching)(?: the| its| our)?|don't change(?: the| its)?|do not change(?: the| its)?|preserve(?: the)?|leave the|matching the(?: existing)?|consistent with the(?: existing| rest of the)?|in (?:its|the)(?: app's)? existing|same style as|no changes to the)"
_A11Y_FACET = ["screen reader", "voiceover", "talkback", "narrator", "accessib*", "a11y", "wcag", "aria", "contrast", "keyboard users", "announce", "skips the", "colour-blind", "color-blind", "colourblind", "colorblind"]


def _hits_any(text, phrases):
    return _count(text, phrases)


def domains_probe(text: str) -> list[str]:
    return [d for d, cues in _DOMAIN_CUES.items() if _count(text, cues) and d not in ("content",)]


def task_intent(query: str, lexicon_modes: dict, problems: dict) -> dict:
    """Structural task intent: artifact_state, operations, problem_domain, change_scope, utterance, preserve.
    Cues combine; nothing is decided by one word. Evidence lists are kept for --explain."""
    text = " " + query.lower().replace("_", " ") + " "
    # a screen name such as "Add Habit sheet" / "the new order dialog" is a noun, not a create verb
    _SURF = r"(?:sheet|dialog|screen|page|modal|button|form|panel|view|flow|tab|wizard|popup|drawer)"
    for m in re.finditer(r"\b(?:Add|New|Create|Edit) [A-Z][A-Za-z]+ " + _SURF + r"\b", query):
        text = text.replace(m.group(0).lower(), re.sub(r"^(add|new|create|edit) ", "the ", m.group(0).lower()))
    text = re.sub(r"\b(the|our|this|my) (add|new|create|edit) ([a-z]+ )" + _SURF + r"\b", lambda m: f"{m.group(1)} {m.group(3)}{m.group(0).split()[-1]}", text)
    stripped = re.sub(r"(?:without (?:changing|redesigning|touching)|keeping|keep(?:ing)? the|matching the|consistent with|in (?:its|the)(?: app's)? existing|like the existing|same style as|do not change|don't change|no changes to the)\b.*?(?=\b(?:but|and|while|so that|then)\b|[,.;]|$)", " ", text)
    ops: dict[str, list] = {op: _hits_any(stripped, cues) for op, cues in _OP_CUES.items()}
    ops = {k: v for k, v in ops.items() if v}
    no_change = _hits_any(text, _NO_CHANGE)
    existing_cues = _hits_any(text, _EXISTING_CUES); new_cues = _hits_any(stripped, _NEW_CUES)
    surf = re.search(r"\b(?:the|our|this|these|my) [a-z0-9-]+(?: [a-z0-9-]+)? (?:page|screen|view|table|grid|form|dialog|modal|app|site|dashboard|flow|guide|player|kiosk|list|section|bar|panel|strip|header|footer|menu|picker|banner|widget|card|tile|toolbar|tab|rail|row|editor|wizard|checkout|settings|onboarding|hero|chart|report|detail|record|overview|summary|board|sheet|listing|basket|cart|sidebar|field|button|counter|terminal|grid)\b", stripped)
    if surf and not new_cues:
        existing_cues = existing_cues + [surf.group(0)[:30]]
    defect = [m.group(0).strip()[:40] for pat in _DEFECT_PATTERNS for m in re.finditer(pat, stripped)]
    defect += [h for hs in problems.values() for h in hs]
    defect = list(dict.fromkeys(defect))
    question = any(re.search(pat, text.strip()) for pat in _QUESTION_PATTERNS)
    request_verb = bool(ops) and not (set(ops) <= {"inspect"})
    utterance = "question" if question else ("request" if request_verb else "observation")
    present_tense = bool(re.search(r"\b(?:is|are|has|have|does|do|pushes|asks|mean|means|changes|sits|reads|looks?|shows?|announces?|takes?|covers?|stacks?|blends?|blocks?|drifts?|disappears?|vanish(?:es)?|jumps?|breaks?|gets?|goes|loses?|keeps?|falls?|lands?|ends up|exits?|forgets?|scrolls?|times out|feels?|seems?|becomes?|needs?|lacks?|never|always|only show|puts?|places?|hides?|mixes?|lets?|makes?|walks?|throws?|rejects?|overwrites?|autoplays?|wraps?|squeezes?|traps?|fights?|opens?|fires?|resets?|wipes?|skips?|loads?|runs?|fails?|edit|edits|update|updates|happens?|touch(?:es)?|prints?|removes?|asks? for)\b", stripped))
    spec_shape = (not existing_cues and not defect and not ops
                  and re.match(r"\s*(?:an? |one |new |online |simple |small |mobile |native )?[a-z0-9-]+(?: [a-z0-9-]+)? (?:store|shop|site|website|app|portal|dashboard|tool|page|player|kiosk|marketplace|landing page|catalogue|catalog|hub|client|console|panel)\b.*\b(?:for|that|which|where)\b", stripped))
    if spec_shape:
        new_cues = new_cues + ["spec-shaped noun phrase (a <thing> for <audience>)"]
        ops.setdefault("create", ["implied by spec-shaped noun phrase"])
        utterance = "request"
    if utterance == "observation" and present_tense and not new_cues:
        existing_cues = existing_cues or ["present-tense observation"]
        if not defect:
            defect = ["observed behaviour"]
    if utterance == "observation" and not new_cues and re.match(r"\s*(?:the|our|this|these|my)\b", text) and domains_probe(text):
        existing_cues = existing_cues or ["determiner-led observation with a problem domain"]
        if not defect:
            defect = ["implicit problem"]
    if re.search(r"\b(?:build|add|create|implement)\b[a-z ]{0,30}\bsupport\b", stripped) or re.search(r"\badd (?:keyboard|screen-reader|voiceover|accessibility|remote|d-pad)\b", stripped):
        ops.pop("create", None); ops.setdefault("modify", ["capability on an existing surface"])
    domains = {d: _hits_any(text, cues) for d, cues in _DOMAIN_CUES.items()}
    if "accessibility" in problems or _hits_any(text, _A11Y_FACET):
        domains.setdefault("accessibility", []).append("a11y facet")
    if "interaction" in problems:
        domains.setdefault("interaction", []).append("interaction problem")
    if "visual" in problems:
        domains.setdefault("visual", []).append("visual problem")
    domains = {d: h for d, h in domains.items() if h}
    ranked = sorted(domains, key=lambda d: (-len(domains[d]), PROBLEM_DOMAINS.index(d)))
    problem_domain = ranked[:3]
    # artifact state
    if new_cues and not (defect and not ops.get("create")):
        artifact = "new"
    elif existing_cues or defect or no_change or ops.get("polish") or ops.get("restructure") or ops.get("diagnose") or ops.get("review") or ops.get("validate") or ops.get("compare") or (ops.get("modify") and not ops.get("create")):
        artifact = "existing"
    elif ops.get("create") or ops.get("redesign"):
        artifact = "new" if not existing_cues else "existing"
    else:
        artifact = "unknown"
    # operations (derived when no verb): an observation of a defect is diagnose + modify
    operations = list(ops)
    if not operations:
        if defect or (utterance == "observation" and artifact == "existing"):
            operations = ["diagnose", "modify"]
        elif question:
            operations = ["diagnose"]
    if question and "diagnose" not in operations and not ops.get("create"):
        operations = ["diagnose"] + [o for o in operations if o != "diagnose"]
    if no_change:
        operations = [o for o in operations if o in ("inspect", "diagnose", "review", "validate", "compare")] or ["review"]
    # change scope
    scope_hits = {sc: _hits_any(text, cues) for sc, cues in _SCOPE_CUES.items()}
    if ops.get("redesign") and (scope_hits["system"] or "navigation" in text or "architecture" in text):
        change_scope = "system"
    elif scope_hits["system"] and (ops.get("redesign") or ops.get("restructure") or ops.get("create") or "design-system" in lexicon_modes or "brand" in lexicon_modes):
        change_scope = "system"
    elif scope_hits["flow"] and (ops.get("redesign") or ops.get("restructure") or "end to end" in text or "end-to-end" in text):
        change_scope = "flow"
    elif scope_hits["local"] and not ops.get("redesign") and not scope_hits["system"]:
        change_scope = "local"
    elif scope_hits["screen"] or scope_hits["flow"]:
        change_scope = "screen" if scope_hits["screen"] else "flow"
    else:
        change_scope = "unknown"
    # preservation targets
    preserve = []
    if _hits_any(text, _PRESERVE):
        for target, words in _PRESERVE_TARGETS.items():
            for w in words:
                if re.search(_PRESERVE_WORDS + r" (?:[a-z'-]+ ){0,4}?" + re.escape(w) + r"\b", text):
                    preserve.append(target); break
        if re.search(r"without (?:redesigning|changing) (?:it|the (?:page|screen|app|flow))\b", text):
            preserve += ["navigation", "layout", "system"]
        if re.search(r"(?:in (?:its|the)(?: app's)? existing style|matching the existing|consistent with the (?:existing|rest)|same style as)", text):
            preserve += ["system"]
    if re.search(r"without (?:changing|touching) (?:how it works|its? (?:behaviou?r|functionality|workflow)|the workflow)", text):
        preserve.append("behaviour")
    preserve = list(dict.fromkeys(preserve))
    facet = "accessibility" if "accessibility" in problem_domain[:2] else "interaction" if problem_domain and problem_domain[0] in ("interaction", "navigation") else "visual" if problem_domain and problem_domain[0] in ("visual", "layout", "brand", "design-system") else "general"
    return {"artifact_state": artifact, "operations": operations, "problem_domain": problem_domain, "change_scope": change_scope, "utterance": utterance,
            "existing": artifact == "existing", "problem": bool(defect), "facet": facet, "diagnose_only": bool(no_change) or (set(operations) <= {"inspect", "diagnose", "review", "validate", "compare"} and bool(operations) and not ops.get("modify")),
            "creation": bool(ops.get("create")) and artifact != "existing" or (bool(ops.get("create")) and not defect), "redesign": bool(ops.get("redesign")),
            "responsive_cues": "responsive" in problem_domain, "preserve": preserve, "scope": {"local": "low", "screen": "moderate", "flow": "moderate", "system": "high", "unknown": "moderate"}[change_scope],
            "evidence": {"existing": existing_cues[:5], "new": new_cues[:3], "defect": defect[:5], "operations": {k: v[:3] for k, v in ops.items()}, "domains": {d: h[:3] for d, h in domains.items()},
                         "no_change": no_change[:2], "scope": {k: v[:2] for k, v in scope_hits.items() if v}, "question": question}}


_MODE_PRIORITY = ["accessibility", "audit", "review", "brand", "design-system", "responsive", "reconstruct", "refactor", "polish", "create"]


def derive_modes(intent: dict, lexicon_modes: dict, problems: dict) -> tuple[list[str], list[str], list[dict]]:
    """Modes from artifact state + operations + problem domain + change scope + explicit verbs.
    Explicit lexicon modes (audit, brand, design-system, responsive, reconstruct, accessibility, review, refactor,
    polish) are the strongest signal; create verbs are structural, not explicit."""
    score: dict[str, float] = {}
    ev: list[str] = []
    conflicts: list[dict] = []

    def bump(m, v, why):
        score[m] = score.get(m, 0.0) + v
        ev.append(f"{m}: {why}")
    ops = set(intent["operations"]); dom = intent["problem_domain"]; art = intent["artifact_state"]
    for m, hits in lexicon_modes.items():
        if m == "create":
            continue
        bump(m, 3.5 + 0.5 * len(hits), "explicit: " + ", ".join(hits[:3]))
    if intent["diagnose_only"]:
        if "review" in ops or "compare" in ops or "validate" in ops or intent["evidence"]["no_change"]:
            bump("review", 3.0, "assessment without changes (" + ", ".join(sorted(ops & {"review", "compare", "validate"})) + ")")
            bump("audit", 2.0, "diagnosis is part of the review")
        else:
            bump("audit", 3.0, "diagnose request")
        if "accessibility" in dom[:2]:
            bump("accessibility", 2.6, "accessibility problem domain")
        if "responsive" in dom[:2]:
            bump("responsive", 1.5, "responsive problem domain")
    elif art == "existing" and ("diagnose" in ops or intent["problem"]) and not ops & {"create", "redesign"}:
        # a defect or observation on existing UI: diagnose + fix, coloured by the problem domain
        lead = dom[0] if dom else "general"
        if "accessibility" in dom[:2]:
            bump("accessibility", 3.0, "accessibility defect on existing UI"); bump("audit", 2.0, "diagnose the reported defect")
        elif lead in ("interaction", "navigation"):
            bump("audit", 3.0, f"{lead} defect on existing UI"); bump("refactor", 2.0, "fix follows the diagnosis")
        elif lead == "layout":
            bump("audit", 3.0, "layout/structure defect on existing UI"); bump("refactor", 2.0, "structural fix follows")
            if "visual" in dom[:2]:
                bump("polish", 1.5, "visual aspect")
        elif lead == "visual":
            bump("polish", 3.0, "visual defect on existing UI"); bump("audit", 2.0, "diagnose first")
        elif lead == "responsive":
            bump("responsive", 3.0, "responsive defect"); bump("audit", 2.0, "diagnose first")
        elif lead == "performance-ux":
            bump("audit", 3.0, "perceived-performance defect"); bump("refactor", 2.0, "fix follows the diagnosis")
        elif lead == "brand":
            bump("brand", 3.0, "brand differentiation problem"); bump("audit", 1.5, "diagnose first")
        elif lead == "design-system":
            bump("design-system", 3.0, "consistency / tokens problem"); bump("audit", 2.0, "diagnose first")
        else:
            bump("audit", 3.0, "problem statement on existing UI"); bump("refactor", 2.0, "fix follows the diagnosis")
        if "responsive" in dom[:2] and "responsive" not in score:
            bump("responsive", 2.5, "size/viewport cues with a defect")
        if ops & {"polish"} and "polish" not in score:
            bump("polish", 1.5, "polish verb")
        if ops & {"restructure"}:
            bump("refactor", 2.5, "restructuring requested")
    elif "redesign" in ops:
        if art == "existing" or lexicon_modes.get("refactor"):
            bump("refactor", 3.0, "redesign of an existing surface"); bump("create", 1.5, "new structure allowed")
        else:
            bump("create", 3.0, "redesign from scratch")
    elif "create" in ops:
        bump("create", 3.0, "build/create request" + (" on an existing surface" if art == "existing" else ""))
        if art == "existing" and (ops & {"modify", "restructure"} or intent["problem"]):
            bump("refactor", 1.0, "existing surface will change")
        if intent["problem"]:
            bump("audit", 1.2, "problem statement alongside the build request")
    elif ops & {"restructure"}:
        bump("refactor", 3.0, "restructure: " + ", ".join(intent["evidence"]["operations"].get("restructure", [])[:2]))
        if ops & {"polish"} or (dom and dom[0] in ("visual", "layout")):
            bump("polish", 1.5, "look/feel words present")
    elif ops & {"polish"}:
        bump("polish", 3.0, "polish request"); bump("audit", 1.0, "diagnose first")
        if ops & {"modify"} and dom and dom[0] in ("interaction", "navigation"):
            bump("refactor", 1.5, "interaction change")
    elif ops & {"modify"}:
        lead = dom[0] if dom else "general"
        if "accessibility" in dom[:2]:
            bump("accessibility", 3.0, "accessibility change"); bump("refactor", 2.0, "modification")
        elif lead in ("visual", "layout") and intent["change_scope"] in ("local", "unknown"):
            bump("polish", 3.0, "visual change on a small scope"); bump("refactor", 1.0, "modification")
        elif lead == "responsive":
            bump("responsive", 3.0, "responsive change"); bump("refactor", 1.5, "modification")
        else:
            bump("refactor", 3.0, "modification of existing UI: " + ", ".join(intent["evidence"]["operations"].get("modify", [])[:2]))
            if intent["problem"]:
                bump("audit", 1.5, "problem statement")
    elif art == "existing" and intent["utterance"] == "observation":
        bump("audit", 2.5, "observation about existing UI without a request verb"); bump("polish", 1.0, "likely a polish"); bump("refactor", 1.0, "or a local fix")
    if intent["evidence"]["domains"].get("accessibility") and "accessibility" not in score and (intent["problem"] or ops):
        bump("accessibility", 1.5, "accessibility vocabulary")
    if intent["problem"] and "audit" not in score and "create" not in score:
        bump("audit", 1.0, "problem statement")
    if intent["evidence"]["no_change"]:
        for m in ("refactor", "polish", "create"):
            if m in score:
                score.pop(m); ev.append(f"{m}: removed (no code changes requested)")
    if intent["preserve"] and "redesign" in ops:
        conflicts.append({"field": "scope", "request": "preserve " + ", ".join(intent["preserve"]), "project": "redesign requested",
                          "resolution": "unresolved: state which parts may change before designing"})
    if not score:
        if intent.get("existing") and intent.get("utterance") == "observation":
            score["audit"] = 2.0; score["refactor"] = 1.0; ev.append("audit: observation about an existing surface (no verb)"); ev.append("refactor: fix follows the diagnosis")
        else:
            score["create"] = 0.0; ev.append("create: default (no cue at all)")
    ordered = sorted(score, key=lambda m: (-score[m], _MODE_PRIORITY.index(m)))
    return ordered, ev, conflicts


def change_budget(modes: list[str], intent: dict, has_project: bool = False) -> str:
    """low (polish/audit/review/accessibility with a local or screen scope) · moderate (refactor, fixes after a
    diagnosis, additions inside an existing surface or repository, flow-level changes) · high (redesign, brand,
    system-level scope) · greenfield (create with no existing surface)."""
    primary = modes[0] if modes else "create"
    ops = set(intent.get("operations", [])); sc = intent.get("change_scope", "unknown")
    if "redesign" in ops or sc == "system" and (primary in ("refactor", "brand", "design-system") or "restructure" in ops):
        return "high"
    if primary == "brand":
        return "high"
    if primary in ("polish", "review"):
        return "low"
    if primary in ("audit", "accessibility"):
        return "moderate" if (("refactor" in modes[1:3] and intent.get("facet") == "interaction") or ops & {"modify", "restructure"} and sc in ("screen", "flow")) else "low"
    if primary in ("refactor", "responsive", "design-system", "reconstruct"):
        return "moderate"
    if primary == "create":
        return "moderate" if (intent.get("existing") or has_project) else "greenfield"
    return "moderate"


# ---------------------------------------------------------------------------
# Canonical alias layer: equivalent phrasings -> concept id. Used for demand (problem/job wording) and by the
# evaluator to credit a concept expressed under another name. Normalisation: lowercase, hyphen/space unified,
# plural and common verb forms folded. Deterministic; no NLP library.
# ---------------------------------------------------------------------------
ALIASES = {
    "state.offline_sync": ["no signal", "lost connection", "poor signal", "without signal", "goes offline", "back online"],
    "form.autofill_attributes": ["retype", "re-type", "type the same", "same address twice", "enter it twice", "again on the next"],
    "onboarding.setup_checklist": ["what to do first", "empty workspace"],
    "state.saving_conflict": ["overwrites the first", "overwrites", "overwrite each other", "edit the same", "second one overwrites", "conflicting edits"],
    "touch.safe_areas": ["notch", "home indicator", "hides the score counter", "safe area", "safe areas", "behind the home indicator"],
    "anti.platform_scaling": ["stretched phone", "stretched phone app", "scaled up", "blown up", "looks like a stretched", "shrunk desktop"],
    "data.realtime_window": ["times a second", "updates every second", "real-time updates", "live updates", "streaming updates", "update forty times"],
    "interaction.focus_visible": ["focus outline", "focus ring", "focus indicator", "outline is missing", "no visible focus", "focus is invisible"],
    "media.details_play_first": ["find play", "play button", "past the cast", "scroll past the cast", "to find play", "play is below"],
    "privacy.shared_device": ["passers-by", "passers by", "everyone shares", "previous visitor", "shared screen", "keeps the previous"],
    "layout.settings_grouping": ["mixes billing", "one wall", "settings page mixes", "grouped settings", "settings grouping"],
    "content.readable_measure": ["too wide to read", "line length", "measure", "wide paragraph", "paragraph is too wide"],
    "onboarding.linear_wizard": ["five steps", "walks through", "no way back", "steps with no way back", "multi-step"],
    "adaptive.navigation_transform": ["hides the bottom", "wideorientation hides", "hides the bottom tabs", "rotating the phone", "rotate the phone", "orientation change", "when rotated"],
    "adaptive.breakpoint_matrix": ["off screen", "off-screen", "wideorientation", "in wideorientation", "portrait and landscape", "pixels wide", "px wide", "breaks between", "window narrower", "narrower the", "viewport", "breakpoint", "breakpoints", "resize the window", "shrink the window", "narrow windows", "narrow screens"],
    "a11y.text_scaling": ["larger text", "large text", "text size", "dynamic type", "font scaling", "text scaling", "bigger text", "accessibility text size"],
    "env.glanceable_status": ["how long each", "sitting there", "waiting time", "glanceable"],
    "a11y.reduced_motion": ["queasy", "motion sick", "slide-in animation", "animation on every", "reduced motion", "motion sickness"],
    "perf.focus_latency": ["hold right", "hold left", "holding right", "holding the remote", "held down", "auto repeat", "key repeat", "flies past", "scrolls too fast", "too fast to read"],
    "table.inline_edit": ["typing the quantity", "operators keep typing", "keep typing", "typing into the"],
    "touch.gestures_discoverable": ["drag", "dragging", "dragged", "swipe to", "long press", "drag and drop"],
    "data.pagination_strategy": ["more than twenty rows", "more than 20 rows", "hundreds of rows", "too many rows", "rows pile up", "long list", "hard to scan once", "once there are more than"],
    "data.kpi_comparison": ["against the quota", "quota", "usage this month", "where we are against", "against the target", "vs last", "weekly summary", "summary card", "kpi"],
    "perf.image_sizing": ["cropped square", "photos are cropped", "load unsized", "images load unsized", "thumbnail", "tiny thumbnail", "photos are tiny", "images are tiny", "full size", "zoom into", "check the photo", "cant check"],
    "touch.ime_keyboard": ["keyboard is up", "keyboard up", "keyboard open", "keyboard is open", "keyboard covers", "keyboard hides", "keyboard pushes", "on screen keyboard", "soft keyboard", "with the keyboard open", "keyboard appears"],
    "content.i18n_expansion": ["language option", "welsh", "another language", "bilingual", "language switcher", "add a language", "language switch", "language toggle", "spanish", "french", "german", "arabic", "translation", "translate", "localise", "localize", "localisation", "localization", "multilingual", "second language", "other language"],
    "feedback.progress_indicator": ["fails silently", "silently", "no error shown", "nothing tells you it failed", "spinning circle", "spinning", "gives no sign", "no sign anything happened", "runs for a minute", "three screens", "only a spinner", "spinner", "what is happening", "whats happening", "never says what", "how far along", "still working", "progress", "n of m", "how long it will take"],
    "state.unsaved_changes_guard": ["unsaved", "lose an unsaved", "lose their edits", "lose your edits", "lose the form", "lose what you typed", "unsaved changes", "switch records", "clicking another one"],
    "a11y.contrast": ["impossible to read", "hard to read", "unreadable", "cannot read", "can't read", "invisible on the dark", "invisible on dark", "nobody can tell which", "can't tell which", "barely visible", "contrast", "indistinguishable from", "grey on grey", "gray on gray", "too light", "too faint to", "barely visible", "hard to see", "cant see", "cannot see", "too dim", "faint", "invisible in dark mode", "in dark mode", "low contrast", "washed out"],
    "interaction.selection_visible": ["selected row", "selected item", "selected tab", "selected state", "the selection", "selected channel", "currently selected", "which is selected", "which one is selected", "tell which", "current choice", "selected language", "selected track", "persistent selection", "selected-state visibility", "selected state visible", "current-row indication", "current row indication", "which row is selected", "what's selected", "what is selected", "selected row is barely visible", "selection is invisible", "selection state", "row highlight", "highlighted row", "selected item disappears", "selection vanishes", "selection visibility"],
    "interaction.focus_restore": ["lose their place", "loses their place", "lose your place", "lost their place", "back at the top of the row", "returns to the top", "remember focus", "return focus", "restore focus", "restore previous item", "restore the previous item", "focus restoration", "lose their place", "loses their place", "lose your place", "come back from", "coming back from", "returning from", "when you go back", "back out of", "focus is lost", "loses focus", "focus lost"],
    "table.column_priority": ["responsive column priority", "column priority", "important columns survive", "hide low-priority columns", "hide columns", "which columns", "columns on the phone", "columns on tablets"],
    "tv.player_autohide": ["never hide", "controls never hide", "never auto-hide", "never auto hide", "auto-hide", "auto hide", "auto-hides", "autohide", "controls never disappear", "controls never go away", "never goes away", "controls disappear", "controls time out", "hide the controls", "transport bar never"],
    "layout.focal_hierarchy": ["nobody can find", "can't find", "cannot find", "hard to find", "buried", "below the fold", "hides the important", "puts the amount", "buried below", "stands out", "nothing stands out", "same weight", "equally sized", "buries", "buried under", "in the footer", "same size", "equal weight", "too much to scan", "equal importance", "shout at the same volume", "hierarchy", "what matters most", "focal point", "miss the important"],
    "data.exception_first": ["scan for problems", "scan for", "spot problems", "staff scan", "look for problems", "late orders", "hides late", "among healthy", "needs action first", "problem orders", "overdue", "which are overdue", "which are late", "late in the list", "without opening each", "see which", "at a glance", "needs attention", "exceptions first", "alerts first", "first thing they see", "notice new alerts", "anomalies", "miss the important numbers"],
    "table.tabular_figures": ["do not line up", "don't line up", "totals do not line up", "line up", "currency symbol", "totals row", "amounts line up", "price column", "quantity into the price", "wrong column", "quantity column", "numbers column", "numbers are hard to compare", "hard to compare", "numbers don't line up", "numbers dont line up", "numeric alignment", "tabular figures", "tabular numbers", "align numbers", "line up numbers"],
    "navigation.orientation_and_back": ["lose where you were", "where you were", "where you are in", "which page you are on", "way back", "find their way back", "where they are", "which section", "breadcrumb shows", "orientation", "back returns", "deep link"],
    "layout.one_primary_action": ["all look the same", "look the same", "same on the form", "three buttons look", "which button", "what to do next", "don't know what to do", "primary action", "one call to action", "two look identical", "buttons look identical", "next step is unclear"],
    "layout.spacing_scale": ["8px grid", "8 px grid", "4px grid", "same grid", "spacing grid", "px grid", "the same spacing as", "cramped", "spacing", "inconsistent spacing", "uneven spacing", "tighten"],
    "a11y.dialog_focus": ["traps keyboard focus", "traps focus", "cannot be dismissed", "can't be dismissed", "can't close it", "cannot close it", "no way to close", "sheet", "dialog", "modal", "popup", "prompt", "chooser", "flyout", "bottom sheet", "focus lands on the body", "focus jumps to the top", "modal loses focus", "modals don't return focus", "trapped inside", "get stuck inside", "keyboard trap", "focus trap"],
    "a11y.color_not_only": ["distinguishable", "greyscale", "grayscale", "black and white", "tell the series apart", "tell apart", "status colour", "status color", "colour-blind", "color-blind", "colourblind", "colorblind", "colour only", "color only", "colour alone", "color alone", "indistinguishable statuses", "status colours"],
    "perf.layout_shift": ["grid shifts", "shifts when images load", "loads late", "loads at the top and", "jumps around", "jump around", "layout shift", "pushes everything down", "shifts when", "moves when it loads"],
    "env.outdoor_readability": ["in sunlight", "outdoors at noon", "impossible to read outdoors", "glare", "bright light"],
    "state.loading_empty_error": ["loading layer", "loading overlay", "shows nothing while", "while it loads", "nothing while it loads", "fetches from the server", "blank while", "shows nothing", "goes blank", "blank area", "finds nothing", "loading state", "empty state", "error state", "blank before", "blank white area", "skeleton"],
    "tv.ten_foot_typography": ["from the sofa", "from the couch", "read from a distance", "ten feet", "10-foot", "readable at distance", "hard to read from"],
    "interaction.keyboard_navigation": ["keyboardonly", "keyboard only", "without the mouse", "mouseless", "hands on the keyboard", "keyboard-first", "keyboard first", "focus order", "tab order", "keyboard order", "keyfocusstep", "skips the search field", "get past the", "cannot get past", "cant get to", "cannot get to", "keyboard alternative", "from the keyboard", "no way to do it from the keyboard", "keyboard-only", "keyboard only", "keyboard users", "tab through", "tab stops per row", "reach with the keyboard", "can't be reached by keyboard"],
    "touch.minimum_target": ["hit the wrong key", "wrong key", "targets too small", "hard to tap", "fat finger", "big buttons", "large targets", "gloves"],
    "state.session_expiry": ["times out", "time out", "timeout", "session expires", "idle reset", "logs people out"],
    "feedback.validation_errors": ["error messages appear far away", "errors far from the field", "validation errors", "inline errors", "required markers", "form errors"],
    "media.resume_playback": ["resume", "continue watching", "where they stopped", "where they left off", "pick up where"],
    "media.track_selection": ["subtitles cannot", "turn on subtitles", "subtitles while", "audio track", "switch the commentary", "commentary language", "subtitles and audio", "audio language", "language chooser", "commentary language", "switch the commentary", "subtitle language", "audio and subtitle", "subtitle picker", "subtitles picker", "subtitle and audio", "audio track", "caption selection", "subtitle selection", "subtitles are three menus deep"],
    "tv.time_navigation": ["half hour ticks", "listings jump when", "ticks over", "time slot moves", "current-time line", "now line", "now marker", "jump to time", "time navigation", "by time and day"],
    "data.comparison_structure": ["pricing plans", "two plans", "difference between the", "pick one", "which plan", "compare plans", "compare our plans", "comparison table", "compare tiers", "feature comparison", "side-by-side plans", "plan comparison"],
    "feedback.trust_signals": ["wrong total", "basket shows", "total after removing", "trust", "shipping costs before", "no surprise costs", "security badges", "what happens next after paying", "cost transparency"],
    "feedback.confirmation_destructive": ["happens instantly", "instantly", "the instant you", "by accident", "accidentally", "no way to undo", "can't undo", "cannot undo", "confirm and cancel", "cancel buttons are flush", "flush together", "next to cancel", "one tap with no confirmation", "no confirmation", "without confirmation", "throws the changes away", "without warning", "discard", "close the window with unsaved", "approve", "approval", "confirm the payment", "delete button sits right next to", "irreversible", "destructive"],
    "interaction.back_semantics": ["when they return from", "return from an episode", "back from the", "back button exits", "exits the app instead", "back closes", "remote's back", "back behaviour", "back behavior"],
    "onboarding.permission_priming": ["asks for every permission", "permission prompt", "permissions on the first screen"],
    "onboarding.feature_education": ["first-run tips", "coach marks", "tips block", "tooltip tour"],
    "data.refresh_timestamp": ["last sync time", "last synced", "sync time", "as of", "last updated", "stale data", "how fresh"],
    "layout.no_nested_cards": ["cards inside cards", "nested cards", "card in a card"],
    "brand.dark_mode_redesign": ["inverted light theme", "dark variant is muddy", "dark mode looks inverted"],
    "brand.structural_differentiation": ["identical apart from the logo", "impossible to tell apart", "tell the tiers apart"],
    "brand.type_roles": ["heading font", "font looks too heavy", "too heavy next to", "nine different sizes", "too many font sizes", "type scale"],
    "brand.token_layers": ["primary button changes colour", "changes colour on every page", "colours into tokens", "extract the colours"],
    "anti.template_landing": ["reads like a template", "looks like a template", "template skeleton"],
    "touch.thumb_reach": ["thumbs cover", "out of thumb reach", "one-handed", "bottom bar labels"],
    "data.accessible_chart_alternative": ["charts have no legend", "chart tooltips can't be reached", "chart without a table"],
    "a11y.live_status": ["never says", "nothing tells", "no way to know", "doesn't say", "does not say", "never tells", "not told", "are not told", "upload finished", "screen reader users are not", "never announced", "not announced", "never says", "nothing tells", "no feedback", "status is a spinner", "sync status", "tells the front desk", "announce", "nobody notices the banner", "announce", "screen reader announces"],
    "a11y.accessible_names": ["visible label", "placeholder text", "placeholder as the label", "placeholder instead of a label", "label on the", "add a tooltip", "tooltip to the", "no names for", "icon-only", "reads the price twice", "announced twice", "icon-only buttons have no name", "unlabeled", "unlabelled"],
    "interaction.hover_independence": ["only show on hover", "hover only", "hover-only"],
    "table.virtualization": ["janky", "stutters when scrolling", "thousands of rows", "3,000 rows", "rows and scrolling", "scrolling is janky", "scrolling freezes", "50,000 rows", "thousands of rows", "virtualize", "virtualise", "giant table"],
    "table.selection_bulk": ["per-row selection", "bulk actions", "select all"],
    "data.filter_chips": ["narrow it down", "narrow down", "cannot narrow", "can't narrow", "refine the results", "filters panel covers", "applied filters", "filter chips"],
    "navigation.platform_grammar": ["bottom bar", "tab bar", "platform navigation"],
    "process.reuse_first": ["reuse the existing components", "existing primitives", "match the existing components"],
}


def normalize_phrase(p: str) -> str:
    p = p.lower().strip().replace("’", "'").replace("'", "")
    p = re.sub(r"[-_/]+", " ", p)
    p = re.sub(r"\s+", " ", p)
    words = []
    for w in p.split(" "):
        if len(w) > 4 and w.endswith("ies"):
            w = w[:-3] + "y"
        elif len(w) > 3 and w.endswith("es") and w[-3] in "shx":
            w = w[:-2]
        elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        if len(w) > 4 and w.endswith("ing") and w[:-3] + "e" in ("hide", "restore", "close", "lose", "resume", "compare"):
            w = w[:-3] + "e"
        words.append(w)
    return " ".join(words)


_ALIAS_NORM = [(cid, normalize_phrase(a)) for cid, als in ALIASES.items() for a in als]


def alias_concepts(text: str) -> dict[str, list[str]]:
    """Concept ids whose alias phrases occur in the text (normalised match)."""
    t = " " + normalize_phrase(text) + " "
    out: dict[str, list[str]] = {}
    for cid, a in _ALIAS_NORM:
        if (" " + a + " ") in t or re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", t):
            out.setdefault(cid, []).append(a)
    return out


def concept_for_phrase(phrase: str) -> str | None:
    """Evaluator helper: canonical concept id for a free-form phrase, if it is a known alias or label."""
    n = normalize_phrase(phrase)
    for cid, a in _ALIAS_NORM:
        if n == a:
            return cid
    for cid, (label, _) in CONCEPT_META.items():
        if n == normalize_phrase(label):
            return cid
    return None


REQUIRED_CAP = 8  # saturation: more than this and the policy is wrong; lowest-priority platform generics demote

# ---------------------------------------------------------------------------
# Expected concepts: requirements + concerns -> REQUIRED / RECOMMENDED / OPTIONAL concept ids with reasons.
# Conditional by platform, input, screen, subtype, component, job, problem, risk, environment, mode.
# ---------------------------------------------------------------------------
INPUT_CONCEPTS = {
    "pointer": ["interaction.hover_independence", "interaction.focus_visible"],
    "keyboard": ["interaction.keyboard_navigation", "interaction.focus_visible"],
    "touch": ["touch.minimum_target", "touch.gestures_discoverable", "touch.ime_keyboard", "touch.thumb_reach"],
    "remote": ["interaction.dpad_reachability", "interaction.focus_restore", "interaction.back_semantics", "tv.ten_foot_typography"],
}
ENVIRONMENT_CONCEPTS = {
    "outdoor": ["env.outdoor_readability", "env.glanceable_status"], "gloves": ["touch.minimum_target"],
    "shared-device": ["privacy.shared_device"], "public": ["privacy.shared_device", "touch.minimum_target"],
    "large-display": ["tv.ten_foot_typography"], "low-bandwidth": ["state.offline_sync"], "low-light": ["a11y.contrast"], "noisy": ["a11y.live_status"],
}
SUBTYPE_CONCEPTS = {"epg": ["tv.epg_pinned_channels", "tv.time_navigation", "table.virtualization", "media.live_channel_switching"],
                    "data-grid": ["table.tabular_figures", "table.selection_bulk", "table.inline_edit", "table.virtualization"],
                    "wizard": ["onboarding.linear_wizard", "feedback.progress_indicator", "state.saving_conflict"], "sign-in": ["tv.sign_in_code"],
                    "rails": ["interaction.focus_restore", "layout.media_card"], "hero": ["layout.hero_thesis"], "feed": ["data.pagination_strategy", "state.loading_empty_error"],
                    "chat": ["a11y.live_status", "state.loading_empty_error"], "map": ["data.accessible_chart_alternative"], "calendar": ["interaction.keyboard_navigation"],
                    "permissions": ["onboarding.permission_priming"], "feature-tour": ["onboarding.feature_education"], "checklist": ["onboarding.setup_checklist"],
                    "catalog": ["data.filter_chips", "data.pagination_strategy", "touch.minimum_target"]}
JOB_CONCEPTS = {"monitor": ["data.realtime_window", "data.exception_first", "data.refresh_timestamp", "a11y.color_not_only"],
                "approve": ["feedback.confirmation_destructive", "feedback.validation_errors", "layout.one_primary_action"],
                "alerts": ["data.exception_first", "a11y.live_status", "layout.one_primary_action", "perf.layout_shift"],
                "compare": ["data.comparison_structure"],
                "browse": ["layout.media_card", "interaction.focus_restore"], "resume": ["media.resume_playback"], "watchlist": ["media.watchlist"],
                "live-tv": ["media.live_channel_switching", "tv.player_autohide"], "details": ["media.details_play_first", "interaction.focus_restore"], "search": ["data.search_results"],
                "enter-data": ["table.inline_edit", "feedback.validation_errors"], "drilldown": ["data.drilldown"], "high-risk-action": ["feedback.confirmation_destructive"],
                "authentication": ["feedback.validation_errors"], "permissions": ["onboarding.permission_priming"], "feature-education": ["onboarding.feature_education"],
                "refresh": ["data.refresh_timestamp"]}
ASYNC_WORDS = ["api", "fetch", "fetches", "load", "loads", "loading", "remote", "server", "sync", "offline", "network", "real-time", "realtime", "live", "refresh", "stream", "paginate", "search", "query", "results", "from the server",
               "confirm", "confirmation", "submit", "submission", "save", "saving", "checkout", "order", "orders", "book", "booking", "upload", "pickup", "pick-up", "claim", "payment", "transfer"]
STATIC_WORDS = ["static", "about us", "about-us", "brochure", "marketing page", "landing", "privacy policy", "terms page", "faq page"]


def derive_expected_concepts(req: dict, concerns: dict) -> dict:
    primary = req["mode"][0] if req["mode"] else "create"
    modes = set(req["mode"])
    plats, inputs, screens, prods = set(req["platform"]), set(req["input"]), set(req["screen"]), set(req["product"])
    comps, envs, subtypes, jobs = set(req["components"]), set(req["environment"]), set(req["screen_subtype"]), set(req.get("jobs", []))
    problems = set(req.get("problems", []))
    known_inputs = {i for i, v in req["evidence"]["input"].items() if v["status"] == "KNOWN"}
    text = " " + (req.get("query_clean") or req["query"]).lower() + " "
    req_ids: dict[str, str] = {}
    rec_ids: dict[str, str] = {}
    opt_ids: dict[str, str] = {}
    prio: dict[str, int] = {}   # 0 named in request · 1 job/subtype/screen/environment/risk · 2 mode/states · 3 platform generic
    phase = {"p": 2}

    def need(level: dict, cid: str, reason: str):
        if cid not in CONCEPTS:
            return
        if level is req_ids:
            rec_ids.pop(cid, None); opt_ids.pop(cid, None)
            if cid not in req_ids:
                req_ids[cid] = reason; prio[cid] = phase["p"]
            elif phase["p"] < prio.get(cid, 9):
                prio[cid] = phase["p"]
        elif level is rec_ids:
            if cid in req_ids:
                return
            opt_ids.pop(cid, None); rec_ids.setdefault(cid, reason)
        else:
            if cid in req_ids or cid in rec_ids:
                return
            opt_ids.setdefault(cid, reason)

    marketing_page = bool(screens & {"landing"} or "marketing" in prods or subtypes & {"hero"})
    ops_create = "create" in (req.get("intent") or {}).get("operations", []) or primary == "create"
    modal_words = bool(_count(text, ["sheet", "dialog", "modal", "popup", "pop-up", "prompt", "chooser", "picker", "flyout", "bottom sheet"]))
    soft_keyboard = bool(_count(text, ["keyboard is up", "keyboard up", "keyboard open", "keyboard is open", "keyboard covers", "keyboard hides", "keyboard pushes", "on-screen keyboard", "soft keyboard", "keyboard appears", "with the keyboard open"])) or (bool(plats & {"mobile", "tablet"}) and "keyboard" in text and not _count(text, ["hardware keyboard", "external keyboard", "bluetooth keyboard", "keyboard shortcut*"]))
    form_like = bool(screens & {"form", "checkout", "auth"} or comps & {"form"} or subtypes & {"wizard", "sign-in"} or "enter-data" in jobs or _count(text, ["invite*", "sign up", "sign-up", "signup", "registration", "register", "apply for", "application form"]))
    # 0. wording that names a principle directly (canonical aliases) is the strongest demand
    phase["p"] = 0
    for cid, hits in alias_concepts(req.get("query_clean") or req["query"]).items():
        if cid in ("tv.player_autohide", "media.track_selection", "tv.time_navigation") and not (plats & {"tv"} or "remote" in inputs or screens & {"player"} or _count(text, ["player", "playback", "controls", "guide", "set-top", "cable box"])):
            continue
        if cid in ("env.outdoor_readability",) and not _count(text, ["outdoor*", "sunlight", "sun", "glare", "bright light"]):
            continue
        need(req_ids, cid, "named in the request: " + ", ".join(hits[:2]))
    if _count(text, ["chart*", "graph*", "the bars", "bars are", "bar chart", "stats screen", "sparkline*"]) and "chart" not in comps:
        comps = comps | {"chart"}
    data_like = bool(screens & {"dashboard", "list"} or comps & {"table", "chart"} or subtypes & {"data-grid", "epg"} or prods & {"finance", "erp"} or jobs & {"monitor", "compare", "drilldown"})
    grid_like = bool(comps & {"table"} or subtypes & {"data-grid"} or "enter-data" in jobs)
    intent_ = req.get("intent") or {}
    visual_task = primary in ("polish", "brand", "design-system") or (intent_.get("problem_domain", [None])[:1] in (["visual"], ["layout"]) and intent_.get("utterance") == "observation" and not _count(text, ASYNC_WORDS))
    async_structural = bool(screens & {"list", "dashboard", "search", "detail", "player", "home", "checkout"}) or bool(comps & {"table", "chart", "list", "search", "media", "empty-state"}) or bool(jobs & {"monitor", "browse", "search", "resume", "refresh"}) or bool(subtypes & {"feed", "epg", "rails", "chat", "map"}) or ("low-bandwidth" in envs)
    async_data = bool(_count(text, ASYNC_WORDS)) or (async_structural and not visual_task)
    static_page = bool(_count(text, STATIC_WORDS)) and not _count(text, ASYNC_WORDS)

    # 1. mode / task shape
    phase["p"] = 2
    named_a11y = {c for c in alias_concepts(req.get("query_clean") or req["query"]) if c.startswith("a11y.") or c in ("interaction.focus_visible", "interaction.keyboard_navigation", "interaction.selection_visible")}
    narrow_a11y = bool(named_a11y) and (req.get("intent") or {}).get("change_scope") not in ("flow", "system") and not _count(text, ["review", "audit", "checklist", "wcag", "compliance", "whole", "entire", "every screen", "all screens", "the app"])
    if primary in ("accessibility",) or "accessibility" in problems or (primary in ("audit", "review") and "accessib" in req["query"].lower()):
        level = rec_ids if narrow_a11y else req_ids
        phase["p"] = 1
        for c in ("a11y.accessible_names", "a11y.contrast", "a11y.semantics"):
            need(level, c, "accessibility review" if not narrow_a11y else "accessibility review (one named defect: kept as a recommendation)")
        need(level, "a11y.color_not_only", "accessibility review"); need(level, "a11y.live_status", "accessibility review")
        phase["p"] = 2
        need(rec_ids, "a11y.text_scaling", "accessibility review"); need(rec_ids, "a11y.reduced_motion", "accessibility review")
    elif primary in ("audit", "review"):
        need(rec_ids, "a11y.accessible_names", f"{primary} mode"); need(rec_ids, "a11y.contrast", f"{primary} mode")
    if "interaction" in problems:
        need(req_ids, "layout.one_primary_action", "interaction problem: which action is primary"); need(rec_ids, "interaction.hover_independence", "interaction problem")
    if "visual" in problems or primary == "polish":
        need(req_ids, "layout.spacing_scale", "visual problem / polish"); need(req_ids, "layout.focal_hierarchy", "visual problem / polish")
        need(rec_ids, "layout.no_nested_cards", "polish removes container noise")
    if primary == "brand":
        need(req_ids, "brand.structural_differentiation", "brand mode"); need(req_ids, "brand.token_layers", "brand mode: tokens per brand")
        need(rec_ids, "brand.corner_language", "brand geometry"); need(rec_ids, "brand.type_roles", "brand typography"); need(rec_ids, "anti.default_fonts", "brand mode")
    if primary == "design-system":
        need(req_ids, "brand.token_layers", "design-system mode"); need(req_ids, "a11y.contrast", "token validation"); need(req_ids, "brand.type_roles", "type scale")
        need(rec_ids, "layout.spacing_scale", "spacing tokens"); need(rec_ids, "brand.dark_mode_redesign", "dark theme")
        if "dark" in text:
            need(req_ids, "brand.dark_mode_redesign", "dark theme requested")
    if primary == "responsive":
        need(req_ids, "adaptive.breakpoint_matrix", "responsive mode"); need(rec_ids, "adaptive.navigation_transform", "responsive mode")
        if comps & {"table"} or grid_like:
            need(req_ids, "table.column_priority", "table across widths")
    if primary == "reconstruct" or "screenshot" in text:
        need(req_ids, "process.reuse_first", "reconstruction inside an existing project keeps its components")
        need(rec_ids, "process.safe_modification", "reconstruction must not replace routing/tokens")
    if primary in ("refactor", "polish") and req.get("constraints", {}).get("preserve_existing_system"):
        need(rec_ids, "process.safe_modification", "modifying an existing system")
    if primary in ("create", "refactor") and marketing_page:
        need(req_ids, "layout.hero_thesis", "landing page"); need(req_ids, "layout.focal_hierarchy", "landing page"); need(rec_ids, "anti.template_landing", "landing page")
        need(rec_ids, "perf.layout_shift", "landing LCP/CLS"); need(rec_ids, "content.readable_measure", "landing copy")

    # 2. states (conditional on async data, submission, network dependency)
    if async_data and not static_page:
        need(req_ids if (screens or comps or jobs) else rec_ids, "state.loading_empty_error", "asynchronous or remote data on this screen")
    elif form_like:
        need(rec_ids, "state.loading_empty_error", "submission states")
    if "low-bandwidth" in envs or "offline" in text:
        need(req_ids, "state.offline_sync", "offline / low bandwidth")
    if form_like and (screens & {"form"} or subtypes & {"wizard"} or "enter-data" in jobs):
        need(rec_ids, "state.unsaved_changes_guard", "long form"); need(rec_ids, "state.saving_conflict", "long form")
    if _count(text, ["session expires", "session expiry", "logs people out", "logged out", "timeout", "time out", "times out", "idle"]):
        need(req_ids, "state.session_expiry", "session wording")
        if _count(text, ["older", "elderly", "before they finish", "slow typist*", "takes them"]):
            need(req_ids, "a11y.text_scaling", "time limits must be adjustable for slower users") if False else None
    phase["p"] = 0 if alias_concepts(req.get("query_clean") or req["query"]) else 2
    if modal_words:
        need(req_ids, "a11y.dialog_focus", "a dialog/sheet is part of the task"); need(rec_ids, "interaction.focus_restore", "focus returns to the opener")
    if soft_keyboard and plats & {"mobile", "tablet"} or _count(text, ["keyboard is up", "keyboard up", "keyboard open", "keyboard is open", "keyboard covers", "on-screen keyboard", "soft keyboard"]):
        need(req_ids, "touch.ime_keyboard", "on-screen keyboard behaviour"); need(rec_ids, "touch.safe_areas", "keyboard inset")
    if "data.exception_first" in req_ids or ("data.exception_first" in rec_ids and _count(text, ["overdue", "late", "at a glance", "see which"])):
        need(req_ids, "a11y.color_not_only", "exception status must not rely on colour alone"); need(req_ids, "env.glanceable_status", "status readable without opening each item")
    if "perf.focus_latency" in req_ids and _count(text, ["flies past", "too fast", "hold right", "hold left", "held down", "auto-repeat", "key repeat"]):
        need(req_ids, "a11y.reduced_motion", "held-key scrolling must respect reduced motion")
    if comps & {"table"} and _count(text, ["hard to scan", "scan", "scanning", "find the ones", "which ones"]):
        need(req_ids, "data.exception_first", "scanning a table means finding the rows that matter first")
    if "env.glanceable_status" in req_ids:
        need(req_ids, "a11y.color_not_only", "glanceable status needs a second channel besides colour")
    if "data.kpi_comparison" in req_ids:
        need(rec_ids, "table.tabular_figures", "KPI values line up"); need(rec_ids, "layout.focal_hierarchy", "one headline number first")
    if modal_words and _count(text, ["chooser", "picker", "choose", "select a", "radio", "options"]):
        need(req_ids, "interaction.selection_visible", "the chosen option must read as selected, distinct from focus")
    if "state.unsaved_changes_guard" in req_ids:
        need(req_ids, "feedback.confirmation_destructive", "discarding unsaved work needs a confirmation with a safe default")
        need(req_ids, "a11y.dialog_focus", "the unsaved-changes prompt is a dialog")
    if "touch.gestures_discoverable" in req_ids or _count(text, ["drag*", "swipe to", "long-press", "long press"]):
        need(req_ids, "interaction.keyboard_navigation", "every gesture needs a keyboard/button alternative"); need(rec_ids, "a11y.live_status", "announce the result of a drag")
    if _count(text, ["spinner", "progress", "what is happening", "what's happening", "never says", "still working"]):
        need(req_ids, "feedback.progress_indicator", "progress feedback"); need(req_ids, "a11y.live_status", "status changes are announced")
    if _count(text, ["language switch", "language toggle", "spanish", "translation*", "translate*", "localis*", "localiz*", "multilingual", "second language"]):
        need(req_ids, "content.i18n_expansion", "second language / localisation"); need(rec_ids, "a11y.live_status", "language change announced")
    phase["p"] = 1
    if primary == "accessibility" or (primary in ("audit", "review") and "accessib" in req["query"].lower()):
        if not (plats and plats <= {"mobile", "tablet"} and "keyboard" not in known_inputs):
            need(req_ids, "interaction.keyboard_navigation", "accessibility review: keyboard operability")
        if plats & {"mobile", "tablet", "kiosk"} or "touch" in known_inputs:
            need(req_ids, "touch.minimum_target", "accessibility review on a touch platform: target size")
    phase["p"] = 2
    if _count(text, ["validation error*", "validation message*", "error message*", "inline error*", "field error*"]):
        need(req_ids, "feedback.validation_errors", "validation wording"); need(req_ids, "a11y.contrast", "readability of error text")
    if _count(text, ["hard to read", "unreadable", "can't read", "cannot read", "too faint", "low contrast", "impossible to read", "difficult to read", "readable", "legible", "illegible", "washed out"]):
        need(req_ids, "a11y.contrast", "readability problem")
    if "web" in plats and plats & {"mobile", "tablet"}:
        need(req_ids, "touch.minimum_target", "responsive web used on phones")
    if req.get("constraints", {}).get("preserve_existing_system") and primary in ("polish", "refactor", "create", "accessibility", "audit", "responsive"):
        phase["p"] = 1
        need(req_ids if primary in ("polish", "refactor", "create", "responsive") else rec_ids, "process.reuse_first", "existing repository: reuse its primitives")
        phase["p"] = 2

    # 3. platform + input matrix — required only when the task has interactive evidence; a static text page or a
    #    single visual tweak keeps them as recommendations (Phase 6: criticality is conditional)
    phase["p"] = 3
    interactive = bool(comps or screens or jobs or subtypes or form_like or data_like or _count(text, ["button*", "tap*", "click*", "keyboard", "focus", "drag*", "swipe*", "scroll*", "select*", "menu*", "control*", "input*", "gesture*", "navigate*", "navigation"]))
    if not interactive or static_page:
        _req_platform = req_ids
        req_ids = rec_ids   # demand platform generics as recommendations only
    if "web" in plats:
        need(req_ids, "interaction.keyboard_navigation", "web content must be keyboard operable")
        need(req_ids, "interaction.hover_independence", "web is used with touch as well as pointer")
        need(req_ids, "interaction.focus_visible", "web keyboard focus")
        need(rec_ids, "touch.minimum_target", "touch on web"); need(rec_ids, "adaptive.breakpoint_matrix", "web viewport range")
    if "desktop" in plats:
        need(req_ids, "interaction.keyboard_navigation", "desktop keyboard-first"); need(req_ids, "interaction.focus_visible", "desktop focus")
        need(rec_ids, "interaction.shortcuts", "desktop accelerators"); need(rec_ids, "desktop.persist_workspace", "desktop state persistence")
        need(opt_ids, "desktop.spacing_grid", "desktop spacing")
        if set(req.get("stack", [])) & {"winui", "wpf"}:
            need(rec_ids, "desktop.fluent_materials", "Windows stack")
    if plats & {"mobile", "tablet", "kiosk"} or "touch" in known_inputs:
        need(req_ids, "touch.minimum_target", "touch platform")
        need(rec_ids, "touch.gestures_discoverable", "touch platform"); need(rec_ids, "touch.thumb_reach", "one-handed use")
        if "mobile" in plats:
            need(rec_ids, "touch.safe_areas", "mobile"); need(rec_ids, "navigation.platform_grammar", "mobile navigation grammar")
    if "tablet" in plats:
        need(rec_ids, "adaptive.breakpoint_matrix", "tablet widths")
    if "tv" in plats or "remote" in inputs:
        for c in ("interaction.dpad_reachability", "interaction.focus_restore", "interaction.focus_visible", "tv.ten_foot_typography", "tv.safe_margins"):
            need(req_ids, c, "TV / remote input")
        need(rec_ids, "interaction.back_semantics", "remote input"); need(rec_ids, "tv.no_touch_hover", "tv"); need(rec_ids, "perf.focus_latency", "tv"); need(rec_ids, "tv.dark_first", "tv")
    if "keyboard" in known_inputs:
        need(req_ids, "interaction.keyboard_navigation", "keyboard stated"); need(req_ids, "interaction.focus_visible", "keyboard stated")
    if "pointer" in known_inputs:
        need(req_ids, "interaction.hover_independence", "pointer stated")
    if "kiosk" in plats:
        need(req_ids, "privacy.shared_device", "kiosk"); need(req_ids, "state.session_expiry", "kiosk idle reset"); need(rec_ids, "env.glanceable_status", "kiosk")
    if not interactive or static_page:
        req_ids = _req_platform

    # 4. screens / subtypes / components / jobs
    phase["p"] = 1
    if form_like:
        validation_cue = bool(ops_create) or bool(_count(text, ["validat*", "error*", "submit*", "required field*", "invalid", "reject*", "typo*", "enter*", "input*", "checkout", "sign in", "sign-in", "log in", "login", "register", "invite"]))
        need(req_ids if validation_cue else rec_ids, "feedback.validation_errors", "form"); need(rec_ids, "form.autofill_attributes", "form")
        if plats & {"mobile", "tablet"} or "touch" in known_inputs or _count(text, ["keyboard open", "keyboard is open", "on-screen keyboard"]):
            need(req_ids, "touch.ime_keyboard", "form on touch")
    elif screens & {"settings"} or comps & {"notification", "dialog", "button"}:
        need(rec_ids, "a11y.live_status", "status messages")
    if screens & {"settings"}:
        need(req_ids, "layout.settings_grouping", "settings screen")
    if data_like:
        if grid_like or "compare" in jobs or _count(text, ["amount*", "total*", "price*", "figure*", "number*", "column*", "align*", "line up", "currency", "decimal*", "transfer*", "payment*", "wire", "balance*", "invoice*", "quota", "usage", "kpi*", "metric*", "cost*"]):
            need(req_ids, "table.tabular_figures", "numeric data")
        elif prods & {"finance", "erp"}:
            phase["p"] = 2; need(req_ids, "table.tabular_figures", "numeric product (baseline)"); phase["p"] = 1
        if grid_like:
            need(req_ids if plats & {"mobile", "tablet"} else rec_ids, "table.column_priority", "table on narrower widths")
            need(rec_ids, "table.virtualization", "large collections"); need(rec_ids, "table.selection_bulk", "table rows")
            if _count(text, ["selection", "selected", "select rows", "per-row"]) or "desktop" in plats:
                need(req_ids if _count(text, ["selection", "selected", "per-row"]) else rec_ids, "interaction.selection_visible", "selectable rows")
            if _count(text, ["50,000", "50000", "100k", "thousands", "large", "huge", "giant", "big table"]):
                need(req_ids, "table.virtualization", "large collection stated")
            if "enter-data" in jobs or _count(text, ["edit", "editing", "editable", "entry", "enter"]):
                need(req_ids, "table.inline_edit", "editable grid")
        if screens & {"dashboard"} or comps & {"chart"}:
            phase["p"] = 1 if "chart" in comps else 2
            need(req_ids, "data.chart_by_question", "charts"); need(req_ids, "a11y.color_not_only", "status and series colour")
            phase["p"] = 1
            need(rec_ids, "data.accessible_chart_alternative", "charts"); need(rec_ids, "data.exception_first", "dashboard focal point"); need(rec_ids, "data.drilldown", "dashboard to detail")
            need(rec_ids, "data.kpi_comparison", "KPIs"); need(rec_ids, "layout.focal_hierarchy", "dashboard hierarchy")
        if screens & {"list"} or comps & {"list"}:
            need(rec_ids, "data.pagination_strategy", "long lists")
    if comps & {"search"} or screens & {"search"}:
        need(req_ids, "data.search_results", "search"); need(rec_ids, "data.filter_chips", "search filters"); need(rec_ids, "a11y.live_status", "result count")
        if "tv" in plats:
            need(req_ids, "media.search_tv", "TV search")
    if _count(text, ["filter", "filters", "facet", "facets"]):
        need(req_ids, "data.filter_chips", "filters mentioned")
    if screens & {"player"} or comps & {"media"} and "player" in text:
        if plats & {"tv"} or "remote" in inputs:
            need(req_ids, "tv.player_autohide", "player on remote"); need(req_ids, "interaction.back_semantics", "player on remote")
            need(rec_ids, "media.track_selection", "player controls")
        else:
            need(rec_ids, "a11y.reduced_motion", "player motion")
        if _count(text, ["subtitle*", "caption*", "audio track*", "audio selection"]):
            need(req_ids, "media.track_selection", "subtitle/audio selection")
    if screens & {"checkout"}:
        need(req_ids, "layout.one_primary_action", "checkout"); need(req_ids, "feedback.trust_signals", "commitment step")
        if _count(text, ["three steps", "3 steps", "multi-step", "multistep", "steps"]):
            need(req_ids, "feedback.progress_indicator", "multi-step checkout")
    if "media" in prods and plats & {"tv"} and screens & {"detail"}:
        need(req_ids, "interaction.focus_restore", "details opened from a rail returns to it"); need(req_ids, "interaction.back_semantics", "details BACK")
    if "media" in prods and plats & {"tv"}:
        if screens & {"home"} or subtypes & {"rails"}:
            need(req_ids, "layout.media_card", "TV browse"); need(rec_ids, "media.resume_playback", "TV home commonly resumes")
        if screens & {"detail"}:
            need(req_ids, "media.details_play_first", "media details"); need(rec_ids, "media.watchlist", "media details")
    for j in sorted(jobs):
        for n, c in enumerate(JOB_CONCEPTS.get(j, [])):
            need(req_ids if n < 3 else rec_ids, c, f"job {j}")
    if "compare" in jobs and _count(text, ["revenue", "sales", "metric*", "numbers", "values", "totals", "trend*", "kpi*", "spend", "traffic", "conversion*", "counts", "over time", "by region", "by month", "monthly", "weekly", "quarterly", "percent", "last week", "this week", "last month"]):
        need(req_ids, "data.kpi_comparison", "compare numbers"); need(req_ids, "data.chart_by_question", "compare numbers"); need(rec_ids, "table.tabular_figures", "compare numbers")
    for st in sorted(subtypes):
        for n, c in enumerate(SUBTYPE_CONCEPTS.get(st, [])):
            need(req_ids if n < 2 else rec_ids, c, f"screen subtype {st}")
    if screens & {"onboarding"} and not (subtypes & {"wizard", "permissions", "feature-tour", "checklist"}) and not (jobs & {"permissions", "feature-education"}):
        need(rec_ids, "onboarding.setup_checklist", "onboarding"); need(rec_ids, "feedback.progress_indicator", "onboarding")
    if comps & {"dialog"}:
        need(req_ids, "a11y.dialog_focus", "dialog"); need(rec_ids, "feedback.confirmation_destructive", "dialog")
    if comps & {"navigation"} or screens & {"home"}:
        need(rec_ids, "navigation.orientation_and_back", "navigation surface")
    if comps & {"card"}:
        need(rec_ids, "layout.no_nested_cards", "cards")
    if _count(text, ["tree", "file tree", "hierarchy panel"]):
        need(req_ids, "interaction.tree_semantics", "tree view")
    if _count(text, ["tabs", "tab bar", "tabbed"]) and "tv" not in plats:
        need(rec_ids, "interaction.tabs_roving", "tabs")
    if _count(text, ["menu", "dropdown", "context menu"]):
        need(rec_ids, "interaction.menu_semantics", "menu")
    if _count(text, ["drawer", "side panel", "side sheet"]):
        need(rec_ids, "interaction.drawer_focus", "drawer")
    if _count(text, ["command palette", "cmd+k", "ctrl+k"]):
        need(req_ids, "interaction.command_palette", "command palette")
    if _count(text, ["virtualize", "virtualise", "virtualized", "scrolling freezes", "10k", "thousands of rows", "large list"]):
        need(req_ids, "table.virtualization", "large collection / scroll performance")
    if _count(text, ["cls", "layout shift", "jumps when", "shifts when"]):
        need(req_ids, "perf.layout_shift", "layout shift wording")
    if _count(text, ["icon button", "icon-only", "icon buttons"]):
        need(req_ids, "a11y.accessible_names", "icon-only controls")
    if _count(text, ["focus indicator", "focus ring", "visible focus"]):
        need(req_ids, "interaction.focus_visible", "focus wording")
    if _count(text, ["modal", "dialog"]) and _count(text, ["focus"]):
        need(req_ids, "a11y.dialog_focus", "modal focus wording")

    # 5. risk / environment
    phase["p"] = 1
    if req["risk"] == "high":
        need(req_ids, "feedback.confirmation_destructive", "high-risk job")
    elif req["risk"] == "medium":
        need(rec_ids, "feedback.confirmation_destructive", "sensitive domain")
    if prods & {"finance", "healthcare"} and (plats & {"tv", "kiosk", "tablet"} or envs & {"shared-device", "public"}):
        phase["p"] = 1 if envs & {"shared-device", "public"} else 2
        need(req_ids, "privacy.shared_device", "sensitive data on a shared screen"); need(req_ids, "privacy.sensitive_masking", "balances / health data visible to onlookers")
        phase["p"] = 1
    for e in sorted(envs):
        ev_e = req["evidence"]["environment"].get(e, {})
        st = ev_e.get("status", "INFERRED"); from_request = str(ev_e.get("reason", "")).startswith("request")
        phase["p"] = 1 if from_request else 2
        for c in ENVIRONMENT_CONCEPTS.get(e, []):
            need(req_ids if st == "KNOWN" else rec_ids, c, f"environment {e}" + ("" if from_request else " (repository hint)"))
        phase["p"] = 1

    # 6. constraints
    phase["p"] = 2
    if "animation" in req["negative_constraints"]:
        need(req_ids, "a11y.reduced_motion", "no-animation constraint")
    if req["negative_constraints"]:
        for lab in req["negative_constraints"]:
            if lab in ("gradient", "glass"):
                need(rec_ids, "anti.decorative_gradient", "exclusion " + lab)
            if lab == "card":
                need(rec_ids, "layout.no_nested_cards", "exclusion card")
    if primary in ("create", "brand", "design-system") and not marketing_page:
        need(opt_ids, "brand.corner_language", "visual identity"); need(opt_ids, "anti.default_fonts", "visual identity")

    # narrow task (Phase 6): the request names a specific principle and the change is local -> demands derived only
    #  from the screen/job stay recommendations (they would pull whole-screen guidance into a one-element fix)
    if _count(text, ["submit*", "submission", "save", "saving", "upload*", "load", "loads", "loading", "sync*", "fetch*", "api", "refresh*", "spinner", "no sign", "nothing happen*", "waiting"]):
        for c_ in ("state.loading_empty_error", "feedback.progress_indicator"):
            if c_ in req_ids and prio.get(c_, 9) > 1:
                prio[c_] = 1
    named = [c for c in req_ids if prio.get(c, 9) == 0]
    ops_ = set((req.get("intent") or {}).get("operations", []))
    if named and not jobs and (req.get("intent") or {}).get("change_scope") != "system" and not _count(text, ["end to end", "end-to-end", "whole flow", "entire flow", "the flow"]) and ops_ <= {"modify", "diagnose", "polish", "inspect"} and primary not in ("create", "brand", "design-system"):
        keep_states = bool(_count(text, ["submit*", "submission", "save", "saving", "upload*", "load", "loads", "loading", "sync*"]))
        for c in list(req_ids):
            if prio.get(c, 9) >= 1 and c not in named and not (prio.get(c, 9) == 3 and plats & {"tv", "kiosk"}) and not (keep_states and c in ("state.loading_empty_error", "feedback.progress_indicator", "a11y.live_status")):
                rec_ids.setdefault(c, req_ids.pop(c) + " (narrow task: kept as a recommendation)")
    # saturation: keep the most task-specific required concepts (priority, then insertion order); demote the rest
    if len(req_ids) > REQUIRED_CAP:
        order = sorted(req_ids, key=lambda c: (prio.get(c, 9), list(req_ids).index(c)))
        for c in order[REQUIRED_CAP:]:
            rec_ids.setdefault(c, req_ids.pop(c) + " (demoted: saturation cap)")
    # closure and conflicts
    closed = requires_closure(list(req_ids))
    for c in closed:
        if c not in req_ids:
            req_ids[c] = "required by " + next((k for k in req_ids if c in RELATIONS.get(k, {}).get("requires", [])), "a required concept")
            rec_ids.pop(c, None); opt_ids.pop(c, None)
    for c in list(req_ids):
        for r in RELATIONS.get(c, {}).get("related", []):
            if r not in req_ids:
                need(rec_ids, r, f"related to {c}")
    for c in list(req_ids):
        for x in RELATIONS.get(c, {}).get("conflicts", []):
            rec_ids.pop(x, None); opt_ids.pop(x, None)
    # Phase 6: criticality is conditional on how the demand arose — named in the request (0) or derived from the
    # task's job / screen / environment / risk (1) is critical; mode/states (2) and platform generics (3) are not.
    return {"version": CONCEPT_POLICY_VERSION,
            "required": [{"id": c, "reason": r, "priority": prio.get(c, 2), "critical": prio.get(c, 2) <= 1} for c, r in req_ids.items()],
            "recommended": [{"id": c, "reason": r} for c, r in rec_ids.items()],
            "optional": [{"id": c, "reason": r} for c, r in opt_ids.items()]}
