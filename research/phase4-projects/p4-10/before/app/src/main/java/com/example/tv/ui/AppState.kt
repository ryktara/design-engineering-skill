package com.example.tv.ui

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.focus.FocusRequester
import com.example.tv.data.HomeContent
import com.example.tv.data.SportsEvent

/** Screen-level states, enumerated before any pixel is drawn (anti-no-states guardrail). */
sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Error(val message: String) : HomeUiState
    data object Empty : HomeUiState                 // provider returned no events (off-season / region block)
    data class Ready(val content: HomeContent) : HomeUiState
}

/** Mini player: shown while the household keeps a game running while browsing. */
sealed interface MiniPlayerState {
    data object Hidden : MiniPlayerState
    data class Playing(val event: SportsEvent) : MiniPlayerState
    data class Paused(val event: SportsEvent) : MiniPlayerState
    data class Buffering(val event: SportsEvent) : MiniPlayerState
}

sealed interface Route {
    data object Home : Route
    data class Details(val event: SportsEvent) : Route
    data class Player(val event: SportsEvent) : Route
    data object Guide : Route
}

/** Sections of the collapsible side navigation (nav-tv-side). */
enum class NavSection(val label: String) { HOME("Home"), LIVE("Live"), GUIDE("Guide"), CATCH_UP("Catch up"), SEARCH("Search"), SETTINGS("Settings") }

/** Focus targets on the home screen that are not rail items. */
object HomeFocusKeys {
    const val HERO_PRIMARY = "hero:primary"
    const val HERO_SECONDARY = "hero:secondary"
    const val MINI_PLAYER = "mini-player"
    const val EPG_TILE = "epg:tile"
    fun item(railId: String, eventId: String) = "rail:$railId:$eventId"
}

/**
 * Focus memory that outlives the Home composition (it is remembered at the app level, not inside HomeScreen),
 * so returning from Details/Player restores the exact tile. Each rail additionally uses Modifier.focusRestorer()
 * for LEFT/RIGHT re-entry within the same composition.
 */
class HomeFocusMemory {
    var lastFocusedKey by mutableStateOf(HomeFocusKeys.HERO_PRIMARY)
    /** Rail id + item index of the last focused tile; null when the last focus was a hero control. */
    var lastFocusedRail: String? = null
    var lastFocusedIndex: Int = 0
    var pendingRestore by mutableStateOf(false)   // set when navigating away; consumed once Home re-composes
    var scrollToTopRequested by mutableStateOf(false)
    val requesters = HashMap<String, FocusRequester>()
    /** One LazyListState per rail so horizontal positions survive the Home composable leaving composition. */
    val railStates = HashMap<String, LazyListState>()
    fun requesterFor(key: String): FocusRequester = requesters.getOrPut(key) { FocusRequester() }
    fun railState(railId: String): LazyListState = railStates.getOrPut(railId) { LazyListState() }
    fun rememberTile(railId: String, index: Int, key: String) { lastFocusedRail = railId; lastFocusedIndex = index; lastFocusedKey = key }
    fun rememberHeroControl(key: String) { lastFocusedRail = null; lastFocusedKey = key }
}

@Immutable
data class AppSnapshot(val route: Route, val home: HomeUiState, val mini: MiniPlayerState, val section: NavSection)
