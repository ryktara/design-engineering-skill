import SwiftUI

/// Habits: manage the full list. Swipe to archive; `+` presents the add sheet.
struct HabitsView: View {
    @Environment(\.theme) private var theme
    @EnvironmentObject private var store: Store

    @State private var isPresentingAdd = false

    var body: some View {
        NavigationStack {
            Group {
                if store.habits.isEmpty {
                    emptyState
                } else {
                    habitList
                }
            }
            .pageBackground(theme)
            .navigationTitle("Habits")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        isPresentingAdd = true
                    } label: {
                        Image(systemName: "plus")
                            .font(.system(size: 17, weight: .semibold))
                    }
                    .accessibilityLabel("Add habit")
                }
            }
            .sheet(isPresented: $isPresentingAdd) {
                AddHabitSheet { habit in
                    withAnimation { store.add(habit) }
                }
            }
        }
    }

    /// First run: nothing has ever been added. The list region is replaced by a
    /// zero state that says what the screen is for and offers the one action
    /// that resolves it (the same action as the `+` in the toolbar).
    private var emptyState: some View {
        // Centred in the region the list would have filled, but inside a
        // ScrollView so it stays reachable at the largest Dynamic Type sizes.
        GeometryReader { proxy in
            ScrollView {
                EmptyStateView(
                    icon: "checklist",
                    title: "No habits yet",
                    message: "Habits you add show up here with their streak and reminder. Start with one you can keep every day.",
                    actionTitle: "Add your first habit",
                    actionSystemImage: "plus"
                ) {
                    isPresentingAdd = true
                }
                .frame(minHeight: proxy.size.height, alignment: .center)
            }
        }
    }

    private var habitList: some View {
        List {
            Section {
                if store.activeHabits.isEmpty {
                    Text("No active habits. Swipe an archived habit to restore it, or add a new one.")
                        .font(theme.font.callout)
                        .foregroundStyle(theme.color.textSecondary)
                        .padding(.vertical, theme.spacing.sm)
                }
                ForEach(store.activeHabits) { habit in
                    HabitRow(habit: habit)
                        .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                            Button {
                                withAnimation { store.archive(habit) }
                            } label: {
                                Label("Archive", systemImage: "archivebox.fill")
                            }
                            .tint(theme.color.textSecondary)
                        }
                }
            } header: {
                Text("Active")
                    .font(theme.font.caption)
                    .foregroundStyle(theme.color.textSecondary)
            }
            .listRowBackground(theme.color.surface)

            if !store.archivedHabits.isEmpty {
                Section {
                    ForEach(store.archivedHabits) { habit in
                        HabitRow(habit: habit)
                            .opacity(0.6)
                            .swipeActions(edge: .trailing) {
                                Button {
                                    withAnimation { store.restore(habit) }
                                } label: {
                                    Label("Restore", systemImage: "arrow.uturn.backward")
                                }
                                .tint(theme.color.accent)
                            }
                    }
                } header: {
                    Text("Archived")
                        .font(theme.font.caption)
                        .foregroundStyle(theme.color.textSecondary)
                }
                .listRowBackground(theme.color.surface)
            }
        }
        .scrollContentBackground(.hidden)
    }
}

/// Compact list row used inside the Habits list (cards are reserved for Today).
private struct HabitRow: View {
    @Environment(\.theme) private var theme
    let habit: Habit

    var body: some View {
        HStack(spacing: theme.spacing.md) {
            Image(systemName: habit.icon)
                .font(.system(size: 16, weight: .semibold))
                .foregroundStyle(theme.color.accent)
                .frame(width: 36, height: 36)
                .background(theme.color.accentSoft)
                .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadiusSmall, style: .continuous))

            VStack(alignment: .leading, spacing: 2) {
                Text(habit.name)
                    .font(theme.font.body)
                    .foregroundStyle(theme.color.text)
                Text(reminderText)
                    .font(theme.font.caption)
                    .foregroundStyle(theme.color.textSecondary)
            }

            Spacer()

            Text("\(habit.streak)")
                .font(theme.font.subheadline)
                .foregroundStyle(theme.color.textSecondary)
            Image(systemName: "flame.fill")
                .font(.caption)
                .foregroundStyle(theme.color.accent)
        }
        .padding(.vertical, theme.spacing.xs)
    }

    private var reminderText: String {
        guard let reminder = habit.reminder else { return habit.frequency.rawValue }
        return "\(habit.frequency.rawValue) · \(reminder.formatted(date: .omitted, time: .shortened))"
    }
}

#Preview("Habits") {
    HabitsView()
        .environmentObject(Store())
}

#Preview("Habits — first run") {
    HabitsView()
        .environmentObject(Store(habits: [], weeklyCompletions: []))
}
