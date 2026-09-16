package com.northbank.app.data.model

import java.math.BigDecimal
import java.time.LocalDate

enum class TransactionCategory {
    GROCERIES,
    TRANSPORT,
    EATING_OUT,
    BILLS,
    SALARY,
    TRANSFER,
    SHOPPING,
    ENTERTAINMENT,
    OTHER,
}

data class Transaction(
    val id: String,
    val accountId: String,
    val merchant: String,
    val amount: BigDecimal,
    val date: LocalDate,
    val category: TransactionCategory = TransactionCategory.OTHER,
    val pending: Boolean = false,
    val reference: String? = null,
) {
    val isCredit: Boolean
        get() = amount.signum() > 0
}
