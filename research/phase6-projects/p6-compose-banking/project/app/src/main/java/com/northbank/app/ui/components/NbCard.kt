package com.northbank.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.northbank.app.ui.theme.CardCornerRadius
import com.northbank.app.ui.theme.Spacing

/**
 * Outlined surface used for account tiles, card art wrappers and settings groups.
 * 12.dp corners, 1.dp outline, no elevation.
 */
@Composable
fun NbCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    contentPadding: androidx.compose.foundation.layout.PaddingValues =
        androidx.compose.foundation.layout.PaddingValues(Spacing.lg),
    content: @Composable ColumnScope.() -> Unit,
) {
    val shape = RoundedCornerShape(CardCornerRadius)
    val border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    val colors = CardDefaults.outlinedCardColors(
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface,
    )

    if (onClick != null) {
        OutlinedCard(
            onClick = onClick,
            modifier = modifier,
            shape = shape,
            border = border,
            colors = colors,
        ) {
            Column(modifier = Modifier.padding(contentPadding), content = content)
        }
    } else {
        OutlinedCard(
            modifier = modifier,
            shape = shape,
            border = border,
            colors = colors,
        ) {
            Column(modifier = Modifier.padding(contentPadding), content = content)
        }
    }
}
