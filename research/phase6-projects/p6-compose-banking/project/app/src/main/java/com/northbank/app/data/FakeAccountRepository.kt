package com.northbank.app.data

import com.northbank.app.data.model.Account
import com.northbank.app.data.model.Card
import com.northbank.app.data.model.Payee
import com.northbank.app.data.model.Transaction
import com.northbank.app.data.model.TransactionCategory
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import java.math.BigDecimal
import java.time.LocalDate
import java.util.UUID

/**
 * In-memory repository seeded from [SampleData]. State survives for the process
 * lifetime only, which is what we want for demos and instrumentation tests.
 */
class FakeAccountRepository(
    private val simulatedLatencyMs: Long = 350L,
) : AccountRepository {

    private val accountsState = MutableStateFlow(SampleData.accounts)
    private val transactionsState = MutableStateFlow(SampleData.transactions)
    private val cardsState = MutableStateFlow(SampleData.cards)
    private val payeesState = MutableStateFlow(SampleData.payees)

    override fun accounts(): Flow<List<Account>> = accountsState

    override fun account(id: String): Flow<Account?> =
        accountsState.map { list -> list.firstOrNull { it.id == id } }

    override fun transactions(accountId: String): Flow<List<Transaction>> =
        transactionsState.map { list ->
            list.filter { it.accountId == accountId }
                .sortedWith(compareByDescending<Transaction> { it.pending }.thenByDescending { it.date })
        }

    override fun cards(): Flow<List<Card>> = cardsState

    override fun payees(): Flow<List<Payee>> = payeesState

    override suspend fun setCardFrozen(cardId: String, frozen: Boolean) {
        delay(simulatedLatencyMs)
        cardsState.update { cards ->
            cards.map { if (it.id == cardId) it.copy(frozen = frozen) else it }
        }
    }

    override suspend fun transfer(
        fromAccountId: String,
        payeeId: String,
        amount: BigDecimal,
        reference: String,
    ): TransferResult {
        delay(simulatedLatencyMs)

        val from = accountsState.value.firstOrNull { it.id == fromAccountId }
            ?: return TransferResult.Failure("Unknown account")
        val payee = payeesState.value.firstOrNull { it.id == payeeId }
            ?: return TransferResult.Failure("Unknown payee")

        if (amount.signum() <= 0) return TransferResult.Failure("Amount must be positive")
        if (amount > from.available) return TransferResult.Failure("Insufficient funds")

        accountsState.update { accounts ->
            accounts.map {
                if (it.id == fromAccountId) {
                    it.copy(balance = it.balance - amount, available = it.available - amount)
                } else {
                    it
                }
            }
        }

        transactionsState.update { txs ->
            txs + Transaction(
                id = "tx_" + UUID.randomUUID().toString().take(8),
                accountId = fromAccountId,
                merchant = payee.displayName,
                amount = amount.negate(),
                date = LocalDate.now(),
                category = TransactionCategory.TRANSFER,
                pending = true,
                reference = reference.ifBlank { null },
            )
        }

        return TransferResult.Success
    }
}
