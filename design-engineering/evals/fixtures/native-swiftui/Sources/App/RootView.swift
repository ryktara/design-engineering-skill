import SwiftUI
struct RootView: View { var body: some View { TabView { NavigationStack { Text("Home") }.tabItem { Label("Home", systemImage: "house") }; NavigationStack { Text("Orders") }.tabItem { Label("Orders", systemImage: "list.bullet") } } } }
