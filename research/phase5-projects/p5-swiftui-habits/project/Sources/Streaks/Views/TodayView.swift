import SwiftUI

/// Today: weekly summary strip, progress ring, then a stack of habit cards to check off.
struct TodayView: View {
    @Environment(\.theme) private var theme
    @EnvironmentObject private var store: Store

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: theme.spacing.xl) {
                    weeklySummary
                    header
                    habitList
                }
                .padding(.horizontal, theme.spacing.lg)
                .padding(.top, theme.spacing.sm)
                .padding(.bottom, theme.spacing.xl)
            }
            .pageBackground(theme)
            .navigationTitle("Today")
            .navigationBarTitleDisplayMode(.large)
        }
    }

    private var weeklySummary: some View {
        WeeklySummaryCard(
            days: store.weeklyCompletions,
            completed: store.weeklyCompletedCount,
            total: store.weeklyTotalCount
        )
    }

    private var header: some View {
        VStack(spacing: theme.spacing.lg) {
            ProgressRing(progress: store.todayProgress)

            VStack(spacing: theme.spacing.xs) {
                Text(headline)
                    .font(theme.font.title2)
                    .foregroundStyle(theme.color.text)
                Text("\(store.completedTodayCount) of \(store.activeHabits.count) habits done")
                    .font(theme.font.subheadline)
                    .foregroundStyle(theme.color.textSecondary)
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, theme.spacing.xl)
        .cardSurface(theme)
    }

    private var headline: String {
        switch store.todayProgress {
        case 1: return "All done. Nice work!"
        case 0.5...: return "Over halfway there"
        case 0: return "Let's get started"
        default: return "Keep it going"
        }
    }

    private var habitList: some View {
        VStack(alignment: .leading, spacing: theme.spacing.md) {
            Text("Habits")
                .font(theme.font.headline)
                .foregroundStyle(theme.color.textSecondary)
                .padding(.leading, theme.spacing.xs)

            ForEach(store.activeHabits) { habit in
                HabitCard(habit: habit) {
                    withAnimation { store.toggleCompletion(habit) }
                }
            }

            if store.activeHabits.isEmpty {
                Text("No habits yet. Add one from the Habits tab.")
                    .font(theme.font.body)
                    .foregroundStyle(theme.color.textSecondary)
                    .frame(maxWidth: .infinity)
                    .padding(theme.spacing.xl)
                    .cardSurface(theme)
            }
        }
    }
}

#Preview {
    TodayView()
        .environmentObject(Store())
}
