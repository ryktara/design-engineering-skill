import SwiftUI

/// Primary navigation: a bottom tab bar with four destinations.
struct RootTabView: View {
    @Environment(\.theme) private var theme

    enum Tab: Hashable {
        case today, habits, stats, profile
    }

    @State private var selection: Tab = .today

    var body: some View {
        TabView(selection: $selection) {
            TodayView()
                .tabItem { Label("Today", systemImage: "sun.max.fill") }
                .tag(Tab.today)

            HabitsView()
                .tabItem { Label("Habits", systemImage: "checklist") }
                .tag(Tab.habits)

            StatsView()
                .tabItem { Label("Stats", systemImage: "chart.bar.fill") }
                .tag(Tab.stats)

            ProfileView()
                .tabItem { Label("Profile", systemImage: "person.crop.circle.fill") }
                .tag(Tab.profile)
        }
        .tint(theme.color.accent)
    }
}

#Preview {
    RootTabView()
        .environmentObject(Store())
}
