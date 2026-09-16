package com.example.tv.ui.details

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.focusRestorer
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.tv.material3.Border
import androidx.tv.material3.Button
import androidx.tv.material3.ButtonDefaults
import androidx.tv.material3.Icon
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.example.tv.data.EventStatus
import com.example.tv.data.SportsEvent
import com.example.tv.ui.LibraryState
import com.example.tv.ui.home.EventCard
import com.example.tv.ui.home.LiveBadge
import com.example.tv.ui.home.Pill
import com.example.tv.ui.home.RailPivotSpec
import com.example.tv.ui.home.formatClock
import com.example.tv.ui.theme.LocalReducedMotion
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.SportsDimens

/**
 * Match details (media-resume-and-details + cta-focus-selects):
 * backdrop → LIVE badge + one metadata line → title (≤2 lines) → score/clock → synopsis (≤3 lines) → a short
 * scannable metadata block (text, never colour alone) → ≤4 actions in one row → a related rail below.
 *
 * Actions by state (the first one is the primary and takes default focus):
 *   LIVE                → Watch live · Watch from start · watchlist toggle
 *   REPLAY, position    → Resume · N min left · Start over · watchlist toggle
 *   REPLAY, no position → Play · watchlist toggle
 *   UPCOMING            → Set reminder · watchlist toggle
 * The watchlist toggle carries its state in text ("Add to watchlist" / "In watchlist") and in semantics.
 *
 * Focus: LEFT/RIGHT between actions, DOWN into the related rail (the LazyColumn brings it into view), UP back
 * to the remembered action (focusRestorer). BACK returns to Home; SportsApp restores the launching tile.
 * SELECT on a related card re-targets this screen (route replaced, not pushed), so BACK still returns Home.
 */
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun EventDetailsScreen(
    event: SportsEvent,
    nowMin: Long,
    library: LibraryState,
    related: List<SportsEvent>,
    onPlay: (startAtMin: Int?) -> Unit,
    onOpenRelated: (SportsEvent) -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val playFr = remember(event.id) { FocusRequester() }
    LaunchedEffect(event.id) { runCatching { playFr.requestFocus() } }
    BackHandler { onBack() }

    val resumeAt = library.resumePoint(event)
    val saved = library.isSaved(event.id)
    val columnState = rememberLazyListState()

    Box(modifier.fillMaxSize().background(SportsColors.canvas)) {
        AsyncImage(model = event.artUrl, contentDescription = null, modifier = Modifier.fillMaxWidth().fillMaxHeight(0.8f).align(Alignment.TopEnd))
        Box(Modifier.fillMaxSize().background(Brush.horizontalGradient(0f to SportsColors.canvas, 0.55f to SportsColors.canvas.copy(alpha = 0.8f), 1f to Color.Transparent)))
        Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0.3f to Color.Transparent, 0.85f to SportsColors.canvas)))

        LazyColumn(
            state = columnState,
            modifier = Modifier.fillMaxSize(),
            // The related rail starts below the fold; composing one item beyond the viewport lets DOWN from the
            // action row find a focus target, and the focus system then scrolls it into view.
            beyondBoundsItemCount = 1,
        ) {
            item(key = "hero") {
                Column(
                    Modifier.fillParentMaxHeight().padding(horizontal = SportsDimens.safeH, vertical = SportsDimens.safeV),
                    verticalArrangement = Arrangement.Bottom,
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        if (event.status == EventStatus.LIVE) LiveBadge()
                        if (event.status == EventStatus.REPLAY) Pill("REPLAY", SportsColors.selectionBg, SportsColors.textPrimary)
                        Text("${event.competition.name} · ${event.channel.name} · ${formatClock(event.startEpochMin)}–${formatClock(event.endEpochMin)}", style = MaterialTheme.typography.labelLarge, color = SportsColors.textSecondary)
                    }
                    Spacer(Modifier.height(8.dp))
                    // displayMedium (same as the home hero), not displayLarge: with a 2-line title, a 3-line synopsis, the
                    // metadata block and the action row, displayLarge pushes the LIVE badge/meta line above the safe area.
                    Text(event.title, style = MaterialTheme.typography.displayMedium, color = SportsColors.textPrimary, maxLines = 2, overflow = TextOverflow.Ellipsis, modifier = Modifier.fillMaxWidth(0.7f).semantics { heading() })
                    if (event.score != null || event.clock != null) {
                        Spacer(Modifier.height(4.dp))
                        Text(listOfNotNull(event.score, event.clock).joinToString("   "), style = MaterialTheme.typography.headlineMedium, color = SportsColors.textPrimary)
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(event.synopsis.ifBlank { "No description available." }, style = MaterialTheme.typography.bodyMedium, color = SportsColors.textSecondary, maxLines = 3, overflow = TextOverflow.Ellipsis, modifier = Modifier.fillMaxWidth(0.55f))
                    Spacer(Modifier.height(16.dp))
                    MetadataBlock(event, nowMin, resumeAt)
                    Spacer(Modifier.height(20.dp))
                    ActionRow(event, nowMin, resumeAt, saved, playFr, onPlay, onToggleWatchlist = { library.toggleWatchlist(event.id) })
                }
            }
            if (related.isNotEmpty()) {
                item(key = "related") {
                    RelatedRail(
                        title = if (related.count { it.competition.id == event.competition.id } >= 2) "More ${event.competition.name}" else "More ${event.competition.sport}",
                        events = related,
                        nowMin = nowMin,
                        library = library,
                        onOpen = onOpenRelated,
                    )
                }
            }
        }
    }
}

/** Short scannable block: label above value, four columns max, all text (badges as text not colour). */
@Composable
private fun MetadataBlock(event: SportsEvent, nowMin: Long, resumeAt: Int?) {
    val status = when (event.status) {
        EventStatus.LIVE -> "Live · ${event.clock ?: ""}".trimEnd(' ', '·')
        EventStatus.UPCOMING -> "Starts in ${event.startEpochMin - nowMin} min"
        EventStatus.REPLAY -> if (resumeAt != null) "${event.durationMin - resumeAt} min left" else "Full time"
    }
    Row(horizontalArrangement = Arrangement.spacedBy(40.dp)) {
        MetaItem("Channel", "${event.channel.number} ${event.channel.name}")
        MetaItem("Kick-off", formatClock(event.startEpochMin))
        MetaItem("Length", "${event.durationMin} min")
        MetaItem("Status", status)
    }
}

@Composable
private fun MetaItem(label: String, value: String) {
    Column(Modifier.semantics(mergeDescendants = true) {}) {
        Text(label, style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary)
        Text(value, style = MaterialTheme.typography.labelLarge, color = SportsColors.textPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
private fun ActionRow(
    event: SportsEvent,
    nowMin: Long,
    resumeAt: Int?,
    saved: Boolean,
    playFr: FocusRequester,
    onPlay: (Int?) -> Unit,
    onToggleWatchlist: () -> Unit,
) {
    // The row sits at the safe-area edge: reserve the 1.08 scale overflow so the focused first button never
    // lifts into the overscan margin. A wide primary ("Resume · 118 min left", ~300 dp) grows ~12 dp per side,
    // so the full focusPadding is reserved (the cards reserve half because they are narrower).
    // The block is bottom-aligned at the vertical safe edge as well, so the lift is reserved below too.
    Row(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(start = SportsDimens.focusPadding, bottom = SportsDimens.focusPadding / 2).focusRestorer()) {
        when (event.status) {
            EventStatus.LIVE -> {
                DetailButton("Watch live", primary = true, onClick = { onPlay(null) }, modifier = Modifier.focusRequester(playFr))
                DetailButton("Watch from start", primary = false, onClick = { onPlay(0) })
            }
            EventStatus.REPLAY -> if (resumeAt != null) {
                DetailButton("Resume · ${event.durationMin - resumeAt} min left", primary = true, onClick = { onPlay(resumeAt) }, modifier = Modifier.focusRequester(playFr))
                DetailButton("Start over", primary = false, onClick = { onPlay(0) })
            } else {
                DetailButton("Play", primary = true, onClick = { onPlay(0) }, modifier = Modifier.focusRequester(playFr))
            }
            EventStatus.UPCOMING -> DetailButton("Set reminder", primary = true, onClick = { /* reminder service */ }, modifier = Modifier.focusRequester(playFr))
        }
        // Toggle with a text state: never colour alone. The state is also exposed to TalkBack.
        DetailButton(
            text = if (saved) "In watchlist" else "Add to watchlist",
            primary = false,
            icon = if (saved) Icons.Filled.Check else Icons.Filled.Add,
            onClick = onToggleWatchlist,
            modifier = Modifier.semantics { stateDescription = if (saved) "In watchlist" else "Not in watchlist" },
        )
    }
}

/** Related events: same card, focus treatment and pivot as the home rails, so the screen reads as one system. */
@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun RelatedRail(title: String, events: List<SportsEvent>, nowMin: Long, library: LibraryState, onOpen: (SportsEvent) -> Unit) {
    Column(Modifier.padding(bottom = SportsDimens.safeV)) {
        Text(title, style = MaterialTheme.typography.titleMedium, color = SportsColors.textPrimary, modifier = Modifier.padding(start = SportsDimens.safeH, bottom = 8.dp).semantics { heading() })
        CompositionLocalProvider(LocalBringIntoViewSpec provides RailPivotSpec) {
            LazyRow(
                modifier = Modifier.fillMaxWidth().focusRestorer(),
                contentPadding = PaddingValues(start = SportsDimens.safeH - SportsDimens.focusPadding / 2, end = SportsDimens.safeH),
                horizontalArrangement = Arrangement.spacedBy(SportsDimens.gutter - SportsDimens.focusPadding),
            ) {
                items(events.size, key = { events[it].id }) { i ->
                    val ev = events[i]
                    EventCard(
                        event = ev,
                        nowMin = nowMin,
                        focusRequester = remember(ev.id) { FocusRequester() },
                        onFocused = {},
                        onClick = { onOpen(ev) },
                        saved = library.isSaved(ev.id),
                        resumeFraction = library.resumePoint(ev)?.let { it / ev.durationMin.toFloat() },
                    )
                }
            }
        }
    }
}

@Composable
private fun DetailButton(text: String, primary: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier, icon: ImageVector? = null) {
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.colors(
            containerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            contentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
            focusedContainerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            focusedContentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
        ),
        // Same focus treatment as the hero buttons: ring + scale (scale dropped under reduced motion).
        scale = ButtonDefaults.scale(focusedScale = if (LocalReducedMotion.current) 1f else SportsDimens.focusScale),
        border = ButtonDefaults.border(focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = RoundedCornerShape(50))),
        contentPadding = PaddingValues(horizontal = 28.dp, vertical = 12.dp),
    ) {
        if (icon != null) { Icon(imageVector = icon, contentDescription = null); Spacer(Modifier.width(10.dp)) }
        Text(text, style = MaterialTheme.typography.labelLarge)
    }
}
