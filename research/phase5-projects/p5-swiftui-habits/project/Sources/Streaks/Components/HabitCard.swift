import SwiftUI

/// Elevated card row for a single habit with a tappable check-off circle.
struct HabitCard: View {
    @Environment(\.theme) private var theme

    let habit: Habit
    let onToggle: () -> Void

    var body: some View {
        HStack(spacing: theme.spacing.md) {
            iconChip

            VStack(alignment: .leading, spacing: theme.spacing.xs) {
                Text(habit.name)
                    .font(theme.font.headline)
                    .foregroundStyle(theme.color.text)
                    .strikethrough(habit.isCompletedToday, color: theme.color.textSecondary)
                    .lineLimit(1)

                HStack(spacing: theme.spacing.xs) {
                    Image(systemName: "flame.fill")
                        .font(.caption2)
                    Text(habit.streak == 1 ? "1 day streak" : "\(habit.streak) day streak")
                    Text("·")
                    Text(habit.frequency.rawValue)
                }
                .font(theme.font.caption)
                .foregroundStyle(theme.color.textSecondary)
            }

            Spacer(minLength: theme.spacing.sm)

            checkCircle
        }
        .padding(theme.spacing.lg)
        .cardSurface(theme)
        .contentShape(Rectangle())
        .onTapGesture(perform: onToggle)
        .accessibilityElement(children: .combine)
        .accessibilityAddTraits(.isButton)
        .accessibilityValue(habit.isCompletedToday ? "Completed" : "Not completed")
    }

    private var iconChip: some View {
        Image(systemName: habit.icon)
            .font(.system(size: 18, weight: .semibold))
            .foregroundStyle(theme.color.accent)
            .frame(width: 44, height: 44)
            .background(theme.color.accentSoft)
            .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadiusSmall, style: .continuous))
    }

    private var checkCircle: some View {
        ZStack {
            Circle()
                .strokeBorder(
                    habit.isCompletedToday ? theme.color.accent : theme.color.separator,
                    lineWidth: 2
                )
                .background(Circle().fill(habit.isCompletedToday ? theme.color.accent : .clear))

            if habit.isCompletedToday {
                Image(systemName: "checkmark")
                    .font(.system(size: 14, weight: .bold))
                    .foregroundStyle(theme.color.surface)
            }
        }
        .frame(width: 32, height: 32)
        .animation(.easeOut(duration: 0.15), value: habit.isCompletedToday)
    }
}

#Preview {
    VStack(spacing: 12) {
        HabitCard(habit: Store.sampleHabits[0]) {}
        HabitCard(habit: Store.sampleHabits[2]) {}
    }
    .padding()
    .background(Theme.default.color.background)
}
