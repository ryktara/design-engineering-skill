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
import androidx.compose.runtime.DisposableEffect
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
 *
 * The layering is enforced by an explicit [NavStack] rather than by each screen happening to own an enabled
 * BackHandler: a route below the top of the stack pops (the app-level fallback handler below catches any screen
 * that does not handle BACK itself), and only the Home root with focus in the side navigation may exit. A screen
 * that forgets its own BackHandler now loses a layer instead of throwing the viewer out of the app.
 */
@Composable
fun SportsApp(onExit: () -> Unit) {
    val nav = remember { NavStack() }
    var home: HomeUiState by remember { mutableStateOf(HomeUiState.Ready(SampleCatalog.content)) }
    var mini: MiniPlayerState by remember { mutableStateOf(MiniPlayerState.Playing(SampleCatalog.liveNow[1])) }
    var section by remember { mutableStateOf(NavSection.HOME) }
    val focusMemory = remember { HomeFocusMemory() }
    val library = remember {
        // Watchlist + resume positions, shared by Home cards, the Continue watching rail and Details.
        // A real app loads the household's history from the account service on launch; the sample seeds three
        // part-watched replays (most recent last) so the rail has content without a player session first.
        LibraryState().apply {
            SampleCatalog.allEvents.firstOrNull { it.id == "r5" }?.let { savePosition(it, 74) }
            SampleCatalog.allEvents.firstOrNull { it.id == "r2" }?.let { savePosition(it, 41) }
            SampleCatalog.allEvents.firstOrNull { it.id == "r1" }?.let { savePosition(it, 88) }
        }
    }
    val playback = remember { PlaybackPrefs() } // remembered subtitle/audio language, applied to every stream that carries it
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val navFirstItem = remember { FocusRequester() }
    var navHasFocus by remember { mutableStateOf(false) }

    // Leaving Home disposes the drawer without an onFocusChanged callback, so the flag that decides "BACK exits"
    // has to be cleared here as well as on dispose; a stale `true` used to arm the exit handler for the next BACK
    // press after the viewer came back to Home.
    fun leaveHome(to: Route) { focusMemory.pendingRestore = true; navHasFocus = false; nav.push(to) }
    fun returnHome() { nav.pop() /* pendingRestore already true → HomeScreen restores the tile */ }

    SportsTheme {
        // App-level fallback, composed first so every screen's own BackHandler takes precedence: below the root,
        // BACK can only pop a layer. Nothing can reach the Activity default (finish) from Details/Player/Guide.
        BackHandler(enabled = !nav.atRoot) { nav.pop() }
        when (val r = nav.current) {
            is Route.Details -> EventDetailsScreen(
                event = r.event,
                nowMin = SampleCatalog.content.nowMin,
                library = library,
                related = SampleCatalog.related(r.event),
                onPlay = { startAt -> nav.push(Route.Player(r.event, startAt)) },
                // A related card re-targets Details (top replaced, not pushed): BACK still returns to the Home tile.
                onOpenRelated = { nav.replaceTop(Route.Details(it)) },
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
                    // Existing contract: leaving the player returns to Home with the stream in the mini player,
                    // it does not step back through Details. Unwind the whole stack in one move.
                    mini = MiniPlayerState.Playing(r.event); nav.popToRoot()
                },
            )
            Route.Guide -> GuidePlaceholder(onBack = { returnHome() })
            Route.Home -> Row(Modifier.fillMaxSize().background(SportsColors.canvas)) {
                // Exiting from the drawer: BACK at the Home root while the drawer has focus finishes the Activity.
                // `nav.atRoot` is redundant inside this branch today and is stated anyway: exit is a root decision.
                BackHandler(enabled = navHasFocus && nav.atRoot) { onExit() }
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
                            // onFocusChanged does not fire on dispose: without this the flag survives the route
                            // switch and the next BACK on Home exits while focus sits on a rail tile.
                            DisposableEffect(Unit) { onDispose { navHasFocus = false } }
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
                            onResume = { event, startAt -> leaveHome(Route.Player(event, startAt)) },
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
