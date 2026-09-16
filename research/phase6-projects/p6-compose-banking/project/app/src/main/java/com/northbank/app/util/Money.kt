package com.northbank.app.util

import java.math.BigDecimal
import java.text.NumberFormat
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.util.Currency
import java.util.Locale

object Money {

    private val ukLocale = Locale.UK

    fun format(amount: BigDecimal, currency: String = "GBP", signed: Boolean = false): String {
        val nf = NumberFormat.getCurrencyInstance(ukLocale).apply {
            this.currency = Currency.getInstance(currency)
            minimumFractionDigits = 2
            maximumFractionDigits = 2
        }
        val formatted = nf.format(amount.abs())
        return when {
            amount.signum() < 0 -> "-$formatted"
            signed && amount.signum() > 0 -> "+$formatted"
            else -> formatted
        }
    }

    fun parse(input: String): BigDecimal? {
        val cleaned = input.trim().replace(",", "").removePrefix("£")
        if (cleaned.isEmpty()) return null
        return runCatching { BigDecimal(cleaned) }.getOrNull()
    }
}

object Dates {
    private val dayFormatter = DateTimeFormatter.ofPattern("d MMM", ukLocale())
    private val fullFormatter = DateTimeFormatter.ofPattern("EEEE d MMMM yyyy", ukLocale())

    private fun ukLocale() = Locale.UK

    fun short(date: LocalDate): String = date.format(dayFormatter)
    fun full(date: LocalDate): String = date.format(fullFormatter)
}
