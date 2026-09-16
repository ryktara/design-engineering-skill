#!/usr/bin/env python3
"""design-engineering core: knowledge, requirements contract, concerns, candidate ranking,
guidance-bundle selection, direction assembly.

Stdlib only. Deterministic. Tunables live in data/lexicon.json and data/*.jsonl.

Pipeline:  request (+ project inspection)
           -> build_requirements()            DesignRequirements (design-requirements/v1)
           -> derive_concerns(requirements)   REQUIRED / RECOMMENDED / OPTIONAL concerns (+ concept ids)
           -> candidates(query, requirements) scored records (lexical + structural, filtered)
           -> select_bundle(...)              GuidanceBundle: core + guardrails covering concerns
           -> direction()                     visual slots + guardrails from the bundle
`search()` remains the raw ranked lookup for debugging.
"""

from __future__ import annotations

import difflib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import de_semantic as sem  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

REQUIREMENTS_SCHEMA = "design-requirements/v1"
BUNDLE_SCHEMA = "guidance-bundle/v2"
CHANGE_BUDGETS = {"low", "moderate", "high", "greenfield"}

KINDS = {"pattern", "rule", "direction", "component", "chart", "antipattern"}
MODES = {"create", "design-system", "audit", "refactor", "polish", "accessibility",
         "responsive", "brand", "reconstruct", "review"}
PLATFORMS = {"web", "mobile", "tablet", "desktop", "tv", "kiosk", "any"}
INPUTS = {"touch", "pointer", "keyboard", "remote", "any"}
PRODUCTS = {"saas", "erp", "ecommerce", "finance", "media", "healthcare", "marketing",
            "devtools", "content", "social", "education", "government", "iot", "any"}
DENSITY = {"low", "medium", "high", "any"}
SCREENS = {"home", "detail", "list", "form", "settings", "player", "search", "dashboard", "auth",
           "onboarding", "checkout", "landing", "any"}
SCREEN_SUBTYPES = {"epg", "data-grid", "wizard", "sign-in", "hero", "rails", "feed", "chat", "map", "calendar", "permissions", "feature-tour", "checklist", "catalog"}
ENVIRONMENTS = {"outdoor", "shared-device", "public", "large-display", "low-bandwidth", "low-light", "gloves", "noisy"}
RISK = {"low", "medium", "high"}
PROVENANCE = {"platform-standard", "accessibility-requirement", "engineering-practice",
              "heuristic", "aesthetic", "internal-preference", "upstream-derived-concept"}
STACK_GROUPS = {"react", "nextjs", "vue", "nuxt", "svelte", "angular", "astro", "html-css",
                "tailwind", "shadcn", "compose", "compose-tv", "swiftui", "flutter",
                "react-native", "winui", "wpf", "avalonia", "any"}
NEGATIVE_LABELS = {"card", "gradient", "glass", "sidebar", "animation", "icon", "pill", "hero", "rails",
                   "navigation-change", "typography-change", "dependencies", "hover", "remote-only",
                   "keyboard-only", "touch-only"}
NEGATIVE_RECORD_TERMS = {
    "card": ["card", "cards", "tile", "tiles"], "gradient": ["gradient"], "glass": ["glass", "glassmorphism", "blur"],
    "sidebar": ["sidebar", "left rail", "rail"], "animation": ["animation", "motion", "cinematic", "spring", "expressive"],
    "icon": ["icon", "icons"], "pill": ["pill", "pills", "chip", "chips", "badge"], "hero": ["hero"],
    "rails": ["rail", "rails", "carousel"], "hover": ["hover"],
}

# Concern taxonomy: what a task must get right. Records address concerns; requirements demand them.
CONCERNS = {"structure", "navigation", "component", "interaction", "accessibility", "content", "data-display",
            "adaptive", "states", "feedback", "performance", "privacy", "environment", "brand", "motion", "anti-pattern"}

# Canonical concept ids live in de_semantic.CONCEPT_META (concept-policy/v1).
CONCEPTS = sem.CONCEPTS
CONCEPT_LABELS = sem.CONCEPT_LABELS

# mode tie-break: a specific mode word beats the generic 'create' when scores tie
MODE_PRIORITY = ["accessibility", "audit", "review", "brand", "design-system", "responsive", "reconstruct", "refactor", "polish", "create"]

REQUIRED_FIELDS = ("id", "kind", "title", "category", "intent", "platform", "input",
                   "product_fit", "density", "risk", "use_when", "avoid_when",
                   "compatible", "incompatible", "guidance", "provenance", "source",
                   "version", "keywords")

FINGERPRINT_AXES = {
    "navigation_model": 3.0, "layout_topology": 3.0, "content_density": 2.0, "grid_behavior": 2.0,
    "card_geometry": 1.5, "corner_language": 0.75, "typography_character": 1.0, "color_strategy": 0.75,
    "surface_strategy": 1.5, "image_strategy": 1.5, "icon_strategy": 0.75, "motion_character": 1.0,
    "focus_strategy": 1.0, "metadata_density": 1.5, "cta_strategy": 1.5,
}
STRUCTURAL_AXES = {"navigation_model", "layout_topology", "content_density", "grid_behavior",
                   "surface_strategy", "image_strategy", "metadata_density", "cta_strategy", "card_geometry"}

DIRECTION_SLOTS = ["navigation", "layout", "density", "surface", "cards", "typography", "color",
                   "motion", "focus", "cta", "imagery", "icon", "metadata"]

# Facets (Phase 2): the record's own concern type, used for diversity metrics.
FACETS = {"component", "layout", "navigation", "visual", "interaction", "accessibility", "performance",
          "process", "direction", "anti-pattern", "data-viz", "platform"}
_PATTERN_FACET = {"navigation": "navigation", "layout": "layout", "density": "layout", "cards": "layout",
                  "surface": "layout", "metadata": "layout", "cta": "layout", "typography": "visual",
                  "color": "visual", "imagery": "visual", "icon": "visual", "motion": "visual", "focus": "interaction"}
_RULE_FACET = {"accessibility": "accessibility", "focus": "interaction", "input": "interaction",
               "navigation": "navigation", "layout": "layout", "typography": "visual", "color": "visual",
               "motion": "visual", "performance": "performance", "implementation": "process",
               "verification": "process", "forms": "component", "feedback": "component", "content": "visual",
               "responsive": "layout", "player": "component", "search": "component", "table": "component",
               "dialog": "component", "surface": "layout", "states": "component", "privacy": "accessibility",
               "environment": "accessibility"}

# Derived concerns by kind/category (records may declare `concerns` to override).
_PATTERN_CONCERNS = {"navigation": {"navigation"}, "layout": {"structure"}, "density": {"structure"}, "cards": {"structure"},
                     "surface": {"structure", "brand"}, "metadata": {"structure", "content"}, "cta": {"structure", "interaction"},
                     "typography": {"content", "brand"}, "color": {"brand", "accessibility"}, "imagery": {"brand", "content"},
                     "icon": {"brand", "content"}, "motion": {"motion"}, "focus": {"interaction", "accessibility"}}
_RULE_CONCERNS = {"accessibility": {"accessibility"}, "focus": {"interaction", "accessibility"}, "input": {"interaction"},
                  "navigation": {"navigation"}, "layout": {"structure"}, "typography": {"content"}, "color": {"brand", "accessibility"},
                  "motion": {"motion", "accessibility"}, "performance": {"performance"}, "implementation": set(), "verification": set(),
                  "forms": {"feedback", "component"}, "feedback": {"feedback", "states"}, "content": {"content", "adaptive"},
                  "responsive": {"adaptive"}, "player": {"component", "interaction"}, "search": {"component"}, "table": {"data-display"},
                  "dialog": {"component", "interaction"}, "surface": {"structure"}, "states": {"states"}, "privacy": {"privacy"},
                  "environment": {"environment"}}
# screen-level components (settings, form, table, epg, player, wizard, hero, sign-in, list) define the screen's
# structure, so they carry the "structure" concern as well.
_COMPONENT_CONCERNS = {"table": {"component", "data-display", "structure"}, "form": {"component", "feedback", "structure"}, "chart": {"data-display"},
                       "empty-state": {"states"}, "notification": {"feedback", "states"}, "player": {"component", "interaction", "structure"},
                       "tv-rail": {"component", "navigation"}, "epg": {"component", "data-display", "navigation", "structure"},
                       "wizard": {"component", "feedback", "structure"}, "command-palette": {"component", "interaction"},
                       "menu": {"component", "interaction"}, "tabs": {"component", "navigation"}, "navigation": {"navigation"},
                       "sign-in": {"component", "privacy", "feedback", "structure"}, "settings": {"component", "structure"},
                       "hero": {"component", "structure", "content"}, "list": {"component", "structure"}, "drawer": {"component", "navigation"},
                       "tree": {"component", "navigation"}, "media-card": {"component", "content"}, "search": {"component", "feedback"}}


def record_facets(rec: dict) -> set[str]:
    kind, cat = rec["kind"], rec["category"]
    if kind == "component":
        f = {"component"}
    elif kind == "pattern":
        f = {_PATTERN_FACET.get(cat, "layout")}
    elif kind == "rule":
        f = {_RULE_FACET.get(cat, "process")}
    elif kind == "direction":
        f = {"direction"}
    elif kind == "antipattern":
        f = {"anti-pattern"}
    else:
        f = {"data-viz"}
    if "any" not in rec["platform"]:
        f.add("platform")
    return f


def record_concerns(rec: dict) -> set[str]:
    if rec.get("concerns"):
        return set(rec["concerns"])
    kind, cat = rec["kind"], rec["category"]
    if kind == "component":
        return set(_COMPONENT_CONCERNS.get(cat, {"component"}))
    if kind == "pattern":
        return set(_PATTERN_CONCERNS.get(cat, {"structure"}))
    if kind == "rule":
        return set(_RULE_CONCERNS.get(cat, set()))
    if kind == "direction":
        return {"structure", "brand"}
    if kind == "antipattern":
        return {"anti-pattern"}
    return {"data-display"}


_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#.-]*")
_STOP = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "is",
         "it", "as", "at", "by", "be", "this", "that", "my", "our", "we", "i", "me",
         "make", "please", "need", "want", "some", "can", "you", "should", "into",
         "screen", "app", "application", "page", "ui", "design", "user", "users", "new", "service"}
# limited normalisation for vocabulary variants seen in practice (Phase 3; not tuned on held-out)
_TOKEN_ALIASES = {"pinned": "sticky", "pin": "sticky", "autohide": "auto-hide", "autohides": "auto-hide", "auto-hides": "auto-hide",
                  "10-foot": "ten-foot", "10ft": "ten-foot", "tenfoot": "ten-foot", "colour": "color", "colours": "color",
                  "grey": "gray", "virtualisation": "virtualization", "virtualise": "virtualize", "virtualised": "virtualized",
                  "behaviour": "behavior", "favourite": "favorite", "prioritise": "prioritize", "prioritised": "prioritized"}


def _tokens(text: str) -> list[str]:
    out = []
    for t in _TOKEN_RE.findall(str(text).lower()):
        t = t.strip(".-")
        if len(t) < 2 or t in _STOP:
            continue
        t = _TOKEN_ALIASES.get(t, t)
        if "-" in t and t not in _TOKEN_ALIASES.values():
            for part in t.split("-"):
                if len(part) >= 3 and part not in _STOP:
                    out.append(part[:-1] if (len(part) > 3 and part.endswith("s") and not part.endswith("ss")) else part)
        if len(t) > 4 and t.endswith("ies"):
            t = t[:-3] + "y"
        elif len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        out.append(_TOKEN_ALIASES.get(t, t))
    return out


# ---------------------------------------------------------------------------
# Loading / validation
# ---------------------------------------------------------------------------

_cache: dict = {}


def load_lexicon() -> dict:
    if "lexicon" not in _cache:
        _cache["lexicon"] = json.loads((DATA_DIR / "lexicon.json").read_text(encoding="utf-8"))
    return _cache["lexicon"]


def load_records(data_dir: Path | None = None) -> list[dict]:
    data_dir = data_dir or DATA_DIR
    key = ("records", str(data_dir))
    if key in _cache:
        return _cache[key]
    records = []
    for path in sorted(data_dir.glob("*.jsonl")):
        with path.open(encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"{path.name}:{n}: invalid JSON: {e}") from e
                rec["_file"] = path.name
                rec["_line"] = n
                records.append(rec)
    _cache[key] = records
    return records


def validate_record(rec: dict, known_ids: set[str] | None = None) -> list[str]:
    errs = []
    where = f"{rec.get('_file', '?')}:{rec.get('_line', '?')} [{rec.get('id', '?')}]"
    for f in REQUIRED_FIELDS:
        if f not in rec:
            errs.append(f"{where}: missing field '{f}'")
    if errs:
        return errs
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", rec["id"]):
        errs.append(f"{where}: id must be kebab-case")
    if rec["kind"] not in KINDS:
        errs.append(f"{where}: kind '{rec['kind']}' not in {sorted(KINDS)}")
    for field, allowed in (("intent", MODES), ("platform", PLATFORMS), ("input", INPUTS), ("product_fit", PRODUCTS)):
        vals = rec[field]
        if not isinstance(vals, list) or not vals:
            errs.append(f"{where}: {field} must be a non-empty list")
            continue
        bad = [v for v in vals if v not in allowed]
        if bad:
            errs.append(f"{where}: {field} has unknown values {bad}; allowed {sorted(allowed)}")
    if rec["density"] not in DENSITY:
        errs.append(f"{where}: density '{rec['density']}' not in {sorted(DENSITY)}")
    risk = rec["risk"]
    if not isinstance(risk, dict) or set(risk) != {"a11y", "perf"} or any(v not in RISK for v in risk.values()):
        errs.append(f"{where}: risk must be {{'a11y': low|medium|high, 'perf': ...}}")
    if rec["provenance"] not in PROVENANCE:
        errs.append(f"{where}: provenance '{rec['provenance']}' not in {sorted(PROVENANCE)}")
    for field in ("compatible", "incompatible", "keywords"):
        if not isinstance(rec[field], list):
            errs.append(f"{where}: {field} must be a list")
    if not isinstance(rec["guidance"], str) or len(rec["guidance"]) < 20:
        errs.append(f"{where}: guidance must be a sentence or more")
    if len(rec["guidance"]) > 900:
        errs.append(f"{where}: guidance is {len(rec['guidance'])} chars; keep records under 900")
    impl = rec.get("implementation", {})
    if impl and (not isinstance(impl, dict) or any(k not in STACK_GROUPS for k in impl)):
        errs.append(f"{where}: implementation keys must be stack groups {sorted(STACK_GROUPS)}")
    sf = rec.get("screen_fit", ["any"])
    if not isinstance(sf, list) or not sf or any(v not in SCREENS for v in sf):
        errs.append(f"{where}: screen_fit must be a non-empty list from {sorted(SCREENS)}")
    if "rank" in rec and (not isinstance(rec["rank"], int) or not 0 <= rec["rank"] <= 100):
        errs.append(f"{where}: rank must be an integer 0-100")
    fp = rec.get("fingerprint", {})
    if fp and (not isinstance(fp, dict) or any(k not in FINGERPRINT_AXES for k in fp)):
        errs.append(f"{where}: fingerprint keys must be in {sorted(FINGERPRINT_AXES)}")
    if rec["kind"] == "pattern" and rec["category"] in DIRECTION_SLOTS and not fp:
        errs.append(f"{where}: pattern in slot '{rec['category']}' needs a fingerprint entry")
    if not record_facets(rec) <= FACETS:
        errs.append(f"{where}: derived facets {record_facets(rec)} outside {sorted(FACETS)}")
    if rec.get("concerns") is not None:
        if not isinstance(rec["concerns"], list) or not rec["concerns"] or not set(rec["concerns"]) <= CONCERNS:
            errs.append(f"{where}: concerns must be a non-empty list from {sorted(CONCERNS)}")
    if rec.get("concepts") is not None:
        if not isinstance(rec["concepts"], list) or not set(rec["concepts"]) <= CONCEPTS:
            errs.append(f"{where}: concepts has unknown ids {sorted(set(rec.get('concepts', [])) - CONCEPTS)}")
    if rec.get("environment") is not None and not set(rec["environment"]) <= ENVIRONMENTS:
        errs.append(f"{where}: environment has unknown values")
    if known_ids is not None:
        for field in ("compatible", "incompatible"):
            for ref in rec[field]:
                if ref not in known_ids:
                    errs.append(f"{where}: {field} references unknown id '{ref}'")
        if rec["id"] in rec["incompatible"]:
            errs.append(f"{where}: record is incompatible with itself")
    return errs


# ---------------------------------------------------------------------------
# Signal extraction
# ---------------------------------------------------------------------------

def _phrase_re(phrase: str) -> re.Pattern:
    words = [re.escape(w) for w in phrase.lower().split()]
    words[-1] = words[-1] + r"(?:s|es)?"
    return re.compile(r"(?<![a-z0-9])" + r"[\s-]+".join(words) + r"(?![a-z0-9])")


_LEX_GROUPS = ("modes", "platforms", "platforms_inferred", "inputs", "products", "density", "stacks", "components", "screens",
               "negatives", "constraints", "problems", "environment", "jobs", "screen_subtypes")


def _compiled_lexicon() -> dict:
    if "compiled" in _cache:
        return _cache["compiled"]
    lex = load_lexicon()
    comp = {}
    for group in _LEX_GROUPS:
        comp[group] = {}
        for label, phrases in lex.get(group, {}).items():
            comp[group][label] = [(p, _phrase_re(p)) for p in phrases]
    comp["ui_vocab"] = [(p, _phrase_re(p)) for p in lex.get("ui_vocab", [])]
    comp["non_ui_vocab"] = [(p, _phrase_re(p)) for p in lex.get("non_ui_vocab", [])]
    _cache["compiled"] = comp
    return comp


def _hits(text: str, entries) -> list[str]:
    return [p for p, rx in entries if rx.search(text)]


def _pick(text: str, group: str) -> dict:
    found = {}
    for label, entries in _compiled_lexicon()[group].items():
        h = _hits(text, entries)
        if h:
            found[label] = h
    return found


def _activation(ui_hits, non_ui_hits, modes, plat, components, stacks=()) -> dict:
    # a UI framework word breaks a tie toward UI only when a UI term is present and no non-UI term is
    ui_score = len(ui_hits) + len(modes) * 1.0 + (1 if plat else 0) + (1 if components else 0) + (1 if (stacks and ui_hits and not non_ui_hits) else 0)
    non_ui_score = len(non_ui_hits)
    if not ui_hits and not modes and not components:
        ui_score = 0
    if ui_score >= 2 and ui_score > non_ui_score:
        decision = "activate"
    elif ui_score == 0 or non_ui_score >= ui_score + 1:
        decision = "skip"
    else:
        decision = "ambiguous"
    return {"decision": decision, "ui_score": ui_score, "non_ui_score": non_ui_score,
            "ui_terms": ui_hits, "non_ui_terms": non_ui_hits}


# ---------------------------------------------------------------------------
# DesignRequirements contract
# ---------------------------------------------------------------------------

_FORM_FACTOR_WORDS = {"phone", "phones", "on phones", "on the phone", "on a phone", "smartphone", "smartphones", "mobile", "on mobile", "handset", "handsets", "small screens", "small screen"}


def _hints_to_project(hints: dict | None) -> dict | None:
    if not hints:
        return None
    return {"platforms": hints.get("platforms", []), "stack_groups": hints.get("stacks", []),
            "product_hints": hints.get("products", []), "findings": [], "_from_hints": True}







_REFERENCE_CLAUSE_RE = re.compile(r"(?:without (?:changing|redesigning|touching)|keeping|keep(?:ing)? the|matching the|consistent with|in (?:its|the)(?: app's)? existing|like the existing|same style as|do not change|don't change|against (?:our|the|a|an|your) [a-z -]*(?:checklist|guideline|guidelines|standard|standards|policy|spec))\b[^,.;]*", re.I)


_TOKEN_TRAPS = [
    (r"\b(?:press(?:ing|es)? |hit(?:ting)? |the |a )?tab key\b|\bpress(?:ing|es)? tab\b|\bshift[- ]tab\b|\bshift\+tab\b|\btab order\b|\btab stops?\b|\btabbing\b|\btab through\b|\btab to the\b|\btab (?:into|out of|between)\b|\btab skips\b|\b(?:hit|hits|hitting|using|via|with) tab\b|\btab (?:twenty|\d+) times\b|\btab (?:to reach|to get)\b", " keyfocusstep "),
    (r"\bbrowser tabs?\b|\bnew tab\b|\btab title\b|\bopens? (?:in )?a (?:new )?tab\b", " browserpane "),
    (r"\blandscape (?:orientation|mode|tablets?|phones?|photos?|images?|pictures?|shots?)\b|\bto landscape\b|\bin landscape\b", " wideorientation "),
    (r"\b(cookie|consent|loading|modal|map|tutorial|onboarding|error|blocking) overlay\b", r"\1 layer"), (r"\boverlay on the (?:map|form|page|chart|grid)\b", " layer "),
    (r"\bterminal (?:output|window|emulator|session|command|commands|log|logs)\b|\bin the terminal\b|\bcommand[- ]line\b", " console "),
    (r"\bplayer (?:profiles?|stats|pages?|cards?)\b|\bplayers'\b|\bplayers (?:list|roster|profiles?)\b|\bteam players?\b", " memberprofile "),
    (r"\b(?:credit|debit|payment|gift|loyalty|id|membership|sim|sd) cards?\b|\bcard (?:reader|number|numbers|details|entry|holder)\b|\bfreez(?:e|es|ing) (?:a|the|my|your|their) card\b|\bcard (?:is |gets )?frozen\b|\b(?:lock|block|unblock|cancel)(?:ing|s)? (?:a|the|my|your) card\b", " paymentcard "),
    (r"\brss feeds?\b|\bfeed imports?\b|\bfeed of (?:audit|log|events|changes)\b|\baudit feed\b|\bevent feed\b|\bdata feeds?\b", " eventlog "),
    (r"\bposter[- ]sized?\b|\bprint(?:ed)? (?:a )?posters?\b|\bposter print\b", " largeformat "),
    (r"\bwithout (?:touching |using |reaching for |needing )?(?:the |a )?mouse\b|\bmouse[- ]free\b|\bmouseless\b|\bkeyboard[- ]only\b|\bnever (?:touch|use) the mouse\b", " keyboardonly "),
    (r"\b(?:confirmation|done|success|thank[- ]you) (?:screen|page) (?:prints|shows|says|never|does not|doesn't|after)\b|\b(?:done|success|thank[- ]you) (?:screen|page)\b", " completion screen "),
    (r"\bbalance sheets?\b|\bspreadsheets?\b|\bcheat sheets?\b|\bsheet music\b|\btime ?sheets?\b|\bworksheets?\b", " ledger "),
    (r"\brail(?:way)? (?:workers|staff|network|operator|company|timetable|line|lines)\b|\brailways?\b|\bhandrails?\b|\bguard ?rails?\b", " railwayservice "),
    (r"\b(?:user|style|quick|onboarding|field|setup|how-to|step-by-step|beginner|getting-started) guides?\b|\bguide (?:to|for) (?:the new|our new|new)\b", " handbook for "),
    (r"\bchannel (?:partners?|managers?|sales)\b|\bsales channels?\b|\bsupport channels?\b|\bslack channels?\b|\bnotification channels?\b", " partnergroup "),
    (r"\bwindows? (?:in|of|on) the (?:dashboard|layout|app|page|screen|editor)\b", " panes in the layout "),
    (r"\bstore hours\b|\bstore locator\b|\bbranch finder\b|\bapp store\b|\bplay store\b|\bin store\b", " branch info "),
    (r"\bcompare (?:two |the two |these two |both )?(?:files?|configs?|configurations?|versions?|documents?|notes|ideas|branches|commits|settings|profiles|records)\b(?: files?)?(?: side by side)?|\bcompare notes\b|\bdiff view\b", " review together "),
    (r"\b(?:\d+ ?px|spacing|layout|css|baseline) grid\b|\bgrid system\b", " spacing scale "),
    (r"\bhero (?:member|user|customer|of the)\b", " lead "),
    (r"\bremote(?:ly)?[- ](?:office|offices|team|teams|work|working|workers|worker|employees|staff|branch|branches|config\w*|access|desktop|server|servers|session|sessions|support|debugging|login|logins|colleagues|first)\b|\bremote into\b", " telework "),
    (r"\bmedia browser\b|\bfile browser\b|\bphoto browser\b|\basset browser\b", " media explorer "),
    (r"\btree of boxes\b", " org tree "),
]


RECORD_WORD_GATES = {
    "comp-mini-player": r"mini|picture[- ]in[- ]picture|\bpip\b|keep(?:s)? playing|while browsing|background play|small player",
    "interaction-drag-drop": r"drag|drop|reorder|re-order|move (?:it|them|cards|items|rows) (?:to|into|between)",
    "comp-plan-comparison": r"\bplans?\b|pricing|\btiers?\b|upgrade|downgrade|subscription",
    "a11y-skip-link": r"skip (?:link|to)|bypass|landmark|repeated navigation|long header|jump to (?:the )?(?:main|content)",
    "comp-kiosk-keypad": r"keypad|\bpin\b|digits?|code|phone number|type (?:in|your)|enter (?:your|the|a)|numeric entry",
    "chart-geo": r"\bmaps?\b|geo|location|region|territor|route",
    "layout-master-detail": r"master|list and detail|side by side|split|pane|select (?:one|an item|a row) to|detail (?:pane|panel|view) (?:beside|next)",
    "comp-pagination": r"pag(?:e|es|ing|inat)|load more|infinite|too many|hundreds|thousands|\b\d{3,}\b|long list|unusable once|rows",
    "comp-data-entry-grid": r"\bent(?:er|ry|ering)\b|typ(?:e|ing) (?:into|in)|edit|editable|input|keying|operators|clerks?|adjust",
    "comp-toast-notification": r"toast|snackbar|notification|banner|alert|message|announce|confirmation|undo",
}


def neutralize_token_traps(text: str) -> str:
    """Literal words that look like a component or screen but mean something else in context (Phase 6):
    the Tab key is not a tabs component, a landscape orientation is not a landscape poster card, a cookie
    overlay is not a player overlay, a balance sheet is not a side sheet. Output is lower-cased."""
    text = text.lower()
    for pat, repl in _TOKEN_TRAPS:
        text = re.sub(pat, repl, text)
    return text


def _strip_reference_clauses(text: str) -> str:
    """Remove clauses that describe what must stay or what to match; they are not build targets. A yardstick clause
    ('against our accessibility checklist') keeps its subject word."""
    text = re.sub(r"\bagainst (?:our|the|a|an|your) ([a-z -]*?)\s*(?:checklist|guideline|guidelines|standard|standards|policy|spec)\b", r" for \1 ", text, flags=re.I)
    text = re.sub(r"\bwithout (?:touching |using |reaching for |needing )?(?:the |a )?mouse\b", " keyboardonly ", text, flags=re.I)
    return _REFERENCE_CLAUSE_RE.sub(" ", text)


def build_requirements(query: str, project: dict | None = None, hints: dict | None = None) -> dict:
    """Evidence priority: explicit request > direct repository evidence > platform inference > default."""
    project = project or _hints_to_project(hints)
    lex = load_lexicon()
    text = " " + query.lower().replace("_", " ") + " "
    ev: dict = {"platform": {}, "input": {}, "product": {}, "stack": {}, "density": {}, "screen": {}, "mode": {},
                "environment": {}, "job": {}}
    conflicts: list[dict] = []

    # --- modes: lexicon verbs + task-intent model (Phase 4: structural cues in combination, evidence exposed)
    text_main = neutralize_token_traps(_strip_reference_clauses(text))   # clauses that describe what to keep or match are not targets; literal traps disarmed
    modes = _pick(re.sub(r"brand[- ]new|\bby brand\b|\bbrand (?:filter|name|names|field|column)\b", "new", text_main), "modes")
    problems = _pick(text, "problems")
    intent = sem.task_intent(query, modes, problems)
    ordered_modes, mode_evidence, mode_conflicts = sem.derive_modes(intent, modes, problems)
    conflicts.extend(mode_conflicts)
    for m in ordered_modes:
        ev["mode"][m] = {"status": "KNOWN" if m in modes else "INFERRED", "reason": "; ".join(e.split(": ", 1)[1] for e in mode_evidence if e.startswith(m + ":"))[:160] or "derived"}
    budget = sem.change_budget(ordered_modes, intent, bool(project) and not (project or {}).get("_from_hints") and bool((project or {}).get("stack_groups")))

    # --- platforms: typed, graded evidence (Phase 5): DIRECT -> KNOWN, STRONG -> INFERRED, WEAK alone -> UNKNOWN + MISSING
    platform_evidence = sem.resolve_platform(query, (project or {}).get("platforms"))
    proj_plats_known = list((project or {}).get("platforms", [])) if not (project or {}).get("_from_hints") else []
    phones_on_web = False
    for p, info in platform_evidence["resolved"].items():
        if info["status"] != "KNOWN" and p in proj_plats_known:
            ev["platform"][p] = {"status": "KNOWN", "reason": "request wording (" + info["reason"].split(": ", 1)[-1] + ") confirmed by project inspection"}
            continue
        ev["platform"][p] = {"status": info["status"], "reason": ("request: " if info["status"] == "KNOWN" else "wording suggests " + p + ": ") + info["reason"].split(": ", 1)[-1]}
    if "web" in proj_plats_known and "mobile" in ev["platform"] and "mobile" not in proj_plats_known:
        cand = next((c for c in platform_evidence["candidates"] if c["platform"] == "mobile"), None)
        if cand and all(str(e if not isinstance(e, dict) else e.get("phrase", e)).lower().strip() in _FORM_FACTOR_WORDS for e in cand["evidence"]):
            del ev["platform"]["mobile"]
            ev["platform"]["web"] = {"status": "KNOWN", "reason": "project inspection; the request names the phone viewport of the web app (" + ", ".join(str(e if not isinstance(e, dict) else e.get("phrase", e)) for e in cand["evidence"][:2]) + ")"}
            phones_on_web = True
    for p in list((project or {}).get("platforms", [])):
        if p in ev["platform"]:
            continue
        if ev["platform"] and any(v["reason"].startswith("request") for v in ev["platform"].values()):
            requested = {k for k, v in ev["platform"].items() if v["reason"].startswith("request")}
            if p == "web" and requested & {"kiosk", "tv"}:
                ev["stack"].setdefault("html-css", {"status": "INFERRED", "reason": "web technology is the substrate of the requested platform"}) if "html-css" in (project or {}).get("stack_groups", []) else None
                continue  # web technology is a normal substrate for kiosk / TV apps: not a conflict
            conflicts.append({"field": "platform", "request": sorted(requested), "project": p, "resolution": "request kept; repository platform recorded as context"})
            continue
        ev["platform"][p] = {"status": "KNOWN", "reason": "project inspection"}

    # --- stacks
    for s, h in _pick(text, "stacks").items():
        ev["stack"][s] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    for s in (project or {}).get("stack_groups", []):
        if s not in ev["stack"]:
            ev["stack"][s] = {"status": "KNOWN", "reason": "project inspection"}
    explicit_platform = any(v["reason"].startswith("request") for v in ev["platform"].values())
    if not ev["platform"]:
        for s in list(ev["stack"]):
            for p in lex.get("stack_platforms", {}).get(s, []):
                if p not in ev["platform"]:
                    ev["platform"][p] = {"status": "INFERRED", "reason": f"implied by stack {s}"}
    if "tv" in ev["platform"] and "compose" in ev["stack"] and "compose-tv" not in ev["stack"]:
        ev["stack"]["compose-tv"] = {"status": "INFERRED", "reason": "Compose on a TV platform uses androidx.tv (tv-material)"}

    # --- inputs
    constraints_hits = _pick(text, "constraints")
    input_only = None
    for label in ("remote-only", "keyboard-only", "touch-only"):
        if label in constraints_hits:
            input_only = label.split("-")[0]
    text_inputs = re.sub(r"(?:on-screen|soft|virtual|the) keyboard (?:open|is open|is up|up|inset|appears|shows|visible|covers|hides|pushes)|keyboard (?:open|is open|is up|up|inset|appears|shows up|pops up|covers|hides|pushes)|on-screen keyboard|soft keyboard|virtual keyboard|ime", " ", text)
    for i, h in _pick(sem.neutralize_platform_traps(neutralize_token_traps(text_inputs)), "inputs").items():
        ev["input"][i] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    if input_only:
        ev["input"][input_only] = {"status": "KNOWN", "reason": "request: " + ", ".join(constraints_hits[input_only + "-only"])}
    for i, hits in platform_evidence.get("inputs", {}).items():
        if i not in ev["input"] and not (input_only and i != input_only):
            ev["input"][i] = {"status": "KNOWN", "reason": "request: " + ", ".join(hits[:2])}
    proj_focus = " ".join(map(str, (project or {}).get("focus_handling", [])))
    constraints_focus_present = bool((project or {}).get("focus_handling"))
    if "DPAD" in proj_focus and "remote" not in ev["input"]:
        ev["input"]["remote"] = {"status": "KNOWN", "reason": "project inspection: DPAD/remote handling in source"}
    for p in ev["platform"]:
        for implied in lex.get("implied_inputs", {}).get(p, []):
            if input_only and implied != input_only:
                continue
            ev["input"].setdefault(implied, {"status": "INFERRED", "reason": f"implied by platform {p}"})
    if input_only:
        for i in list(ev["input"]):
            if i != input_only and ev["input"][i]["status"] == "INFERRED":
                del ev["input"][i]
        if input_only == "touch" and "tv" in ev["platform"]:
            conflicts.append({"field": "input", "request": "touch", "project": "tv platform normally remote-first",
                              "resolution": "request kept; verify the display is touch-enabled"})

    # --- products
    for p, h in _pick(text_main, "products").items():   # trap-neutralised: a poster-sized print is not a media product
        ev["product"][p] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    for e in (project or {}).get("environment_hints", []):
        ev["environment"].setdefault(e, {"status": "KNOWN", "reason": "project inspection (README)"})
    for p in (project or {}).get("product_hints", []):
        if p not in ev["product"]:
            ev["product"][p] = {"status": "KNOWN", "reason": "project inspection (README)"}

    # --- screens, subtypes, components, environment, jobs
    for s, h in _pick(text_main, "screens").items():
        ev["screen"][s] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    subtypes = sorted(_pick(text_main, "screen_subtypes"))
    if "sign-in" in subtypes and "auth" not in ev["screen"]:
        ev["screen"]["auth"] = {"status": "INFERRED", "reason": "sign-in subtype"}
    if "epg" in subtypes and "list" not in ev["screen"]:
        ev["screen"]["list"] = {"status": "INFERRED", "reason": "EPG is a scheduled list/grid screen"}
    components = sorted(_pick(text_main, "components"))
    if re.search(r"\bchart|\bgraph|\bthe bars\b|\bbars are\b|\bbar chart\b|\bstats screen\b|\bsparkline", text_main) and "chart" not in components:
        components = sorted(set(components) | {"chart"})
    for e, h in _pick(text, "environment").items():
        ev["environment"][e] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    if "kiosk" in ev["platform"]:
        ev["environment"].setdefault("public", {"status": "INFERRED", "reason": "kiosk platform implies public use"})
    if "tv" in ev["platform"]:
        ev["environment"].setdefault("shared-device", {"status": "INFERRED", "reason": "a TV is normally a shared household device"})
        ev["environment"].setdefault("large-display", {"status": "INFERRED", "reason": "TV platform"})
    for j, h in _pick(text_main, "jobs").items():
        ev["job"][j] = {"status": "KNOWN", "reason": "request: " + ", ".join(h)}
    if "high-risk-action" in ev["job"]:
        risk = "high"
    elif set(ev["product"]) & {"finance", "healthcare", "government"} or set(ev["screen"]) & {"auth", "checkout"} or "authentication" in ev["job"]:
        risk = "medium"
    else:
        risk = "low"

    # --- density
    dens = _pick(text, "density")
    density = None
    if dens:
        density = sorted(dens, key=lambda d: -len(dens[d]))[0]
        ev["density"][density] = {"status": "KNOWN", "reason": "request: " + ", ".join(dens[density])}
    else:
        for p in ev["product"]:
            implied = lex.get("implied_density", {}).get(p)
            if implied:
                capped = implied == "high" and bool(set(ev["platform"]) & {"mobile", "tv", "kiosk", "tablet"})
                density = "medium" if capped else implied
                ev["density"][density] = {"status": "INFERRED", "reason": f"implied by product {p}" + (" (capped for touch/remote platform)" if capped else "")}
                break

    # --- negative and preservation constraints
    negatives = _pick(text, "negatives")
    negative_labels = sorted(set(negatives) | {k for k in constraints_hits if k in NEGATIVE_LABELS})
    negative_phrases = sorted({t for hits in negatives.values() for t in hits} | {t for k, hits in constraints_hits.items() if k in NEGATIVE_LABELS for t in hits})
    has_project = bool(project) and not (project or {}).get("_from_hints") and bool((project or {}).get("stack_groups"))
    constraints = {
        "preserve_existing_system": True if (has_project and ordered_modes[0] not in ("brand",)) else (True if ("preserve-system" in constraints_hits or "system" in intent["preserve"]) else None),
        "focus_handling_present": constraints_focus_present,
        "preserve_navigation": True if ("navigation-change" in negative_labels or "navigation" in intent["preserve"]) else None,
        "preserve_color": True if ("color" in intent["preserve"] or "system" in intent["preserve"]) else None,
        "preserve_typography": True if ("typography-change" in negative_labels or "typography" in intent["preserve"] or "system" in intent["preserve"]) else None,
        "preserve_behaviour": True if "behaviour" in intent["preserve"] else None,
        "no_new_dependencies": True if "dependencies" in negative_labels else None,
        "performance_sensitive": True if ("performance" in constraints_hits or set(ev["platform"]) & {"tv", "kiosk"} or "low-bandwidth" in ev["environment"]) else None,
        "brand_system_present": True if (project or {}).get("design_docs") else (False if has_project else None),
        "input_only": input_only,
    }

    plats = set(ev["platform"])
    inputs = set(ev["input"])
    a11y_mode = ordered_modes[0] in ("accessibility", "audit", "review")
    accessibility = {
        "keyboard": True if ("keyboard" in inputs or plats & {"web", "desktop"} or a11y_mode) else None,
        "screen_reader": True if (a11y_mode or plats) else None,
        "focus": True if (inputs & {"keyboard", "remote"} or plats & {"tv", "desktop", "web"}) else None,
        "touch_targets": True if (inputs & {"touch"} or plats & {"mobile", "kiosk", "tablet"}) else None,
        "reduced_motion": True if ("animation" in negative_labels or ordered_modes[0] in ("create", "polish", "brand", "design-system") or a11y_mode) else None,
        "contrast": True,
    }

    known, inferred = [], []
    for field, entries in ev.items():
        for value, v in entries.items():
            (known if v["status"] == "KNOWN" else inferred).append({"field": field, "value": value, "reason": v["reason"]})
    missing = []
    primary = ordered_modes[0]
    if primary in ("create", "design-system", "refactor", "responsive") and not ev["platform"]:
        missing.append({"field": "platform", "reason": "not stated and not detectable from a repository"})
    if primary in ("create", "design-system", "brand") and not ev["product"]:
        missing.append({"field": "product", "reason": "product family / primary user task not stated"})
    if primary in ("create", "brand", "design-system", "polish") and not constraints["brand_system_present"]:
        missing.append({"field": "brand", "reason": "no brand assets, guideline, or character description available"})
    if primary in ("create", "refactor", "reconstruct") and not ev["stack"]:
        missing.append({"field": "stack", "reason": "implementation stack not stated and no repository evidence"})
    if primary in ("accessibility", "audit", "review", "polish") and not ev["platform"]:
        missing.append({"field": "platform", "reason": "audit targets differ by platform; not stated"})
    wording_only = [p for p, v in ev["platform"].items() if v["reason"].startswith("wording suggests")]
    if wording_only and not any(m["field"] == "platform" for m in missing):
        missing.append({"field": "platform", "reason": "only inferred from wording (" + ", ".join(wording_only) + "); confirm before committing"})
    if not ev["platform"] and platform_evidence["weak_only"] and not any(m["field"] == "platform" for m in missing):
        missing.append({"field": "platform", "reason": "target platform/form factor needs confirmation (weak evidence for " + ", ".join(platform_evidence["weak_only"]) + ")"})
    elif not ev["platform"] and not any(m["field"] == "platform" for m in missing) and primary not in ("brand", "design-system"):
        missing.append({"field": "platform", "reason": "target platform/form factor not stated"})

    # project design context (repository evidence; the request can override it)
    dc = (project or {}).get("design_context") or {}
    project_context = {k: {"value": v.get("value", "unknown"), "status": v.get("status", "UNKNOWN"), "evidence": v.get("evidence", [])[:3], **({"default": v["default"]} if v.get("default") else {})}
                       for k, v in dc.items() if isinstance(v, dict)}
    for k in ("navigation", "theme", "surfaces", "radius", "spacing", "typography", "components"):
        project_context.setdefault(k, {"value": "unknown", "status": "UNKNOWN", "evidence": []})
    for k, v in project_context.items():
        if v["status"] in ("KNOWN", "INFERRED") and v["value"] not in ("unknown", None):
            (known if v["status"] == "KNOWN" else inferred).append({"field": "project_" + k, "value": str(v["value"]), "reason": "repository: " + "; ".join(map(str, v["evidence"][:2]))})

    ui_hits = _hits(text, _compiled_lexicon()["ui_vocab"])
    non_ui_hits = _hits(text, _compiled_lexicon()["non_ui_vocab"])
    explicit_plats = {p for p, v in ev["platform"].items() if v["reason"].startswith("request")}
    explicit_stacks = {k for k, v in ev["stack"].items() if v["reason"].startswith("request")}
    activation = _activation(ui_hits, non_ui_hits, modes or problems, explicit_plats, components, explicit_stacks)
    ui_signal = len(problems) + len(components) + len(ev["screen"]) + len(explicit_plats) + len([m for m in modes if m in ("accessibility", "brand", "design-system", "reconstruct", "responsive", "polish")])
    scope = sem.classify_scope(query, ui_signal, has_project=bool(project) and not (project or {}).get("_from_hints"))
    if activation["decision"] == "activate" and scope["kind"] == "abstain" and scope["domain"] in ("DATA", "BACKEND", "INFRASTRUCTURE", "BUILD_TOOLING", "FRONTEND_RUNTIME"):
        # Phase 5: activation must not disagree with a decisive technical-scope abstention
        activation = {**activation, "decision": "skip", "overridden_by_scope": scope["reason"]}

    if phones_on_web and "responsive" not in ordered_modes:
        ordered_modes.insert(min(1, len(ordered_modes)), "responsive")
        mode_evidence.append("responsive: phone viewport of a web app")
    primary_jobs = [f"{primary} {s}" for s in sorted(ev["screen"])] or [f"{primary} {c}" for c in components[:2]] or [primary]
    if ev["job"]:
        primary_jobs = sorted(ev["job"]) + primary_jobs
    req = {
        "schema": REQUIREMENTS_SCHEMA, "query": query, "query_clean": text_main.strip(), "mode": ordered_modes,
        "platform": sorted(ev["platform"]), "input": sorted(ev["input"]), "product": sorted(ev["product"]),
        "screen": sorted(ev["screen"]), "screen_subtype": subtypes, "stack": sorted(ev["stack"]), "density": density,
        "components": components, "environment": sorted(ev["environment"]), "jobs": sorted(ev["job"]), "risk": risk,
        "problems": sorted(problems), "intent": {k: v for k, v in intent.items() if k != "evidence"}, "intent_evidence": intent["evidence"],
        "mode_evidence": mode_evidence, "change_budget": budget, "scope": scope, "project_context": project_context,
        "platform_evidence": {"candidates": platform_evidence["candidates"], "weak_only": platform_evidence["weak_only"], "unknown": not ev["platform"]},
        "primary_jobs": primary_jobs, "secondary_jobs": [m for m in ordered_modes[1:]],
        "constraints": constraints, "accessibility": accessibility,
        "negative_constraints": negative_labels, "negative_phrases": negative_phrases,
        "known": known, "inferred": inferred, "missing": missing, "conflicts": conflicts,
        "source": {"request": sorted({h for grp in (modes, negatives, constraints_hits, problems) for hs in grp.values() for h in hs}
                                     | {v["reason"][9:] for e in ev.values() for v in e.values() if v["reason"].startswith("request: ")}),
                   "project": [f["note"] for f in (project or {}).get("findings", [])][:12]},
        "evidence": ev, "activation": activation,
    }
    return req


def validate_requirements(req: dict) -> list[str]:
    errs = []
    if req.get("schema") != REQUIREMENTS_SCHEMA:
        errs.append(f"schema must be {REQUIREMENTS_SCHEMA}")
    for field, allowed in (("mode", MODES), ("platform", PLATFORMS - {"any"}), ("input", INPUTS - {"any"}),
                           ("product", PRODUCTS - {"any"}), ("screen", SCREENS - {"any"}), ("stack", STACK_GROUPS - {"any"}),
                           ("environment", ENVIRONMENTS), ("screen_subtype", SCREEN_SUBTYPES)):
        vals = req.get(field)
        if not isinstance(vals, list):
            errs.append(f"{field} must be a list")
        else:
            bad = [v for v in vals if v not in allowed]
            if bad:
                errs.append(f"{field} has unknown values {bad}")
    if not req.get("mode"):
        errs.append("mode must have at least one entry")
    if req.get("density") not in (None, "low", "medium", "high"):
        errs.append("density must be low|medium|high|null")
    if req.get("risk") not in RISK:
        errs.append("risk must be low|medium|high")
    for field in ("known", "inferred", "missing", "conflicts", "negative_constraints", "jobs", "problems"):
        if not isinstance(req.get(field), list):
            errs.append(f"{field} must be a list")
    for entry in req.get("known", []) + req.get("inferred", []):
        if not {"field", "value", "reason"} <= set(entry):
            errs.append(f"ledger entry missing keys: {entry}")
    for entry in req.get("missing", []):
        if not {"field", "reason"} <= set(entry):
            errs.append(f"missing entry needs field and reason: {entry}")
    bad_neg = [n for n in req.get("negative_constraints", []) if n not in NEGATIVE_LABELS]
    if bad_neg:
        errs.append(f"unknown negative constraints {bad_neg}")
    for key in ("constraints", "accessibility", "source", "evidence", "activation", "scope", "intent", "project_context"):
        if not isinstance(req.get(key), dict):
            errs.append(f"{key} must be an object")
    if req.get("change_budget") not in CHANGE_BUDGETS:
        errs.append(f"change_budget must be one of {sorted(CHANGE_BUDGETS)}")
    if req.get("scope", {}).get("domain") not in sem.DOMAINS:
        errs.append("scope.domain must be a known domain")
    return errs


def compact_requirements(req: dict, explain: bool = False) -> dict:
    out = {k: req[k] for k in ("schema", "mode", "platform", "input", "product", "screen", "screen_subtype", "stack", "density",
                               "components", "environment", "jobs", "problems", "risk", "primary_jobs", "constraints", "accessibility", "negative_constraints", "change_budget")}
    out["scope"] = {k: req["scope"].get(k) for k in ("domain", "in_scope", "kind", "reason", "nearest_ui_task")}
    out["intent"] = {k: req["intent"].get(k) for k in ("artifact_state", "operations", "problem_domain", "change_scope", "utterance", "preserve")}
    out["platform_evidence"] = [{"platform": c["platform"], "strength": c["strength"], "evidence": [e["phrase"] for e in c["evidence"][:3]]} for c in req["platform_evidence"]["candidates"]]
    out["mode_evidence"] = req["mode_evidence"][:6]
    out["project_context"] = {k: f"{v['value']} ({v['status']})" for k, v in req["project_context"].items() if v["status"] != "UNKNOWN"}
    out["constraints"] = {k: v for k, v in req["constraints"].items() if v is not None}
    out["accessibility"] = {k: v for k, v in req["accessibility"].items() if v}
    out["known"] = [f"{e['field']}={e['value']}" for e in req["known"]]
    out["inferred"] = [f"{e['field']}={e['value']}" for e in req["inferred"]]
    out["missing"] = [f"{e['field']}: {e['reason']}" for e in req["missing"]]
    if req["conflicts"]:
        out["conflicts"] = req["conflicts"]
    out["status"] = requirements_status(req)
    if explain:
        out["known"] = [f"{e['field']}={e['value']} ({e['reason']})" for e in req["known"]]
        out["inferred"] = [f"{e['field']}={e['value']} ({e['reason']})" for e in req["inferred"]]
        out["source"] = req["source"]
        out["activation"] = req["activation"]
        out["intent"] = req["intent"]; out["intent_evidence"] = req["intent_evidence"]; out["mode_evidence"] = req["mode_evidence"]
        out["scope_evidence"] = req["scope"]["evidence"]
        out["project_context"] = req["project_context"]
    return out


def requirements_status(req: dict) -> str:
    """Scope decides abstention (the activation proxy is a separate, frozen routing estimate)."""
    if not req.get("scope", {}).get("in_scope", True):
        return "ABSTAIN"
    if req["conflicts"]:
        return "AMBIGUOUS"
    if req["activation"]["decision"] == "ambiguous" and (not req["platform"] or all(v["reason"].startswith("wording suggests") for v in req["evidence"]["platform"].values())) and len(req["query"].split()) <= 4:
        return "AMBIGUOUS"
    explicit_platforms = set(k for k, v in req["evidence"]["platform"].items() if v["reason"].startswith("request"))
    if len(explicit_platforms) > 1 and not ({"mobile", "tablet"} >= explicit_platforms) and not ({"web", "mobile", "tablet"} >= explicit_platforms):
        return "AMBIGUOUS"
    return "CONFIDENT"


def classify(query: str, hints: dict | None = None) -> dict:
    return _signals_view(build_requirements(query, hints=hints))


def _signals_view(req: dict) -> dict:
    ev = req["evidence"]
    return {
        "query": req["query"], "modes": req["mode"],
        "platforms": {p: {"status": v["status"], "evidence": [v["reason"]]} for p, v in ev["platform"].items()},
        "inputs": {i: {"status": v["status"], "evidence": [v["reason"]]} for i, v in ev["input"].items()},
        "products": {p: {"status": v["status"], "evidence": [v["reason"]]} for p, v in ev["product"].items()},
        "stacks": {s: {"status": v["status"], "evidence": [v["reason"]]} for s, v in ev["stack"].items()},
        "density": {"value": req["density"], "status": (next(iter(ev["density"].values()))["status"] if ev["density"] else None)},
        "components": {c: [] for c in req["components"]}, "screens": {s: [] for s in req["screen"]},
        "negatives": req["negative_phrases"], "negative_targets": req["negative_constraints"],
        "activation": req["activation"], "missing": [f"{m['field']}: {m['reason']}" for m in req["missing"]], "requirements": req,
    }


def _compact_signals(req: dict) -> dict:
    ev = req["evidence"]
    return {
        "modes": req["mode"], "platforms": {p: v["status"] for p, v in ev["platform"].items()},
        "inputs": {i: v["status"] for i, v in ev["input"].items()}, "products": {p: v["status"] for p, v in ev["product"].items()},
        "density": {"value": req["density"], "status": (next(iter(ev["density"].values()))["status"] if ev["density"] else None)},
        "stacks": {s: v["status"] for s, v in ev["stack"].items()}, "components": req["components"], "screens": req["screen"],
        "environment": req["environment"], "risk": req["risk"], "negatives": req["negative_constraints"],
    }


# ---------------------------------------------------------------------------
# Concern derivation (deterministic design policy; documented in docs/MAINTENANCE.md)
# ---------------------------------------------------------------------------

def derive_concerns(req: dict) -> dict:
    """REQUIRED / RECOMMENDED / OPTIONAL concerns with reasons (policy, not statistics), plus the expected
    concept ids from de_semantic.derive_expected_concepts (concept-policy/v1)."""
    primary = req["mode"][0] if req["mode"] else "create"
    plats, inputs, screens, prods = set(req["platform"]), set(req["input"]), set(req["screen"]), set(req["product"])
    comps, envs, subtypes, jobs = set(req["components"]), set(req["environment"]), set(req["screen_subtype"]), set(req.get("jobs", []))
    problems = set(req.get("problems", []))
    req_c: dict[str, str] = {}
    rec_c: dict[str, str] = {}
    opt_c: dict[str, str] = {}

    def need(level: dict, concern: str, reason: str):
        if level is req_c:
            rec_c.pop(concern, None); opt_c.pop(concern, None); req_c.setdefault(concern, reason)
        elif level is rec_c:
            if concern in req_c:
                return
            opt_c.pop(concern, None); rec_c.setdefault(concern, reason)
        else:
            if concern in req_c or concern in rec_c:
                return
            opt_c.setdefault(concern, reason)

    marketing_page = bool(screens & {"landing"} or "marketing" in prods or subtypes & {"hero"})
    form_like = bool(screens & {"form", "checkout", "auth", "onboarding"} or comps & {"form"} or subtypes & {"wizard", "sign-in"} or "enter-data" in jobs)
    data_like = bool(screens & {"dashboard", "list"} or comps & {"table", "chart"} or subtypes & {"data-grid", "epg"} or prods & {"finance", "erp"} or jobs & {"monitor", "compare", "drilldown"})
    text = " " + req["query"].lower() + " "
    async_data = bool(sem._count(text, sem.ASYNC_WORDS)) or bool(screens & {"list", "dashboard", "search", "detail", "player", "home", "checkout"}) \
        or bool(comps & {"table", "chart", "list", "search", "media", "empty-state"}) or bool(jobs & {"monitor", "browse", "search", "resume", "refresh"}) or bool(subtypes & {"feed", "epg", "rails", "chat", "map"})
    static_page = bool(sem._count(text, sem.STATIC_WORDS)) and not comps and not (screens - {"landing"})

    if primary in ("accessibility", "audit", "review"):
        need(req_c, "accessibility", f"{primary} mode"); need(req_c, "interaction", f"{primary} mode: operability is part of the review")
        need(req_c, "component", "the reviewed component/screen")
        need(rec_c, "states", "audits check empty/loading/error handling"); need(rec_c, "anti-pattern", "audits name generic-design defects")
        if "interaction" in problems:
            need(req_c, "feedback", "interaction problem: discoverability and confirmation of actions")
        elif primary == "audit":
            need(rec_c, "feedback", "audits check that actions are discoverable and confirmed")
        if "visual" in problems:
            need(req_c, "structure", "visual problem: hierarchy and spacing")
    elif primary == "brand":
        need(req_c, "brand", "brand mode"); need(req_c, "structure", "brands differ structurally, not cosmetically"); need(req_c, "anti-pattern", "cosmetic-only differentiation is the failure to avoid")
        need(rec_c, "navigation", "navigation model is a structural brand axis"); need(rec_c, "content", "typography carries identity")
    elif primary == "design-system":
        need(req_c, "brand", "tokens and type express identity"); need(req_c, "content", "type scale"); need(req_c, "accessibility", "contrast and states are validated per theme")
        need(rec_c, "structure", "spacing scale"); need(rec_c, "motion", "motion tokens")
    elif primary == "polish":
        need(req_c, "structure", "hierarchy and spacing are the usual polish defects"); need(req_c, "anti-pattern", "polish removes generic devices")
        need(rec_c, "content", "typography"); need(rec_c, "component", "the component being polished")
    elif primary == "responsive":
        need(req_c, "adaptive", "responsive mode"); need(req_c, "structure", "layout transformation"); need(rec_c, "navigation", "navigation transforms across widths")
    else:  # create / refactor / reconstruct
        if comps or subtypes or (screens - {"landing", "home"}):
            need(req_c, "component", "a specific component/screen is requested")
        need(req_c, "structure", "layout topology and hierarchy")
        if screens & {"home", "list", "dashboard", "search"} or comps & {"navigation"} or subtypes & {"rails"}:
            need(req_c, "navigation", "entry screen or navigation component")
        else:
            need(rec_c, "navigation", "how users arrive and leave")
        if async_data and not static_page and not (marketing_page and not (comps or form_like or data_like)):
            need(req_c, "states", "asynchronous or remote data on this screen")
        elif form_like:
            need(req_c, "states", "submission states")
        else:
            need(rec_c, "states", "few states; still handle failed media")
        need(rec_c, "anti-pattern", "create/refactor requests attract generic defaults")
        if primary == "create":
            need(rec_c, "brand", "visual identity direction")
    if plats or inputs:
        need(req_c, "interaction", ("input model: " + ",".join(sorted(inputs))) if inputs else "platform interaction conventions")
        need(req_c, "accessibility", "platform accessibility baseline")
    if "tv" in plats:
        need(req_c, "performance", "focus latency and catalog virtualization on TV"); need(rec_c, "content", "10-foot readability")
    if "kiosk" in plats:
        need(req_c, "environment", "public kiosk use"); need(req_c, "privacy", "shared public device")
    if plats & {"web", "tablet"}:
        need(rec_c, "adaptive", "viewport range")
    if "mobile" in plats:
        need(rec_c, "adaptive", "device sizes and orientation")
    if form_like:
        need(req_c, "feedback", "form validation and submission feedback")
    elif screens & {"settings"} or comps & {"notification", "dialog", "button"}:
        need(rec_c, "feedback", "actions need confirmation and status")
    if data_like:
        need(req_c, "data-display", "numbers, tables or charts are the content")
    if marketing_page:
        need(req_c, "content", "hierarchy and readable copy"); need(req_c, "brand", "identity"); need(rec_c, "performance", "LCP/CLS")
    for st in sorted(subtypes):
        for c in SUBTYPE_CONCERNS.get(st, []):
            need(rec_c, c, f"screen subtype {st}")
    if req["risk"] == "high":
        need(req_c, "feedback", "high-risk action: confirmation and recovery"); need(rec_c, "privacy", "sensitive data on screen")
    elif req["risk"] == "medium":
        need(rec_c, "feedback", "sensitive domain: errors must be recoverable")
    if prods & {"finance", "healthcare"} and (plats & {"tv", "kiosk", "tablet"} or envs & {"shared-device", "public"}):
        need(req_c, "privacy", "sensitive data on a shared screen")
    for e in sorted(envs):
        st = req["evidence"]["environment"].get(e, {}).get("status", "INFERRED")
        need(req_c if (st == "KNOWN" or e == "public") else rec_c, "environment", f"environment {e} ({st})")
        if e == "shared-device" and st == "KNOWN":
            need(req_c, "privacy", "shared device stated")
        if e == "low-bandwidth":
            need(req_c, "states", "offline/sync states")
    if req["negative_constraints"]:
        need(req_c, "anti-pattern", "explicit exclusions: " + ",".join(req["negative_constraints"]))
    if req["constraints"].get("performance_sensitive"):
        need(rec_c, "performance", "performance-sensitive context")
    if primary in ("create", "brand", "design-system", "polish"):
        need(opt_c, "motion", "motion character is optional for this task")
    need(opt_c, "content", "typography roles"); need(opt_c, "performance", "runtime cost of UI choices")

    concerns = {"required": [{"concern": c, "reason": r} for c, r in req_c.items()],
                "recommended": [{"concern": c, "reason": r} for c, r in rec_c.items()],
                "optional": [{"concern": c, "reason": r} for c, r in opt_c.items()]}
    expected = sem.derive_expected_concepts(req, concerns)
    concerns["required_concepts"] = [{"concept": e["id"], "reason": e["reason"], "priority": e.get("priority", 2), "critical": bool(e.get("critical"))} for e in expected["required"]]
    concerns["recommended_concepts"] = [{"concept": e["id"], "reason": e["reason"]} for e in expected["recommended"]]
    concerns["optional_concepts"] = [{"concept": e["id"], "reason": e["reason"]} for e in expected["optional"]]
    concerns["concept_policy"] = expected["version"]
    return concerns


SUBTYPE_CONCERNS = {"epg": ["data-display", "navigation", "performance"], "data-grid": ["data-display", "interaction"],
                    "wizard": ["feedback", "states"], "sign-in": ["privacy", "feedback"], "rails": ["navigation", "performance"],
                    "hero": ["content", "brand"], "feed": ["states", "performance"], "chat": ["states", "feedback"],
                    "map": ["data-display", "accessibility"], "calendar": ["data-display", "interaction"],
                    "permissions": ["feedback", "privacy"], "feature-tour": ["feedback", "content"], "checklist": ["feedback", "states"], "catalog": ["data-display", "navigation"]}


# ---------------------------------------------------------------------------
# Candidate generation (lexical + structural)
# ---------------------------------------------------------------------------

FIELD_WEIGHTS = {"title": 3.0, "keywords": 3.0, "category": 1.5, "use_when": 1.5, "guidance": 1.0}


class _FieldIndex:
    def __init__(self, docs: list[list[str]], k1=1.2, b=0.75):
        self.k1, self.b = k1, b
        self.N = len(docs)
        self.dl = [len(d) for d in docs]
        self.avgdl = (sum(self.dl) / self.N) if self.N else 1.0
        self.tf = []
        df = defaultdict(int)
        for d in docs:
            tf = defaultdict(int)
            for t in d:
                tf[t] += 1
            self.tf.append(tf)
            for t in tf:
                df[t] += 1
        self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}

    def score(self, i: int, qtokens: list[str]) -> float:
        s = 0.0
        tf = self.tf[i]
        for t in qtokens:
            if t not in tf:
                continue
            f = tf[t]
            s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.dl[i] / self.avgdl))
        return s

    def vocab(self):
        return self.idf.keys()


class Ranker:
    def __init__(self, records: list[dict]):
        self.records = records
        self.index = {}
        for field in FIELD_WEIGHTS:
            docs = []
            for r in records:
                val = r.get(field, "")
                if isinstance(val, list):
                    val = " ".join(val)
                docs.append(_tokens(val))
            self.index[field] = _FieldIndex(docs)
        self.vocab = set()
        for idx in self.index.values():
            self.vocab.update(idx.vocab())

    def lexical(self, qweights: dict[str, float]) -> tuple[list[float], list[float]]:
        total_w = sum(qweights.values()) or 1.0
        scores, coverage = [], []
        for i in range(len(self.records)):
            sc = 0.0
            matched = 0.0
            for t, w in qweights.items():
                per_field = sum(fw * self.index[f].score(i, [t]) for f, fw in FIELD_WEIGHTS.items())
                if per_field > 0:
                    matched += w
                sc += w * per_field
            scores.append(sc)
            coverage.append(matched / total_w)
        return scores, coverage

    def suggest(self, qtokens: list[str], limit=6) -> list[str]:
        out = []
        for t in qtokens:
            if t in self.vocab:
                continue
            for m in difflib.get_close_matches(t, list(self.vocab), n=2, cutoff=0.78):
                if m not in out:
                    out.append(m)
        return out[:limit]


_ranker_cache: dict = {}


def _ranker_for(pool: list[dict]) -> Ranker:
    key = tuple(r["id"] for r in pool)
    if key not in _ranker_cache:
        _ranker_cache[key] = Ranker(pool)
    return _ranker_cache[key]


def _record_mentions(rec: dict, label: str) -> bool:
    terms = NEGATIVE_RECORD_TERMS.get(label, [])
    hay = " ".join(rec.get("keywords", [])) + " " + rec["title"].lower()
    return any(re.search(r"\b" + re.escape(t) + r"\b", hay) for t in terms)


def _structured(rec: dict, req: dict) -> tuple[float, list[str], str | None]:
    reasons, boost, maxb = [], 0.0, 0.0
    ev = req["evidence"]
    plats = set(req["platform"]); inputs = set(req["input"])
    known_inputs = {i for i, v in ev["input"].items() if v["status"] == "KNOWN"}
    modes = req["mode"]; prods = set(req["product"]); density = req["density"]; screens = set(req["screen"])

    rp = set(rec["platform"])
    maxb += 3
    if plats:
        if "any" in rp:
            boost += 1.5
        elif rp & plats:
            boost += 3.0; reasons.append("platform " + ",".join(sorted(rp & plats)))
        else:
            return 0.0, reasons, f"platform {sorted(rp)} not in request {sorted(plats)}"
    else:
        boost += 1.0 if "any" in rp else 0.5

    ri = set(rec["input"])
    maxb += 2.5
    if inputs and "any" not in ri:
        if ri & known_inputs:
            boost += 2.5; reasons.append("input " + ",".join(sorted(ri & known_inputs)) + " (stated)")
        elif ri & inputs:
            boost += 1.5; reasons.append("input " + ",".join(sorted(ri & inputs)))
        elif plats or req["constraints"]["input_only"]:
            return 0.0, reasons, f"input {sorted(ri)} not available in request {sorted(inputs)}"
    elif "any" in ri:
        boost += 0.75

    maxb += 2
    if modes and modes[0] in rec["intent"]:
        boost += 2.0; reasons.append("mode " + modes[0])
    elif any(m in rec["intent"] for m in modes[1:]):
        boost += 1.0; reasons.append("secondary mode")

    maxb += 2.5
    rpf = set(rec["product_fit"])
    if prods and rpf & prods:
        boost += 2.5; reasons.append("product " + ",".join(sorted(rpf & prods)))
    elif "any" in rpf:
        boost += 2.5 if rec["kind"] in ("rule", "antipattern") else 0.75
    elif prods:
        boost -= 1.0; reasons.append("product mismatch")

    rsf = set(rec.get("screen_fit", ["any"]))
    maxb += 1.5
    if screens and "any" not in rsf:
        if rsf & screens:
            boost += 1.5; reasons.append("screen " + ",".join(sorted(rsf & screens)))
        else:
            boost -= 2.5; reasons.append("screen mismatch")
    elif screens:
        boost += 0.5

    maxb += 1
    if density and rec["density"] != "any":
        if rec["density"] == density:
            boost += 1.0; reasons.append("density " + density)
        elif {rec["density"], density} == {"low", "high"}:
            boost -= 1.0; reasons.append("density conflict")

    # environment-tagged records apply only when that environment is present
    renv = set(rec.get("environment", []))
    if renv:
        if renv & set(req["environment"]):
            boost += 1.0; reasons.append("environment " + ",".join(sorted(renv & set(req["environment"]))))
        else:
            return 0.0, reasons, f"environment {sorted(renv)} not in request"

    for label in req["negative_constraints"]:
        if label not in NEGATIVE_RECORD_TERMS or not _record_mentions(rec, label):
            continue
        is_alternative = rec["id"].endswith("-none") or rec["kind"] == "antipattern" or ("no " + label.rstrip("s")) in rec["title"].lower() \
            or (label == "animation" and rec["id"] in ("motion-functional-minimal",)) or (label == "hover" and rec["kind"] == "rule")
        if rec["kind"] in ("pattern", "component", "direction") and not is_alternative:
            return 0.0, reasons, f"user excluded '{label}'"
        if not is_alternative:
            boost -= 2.0; reasons.append(f"user excluded '{label}'")
    return max(0.0, boost) / maxb, reasons, None


def _lexical_tokens(query: str, req: dict) -> dict[str, float]:
    routing = set()
    for field in ("platform", "stack"):
        for v in req["evidence"][field].values():
            if v["reason"].startswith("request: "):
                for phrase in v["reason"][9:].split(", "):
                    routing.update(_tokens(phrase))
    all_tokens = _tokens(query)
    kept = [t for t in all_tokens if t not in routing]
    return {t: 1.0 for t in (kept or all_tokens)}


def candidates(query: str, req: dict, records: list[dict], kinds: set[str] | None = None, categories: set[str] | None = None,
               require_evidence: bool = True) -> tuple[list, list, Ranker, list[str]]:
    """Score every admissible record. Returns (scored, rejected, ranker, qtokens); scored items are
    (total, lex_n, boost, rec, reasons, facets, concerns)."""
    pool = [r for r in records if (not kinds or r["kind"] in kinds) and (not categories or r["category"] in categories)]
    ranker = _ranker_for(pool)
    qweights = _lexical_tokens(query, req)
    qtokens = list(qweights)
    lex, cov = ranker.lexical(qweights)
    top_lex = max(lex) if lex and max(lex) > 0 else 1.0
    scored, rejected = [], []
    for i, rec in enumerate(pool):
        boost, reasons, excl = _structured(rec, req)
        if excl:
            if lex[i] > 0:
                rejected.append({"id": rec["id"], "reason": excl})
            continue
        lex_n = (lex[i] / top_lex) * (cov[i] ** 0.5)
        total = 0.55 * lex_n + 0.45 * boost - (rec.get("rank", 50) - 50) / 500
        if require_evidence and lex_n == 0 and boost < 0.55:
            continue
        scored.append((total, lex_n, boost, rec, reasons, record_facets(rec), record_concerns(rec)))
    scored.sort(key=lambda t: (-round(t[0], 6), t[3].get("rank", 50), t[3]["id"]))
    return scored, rejected, ranker, qtokens


# ---------------------------------------------------------------------------
# Facet-aware search (Phase 2) — raw ranked lookup, kept for debugging/knowledge lookup
# ---------------------------------------------------------------------------

def required_facets(req: dict) -> list[str]:
    modes = req["mode"]
    primary = modes[0] if modes else "create"
    out: list[str] = []

    def add(*fs):
        for f in fs:
            if f not in out:
                out.append(f)
    if primary in ("accessibility", "audit", "review"):
        add("accessibility", "interaction", "component")
        if req["platform"]:
            add("platform")
        add("anti-pattern")
    elif primary == "brand":
        add("direction", "anti-pattern", "layout", "navigation", "visual")
    elif primary in ("polish",):
        add("anti-pattern", "layout", "visual", "component")
    elif primary == "responsive":
        add("layout", "component", "navigation")
        if req["platform"]:
            add("platform")
    elif primary == "design-system":
        add("visual", "layout", "direction", "accessibility")
    else:
        add("component" if req["components"] or req["screen"] else "layout", "layout")
        if req["platform"]:
            add("platform")
        if req["evidence"]["input"] and any(v["status"] == "KNOWN" for v in req["evidence"]["input"].values()):
            add("interaction")
        elif set(req["platform"]) & {"tv", "desktop", "kiosk"}:
            add("interaction")
        add("navigation")
        if primary == "create":
            add("direction")
    if "chart" in req["components"]:
        add("data-viz")
    if req["negative_constraints"] or primary in ("refactor",):
        add("anti-pattern")
    return out


def select_with_coverage(scored: list, req_facets: list[str], k: int, per_category: int,
                         relevance_floor: float = 0.5, window: int = 4, swap_ratio: float = 0.75) -> tuple[list, dict]:
    picked, per_cat, overflow = [], defaultdict(int), []
    for item in scored:
        cat = item[3]["category"]
        if per_cat[cat] >= per_category:
            overflow.append(item); continue
        per_cat[cat] += 1
        picked.append(item)
        if len(picked) >= k:
            break
    if len(picked) < k:
        for item in overflow:
            picked.append(item)
            if len(picked) >= k:
                break
    top = picked[0][0] if picked else 0.0
    swaps = []
    req_facets = req_facets[: max(1, k - 1)]
    if picked and req_facets:
        pool = scored[: window * k]
        for facet in req_facets:
            covered = set().union(*(it[5] for it in picked))
            if facet in covered:
                continue
            cand = next((it for it in pool if facet in it[5] and it not in picked and it[0] >= relevance_floor * top), None)
            if cand is None:
                continue
            for idx in range(len(picked) - 1, 0, -1):
                others = set().union(*(it[5] for j, it in enumerate(picked) if j != idx))
                if picked[idx][5] <= others and cand[0] >= swap_ratio * picked[idx][0]:
                    swaps.append({"out": picked[idx][3]["id"], "in": cand[3]["id"], "facet": facet})
                    picked[idx] = cand
                    break
        picked.sort(key=lambda t: (-round(t[0], 6), t[3].get("rank", 50), t[3]["id"]))
    covered = set().union(*(it[5] for it in picked)) if picked else set()
    cats = [it[3]["category"] for it in picked]
    metrics = {
        "required_facets": req_facets, "required_facets_satisfied": [f for f in req_facets if f in covered],
        "required_facets_unmet": [f for f in req_facets if f not in covered],
        "facet_coverage": round(len([f for f in req_facets if f in covered]) / len(req_facets), 2) if req_facets else 1.0,
        "category_diversity": round(len(set(cats)) / len(cats), 2) if cats else 0.0,
        "duplicate_pressure": round(max(cats.count(c) for c in set(cats)) / len(cats), 2) if cats else 0.0, "swaps": swaps,
    }
    return picked, metrics


def _item(rec: dict, req: dict, total: float, lex_n: float, boost: float, reasons: list[str], fac: set[str], explain: bool) -> dict:
    item = {"id": rec["id"], "kind": rec["kind"], "category": rec["category"], "title": rec["title"], "facets": sorted(fac),
            "concerns": sorted(record_concerns(rec)), "concepts": rec.get("concepts", []),
            "covers": [CONCEPT_LABELS.get(c, c) for c in rec.get("concepts", [])], "score": round(total, 3),
            "guidance": rec["guidance"], "use_when": rec["use_when"], "avoid_when": rec["avoid_when"], "risk": rec["risk"], "provenance": rec["provenance"]}
    impl = rec.get("implementation", {})
    if impl:
        wanted = set(req["stack"]) | {"any"}
        chosen = {k2: v for k2, v in impl.items() if k2 in wanted}
        if chosen:
            item["implementation"] = chosen
    if rec.get("incompatible"):
        item["incompatible"] = rec["incompatible"]
    if explain:
        item["why"] = {"lexical": round(lex_n, 3), "structural": round(boost, 3), "matched": reasons}
    return item


def search(query: str, records: list[dict] | None = None, k: int = 5, hints: dict | None = None,
           kinds: set[str] | None = None, categories: set[str] | None = None,
           per_category: int = 2, explain: bool = False, require_evidence: bool = True,
           requirements: dict | None = None, project: dict | None = None, facets: bool = True) -> dict:
    """Raw ranked lookup (debugging / knowledge lookup). Task-oriented retrieval is guidance()."""
    records = records or load_records()
    req = requirements or build_requirements(query, project=project, hints=hints)
    scored, rejected, ranker, qtokens = candidates(query, req, records, kinds, categories, require_evidence)
    req_facets = required_facets(req) if (facets and not categories) else []
    picked, metrics = select_with_coverage(scored, req_facets, k, per_category if not categories else 10 ** 6)
    coverage = (sum(t in ranker.vocab for t in qtokens) / len(qtokens)) if qtokens else 0.0
    top = picked[0][0] if picked else 0.0
    confidence = "none" if not picked else "high" if (top >= 0.6 and coverage >= 0.5) else "medium" if (top >= 0.4 or coverage >= 0.5) else "low"
    req_status = requirements_status(req)
    if not picked or not req.get("scope", {}).get("in_scope", True) or (coverage < 0.25 and not req["platform"] and not req["product"] and not req["components"]):
        status = "ABSTAIN"
    elif req_status == "AMBIGUOUS":
        status = "AMBIGUOUS"
    elif top < 0.45 or metrics["facet_coverage"] < 0.5:
        status = "PARTIAL"
    else:
        status = "CONFIDENT"
    results = [_item(rec, req, total, lex_n, boost, reasons, fac, explain) for total, lex_n, boost, rec, reasons, fac, _ in picked]
    out = {"query": query, "signals": _compact_signals(req), "status": status, "confidence": confidence,
           "token_coverage": round(coverage, 2), "coverage": metrics, "count": len(results), "results": results}
    if not results:
        out["suggestions"] = ranker.suggest(qtokens)
        out["note"] = "No verified match. Do not present this as knowledge; use general principles from references/ and say so."
    if explain:
        out["rejected"] = rejected[:8]
        out["requirements"] = compact_requirements(req, explain=True)
    if req["missing"]:
        out["missing"] = [f"{m['field']}: {m['reason']}" for m in req["missing"]]
    if req["conflicts"]:
        out["conflicts"] = req["conflicts"]
    return out


# ---------------------------------------------------------------------------
# Guidance bundle (Phase 3): concern-driven final selection
# ---------------------------------------------------------------------------

CORE_KINDS = ("pattern", "component", "direction", "chart")
BUILD_CONCERNS = {"component", "structure", "navigation", "brand", "data-display"}  # concerns best served by core kinds
BUNDLE_MIN, BUNDLE_SOFT, BUNDLE_MAX = 5, 6, 8  # min fill; recommended coverage fills to SOFT; required coverage may reach MAX


def record_tokens(rec: dict) -> int:
    return max(40, (len(rec["guidance"]) + len(rec["use_when"]) + len(rec["avoid_when"]) + sum(len(v) for v in rec.get("implementation", {}).values())) // 4)


def record_purity(rec: dict, wanted: set[str]) -> float:
    """relevant concepts for this task / all concepts the record expresses (1.0 when it declares <= 1)."""
    cs = rec.get("concepts", [])
    if len(cs) <= 1:
        return 1.0
    return len(set(cs) & wanted) / len(cs)


SCREEN_FAMILY = {"discover": {"list", "search", "home", "landing"}, "inspect": {"detail"}, "commit": {"checkout", "form", "auth", "onboarding"},
                 "operate": {"dashboard", "settings"}, "watch": {"player"}}
JOB_CATEGORY_AFFINITY = {  # record category -> jobs it serves; used only when the request states a job
    "detail": {"details", "browse", "resume"}, "media-card": {"browse", "resume", "watchlist", "details"}, "tv-rail": {"browse", "resume", "watchlist", "details"},
    "search": {"search", "browse"}, "list": {"browse", "monitor", "search"}, "table": {"monitor", "enter-data", "compare", "drilldown", "browse"},
    "chart": {"monitor", "compare", "drilldown"}, "form": {"enter-data", "authentication", "approve", "high-risk-action"}, "forms": {"enter-data", "authentication"},
    "wizard": {"enter-data", "permissions"}, "sign-in": {"authentication"}, "player": {"live-tv", "resume", "watchlist"}, "epg": {"live-tv", "browse"},
    "settings": {"permissions", "compare"}, "dialog": {"approve", "high-risk-action", "enter-data"}, "hero": set(), "command-palette": {"search"},
    "cta": {"approve", "high-risk-action"},
}
_NUMERIC_WORDS = ["revenue", "sales", "metric", "metrics", "numbers", "values", "totals", "trend", "trends", "kpi", "kpis", "spend", "traffic", "conversion", "counts", "over time", "by region", "by month", "monthly", "weekly", "quarterly", "percent", "%", "chart", "graph"]


def screen_family(screen: str) -> str | None:
    return next((f for f, members in SCREEN_FAMILY.items() if screen in members), None)


def contamination(rec: dict, req: dict, wanted: set[str]) -> tuple[float, list[str]]:
    """Semantic contamination penalty: the record would satisfy a demand while its other guidance conflicts
    with the task's product / screen / platform-job context. No record-specific exceptions."""
    pen, why = 0.0, []
    prods = set(req["product"]); screens = set(req["screen"])
    text = " " + req["query"].lower() + " "
    pf = set(rec["product_fit"]); sf = set(rec.get("screen_fit", ["any"]))
    critical = set(req.get("_critical_ids", set()))
    explicit_carrier = bool(critical & set(rec.get("concepts", []))) and (rec["kind"] in ("rule", "antipattern") or len(rec.get("concepts", [])) <= 3)   # a composite for another product is not waived
    if "any" not in pf and prods and not (pf & prods):
        pen += 0.3 if explicit_carrier else 0.6; why.append(f"product-specific ({','.join(sorted(pf))}) vs {sorted(prods)}" + (" (waived in part: carries a named concept)" if explicit_carrier else ""))
    if "any" not in pf and not prods and rec["kind"] in CORE_KINDS and not explicit_carrier:
        pen += 0.25; why.append("product-specific with product unknown")
    rp = set(rec.get("platform", ["any"])); plats_ = set(req["platform"])
    cand_plats = {c_.get("platform") for c_ in (req.get("platform_evidence") or {}).get("candidates", [])}
    if not plats_ and "any" not in rp and not (rp & ({"web"} | cand_plats)) and rec["kind"] in ("rule", "component", "pattern", "antipattern"):
        pen += 0.25 if (explicit_carrier and rec["kind"] in ("rule", "antipattern")) else 0.5; why.append(f"platform-specific ({','.join(sorted(rp))}) guidance with no platform evidence in the request")
    if "any" not in sf and screens and not (sf & screens):
        rec_fams = {screen_family(x) for x in sf} - {None}; req_fams = {screen_family(x) for x in screens} - {None}
        if rec_fams and req_fams and not (rec_fams & req_fams):
            pen += 0.7; why.append(f"screen family mismatch ({','.join(sorted(sf))} vs {sorted(screens)})")   # hard: PLP is not a PDP, checkout is not discovery
        else:
            pen += 0.5; why.append(f"screen-specific ({','.join(sorted(sf))}) vs {sorted(screens)}")
    if req["constraints"].get("preserve_navigation") and (rec["category"] in ("navigation", "drawer", "tabs") or rec["id"].startswith("nav-")) and rec["kind"] in CORE_KINDS:
        pen += 0.6; why.append("navigation must be preserved")
    if req["constraints"].get("preserve_typography") and rec["category"] == "typography" and rec["kind"] in CORE_KINDS:
        pen += 0.6; why.append("typography must be preserved")
    req_jobs = set(req.get("jobs", []))
    aff = JOB_CATEGORY_AFFINITY.get(rec["category"])
    if req_jobs and aff and rec["kind"] in ("component", "chart") and not (aff & req_jobs):
        pen += 0.4; why.append(f"job mismatch: {rec['category']} records serve {sorted(aff)}, the task is {sorted(req_jobs)}")
    purity = record_purity(rec, wanted | critical)
    if rec["kind"] in ("component", "chart", "direction") and purity < 0.34 and not explicit_carrier:
        pen += 0.4; why.append(f"low purity {purity:.2f}: most of its concepts are off-task")
    kpi_wanted = bool(wanted & {"data.kpi_comparison", "data.chart_by_question", "data.accessible_chart_alternative", "data.realtime_window"})
    if rec["kind"] == "chart" and not (set(req["components"]) & {"chart"} or screens & {"dashboard"} or ("compare" in req.get("jobs", []) and sem._count(text, _NUMERIC_WORDS)) or "monitor" in req.get("jobs", []) or kpi_wanted):
        pen += 0.5; why.append("chart record outside a data-visualisation task")
    comps = set(req["components"]); subs = set(req["screen_subtype"]); jobs = set(req.get("jobs", []))
    cat_needs = {
        "table": comps & {"table"} or subs & {"data-grid"} or "enter-data" in jobs or bool(re.search(r"\bgrid\b|\btable\b|\brows\b|spreadsheet|column", re.sub(r"css grid|grid layout|grid of cards|card grid|grid system", " ", text))),
        "epg": subs & {"epg"} or "live-tv" in jobs, "player": screens & {"player"} or "media" in comps or "live-tv" in jobs or bool(re.search(r"player|playback", text)),
        "wizard": subs & {"wizard", "checklist"} or screens & {"onboarding"} or bool(re.search(r"wizard|stepper|multi-step|steps|checklist|getting started|setup|\b(?:two|three|four|five|six|\d+) (?:screens|pages|stages)\b", text)),
        "sign-in": screens & {"auth"} or subs & {"sign-in"} or "authentication" in jobs, "tv-rail": subs & {"rails"} or screens & {"home"} or bool(re.search(r"\brail", text)),
        "search": comps & {"search"} or screens & {"search"} or "search" in jobs or bool(re.search(r"search|filter", text)), "tree": bool(re.search(r"\btree\b|hierarch", text)),
        "menu": bool(re.search(r"\bmenu\b|dropdown|context menu", text)), "tabs": bool(re.search(r"\btabs?\b|tabbed", text)), "drawer": bool(re.search(r"drawer|side panel|side sheet|sheet", text)),
        "command-palette": bool(re.search(r"command palette|cmd\+k|ctrl\+k|palette", text)), "chart": comps & {"chart"} or screens & {"dashboard"} or "monitor" in jobs or ("compare" in jobs and bool(sem._count(text, _NUMERIC_WORDS))) or kpi_wanted,
        "media-card": "media" in req["product"] or subs & {"rails"}, "hero": screens & {"landing"} or subs & {"hero"} or "marketing" in req["product"],
        "empty-state": True, "notification": True, "list": True, "form": True, "settings": True, "detail": True, "navigation": True, "dialog": True,
    }
    need = cat_needs.get(rec["category"])
    if need is not None and not need and rec["kind"] in ("component", "rule"):
        pen += 0.5; why.append(f"{rec['category']}-specific record with no {rec['category']} evidence in the request")
    gate = RECORD_WORD_GATES.get(rec["id"])
    if gate and not re.search(gate, text) and not (critical & set(rec.get("concepts", [])) and rec.get("concepts") and rec["concepts"][0] in critical):
        pen += 0.5; why.append("record-specific subject absent from the request")
    if rec["kind"] == "pattern" and rec["category"] == "cta" and not re.search(r"button|action|cta|submit|save|pay|checkout|toolbar|command|primary|sticky|bar\b|remove|delete|edit|invite|approve|export|send|add ", text) and not (screens & {"checkout", "form", "auth"} or "high-risk-action" in jobs):
        pen += 0.5; why.append("call-to-action pattern with no action wording or commitment screen in the request")
    return pen, why


COMPONENT_CATEGORIES = {"table": {"table"}, "chart": {"chart"}, "form": {"form", "forms"}, "search": {"search"}, "filters": {"search"}, "dialog": {"dialog"}, "tabs": {"tabs"},
                        "tree": {"tree"}, "menu": {"menu"}, "list": {"list", "table"}, "notification": {"notification"}, "media": {"player", "media-card"}, "empty-state": {"empty-state"},
                        "button": {"cta"}, "card": {"cards"}, "navigation": {"navigation"}, "wizard": {"wizard"}, "player": {"player"}, "toast": {"notification"}, "drawer": {"drawer"}}
SUBTYPE_CATEGORIES = {"epg": {"epg"}, "data-grid": {"table"}, "wizard": {"wizard"}, "sign-in": {"sign-in"}, "rails": {"tv-rail", "media-card"}, "hero": {"hero"}, "feed": {"list"},
                      "chat": {"list"}, "checklist": {"wizard"}, "catalog": {"search", "cards", "layout"}, "permissions": {"wizard"}, "feature-tour": {"wizard"}}
PLATFORM_BASELINE_CATEGORIES = {"input", "layout", "navigation", "focus", "performance", "environment", "privacy", "typography", "color", "player", "responsive"}
PROBLEM_CATEGORIES = {"accessibility": {"accessibility", "focus", "typography", "color", "motion"}, "interaction": {"input", "focus", "navigation", "dialog", "forms", "table"}, "visual": {"typography", "color", "layout", "surface", "cards", "icon"}}


def task_evidence(it, req: dict, critical_ids: set[str] | None = None) -> dict:
    """Deterministic positive evidence that a record fits THIS task beyond covering a concern (Phase 6)."""
    rec = it[3]; lex = it[1]
    cat = rec["category"]
    screens = set(req["screen"]); comps = set(req["components"]); subs = set(req["screen_subtype"]); jobs = set(req.get("jobs", []))
    prods = {p for p, v in req["evidence"]["product"].items() if str(v.get("reason", "")).startswith("request")}
    plats = set(req["platform"]); problems = set(req.get("problems", []))
    sf = set(rec.get("screen_fit", ["any"])); rp = set(rec["platform"]); pf = set(rec["product_fit"])
    ev = {
        "lexical_strong": lex >= 0.25, "lexical": lex >= 0.1,
        "screen": bool(screens and "any" not in sf and sf & screens),
        "subtype": bool(subs and any(cat in SUBTYPE_CATEGORIES.get(s_, set()) for s_ in subs)),
        "component": bool(comps and any(cat in COMPONENT_CATEGORIES.get(c_, set()) for c_ in comps)),
        "job": bool(jobs and JOB_CATEGORY_AFFINITY.get(cat) and JOB_CATEGORY_AFFINITY[cat] & jobs),
        "product": bool(prods and "any" not in pf and pf & prods),
        "platform_specific": bool(plats and "any" not in rp and rp <= plats | {"tablet"} and cat in PLATFORM_BASELINE_CATEGORIES),
        "problem": bool(problems and any(cat in PROBLEM_CATEGORIES.get(p_, set()) for p_ in problems)),
        "explicit_demand": bool(critical_ids and set(rec.get("concepts", [])) & critical_ids),
        "repository": bool(req.get("constraints", {}).get("preserve_existing_system")) and rec["kind"] == "rule" and cat == "implementation",
    }
    ev["specificity"] = sum(1 for k in ("lexical_strong", "screen", "subtype", "component", "job", "product", "platform_specific", "problem", "explicit_demand") if ev[k])
    return ev


def coverage_quality(it, req: dict, concept: str, ev: dict | None = None, critical_ids: set[str] | None = None) -> str:
    """How well a record's coverage of `concept` fits the task: DIRECT > SPECIFIC > GENERIC > INCIDENTAL (Phase 6)."""
    rec = it[3]; ev = ev or task_evidence(it, req, critical_ids)
    n = len(rec.get("concepts", []))
    focused = n <= 3
    task_fit = ev["screen"] or ev["subtype"] or ev["component"] or ev["job"]
    screen_specific = "any" not in set(rec.get("screen_fit", ["any"]))
    if screen_specific and not ev["screen"] and req.get("screen") is not None and not (ev["component"] or ev["job"]):
        return "GENERIC" if (focused or ev["lexical"]) else "INCIDENTAL"
    if focused and ((critical_ids and concept in critical_ids and (task_fit or ev["lexical_strong"])) or (task_fit and ev["lexical_strong"])):
        return "DIRECT"
    if task_fit or ev["platform_specific"] or ev["lexical_strong"] or ev["problem"] or (ev["product"] and focused and rec["kind"] in ("rule", "antipattern", "direction")):
        return "SPECIFIC"
    if focused or ev["lexical"] or (ev["explicit_demand"] and critical_ids and concept in critical_ids):
        return "GENERIC"
    return "INCIDENTAL"


QUALITY_RANK = {"DIRECT": 3, "SPECIFIC": 2, "GENERIC": 1, "INCIDENTAL": 0}


def bundle_budget(req: dict, concerns: dict) -> int:
    """Core size (what to build): 3 for build tasks, 2 for audit/review/accessibility."""
    primary = req["mode"][0] if req["mode"] else "create"
    return 2 if primary in ("audit", "accessibility", "review") else 3


def select_bundle(scored: list, req: dict, concerns: dict, core_size: int, total_cap: int | None = None) -> dict:
    """Precision-first compact set cover (guidance-bundle/v3, Phase 6). Deterministic; no learned weights.
    1. CORE: core-kind records with POSITIVE TASK EVIDENCE (screen / subtype / component / job / explicit product /
       strong wording / repository); direction records additionally need product-or-job evidence or strong wording.
    2. Most relevant rules for the wording (lexical >= 0.4 and some task evidence) are guardrails.
    3. CRITICAL required concepts first, then other required concepts, then recommended: a record enters only
       with a coverage quality of DIRECT or SPECIFIC, or GENERIC when it carries a critical concept, matches the
       wording, is a platform-baseline rule for the task's platform, or the task is high-risk. Recommended
       concepts are surfaced only by DIRECT / SPECIFIC carriers; otherwise they stay 'not surfaced'.
    4. No soft minimum: the bundle stops when critical and required demands are covered (or uncoverable) and
       no candidate with real task evidence remains. Hard cap 8. Every pick records its marginal value."""
    top = scored[0][0] if scored else 0.0
    by_id = {it[3]["id"]: it for it in scored}
    selected: list = []
    selected_ids: set[str] = set()
    covered_c: set[str] = set()
    covered_ids: set[str] = set()
    omitted = []
    marginal: dict[str, dict] = {}
    required = [e["concern"] for e in concerns["required"]]
    recommended = [e["concern"] for e in concerns["recommended"]]
    req_ids = [c["concept"] for c in concerns["required_concepts"]]
    critical_ids = {c["concept"] for c in concerns["required_concepts"] if c.get("critical")}
    priority_of = {c["concept"]: c.get("priority", 2) for c in concerns["required_concepts"]}
    rec_ids = [c["concept"] for c in concerns["recommended_concepts"]]
    wanted = set(req_ids) | set(rec_ids) | {c["concept"] for c in concerns.get("optional_concepts", [])}
    high_risk = req.get("risk") == "high" or "high-risk-action" in req.get("jobs", []) or "approve" in req.get("jobs", [])
    req["_critical_ids"] = critical_ids
    evidence = {it[3]["id"]: task_evidence(it, req, critical_ids) for it in scored}

    def compatible(rec):
        return not any(o in rec.get("incompatible", []) or rec["id"] in by_id[o][3].get("incompatible", []) for o in selected_ids)

    def role_of(rec):
        return "guardrail" if rec["kind"] in ("rule", "antipattern") else "core"

    def add(it, role, reason, gained_ids=(), gained_c=(), quality=None):
        rec = it[3]
        selected.append((it, role, reason))
        selected_ids.add(rec["id"])
        new_ids = set(rec.get("concepts", [])) - covered_ids
        marginal[rec["id"]] = {"new_critical": sorted(new_ids & critical_ids), "new_required": sorted((new_ids & set(req_ids)) - critical_ids),
                               "new_recommended": sorted(new_ids & set(rec_ids)), "new_concerns": sorted(it[6] - covered_c),
                               "specificity": evidence[rec["id"]]["specificity"], "evidence": [k for k, v in evidence[rec["id"]].items() if v is True],
                               "quality": quality, "contamination": round(contamination(rec, req, wanted)[0], 2), "tokens": record_tokens(rec)}
        covered_c.update(it[6]); covered_ids.update(rec.get("concepts", []))

    primary = req["mode"][0] if req["mode"] else "create"
    intent_ = req.get("intent") or {}
    build_task = primary in ("create", "brand", "design-system", "reconstruct") or intent_.get("artifact_state") == "new"
    narrow_existing = (intent_.get("artifact_state") == "existing" and intent_.get("change_scope") != "system" and not build_task and set(intent_.get("operations", [])) <= {"modify", "diagnose", "polish", "inspect"}
                       and not re.search(r"end[- ]to[- ]end|whole flow|entire flow|the flow", req["query"].lower()))

    def core_evidence_ok(rec, ev):
        structural = ev["screen"] or ev["subtype"] or ev["component"] or ev["job"]
        if rec["kind"] == "direction":
            return (ev["product"] and (ev["screen"] or ev["job"] or ev["lexical"])) or by_id[rec["id"]][1] >= 0.4 or (build_task and ev["product"])
        focused = len(rec.get("concepts", [])) <= 4
        screen_specific = "any" not in set(rec.get("screen_fit", ["any"]))
        demand_ok = ev["explicit_demand"] and (focused or structural or by_id[rec["id"]][1] >= 0.1) and not (screen_specific and not (ev["screen"] or ev["job"]) and by_id[rec["id"]][1] < 0.4)
        if narrow_existing and rec["kind"] == "pattern":
            if critical_ids and not (set(rec.get("concepts", [])) & set(req_ids)):
                return False
            if (req.get("intent") or {}).get("change_scope") == "local":
                return demand_ok and structural
            return ((demand_ok or ev["lexical_strong"]) and structural) or by_id[rec["id"]][1] >= 0.5
        if rec["kind"] == "pattern":   # visual patterns restyle: they need a structural reason, an explicit demand, a build task with wording, or very strong wording
            return structural or demand_ok or (build_task and ev["lexical_strong"]) or by_id[rec["id"]][1] >= 0.5
        if rec["kind"] == "chart":
            return structural or ev["lexical_strong"] or demand_ok
        purity_ok = record_purity(rec, set(req_ids) if narrow_existing else wanted) > 0 or ev["lexical_strong"]   # narrow tasks: only required concepts count
        if narrow_existing:
            named_component = ev["component"] and not (screen_specific and not ev["screen"] and req.get("screen"))
            return named_component or (structural and purity_ok) or demand_ok or (ev["lexical_strong"] and not screen_specific)
        return (structural and purity_ok) or demand_ok or by_id[rec["id"]][1] >= 0.4 or (ev["lexical_strong"] and ev["product"])

    # 1. core: positive task evidence, one per category unless a second adds uncovered concepts
    hard_cap = total_cap or BUNDLE_MAX
    not_surfaced: list[dict] = []

    def select_core():
        per_cat: dict = defaultdict(int)
        core_order = sorted(scored, key=lambda it: (-evidence[it[3]["id"]]["specificity"], 0 if evidence[it[3]["id"]]["component"] else 1, len(it[3].get("screen_fit", ["any"])) if evidence[it[3]["id"]]["screen"] else 9, -round(it[0], 3)))
        has_product_direction = build_task and any(it[3]["kind"] == "direction" and evidence[it[3]["id"]]["product"] for it in scored)
        for kinds in ((("direction",), ("component", "chart", "pattern")) if has_product_direction else (("component", "chart", "pattern"), ("direction",))):
            for it in core_order:
                if sum(1 for s_ in selected if s_[1] == "core") >= core_size:
                    break
                rec = it[3]; ev = evidence[rec["id"]]
                if rec["id"] in selected_ids:
                    continue
                floor = 0.1 if (ev["explicit_demand"] or (rec["kind"] == "direction" and build_task and ev["product"])) else 0.35
                if rec["kind"] not in kinds or it[0] < floor * top:
                    continue
                if not core_evidence_ok(rec, ev):
                    omitted.append({"id": rec["id"], "reason": "no positive task evidence (screen / subtype / component / job / product / wording) for a core record"}); continue
                if rec["kind"] == "pattern" and it[1] < 0.25 and (req.get("intent") or {}).get("artifact_state") == "existing" and not (ev["screen"] or ev["component"]):
                    omitted.append({"id": rec["id"], "reason": "visual pattern without wording evidence on an existing UI (would restyle what the task does not concern)"}); continue
                pen, why = contamination(rec, req, wanted)
                if pen >= 0.5:
                    omitted.append({"id": rec["id"], "reason": "contamination: " + "; ".join(why)}); continue
                adds_concepts = bool((set(rec.get("concepts", [])) - covered_ids) & wanted) or (bool(set(rec.get("concepts", [])) - covered_ids) and it[0] >= 0.85 * top)
                if per_cat[rec["category"]] >= 1 and ev["screen"] and compatible(rec):
                    prev = next((s_ for s_ in selected if s_[1] == "core" and s_[0][3]["category"] == rec["category"]), None)
                    if prev is not None and len(prev[0][3].get("screen_fit", ["any"])) > len(rec.get("screen_fit", ["any"])) and it[1] >= prev[0][1] - 0.05 and not (set(prev[0][3].get("concepts", [])) & critical_ids):
                        selected.remove(prev); selected_ids.discard(prev[0][3]["id"]); marginal.pop(prev[0][3]["id"], None)
                        covered_ids.clear(); covered_c.clear()
                        for s_ in selected:
                            covered_ids.update(s_[0][3].get("concepts", [])); covered_c.update(s_[0][6])
                        per_cat[rec["category"]] -= 1
                        omitted.append({"id": prev[0][3]["id"], "reason": f"replaced by the screen-specific {rec['id']}"})
                if (per_cat[rec["category"]] >= 1 and not adds_concepts) or not compatible(rec):
                    omitted.append({"id": rec["id"], "reason": "same category as a core pick (adds no new concept) or incompatible with one"}); continue
                per_cat[rec["category"]] += 1
                add(it, "core", "task evidence: " + ", ".join(k for k in ("screen", "subtype", "component", "job", "product", "lexical_strong") if ev[k]), quality="SPECIFIC")
        # 1b. most relevant rules for the wording
        for it in scored:
            rec = it[3]
            if rec["kind"] not in ("rule", "antipattern") or rec["id"] in selected_ids:
                continue
            if it[0] >= 0.75 * top and it[1] >= 0.4 and evidence[rec["id"]]["specificity"] >= 1 and compatible(rec) and sum(1 for s_ in selected if "most relevant" in s_[2]) < (1 if narrow_existing else 3):
                if contamination(rec, req, wanted)[0] < 0.5 and ((set(rec.get("concepts", [])) - covered_ids) & wanted or it[1] >= 0.6):
                    add(it, "guardrail", "most relevant record for the request wording", quality="SPECIFIC")


    def admissible(it, gained_ids, phase):
        rec = it[3]; ev = evidence[rec["id"]]
        pen, why = contamination(rec, req, wanted)
        if pen >= 0.5:
            return None, "contamination: " + "; ".join(why)
        qualities = [coverage_quality(it, req, c, ev, critical_ids) for c in gained_ids] or ["GENERIC"]
        best = max(qualities, key=lambda q: QUALITY_RANK[q])
        if rec["kind"] in CORE_KINDS and not core_evidence_ok(rec, ev):
            return None, "core-kind record without task evidence"
        strong_fit = ev["screen"] or ev["subtype"] or ev["component"] or ev["job"] or ev["lexical_strong"] or ev["problem"]
        prios = [priority_of.get(c, 2) for c in gained_ids] or [2]
        if best == "DIRECT":
            return best, ""
        if best == "SPECIFIC":
            if phase == "recommended" and (not strong_fit or (narrow_existing and not ev["lexical_strong"])):
                return None, "a recommendation needs direct task evidence" if narrow_existing else "platform-only fit: a recommendation needs task evidence"
            return best, ""
        if best == "GENERIC":
            primary_hit = bool(rec.get("concepts")) and rec["concepts"][0] in gained_ids
            named = min(prios) == 0   # the request names the concept: any focused carrier is on task
            if phase == "critical" and (primary_hit or named or ev["lexical"] or ev["problem"]):
                return best, ""
            if phase == "required" and (named or (primary_hit and (min(prios) <= 1 or min(prios) >= 3 or build_task or ev["lexical"] or high_risk or ev["problem"]))):
                return best, ""
            return None, "generic carrier: concern coverage alone is not task evidence"
        return None, "incidental coverage: the concept is a side note of unrelated guidance"

    def greedy(demand_ids: set, demand_c: set, phase: str, w_ids: float, w_c: float):
        while len(selected) < hard_cap:
            pool = []
            for it in scored:
                rec = it[3]
                if rec["id"] in selected_ids or not compatible(rec):
                    continue
                gained_ids = (set(rec.get("concepts", [])) - covered_ids) & demand_ids
                gained_c = (it[6] - covered_c) & demand_c
                if not gained_ids and not (gained_c and phase == "required" and evidence[rec["id"]]["specificity"] >= 2):
                    continue
                quality, why = admissible(it, gained_ids, phase)
                if quality is None:
                    continue
                ev = evidence[rec["id"]]
                primary_concept = 0.3 if (rec.get("concepts") and rec["concepts"][0] in gained_ids) else 0.0
                if phase == "critical":
                    primary_concept += 0.5 if len(rec.get("concepts", [])) <= 3 else (-1.2 if len(rec.get("concepts", [])) >= 5 and narrow_existing else (-0.5 if len(rec.get("concepts", [])) >= 5 and not (ev["screen"] or ev["component"] or ev["job"]) else 0.0))
                util = (w_ids * len(gained_ids) + w_c * len(gained_c) + 0.6 * QUALITY_RANK[quality] + 0.4 * ev["specificity"] + 0.8 * (it[0] / max(top, 1e-6)) + primary_concept
                        - contamination(rec, req, wanted)[0] - 0.25 * record_tokens(rec) / 300 - (0.15 if rec["kind"] == "antipattern" else 0.0))
                pool.append((util, it, gained_ids, gained_c, quality))
            if not pool:
                break
            pool.sort(key=lambda x: (-round(x[0], 3), 0 if x[1][3]["kind"] in ("rule", "antipattern") else 1, x[1][3].get("rank", 50), x[1][3]["id"]))
            util, it, gained_ids, gained_c, quality = pool[0]
            if util <= 0.5:
                break
            label = {"critical": "critical concept", "required": "required coverage", "recommended": "recommended coverage"}[phase]
            add(it, role_of(it[3]), f"{label} ({quality}): " + ", ".join([CONCEPT_LABELS.get(c, c) for c in sorted(gained_ids)] + sorted(gained_c)), gained_ids, gained_c, quality)

    # 2. critical concepts FIRST (Phase 6), then the core "what to build" records, then other required concepts
    greedy(critical_ids, set(), "critical", 3.0, 0.0)
    select_core()
    if build_task and not any(r_ == "core" for _, r_, _ in selected):
        fb = next((it for it in scored if it[3]["kind"] == "direction" and compatible(it[3]) and contamination(it[3], req, wanted)[0] < 0.5 and evidence[it[3]["id"]]["product"]), None)
        if fb:
            add(fb, "core", "new product with a stated product family: best whole-product direction", quality="SPECIFIC")
    greedy(set(req_ids) - critical_ids, set(required), "required", 2.0, 0.5)
    # 2b. specialist rules for critical concepts that only composite records cover
    for cid in [c for c in req_ids if c in critical_ids]:
        if len(selected) >= hard_cap:
            break
        coverers = [it for it, _, _ in selected if cid in it[3].get("concepts", [])]
        if not coverers or any(len(it[3].get("concepts", [])) <= 3 and it[3]["kind"] not in ("antipattern", "pattern") for it in coverers):
            continue
        spec = [it for it in scored if it[3]["kind"] == "rule" and cid in it[3].get("concepts", []) and it[3]["id"] not in selected_ids and compatible(it[3])
                and len(it[3].get("concepts", [])) <= 3 and contamination(it[3], req, wanted)[0] < 0.5]
        if spec:
            spec.sort(key=lambda it: (0 if it[3]["concepts"][0] == cid else 1, -round(it[0], 2), it[3].get("rank", 50), it[3]["id"]))
            add(spec[0], "guardrail", f"specialist rule for {CONCEPT_LABELS.get(cid, cid)} (only covered by a composite record)", quality="DIRECT")
    # 3. recommended: only when a DIRECT / SPECIFIC carrier exists; otherwise say so
    greedy(set(rec_ids), set(), "recommended", 1.0, 0.0)
    for cid in rec_ids:
        if cid not in covered_ids:
            not_surfaced.append({"concept": cid, "reason": "recommended concept not surfaced: no sufficiently specific guidance"})
    for c in recommended:
        if c not in covered_c:
            not_surfaced.append({"concern": c, "reason": "recommended concern not surfaced: no sufficiently specific guidance"})

    all_c = [it[6] for it, _, _ in selected]
    cats = [it[3]["category"] for it, _, _ in selected]
    facets = set().union(*(it[5] for it, _, _ in selected)) if selected else set()
    rf = required_facets(req)
    tokens = sum(record_tokens(it[3]) for it, _, _ in selected)
    cov_req_ids = [c for c in req_ids if c in covered_ids]
    qualities = [m["quality"] for m in marginal.values() if m.get("quality")]
    metrics = {
        "required_concerns": required, "covered_required_concerns": [c for c in required if c in covered_c],
        "uncovered_required_concerns": [c for c in required if c not in covered_c],
        "recommended_concerns": recommended, "covered_recommended_concerns": [c for c in recommended if c in covered_c],
        "coverage_ratio": round(sum(1 for c in required if c in covered_c) / len(required), 2) if required else 1.0,
        "required_concepts": req_ids, "covered_required_concepts": cov_req_ids,
        "uncovered_required_concepts": [c for c in req_ids if c not in covered_ids],
        "critical_concepts": sorted(critical_ids), "uncovered_critical_concepts": [c for c in req_ids if c in critical_ids and c not in covered_ids],
        "critical_coverage_ratio": round(sum(1 for c in critical_ids if c in covered_ids) / len(critical_ids), 2) if critical_ids else 1.0,
        "concept_coverage_ratio": round(len(cov_req_ids) / len(req_ids), 2) if req_ids else 1.0,
        "recommended_concept_coverage": round(len([c for c in rec_ids if c in covered_ids]) / len(rec_ids), 2) if rec_ids else 1.0,
        "not_surfaced": not_surfaced,
        "bundle_size": len(selected), "cap": {"soft": total_cap or BUNDLE_SOFT, "hard": hard_cap}, "core_size": sum(1 for _, r, _ in selected if r == "core"),
        "guardrail_size": sum(1 for _, r, _ in selected if r == "guardrail"),
        "bundle_tokens": tokens, "coverage_per_1k_tokens": round(len(cov_req_ids) / max(1, tokens) * 1000, 2),
        "mean_purity": round(sum(record_purity(it[3], wanted) for it, _, _ in selected) / len(selected), 2) if selected else 0.0,
        "mean_specificity": round(sum(m["specificity"] for m in marginal.values()) / len(marginal), 2) if marginal else 0.0,
        "quality_counts": {q: qualities.count(q) for q in ("DIRECT", "SPECIFIC", "GENERIC", "INCIDENTAL") if qualities.count(q)},
        "contaminated": [it[3]["id"] for it, _, _ in selected if contamination(it[3], req, wanted)[0] >= 0.5],
        "category_diversity": round(len(set(cats)) / len(cats), 2) if cats else 0.0,
        "duplicate_pressure": round(max(cats.count(c) for c in set(cats)) / len(cats), 2) if cats else 0.0,
        "facet_coverage": round(len(facets & set(rf)) / len(rf), 2) if rf else 1.0,
        "redundancy": round(1 - len(set().union(*all_c)) / max(1, sum(len(c) for c in all_c)), 2) if all_c else 0.0,
    }
    return {"selected": selected, "metrics": metrics, "omitted": omitted[:10], "marginal": marginal}


def guidance(query: str, records: list[dict] | None = None, requirements: dict | None = None, project: dict | None = None,
             hints: dict | None = None, explain: bool = False, size: int | None = None) -> dict:
    """Task-oriented retrieval: the smallest useful bundle covering the task's concerns and expected concepts."""
    records = records or load_records()
    req = requirements or build_requirements(query, project=project, hints=hints)
    concerns = derive_concerns(req)
    scope = req.get("scope", {"in_scope": True})
    if not scope.get("in_scope", True):
        return {"schema": BUNDLE_SCHEMA, "query": query, "status": "ABSTAIN", "requirements": compact_requirements(req, explain=explain),
                "scope": {k: scope.get(k) for k in ("domain", "in_scope", "reason", "nearest_ui_task")},
                "concerns": {"required": [], "recommended": [], "optional": [], "required_concepts": [], "recommended_concepts": []},
                "core": [], "guardrails": [], "metrics": {"bundle_size": 0, "coverage_ratio": 0.0, "concept_coverage_ratio": 0.0, "uncovered_required_concerns": [], "uncovered_required_concepts": [],
                                                          "bundle_tokens": 0, "coverage_per_1k_tokens": 0.0, "facet_coverage": 0.0, "category_diversity": 0.0, "duplicate_pressure": 0.0, "redundancy": 0.0, "core_size": 0, "guardrail_size": 0, "contaminated": [], "mean_purity": 0.0},
                "token_coverage": 0.0, "note": f"OUT_OF_SCOPE: {scope.get('reason')}. Nearest supported UI task: {scope.get('nearest_ui_task') or 'none'}."}
    scored, rejected, ranker, qtokens = candidates(neutralize_token_traps(_strip_reference_clauses(query)), req, records, require_evidence=False)
    wanted = {c["concept"] for c in concerns["required_concepts"]} | {c["concept"] for c in concerns["recommended_concepts"]}
    scored = [it for it in scored if it[1] > 0 or it[2] >= 0.5 or (set(it[3].get("concepts", [])) & wanted and it[2] >= 0.3)
              or (it[3]["kind"] == "direction" and it[2] >= 0.35 and any(x.startswith("product ") and x != "product any" for x in it[4]))]
    sel = select_bundle(scored, req, concerns, bundle_budget(req, concerns), size)
    core = [dict(_item(it[3], req, it[0], it[1], it[2], it[4], it[5], explain), role=role, selected_for=reason) for it, role, reason in sel["selected"] if role == "core"]
    guard = [dict(_item(it[3], req, it[0], it[1], it[2], it[4], it[5], explain), role=role, selected_for=reason) for it, role, reason in sel["selected"] if role == "guardrail"]
    m = sel["metrics"]
    coverage = (sum(t in ranker.vocab for t in qtokens) / len(qtokens)) if qtokens else 0.0
    req_status = requirements_status(req)
    if not sel["selected"]:
        status = "ABSTAIN"
    elif req_status == "AMBIGUOUS":
        status = "AMBIGUOUS"
    elif m["coverage_ratio"] < 1.0 or m["concept_coverage_ratio"] < 0.5 or any(x["field"] == "platform" for x in req["missing"]):
        status = "PARTIAL"
    else:
        status = "CONFIDENT"
    out = {"schema": BUNDLE_SCHEMA, "query": query, "status": status, "requirements": compact_requirements(req, explain=explain),
           "scope": {k: scope.get(k) for k in ("domain", "in_scope", "kind", "reason", "nearest_ui_task")},
           "concerns": {"required": concerns["required"], "recommended": concerns["recommended"], "optional": [c["concern"] for c in concerns["optional"]],
                        "required_concepts": concerns["required_concepts"], "recommended_concepts": [c["concept"] for c in concerns["recommended_concepts"]],
                        "concept_policy": concerns.get("concept_policy")},
           "core": core, "guardrails": guard, "metrics": m, "token_coverage": round(coverage, 2)}
    if not sel["selected"]:
        out["suggestions"] = ranker.suggest(qtokens)
        out["note"] = "No verified guidance. Do not present this as knowledge; use general principles from references/ and say so."
    if scope.get("kind") == "partial":
        out["note"] = "PARTIAL_SCOPE: " + (scope.get("nearest_ui_task") or scope.get("reason") or "")
    if explain:
        out["omitted"] = sel["omitted"]
        out["marginal"] = sel.get("marginal", {})
        out["rejected"] = rejected[:8]
        out["concept_trace"] = concept_trace(req, concerns, scored, sel, rejected)
        crit = [t for t in out["concept_trace"] if t.get("critical")]
        out["metrics"]["critical_trace"] = {"covered": [t["concept"] for t in crit if t["status"] == "covered"], "uncovered": [t["concept"] for t in crit if t["status"] != "covered"],
                                            "carrier_quality": {t["concept"]: t.get("carrier_quality") for t in crit if t["status"] == "covered"}}
    return out


def concept_trace(req: dict, concerns: dict, scored: list, sel: dict, rejected: list) -> list[dict]:
    """Per expected concept: why it was demanded, which records could carry it, what was selected, and the
    reason when it stays uncovered. Makes concept failures visible (Phase 5)."""
    selected_ids = {it[3]["id"] for it, _, _ in sel["selected"]}
    marginal = sel.get("marginal", {})
    by_id = {it[3]["id"]: it for it in scored}
    all_recs = {r["id"]: r for r in load_records()}
    rejected_ids = {r["id"]: r["reason"] for r in rejected}
    wanted = {c["concept"] for c in concerns["required_concepts"]} | {c["concept"] for c in concerns["recommended_concepts"]}
    trace = []
    for prio, key in (("required", "required_concepts"), ("recommended", "recommended_concepts")):
        for e in concerns[key]:
            cid = e["concept"]
            carriers = [r for r in all_recs.values() if cid in r.get("concepts", [])]
            cands = [(rid, round(by_id[rid][0], 3)) for rid in (r["id"] for r in carriers) if rid in by_id]
            cands.sort(key=lambda x: -x[1])
            picked = [rid for rid, _ in cands if rid in selected_ids]
            if picked:
                status, why = "covered", ""
            elif not carriers:
                status, why = "uncovered", "no record carries this concept"
            elif not cands:
                rej = [rejected_ids[r["id"]] for r in carriers if r["id"] in rejected_ids]
                status, why = "uncovered", ("carriers filtered before ranking: " + rej[0]) if rej else "carriers were not admissible for this platform/input/environment"
            else:
                pens = [contamination(all_recs[rid], req, wanted) for rid, _ in cands[:3]]
                if all(p_[0] >= 0.5 for p_ in pens):
                    status, why = "uncovered", "candidates rejected as contaminated: " + "; ".join(p_[1][0] for p_ in pens if p_[1])
                else:
                    status, why = "uncovered", "candidates existed but the bundle cap or a lower utility left them out"
            picked_q = None
            if picked:
                qs = [marginal.get(rid, {}).get("quality") for rid in picked if marginal.get(rid, {}).get("quality")]
                picked_q = max(qs, key=lambda q: QUALITY_RANK.get(q, 0)) if qs else None
            trace.append({"concept": cid, "priority": prio, "critical": bool(e.get("critical")), "concept_priority": e.get("priority"), "reason": e["reason"],
                          "candidate_records": cands[:4], "selected_record": picked[0] if picked else None, "carrier_quality": picked_q, "status": status, "why": why})
    return trace


def format_guidance_md(g: dict) -> str:
    r = g["requirements"]
    L = [f"## guidance: {g['query']}",
         f"status={g['status']} mode={r['mode']} platform={r['platform']} input={r['input']} product={r['product']} screen={r['screen']}{'/' + ','.join(r['screen_subtype']) if r['screen_subtype'] else ''} "
         f"stack={r['stack']} density={r['density']} env={r['environment']} risk={r['risk']} negatives={r['negative_constraints']}"]
    if r.get("missing"):
        L.append("MISSING: " + "; ".join(r["missing"]))
    if r.get("conflicts"):
        L.append("CONFLICTS: " + "; ".join(f"{c['field']} ({c['resolution']})" for c in r["conflicts"]))
    if g.get("scope") and not g["scope"].get("in_scope", True):
        L.append(f"OUT_OF_SCOPE ({g['scope']['domain']}): {g['scope']['reason']}. Nearest supported UI task: {g['scope'].get('nearest_ui_task') or 'none'}.")
        return "\n".join(L)
    L.append(f"budget={r.get('change_budget')} mode evidence: " + " | ".join(r.get("mode_evidence", [])[:4]))
    if r.get("project_context"):
        L.append("project context: " + ", ".join(f"{k}={v}" for k, v in r["project_context"].items()))
    m = g["metrics"]
    L.append(f"concepts required={m.get('concept_coverage_ratio')} covered ({len(m.get('covered_required_concepts', []))}/{len(m.get('required_concepts', []))}); tokens≈{m.get('bundle_tokens')} coverage/1k={m.get('coverage_per_1k_tokens')} purity={m.get('mean_purity')}")
    L.append(f"concerns required={[c['concern'] for c in g['concerns']['required']]} covered={m['coverage_ratio']} uncovered={m['uncovered_required_concerns']} "
             f"recommended={[c['concern'] for c in g['concerns']['recommended']]} bundle={m['bundle_size']} (core {m['core_size']} + guardrails {m['guardrail_size']}) "
             f"diversity={m['category_diversity']} redundancy={m['redundancy']}")
    if m["uncovered_required_concepts"]:
        L.append("uncovered required concepts (no record carries them for this context): " + ", ".join(m["uncovered_required_concepts"]))
    if not g["core"] and not g["guardrails"]:
        L.append(g.get("note", "No results."))
        if g.get("suggestions"):
            L.append("Closest known terms: " + ", ".join(g["suggestions"]))
        return "\n".join(L)
    marg = g.get("marginal", {})
    optional = [it for it in g["guardrails"] if str(it.get("selected_for", "")).startswith("recommended coverage")]
    critical = [it for it in g["guardrails"] if it not in optional]
    if g["core"]:
        L += ["", "### CORE (what to build)"]
    for it in g["core"]:
        L.append(f"- **{it['title']}** `{it['id']}` [{'/'.join(it['concerns'])}] — {it['guidance']}" + (f" _(covers: {', '.join(it['covers'])})_" if it['covers'] else ""))
        for stack, note in it.get("implementation", {}).items():
            L.append(f"  - {stack}: {note}")
        if it.get("why"):
            L.append(f"  - selected for: {it['selected_for']}; lexical {it['why']['lexical']}, structural {it['why']['structural']}")
    for title, items in (("### CRITICAL GUARDRAILS (must hold)", critical), ("### OPTIONAL NOTES (apply only when they fit)", optional)):
        if not items:
            continue
        L += ["", title]
        for it in items:
            q = marg.get(it["id"], {}).get("quality")
            L.append(f"- **{it['title']}** `{it['id']}` [{'/'.join(it['concerns'])}; {it['provenance']}{'; ' + q if q else ''}] — {it['guidance']}" + (f" _(covers: {', '.join(it['covers'])})_" if it['covers'] else ""))
            for stack, note in it.get("implementation", {}).items():
                L.append(f"  - {stack}: {note}")
            if it.get("why"):
                L.append(f"  - selected for: {it['selected_for']}" + (f"; marginal utility {marg[it['id']].get('utility')}" if marg.get(it["id"], {}).get("utility") is not None else ""))
    if g.get("omitted"):
        L += ["", "Omitted (redundant): " + "; ".join(f"{o['id']} ({o['reason']})" for o in g["omitted"][:6])]
    if g.get("rejected"):
        L.append("Filtered out: " + "; ".join(f"{x['id']} ({x['reason']})" for x in g["rejected"][:6]))
    if g.get("concept_trace"):
        unc = [t for t in g["concept_trace"] if t.get("status") == "uncovered"]
        L += ["", "Concept trace (explain): covered " + ", ".join(t["concept"] + (" [CRITICAL " + str(t.get("carrier_quality")) + "]" if t.get("critical") else "") for t in g["concept_trace"] if t.get("status") == "covered")]
        for t in unc[:8]:
            if t.get("critical"):
                t = dict(t, why="CRITICAL: " + str(t.get("why")))
            cands = t.get("candidate_records") or []
            L.append(f"  - UNCOVERED {t['concept']}: {t.get('why')}" + (" (candidates " + ", ".join(str(r[0]) if isinstance(r, (list, tuple)) else str(r) for r in cands[:3]) + ")" if cands else ""))
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Direction assembly + invariants (consumes the guidance bundle for guardrails)
# ---------------------------------------------------------------------------

PRESERVED_SLOT = {"navigation": "preserve_navigation", "typography": "preserve_typography", "color": "preserve_color"}

# project design context -> the pattern ids that represent the existing system per slot
CONTEXT_SLOT_PATTERNS = {
    "navigation": {"left-rail": "nav-left-rail", "top-bar": "nav-top-bar", "bottom-tabs": "nav-bottom-tabs", "hub-spoke": "nav-hub-spoke", "tv-rails": "nav-tv-side",
                   "tv-side": "nav-tv-side", "tv-top-tabs": "nav-tv-top-tabs", "menu-bar": "nav-menu-bar-desktop", "command-bar": "nav-menu-bar-desktop", "command-palette": "nav-command-palette",
                   "breadcrumb-tree": "nav-breadcrumb-tree", "drawer": "nav-left-rail", "split-view": "nav-left-rail", "master-detail": "nav-left-rail", "wizard": "nav-wizard"},
    "color": {"light-first": "color-neutral-accent", "dark-first": "color-dark-accent", "dual-theme": "color-neutral-accent"},
    "surface": {"bordered-flat": "surface-bordered-panes", "flat-tonal": "surface-flat-tonal", "elevated": "surface-elevated-cards", "imagery-backed": "surface-imagery-backed", "glass": "surface-glass"},
    "typography": {"system": "typography-system-native", "neutral-sans": "typography-neutral-sans", "geometric-sans": "typography-geometric-sans", "humanist-sans": "typography-humanist-sans",
                   "serif": "typography-serif-editorial", "monospace": "typography-monospace-technical", "rounded": "typography-rounded-friendly", "grotesk": "typography-grotesk-display", "condensed": "typography-condensed-display"},
    "density": {"low": "density-low", "medium": "density-medium", "high": "density-high"},
}
# what each change budget may alter without a stated reason
BUDGET_FREEDOM = {
    "low": set(),                                                      # polish / audit / review / accessibility: keep the system
    "moderate": {"layout", "cards", "cta", "metadata", "focus", "motion", "imagery", "icon", "density"},
    "high": {"layout", "cards", "cta", "metadata", "focus", "motion", "imagery", "icon", "density", "navigation", "surface", "typography", "color"},
    "greenfield": set(DIRECTION_SLOTS),
}
BRAND_FREEDOM = {"typography", "color", "surface", "cards", "imagery", "icon", "motion", "metadata", "cta", "layout", "density"}  # brand keeps navigation and workflow
A11Y_OVERRIDE_SLOTS = {"focus", "color", "density", "cta"}  # may change under a low budget when an accessibility/platform requirement forces it


_SLOT_WORDS = {"navigation": r"navigation|\bnav\b|sidebar|rail|tabs|menu bar|drawer", "layout": r"layout|hierarchy|structure|arrange|grid|columns|panes?", "surface": r"surface|card|panel|elevation|shadow|border",
               "cards": r"card|tile|row", "typography": r"typograph|font|type scale|heading|text size|readab", "color": r"colou?r|theme|palette|contrast|dark mode", "motion": r"motion|animation|transition",
               "focus": r"focus|keyboard|remote|d-?pad", "cta": r"button|cta|call to action|action bar|toolbar|command", "imagery": r"image|photo|hero|illustration|thumbnail|poster", "icon": r"icon", "metadata": r"metadata|badge|chip|status|label"}


def _slot_mentioned(query: str, slot: str) -> bool:
    return bool(re.search(_SLOT_WORDS.get(slot, slot), query.lower()))


def _context_value(req: dict, key: str):
    v = req.get("project_context", {}).get(key, {})
    return (v.get("value"), v.get("status")) if v.get("status") in ("KNOWN", "INFERRED") and v.get("value") not in (None, "unknown") else (None, None)


def direction(query: str, hints: dict | None = None, records: list[dict] | None = None,
              explain: bool = False, brand_hint: str | None = None,
              requirements: dict | None = None, project: dict | None = None) -> dict:
    """Visual direction per slot, constrained by the change budget and the repository's existing design
    context. Existing systems are preserved by default; every change is labelled with its reason."""
    records = records or load_records()
    req = requirements or build_requirements(query, project=project, hints=hints)
    patterns = [r for r in records if r["kind"] == "pattern"]
    by_id = {r["id"]: r for r in patterns}
    chosen, fingerprint, rejected, alternatives, compat = {}, {}, [], {}, {}
    chosen_ids: set[str] = set()
    primary = req["mode"][0] if req["mode"] else "create"
    budget = req.get("change_budget", "greenfield")
    freedom = BRAND_FREEDOM if primary == "brand" else BUDGET_FREEDOM.get(budget, set())
    has_context = any(_context_value(req, k)[0] for k in ("navigation", "theme", "surfaces", "typography", "spacing"))
    plats = set(req["platform"]); inputs = set(req["input"])
    a11y_forced = {"focus"} if (plats & {"tv", "desktop"} or inputs & {"remote", "keyboard"}) else set()
    if "kiosk" in plats:
        a11y_forced |= {"density", "cta", "focus"}

    def preserve(slot, label, why, existing_id=None):
        rec = by_id.get(existing_id) if existing_id else None
        if rec and plats and "any" not in rec["platform"] and not (set(rec["platform"]) & plats):
            rec = None  # the detected model exists but our pattern for it is another platform's; keep as implemented
        chosen[slot] = {"id": rec["id"] if rec else None, "title": f"Preserve existing {slot}: {label}", "preserved": True,
                        "guidance": (rec["guidance"] if rec else f"Keep the current {slot}; inspect and reuse it.") + " (Existing system: do not replace it for this task.)",
                        "why": [why], "score": 1.0, "provenance": "repository" if existing_id or "repository" in why else "request"}
        if rec:
            chosen_ids.add(rec["id"]); fingerprint.update(rec.get("fingerprint", {}))
        compat[slot] = {"status": "preserved", "reason": why}

    for slot in DIRECTION_SLOTS:
        flag = PRESERVED_SLOT.get(slot)
        ctx_key = {"navigation": "navigation", "color": "theme", "surface": "surfaces", "typography": "typography", "density": "spacing"}.get(slot)
        ctx_val, ctx_status = _context_value(req, ctx_key) if ctx_key else (None, None)
        if slot == "color" and ctx_val == "dual-theme":
            ctx_val = (req.get("project_context", {}).get("theme", {}).get("default") or "light") + "-first (dual theme)"
        existing_id = CONTEXT_SLOT_PATTERNS.get(slot, {}).get(str(ctx_val).split(" ")[0]) if ctx_val else None
        # 1. explicit preservation from the request
        if flag and req["constraints"].get(flag):
            preserve(slot, str(ctx_val or "as implemented"), f"request: keep the {slot}", existing_id)
            continue
        # 1b. the repository already handles focus: keep it (an accessibility task verifies it instead of replacing it)
        if slot == "focus" and req["constraints"].get("focus_handling_present") and budget in ("low", "moderate") and primary != "brand":
            note_f = " Verify the existing indicator: ≥ 3:1 against adjacent colours, visible in every theme and state." if slot in a11y_forced else ""
            preserve(slot, "as implemented" + note_f, "repository: explicit focus handling in source (keep and verify the existing focus treatment)", None)
            continue
        # 1c. moderate budget on an existing surface: a slot the task does not mention stays as implemented;
        #     only a genuinely new screen may pick layout / cards / cta / metadata / imagery freely
        artifact_new = (req.get("intent") or {}).get("artifact_state") == "new" and budget == "greenfield"
        if budget == "moderate" and req["constraints"].get("preserve_existing_system") and not ctx_val and slot != "density" and not _slot_mentioned(req["query"], slot) \
                and not (artifact_new and slot in {"layout", "cards", "cta", "metadata", "imagery"}) and not (slot in a11y_forced and slot in A11Y_OVERRIDE_SLOTS):
            preserve(slot, "as implemented", f"existing system with change budget 'moderate': the task does not concern this slot (inspect and reuse what is there)", None)
            continue
        # 2. repository evidence + change budget: preserve what the codebase already decided
        if ctx_val and slot not in freedom and slot not in (a11y_forced & A11Y_OVERRIDE_SLOTS if budget == "low" else set()) and slot != "density":
            preserve(slot, f"{ctx_val} ({ctx_status})", f"repository evidence with change budget '{budget}'", existing_id)
            continue
        # 2b. low budget: a slot the task does not mention and the repository does not describe stays as implemented
        if budget == "low" and not ctx_val and slot not in (a11y_forced & A11Y_OVERRIDE_SLOTS) and slot != "density" and not _slot_mentioned(req["query"], slot):
            preserve(slot, "as implemented", f"change budget 'low': the task does not concern this slot", None)
            continue
        if slot == "focus" and req["constraints"].get("focus_handling_present") and budget in ("low", "moderate") and slot not in freedom and slot not in a11y_forced:
            preserve(slot, "as implemented", "repository: explicit focus handling in source (keep the existing focus treatment)", None)
            continue
        # 3. density: request > repository > kiosk/outdoor floor > product inference
        low_density_context = "kiosk" in plats or set(req["environment"]) & {"outdoor", "gloves"}
        if slot == "density":
            dens_known = any(v["status"] == "KNOWN" for v in req["evidence"]["density"].values())
            dens_requested = any(v["status"] == "KNOWN" and str(v.get("reason", "")).startswith("request") for v in req["evidence"]["density"].values())
            if req["constraints"].get("preserve_existing_system") and not dens_requested and budget in ("low", "moderate"):
                floor = " Kiosk floor: targets ≥ 64 px, body ≥ 20 px." if "kiosk" in plats else (" Field-use floor: targets ≥ 48 dp with ≥ 12 dp spacing." if low_density_context else "")
                preserve(slot, (f"spacing base {ctx_val} ({ctx_status})" if ctx_val else "as implemented") + floor, f"existing system with change budget '{budget}': density is not the task", None)
                continue
            dens_requested = any(v["status"] == "KNOWN" and str(v.get("reason", "")).startswith("request") for v in req["evidence"]["density"].values())
            if req["constraints"].get("preserve_existing_system") and not dens_requested and budget in ("low", "moderate") and not (low_density_context and not dens_known and not ctx_val):
                preserve(slot, f"spacing base {ctx_val} ({ctx_status})" if ctx_val else "as implemented", f"existing system with change budget '{budget}': density is not the task", None)
                continue
            if not dens_known and low_density_context:
                rec = by_id.get("density-low")
                note = " Kiosk: targets ≥ 64 px, body ≥ 20 px (platform floor overrides the generic numbers)." if "kiosk" in plats else " Field use: targets ≥ 48 dp with ≥ 12 dp spacing, large glanceable status."
                chosen[slot] = {"id": rec["id"], "title": rec["title"], "guidance": rec["guidance"] + note, "why": ["kiosk platform: low density unless stated" if "kiosk" in plats else "outdoor/gloves: low density unless stated"], "score": 1.0, "provenance": rec["provenance"]}
                chosen_ids.add(rec["id"]); fingerprint.update(rec.get("fingerprint", {})); compat[slot] = {"status": "changed" if ctx_val else "new", "reason": chosen[slot]["why"][0]}
                continue
            if not dens_known and ctx_val and slot not in freedom:
                preserve(slot, f"spacing base {ctx_val} ({ctx_status})", f"repository spacing rhythm with change budget '{budget}'", None)
                continue
            if req["density"]:
                rec = by_id.get(f"density-{req['density']}")
                if rec:
                    st = next(iter(req["evidence"]["density"].values()))["status"]
                    chosen[slot] = {"id": rec["id"], "title": rec["title"], "guidance": rec["guidance"], "why": [f"density {req['density']} ({st})"], "score": 1.0, "provenance": rec["provenance"]}
                    chosen_ids.add(rec["id"]); fingerprint.update(rec.get("fingerprint", {})); compat[slot] = {"status": "new", "reason": chosen[slot]["why"][0]}
                    continue
        # 4. search the slot
        res = search(query, patterns, k=6, kinds={"pattern"}, categories={slot}, per_category=6,
                     explain=True, require_evidence=False, requirements=req, facets=False)
        compatible_results = []
        media_signal = bool(set(req["screen"]) & {"player", "home"} or set(req["screen_subtype"]) & {"rails", "epg"} or "media" in req["product"] or set(req["components"]) & {"media"})
        for c in res["results"]:
            rec = by_id[c["id"]]
            rpf_slot = set(rec.get("product_fit", ["any"]))
            if "any" not in rpf_slot and rpf_slot <= {"media", "education", "games"} and not media_signal and not (set(req["product"]) & rpf_slot):
                rejected.append({"slot": slot, "id": rec["id"], "reason": f"media-specific pattern ({','.join(sorted(rpf_slot))}) with no media signal in the request or repository"})
                continue
            conflict = [x for x in rec.get("incompatible", []) if x in chosen_ids]
            back_conflict = [cid for cid in chosen_ids if rec["id"] in by_id[cid].get("incompatible", [])]
            if conflict or back_conflict:
                rejected.append({"slot": slot, "id": rec["id"], "reason": "incompatible with " + ",".join(conflict + back_conflict)})
                continue
            compatible_results.append((c, rec))
        envs = set(req["environment"])
        if envs & {"outdoor", "gloves"} and slot == "surface":
            kept = [(c, r) for c, r in compatible_results if r.get("fingerprint", {}).get("surface_strategy") not in ("elevated", "glass", "imagery-backed")]
            for c, r in compatible_results:
                if (c, r) not in kept:
                    rejected.append({"slot": slot, "id": r["id"], "reason": "outdoor/gloves: surface washes out in sunlight"})
            compatible_results = kept or compatible_results
        theme_val, _ = _context_value(req, "theme")
        if theme_val == "dual-theme":
            theme_val = (req.get("project_context", {}).get("theme", {}).get("default") or "light") + "-first"
        if slot == "color" and theme_val in ("light-first", "dark-first") and primary != "brand":
            bad = "dark-first" if theme_val == "light-first" else "light-first"
            kept = [(c, r) for c, r in compatible_results if r.get("fingerprint", {}).get("color_strategy") != bad]
            for c, r in compatible_results:
                if (c, r) not in kept:
                    rejected.append({"slot": slot, "id": r["id"], "reason": f"theme polarity: project is {theme_val}"})
            compatible_results = kept or compatible_results
        if not compatible_results:
            chosen[slot] = None; compat[slot] = {"status": "unfilled", "reason": "no compatible option"}
            continue
        pick = compatible_results[0]
        prods = set(req["product"])

        def fits_product(r):
            return "any" in r["product_fit"] or (prods and set(r["product_fit"]) & prods)
        if not fits_product(pick[1]):
            alt = next(((c, r) for c, r in compatible_results[1:] if fits_product(r) and c["score"] >= (0.55 if prods else 0.75) * pick[0]["score"]), None)
            if alt:
                rejected.append({"slot": slot, "id": pick[1]["id"], "reason": f"product-specific ({','.join(pick[1]['product_fit'])}) does not fit request product {sorted(prods) or 'unknown'}; alternative within 25%"})
                pick = alt
        # existing system wins when the search pick is only marginally better and the budget is not free
        if existing_id and existing_id != pick[1]["id"] and slot in freedom and budget != "greenfield" and primary != "brand":
            ex_c = next((c for c, r in compatible_results if r["id"] == existing_id), None)
            if ex_c and ex_c["score"] >= 0.8 * pick[0]["score"]:
                pick = (ex_c, by_id[existing_id]); compat[slot] = {"status": "preserved", "reason": f"existing {ctx_val} scores within 20% of the alternative; kept under budget '{budget}'"}
        c, rec = pick
        chosen_ids.add(rec["id"])
        chosen[slot] = {"id": rec["id"], "title": rec["title"], "guidance": rec["guidance"], "why": c["why"]["matched"], "score": c["score"], "provenance": rec["provenance"]}
        alternatives[slot] = [{"id": x["id"], "title": x["title"], "score": x["score"]} for x in res["results"][1:4] if x["id"] != rec["id"]]
        fingerprint.update(rec.get("fingerprint", {}))
        if slot not in compat:
            if existing_id and existing_id == rec["id"]:
                compat[slot] = {"status": "preserved", "reason": "search agrees with the existing system"}
            elif ctx_val:
                why = "brand mode may change visual identity" if primary == "brand" else ("accessibility/platform requirement" if slot in a11y_forced else f"allowed by change budget '{budget}'")
                compat[slot] = {"status": "changed", "reason": f"existing {ctx_val} ({ctx_status}) → {rec['id']}: {why}"}
            else:
                compat[slot] = {"status": "new", "reason": "no repository evidence for this slot"}

    g = guidance(query, records, requirements=req)
    guard_groups: dict[str, list] = {"interaction": [], "accessibility": [], "platform": [], "states": [], "feedback": [], "privacy_environment": [], "anti_patterns": []}
    for it in g["guardrails"]:
        entry = {"id": it["id"], "title": it["title"], "guidance": it["guidance"], "concerns": it["concerns"], "covers": it["covers"]}
        cs = set(it["concerns"])
        if it["kind"] == "antipattern":
            guard_groups["anti_patterns"].append(entry)
        elif cs & {"privacy", "environment"}:
            guard_groups["privacy_environment"].append(entry)
        elif "interaction" in cs:
            guard_groups["interaction"].append(entry)
        elif "accessibility" in cs:
            guard_groups["accessibility"].append(entry)
        elif "states" in cs:
            guard_groups["states"].append(entry)
        elif "feedback" in cs:
            guard_groups["feedback"].append(entry)
        elif "platform" in it["facets"]:
            guard_groups["platform"].append(entry)
        else:
            guard_groups["accessibility"].append(entry)
    a11y = [e for grp in ("accessibility", "interaction", "platform") for e in guard_groups[grp]]
    ledger = {"KNOWN": [f"{e['field']}: {e['value']} ({e['reason']})" for e in req["known"]],
              "INFERRED": [f"{e['field']}: {e['value']} ({e['reason']})" for e in req["inferred"]],
              "MISSING": [f"{m['field']}: {m['reason']}" for m in req["missing"]]}
    n_ctx = sum(1 for k in ("navigation", "theme", "surfaces", "typography", "spacing") if _context_value(req, k)[0])
    preserved = [k for k, v in compat.items() if v["status"] == "preserved"]
    changed = [k for k, v in compat.items() if v["status"] == "changed"]
    unjustified = [k for k in changed if budget == "low" and k not in a11y_forced]
    out = {"query": query, "brand": brand_hint, "requirements": compact_requirements(req), "signals": _compact_signals(req),
           "ledger": ledger, "change_budget": budget, "project_context": {k: v for k, v in req.get("project_context", {}).items() if v.get("status") != "UNKNOWN"},
           "direction": chosen, "compatibility": compat,
           "preservation": {"context_slots_detected": n_ctx, "preserved": preserved, "changed": changed, "unjustified_structural_change": unjustified,
                            "navigation_preserved": compat.get("navigation", {}).get("status") == "preserved", "theme_preserved": compat.get("color", {}).get("status") == "preserved",
                            "typography_preserved": compat.get("typography", {}).get("status") == "preserved"},
           "fingerprint": fingerprint, "concerns": g["concerns"], "guardrails": {k: v for k, v in guard_groups.items() if v}, "guidance_metrics": g["metrics"],
           "core_guidance": [{"id": c["id"], "title": c["title"], "guidance": c["guidance"]} for c in g["core"]],
           "accessibility_constraints": a11y, "anti_patterns_to_avoid": guard_groups["anti_patterns"],
           "note": "Reconcile every slot with the existing codebase before implementing; preserved slots are the existing system and win unless the task is to change them. Guardrails are not optional."}
    out["validation"] = validate_direction(out, req, by_id)
    if explain:
        out["alternatives"] = alternatives
        out["rejected"] = rejected
    return out


def validate_direction(d: dict, req: dict, by_id: dict | None = None) -> dict:
    by_id = by_id or {r["id"]: r for r in load_records() if r["kind"] == "pattern"}
    v: list[str] = []
    fp = d["fingerprint"]
    plats = set(req["platform"]); inputs = set(req["input"])
    chosen = {slot: (c or {}).get("id") for slot, c in d["direction"].items()}
    primary = req["mode"][0] if req["mode"] else "create"
    if "tv" in plats or "remote" in inputs:
        if not chosen.get("focus") and not (d["direction"].get("focus") or {}).get("preserved"):
            v.append("tv/remote: focus slot missing")
        elif fp.get("focus_strategy") in ("ring", "underline", "none-touch-only", "browser-default"):
            v.append(f"tv/remote: focus strategy '{fp.get('focus_strategy')}' is not a 10-foot focus treatment")
        if fp.get("navigation_model") in ("top-bar", "left-rail", "bottom-tabs", "menu-bar"):
            v.append(f"tv/remote: navigation '{fp.get('navigation_model')}' is a pointer/touch model")
        if chosen.get("cta") and by_id.get(chosen["cta"], {}).get("input") == ["touch"]:
            v.append("tv/remote: CTA pattern is touch-only")
    if "desktop" in plats and "keyboard" in inputs and not chosen.get("focus") and not (d["direction"].get("focus") or {}).get("preserved"):
        v.append("desktop/keyboard: focus slot missing")
    if "kiosk" in plats:
        if fp.get("focus_strategy") not in (None, "none-touch-only"):
            v.append("kiosk: focus treatment should be touch-first")
        if fp.get("content_density") == "high":
            v.append("kiosk: high density is unsuitable for public touch use")
    if ("erp" in req["product"] or req["density"] == "high") and fp.get("content_density") == "low":
        v.append("dense product: low/spacious density selected")
    if primary in ("accessibility", "audit") and not d["accessibility_constraints"] and not any((req.get("accessibility") or {}).values()):
        v.append("audit: no accessibility constraints attached")
    if primary == "brand" and len(fp) < len(FINGERPRINT_AXES):
        v.append(f"brand: fingerprint incomplete ({len(fp)}/{len(FINGERPRINT_AXES)} axes)")
    if req["constraints"].get("preserve_navigation") and chosen.get("navigation") and not (d["direction"].get("navigation") or {}).get("preserved"):
        v.append("preserve_navigation violated: a navigation pattern was selected")
    if req["constraints"].get("preserve_typography") and chosen.get("typography") and not (d["direction"].get("typography") or {}).get("preserved"):
        v.append("preserve_typography violated: a typography pattern was selected")
    if "rails" in req["negative_constraints"] and fp.get("layout_topology") in ("rails", "immersive-hero-rails"):
        v.append("negative constraint 'no rails' violated by layout")
    if "card" in req["negative_constraints"] and fp.get("card_geometry") not in (None, "none", "list-row"):
        v.append("negative constraint 'no cards' violated by card geometry")
    if "sidebar" in req["negative_constraints"] and fp.get("navigation_model") in ("left-rail", "left-drawer"):
        v.append("negative constraint 'no sidebar' violated by navigation")
    if "glass" in req["negative_constraints"] and fp.get("surface_strategy") == "glass":
        v.append("negative constraint 'no glass' violated by surface")
    if "animation" in req["negative_constraints"] and fp.get("motion_character") not in (None, "none", "functional-minimal"):
        v.append("negative constraint 'no animation' violated by motion")
    gm = d.get("guidance_metrics", {})
    if plats and "interaction" in gm.get("uncovered_required_concerns", []):
        v.append("guardrails: critical interaction concept uncovered") if (d.get("guidance_metrics") or {}).get("uncovered_critical_concepts") else None
    for slot in d.get("preservation", {}).get("unjustified_structural_change", []):
        v.append(f"change budget '{d.get('change_budget')}': slot '{slot}' changes the existing system without an accessibility/platform reason")
    if req["constraints"].get("preserve_color") and chosen.get("color") and not (d["direction"].get("color") or {}).get("preserved"):
        v.append("preserve_color violated: a colour pattern was selected")
    envs = set(req.get("environment", []))
    if envs & {"outdoor", "gloves"} and fp.get("surface_strategy") in ("elevated", "glass", "imagery-backed"):
        v.append(f"outdoor/gloves: surface '{fp.get('surface_strategy')}' washes out in sunlight; use flat high-contrast surfaces")
    if req["product"] and "media" not in req["product"] and "education" not in req["product"] and str(fp.get("card_geometry", "")).startswith("poster"):
        v.append("non-media product: poster (media) card geometry selected")
    if "kiosk" in plats and fp.get("content_density") == "medium":
        v.append("kiosk: medium density selected; kiosk targets ≥ 64 px need low density")
    if "tv" in plats and fp.get("color_strategy") in ("light-first", "paper"):
        v.append("tv: light-first colour strategy; TV is dark-first")
    for a, cid in chosen.items():
        if not cid:
            continue
        for b, other in chosen.items():
            if other and other in by_id.get(cid, {}).get("incompatible", []):
                v.append(f"incompatible pair chosen: {cid} / {other}")
    return {"ok": not v, "violations": v}


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_direction_md(d: dict) -> str:
    lines = [f"# Design direction: {d['query']}"]
    if d.get("brand"):
        lines.append(f"Brand: {d['brand']}")
    lines.append("")
    for status in ("KNOWN", "INFERRED", "MISSING"):
        items = d["ledger"].get(status, [])
        if items:
            lines.append(f"**{status}:** " + "; ".join(items))
    if d["requirements"].get("conflicts"):
        lines.append("**CONFLICTS:** " + "; ".join(f"{c['field']}: request {c['request']} vs project {c['project']} → {c['resolution']}" for c in d["requirements"]["conflicts"]))
    if d.get("project_context"):
        lines.append("**Project context:** " + "; ".join(f"{k}={v['value']} ({v['status']})" for k, v in d["project_context"].items()))
    lines.append(f"**Change budget:** {d.get('change_budget')} · preserved {d.get('preservation', {}).get('preserved')} · changed {d.get('preservation', {}).get('changed')}")
    lines += ["", "| Slot | Choice | Status | Why |", "|---|---|---|---|"]
    for slot, c in d["direction"].items():
        st = d.get("compatibility", {}).get(slot, {})
        if c:
            lines.append(f"| {slot} | {c['title']}{' (`' + c['id'] + '`)' if c.get('id') else ''} | {st.get('status', '')} | {st.get('reason') or ', '.join(c['why']) or 'lexical'} |")
        else:
            lines.append(f"| {slot} | *(no compatible option; decide from references)* | unfilled | |")
    lines += ["", "## Guidance per slot"]
    for slot, c in d["direction"].items():
        if c:
            lines.append(f"- **{slot}** — {c['guidance']}")
    if d.get("core_guidance"):
        lines += ["", "## Core guidance (components / layouts to build)"]
        for c in d["core_guidance"]:
            lines.append(f"- **{c['title']}** — {c['guidance']}")
    gm = d.get("guidance_metrics", {})
    lines += ["", f"## Guardrails (required concerns: {', '.join(gm.get('required_concerns', []))}; uncovered: {', '.join(gm.get('uncovered_required_concerns', [])) or 'none'})"]
    for grp, items in d.get("guardrails", {}).items():
        lines.append(f"**{grp.replace('_', ' / ')}**")
        for r in items:
            lines.append(f"- {r['title']}: {r['guidance']}" + (f" _(covers: {', '.join(r['covers'])})_" if r.get('covers') else ""))
    lines += ["", "## Fingerprint", "```json", json.dumps(d["fingerprint"], indent=2), "```"]
    val = d.get("validation", {})
    lines += ["", "## Validation: " + ("OK" if val.get("ok") else "VIOLATIONS")]
    lines += [f"- {x}" for x in val.get("violations", [])]
    if d.get("alternatives"):
        lines += ["", "## Alternatives considered"] + [f"- {slot}: " + ", ".join(f"{a['title']} ({a['score']})" for a in alts) for slot, alts in d["alternatives"].items() if alts]
    if d.get("rejected"):
        lines += ["", "## Rejected for incompatibility"] + [f"- {r['slot']}: {r['id']} — {r['reason']}" for r in d["rejected"]]
    lines += ["", d["note"]]
    return "\n".join(lines)


def format_search_md(res: dict) -> str:
    s = res["signals"]
    lines = [f"## design-engineering search: {res['query']}",
             f"status={res['status']} modes={s['modes']} platforms={s['platforms']} inputs={s['inputs']} products={s['products']} "
             f"density={s['density']['value']} stacks={list(s['stacks'])} screens={s['screens']} negatives={s['negatives']}"]
    cov = res.get("coverage", {})
    if cov.get("required_facets"):
        lines.append(f"facets required={cov['required_facets']} unmet={cov['required_facets_unmet']} diversity={cov['category_diversity']}")
    if res.get("missing"):
        lines.append("MISSING: " + "; ".join(res["missing"]))
    if res.get("conflicts"):
        lines.append("CONFLICTS: " + "; ".join(f"{c['field']} ({c['resolution']})" for c in res["conflicts"]))
    if not res["results"]:
        lines.append(res.get("note", "No results."))
        if res.get("suggestions"):
            lines.append("Closest known terms: " + ", ".join(res["suggestions"]))
        return "\n".join(lines)
    for r in res["results"]:
        lines += ["", f"### {r['title']}  `{r['id']}`  [{r['kind']}/{r['category']}; {'/'.join(r['facets'])}] score {r['score']} · {r['provenance']}", r["guidance"],
                  f"- use when: {r['use_when']}", f"- avoid when: {r['avoid_when']}"]
        for stack, note in r.get("implementation", {}).items():
            lines.append(f"- {stack}: {note}")
        if r.get("incompatible"):
            lines.append(f"- incompatible with: {', '.join(r['incompatible'])}")
        if r.get("why"):
            lines.append(f"- why: lexical {r['why']['lexical']}, structural {r['why']['structural']} ({', '.join(r['why']['matched']) or 'generic'})")
    if res.get("rejected"):
        lines += ["", "Filtered out: " + "; ".join(f"{x['id']} ({x['reason']})" for x in res["rejected"])]
    return "\n".join(lines)
