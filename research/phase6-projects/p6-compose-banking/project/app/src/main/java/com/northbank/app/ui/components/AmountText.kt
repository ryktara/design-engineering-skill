package com.northbank.app.ui.components

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import com.northbank.app.ui.theme.PositiveGreen
import com.northbank.app.util.Money
import java.math.BigDecimal

/**
 * Monetary value rendered with tabular (monospaced) figures so columns of
 * amounts line up in lists.
 */
@Composable
fun AmountText(
    amount: BigDecimal,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyLarge,
    signed: Boolean = false,
    colorCredits: Boolean = false,
    currency: String = "GBP",
) {
    val color: Color = when {
        colorCredits && amount.signum() > 0 -> PositiveGreen
        else -> Color.Unspecified
    }

    Text(
        text = Money.format(amount, currency = currency, signed = signed),
        modifier = modifier,
        style = style.copy(fontFeatureSettings = "tnum"),
        color = color,
        maxLines = 1,
    )
}
