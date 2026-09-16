package com.northbank.app.ui.screens.transfer

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.northbank.app.data.AccountRepository
import com.northbank.app.data.TransferResult
import com.northbank.app.data.model.Account
import com.northbank.app.data.model.AccountType
import com.northbank.app.data.model.Payee
import com.northbank.app.util.Money
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class TransferUiState(
    val accounts: List<Account> = emptyList(),
    val payees: List<Payee> = emptyList(),
    val fromAccountId: String? = null,
    val payeeId: String? = null,
    val amountInput: String = "",
    val reference: String = "",
    val submitting: Boolean = false,
)

sealed class TransferEvent {
    data class Error(val message: String) : TransferEvent()
    data object Sent : TransferEvent()
}

class TransferViewModel(
    private val repository: AccountRepository,
) : ViewModel() {

    private val _state = MutableStateFlow(TransferUiState())
    val state: StateFlow<TransferUiState> = _state.asStateFlow()

    private val _events = MutableSharedFlow<TransferEvent>()
    val events: SharedFlow<TransferEvent> = _events.asSharedFlow()

    init {
        viewModelScope.launch {
            repository.accounts().collect { accounts ->
                val sources = accounts.filter { it.type != AccountType.CREDIT }
                _state.update { s ->
                    s.copy(
                        accounts = sources,
                        fromAccountId = s.fromAccountId ?: sources.firstOrNull()?.id,
                    )
                }
            }
        }
        viewModelScope.launch {
            repository.payees().collect { payees ->
                _state.update { it.copy(payees = payees) }
            }
        }
    }

    fun onFromAccountSelected(id: String) = _state.update { it.copy(fromAccountId = id) }
    fun onPayeeSelected(id: String) = _state.update { it.copy(payeeId = id) }
    fun onAmountChanged(value: String) = _state.update { it.copy(amountInput = value) }
    fun onReferenceChanged(value: String) = _state.update { it.copy(reference = value) }

    fun submit() {
        val s = _state.value
        val payeeId = s.payeeId
        val fromId = s.fromAccountId
        val amount = Money.parse(s.amountInput)

        viewModelScope.launch {
            if (payeeId == null) {
                _events.emit(TransferEvent.Error("Please choose a payee"))
                return@launch
            }
            if (fromId == null) {
                _events.emit(TransferEvent.Error("Please choose an account"))
                return@launch
            }
            if (amount == null || amount.signum() <= 0) {
                _events.emit(TransferEvent.Error("Enter a valid amount"))
                return@launch
            }

            _state.update { it.copy(submitting = true) }
            when (val result = repository.transfer(fromId, payeeId, amount, s.reference)) {
                is TransferResult.Success -> {
                    _state.update { it.copy(submitting = false, amountInput = "", reference = "", payeeId = null) }
                    _events.emit(TransferEvent.Sent)
                }
                is TransferResult.Failure -> {
                    _state.update { it.copy(submitting = false) }
                    _events.emit(TransferEvent.Error(result.reason))
                }
            }
        }
    }

    class Factory(private val repository: AccountRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            return TransferViewModel(repository) as T
        }
    }
}
