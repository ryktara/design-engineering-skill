package com.northbank.app.data

import com.northbank.app.data.model.Account
import com.northbank.app.data.model.Card
import com.northbank.app.data.model.Payee
import com.northbank.app.data.model.Transaction
import kotlinx.coroutines.flow.Flow
import java.math.BigDecimal

sealed class TransferResult {
    data object Success : TransferResult()
    data class Failure(val reason: String) : TransferResult()
}

interface AccountRepository {
    fun accounts(): Flow<List<Account>>
    fun account(id: String): Flow<Account?>
    fun transactions(accountId: String): Flow<List<Transaction>>
    fun cards(): Flow<List<Card>>
    fun payees(): Flow<List<Payee>>

    suspend fun setCardFrozen(cardId: String, frozen: Boolean)

    suspend fun transfer(
        fromAccountId: String,
        payeeId: String,
        amount: BigDecimal,
        reference: String,
    ): TransferResult
}
