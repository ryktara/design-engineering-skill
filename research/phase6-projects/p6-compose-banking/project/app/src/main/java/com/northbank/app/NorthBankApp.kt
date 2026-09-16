package com.northbank.app

import android.app.Application
import com.northbank.app.data.AccountRepository
import com.northbank.app.data.FakeAccountRepository

class NorthBankApp : Application() {

    lateinit var repository: AccountRepository
        private set

    override fun onCreate() {
        super.onCreate()
        // Swapped for the network-backed repository in the `prod` flavor.
        repository = FakeAccountRepository()
    }
}
