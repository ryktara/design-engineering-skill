package com.example.tv.ui.home

import androidx.activity.compose.BackHandler
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.focusGroup
import androidx.compose.foundation.gestures.BringIntoViewSpec
import androidx.compose.foundation.gestures.LocalBringIntoViewSpec
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusProperties
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.focusRestorer
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.tv.material3.Border
import androidx.tv.material3.Button
import androidx.tv.material3.ButtonDefaults
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Surface
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.example.tv.data.EventStatus
import com.example.tv.data.HomeContent
import com.example.tv.data.Rail
import com.example.tv.data.SportsEvent
import com.example.tv.ui.HomeFocusKeys
import com.example.tv.ui.HomeFocusMemory
import com.example.tv.ui.HomeUiState
import com.example.tv.ui.MiniPlayerState
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.LocalReducedMotion
import com.example.tv.ui.theme.SportsDimens
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.android.awaitFrame

/** Pins the focused rail item at ~25% from the left instead of centring it (layout-rails pivot). */
private val RailPivotSpec = object : BringIntoViewSpec {
    override fun calculateScrollDistance(offset: Float, size: Float, containerSize: Float): Float {
        val pivot = containerSize * 0.25f
        val leading = offset
        return if (leading in 0f..(containerSize - size) && leading <= pivot) 0f else leading - pivot
    }
}

@Composable
fun HomeScreen(
    state: HomeUiState,
    mini: MiniPlayerState,
    focusMemory: HomeFocusMemory,
    onOpenDetails: (SportsEvent) -> Unit,
    onWatch: (SportsEvent) -> Unit,
    onOpenGuide: () -> Unit,
    onExpandMiniPlayer: () -> Unit,
    onRetry: () -> Unit,
    onBackToNav: () -> Unit,
    backEnabled: Boolean = true,   // false while the side navigation owns focus (its own handler exits the app)
    modifier: Modifier = Modifier,
) {
    when (state) {
        HomeUiState.Loading -> StatusPane("Loading today's sport…", action = null, onAction = null, modifier)
        is HomeUiState.Error -> StatusPane(state.message, action = "Try again", onAction = onRetry, modifier)
        HomeUiState.Empty -> StatusPane("No live sport right now. Check the guide for what is coming up.", action = "Open guide", onAction = onOpenGuide, modifier)
        is HomeUiState.Ready -> HomeReady(state.content, mini, focusMemory, onOpenDetails, onWatch, onOpenGuide, onExpandMiniPlayer, onBackToNav, backEnabled, modifier)
    }
}

/** Every non-ready state still has exactly one focusable element (never a screen without focus). */
@Composable
private fun StatusPane(message: String, action: String?, onAction: (() -> Unit)?, modifier: Modifier) {
    val fr = remember { FocusRequester() }
    LaunchedEffect(action) { if (action != null) fr.requestFocus() }
    Column(
        modifier.fillMaxSize().padding(horizontal = SportsDimens.safeH, vertical = SportsDimens.safeV),
        verticalArrangement = Arrangement.Center,
    ) {
        Text(message, style = MaterialTheme.typography.headlineMedium, color = SportsColors.textPrimary)
        if (action != null && onAction != null) {
            Spacer(Modifier.height(24.dp))
            Button(onClick = onAction, modifier = Modifier.focusRequester(fr)) { Text(action, style = MaterialTheme.typography.labelLarge) }
        }
    }
}

@OptIn(FlowPreview::class, ExperimentalFoundationApi::class)
@Composable
private fun HomeReady(
    content: HomeContent,
    mini: MiniPlayerState,
    focusMemory: HomeFocusMemory,
    onOpenDetails: (SportsEvent) -> Unit,
    onWatch: (SportsEvent) -> Unit,
    onOpenGuide: () -> Unit,
    onExpandMiniPlayer: () -> Unit,
    onBackToNav: () -> Unit,
    backEnabled: Boolean,
    modifier: Modifier,
) {
    // The hero follows the focused live tile; other rails leave it on the last live item (debounced 300 ms so
    // scrubbing across a rail does not thrash backdrop decodes). Seeded from the app-level memory so a return
    // from Details/Player shows the same backdrop the viewer left, not the first live event.
    var focusedLive by remember { mutableStateOf(focusMemory.heroEvent ?: content.heroDefault) }
    var heroEvent by remember { mutableStateOf(focusMemory.heroEvent ?: content.heroDefault) }
    LaunchedEffect(Unit) {
        snapshotFlow { focusedLive }.debounce(300).distinctUntilChanged().collect { heroEvent = it; focusMemory.heroEvent = it }
    }

    // Vertical position is app-level too (rememberSaveable only survives configuration changes, not the route
    // switch that removes Home from composition).
    val listState: LazyListState = focusMemory.columnState
    val inRails = remember { mutableStateOf(false) }

    // Focus restoration on return from Details/Player.
    // 1. Resolve the target against the *current* content: the rail is time-based, so the match may have moved
    //    or left the rail while the viewer was in the player; the same id wins, otherwise the neighbour at the
    //    remembered index, otherwise the hero.
    // 2. Scroll only when the target is not already laid out: both list states are hoisted, so in the common
    //    case the column and the rail are exactly where the viewer left them and must not be re-aligned
    //    (scrollToItem would top-align the rail, hiding the hero, and snap the card to the left edge).
    // 3. Lazy items compose one frame after the scroll: wait until the item is in layoutInfo (bounded) before
    //    requestFocus(), which throws on a detached requester and is therefore guarded.
    val railIndexById = remember(content) {
        buildMap { put("live", 1); content.rails.forEachIndexed { i, r -> put(r.id, i + 2) } }
    }
    val railItemKeys: (String) -> List<Pair<String, String?>>? = remember(content) {
        { railId ->
            val events = if (railId == "live") content.liveNow else content.rails.firstOrNull { it.id == railId }?.events
            events?.let { evs ->
                buildList {
                    if (railId == "upcoming") add(HomeFocusKeys.EPG_TILE to null)
                    evs.forEach { add(HomeFocusKeys.item(railId, it.id) to it.id) }
                }
            }
        }
    }
    LaunchedEffect(focusMemory.pendingRestore) {
        if (!focusMemory.pendingRestore) return@LaunchedEffect
        val target = focusMemory.resolveRestoreTarget(railItemKeys)
        val rail = target.railId
        if (rail != null) {
            val railState = focusMemory.railState(rail)
            railIndexById[rail]?.let { columnIndex ->
                if (listState.layoutInfo.visibleItemsInfo.none { it.index == columnIndex }) listState.scrollToItem(columnIndex)
            }
            // Wait for the rail to compose (it is a lazy column item), then align only if the card is off-screen.
            repeat(3) { if (railState.layoutInfo.totalItemsCount == 0) awaitFrame() }
            val visible = railState.layoutInfo.visibleItemsInfo
            val viewportEnd = railState.layoutInfo.viewportEndOffset
            val fullyVisible = visible.any { it.index == target.index && it.offset >= 0 && it.offset + it.size <= viewportEnd }
            if (!fullyVisible) railState.scrollToItem(target.index)
            repeat(3) { if (railState.layoutInfo.visibleItemsInfo.none { it.index == target.index }) awaitFrame() }
            // The neighbour that took the slot is now the remembered tile (next BACK/return behaves the same way).
            if (!target.exact) focusMemory.rememberTile(rail, target.index, target.key, railItemKeys(rail)?.getOrNull(target.index)?.second)
        }
        val restored = runCatching { focusMemory.requesters[target.key]?.requestFocus() }.getOrNull() == true
        if (!restored) runCatching { focusMemory.requesterFor(HomeFocusKeys.HERO_PRIMARY).requestFocus() }
        focusMemory.pendingRestore = false
    }
    LaunchedEffect(focusMemory.scrollToTopRequested) {
        if (focusMemory.scrollToTopRequested) {
            listState.animateScrollToItem(0)
            focusMemory.requesterFor(HomeFocusKeys.HERO_PRIMARY).requestFocus()
            focusMemory.scrollToTopRequested = false
        }
    }
    // Deterministic initial focus (first composition only).
    LaunchedEffect(Unit) { if (!focusMemory.pendingRestore) focusMemory.requesterFor(HomeFocusKeys.HERO_PRIMARY).requestFocus() }

    // BACK from a rail → hero/top. BACK on the hero → side navigation (then the drawer's own BackHandler exits).
    BackHandler(enabled = backEnabled) {
        if (inRails.value) focusMemory.scrollToTopRequested = true else onBackToNav()
    }

    Box(modifier.fillMaxSize().background(SportsColors.canvas)) {
        ImmersiveBackdrop(heroEvent)

        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(top = SportsDimens.safeV, bottom = SportsDimens.safeV + 24.dp),
            verticalArrangement = Arrangement.spacedBy(SportsDimens.railGap),
        ) {
            item(key = "hero") {
                HeroBlock(
                    event = heroEvent,
                    nowMin = content.nowMin,
                    mini = mini,
                    focusMemory = focusMemory,
                    onWatch = onWatch,
                    onOpenDetails = onOpenDetails,
                    onExpandMiniPlayer = onExpandMiniPlayer,
                    onFocusedAnyHeroControl = { inRails.value = false },
                )
            }
            item(key = "live-now") {
                RailRow(
                    rail = Rail("live", "Live now", content.liveNow),
                    nowMin = content.nowMin,
                    focusMemory = focusMemory,
                    onItemFocused = { ev -> focusedLive = ev; inRails.value = true },
                    onItemClick = onOpenDetails,
                )
            }
            content.rails.forEach { rail ->
                item(key = rail.id) {
                    RailRow(
                        rail = rail,
                        nowMin = content.nowMin,
                        focusMemory = focusMemory,
                        onItemFocused = { inRails.value = true },
                        onItemClick = onOpenDetails,
                        leading = if (rail.id == "upcoming") {
                            {
                                EpgEntryTile(
                                    rows = content.epgPreview,
                                    nowMin = content.nowMin,
                                    focusRequester = focusMemory.requesterFor(HomeFocusKeys.EPG_TILE),
                                    onFocused = { focusMemory.rememberTile(rail.id, 0, HomeFocusKeys.EPG_TILE); inRails.value = true },
                                    onClick = onOpenGuide,
                                )
                            }
                        } else null,
                    )
                }
            }
        }
    }
}

/** Backdrop capped to the panel, dual scrim (left→right for the text block, bottom→top for the rails). */
@Composable
private fun ImmersiveBackdrop(event: SportsEvent?) {
    // Reduced motion (ANIMATOR_DURATION_SCALE = 0): swap instantly instead of crossfading.
    val reduced = LocalReducedMotion.current
    Crossfade(targetState = event?.artUrl, animationSpec = tween(if (reduced) 0 else 400), label = "backdrop") { url ->
        Box(Modifier.fillMaxSize()) {
            if (url != null) {
                AsyncImage(model = url, contentDescription = null, modifier = Modifier.fillMaxWidth().fillMaxHeight(0.72f).align(Alignment.TopEnd))
            }
            Box(Modifier.fillMaxSize().background(Brush.horizontalGradient(0f to SportsColors.canvas, 0.45f to SportsColors.canvas.copy(alpha = 0.85f), 1f to Color.Transparent)))
            Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0f to Color.Transparent, 0.45f to SportsColors.canvas.copy(alpha = 0.55f), 0.75f to SportsColors.canvas)))
        }
    }
}

/**
 * Hero: title, one metadata line, ≤3-line synopsis, two actions (Watch live = first focus, Details), and the
 * mini player docked at the right edge of the hero band (RIGHT from Details reaches it; DOWN from it lands in
 * the Live rail). All inside the safe area.
 */
@Composable
private fun HeroBlock(
    event: SportsEvent?,
    nowMin: Long,
    mini: MiniPlayerState,
    focusMemory: HomeFocusMemory,
    onWatch: (SportsEvent) -> Unit,
    onOpenDetails: (SportsEvent) -> Unit,
    onExpandMiniPlayer: () -> Unit,
    onFocusedAnyHeroControl: () -> Unit,
) {
    val primaryFr = focusMemory.requesterFor(HomeFocusKeys.HERO_PRIMARY)
    val secondaryFr = focusMemory.requesterFor(HomeFocusKeys.HERO_SECONDARY)
    val miniFr = focusMemory.requesterFor(HomeFocusKeys.MINI_PLAYER)
    Row(
        Modifier.fillMaxWidth().padding(start = SportsDimens.contentStart, end = SportsDimens.safeH).height(SportsDimens.heroHeight).focusGroup(),
        verticalAlignment = Alignment.Bottom,
    ) {
        Column(Modifier.weight(1f)) {
            if (event != null) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (event.progressAt(nowMin) != null) { LiveBadge(); Spacer(Modifier.width(12.dp)) }
                    Text(
                        "${event.competition.name} · ${event.channel.name} · ${formatClock(event.startEpochMin)}–${formatClock(event.endEpochMin)}",
                        style = MaterialTheme.typography.labelLarge,
                        color = SportsColors.textSecondary,
                    )
                }
                Spacer(Modifier.height(6.dp))
                // One line: the hero band has a fixed height so the first rail never jumps when the focused item changes.
                Text(event.title, style = MaterialTheme.typography.displayMedium, color = SportsColors.textPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Spacer(Modifier.height(2.dp))
                Text(
                    listOfNotNull(event.score, event.clock).joinToString("   ")
                        .ifBlank { if (event.status == EventStatus.UPCOMING) "Starts in ${event.startEpochMin - nowMin} min" else "" },
                    style = MaterialTheme.typography.titleLarge,
                    color = SportsColors.textPrimary,
                )
                if (event.synopsis.isNotBlank()) {
                    Spacer(Modifier.height(6.dp))
                    Text(event.synopsis, style = MaterialTheme.typography.bodyMedium, color = SportsColors.textSecondary, maxLines = 2, overflow = TextOverflow.Ellipsis, modifier = Modifier.fillMaxWidth(0.6f))
                }
                Spacer(Modifier.height(14.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    HeroButton(
                        text = if (event.progressAt(nowMin) != null) "Watch live" else "Watch",
                        primary = true,
                        focusRequester = primaryFr,
                        onFocused = { focusMemory.rememberHeroControl(HomeFocusKeys.HERO_PRIMARY); onFocusedAnyHeroControl() },
                        onClick = { onWatch(event) },
                    )
                    HeroButton(
                        text = "Details",
                        primary = false,
                        focusRequester = secondaryFr,
                        onFocused = { focusMemory.rememberHeroControl(HomeFocusKeys.HERO_SECONDARY); onFocusedAnyHeroControl() },
                        onClick = { onOpenDetails(event) },
                        modifier = Modifier.focusProperties { if (mini !is MiniPlayerState.Hidden) right = miniFr },
                    )
                }
            }
        }
        if (mini !is MiniPlayerState.Hidden) {
            MiniPlayer(
                state = mini,
                focusRequester = miniFr,
                onFocused = { focusMemory.rememberHeroControl(HomeFocusKeys.MINI_PLAYER); onFocusedAnyHeroControl() },
                onClick = onExpandMiniPlayer,
                modifier = Modifier.focusProperties { left = secondaryFr },
            )
        }
    }
}

@Composable
private fun HeroButton(
    text: String,
    primary: Boolean,
    focusRequester: FocusRequester,
    onFocused: () -> Unit,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Button(
        onClick = onClick,
        modifier = modifier.focusRequester(focusRequester).onFocusChanged { if (it.isFocused) onFocused() },
        colors = ButtonDefaults.colors(
            containerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            contentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
            focusedContainerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            focusedContentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
        ),
        // Reduced motion keeps the ring and glow but drops the scale animation.
        scale = ButtonDefaults.scale(focusedScale = if (LocalReducedMotion.current) 1f else SportsDimens.focusScale),
        border = ButtonDefaults.border(focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = RoundedCornerShape(50))),
        contentPadding = PaddingValues(horizontal = 28.dp, vertical = 12.dp),
    ) {
        Text(text, style = MaterialTheme.typography.labelLarge)
    }
}

/**
 * Mini player: 16:9 thumbnail 1/4 width, LIVE/paused/buffering state text, score. One focusable surface;
 * SELECT expands to the full player. Sits inside the safe area at the right edge of the hero band.
 */
@Composable
fun MiniPlayer(
    state: MiniPlayerState,
    focusRequester: FocusRequester,
    onFocused: () -> Unit,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val event = when (state) {
        is MiniPlayerState.Playing -> state.event
        is MiniPlayerState.Paused -> state.event
        is MiniPlayerState.Buffering -> state.event
        MiniPlayerState.Hidden -> return
    }
    val statusText = when (state) {
        is MiniPlayerState.Playing -> "Playing"
        is MiniPlayerState.Paused -> "Paused"
        is MiniPlayerState.Buffering -> "Buffering…"
        MiniPlayerState.Hidden -> ""
    }
    Surface(
        onClick = onClick,
        modifier = modifier
            .focusRequester(focusRequester)
            .onFocusChanged { if (it.isFocused) onFocused() }
            .semantics(mergeDescendants = true) {
                contentDescription = "Now playing ${event.title}, ${listOfNotNull(event.score, event.clock).joinToString(" ")}. $statusText. Select to expand"
            }
            .padding(SportsDimens.focusPadding / 2),
        shape = androidx.tv.material3.ClickableSurfaceDefaults.shape(RoundedCornerShape(8.dp)),
        scale = androidx.tv.material3.ClickableSurfaceDefaults.scale(focusedScale = 1.05f),
        border = androidx.tv.material3.ClickableSurfaceDefaults.border(focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = RoundedCornerShape(8.dp))),
        colors = androidx.tv.material3.ClickableSurfaceDefaults.colors(containerColor = SportsColors.surface, focusedContainerColor = SportsColors.surface),
    ) {
        Column(Modifier.width(240.dp)) {
            Box(Modifier.fillMaxWidth().height(135.dp).clip(RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp))) {
                // Real app: Media3 PlayerView in an AndroidView sized to this box; here the poster stands in.
                AsyncImage(model = event.artUrl, contentDescription = null, modifier = Modifier.fillMaxSize())
                Row(Modifier.align(Alignment.TopStart).padding(8.dp)) { LiveBadge() }
                if (state !is MiniPlayerState.Playing) {
                    Box(Modifier.fillMaxSize().background(SportsColors.canvas.copy(alpha = 0.6f)), contentAlignment = Alignment.Center) {
                        Text(statusText, style = MaterialTheme.typography.labelLarge, color = SportsColors.textPrimary)
                    }
                }
            }
            Column(Modifier.padding(horizontal = 12.dp, vertical = 8.dp)) {
                Text(event.title, style = MaterialTheme.typography.labelLarge, color = SportsColors.textPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(
                    listOfNotNull(event.score, event.clock).joinToString("  ").ifBlank { statusText },
                    style = MaterialTheme.typography.labelMedium,
                    color = SportsColors.textSecondary,
                    maxLines = 1,
                )
            }
        }
    }
}

/** One rail: heading (semantics heading for TalkBack), LazyRow with focusRestorer + pivot spec; optional leading tile. */
@Composable
private fun RailRow(
    rail: Rail,
    nowMin: Long,
    focusMemory: HomeFocusMemory,
    onItemFocused: (SportsEvent) -> Unit,
    onItemClick: (SportsEvent) -> Unit,
    leading: (@Composable () -> Unit)? = null,
) {
    Column {
        Text(
            rail.title,
            style = MaterialTheme.typography.titleMedium,
            color = SportsColors.textPrimary,
            modifier = Modifier.padding(start = SportsDimens.contentStart, bottom = 8.dp).semantics { heading() },
        )
        CompositionLocalProvider(LocalBringIntoViewSpec provides RailPivotSpec) {
            LazyRow(
                state = focusMemory.railState(rail.id),
                modifier = Modifier.fillMaxWidth().focusRestorer(),
                // Cards start at the safe margin but scroll under it; the trailing partial card signals more.
                contentPadding = PaddingValues(start = SportsDimens.contentStart - SportsDimens.focusPadding / 2, end = SportsDimens.safeH),
                horizontalArrangement = Arrangement.spacedBy(SportsDimens.gutter - SportsDimens.focusPadding),
            ) {
                if (leading != null) item(key = "leading") { leading() }
                items(rail.events.size, key = { rail.events[it].id }) { index ->
                    val event = rail.events[index]
                    val key = HomeFocusKeys.item(rail.id, event.id)
                    val lazyIndex = if (leading != null) index + 1 else index
                    EventCard(
                        event = event,
                        nowMin = nowMin,
                        focusRequester = focusMemory.requesterFor(key),
                        onFocused = { focusMemory.rememberTile(rail.id, lazyIndex, key, event.id); onItemFocused(event) },
                        onClick = { onItemClick(event) },
                    )
                }
            }
        }
    }
}
