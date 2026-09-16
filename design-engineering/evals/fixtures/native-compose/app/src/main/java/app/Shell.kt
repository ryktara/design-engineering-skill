package app
@Composable fun Shell() {
  Scaffold(bottomBar = { NavigationBar { NavigationBarItem(selected = true, onClick = {}, icon = {}, label = { Text("Home") }) } }) { padding ->
    Surface(modifier = Modifier.padding(padding), tonalElevation = 1.dp) { Column(Modifier.padding(16.dp)) { Text("Hello") } }
  }
}
