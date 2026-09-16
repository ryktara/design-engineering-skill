import SwiftUI

/// Compact week-to-date summary shown above the progress ring on Today:
/// a headline rate plus one mini ring per day (same visual language as
/// `ProgressRing`, scaled down). Intentionally one row high (~80 pt) so the
/// daily ring stays the screen's focal point; at larger Dynamic Type sizes
/// `ViewThatFits` stacks the strip under the numbers instead of truncating.
struct WeeklySummaryCard: View {
    @Environment(\.theme) private var theme

    let days: [DailyCompletion]
    let completed: Int
    let total: Int

    private var rate: Double { total == 0 ? 0 : Double(completed) / Double(total) }
    private var percent: Int { Int((rate * 100).rounded()) }

    var body: some View {
        ViewThatFits(in: .horizontal) {
            HStack(alignment: .center, spacing: theme.spacing.lg) {
                summary
                Spacer(minLength: 0)
                strip
            }
            VStack(alignment: .leading, spacing: theme.spacing.md) {
                summary
                strip
            }
        }
        .padding(theme.spacing.lg)
        .cardSurface(theme)
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("This week")
        .accessibilityValue(accessibilityValue)
    }

    private var summary: some View {
        VStack(alignment: .leading, spacing: theme.spacing.xs) {
            Text("\(percent)%")
                .font(theme.font.title2)
                .foregroundStyle(theme.color.text)
                .monospacedDigit()
            Text("This week · \(completed) of \(total)")
                .font(theme.font.caption)
                .foregroundStyle(theme.color.textSecondary)
        }
    }

    private var strip: some View {
        HStack(spacing: theme.spacing.sm) {
            ForEach(days) { day in
                DayRing(day: day)
            }
        }
    }

    private var accessibilityValue: String {
        let perDay = days.map { "\($0.day) \($0.completed) of \($0.total)" }.joined(separator: ", ")
        return "\(percent) percent of habits done, \(completed) of \(total). \(perDay)"
    }
}

/// One day of the strip: a 20 pt ring filled to the day's completion ratio
/// with the day's initial beneath. Not colour-only: the ratio is the ring's
/// arc length, and the parent exposes per-day counts to VoiceOver. The track
/// uses `chartTrack` (not `accentSoft`) so an empty day still reads at 3:1
/// on the dark card surface.
private struct DayRing: View {
    @Environment(\.theme) private var theme

    let day: DailyCompletion
    private let size: CGFloat = 20
    private let lineWidth: CGFloat = 3

    var body: some View {
        VStack(spacing: theme.spacing.xs) {
            ZStack {
                Circle()
                    .stroke(theme.color.chartTrack, lineWidth: lineWidth)
                Circle()
                    .trim(from: 0, to: min(max(day.ratio, 0), 1))
                    .stroke(theme.color.accent, style: StrokeStyle(lineWidth: lineWidth, lineCap: .round))
                    .rotationEffect(.degrees(-90))
                if day.ratio >= 1 {
                    Image(systemName: "checkmark")
                        .font(.system(size: 9, weight: .bold))
                        .foregroundStyle(theme.color.accent)
                }
            }
            .frame(width: size, height: size)

            Text(day.day.prefix(1))
                .font(theme.font.caption)
                .foregroundStyle(theme.color.textSecondary)
        }
        .frame(minWidth: size)
    }
}

#Preview {
    WeeklySummaryCard(days: Store.sampleWeek, completed: 25, total: 35)
        .padding()
        .background(Theme.default.color.background)
}
