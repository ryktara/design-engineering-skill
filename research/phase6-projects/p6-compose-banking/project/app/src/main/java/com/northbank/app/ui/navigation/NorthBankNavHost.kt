package com.northbank.app.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.northbank.app.data.AccountRepository
import com.northbank.app.ui.screens.accounts.AccountDetailScreen
import com.northbank.app.ui.screens.accounts.AccountsScreen
import com.northbank.app.ui.screens.cards.CardsScreen
import com.northbank.app.ui.screens.more.MoreScreen
import com.northbank.app.ui.screens.transfer.TransferScreen

@Composable
fun NorthBankApp(
    repository: AccountRepository,
    navController: NavHostController = rememberNavController(),
) {
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = backStackEntry?.destination

    Scaffold(
        bottomBar = {
            NorthBankBottomBar(
                currentDestination = currentDestination,
                onTabSelected = { tab ->
                    navController.navigate(tab.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                },
            )
        },
    ) { innerPadding ->
        NorthBankNavHost(
            navController = navController,
            repository = repository,
            modifier = Modifier.padding(innerPadding),
        )
    }
}

@Composable
fun NorthBankNavHost(
    navController: NavHostController,
    repository: AccountRepository,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = Routes.ACCOUNTS,
        modifier = modifier,
    ) {
        composable(Routes.ACCOUNTS) {
            AccountsScreen(
                repository = repository,
                onAccountClick = { accountId ->
                    navController.navigate(Routes.accountDetail(accountId))
                },
            )
        }

        composable(
            route = Routes.ACCOUNT_DETAIL,
            arguments = listOf(navArgument("accountId") { type = NavType.StringType }),
        ) { entry ->
            val accountId = requireNotNull(entry.arguments?.getString("accountId"))
            AccountDetailScreen(
                accountId = accountId,
                repository = repository,
                onBack = { navController.popBackStack() },
            )
        }

        composable(Routes.PAY) {
            TransferScreen(repository = repository)
        }

        composable(Routes.CARDS) {
            CardsScreen(repository = repository)
        }

        composable(Routes.MORE) {
            MoreScreen()
        }
    }
}
