package com.example.tv.ui

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateMapOf
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
    /** [startAtMin] null = live edge / from the start; a value = resume from a saved position. */
    data class Player(val event: SportsEvent, val startAtMin: Int? = null) : Route
    data object Guide : Route
}

/**
 * Viewer library shared by the home cards and the details screen (media-resume-and-details): the watchlist
 * toggle must be reflected immediately wherever the event is shown, and the saved playback position decides
 * whether details offers Play or Resume + Start over. App-level so it survives route switches; a real app backs
 * it with the account service.
 */
class LibraryState {
    val watchlist = mutableStateListOf<String>()            // event ids, insertion order
    val positions = mutableStateMapOf<String, Int>()        // event id → minutes watched
    fun isSaved(id: String): Boolean = id in watchlist
    /** Returns the new state. */
    fun toggleWatchlist(id: String): Boolean { if (id in watchlist) watchlist.remove(id) else watchlist.add(id); return id in watchlist }
    /** Minutes into the broadcast to resume from, or null when nothing meaningful was watched / it was finished. */
    fun resumePoint(event: SportsEvent): Int? = positions[event.id]?.takeIf { it in 2 until event.durationMin - 1 }
    fun savePosition(event: SportsEvent, minutes: Int) { positions[event.id] = minutes.coerceIn(0, event.durationMin) }
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
 *
 * Everything the viewer perceives as "their place" lives here, not in HomeScreen: the focused tile (by rail +
 * event id + index), the vertical scroll of the rail column, the horizontal scroll of every rail, and the hero
 * event the backdrop was showing. HomeScreen's own `remember`s are dropped when the route switches to
 * Details/Player, which is exactly when the place must survive.
 */
class HomeFocusMemory {
    var lastFocusedKey by mutableStateOf(HomeFocusKeys.HERO_PRIMARY)
    /** Rail id + item index of the last focused tile; null when the last focus was a hero control. */
    var lastFocusedRail: String? = null
    var lastFocusedIndex: Int = 0
    /** Event id of the last focused tile (null for the EPG tile / hero controls); rails are time-based, so the
     *  id is matched first and the index is only a fallback when the event has left the rail. */
    var lastFocusedEventId: String? = null
    /** Hero/backdrop event at the moment Home was left; restored as-is so the backdrop does not jump back to
     *  the first live event and then crossfade to the remembered tile 300 ms later. */
    var heroEvent: SportsEvent? = null
    var pendingRestore by mutableStateOf(false)   // set when navigating away; consumed once Home re-composes
    var scrollToTopRequested by mutableStateOf(false)
    val requesters = HashMap<String, FocusRequester>()
    /** Vertical LazyColumn state of the rails, hoisted so the column does not reset to the top (and does not
     *  need to be re-scrolled to a rail, hiding the hero) when Home re-enters composition. */
    val columnState = LazyListState()
    /** One LazyListState per rail so horizontal positions survive the Home composable leaving composition. */
    val railStates = HashMap<String, LazyListState>()
    fun requesterFor(key: String): FocusRequester = requesters.getOrPut(key) { FocusRequester() }
    fun railState(railId: String): LazyListState = railStates.getOrPut(railId) { LazyListState() }
    fun rememberTile(railId: String, index: Int, key: String, eventId: String? = null) {
        lastFocusedRail = railId; lastFocusedIndex = index; lastFocusedKey = key; lastFocusedEventId = eventId
    }
    fun rememberHeroControl(key: String) { lastFocusedRail = null; lastFocusedKey = key; lastFocusedEventId = null }

    /**
     * Where focus should land when Home comes back (a11y-tv-focus-always: "move focus to a sensible neighbour
     * when the focused item is removed"). Pure so it can be unit-tested without Compose.
     *
     * 1. the same event in the same rail (it may have moved: a rail is re-sorted as matches start and end);
     * 2. the tile now at the remembered index in the same rail, clamped to the rail's end (the match ended and
     *    left "Live now": the neighbour that took its slot is the sensible place, not the hero);
     * 3. the hero primary action (rail gone / empty).
     *
     * [railItems] lists the focus keys of a rail in lazy order (the EPG leading tile included when present).
     */
    fun resolveRestoreTarget(railItems: (String) -> List<Pair<String, String?>>?): RestoreTarget {
        val rail = lastFocusedRail ?: return RestoreTarget(lastFocusedKey, null, 0, exact = true)
        val items = railItems(rail)
        if (items.isNullOrEmpty()) return RestoreTarget(HomeFocusKeys.HERO_PRIMARY, null, 0, exact = false)
        val byId = lastFocusedEventId?.let { id -> items.indexOfFirst { it.second == id } } ?: -1
        if (byId >= 0) return RestoreTarget(items[byId].first, rail, byId, exact = true)
        val byKey = items.indexOfFirst { it.first == lastFocusedKey }
        if (byKey >= 0) return RestoreTarget(items[byKey].first, rail, byKey, exact = true)
        val clamped = lastFocusedIndex.coerceIn(0, items.lastIndex)
        return RestoreTarget(items[clamped].first, rail, clamped, exact = false)
    }
}

/** Result of [HomeFocusMemory.resolveRestoreTarget]; `exact` is false when a neighbour stood in for a removed tile. */
data class RestoreTarget(val key: String, val railId: String?, val index: Int, val exact: Boolean)

@Immutable
data class AppSnapshot(val route: Route, val home: HomeUiState, val mini: MiniPlayerState, val section: NavSection)
