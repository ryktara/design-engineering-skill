import SwiftUI

@main
struct StreaksApp: App {
    @StateObject private var store = Store()
    private let theme = Theme.default

    init() {
        Self.configureAppearance(theme: theme)
    }

    var body: some Scene {
        WindowGroup {
            RootTabView()
                .environmentObject(store)
                .environment(\.theme, theme)
                .tint(theme.color.accent)
        }
    }

    /// UIKit-backed bars (tab bar, navigation bar) do not read SwiftUI environment,
    /// so the theme is pushed into their appearance proxies once at launch.
    private static func configureAppearance(theme: Theme) {
        let tabBar = UITabBarAppearance()
        tabBar.configureWithDefaultBackground()
        tabBar.backgroundColor = UIColor(theme.color.surface)
        tabBar.shadowColor = UIColor(theme.color.separator)
        UITabBar.appearance().standardAppearance = tabBar
        UITabBar.appearance().scrollEdgeAppearance = tabBar

        let navBar = UINavigationBarAppearance()
        navBar.configureWithTransparentBackground()
        navBar.backgroundColor = UIColor(theme.color.background)
        navBar.titleTextAttributes = [.foregroundColor: UIColor(theme.color.text)]
        navBar.largeTitleTextAttributes = [.foregroundColor: UIColor(theme.color.text)]
        UINavigationBar.appearance().standardAppearance = navBar
        UINavigationBar.appearance().scrollEdgeAppearance = navBar
    }
}
