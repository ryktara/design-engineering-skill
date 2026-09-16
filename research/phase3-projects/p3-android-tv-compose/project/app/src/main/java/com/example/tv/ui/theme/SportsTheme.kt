package com.example.tv.ui.theme

import android.provider.Settings
import androidx.compose.runtime.Composable
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Typography
import androidx.tv.material3.darkColorScheme

/*
 * Values mirror design/tokens.json (semantic roles, dark-first, validated with tokens.py --platform tv).
 * Keep hex here and in tokens.json in sync; UI code never uses raw hex.
 */
object SportsColors {
    val canvas = Color(0xFF0B1220)
    val surface = Color(0xFF131C2B)
    val elevated = Color(0xFF1B2738)
    val textPrimary = Color(0xFFEAF0F6)
    val textSecondary = Color(0xFF9FB0C3)
    val textDisabled = Color(0xFF6B7C90)
    val onAction = Color(0xFF0B1220)
    val accent = Color(0xFFFFC533)         // one accent: primary actions + progress
    val accentPressed = Color(0xFFE6B02E)
    val borderDefault = Color(0xFF263447)
    val borderStrong = Color(0xFF66799A)
    val focusRing = Color(0xFFFFFFFF)      // white ring survives any artwork; glow adds the accent
    val selectionBg = Color(0xFF24344A)
    val live = Color(0xFFE0203A)           // LIVE badge only; never used for large areas (bloom)
    val success = Color(0xFF3DDC84)
    val error = Color(0xFFFF5C5C)
    val info = Color(0xFF7CB7FF)
}

/** Design frame 960×540 dp; every number here is dp on that frame (1080p = 2×). */
object SportsDimens {
    val safeH: Dp = 48.dp      // ≥5% horizontal overscan margin
    val safeV: Dp = 27.dp      // ≥5% vertical overscan margin
    val gutter: Dp = 20.dp
    val railGap: Dp = 28.dp
    val contentStart: Dp = 20.dp  // content sits right of the collapsed drawer; the drawer itself carries the safe margin
    val heroHeight: Dp = 288.dp   // meta + 1-line title + score + 2-line synopsis + actions; first rail stays visible below
    val cardW: Dp = 268.dp     // 3-up landscape width at 960 dp (plus partial 4th to signal continuation)
    val cardH: Dp = 151.dp     // 16:9
    val epgTileW: Dp = 412.dp  // 2-up width: the EPG entry tile is deliberately wider than an event card
    val navCollapsed: Dp = 92.dp  // safeH (48) + 32 icon + paddings: the icon strip sits inside the overscan margin
    val navExpanded: Dp = 240.dp
    val focusScale = 1.08f
    val focusBorder: Dp = 3.dp
    val focusPadding: Dp = 12.dp // reserved so the 1.08 scale never clips neighbours
    val railScrollMs = 220        // one pivot step of a rail (tween); the twin's --dur-rail
    val railHoldStepMs = 280L     // held LEFT/RIGHT admits one card per step (~3.5 cards/s) so each title can be read;
                                  // must be ≥ railScrollMs so a step finishes before the next is admitted
    // Player (PlayerScreen.kt)
    val playerAutoHideMs = 4000L  // transport overlay hides after 4 s without input; never while the track sheet is open
    val playerSeekStepSec = 10    // LEFT/RIGHT on the progress bar
    val trackSheetW: Dp = 600.dp  // right-hand side sheet: two track columns of ~256 dp (24 sp "English (CC)" + check, and a
                                  // 20 sp "Audio description" detail, fit without ellipsis); the left 360 dp of the picture stays visible
    val trackRowH: Dp = 56.dp     // one track row (24 sp label + optional 20 sp detail)
}

/**
 * 10-foot type scale (tokens.py scale --platform tv --base 24 --ratio 1.25, caption raised to the 20 sp floor).
 * Condensed display face only for titles/scores; body stays in a normal-width sans with tabular figures.
 */
val DisplayCondensed: FontFamily = FontFamily.SansSerif  // swap for Barlow Condensed / Roboto Condensed via res/font
val BodySans: FontFamily = FontFamily.SansSerif

val SportsTypography = Typography(
    displayLarge = TextStyle(fontFamily = DisplayCondensed, fontWeight = FontWeight.Bold, fontSize = 74.sp, lineHeight = 82.sp),
    displayMedium = TextStyle(fontFamily = DisplayCondensed, fontWeight = FontWeight.Bold, fontSize = 56.sp, lineHeight = 62.sp),
    headlineLarge = TextStyle(fontFamily = DisplayCondensed, fontWeight = FontWeight.SemiBold, fontSize = 46.sp, lineHeight = 54.sp),
    headlineMedium = TextStyle(fontFamily = DisplayCondensed, fontWeight = FontWeight.SemiBold, fontSize = 38.sp, lineHeight = 46.sp),
    titleLarge = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.SemiBold, fontSize = 30.sp, lineHeight = 38.sp),
    titleMedium = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.SemiBold, fontSize = 28.sp, lineHeight = 36.sp), // rail titles ≥24 sp
    bodyLarge = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.Normal, fontSize = 30.sp, lineHeight = 42.sp),
    bodyMedium = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.Normal, fontSize = 24.sp, lineHeight = 34.sp),   // body floor
    labelLarge = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.Medium, fontSize = 24.sp, lineHeight = 30.sp),
    labelMedium = TextStyle(fontFamily = BodySans, fontWeight = FontWeight.Medium, fontSize = 20.sp, lineHeight = 28.sp),  // caption floor
)

/** True when the system animator scale is 0 (Settings > Accessibility > Remove animations). */
val LocalReducedMotion = compositionLocalOf { false }

@Composable
fun SportsTheme(content: @Composable () -> Unit) {
    val context = LocalContext.current
    val reducedMotion = remember {
        Settings.Global.getFloat(context.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f
    }
    CompositionLocalProvider(LocalReducedMotion provides reducedMotion) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = SportsColors.accent,
            onPrimary = SportsColors.onAction,
            background = SportsColors.canvas,
            onBackground = SportsColors.textPrimary,
            surface = SportsColors.surface,
            onSurface = SportsColors.textPrimary,
            surfaceVariant = SportsColors.elevated,
            onSurfaceVariant = SportsColors.textSecondary,
            outline = SportsColors.borderDefault,
            error = SportsColors.error,
            border = SportsColors.focusRing,
        ),
        typography = SportsTypography,
        content = content,
    )
    }
}
