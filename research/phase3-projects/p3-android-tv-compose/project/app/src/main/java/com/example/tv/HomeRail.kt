package com.example.tv

/*
 * Fixture entry point kept for compatibility. The real rails live in ui/home/HomeScreen.kt (RailRow):
 * LazyRow + Modifier.focusRestorer() + LocalBringIntoViewSpec pivot, driven by HomeFocusMemory so focus
 * survives navigation to Details/Player. TvLazyRow (androidx.tv.foundation) is deprecated and not used.
 */
@Deprecated("Use com.example.tv.ui.home.HomeScreen", level = DeprecationLevel.WARNING)
object HomeRail
