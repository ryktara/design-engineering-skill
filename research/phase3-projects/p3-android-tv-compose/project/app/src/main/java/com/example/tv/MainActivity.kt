package com.example.tv

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.tv.ui.SportsApp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // No splash in the back stack; BACK from the side navigation finishes (no exit-confirmation loop).
        setContent { SportsApp(onExit = { finish() }) }
    }
}
