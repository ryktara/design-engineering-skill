package com.example.tv.ui

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.focus.FocusRequester
import com.example.tv.data.EventStatus
import com.example.tv.data.HomeContent
import com.example.tv.data.MediaTrack
import com.example.tv.data.SportsEvent
import com.example.tv.data.TrackList
import com.example.tv.data.TrackSelection

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
 * Explicit back stack (tv-back-behavior + nav-orientation-and-back). Home is the root and is never popped, so
 * BACK on a pushed route (Details / Player / Guide) can only ever unwind one layer — it can never fall through
 * to the Activity default (finish) and throw the viewer out of the app. Exit is a decision taken at the root
 * only, by [atRoot] plus drawer focus, never by the absence of a BackHandler on a screen.
 */
class NavStack {
    private val stack = mutableStateListOf<Route>(Route.Home)
    val current: Route get() = stack.last()
    val atRoot: Boolean get() = stack.size == 1
    fun push(route: Route) { stack.add(route) }
    /** Re-target the topmost layer without deepening the stack (a related card on Details). */
    fun replaceTop(route: Route) { stack[stack.lastIndex] = route }
    /** Pops one layer; returns false at the root so the caller decides what BACK means there. */
    fun pop(): Boolean { if (stack.size <= 1) return false; stack.removeAt(stack.lastIndex); return true }
    /** Unwinds to the Home root in one step (the player hands the stream to the mini player and returns Home). */
    fun popToRoot() { while (stack.size > 1) stack.removeAt(stack.lastIndex) }
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
    /** Event ids in most-recently-watched order (index 0 = the last thing watched). Drives the order of the
     *  Continue watching rail, which is a history, not a catalogue section. */
    private val recent = mutableStateListOf<String>()
    fun isSaved(id: String): Boolean = id in watchlist
    /** Returns the new state. */
    fun toggleWatchlist(id: String): Boolean { if (id in watchlist) watchlist.remove(id) else watchlist.add(id); return id in watchlist }
    /** Minutes into the broadcast to resume from, or null when nothing meaningful was watched / it was finished. */
    fun resumePoint(event: SportsEvent): Int? = positions[event.id]?.takeIf { it in 2 until event.durationMin - 1 }
    fun savePosition(event: SportsEvent, minutes: Int) {
        positions[event.id] = minutes.coerceIn(0, event.durationMin)
        recent.remove(event.id); recent.add(0, event.id)
    }

    /**
     * What the Continue watching rail shows: events with a meaningful saved position, most recently watched
     * first. A live broadcast never appears (there is no saved position to return to — the live edge is the
     * only sensible place), and [resumePoint] already drops items that were barely started or finished, so a
     * title leaves the rail by itself once it is watched to the end.
     * Returns an empty list when the household has watched nothing: the caller must then omit the rail
     * entirely rather than render an empty row.
     */
    fun continueWatching(catalogue: List<SportsEvent>, max: Int = 10): List<SportsEvent> =
        recent.asSequence()
            .mapNotNull { id -> catalogue.firstOrNull { it.id == id } }
            .filter { it.status != EventStatus.LIVE && resumePoint(it) != null }
            .take(max)
            .toList()
}

/**
 * Household playback preferences (comp-player-controls: track selectors). Remembered by language, not by track id,
 * because ids are per stream: a viewer who picked Spanish subtitles on one match gets Spanish on the next one when
 * the broadcaster carries it, and "off" stays off. App-level so it survives route switches; a real app persists it
 * with DataStore and seeds it from the system locale / caption settings on first launch.
 */
class PlaybackPrefs {
    /** null = subtitles off (the default on a shared living-room screen; the system caption preference overrides it). */
    var subtitleLanguage: String? by mutableStateOf(null)
    /** Flavour within the language ("English (CC)" vs "English"): exact label first, then any track of the language. */
    var subtitleLabel: String? by mutableStateOf(null)
    var audioLanguage: String by mutableStateOf("en")
    /** Last chosen audio flavour within a language ("Audio description", "Team radio"), so it is re-applied when offered. */
    var audioDetail: String? by mutableStateOf(null)

    /** Resolve the remembered preference against what this stream offers; falls back to the first audio track. */
    fun selectionFor(tracks: TrackList): TrackSelection {
        val sub = subtitleLanguage?.let { lang ->
            tracks.subtitles.firstOrNull { it.language == lang && it.label == subtitleLabel } ?: tracks.subtitles.firstOrNull { it.language == lang }
        }
        val audio = tracks.audio.firstOrNull { it.language == audioLanguage && it.detail == audioDetail }
            ?: tracks.audio.firstOrNull { it.language == audioLanguage }
            ?: tracks.audio.first()
        return TrackSelection(subtitleId = sub?.id, audioId = audio.id)
    }
    fun rememberSubtitle(track: MediaTrack?) { subtitleLanguage = track?.language; subtitleLabel = track?.label }
    fun rememberAudio(track: MediaTrack) { audioLanguage = track.language; audioDetail = track.detail }
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
