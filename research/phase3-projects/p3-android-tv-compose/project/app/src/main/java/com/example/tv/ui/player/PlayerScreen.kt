package com.example.tv.ui.player

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.focusable
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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.focusRestorer
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onKeyEvent
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.paneTitle
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.tv.material3.Border
import androidx.tv.material3.Button
import androidx.tv.material3.ButtonDefaults
import androidx.tv.material3.Icon
import androidx.tv.material3.ListItem
import androidx.tv.material3.ListItemDefaults
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.example.tv.data.EventStatus
import com.example.tv.data.MediaTrack
import com.example.tv.data.SportsEvent
import com.example.tv.data.TrackList
import com.example.tv.data.TrackSelection
import com.example.tv.ui.PlaybackPrefs
import com.example.tv.ui.home.LiveBadge
import com.example.tv.ui.theme.LocalReducedMotion
import com.example.tv.ui.theme.SportsColors
import com.example.tv.ui.theme.SportsDimens
import kotlinx.coroutines.delay

/**
 * Full-screen player (comp-player-controls + layout-split-player + tv-player-controls).
 *
 * Picture: Media3 PlayerView in an AndroidView fills the screen (the poster stands in here). Everything else is a
 * Compose overlay in three layers:
 *   1. transport overlay — title block top-left, seek bar + control row bottom-left, both inside the safe area,
 *      over a top/bottom scrim. Shown on entry and on any D-pad key; hides after [SportsDimens.playerAutoHideMs]
 *      without input, but never while paused or while the track sheet is open. First focus lands on Play/pause.
 *   2. track sheet — [TrackSheet] on the right ([SportsDimens.trackSheetW]); the left of the picture stays visible.
 *      Opened by the "Subtitles & audio" control; default focus on the current subtitle row; LEFT/RIGHT between
 *      the Subtitles and Audio columns, UP/DOWN inside a column; SELECT applies at once (the check mark moves, the
 *      summary line under the controls updates) and the sheet stays open so the other column can be changed too.
 *   3. keys — MEDIA_PLAY_PAUSE toggles without showing the overlay; DPAD_CENTER on the bare picture shows the
 *      controls (Leanback convention; it never toggles playback blind). The key that reveals the overlay is consumed.
 *
 * BACK layering (tv-back-behavior): sheet → closes it, focus returns to the "Subtitles & audio" control · otherwise
 * BACK leaves the player whether or not the overlay is showing (the app's existing contract, "player → home";
 * SportsApp puts the stream in the mini player). The overlay is only ever dismissed by the timer.
 *
 * The current choice is remembered per language in [PlaybackPrefs] so the next match starts with the same
 * subtitles/audio when the broadcaster carries them.
 */
@Composable
fun PlayerScreen(
    event: SportsEvent,
    startAtMin: Int?,
    nowMin: Long,
    tracks: TrackList,
    prefs: PlaybackPrefs,
    onBack: (watchedMin: Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    val live = event.status == EventStatus.LIVE
    val durationSec = event.durationMin * 60
    val liveEdgeSec = if (live) ((nowMin - event.startEpochMin).coerceIn(0, event.durationMin.toLong()) * 60).toInt() else durationSec
    var positionSec by remember(event.id) { mutableIntStateOf(if (startAtMin != null) startAtMin * 60 else if (live) liveEdgeSec else 0) }
    var paused by remember(event.id) { mutableStateOf(false) }
    var overlayVisible by remember(event.id) { mutableStateOf(true) }
    var sheetOpen by remember(event.id) { mutableStateOf(false) }
    var sheetOpenedOnce by remember(event.id) { mutableStateOf(false) }
    var selection by remember(event.id) { mutableStateOf(prefs.selectionFor(tracks)) }
    var inputTick by remember { mutableIntStateOf(0) }   // bumped on every key so the auto-hide timer restarts

    val rootFr = remember { FocusRequester() }
    val playFr = remember { FocusRequester() }
    val tracksFr = remember { FocusRequester() }

    // Auto-hide: 4 s after the last key, unless paused or the sheet is open (never hide while a menu is open).
    LaunchedEffect(overlayVisible, sheetOpen, paused, inputTick) {
        if (overlayVisible && !sheetOpen && !paused) { delay(SportsDimens.playerAutoHideMs); overlayVisible = false }
    }
    // Deterministic focus per layer: overlay → Play/pause; bare picture → the root (so keys still arrive);
    // sheet closing → back to the control that opened it.
    LaunchedEffect(overlayVisible) { runCatching { if (overlayVisible) playFr.requestFocus() else rootFr.requestFocus() } }
    LaunchedEffect(sheetOpen) { if (!sheetOpen && sheetOpenedOnce && overlayVisible) runCatching { tracksFr.requestFocus() } }

    BackHandler {
        if (sheetOpen) sheetOpen = false else onBack(positionSec / 60)
    }

    fun seek(deltaSec: Int) { positionSec = (positionSec + deltaSec).coerceIn(0, liveEdgeSec) }

    Box(
        modifier
            .fillMaxSize()
            .background(Color.Black)
            .focusRequester(rootFr)
            .focusable()
            .onPreviewKeyEvent { ev ->
                if (ev.type != KeyEventType.KeyDown) return@onPreviewKeyEvent false
                when (ev.key) {
                    // Media keys work without showing the overlay.
                    Key.MediaPlayPause, Key.MediaPlay, Key.MediaPause -> {
                        paused = !paused; inputTick++
                        if (paused) overlayVisible = true   // a paused picture shows its state; resuming needs no overlay
                        true
                    }
                    Key.Back -> false   // BackHandler above decides which layer closes
                    else -> {
                        inputTick++
                        if (!overlayVisible) { overlayVisible = true; true } else false
                    }
                }
            },
    ) {
        // Real app: AndroidView { PlayerView(context).apply { useController = false } } bound to the ExoPlayer.
        AsyncImage(model = event.artUrl, contentDescription = null, modifier = Modifier.fillMaxSize())

        if (overlayVisible) {
            TransportOverlay(
                event = event,
                live = live,
                paused = paused,
                positionSec = positionSec,
                durationSec = durationSec,
                liveEdgeSec = liveEdgeSec,
                tracks = tracks,
                selection = selection,
                playFr = playFr,
                tracksFr = tracksFr,
                onTogglePause = { paused = !paused },
                onSeek = ::seek,
                onOpenTracks = { sheetOpenedOnce = true; sheetOpen = true },
            )
        }
        if (sheetOpen) {
            TrackSheet(
                tracks = tracks,
                selection = selection,
                onSelectSubtitle = { track ->
                    selection = selection.copy(subtitleId = track?.id); prefs.rememberSubtitle(track)
                    // Real app: player.trackSelectionParameters = ...buildUpon().setOverrideForType(...) / setTrackTypeDisabled(TEXT, track == null)
                },
                onSelectAudio = { track -> selection = selection.copy(audioId = track.id); prefs.rememberAudio(track) },
                modifier = Modifier.align(Alignment.CenterEnd),
            )
        }
    }
}

@Composable
private fun TransportOverlay(
    event: SportsEvent,
    live: Boolean,
    paused: Boolean,
    positionSec: Int,
    durationSec: Int,
    liveEdgeSec: Int,
    tracks: TrackList,
    selection: TrackSelection,
    playFr: FocusRequester,
    tracksFr: FocusRequester,
    onTogglePause: () -> Unit,
    onSeek: (Int) -> Unit,
    onOpenTracks: () -> Unit,
) {
    val behindLive = live && liveEdgeSec - positionSec >= SportsDimens.playerSeekStepSec
    Box(Modifier.fillMaxSize()) {
        // Dual scrim so the title block and the control row read on any picture; the middle stays clear.
        Box(Modifier.fillMaxWidth().height(200.dp).align(Alignment.TopCenter).background(Brush.verticalGradient(0f to SportsColors.canvas.copy(alpha = 0.85f), 1f to Color.Transparent)))
        Box(Modifier.fillMaxWidth().height(260.dp).align(Alignment.BottomCenter).background(Brush.verticalGradient(0f to Color.Transparent, 1f to SportsColors.canvas.copy(alpha = 0.92f))))

        Column(Modifier.align(Alignment.TopStart).padding(start = SportsDimens.safeH, top = SportsDimens.safeV, end = SportsDimens.safeH)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                if (live) LiveBadge()
                Text("${event.competition.name} · ${event.channel.number} ${event.channel.name}", style = MaterialTheme.typography.labelLarge, color = SportsColors.textSecondary)
            }
            Spacer(Modifier.height(4.dp))
            Text(event.title, style = MaterialTheme.typography.headlineMedium, color = SportsColors.textPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.fillMaxWidth(0.7f).semantics { heading() })
            if (event.score != null || event.clock != null) {
                Text(listOfNotNull(event.score, event.clock).joinToString("   "), style = MaterialTheme.typography.titleLarge, color = SportsColors.textPrimary)
            }
        }

        Column(
            Modifier.align(Alignment.BottomStart).fillMaxWidth().padding(start = SportsDimens.safeH, end = SportsDimens.safeH, bottom = SportsDimens.safeV),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            SeekBar(positionSec = positionSec, durationSec = durationSec, liveEdgeSec = liveEdgeSec, live = live, onSeek = onSeek)
            // Controls: reserve the 1.08 focus lift at the safe edges (same as the details action row).
            Row(
                Modifier.padding(start = SportsDimens.focusPadding, bottom = SportsDimens.focusPadding / 2).focusRestorer(),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                // Text state, never an icon alone: TalkBack reads "Pause, button" / "Play, button".
                PlayerButton(if (paused) "Play" else "Pause", primary = true, onClick = onTogglePause, modifier = Modifier.focusRequester(playFr))
                PlayerButton("−${SportsDimens.playerSeekStepSec} s", primary = false, onClick = { onSeek(-SportsDimens.playerSeekStepSec) })
                if (live) {
                    // Always focusable: a disabled button would vanish from the D-pad path while still being visible.
                    // At the live edge SELECT is a no-op and the seek readout already says LIVE.
                    PlayerButton("Go to live", primary = false, onClick = { if (behindLive) onSeek(liveEdgeSec) })
                } else {
                    PlayerButton("+${SportsDimens.playerSeekStepSec} s", primary = false, onClick = { onSeek(SportsDimens.playerSeekStepSec) })
                }
                Spacer(Modifier.width(16.dp))
                PlayerButton("Subtitles & audio", primary = false, onClick = onOpenTracks, modifier = Modifier.focusRequester(tracksFr))
                // Current choice, always visible in text next to the control that changes it. It takes the remaining
                // width and ellipsises, so the pills never wrap or push past the safe edge.
                Text(trackSummary(tracks, selection), style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
            }
        }
    }
}

/** "Subtitles off · English 5.1" — what the picture is doing right now, for the overlay and for TalkBack. */
internal fun trackSummary(tracks: TrackList, selection: TrackSelection): String {
    val sub = tracks.subtitles.firstOrNull { it.id == selection.subtitleId }
    val audio = tracks.audio.firstOrNull { it.id == selection.audioId }
    val subText = if (sub == null) "Subtitles off" else "Subtitles ${sub.label}"
    val audioText = audio?.let { listOfNotNull(it.label, it.detail).joinToString(" ") } ?: ""
    return listOf(subText, audioText).filter { it.isNotBlank() }.joinToString(" · ")
}

/**
 * Focusable progress bar with remote semantics: LEFT/RIGHT seek [SportsDimens.playerSeekStepSec]; the elapsed time
 * and the total (or LIVE) are text at both ends; focus = the white ring around the track (no scale on a full-width bar).
 */
@Composable
private fun SeekBar(positionSec: Int, durationSec: Int, liveEdgeSec: Int, live: Boolean, onSeek: (Int) -> Unit) {
    var focused by remember { mutableStateOf(false) }
    val fraction = if (durationSec == 0) 0f else positionSec / durationSec.toFloat()
    val liveFraction = if (durationSec == 0) 0f else liveEdgeSec / durationSec.toFloat()
    val readout = "${formatTime(positionSec)} of ${formatTime(durationSec)}${if (live) ", live broadcast" else ""}"
    Row(
        Modifier
            .fillMaxWidth()
            .onFocusChanged { focused = it.isFocused }
            .focusable()
            .onKeyEvent { ev ->
                if (ev.type != KeyEventType.KeyDown) return@onKeyEvent false
                when (ev.key) {
                    Key.DirectionLeft -> { onSeek(-SportsDimens.playerSeekStepSec); true }
                    Key.DirectionRight -> { onSeek(SportsDimens.playerSeekStepSec); true }
                    else -> false
                }
            }
            .semantics(mergeDescendants = true) { contentDescription = "Position $readout. Left and right seek ${SportsDimens.playerSeekStepSec} seconds" },
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(formatTime(positionSec), style = MaterialTheme.typography.labelLarge, color = SportsColors.textPrimary)
        // Track grows from 8 to 14 dp when focused and takes the white ring; accent = elapsed, faint white = buffered live edge.
        Box(
            Modifier
                .weight(1f)
                .height(if (focused) 14.dp else 8.dp)
                .clip(RoundedCornerShape(50))
                .background(Color.White.copy(alpha = 0.35f)),
        ) {
            if (live) Box(Modifier.fillMaxWidth(liveFraction).fillMaxHeight().background(Color.White.copy(alpha = 0.25f)))
            Box(Modifier.fillMaxWidth(fraction).fillMaxHeight().background(SportsColors.accent))
            if (focused) Box(Modifier.fillMaxSize().border(SportsDimens.focusBorder, SportsColors.focusRing, RoundedCornerShape(50)))
        }
        Text(
            if (live && liveEdgeSec - positionSec < SportsDimens.playerSeekStepSec) "LIVE" else if (live) "−${formatTime(liveEdgeSec - positionSec)}" else formatTime(durationSec),
            style = MaterialTheme.typography.labelLarge,
            color = if (live) SportsColors.live else SportsColors.textPrimary,
        )
    }
}

/** Same pill treatment as the hero/details buttons: accent primary, elevated secondary, white ring + scale on focus. */
@Composable
private fun PlayerButton(text: String, primary: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.colors(
            containerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            contentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
            focusedContainerColor = if (primary) SportsColors.accent else SportsColors.elevated,
            focusedContentColor = if (primary) SportsColors.onAction else SportsColors.textPrimary,
        ),
        scale = ButtonDefaults.scale(focusedScale = if (LocalReducedMotion.current) 1f else SportsDimens.focusScale),
        border = ButtonDefaults.border(focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = RoundedCornerShape(50))),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 28.dp, vertical = 12.dp),
    ) { Text(text, style = MaterialTheme.typography.labelLarge) }
}

/**
 * Side sheet with two radio-style columns (tv-player-controls: "subtitle/audio pickers are side sheets that keep
 * playback visible"; comp-dialog: TV has no dialog — a composable with a focusRequester). Selected ≠ focused:
 * the current track has the selection fill + a check glyph + "Selected" in semantics; the focused row has the white
 * ring. Default focus is the current subtitle row (or "Off"). LEFT/RIGHT cross between the columns (Compose 2-D
 * focus search), each column remembers its last row (focusRestorer). Streams without subtitles show "Off" only
 * plus a text explanation, so the column is never blank.
 */
@Composable
private fun TrackSheet(
    tracks: TrackList,
    selection: TrackSelection,
    onSelectSubtitle: (MediaTrack?) -> Unit,
    onSelectAudio: (MediaTrack) -> Unit,
    modifier: Modifier = Modifier,
) {
    val initialFr = remember { FocusRequester() }
    LaunchedEffect(Unit) { runCatching { initialFr.requestFocus() } }
    Column(
        modifier
            .fillMaxHeight()
            .width(SportsDimens.trackSheetW)
            .background(SportsColors.surface.copy(alpha = 0.96f))
            .padding(start = 24.dp, end = SportsDimens.safeH, top = SportsDimens.safeV, bottom = SportsDimens.safeV)
            .semantics { paneTitle = "Subtitles and audio" },
    ) {
        Text("Subtitles & audio", style = MaterialTheme.typography.titleLarge, color = SportsColors.textPrimary, modifier = Modifier.semantics { heading() })
        Text("Applies straight away · BACK closes", style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary)
        Spacer(Modifier.height(20.dp))
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            TrackColumn(title = "Subtitles", modifier = Modifier.weight(1f)) {
                TrackRow(
                    label = "Off", detail = null, selected = selection.subtitleId == null,
                    onClick = { onSelectSubtitle(null) },
                    modifier = if (selection.subtitleId == null) Modifier.focusRequester(initialFr) else Modifier,
                )
                tracks.subtitles.forEach { t ->
                    TrackRow(
                        label = t.label, detail = t.detail, selected = selection.subtitleId == t.id,
                        onClick = { onSelectSubtitle(t) },
                        modifier = if (selection.subtitleId == t.id) Modifier.focusRequester(initialFr) else Modifier,
                    )
                }
                if (!tracks.hasSubtitles) {
                    Text("This broadcast has no subtitles.", style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary, modifier = Modifier.padding(start = 16.dp, top = 8.dp))
                }
            }
            TrackColumn(title = "Audio", modifier = Modifier.weight(1f)) {
                tracks.audio.forEach { t ->
                    TrackRow(label = t.label, detail = t.detail, selected = selection.audioId == t.id, onClick = { onSelectAudio(t) })
                }
            }
        }
    }
}

@Composable
private fun TrackColumn(title: String, modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Column(modifier.focusRestorer(), verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(title, style = MaterialTheme.typography.titleMedium, color = SportsColors.textPrimary, modifier = Modifier.padding(start = 16.dp, bottom = 8.dp).semantics { heading() })
        content()
    }
}

@Composable
private fun TrackRow(label: String, detail: String?, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(8.dp)
    ListItem(
        selected = selected,
        onClick = onClick,
        headlineContent = { Text(label, style = MaterialTheme.typography.labelLarge, maxLines = 1, overflow = TextOverflow.Ellipsis) },
        supportingContent = detail?.let { { Text(it, style = MaterialTheme.typography.labelMedium, color = SportsColors.textSecondary, maxLines = 1, overflow = TextOverflow.Ellipsis) } },
        trailingContent = {
            // The check is the selected state (with the fill and the semantics); a fixed-size slot so labels never shift.
            if (selected) Icon(Icons.Filled.Check, contentDescription = null, tint = SportsColors.accent, modifier = Modifier.size(28.dp)) else Spacer(Modifier.size(28.dp))
        },
        modifier = modifier
            .fillMaxWidth()
            .height(SportsDimens.trackRowH + if (detail != null) 12.dp else 0.dp)
            .semantics { role = Role.RadioButton; this.selected = selected; stateDescription = if (selected) "Selected" else "Not selected" },
        shape = ListItemDefaults.shape(shape = shape, focusedShape = shape, selectedShape = shape, focusedSelectedShape = shape),
        colors = ListItemDefaults.colors(
            containerColor = Color.Transparent, contentColor = SportsColors.textPrimary,
            focusedContainerColor = SportsColors.elevated, focusedContentColor = SportsColors.textPrimary,
            selectedContainerColor = SportsColors.selectionBg, selectedContentColor = SportsColors.textPrimary,
            focusedSelectedContainerColor = SportsColors.selectionBg, focusedSelectedContentColor = SportsColors.textPrimary,
        ),
        // No scale inside a dense list (it would clip neighbours); the 3 dp white ring is the focus at 3 m.
        scale = ListItemDefaults.scale(focusedScale = 1f, focusedSelectedScale = 1f),
        border = ListItemDefaults.border(
            focusedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = shape),
            focusedSelectedBorder = Border(androidx.compose.foundation.BorderStroke(SportsDimens.focusBorder, SportsColors.focusRing), shape = shape),
        ),
    )
}

/** Seconds → "1:07:12" / "07:12" (tabular digits from the font). */
internal fun formatTime(sec: Int): String {
    val s = sec.coerceAtLeast(0)
    val h = s / 3600; val m = (s % 3600) / 60; val r = s % 60
    return if (h > 0) "%d:%02d:%02d".format(h, m, r) else "%02d:%02d".format(m, r)
}
