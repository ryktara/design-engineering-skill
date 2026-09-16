package com.northbank.app.data.model

enum class CardNetwork(val label: String) {
    VISA("Visa"),
    MASTERCARD("Mastercard"),
}

data class Card(
    val id: String,
    val accountId: String,
    val holderName: String,
    val lastFour: String,
    val expiry: String,
    val network: CardNetwork,
    val frozen: Boolean = false,
)

data class Payee(
    val id: String,
    val name: String,
    val sortCode: String,
    val accountNumber: String,
    val nickname: String? = null,
) {
    val displayName: String
        get() = nickname ?: name
}
