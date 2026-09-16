import SwiftUI
import Charts

/// Stats: weekly completion bar chart plus a 2x2 grid of stat tiles.
struct StatsView: View {
    @Environment(\.theme) private var theme
    @EnvironmentObject private var store: Store

    private var columns: [GridItem] {
        [GridItem(.flexible(), spacing: theme.spacing.md), GridItem(.flexible(), spacing: theme.spacing.md)]
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: theme.spacing.xl) {
                    weeklyChart
                    tileGrid
                }
                .padding(.horizontal, theme.spacing.lg)
                .padding(.top, theme.spacing.sm)
                .padding(.bottom, theme.spacing.xl)
            }
            .pageBackground(theme)
            .navigationTitle("Stats")
        }
    }

    // MARK: Chart

    private var weeklyChart: some View {
        VStack(alignment: .leading, spacing: theme.spacing.lg) {
            VStack(alignment: .leading, spacing: theme.spacing.xs) {
                Text("This week")
                    .font(theme.font.headline)
                    .foregroundStyle(theme.color.text)
                Text("\(Int((store.weeklyCompletionRate * 100).rounded()))% of habits completed")
                    .font(theme.font.caption)
                    .foregroundStyle(theme.color.textSecondary)
            }

            Chart(store.weeklyCompletions) { day in
                // Track: the full day's total, drawn behind the completed bar.
                // Unstacked so both marks share the same baseline (the default
                // stacks marks at the same x and would sum total + completed).
                BarMark(
                    x: .value("Day", day.day),
                    y: .value("Total", day.total, stacking: .unstacked)
                )
                .foregroundStyle(theme.color.chartTrack)
                .cornerRadius(theme.shape.cornerRadiusSmall / 2)

                BarMark(
                    x: .value("Day", day.day),
                    y: .value("Completed", day.completed, stacking: .unstacked)
                )
                .foregroundStyle(theme.color.accent)
                .cornerRadius(theme.shape.cornerRadiusSmall / 2)
            }
            .chartYAxis(.hidden)
            .chartXAxis {
                AxisMarks { _ in
                    AxisValueLabel()
                        .font(theme.font.caption)
                        .foregroundStyle(theme.color.textSecondary)
                }
            }
            .chartPlotStyle { plot in
                plot.background(Color.clear)
            }
            .frame(height: 160)
        }
        .padding(theme.spacing.lg)
        .cardSurface(theme)
    }

    // MARK: Tiles

    private var tileGrid: some View {
        LazyVGrid(columns: columns, spacing: theme.spacing.md) {
            StatTile(value: "\(store.longestStreak)", label: "Longest streak", systemImage: "flame.fill")
            StatTile(value: "\(store.activeHabits.count)", label: "Active habits", systemImage: "checklist")
            StatTile(value: "\(store.completedTodayCount)", label: "Done today", systemImage: "checkmark.circle.fill")
            StatTile(value: "\(Int((store.weeklyCompletionRate * 100).rounded()))%", label: "Weekly rate", systemImage: "chart.line.uptrend.xyaxis")
        }
    }
}

private struct StatTile: View {
    @Environment(\.theme) private var theme

    let value: String
    let label: String
    let systemImage: String

    var body: some View {
        VStack(alignment: .leading, spacing: theme.spacing.sm) {
            Image(systemName: systemImage)
                .font(.system(size: 16, weight: .semibold))
                .foregroundStyle(theme.color.accent)
                .frame(width: 32, height: 32)
                .background(theme.color.accentSoft)
                .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadiusSmall, style: .continuous))

            Text(value)
                .font(theme.font.stat)
                .foregroundStyle(theme.color.text)

            Text(label)
                .font(theme.font.caption)
                .foregroundStyle(theme.color.textSecondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(theme.spacing.lg)
        .cardSurface(theme)
        .accessibilityElement(children: .combine)
    }
}

#Preview {
    StatsView()
        .environmentObject(Store())
}
