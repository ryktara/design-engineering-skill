package com.northbank.app.data

import com.northbank.app.data.model.Account
import com.northbank.app.data.model.AccountType
import com.northbank.app.data.model.Card
import com.northbank.app.data.model.CardNetwork
import com.northbank.app.data.model.Payee
import com.northbank.app.data.model.Transaction
import com.northbank.app.data.model.TransactionCategory
import java.math.BigDecimal
import java.time.LocalDate

/**
 * Deterministic fixture data used by [FakeAccountRepository], previews and UI tests.
 * Dates are fixed so screenshots are stable across runs.
 */
object SampleData {

    private val baseDate: LocalDate = LocalDate.of(2025, 3, 14)

    val accounts: List<Account> = listOf(
        Account(
            id = "acc_current",
            name = "Everyday Current",
            type = AccountType.CURRENT,
            sortCode = "40-11-27",
            accountNumber = "31842970",
            balance = BigDecimal("2418.63"),
            available = BigDecimal("2368.63"),
        ),
        Account(
            id = "acc_savings",
            name = "Rainy Day Saver",
            type = AccountType.SAVINGS,
            sortCode = "40-11-27",
            accountNumber = "31842988",
            balance = BigDecimal("12750.00"),
        ),
        Account(
            id = "acc_credit",
            name = "NorthBank Rewards Credit",
            type = AccountType.CREDIT,
            sortCode = "40-11-27",
            accountNumber = "55019034",
            balance = BigDecimal("-486.20"),
            available = BigDecimal("4513.80"),
        ),
        Account(
            id = "acc_holiday",
            name = "Holiday Pot",
            type = AccountType.SAVINGS,
            sortCode = "40-11-27",
            accountNumber = "31843001",
            balance = BigDecimal("0.00"),
        ),
    )

    val transactions: List<Transaction> = listOf(
        Transaction("tx_001", "acc_current", "Tesco Express", BigDecimal("-23.47"), baseDate, TransactionCategory.GROCERIES, pending = true),
        Transaction("tx_002", "acc_current", "TfL Travel", BigDecimal("-6.80"), baseDate, TransactionCategory.TRANSPORT, pending = true),
        Transaction("tx_003", "acc_current", "Pret A Manger", BigDecimal("-9.15"), baseDate.minusDays(1), TransactionCategory.EATING_OUT),
        Transaction("tx_004", "acc_current", "Octopus Energy", BigDecimal("-112.00"), baseDate.minusDays(2), TransactionCategory.BILLS, reference = "DD ENERGY"),
        Transaction("tx_005", "acc_current", "Amazon.co.uk", BigDecimal("-34.99"), baseDate.minusDays(3), TransactionCategory.SHOPPING),
        Transaction("tx_006", "acc_current", "Spotify", BigDecimal("-10.99"), baseDate.minusDays(4), TransactionCategory.ENTERTAINMENT),
        Transaction("tx_007", "acc_current", "Transfer to Rainy Day Saver", BigDecimal("-250.00"), baseDate.minusDays(5), TransactionCategory.TRANSFER, reference = "Monthly saving"),
        Transaction("tx_008", "acc_current", "Sainsbury's", BigDecimal("-61.23"), baseDate.minusDays(6), TransactionCategory.GROCERIES),
        Transaction("tx_009", "acc_current", "Meridian Software Ltd", BigDecimal("3120.00"), baseDate.minusDays(14), TransactionCategory.SALARY, reference = "SALARY FEB"),
        Transaction("tx_010", "acc_current", "Thames Water", BigDecimal("-38.50"), baseDate.minusDays(15), TransactionCategory.BILLS),
        Transaction("tx_011", "acc_current", "Dishoom", BigDecimal("-58.40"), baseDate.minusDays(16), TransactionCategory.EATING_OUT),
        Transaction("tx_012", "acc_current", "Uber", BigDecimal("-14.62"), baseDate.minusDays(17), TransactionCategory.TRANSPORT),

        Transaction("tx_020", "acc_savings", "Transfer from Everyday Current", BigDecimal("250.00"), baseDate.minusDays(5), TransactionCategory.TRANSFER, reference = "Monthly saving"),
        Transaction("tx_021", "acc_savings", "Interest", BigDecimal("31.88"), baseDate.minusDays(13), TransactionCategory.OTHER),
        Transaction("tx_022", "acc_savings", "Transfer from Everyday Current", BigDecimal("250.00"), baseDate.minusDays(36), TransactionCategory.TRANSFER, reference = "Monthly saving"),

        Transaction("tx_030", "acc_credit", "British Airways", BigDecimal("-312.20"), baseDate.minusDays(8), TransactionCategory.TRANSPORT),
        Transaction("tx_031", "acc_credit", "John Lewis", BigDecimal("-174.00"), baseDate.minusDays(11), TransactionCategory.SHOPPING),
        Transaction("tx_032", "acc_credit", "Payment received - thank you", BigDecimal("500.00"), baseDate.minusDays(20), TransactionCategory.TRANSFER),
    )

    val cards: List<Card> = listOf(
        Card(
            id = "card_debit",
            accountId = "acc_current",
            holderName = "A. J. WHITFIELD",
            lastFour = "4471",
            expiry = "09/27",
            network = CardNetwork.VISA,
        ),
        Card(
            id = "card_credit",
            accountId = "acc_credit",
            holderName = "A. J. WHITFIELD",
            lastFour = "8830",
            expiry = "02/28",
            network = CardNetwork.MASTERCARD,
        ),
    )

    val payees: List<Payee> = listOf(
        Payee("payee_001", "Samira Khan", "20-45-19", "70023381", nickname = "Samira (rent)"),
        Payee("payee_002", "Daniel Osei", "30-98-12", "18832049"),
        Payee("payee_003", "Greenway Lettings Ltd", "60-12-88", "40015522", nickname = "Landlord"),
        Payee("payee_004", "Priya Natarajan", "09-01-27", "55211980"),
    )
}
