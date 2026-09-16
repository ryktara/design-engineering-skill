package com.northbank.app.ui.screens.cards

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.northbank.app.R
import com.northbank.app.data.AccountRepository
import com.northbank.app.data.model.Card
import com.northbank.app.data.model.CardNetwork
import com.northbank.app.ui.components.NbCard
import com.northbank.app.ui.components.NbListRow
import com.northbank.app.ui.theme.CardCornerRadius
import com.northbank.app.ui.theme.Gold500
import com.northbank.app.ui.theme.Green500
import com.northbank.app.ui.theme.Green900
import com.northbank.app.ui.theme.Grey700
import com.northbank.app.ui.theme.Grey900
import com.northbank.app.ui.theme.Spacing
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CardsScreen(repository: AccountRepository) {
    val cards by repository.cards().collectAsStateWithLifecycle(initialValue = emptyList())
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.cards_title)) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                ),
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(horizontal = Spacing.screen, vertical = Spacing.sm),
            verticalArrangement = Arrangement.spacedBy(Spacing.xl),
        ) {
            items(cards, key = { it.id }) { card ->
                CardSection(
                    card = card,
                    repository = repository,
                    scope = scope,
                    snackbarHostState = snackbarHostState,
                )
            }
        }
    }
}

@Composable
private fun CardSection(
    card: Card,
    repository: AccountRepository,
    scope: CoroutineScope,
    snackbarHostState: SnackbarHostState,
) {
    // Target of an in-flight freeze/unfreeze; null when nothing is pending.
    var pendingTarget by remember(card.id) { mutableStateOf<Boolean?>(null) }
    var confirmVisible by remember(card.id) { mutableStateOf(false) }

    val displayedFrozen = pendingTarget ?: card.frozen
    val inFlight = pendingTarget != null

    val frozenLabel = stringResource(R.string.card_frozen)
    val activeLabel = stringResource(R.string.card_active)
    val freezingLabel = stringResource(R.string.card_freezing)
    val unfreezingLabel = stringResource(R.string.card_unfreezing)
    val freezeLabel = stringResource(R.string.card_freeze)
    val frozenDone = stringResource(R.string.card_freeze_done)
    val unfrozenDone = stringResource(R.string.card_unfreeze_done)
    val undoLabel = stringResource(R.string.action_undo)

    // One place that performs the change, reports the result and offers Undo.
    fun apply(target: Boolean, offerUndo: Boolean) {
        scope.launch {
            pendingTarget = target
            repository.setCardFrozen(card.id, target)
            pendingTarget = null
            val message = if (target) frozenDone else unfrozenDone
            val result = snackbarHostState.showSnackbar(
                message = message,
                actionLabel = if (offerUndo) undoLabel else null,
                withDismissAction = false,
                duration = SnackbarDuration.Short,
            )
            if (result == SnackbarResult.ActionPerformed) {
                apply(target = !target, offerUndo = false)
            }
        }
    }

    Column {
        CardArt(
            card = card,
            frozen = displayedFrozen,
            statusLabel = when {
                inFlight && displayedFrozen -> freezingLabel
                inFlight -> unfreezingLabel
                else -> frozenLabel
            },
        )
        Spacer(Modifier.height(Spacing.md))
        NbCard(contentPadding = PaddingValues(0.dp)) {
            NbListRow(
                title = freezeLabel,
                subtitle = when {
                    inFlight && displayedFrozen -> freezingLabel
                    inFlight -> unfreezingLabel
                    displayedFrozen -> frozenLabel
                    else -> activeLabel
                },
                trailing = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (inFlight) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            Spacer(Modifier.width(Spacing.md))
                        }
                        Switch(
                            checked = displayedFrozen,
                            enabled = !inFlight,
                            onCheckedChange = { requested ->
                                // Freezing stops payments: ask first. Unfreezing
                                // restores the normal state and applies directly.
                                if (requested) confirmVisible = true else apply(false, offerUndo = true)
                            },
                            modifier = Modifier.semantics {
                                contentDescription = freezeLabel
                                stateDescription = when {
                                    inFlight && displayedFrozen -> freezingLabel
                                    inFlight -> unfreezingLabel
                                    displayedFrozen -> frozenLabel
                                    else -> activeLabel
                                }
                            },
                        )
                    }
                },
            )
            NbListRow(
                title = stringResource(R.string.card_show_pin),
                onClick = { /* PIN reveal requires biometric; wired in NB-412 */ },
            )
            NbListRow(
                title = stringResource(R.string.card_report_lost),
                onClick = { /* deep-links to support flow */ },
                showDivider = false,
            )
        }
    }

    if (confirmVisible) {
        AlertDialog(
            onDismissRequest = { confirmVisible = false },
            title = { Text(stringResource(R.string.card_freeze_confirm_title)) },
            text = {
                Text(
                    text = stringResource(R.string.card_freeze_confirm_body, card.lastFour),
                    style = MaterialTheme.typography.bodyMedium,
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        confirmVisible = false
                        apply(target = true, offerUndo = true)
                    },
                ) {
                    Text(stringResource(R.string.card_freeze_confirm_action))
                }
            },
            dismissButton = {
                TextButton(onClick = { confirmVisible = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
            shape = MaterialTheme.shapes.large,
            containerColor = MaterialTheme.colorScheme.surface,
        )
    }
}

@Composable
private fun CardArt(card: Card, frozen: Boolean, statusLabel: String) {
    val gradient = when (card.network) {
        CardNetwork.VISA -> Brush.linearGradient(listOf(Green900, Green500))
        CardNetwork.MASTERCARD -> Brush.linearGradient(listOf(Grey900, Grey700))
    }
    // The wash dims the art; the status itself is carried by the "Frozen" label
    // below, so it stays light enough to keep the white card details legible.
    val frozenOverlay = if (frozen) Color.White.copy(alpha = 0.22f) else Color.Transparent

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1.586f)
            .clip(RoundedCornerShape(CardCornerRadius))
            .background(gradient)
            .background(frozenOverlay),
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(Spacing.xl),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "NorthBank",
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                )
                Spacer(Modifier.weight(1f))
                Box(
                    modifier = Modifier
                        .height(28.dp)
                        .aspectRatio(1.3f)
                        .clip(RoundedCornerShape(4.dp))
                        .background(Gold500),
                )
            }
            Spacer(Modifier.weight(1f))
            if (frozen) {
                // Status is not carried by the wash alone: it is also a label.
                Box(
                    modifier = Modifier
                        .clip(MaterialTheme.shapes.extraSmall)
                        .background(Grey900)
                        .padding(horizontal = Spacing.sm, vertical = Spacing.xs),
                ) {
                    Text(
                        text = statusLabel,
                        style = MaterialTheme.typography.labelMedium,
                        color = Color.White,
                    )
                }
                Spacer(Modifier.height(Spacing.md))
            }
            Text(
                text = "••••  ••••  ••••  ${card.lastFour}",
                style = MaterialTheme.typography.titleLarge.copy(fontFeatureSettings = "tnum"),
                color = Color.White,
            )
            Spacer(Modifier.height(Spacing.md))
            Row {
                Column {
                    Text(
                        text = stringResource(R.string.card_expires),
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.White.copy(alpha = 0.7f),
                    )
                    Text(
                        text = card.expiry,
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color.White,
                    )
                }
                Spacer(Modifier.weight(1f))
                Column(horizontalAlignment = Alignment.End) {
                    Text(
                        text = card.holderName,
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color.White,
                    )
                    Text(
                        text = card.network.label,
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.White.copy(alpha = 0.7f),
                    )
                }
            }
        }
    }
}
