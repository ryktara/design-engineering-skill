package com.northbank.app.ui.screens.accounts

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.northbank.app.R
import com.northbank.app.data.AccountRepository
import com.northbank.app.data.model.Account
import com.northbank.app.data.model.AccountType
import com.northbank.app.ui.components.AmountText
import com.northbank.app.ui.components.NbCard
import com.northbank.app.ui.theme.Spacing
import java.math.BigDecimal

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountsScreen(
    repository: AccountRepository,
    onAccountClick: (String) -> Unit,
) {
    val accounts by repository.accounts().collectAsStateWithLifecycle(initialValue = emptyList())

    val total = accounts
        .filter { it.type != AccountType.CREDIT }
        .fold(BigDecimal.ZERO) { acc, a -> acc + a.balance }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.accounts_title)) },
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
            verticalArrangement = Arrangement.spacedBy(Spacing.lg),
        ) {
            item {
                TotalBalanceCard(total = total)
            }
            item {
                NbCard(contentPadding = PaddingValues(0.dp)) {
                    accounts.forEachIndexed { index, account ->
                        AccountRow(
                            account = account,
                            onClick = { onAccountClick(account.id) },
                        )
                        if (index < accounts.lastIndex) {
                            HorizontalDivider(
                                modifier = Modifier.padding(start = Spacing.lg),
                                color = MaterialTheme.colorScheme.outlineVariant,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun TotalBalanceCard(total: BigDecimal) {
    NbCard {
        Text(
            text = stringResource(R.string.accounts_total_balance),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.height(Spacing.xs))
        AmountText(
            amount = total,
            style = MaterialTheme.typography.headlineLarge,
        )
    }
}

@Composable
private fun AccountRow(
    account: Account,
    onClick: () -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(40.dp)
            .clickable(onClick = onClick)
            .padding(horizontal = Spacing.lg),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = account.name,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
            )
            Text(
                text = "${account.type.label} · ${account.maskedNumber}",
                style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
            )
        }
        AmountText(
            amount = account.balance,
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}
