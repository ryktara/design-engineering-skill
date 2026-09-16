package com.northbank.app.ui.navigation

import androidx.annotation.StringRes
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBalanceWallet
import androidx.compose.material.icons.filled.CreditCard
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.outlined.AccountBalanceWallet
import androidx.compose.material.icons.outlined.CreditCard
import androidx.compose.material.icons.outlined.MoreHoriz
import androidx.compose.material.icons.outlined.Send
import androidx.compose.ui.graphics.vector.ImageVector
import com.northbank.app.R

object Routes {
    const val ACCOUNTS = "accounts"
    const val ACCOUNT_DETAIL = "accounts/{accountId}"
    const val PAY = "pay"
    const val CARDS = "cards"
    const val MORE = "more"

    fun accountDetail(accountId: String) = "accounts/$accountId"
}

enum class BottomTab(
    val route: String,
    @StringRes val labelRes: Int,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
) {
    Accounts(
        route = Routes.ACCOUNTS,
        labelRes = R.string.tab_accounts,
        selectedIcon = Icons.Filled.AccountBalanceWallet,
        unselectedIcon = Icons.Outlined.AccountBalanceWallet,
    ),
    Pay(
        route = Routes.PAY,
        labelRes = R.string.tab_pay,
        selectedIcon = Icons.Filled.Send,
        unselectedIcon = Icons.Outlined.Send,
    ),
    Cards(
        route = Routes.CARDS,
        labelRes = R.string.tab_cards,
        selectedIcon = Icons.Filled.CreditCard,
        unselectedIcon = Icons.Outlined.CreditCard,
    ),
    More(
        route = Routes.MORE,
        labelRes = R.string.tab_more,
        selectedIcon = Icons.Filled.MoreHoriz,
        unselectedIcon = Icons.Outlined.MoreHoriz,
    ),
}
