package com.northbank.app.data.model

import java.math.BigDecimal

enum class AccountType(val label: String) {
    CURRENT("Current"),
    SAVINGS("Savings"),
    CREDIT("Credit card"),
}

data class Account(
    val id: String,
    val name: String,
    val type: AccountType,
    val sortCode: String,
    val accountNumber: String,
    val balance: BigDecimal,
    val available: BigDecimal = balance,
    val currency: String = "GBP",
) {
    val maskedNumber: String
        get() = "•••• " + accountNumber.takeLast(4)
}
