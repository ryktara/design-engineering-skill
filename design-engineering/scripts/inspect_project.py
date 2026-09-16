#!/usr/bin/env python3
"""Cheap, deterministic project inspection for UI work.

  python inspect_project.py <project-root> [--json] [--out inspect.json] [--max-files 4000]

Reads manifests and a bounded sample of source files; never descends into node_modules,
build output, caches, or binaries. Output is compact JSON suitable for model context plus
a markdown summary. Confidence per finding: KNOWN (read from a manifest/config) or
INFERRED (from file names or content heuristics).
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

IGNORE_DIRS = {"node_modules", ".git", ".hg", ".svn", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit",
               ".output", ".turbo", ".cache", "coverage", "target", "bin", "obj", ".gradle", ".idea", ".vs",
               ".vscode", "Pods", "DerivedData", ".dart_tool", ".pub-cache", "__pycache__", ".venv", "venv",
               "vendor", "storybook-static", ".expo", ".angular", "packages-cache", "tmp", "temp", ".claude", "render", "screenshots"}
TEXT_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".css", ".scss", ".sass",
            ".less", ".html", ".kt", ".kts", ".java", ".swift", ".dart", ".xaml", ".cs", ".axaml", ".json",
            ".xml", ".md", ".yaml", ".yml", ".toml", ".gradle", ".pbxproj"}
MAX_READ = 200_000  # bytes per file; larger files are skipped

# dependency name -> (stack group, platform hints, ui library label)
DEP_MAP = {
    "next": ("nextjs", ["web"], None), "react": ("react", ["web"], None), "react-dom": ("react", ["web"], None),
    "vue": ("vue", ["web"], None), "nuxt": ("nuxt", ["web"], None), "svelte": ("svelte", ["web"], None),
    "@sveltejs/kit": ("svelte", ["web"], None), "@angular/core": ("angular", ["web"], None), "astro": ("astro", ["web"], None),
    "tailwindcss": ("tailwind", [], "tailwind"), "@tailwindcss/vite": ("tailwind", [], "tailwind"),
    "react-native": ("react-native", ["mobile"], None), "expo": ("react-native", ["mobile"], None),
    "react-native-tvos": ("react-native", ["tv"], None), "@react-native-tvos/config-tv": ("react-native", ["tv"], None),
    "@radix-ui/react-dialog": ("shadcn", [], "radix"), "class-variance-authority": ("shadcn", [], "shadcn-style cva"),
    "@mui/material": ("react", [], "mui"), "antd": ("react", [], "antd"), "@chakra-ui/react": ("react", [], "chakra"),
    "@mantine/core": ("react", [], "mantine"), "@headlessui/react": ("react", [], "headlessui"),
    "vuetify": ("vue", [], "vuetify"), "primevue": ("vue", [], "primevue"), "@nuxt/ui": ("nuxt", [], "nuxt-ui"),
    "@angular/material": ("angular", [], "angular-material"), "primeng": ("angular", [], "primeng"),
    "bootstrap": ("html-css", [], "bootstrap"), "@fluentui/react-components": ("react", [], "fluent"),
    "styled-components": ("react", [], "styled-components"), "@emotion/react": ("react", [], "emotion"),
    "@stitches/react": ("react", [], "stitches"), "@vanilla-extract/css": ("react", [], "vanilla-extract"),
    "framer-motion": ("react", [], "framer-motion"), "motion": ("react", [], "motion"), "gsap": ("html-css", [], "gsap"),
    "lucide-react": ("react", [], "icons:lucide"), "@phosphor-icons/react": ("react", [], "icons:phosphor"),
    "@heroicons/react": ("react", [], "icons:heroicons"), "react-icons": ("react", [], "icons:react-icons"),
    "@tabler/icons-react": ("react", [], "icons:tabler"), "@iconify/vue": ("vue", [], "icons:iconify"),
    "@tanstack/react-table": ("react", [], "table:tanstack"), "ag-grid-react": ("react", [], "table:ag-grid"),
    "@tanstack/react-virtual": ("react", [], "virtualization:tanstack-virtual"), "react-window": ("react", [], "virtualization:react-window"),
    "recharts": ("react", [], "charts:recharts"), "chart.js": ("html-css", [], "charts:chart.js"), "d3": ("html-css", [], "charts:d3"),
    "echarts": ("html-css", [], "charts:echarts"), "@nivo/core": ("react", [], "charts:nivo"), "victory": ("react", [], "charts:victory"),
    "@norigin/spatial-navigation": ("react", ["tv"], "spatial-navigation"), "@bam.tech/lrud": ("react", ["tv"], "lrud"),
    "@noriginmedia/norigin-spatial-navigation": ("react", ["tv"], "spatial-navigation"),
    "eslint-plugin-jsx-a11y": ("react", [], "a11y:jsx-a11y"), "@axe-core/react": ("react", [], "a11y:axe"), "axe-core": ("html-css", [], "a11y:axe"),
    "@playwright/test": ("any", [], "test:playwright"), "cypress": ("any", [], "test:cypress"), "@storybook/react": ("react", [], "storybook"),
    "next-intl": ("nextjs", [], "i18n:next-intl"), "react-i18next": ("react", [], "i18n:react-i18next"), "i18next": ("any", [], "i18n:i18next"), "vue-i18n": ("vue", [], "i18n:vue-i18n"),
    "electron": ("react", ["desktop"], "electron"), "@tauri-apps/api": ("react", ["desktop"], "tauri"),
    "three": ("html-css", [], "three.js"), "@react-three/fiber": ("react", [], "r3f"),
}
GRADLE_MAP = {
    "androidx.compose": ("compose", ["mobile"], "compose"),
    "androidx.tv:tv-material": ("compose-tv", ["tv"], "compose-tv-material"),
    "androidx.tv:tv-foundation": ("compose-tv", ["tv"], "compose-tv-foundation"),
    "androidx.leanback": ("compose-tv", ["tv"], "leanback (views)"),
    "androidx.compose.material3": ("compose", ["mobile"], "material3"),
    "com.google.android.material": ("compose", ["mobile"], "material-components-views"),
    "androidx.media3": ("compose", [], "media3"),
    "coil": ("compose", [], "images:coil"), "com.github.bumptech.glide": ("compose", [], "images:glide"),
}
DOTNET_MAP = {
    "Microsoft.WindowsAppSDK": ("winui", ["desktop"], "winui3"), "Microsoft.UI.Xaml": ("winui", ["desktop"], "winui"),
    "UseWPF": ("wpf", ["desktop"], "wpf"), "Avalonia": ("avalonia", ["desktop"], "avalonia"),
    "Uno.": ("winui", ["desktop", "mobile"], "uno"), "CommunityToolkit.WinUI": ("winui", [], "community-toolkit"),
    "MaterialDesignThemes": ("wpf", [], "material-design-in-xaml"), "DevExpress.Win": ("wpf", ["desktop"], "devexpress-winforms"),
    "DevExpress.Wpf": ("wpf", ["desktop"], "devexpress-wpf"), "MahApps.Metro": ("wpf", [], "mahapps"), "UseWindowsForms": ("wpf", ["desktop"], "winforms"),
}
FONT_RE = re.compile(r"fonts\.googleapis\.com/css2?\?family=([^&\"')]+)|@font-face\s*{[^}]*font-family:\s*['\"]?([^;'\"]+)|next/font/google['\"];?\s*(?:import|const)?[^;]*?\b([A-Z][A-Za-z_]+)\b|font-family:\s*['\"]?([A-Za-z][A-Za-z0-9 ]+)", re.I)
CSS_VAR_RE = re.compile(r"--([a-z][a-z0-9-]*)\s*:")
MEDIA_RE = re.compile(r"@media[^{]*\(\s*(?:min|max)-width\s*:\s*(\d+)(px|em|rem)")
FOCUS_RE = re.compile(r"focus-visible|:focus|isFocused|onFocusChanged|focusRequester|FocusRequester|focusable\(|Focusable|GotFocus|IsTabStop|KeyboardNavigation|IsKeyboardFocused|FocusVisual|UseSystemFocusVisuals|Focus\.Ring|focus-ring|focus:ring|ring-offset|@FocusState|focused\(|prefersDefaultFocus", re.I)
A11Y_RE = re.compile(r"aria-[a-z]+|role=|contentDescription|accessibilityLabel|semantics\s*\{|Semantics\(|AutomationProperties|accessibilityRole", re.I)
DPAD_RE = re.compile(r"KEYCODE_DPAD|\bd-?pad\b|onKeyEvent|Key\.DirectionLeft|DirectionRight|LEANBACK_LAUNCHER|remote control|SpatialNavigation|setFocusable|nextFocus|focusRestorer|TvLazy|androidx\.tv|hasTVPreferredFocus|TVFocusGuideView|TVEventHandler|focusSection|\bisTV\b|\bisTv\b", re.I)


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_READ:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def walk(root: Path, max_files: int):
    count = 0
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir(), key=lambda p: p.name)
        except OSError:
            continue
        for p in entries:
            if p.is_dir():
                if p.name in IGNORE_DIRS or p.name.startswith("."):
                    continue
                stack.append(p)
            else:
                if p.suffix.lower() in TEXT_EXT:
                    count += 1
                    if count > max_files:
                        return
                    yield p


# ---------------------------------------------------------------- design context (Phase 4)
NAV_SIGNALS = {
    "left-rail": [r"<aside\b", r"\bSidebar\b", r"sidebar", r"nav-rail", r"NavigationRail", r"<NavigationView\b(?![^>]*PaneDisplayMode=\"Top\")", r"NavigationView\s*\(", r"PaneDisplayMode=\"Left", r"PermanentNavigationDrawer", r"NavigationDrawer", r"ModalNavigationDrawer", r"SplitView\b", r"NavigationSplitView", r"left-nav", r"side-nav", r"Sidenav"],
    "top-bar": [r"<header\b[^>]*>\s*<nav", r"<nav\b[^>]*class(?:Name)?=\"[^\"]*(?:top|header|navbar|primary)", r"\bNavbar\b", r"\bTopBar\b", r"\btopbar\b", r"top-nav", r"TopAppBar", r"AppBar\b", r"PaneDisplayMode=\"Top", r"toolbar-nav", r"<header\b[^>]*class(?:Name)?=\"[^\"]*(?:app|top|site)"],
    "bottom-tabs": [r"BottomNavigation", r"NavigationBar\s*\(", r"BottomNavigationBar", r"TabBar\b", r"\bTabView\b", r"UITabBar", r"bottom-nav", r"BottomTabs", r"createBottomTabNavigator", r"NavigationBarItem"],
    "menu-bar": [r"<Menu\b", r"<MenuBar\b", r"<CommandBar\b", r"<ToolBar\b", r"MenuFlyout", r"NSMenu", r"\bMenuBar\b", r"<Ribbon"],
    "tv-rails": [r"TvLazyRow", r"TvLazyColumn", r"\bLazyRow\b", r"ImmersiveList", r"\brail\b", r"Rails\b", r"HorizontalGridView", r"RowsSupportFragment", r"BrowseSupportFragment", r"focusRestorer"],
    "hub-spoke": [r"(?<![a-z])hub(?![a-z])", r"\battract\b", r"idle-screen", r"home-hub", r"start-over", r"(?<![A-Za-z])Hub\b"],
    "master-detail": [r"master-detail", r"MasterDetail", r"ListDetailPaneScaffold", r"TwoPane", r"detail-pane", r"split-pane"],
    "breadcrumb-tree": [r"Breadcrumb", r"TreeView\b", r"<tree\b", r"role=\"tree\""],
    "command-palette": [r"CommandPalette", r"command-palette", r"cmdk", r"CommandDialog"],
    "wizard": [r"Stepper\b", r"wizard", r"step-indicator", r"Wizard\b"],
}
NAV_PRIORITY = ["left-rail", "top-bar", "bottom-tabs", "menu-bar", "tv-rails", "master-detail", "breadcrumb-tree", "command-palette", "wizard", "hub-spoke"]
NAV_WEIGHT = {"breadcrumb-tree": 0.4, "wizard": 0.5, "hub-spoke": 0.7, "command-palette": 0.6, "master-detail": 0.8}
TW_SPACING_RE = re.compile(r"(?<![a-z-])(?:p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|gap|gap-x|gap-y|space-x|space-y)-(\d{1,2})(?![\w-])")
SHELL_HINT_FILES = ("layout", "shell", "app", "main", "root", "scaffold", "navigation", "sidebar", "navbar", "window", "home")
HEX_RE = re.compile(r"#([0-9a-fA-F]{6})\b")
ROOT_BG_RE = re.compile(r"(?::root|html|body)[^{]*\{[^}]*(?:--(?:background|bg|surface|canvas)[a-z0-9-]*|background(?:-color)?)\s*:\s*(#[0-9a-fA-F]{3,6}|hsl\([^)]*\)|rgb\([^)]*\)|oklch\([^)]*\))", re.I | re.S)
RADIUS_RE = re.compile(r"(?:border-radius|--radius[a-z0-9-]*|CornerRadius|cornerRadius|RoundedCornerShape|borderRadius|BorderRadius\.circular|Radius\.circular)\s*[:=(]\s*\"?(\d+(?:\.\d+)?)\s*(px|dp|pt|rem|em)?(?!\s*%)", re.I)
SPACING_RE = re.compile(r"(?:padding|margin|gap|Padding|Margin|spacing|Spacer|\.padding\(|Thickness=\"|EdgeInsets\.(?:all|symmetric|only)\([a-z:]*|SizedBox\((?:height|width):\s*)\s*[:=(\"]*\s*(\d{1,3})(?:px|dp|pt|\b)", re.I)
REM_SPACING_RE = re.compile(r"(?:padding|margin|gap)[a-z-]*\s*:\s*(\d*\.?\d+)rem", re.I)
XAML_FONT_RE = re.compile(r"<FontFamily[^>]*>([^<]+)</FontFamily>|FontFamily=\"([A-Za-z][A-Za-z0-9 ]+)\"|--font-(?:sans|body|display|heading|mono|family)[a-z-]*\s*:\s*['\"]?([A-Za-z][A-Za-z0-9 ]+)|from\s+['\"]geist/font(?:/([a-z]+))?['\"]|Font\.custom\(\s*\"([A-Za-z][A-Za-z0-9 ]+)\"|GoogleFonts\.([a-zA-Z]+)TextTheme|fontFamily:\s*['\"]([A-Za-z][A-Za-z0-9 ]+)['\"]|R\.font\.([a-z0-9_]+)|FontFamily\(\s*Font\(R\.font\.([a-z0-9_]+)", re.I)
NATIVE_LIGHT_RE = re.compile(r"lightColorScheme|Brightness\.light|\.light\b|ColorScheme\.fromSeed\([^)]*brightness:\s*Brightness\.light", re.I)
XAML_BRUSH_BG_RE = re.compile(r"x:Key=\"[^\"]*(?:Canvas|Background|Bg\.|Window|Surface)[^\"]*\"\s+Color=\"#(?:FF)?([0-9A-Fa-f]{6})\"", re.I)
COMPOSE_BG_RE = re.compile(r"(?:background|surface)\s*=\s*Color\(0x(?:FF)?([0-9A-Fa-f]{6})\)", re.I)
SHADOW_RE = re.compile(r"box-shadow\s*:\s*(?!none)|\belevation\s*[:=]\s*\"?(?!0(?:\.0)?\b)\d|\.shadow\(\s*(?!0\b)|shadowElevation\s*=\s*(?!0)|DropShadow|class(?:Name)?=\"[^\"]*\bshadow(?:-(?:sm|md|lg|xl|2xl))?\b", re.I)
BORDER_RE = re.compile(r"\bborder(?:-(?:top|bottom|left|right))?\s*:\s*(?:\d+px|thin)|BorderThickness=\"[1-9]|\.border\(|BorderStroke\(|class(?:Name)?=\"[^\"]*\bborder(?:-[a-z0-9]+)?\b|\bdivide-", re.I)
WEIGHT_RE = re.compile(r"font-weight\s*:\s*(\d{3})|FontWeight\.(\w+)|FontWeight=\"(\w+)\"|\.fontWeight\(\.(\w+)\)|weight=\"(\d{3})", re.I)
TYPE_SCALE_RE = re.compile(r"--(?:font-size|text|fs)-[a-z0-9]+\s*:|fontSize\s*=\s*\d+|\.font\(\.(?:largeTitle|title|headline|body|caption)|Typography\s*\(|TextStyle\(", re.I)
MONO_RE = re.compile(r"font-family\s*:[^;]*(?:mono|Consolas|Menlo|JetBrains|Fira Code)|font-mono|FontFamily\.Monospace|\.monospaced", re.I)
TABULAR_RE = re.compile(r"tabular-nums|font-variant-numeric|tnum|NumeralAlignment\s*=\s*\"?Tabular|FontFeatureSettings|monospacedDigit", re.I)
FONT_FAMILY_HINTS = {"geometric-sans": ["geist", "inter", "poppins", "montserrat", "futura", "manrope", "plus jakarta", "outfit", "urbanist", "sora", "dm sans"],
                     "humanist-sans": ["source sans", "open sans", "lato", "noto sans", "segoe", "san francisco", "sf pro", "roboto", "nunito", "ibm plex sans", "work sans"],
                     "grotesk": ["space grotesk", "helvetica", "arial", "neue", "grotesk", "archivo", "public sans"], "serif": ["georgia", "playfair", "merriweather", "lora", "serif", "times", "garamond", "fraunces"],
                     "monospace": ["mono", "consolas", "menlo", "fira code", "jetbrains"], "rounded": ["nunito", "quicksand", "varela round", "comfortaa"],
                     "condensed": ["condensed", "oswald", "barlow condensed", "roboto condensed"], "system": ["system-ui", "-apple-system", "segoe ui", "ui-sans-serif", "san francisco", "roboto"]}
FONT_FAMILY_HINTS["rounded"] = FONT_FAMILY_HINTS["rounded"] + ["rounded system"]
FONT_FAMILY_HINTS["humanist-sans"] = FONT_FAMILY_HINTS["humanist-sans"] + ["source sans", "segoe"]
DARK_THEME_CFG = [r"darkMode\s*:", r"\.dark\b", r"\[data-theme=\"?dark", r"prefers-color-scheme:\s*dark", r"darkColorScheme", r"isSystemInDarkTheme", r"preferredColorScheme\(\.dark\)",
                  r"RequestedTheme=\"Dark\"", r"ThemeDictionaries", r"Theme\.Dark", r"ThemeMode\.dark", r"Brightness\.dark", r"ColorScheme\.dark", r"Colors\.Dark", r"darkTheme\s*[:=]"]
LIGHT_THEME_CFG = [r"lightColorScheme", r"preferredColorScheme\(\.light\)", r"RequestedTheme=\"Light\"", r"Theme\.Light", r"ThemeMode\.light", r"Brightness\.light", r"Colors\.Light"]


def _luminance(hex6: str) -> float:
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


class _ContextCollector:
    def __init__(self):
        self.nav = Counter(); self.nav_files = defaultdict(set); self.nav_shell = Counter()
        self.dark_cfg = Counter(); self.light_cfg = Counter(); self.root_bg = []; self.dark_hex = 0; self.light_hex = 0
        self.radius = Counter(); self.spacing = Counter(); self.shadow = 0; self.border = 0; self.surface_files = 0
        self.weights = Counter(); self.type_scale = 0; self.mono = 0; self.tabular = 0
        self.dark_only_frameworks = 0; self.tailwind_spacing = 0; self.extra_fonts = Counter()

    def feed(self, path: Path, txt: str, ext: str):
        name = path.stem.lower()
        shell = any(h in name for h in SHELL_HINT_FILES) or bool(re.search(r"<aside\b|<nav\b|NavigationView|Scaffold\(|NavigationStack|NavigationSplitView", txt))
        for model, pats in NAV_SIGNALS.items():
            for pat in pats:
                n = len(re.findall(pat, txt))
                if n:
                    self.nav[model] += n; self.nav_files[model].add(path.name)
                    if shell:
                        self.nav_shell[model] += n
        for pat in DARK_THEME_CFG:
            if re.search(pat, txt):
                self.dark_cfg[pat] += 1
        for pat in LIGHT_THEME_CFG:
            if re.search(pat, txt):
                self.light_cfg[pat] += 1
        if ext in (".css", ".scss", ".less", ".xaml", ".axaml", ".kt", ".swift", ".dart", ".ts", ".tsx", ".js", ".jsx", ".json", ".svelte", ".vue", ".html", ".astro", ".razor", ".cshtml"):
            for m in ROOT_BG_RE.finditer(txt):
                val = m.group(1)
                hm = HEX_RE.search(val + " ") if val.startswith("#") else None
                if hm:
                    self.root_bg.append(_luminance(hm.group(1)))
                elif val.startswith("#") and len(val) == 4:
                    self.root_bg.append(_luminance("".join(c * 2 for c in val[1:])))
                elif val.lower().startswith("hsl"):
                    lm = re.search(r"(\d+(?:\.\d+)?)%\s*\)?\s*$", val.replace(" ", ""))
                    parts = re.findall(r"(\d+(?:\.\d+)?)%", val)
                    if len(parts) >= 2:
                        self.root_bg.append(float(parts[-1]) / 100)
            for hm in HEX_RE.finditer(txt):
                lum = _luminance(hm.group(1))
                if lum < 0.15: self.dark_hex += 1
                elif lum > 0.85: self.light_hex += 1
            for m in RADIUS_RE.finditer(txt):
                self.radius[float(m.group(1))] += 1
            for m in re.finditer(r"<CornerRadius[^>]*>\s*(\d+(?:\.\d+)?)\s*</CornerRadius>|CornerRadius=\"(\d+(?:\.\d+)?)\"", txt):
                self.radius[float(m.group(1) or m.group(2))] += 1
            for m in re.finditer(r"x:Key=\"(?:Space|Spacing|Gap|Pad|Inset)[A-Za-z0-9]*\"\s*>\s*(\d{1,3})\s*<", txt):
                v = int(m.group(1))
                if 2 <= v <= 96: self.spacing[v] += 1
            if re.search(r"<Thickness x:Key=\"[^\"]*Border[^\"]*\">\s*[1-9]|BorderThickness=\"\{StaticResource|BorderBrush=\"", txt):
                self.border += 1
            for m in SPACING_RE.finditer(txt):
                v = int(m.group(1))
                if 2 <= v <= 96: self.spacing[v] += 1
            for m in TW_SPACING_RE.finditer(txt):
                v = int(m.group(1)) * 4
                if 2 <= v <= 96: self.spacing[v] += 1; self.tailwind_spacing += 1
            for m in REM_SPACING_RE.finditer(txt):
                v = int(round(float(m.group(1)) * 16))
                if 2 <= v <= 96: self.spacing[v] += 1
            for m in re.finditer(r"FontFamily=\"([^\"{}]+,[^\"{}]+)\"", txt):
                self.extra_fonts[m.group(1).split(",")[0].strip()] += 1
            for m in XAML_FONT_RE.finditer(txt):
                fam = next((g for g in m.groups() if g), None)
                if fam:
                    if "geist" in m.group(0).lower() and not m.group(1):
                        fam = "Geist"
                    fam = re.sub(r"_(?:regular|semibold|bold|medium|light|italic|variable)\b", "", fam).replace("_", " ").strip()
                    self.extra_fonts[fam.title() if fam.islower() else fam] += 1
            if re.search(r"design:\s*\.rounded", txt):
                self.extra_fonts["Rounded system"] += 1
            if re.search(r"Font\.system\(|\.font\(\.system|\.font\(\.(?:largeTitle|title[23]?|headline|subheadline|body|callout|footnote|caption[2]?)\)|FontFamily=\"Segoe UI(?: Variable)?\"|Segoe UI Variable|MaterialTheme\.typography|Theme\.of\(context\)\.textTheme", txt):
                self.extra_fonts["System"] += 1
            for m in XAML_BRUSH_BG_RE.finditer(txt):
                self.root_bg.append(_luminance(m.group(1)))
            for m in COMPOSE_BG_RE.finditer(txt):
                self.root_bg.append(_luminance(m.group(1)))
            if re.search(r"\bBrightness\.light\b|\blightColorScheme\(", txt):
                self.light_cfg["native-light"] += 1
            if re.search(r"Property=\"BorderThickness\"\s+Value=\"[1-9]|BorderStroke\(|border\s*=\s*BorderStroke|\.border\(", txt):
                self.border += 1
            if re.search(r"tonalElevation\s*=\s*(?!0)\d|elevation:\s*(?!0)\d|\.shadow\(\s*(?:radius|color)", txt):
                self.shadow += 1
            if SHADOW_RE.search(txt): self.shadow += 1
            if BORDER_RE.search(txt): self.border += 1
            self.surface_files += 1
            for m in WEIGHT_RE.finditer(txt):
                w = next((g for g in m.groups() if g), None)
                if w: self.weights[w.lower()] += 1
            if TYPE_SCALE_RE.search(txt): self.type_scale += 1
            if MONO_RE.search(txt): self.mono += 1
            if TABULAR_RE.search(txt): self.tabular += 1

    def result(self, fonts: Counter, platforms: list, libs: list) -> dict:
        out = {}
        fonts = fonts + self.extra_fonts
        # navigation
        if "tv" not in platforms:
            self.nav.pop("tv-rails", None)
        if self.nav:
            score = {m: (self.nav_shell[m] * 3 + self.nav[m]) * NAV_WEIGHT.get(m, 1.0) for m in self.nav}
            best = sorted(self.nav, key=lambda m: (-score[m], NAV_PRIORITY.index(m)))
            top = best[0]
            strong = self.nav_shell[top] >= 1 or len(self.nav_files[top]) >= 2
            second = best[1] if len(best) > 1 else None
            ev = [f"{top}: {self.nav[top]} matches in {', '.join(sorted(self.nav_files[top])[:3])}" + (" (shell/layout file)" if self.nav_shell[top] else "")]
            if second and self.nav[second] >= self.nav[top] * 0.6:
                ev.append(f"also {second}: {self.nav[second]} matches")
            out["navigation"] = {"value": top, "status": "KNOWN" if strong and not (second and score[second] >= score[top] * 0.8 and not self.nav_shell[top]) else "INFERRED", "evidence": ev,
                                 "candidates": {m: self.nav[m] for m in best[:4]}}
        else:
            out["navigation"] = {"value": "unknown", "status": "UNKNOWN", "evidence": ["no navigation component/shell signal found"]}
        # theme polarity: require configuration or several signals
        dark_cfg = sum(self.dark_cfg.values()); light_cfg = sum(self.light_cfg.values())
        dark_root = sum(1 for l in self.root_bg if l < 0.25); light_root = sum(1 for l in self.root_bg if l > 0.75)
        ev = []
        if dark_cfg: ev.append(f"dark theme configuration signals: {dark_cfg}")
        if light_cfg: ev.append(f"light theme configuration signals: {light_cfg}")
        if self.root_bg: ev.append(f"root/canvas backgrounds: {light_root} light, {dark_root} dark")
        ev.append(f"hex palette: {self.light_hex} near-white, {self.dark_hex} near-black")
        if dark_cfg and light_cfg or (dark_cfg and light_root >= 1) or (dark_root >= 1 and light_root >= 1 and dark_cfg):
            default = "light" if light_root >= dark_root else "dark"
            out["theme"] = {"value": "dual-theme", "default": default, "status": "KNOWN" if (dark_cfg and (light_root or light_cfg)) else "INFERRED", "evidence": ev + [f"default polarity {default} (root canvas)"]}
        elif dark_root >= 1 and not light_root and (dark_cfg or self.dark_hex > self.light_hex * 1.5):
            out["theme"] = {"value": "dark-first", "status": "KNOWN" if dark_cfg else "INFERRED", "evidence": ev}
        elif "tv" in platforms and self.dark_hex > self.light_hex and dark_root == 0 and light_root == 0:
            out["theme"] = {"value": "dark-first", "status": "INFERRED", "evidence": ev + ["TV platform with a dark-leaning palette"]}
        elif light_root >= 1 and not dark_root and not dark_cfg:
            out["theme"] = {"value": "light-first", "status": "KNOWN" if light_root >= 2 or light_cfg else "INFERRED", "evidence": ev}
        elif light_cfg and not dark_cfg:
            out["theme"] = {"value": "light-first", "status": "INFERRED", "evidence": ev + ["light theme configuration only"]}
        elif dark_cfg and not self.root_bg:
            out["theme"] = {"value": "dual-theme", "status": "INFERRED", "evidence": ev}
        elif self.light_hex >= 3 and self.light_hex > self.dark_hex * 2 and not dark_cfg:
            out["theme"] = {"value": "light-first", "status": "INFERRED", "evidence": ev}
        else:
            out["theme"] = {"value": "unknown", "status": "UNKNOWN", "evidence": ev}
        # surfaces / radius / spacing
        if self.surface_files:
            if self.shadow >= 2 and self.shadow >= self.border:
                sv, ev = "elevated", [f"shadow/elevation in {self.shadow} files, borders in {self.border}"]
            elif self.border >= 2:
                sv, ev = "bordered-flat", [f"borders in {self.border} files, shadow/elevation in {self.shadow}"]
            elif self.shadow or self.border:
                sv, ev = ("elevated" if self.shadow else "bordered-flat"), [f"weak signal: shadow {self.shadow}, border {self.border}"]
            else:
                sv, ev = "flat-tonal", ["no shadow or border declarations found"]
            out["surfaces"] = {"value": sv, "status": "INFERRED" if (self.shadow + self.border) >= 2 else "UNKNOWN" if not (self.shadow or self.border) else "INFERRED", "evidence": ev}
        else:
            out["surfaces"] = {"value": "unknown", "status": "UNKNOWN", "evidence": []}
        if self.radius:
            common = sorted(self.radius.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
            med = common[0][0]
            label = "none" if med == 0 else "small" if med <= 6 else "medium" if med <= 12 else "large" if med <= 24 else "pill"
            out["radius"] = {"value": label, "status": "INFERRED", "evidence": [f"most common radius {med:g} ({common[0][1]}×); others {[c[0] for c in common[1:]]}"]}
        else:
            out["radius"] = {"value": "unknown", "status": "UNKNOWN", "evidence": []}
        if self.spacing:
            vals = [v for v, n in self.spacing.items() for _ in range(min(n, 50))]
            base = 8 if sum(1 for v in vals if v % 8 == 0) >= 0.6 * len(vals) else 4 if sum(1 for v in vals if v % 4 == 0) >= 0.6 * len(vals) else None
            top = sorted(self.spacing.items(), key=lambda kv: -kv[1])[:5]
            ev2 = [f"most used spacing values {[t[0] for t in top]}"] + ([f"tailwind spacing classes ({self.tailwind_spacing})"] if self.tailwind_spacing else [])
            out["spacing"] = {"value": base or "irregular", "status": "INFERRED" if base else "UNKNOWN", "evidence": ev2}
        else:
            out["spacing"] = {"value": "unknown", "status": "UNKNOWN", "evidence": []}
        # typography
        fam = None
        if fonts:
            ranked = fonts.most_common()
            non_mono = [(f, n) for f, n in ranked if not any(h in f.lower() for h in FONT_FAMILY_HINTS["monospace"])]
            top_name, top_n = (non_mono or ranked)[0]
            top_font = top_name.lower().split(",")[0].strip()
            for label, hints in FONT_FAMILY_HINTS.items():
                if label == "monospace" and non_mono:
                    continue
                if any(h in top_font for h in hints):
                    fam = label; break
            fam = fam or "custom"
            ev = [f"font family {top_name} ({top_n} refs)"] + ([f"monospace face {ranked[0][0]} used for a code/number role"] if non_mono and ranked[0][0] != top_name else [])
            if self.weights: ev.append("weights " + ", ".join(w for w, _ in self.weights.most_common(4)))
            if self.type_scale: ev.append(f"encoded type scale in {self.type_scale} files")
            if self.mono: ev.append("monospace usage")
            if self.tabular: ev.append("tabular numerals")
            out["typography"] = {"value": fam, "status": "KNOWN" if fonts.most_common(1)[0][1] >= 2 else "INFERRED", "evidence": ev,
                                 "features": {"weights": [w for w, _ in self.weights.most_common(4)], "type_scale": bool(self.type_scale), "monospace": bool(self.mono), "tabular_numerals": bool(self.tabular)}}
        else:
            out["typography"] = {"value": "unknown", "status": "UNKNOWN", "evidence": ["no font family declaration found"],
                                 "features": {"weights": [w for w, _ in self.weights.most_common(4)], "type_scale": bool(self.type_scale), "monospace": bool(self.mono), "tabular_numerals": bool(self.tabular)}}
        ui_libs = [l for l in libs if l and not l.startswith(("icons:", "i18n:", "test:", "a11y:", "charts:"))]
        out["components"] = {"value": ", ".join(dict.fromkeys(ui_libs)) or "unknown", "status": "KNOWN" if ui_libs else "UNKNOWN", "evidence": ui_libs[:5]}
        return out


def inspect(root: Path, max_files: int) -> dict:
    res = {"root": str(root), "findings": [], "stack_groups": [], "platforms": [], "ui_libraries": [],
           "package_manager": None, "css_architecture": [], "tokens": [], "fonts": [], "icons": [],
           "routing": [], "breakpoints": [], "accessibility": [], "focus_handling": [], "design_docs": [],
           "component_dirs": [], "tests": [], "i18n": [], "product_hints": [], "environment_hints": [], "sample": {"files_scanned": 0}}
    known = lambda msg: res["findings"].append({"status": "KNOWN", "note": msg})
    inferred = lambda msg: res["findings"].append({"status": "INFERRED", "note": msg})
    stacks, plats, libs = [], [], []

    # --- manifests -------------------------------------------------------------
    for pj in [root / "package.json"] + sorted(root.glob("apps/*/package.json"))[:6] + sorted(root.glob("packages/*/package.json"))[:6]:
        if not pj.exists():
            continue
        try:
            data = json.loads(read_text(pj) or "{}")
        except json.JSONDecodeError:
            res["findings"].append({"status": "KNOWN", "note": f"{pj.relative_to(root)} is not valid JSON"})
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        for dep, (grp, pl, lib) in DEP_MAP.items():
            if dep in deps:
                stacks.append(grp); plats += pl
                if lib:
                    libs.append(lib)
                known(f"{pj.relative_to(root)}: {dep}@{deps[dep]}")
        if "workspaces" in data:
            inferred("monorepo (package.json workspaces)")
    for lock, pm in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"), ("bun.lock", "bun"), ("package-lock.json", "npm")):
        if (root / lock).exists():
            res["package_manager"] = pm
            break
    for g in list(root.glob("*.gradle*")) + list(root.glob("app/*.gradle*")) + list(root.glob("**/libs.versions.toml"))[:2]:
        txt = read_text(g)
        for key, (grp, pl, lib) in GRADLE_MAP.items():
            if key in txt:
                stacks.append(grp); plats += pl; libs.append(lib)
                known(f"{g.relative_to(root)}: {key}")
    tv_manifest, phone_manifest, tv_web = False, False, False
    for cfg in list(root.glob("config.xml"))[:1] + list(root.glob("*/config.xml"))[:2]:
        txt = read_text(cfg)
        if "tizen" in txt.lower():
            tv_manifest = True; tv_web = True; plats.append("tv"); known(f"{cfg.relative_to(root)}: Tizen widget config (Samsung TV web app)")
    for ai in list(root.glob("appinfo.json"))[:1] + list(root.glob("*/appinfo.json"))[:2]:
        txt = read_text(ai).lower()
        if '"type"' in txt and ("webos" in txt or '"web"' in txt) and ("vendor" in txt or "largeicon" in txt or "iconcolor" in txt):
            tv_manifest = True; tv_web = True; plats.append("tv"); known(f"{ai.relative_to(root)}: webOS appinfo (LG TV web app)")
    for m in list(root.glob("**/AndroidManifest.xml"))[:4]:
        txt = read_text(m)
        if "LEANBACK_LAUNCHER" in txt or "android.software.leanback" in txt:
            tv_manifest = True
            plats.append("tv"); known(f"{m.relative_to(root)}: leanback launcher (Android TV)")
        elif "android.intent.category.LAUNCHER" in txt:
            phone_manifest = True
        if 'android.hardware.touchscreen" android:required="false"' in txt:
            inferred("touchscreen not required in manifest (TV/set-top)")
    for cs in list(root.glob("*.csproj")) + list(root.glob("*/*.csproj"))[:8]:
        txt = read_text(cs)
        for key, (grp, pl, lib) in DOTNET_MAP.items():
            if key in txt:
                stacks.append(grp); plats += pl; libs.append(lib)
                known(f"{cs.relative_to(root)}: {key}")
        if "<TargetFramework" in txt and "windows" in txt.lower():
            plats.append("desktop")
    if (root / "pubspec.yaml").exists():
        txt = read_text(root / "pubspec.yaml")
        stacks.append("flutter"); plats.append("mobile"); known("pubspec.yaml: Flutter")
        for pkg in ("go_router", "flutter_bloc", "riverpod", "provider", "dpad_navigation", "flutter_tv"):
            if pkg in txt:
                libs.append(pkg)
    for x in list(root.glob("*.xcodeproj")) + list(root.glob("Package.swift")):
        txt = read_text(x / "project.pbxproj") if x.is_dir() else read_text(x)
        stacks.append("swiftui"); known(f"{x.name}: Apple project")
        low = txt.lower()
        apple_targets = []
        if "appletvos" in low or "tvos" in low:
            apple_targets.append("tv"); known(f"{x.name}: tvOS target")
        if "iphoneos" in low or ".ios(" in low or "iphoneos_deployment_target" in low:
            apple_targets.append("mobile"); known(f"{x.name}: iOS target")
        if "sdkroot = macosx" in low or ".macos(" in low:
            apple_targets.append("desktop"); known(f"{x.name}: macOS target")
        if not apple_targets:
            apple_targets.append("mobile"); inferred(f"{x.name}: no platform target found; assuming iOS")
        plats += apple_targets
    if (root / "tailwind.config.js").exists() or (root / "tailwind.config.ts").exists() or (root / "tailwind.config.cjs").exists():
        res["css_architecture"].append("tailwind-config")
        cfg = "".join(read_text(p) for p in root.glob("tailwind.config.*"))
        m = re.search(r"screens\s*:\s*{([^}]*)}", cfg)
        if m:
            res["breakpoints"] += re.findall(r"['\"]?([a-z0-9]+)['\"]?\s*:\s*['\"](\d+px)['\"]", m.group(1))
        if "extend" in cfg and "colors" in cfg:
            res["tokens"].append("tailwind.config theme.extend.colors")
    if (root / "components.json").exists():
        stacks.append("shadcn"); libs.append("shadcn"); known("components.json: shadcn/ui")
        try:
            cj = json.loads(read_text(root / "components.json") or "{}")
            res["tokens"].append(f"shadcn cssVariables={cj.get('tailwind', {}).get('cssVariables')} baseColor={cj.get('tailwind', {}).get('baseColor')}")
        except json.JSONDecodeError:
            pass

    # plain HTML/CSS site with no framework manifest
    if not stacks and (any(root.glob("*.html")) or any(root.glob("*/*.html"))):
        stacks.append("html-css"); plats.append("web")
        known("*.html without a framework manifest: plain HTML/CSS site")
        if any(root.rglob("*.css")):
            res["css_architecture"].append("plain stylesheets")

    # --- routing / structure ---------------------------------------------------
    for rel, label in (("app", "next-app-router or nuxt app dir"), ("pages", "pages router"), ("src/app", "next app router"),
                       ("src/pages", "pages router"), ("src/routes", "sveltekit/solid routes"), ("src/router", "vue-router"),
                       ("Views", "views"), ("Pages", "xaml pages"), ("ViewModels", "mvvm viewmodels"), ("features", "feature modules")):
        if (root / rel).is_dir():
            if rel in ("app", "src/app") and not (any((root / rel).glob("**/page.*")) or any((root / rel).glob("**/layout.*")) or any((root / rel).glob("**/*.vue"))):
                continue  # an Android/Gradle "app" module is not a web app-router
            res["routing"].append(f"{rel}/ ({label})")
    for rel in ("components", "src/components", "src/ui", "ui", "src/lib/components", "app/components", "src/shared/ui",
                "components/ui", "src/components/ui", "designsystem", "design-system", "src/design-system", "packages/ui",
                "Controls", "Styles", "Themes", "lib/widgets", "lib/ui"):
        if (root / rel).is_dir():
            try:
                n = sum(1 for _ in (root / rel).rglob("*") if _.is_file())
            except OSError:
                n = 0
            res["component_dirs"].append(f"{rel}/ ({n} files)")
    for rel in ("DESIGN.md", "design-system", "docs/design", "DESIGN_SYSTEM.md", "STYLEGUIDE.md", "design-tokens.json",
                "tokens.json", "tokens", "src/tokens", "src/styles/tokens.css", "theme.ts", "src/theme", "src/theme.ts",
                "Themes/Generic.xaml", "App.xaml", "styles.xml", "res/values/themes.xml", ".storybook"):
        if (root / rel).exists():
            (res["design_docs"] if rel.endswith(".md") or rel in ("design-system", "docs/design", ".storybook") else res["tokens"]).append(rel)

    # --- bounded content sample -----------------------------------------------
    css_vars, fonts, media, focus_hits, a11y_hits, dpad_hits, files = Counter(), Counter(), Counter(), 0, 0, 0, 0
    css_kinds = Counter()
    ctx = _ContextCollector()
    for p in walk(root, max_files):
        files += 1
        txt = read_text(p)
        if not txt:
            continue
        ext = p.suffix.lower()
        if ext in (".css", ".scss", ".sass", ".less"):
            css_kinds[ext] += 1
            if ".module." in p.name:
                css_kinds["css-modules"] += 1
            for v in CSS_VAR_RE.findall(txt):
                css_vars[v.split("-")[0]] += 1
            for size, unit in MEDIA_RE.findall(txt):
                media[f"{size}{unit}"] += 1
        ctx.feed(p, txt, ext)
        if ext in (".tsx", ".jsx", ".vue", ".svelte", ".astro", ".html", ".kt", ".swift", ".dart", ".xaml", ".axaml", ".cs", ".css", ".ts", ".js", ".xml", ".kts"):
            for m in FONT_RE.finditer(txt):
                fam = next((g for g in m.groups() if g), None)
                if fam:
                    fam = fam.replace("+", " ").split(":")[0].strip()
                    if fam.lower() not in ("inherit", "sans-serif", "serif", "monospace", "system-ui", "var", "ui-sans-serif"):
                        fonts[fam] += 1
            if FOCUS_RE.search(txt):
                focus_hits += 1
            if A11Y_RE.search(txt):
                a11y_hits += 1
            if DPAD_RE.search(txt):
                dpad_hits += 1
            if "styled." in txt or "styled(" in txt:
                css_kinds["css-in-js"] += 1
            if 'className="' in txt and re.search(r'className="[^"]*\b(flex|grid|px-|text-)', txt):
                css_kinds["tailwind-classes"] += 1
    res["sample"]["files_scanned"] = files
    res["css_architecture"] += [f"{k} ({n} files)" for k, n in css_kinds.most_common(6)]
    if css_vars:
        res["tokens"].append("css custom properties: " + ", ".join(f"--{k}* ({n})" for k, n in css_vars.most_common(8)))
    res["fonts"] = [f"{k} ({n})" for k, n in fonts.most_common(8)]
    res["breakpoints"] += [f"{k} ({n} rules)" for k, n in media.most_common(8)]
    if a11y_hits:
        res["accessibility"].append(f"a11y attributes present in {a11y_hits} files")
    res["focus_handling"].append(f"explicit focus handling in {focus_hits} files")
    if dpad_hits:
        res["focus_handling"].append(f"DPAD/remote/TV-focus handling in {dpad_hits} files")
        plats.append("tv")
        inferred("DPAD / remote key handling found in source")
    for lib in libs:
        if lib.startswith("icons:"):
            res["icons"].append(lib[6:])
        elif lib.startswith("i18n:"):
            res["i18n"].append(lib[5:])
        elif lib.startswith("test:"):
            res["tests"].append(lib[5:])
        elif lib.startswith("a11y:"):
            res["accessibility"].append(lib[5:])
        else:
            res["ui_libraries"].append(lib)

    # dedupe preserving order
    def uniq(seq):
        seen, out = set(), []
        for x in seq:
            if x not in seen and x != "any":
                seen.add(x); out.append(x)
        return out
    if tv_manifest and not phone_manifest and "mobile" in plats and "compose" in stacks:
        plats = [p_ for p_ in plats if p_ != "mobile"]
        inferred("Compose dependencies imply mobile but the only launcher is leanback: TV-only app")
    res["stack_groups"] = uniq(stacks)
    if tv_web:
        plats = [p for p in plats if p != "web"]   # a Tizen / webOS package is a TV app on a web substrate
    res["platforms"] = uniq(plats)
    res["design_context"] = ctx.result(fonts, res["platforms"], libs)
    res["design_context"]["schema"] = "design-context/v1"
    res["ui_libraries"] = uniq(res["ui_libraries"])
    if "tv" in res["platforms"] and "mobile" in res["platforms"] and "compose-tv" in res["stack_groups"]:
        inferred("both mobile and TV Android targets; check product flavors before assuming one UI")
    if not res["stack_groups"]:
        inferred("no recognised UI stack; treat stack as MISSING and ask or inspect further")
    # product hints from README title/description (cheap, INFERRED)
    readme = next((p for p in (root / "README.md", root / "readme.md") if p.exists()), None)
    if readme:
        full = read_text(readme)
        head = full[:900].lower()
        for pat, fam in ((r"\berp\b", "erp"), (r"\binvoic(?:e|es|ing)\b", "finance"), (r"\bbank(?:ing)?\b", "finance"), (r"\btrading\b", "finance"),
                         (r"\biptv\b", "media"), (r"\bstreaming\b", "media"), (r"\bvideo player\b|\bmedia player\b", "media"),
                         (r"\b(?:web ?shop|online shop|online store|storefront|e-?commerce|shopping cart|checkout)\b", "ecommerce"),
                         (r"\bpatients?\b", "healthcare"), (r"\bclinic\b", "healthcare"), (r"\bpharmacy\b", "healthcare"), (r"\bprescriptions?\b", "healthcare"),
                         (r"\bsaas\b", "saas"), (r"\bcourses?\b", "education"), (r"\bstudents?\b", "education"),
                         (r"\butility\b", "iot"), (r"\benergy\b", "iot"), (r"\bfield service\b|\bfield team\b|\bfield crew\b", "iot"), (r"\btechnicians?\b", "iot")):
            if re.search(pat, head) and fam not in res["product_hints"]:
                res["product_hints"].append(fam)
        env_head = full[:2500].lower()
        for pat, env in ((r"\boutdoors?\b|\bsunlight\b|\bglare\b", "outdoor"), (r"\bgloves?\b", "gloves"),
                         (r"\bpublic (?:touch|use|terminal|kiosk)\b|\bshared device\b|\bwalk-up\b", "public"), (r"\blow[- ]bandwidth\b|\boffline[- ]first\b", "low-bandwidth")):
            if re.search(pat, env_head) and env not in res["environment_hints"]:
                res["environment_hints"].append(env)
        if re.search(r"\bkiosks?\b|\btouch terminal\b|\bself-service terminal\b", head) and "kiosk" not in res["platforms"]:
            res["platforms"] = ["kiosk"] + [p for p in res["platforms"] if p != "web"]
            res["findings"].append({"status": "KNOWN", "note": "README: public touch kiosk (web technology is the substrate, not the target platform)"})
            if "public" not in res["environment_hints"]:
                res["environment_hints"].append("public")
    return res


def summary(res: dict) -> str:
    L = [f"# Project inspection: {res['root']}", ""]
    L.append(f"- stacks: {', '.join(res['stack_groups']) or 'none detected (MISSING)'}")
    L.append(f"- platforms: {', '.join(res['platforms']) or 'none detected (MISSING)'}")
    dc = res.get("design_context", {})
    L.append("- design context: " + "; ".join(f"{k}={v['value']} ({v['status']})" for k, v in dc.items() if isinstance(v, dict)))
    L.append(f"- package manager: {res['package_manager'] or 'n/a'}")
    for key in ("ui_libraries", "css_architecture", "tokens", "fonts", "icons", "routing", "component_dirs",
                "breakpoints", "accessibility", "focus_handling", "i18n", "tests", "design_docs", "product_hints", "environment_hints"):
        if res[key]:
            L.append(f"- {key.replace('_', ' ')}: {', '.join(map(str, res[key]))}")
    L.append(f"- files scanned: {res['sample']['files_scanned']}")
    L.append("")
    L.append("Findings:")
    for f in res["findings"][:30]:
        L.append(f"- [{f['status']}] {f['note']}")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="also write JSON here (feed to advise.py --project)")
    ap.add_argument("--max-files", type=int, default=4000)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"error: {root} is not a directory")
    res = inspect(root, args.max_files)
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(json.dumps(res, indent=2) if args.json else summary(res))


if __name__ == "__main__":
    main()
