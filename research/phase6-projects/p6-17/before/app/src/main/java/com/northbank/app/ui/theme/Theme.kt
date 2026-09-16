package com.northbank.app.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val LightColors = lightColorScheme(
    primary = Green700,
    onPrimary = Color.White,
    primaryContainer = Green50,
    onPrimaryContainer = Green900,
    secondary = Gold500,
    onSecondary = Grey900,
    secondaryContainer = Gold200,
    onSecondaryContainer = Grey900,
    tertiary = Green500,
    onTertiary = Color.White,
    background = Grey100,
    onBackground = Grey900,
    surface = Color.White,
    onSurface = Grey900,
    surfaceVariant = Grey100,
    onSurfaceVariant = Grey700,
    outline = Grey300,
    outlineVariant = Grey200,
    error = Red600,
    onError = Color.White,
    errorContainer = Red200,
    onErrorContainer = Red600,
)

private val DarkColors = darkColorScheme(
    primary = Green200,
    onPrimary = Green900,
    primaryContainer = Green700,
    onPrimaryContainer = Green50,
    secondary = Gold200,
    onSecondary = Grey900,
    secondaryContainer = Gold500,
    onSecondaryContainer = Grey900,
    tertiary = Green200,
    onTertiary = Green900,
    background = Grey900,
    onBackground = Grey100,
    surface = Grey900,
    onSurface = Grey100,
    surfaceVariant = Grey850,
    onSurfaceVariant = Grey600,
    outline = Grey700,
    outlineVariant = Grey800,
    error = Red200,
    onError = Grey900,
    errorContainer = Red600,
    onErrorContainer = Red200,
)

@Composable
fun NorthBankTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    // Brand colour is part of the product; we never adopt Material You palettes.
    val colorScheme = if (darkTheme) DarkColors else LightColors

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            WindowCompat.getInsetsController(window, view).apply {
                isAppearanceLightStatusBars = !darkTheme
                isAppearanceLightNavigationBars = !darkTheme
            }
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = NorthBankTypography,
        shapes = NorthBankShapes,
        content = content,
    )
}
