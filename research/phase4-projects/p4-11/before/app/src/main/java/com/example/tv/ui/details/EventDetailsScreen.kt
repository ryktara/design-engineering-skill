package com.example.tv.ui.details

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.tv.material3.Border
import androidx.tv.material3.Button
import androidx.tv.material3.ButtonDefaults
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.example.tv.data.EventStatus
import com.example.tv.data.SportsEvent
import com.example.tv.ui.home.LiveBadge
import com.example.tv.ui.home.formatClock
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.SportsDimens

/**
 * Details: backdrop, title, one metadata line, ≤3-line synopsis, ≤4 actions in one row with first focus on
 * Watch/Play. BACK returns to Home (the caller restores focus to the tile that opened this screen).
 */
@Composable
fun EventDetailsScreen(event: SportsEvent, nowMin: Long, onWatch: () -> Unit, onBack: () -> Unit, modifier: Modifier = Modifier) {
    val playFr = remember { FocusRequester() }
    LaunchedEffect(event.id) { playFr.requestFocus() }
    BackHandler { onBack() }

    Box(modifier.fillMaxSize().background(SportsColors.canvas)) {
        AsyncImage(model = event.artUrl, contentDescription = null, modifier = Modifier.fillMaxWidth().fillMaxHeight(0.8f).align(Alignment.TopEnd))
        Box(Modifier.fillMaxSize().background(Brush.horizontalGradient(0f to SportsColors.canvas, 0.55f to SportsColors.canvas.copy(alpha = 0.8f), 1f to Color.Transparent)))
        Box(Modifier.fillMaxSize().background(Brush.verticalGradient(0.3f to Color.Transparent, 0.85f to SportsColors.canvas)))

        Column(
            Modifier.fillMaxSize().padding(horizontal = SportsDimens.safeH, vertical = SportsDimens.safeV),
            verticalArrangement = Arrangement.Bottom,
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (event.status == EventStatus.LIVE) { LiveBadge(); Spacer(Modifier.padding(6.dp)) }
                Text("${event.competition.name} · ${event.channel.name} · ${formatClock(event.startEpochMin)}–${formatClock(event.endEpochMin)}", style = MaterialTheme.typography.labelLarge, color = SportsColors.textSecondary)
            }
            Spacer(Modifier.height(8.dp))
            Text(event.title, style = MaterialTheme.typography.displayLarge, color = SportsColors.textPrimary, maxLines = 2, overflow = TextOverflow.Ellipsis)
            if (event.score != null || event.clock != null) {
                Spacer(Modifier.height(4.dp))
                Text(listOfNotNull(event.score, event.clock).joinToString("   "), style = MaterialTheme.typography.headlineMedium, color = SportsColors.textPrimary)
            }
            Spacer(Modifier.height(8.dp))
            Text(event.synopsis.ifBlank { "No description available." }, style = MaterialTheme.typography.bodyMedium, color = SportsColors.textSecondary, maxLines = 3, overflow = TextOverflow.Ellipsis, modifier = Modifier.fillMaxWidth(0.55f))
            Spacer(Modifier.height(24.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                DetailButton(text = when (event.status) { EventStatus.LIVE -> "Watch live"; EventStatus.UPCOMING -> "Set reminder"; EventStatus.REPLAY -> "Play" }, primary = true, onClick = onWatch, modifier = Modifier.focusRequester(playFr))
                if (event.status == EventStatus.LIVE) DetailButton(text = "Watch from start", primary = false, onClick = onWatch)
                DetailButton(text = "Add to favourites", primary = false, onClick = {})
            }
            Spacer(Modifier.height(SportsDimens.safeV))
        }
    }
}

@Composable
private fun DetailButton(text: String, primary: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.colors(
            containerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            contentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
            focusedContainerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            focusedContentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
        ),
        scale = ButtonDefaults.scale(focusedScale = SportsDimens.focusScale),
        border = ButtonDefaults.border(focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = RoundedCornerShape(50))),
    ) { Text(text, style = MaterialTheme.typography.labelLarge) }
}
