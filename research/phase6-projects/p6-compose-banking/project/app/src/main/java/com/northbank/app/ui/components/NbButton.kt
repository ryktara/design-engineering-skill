package com.northbank.app.ui.components

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.northbank.app.ui.theme.Spacing

enum class NbButtonStyle { Primary, Secondary }

@Composable
fun NbButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    style: NbButtonStyle = NbButtonStyle.Primary,
    enabled: Boolean = true,
) {
    val contentPadding = PaddingValues(horizontal = Spacing.xl, vertical = Spacing.md)
    val shape = MaterialTheme.shapes.medium

    when (style) {
        NbButtonStyle.Primary -> Button(
            onClick = onClick,
            modifier = modifier.height(48.dp),
            enabled = enabled,
            shape = shape,
            contentPadding = contentPadding,
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
            ),
        ) {
            Text(text = text, style = MaterialTheme.typography.labelLarge)
        }

        NbButtonStyle.Secondary -> OutlinedButton(
            onClick = onClick,
            modifier = modifier.height(48.dp),
            enabled = enabled,
            shape = shape,
            contentPadding = contentPadding,
        ) {
            Text(text = text, style = MaterialTheme.typography.labelLarge)
        }
    }
}
