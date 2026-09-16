package com.example.tv.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.focusRestorer
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.unit.dp
import androidx.tv.material3.DrawerValue
import androidx.tv.material3.Icon
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.ModalNavigationDrawer
import androidx.tv.material3.NavigationDrawerItem
import androidx.tv.material3.Text
import androidx.tv.material3.rememberDrawerState
import com.example.tv.data.EventStatus
import com.example.tv.data.SampleCatalog
import com.example.tv.data.SportsEvent
import com.example.tv.ui.details.EventDetailsScreen
import com.example.tv.ui.home.HomeScreen
import com.example.tv.ui.player.PlayerScreen
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.SportsDimens
import com.example.tv.ui.theme.SportsTheme

/**
 * App shell: collapsible side navigation + route switch. Focus memory for Home lives here so it survives
 * the Home composable leaving composition while Details/Player are shown.
 *
 * BACK layering (tv-back-behavior): player track sheet → player · player → home (the stream keeps playing in the
 * mini player) · details → home (focus restored to the opening tile) · home rails → hero/top · hero → side nav ·
 * side nav → exit (Activity finish, no confirmation loop).
 */
@Composable
fun SportsApp(onExit: () -> Unit) {
    var route: Route by remember { mutableStateOf(Route.Home) }
    var home: HomeUiState by remember { mutableStateOf(HomeUiState.Ready(SampleCatalog.content)) }
    var mini: MiniPlayerState by remember { mutableStateOf(MiniPlayerState.Playing(SampleCatalog.liveNow[1])) }
    var section by remember { mutableStateOf(NavSection.HOME) }
    val focusMemory = remember { HomeFocusMemory() }
    val library = remember { LibraryState() }   // watchlist + resume positions, shared by Home cards and Details
    val playback = remember { PlaybackPrefs() } // remembered subtitle/audio language, applied to every stream that carries it
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val navFirstItem = remember { FocusRequester() }
    var navHasFocus by remember { mutableStateOf(false) }

    fun leaveHome(to: Route) { focusMemory.pendingRestore = true; route = to }
    fun returnHome() { route = Route.Home /* pendingRestore already true → HomeScreen restores the tile */ }

    SportsTheme {
        when (val r = route) {
            is Route.Details -> EventDetailsScreen(
                event = r.event,
                nowMin = SampleCatalog.content.nowMin,
                library = library,
                related = SampleCatalog.related(r.event),
                onPlay = { startAt -> route = Route.Player(r.event, startAt) },
                // A related card re-targets Details (route replaced, not pushed): BACK still returns to the Home tile.
                onOpenRelated = { route = Route.Details(it) },
                onBack = { returnHome() },
            )
            is Route.Player -> PlayerScreen(
                event = r.event,
                startAtMin = r.startAtMin,
                nowMin = SampleCatalog.content.nowMin,
                tracks = SampleCatalog.tracksFor(r.event),   // real app: Player.currentTracks after onTracksChanged
                prefs = playback,
                onBack = { watchedMin ->
                    // Media3 reports the real position; the placeholder stands in with what it "played".
                    if (r.event.status != EventStatus.LIVE) library.savePosition(r.event, watchedMin)
                    mini = MiniPlayerState.Playing(r.event); returnHome()
                },
            )
            Route.Guide -> GuidePlaceholder(onBack = { returnHome() })
            Route.Home -> Row(Modifier.fillMaxSize().background(SportsColors.canvas)) {
                // Exiting from the drawer: BACK while the drawer has focus finishes the Activity.
                BackHandler(enabled = navHasFocus) { onExit() }
                // Modal (overlay) drawer: expanding it must not reflow the hero and rails behind it.
                ModalNavigationDrawer(
                    drawerState = drawerState,
                    drawerContent = {
                        Column(
                            Modifier
                                .fillMaxHeight()
                                .width(if (drawerState.currentValue == DrawerValue.Open) SportsDimens.navExpanded else SportsDimens.navCollapsed)
                                // The icon strip is persistent UI: it carries the 48 dp overscan margin itself.
                                .padding(start = SportsDimens.safeH, end = 12.dp, top = SportsDimens.safeV, bottom = SportsDimens.safeV)
                                .onFocusChanged { navHasFocus = it.hasFocus }
                                .focusRestorer(),
                        ) {
                            NavSection.entries.forEachIndexed { i, s ->
                                NavigationDrawerItem(
                                    selected = s == section,
                                    onClick = { section = s; if (s == NavSection.GUIDE) leaveHome(Route.Guide) },
                                    leadingContent = { Icon(imageVector = sectionIcon(s), contentDescription = null) },
                                    modifier = if (i == 0) Modifier.focusRequester(navFirstItem) else Modifier,
                                ) { Text(s.label, style = MaterialTheme.typography.labelLarge) }
                            }
                        }
                    },
                ) {
                    Box(Modifier.fillMaxSize().padding(start = SportsDimens.navCollapsed).focusRestorer()) {
                        HomeScreen(
                            state = home,
                            mini = mini,
                            focusMemory = focusMemory,
                            onOpenDetails = { leaveHome(Route.Details(it)) },
                            onWatch = { leaveHome(Route.Player(it)) },
                            onOpenGuide = { leaveHome(Route.Guide) },
                            onExpandMiniPlayer = { (mini as? MiniPlayerState.Playing)?.let { leaveHome(Route.Player(it.event)) } },
                            onRetry = { home = HomeUiState.Loading },
                            onBackToNav = { navFirstItem.requestFocus() },
                            backEnabled = !navHasFocus,   // while the drawer has focus, BACK exits (handler above)
                            library = library,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun GuidePlaceholder(onBack: () -> Unit) {
    BackHandler { onBack() }
    Box(Modifier.fillMaxSize().background(SportsColors.canvas)) {
        Text("TV Guide", style = MaterialTheme.typography.headlineMedium, color = SportsColors.textPrimary, modifier = Modifier.padding(SportsDimens.safeH, SportsDimens.safeV))
    }
}

private fun sectionIcon(s: NavSection) = when (s) {
    NavSection.HOME -> androidx.compose.material.icons.Icons.Filled.Home
    NavSection.LIVE -> androidx.compose.material.icons.Icons.Filled.PlayArrow
    NavSection.GUIDE -> androidx.compose.material.icons.Icons.Filled.List
    NavSection.CATCH_UP -> androidx.compose.material.icons.Icons.Filled.Refresh
    NavSection.SEARCH -> androidx.compose.material.icons.Icons.Filled.Search
    NavSection.SETTINGS -> androidx.compose.material.icons.Icons.Filled.Settings
}
