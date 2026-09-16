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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
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
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CardsScreen(repository: AccountRepository) {
    val cards by repository.cards().collectAsStateWithLifecycle(initialValue = emptyList())
    val scope = rememberCoroutineScope()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.cards_title)) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                ),
            )
        },
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
                    onFreezeChanged = { frozen ->
                        scope.launch { repository.setCardFrozen(card.id, frozen) }
                    },
                )
            }
        }
    }
}

@Composable
private fun CardSection(
    card: Card,
    onFreezeChanged: (Boolean) -> Unit,
) {
    Column {
        CardArt(card = card)
        Spacer(Modifier.height(Spacing.md))
        NbCard(contentPadding = PaddingValues(0.dp)) {
            NbListRow(
                title = stringResource(R.string.card_freeze),
                subtitle = if (card.frozen) {
                    stringResource(R.string.card_frozen)
                } else {
                    stringResource(R.string.card_active)
                },
                trailing = {
                    Switch(
                        checked = card.frozen,
                        onCheckedChange = onFreezeChanged,
                    )
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
}

@Composable
private fun CardArt(card: Card) {
    val gradient = when (card.network) {
        CardNetwork.VISA -> Brush.linearGradient(listOf(Green900, Green500))
        CardNetwork.MASTERCARD -> Brush.linearGradient(listOf(Grey900, Grey700))
    }
    val frozenOverlay = if (card.frozen) Color.White.copy(alpha = 0.55f) else Color.Transparent

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
