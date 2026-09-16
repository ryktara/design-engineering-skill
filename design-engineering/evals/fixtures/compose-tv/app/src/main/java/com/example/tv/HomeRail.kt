package com.example.tv
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRestorer
@Composable fun HomeRail() { val fr = remember { FocusRequester() }; LazyRow(Modifier.focusRestorer()) { } }
