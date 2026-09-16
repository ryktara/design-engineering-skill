package com.northbank.app.ui.screens.more

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.northbank.app.BuildConfig
import com.northbank.app.R
import com.northbank.app.ui.components.NbButton
import com.northbank.app.ui.components.NbButtonStyle
import com.northbank.app.ui.components.NbCard
import com.northbank.app.ui.components.NbListRow
import com.northbank.app.ui.theme.Spacing

private data class SettingsItem(
    val labelRes: Int,
    val icon: ImageVector,
)

private val accountItems = listOf(
    SettingsItem(R.string.more_profile, Icons.Outlined.Person),
    SettingsItem(R.string.more_security, Icons.Outlined.Lock),
    SettingsItem(R.string.more_notifications, Icons.Outlined.Notifications),
)

private val supportItems = listOf(
    SettingsItem(R.string.more_statements, Icons.Outlined.Description),
    SettingsItem(R.string.more_help, Icons.AutoMirrored.Filled.HelpOutline),
    SettingsItem(R.string.more_about, Icons.Outlined.Info),
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MoreScreen() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.more_title)) },
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
            item { SettingsGroup(items = accountItems) }
            item { SettingsGroup(items = supportItems) }
            item {
                NbButton(
                    text = stringResource(R.string.more_sign_out),
                    onClick = { /* handled by SessionManager */ },
                    style = NbButtonStyle.Secondary,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
            item {
                Text(
                    text = stringResource(R.string.more_version, BuildConfig.VERSION_NAME),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = Spacing.sm),
                )
            }
        }
    }
}

@Composable
private fun SettingsGroup(items: List<SettingsItem>) {
    NbCard(contentPadding = PaddingValues(0.dp)) {
        items.forEachIndexed { index, item ->
            NbListRow(
                title = stringResource(item.labelRes),
                leading = {
                    Icon(
                        imageVector = item.icon,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                },
                trailing = {
                    Icon(
                        imageVector = Icons.Filled.ChevronRight,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                },
                onClick = { /* navigation wired per item in NB-388 */ },
                showDivider = index < items.lastIndex,
            )
        }
    }
}
