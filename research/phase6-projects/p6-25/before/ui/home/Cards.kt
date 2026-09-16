package com.example.tv.ui.home

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.tv.material3.Border
import androidx.tv.material3.Card
import androidx.tv.material3.CardDefaults
import androidx.tv.material3.Glow
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.example.tv.data.EpgPreviewRow
import com.example.tv.data.EventStatus
import com.example.tv.data.SportsEvent
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.LocalReducedMotion
import com.example.tv.ui.theme.SportsDimens

private val CardShape = RoundedCornerShape(8.dp)

/** Shared focus treatment: scale + 3 dp white border + accent glow. Never colour tint alone. */
@Composable
private fun focusedCardStyle() = Triple(
    CardDefaults.scale(focusedScale = if (LocalReducedMotion.current) 1f else SportsDimens.focusScale),
    CardDefaults.border(
        focusedBorder = Border(
            border = androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing),
            shape = CardShape,
        ),
    ),
    CardDefaults.glow(focusedGlow = Glow(elevationColor = SportsColors.accent.copy(alpha = 0.55f), elevation = 16.dp)),
)

/**
 * 16:9 event card. The whole card is the target (cta-focus-selects); no inner buttons.
 * Live cards carry a LIVE badge + score/clock and a progress bar of the broadcast inside the art bottom edge;
 * a replay with a saved position shows the watched fraction on the same bar (continue watching).
 * [saved] renders a text "SAVED" pill (watchlist state is reflected wherever the event appears).
 */
@Composable
fun EventCard(
    event: SportsEvent,
    nowMin: Long,
    focusRequester: FocusRequester,
    onFocused: () -> Unit,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    saved: Boolean = false,
    resumeFraction: Float? = null,
) {
    val (scale, border, glow) = focusedCardStyle()
    val progress = event.progressAt(nowMin) ?: resumeFraction
    val status = when (event.status) {
        EventStatus.LIVE -> "Live, ${event.clock ?: ""} ${event.score ?: ""}"
        EventStatus.UPCOMING -> "Starts in ${event.startEpochMin - nowMin} minutes"
        EventStatus.REPLAY -> "Replay${event.score?.let { ", final score $it" } ?: ""}${resumeFraction?.let { ", ${(it * 100).toInt()} percent watched" } ?: ""}"
    } + if (saved) ". In watchlist" else ""
    Column(
        modifier = modifier
            .width(SportsDimens.cardW)
            .padding(SportsDimens.focusPadding / 2), // room for the 1.08 scale so neighbours are not clipped
    ) {
        Card(
            onClick = onClick,
            modifier = Modifier
                .focusRequester(focusRequester)
                .onFocusChanged { if (it.isFocused) onFocused() }
                .semantics(mergeDescendants = true) {
                    contentDescription = "${event.title}, ${event.competition.name}, ${event.channel.name}. $status"
                },
            shape = CardDefaults.shape(CardShape),
            scale = scale,
            border = border,
            glow = glow,
            colors = CardDefaults.colors(containerColor = SportsColors.elevated),
        ) {
            Box(Modifier.width(SportsDimens.cardW - SportsDimens.focusPadding).height(SportsDimens.cardH)) {
                AsyncImage(
                    model = event.artUrl,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    placeholder = null,
                    error = null,
                )
                // Text-only fallback under the image keeps the card legible when artwork is missing/slow.
                Text(
                    text = event.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = SportsColors.textSecondary,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.align(Alignment.Center).padding(16.dp),
                )
                // Bottom scrim so badge/score/progress read on any artwork.
                Box(
                    Modifier
                        .fillMaxWidth()
                        .height(64.dp)
                        .align(Alignment.BottomCenter)
                        .background(Brush.verticalGradient(listOf(Color.Transparent, SportsColors.canvas.copy(alpha = 0.85f)))),
                )
                Row(
                    Modifier.align(Alignment.TopStart).padding(10.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    if (event.status == EventStatus.LIVE) LiveBadge()
                    if (event.status == EventStatus.REPLAY) Pill("REPLAY", SportsColors.selectionBg, SportsColors.textPrimary)
                    Spacer(Modifier.weight(1f))
                    if (saved) Pill("SAVED", SportsColors.selectionBg, SportsColors.textPrimary)
                }
                Row(
                    Modifier.align(Alignment.BottomStart).padding(start = 12.dp, end = 12.dp, bottom = if (progress != null) 14.dp else 10.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    // Left: match clock / start time / full time. Right: score or countdown. The channel lives in the
                    // subtitle line so a long tennis score never squeezes it to a two-letter ellipsis.
                    Text(
                        text = when (event.status) {
                            EventStatus.LIVE -> event.clock ?: "Live"
                            EventStatus.UPCOMING -> formatClock(event.startEpochMin)
                            EventStatus.REPLAY -> "Full time"
                        },
                        style = MaterialTheme.typography.labelMedium,
                        color = SportsColors.textPrimary,
                        modifier = Modifier.weight(1f),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    val trailing = when (event.status) {
                        EventStatus.LIVE -> event.score ?: ""
                        EventStatus.UPCOMING -> "in ${event.startEpochMin - nowMin} min"
                        EventStatus.REPLAY -> event.score ?: ""
                    }
                    Text(
                        text = trailing,
                        style = MaterialTheme.typography.labelLarge.copy(fontWeight = FontWeight.Bold),
                        color = SportsColors.textPrimary,
                        maxLines = 1,
                    )
                }
                if (progress != null) {
                    // Elapsed broadcast; accent on a 40% white track so it stays ≥3:1 on any art.
                    Box(Modifier.fillMaxWidth().height(6.dp).align(Alignment.BottomCenter).background(Color.White.copy(alpha = 0.35f))) {
                        Box(Modifier.fillMaxWidth(progress).height(6.dp).background(SportsColors.accent))
                    }
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        // Title below the art (art does not reliably contain it); reserved two lines so rows never jump.
        Text(
            text = event.title,
            style = MaterialTheme.typography.bodyMedium,
            color = SportsColors.textPrimary,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.padding(horizontal = 4.dp),
        )
        Text(
            text = "${event.competition.name} · ${event.channel.name}",
            style = MaterialTheme.typography.labelMedium,
            color = SportsColors.textSecondary,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.padding(horizontal = 4.dp),
        )
    }
}

/**
 * EPG entry tile: the first item of the "Coming up" rail. Wider than an event card (2-up width), flat tonal
 * surface (guide identity, not imagery), three channel rows of now/next with tabular times, and a "Full guide"
 * affordance. SELECT opens the Guide route.
 */
@Composable
fun EpgEntryTile(
    rows: List<EpgPreviewRow>,
    nowMin: Long,
    focusRequester: FocusRequester,
    onFocused: () -> Unit,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val (scale, border, glow) = focusedCardStyle()
    Column(modifier = modifier.width(SportsDimens.epgTileW).padding(SportsDimens.focusPadding / 2)) {
        Card(
            onClick = onClick,
            modifier = Modifier
                .focusRequester(focusRequester)
                .onFocusChanged { if (it.isFocused) onFocused() }
                .semantics(mergeDescendants = true) { contentDescription = "TV guide. ${rows.size} channels now and next. Open full guide" },
            shape = CardDefaults.shape(CardShape),
            scale = scale,
            border = border,
            glow = glow,
            colors = CardDefaults.colors(containerColor = SportsColors.surface),
        ) {
            Column(
                Modifier
                    .width(SportsDimens.epgTileW - SportsDimens.focusPadding)
                    .height(SportsDimens.cardH)
                    .border(1.dp, SportsColors.borderDefault, CardShape)
                    .padding(horizontal = 16.dp, vertical = 12.dp),
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("TV Guide", style = MaterialTheme.typography.titleMedium, color = SportsColors.textPrimary, modifier = Modifier.weight(1f))
                    Text(formatClock(nowMin), style = MaterialTheme.typography.labelLarge, color = SportsColors.accent)
                }
                Spacer(Modifier.height(6.dp))
                rows.take(3).forEach { row ->
                    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            "%03d".format(row.channel.number),
                            style = MaterialTheme.typography.labelMedium,
                            color = SportsColors.textSecondary,
                            modifier = Modifier.width(48.dp),
                        )
                        Text(
                            row.now.title,
                            style = MaterialTheme.typography.labelMedium,
                            color = SportsColors.textPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f),
                        )
                        Text(
                            row.next?.let { "${formatClock(it.startEpochMin)} ${it.title}" } ?: "",
                            style = MaterialTheme.typography.labelMedium,
                            color = SportsColors.textSecondary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f).padding(start = 12.dp),
                        )
                    }
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        Text("Full guide", style = MaterialTheme.typography.bodyMedium, color = SportsColors.textPrimary, modifier = Modifier.padding(horizontal = 4.dp))
        Text("All channels · now and next", style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary, modifier = Modifier.padding(horizontal = 4.dp))
    }
}

@Composable
fun LiveBadge() = Row(
    Modifier.clip(RoundedCornerShape(4.dp)).background(SportsColors.live).padding(horizontal = 8.dp, vertical = 2.dp),
    verticalAlignment = Alignment.CenterVertically,
) {
    Box(Modifier.size(8.dp).clip(RoundedCornerShape(50)).background(Color.White))
    Spacer(Modifier.width(6.dp))
    Text("LIVE", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold), color = Color.White)
}

@Composable
fun Pill(text: String, bg: Color, fg: Color) = Text(
    text,
    style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
    color = fg,
    modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(bg).padding(horizontal = 8.dp, vertical = 2.dp),
)

/** Minutes-since-epoch → "HH:MM" (tabular digits come from the font; keep strings short). */
fun formatClock(epochMin: Long): String {
    val m = ((epochMin % 1440) + 1440) % 1440
    return "%02d:%02d".format(m / 60, m % 60)
}
