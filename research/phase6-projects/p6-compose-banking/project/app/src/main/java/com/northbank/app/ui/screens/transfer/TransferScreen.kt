package com.northbank.app.ui.screens.transfer

import android.widget.Toast
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.northbank.app.R
import com.northbank.app.data.AccountRepository
import com.northbank.app.ui.components.NbButton
import com.northbank.app.ui.components.NbCard
import com.northbank.app.ui.theme.Spacing
import com.northbank.app.util.Money

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TransferScreen(
    repository: AccountRepository,
    viewModel: TransferViewModel = viewModel(factory = TransferViewModel.Factory(repository)),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val keyboard = LocalSoftwareKeyboardController.current
    val sentMessage = stringResource(R.string.transfer_sent)

    LaunchedEffect(viewModel) {
        viewModel.events.collect { event ->
            when (event) {
                is TransferEvent.Error ->
                    Toast.makeText(context, event.message, Toast.LENGTH_SHORT).show()
                TransferEvent.Sent ->
                    Toast.makeText(context, sentMessage, Toast.LENGTH_SHORT).show()
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.transfer_title)) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                ),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .imePadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = Spacing.screen, vertical = Spacing.sm),
        ) {
            NbCard {
                Text(
                    text = stringResource(R.string.transfer_from),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(Spacing.sm))
                AccountPicker(
                    accounts = state.accounts,
                    selectedId = state.fromAccountId,
                    onSelected = viewModel::onFromAccountSelected,
                )
            }

            Spacer(Modifier.height(Spacing.lg))

            NbCard {
                Text(
                    text = stringResource(R.string.transfer_to),
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(Spacing.sm))
                PayeePicker(
                    payees = state.payees,
                    selectedId = state.payeeId,
                    onSelected = viewModel::onPayeeSelected,
                )

                Spacer(Modifier.height(Spacing.lg))

                OutlinedTextField(
                    value = state.amountInput,
                    onValueChange = viewModel::onAmountChanged,
                    label = { Text(stringResource(R.string.transfer_amount)) },
                    prefix = { Text("£") },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Decimal,
                        imeAction = ImeAction.Next,
                    ),
                    modifier = Modifier.fillMaxWidth(),
                )

                Spacer(Modifier.height(Spacing.lg))

                OutlinedTextField(
                    value = state.reference,
                    onValueChange = viewModel::onReferenceChanged,
                    label = { Text(stringResource(R.string.transfer_reference)) },
                    placeholder = { Text(stringResource(R.string.transfer_reference_hint)) },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                    keyboardActions = KeyboardActions(onDone = { keyboard?.hide() }),
                    modifier = Modifier.fillMaxWidth(),
                )
            }

            Spacer(Modifier.height(Spacing.xxl))

            NbButton(
                text = stringResource(R.string.transfer_send),
                onClick = viewModel::submit,
                enabled = !state.submitting,
                modifier = Modifier.fillMaxWidth(),
            )

            Spacer(Modifier.height(Spacing.lg))
        }
    }
}

@Composable
private fun AccountPicker(
    accounts: List<com.northbank.app.data.model.Account>,
    selectedId: String?,
    onSelected: (String) -> Unit,
) {
    var expanded by remember { mutableStateOf(false) }
    val selected = accounts.firstOrNull { it.id == selectedId }

    OutlinedTextField(
        value = selected?.let { "${it.name} · ${Money.format(it.available)}" } ?: "",
        onValueChange = {},
        readOnly = true,
        singleLine = true,
        trailingIcon = {
            Icon(Icons.Filled.ArrowDropDown, contentDescription = null)
        },
        modifier = Modifier.fillMaxWidth(),
    )
    // Clicking a read-only field doesn't open the menu; the drop-down icon does.
    androidx.compose.foundation.layout.Box {
        androidx.compose.material3.TextButton(onClick = { expanded = true }) {
            Text(if (selected == null) "Choose account" else "Change")
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            accounts.forEach { account ->
                DropdownMenuItem(
                    text = { Text("${account.name} · ${Money.format(account.available)}") },
                    onClick = {
                        onSelected(account.id)
                        expanded = false
                    },
                )
            }
        }
    }
}

@Composable
private fun PayeePicker(
    payees: List<com.northbank.app.data.model.Payee>,
    selectedId: String?,
    onSelected: (String) -> Unit,
) {
    var expanded by remember { mutableStateOf(false) }
    val selected = payees.firstOrNull { it.id == selectedId }

    OutlinedTextField(
        value = selected?.let { "${it.displayName} · ${it.sortCode} ${it.accountNumber}" } ?: "",
        onValueChange = {},
        readOnly = true,
        singleLine = true,
        placeholder = { Text(stringResource(R.string.transfer_choose_payee)) },
        trailingIcon = {
            Icon(Icons.Filled.ArrowDropDown, contentDescription = null)
        },
        modifier = Modifier.fillMaxWidth(),
    )
    androidx.compose.foundation.layout.Box {
        androidx.compose.material3.TextButton(onClick = { expanded = true }) {
            Text(if (selected == null) stringResource(R.string.transfer_choose_payee) else "Change")
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            payees.forEach { payee ->
                DropdownMenuItem(
                    text = { Text(payee.displayName) },
                    onClick = {
                        onSelected(payee.id)
                        expanded = false
                    },
                )
            }
        }
    }
}
