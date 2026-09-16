import Foundation
import Combine

/// In-memory app state with deterministic sample data.
/// No persistence on purpose: the fixture must render identically on every launch.
@MainActor
final class Store: ObservableObject {
    @Published var habits: [Habit]
    @Published var weeklyCompletions: [DailyCompletion]
    @Published var remindersEnabled: Bool = true
    @Published var weekStartsOnMonday: Bool = true

    static let sampleIcons = [
        "drop.fill", "book.fill", "figure.run", "leaf.fill", "moon.fill",
        "brain.head.profile", "pencil", "cup.and.saucer.fill", "dumbbell.fill", "sun.max.fill"
    ]

    init(habits: [Habit] = Store.sampleHabits, weeklyCompletions: [DailyCompletion] = Store.sampleWeek) {
        self.habits = habits
        self.weeklyCompletions = weeklyCompletions
    }

    // MARK: - Derived

    var activeHabits: [Habit] { habits.filter { !$0.isArchived } }
    var archivedHabits: [Habit] { habits.filter { $0.isArchived } }

    var completedTodayCount: Int { activeHabits.filter(\.isCompletedToday).count }

    var todayProgress: Double {
        let total = activeHabits.count
        return total == 0 ? 0 : Double(completedTodayCount) / Double(total)
    }

    var longestStreak: Int { activeHabits.map(\.streak).max() ?? 0 }

    var weeklyCompletionRate: Double {
        let completed = weeklyCompletions.reduce(0) { $0 + $1.completed }
        let total = weeklyCompletions.reduce(0) { $0 + $1.total }
        return total == 0 ? 0 : Double(completed) / Double(total)
    }

    // MARK: - Mutations

    func toggleCompletion(_ habit: Habit) {
        guard let index = habits.firstIndex(where: { $0.id == habit.id }) else { return }
        habits[index].isCompletedToday.toggle()
        habits[index].streak += habits[index].isCompletedToday ? 1 : -1
        habits[index].streak = max(0, habits[index].streak)
    }

    func add(_ habit: Habit) {
        habits.append(habit)
    }

    func archive(_ habit: Habit) {
        guard let index = habits.firstIndex(where: { $0.id == habit.id }) else { return }
        habits[index].isArchived = true
    }

    func restore(_ habit: Habit) {
        guard let index = habits.firstIndex(where: { $0.id == habit.id }) else { return }
        habits[index].isArchived = false
    }

    // MARK: - Sample data (deterministic UUIDs so previews and snapshots are stable)

    static func reminder(hour: Int, minute: Int = 0) -> Date {
        var components = DateComponents()
        components.year = 2026
        components.month = 1
        components.day = 1
        components.hour = hour
        components.minute = minute
        return Calendar(identifier: .gregorian).date(from: components) ?? Date(timeIntervalSince1970: 0)
    }

    static let sampleHabits: [Habit] = [
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000001")!,
              name: "Drink water", icon: "drop.fill", frequency: .daily,
              reminder: reminder(hour: 8), streak: 12, isCompletedToday: true),
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000002")!,
              name: "Read 20 pages", icon: "book.fill", frequency: .daily,
              reminder: reminder(hour: 21), streak: 5, isCompletedToday: true),
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000003")!,
              name: "Morning run", icon: "figure.run", frequency: .weekdays,
              reminder: reminder(hour: 6, minute: 30), streak: 3, isCompletedToday: false),
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000004")!,
              name: "Meditate", icon: "brain.head.profile", frequency: .daily,
              reminder: reminder(hour: 7), streak: 21, isCompletedToday: false),
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000005")!,
              name: "No screens after 10pm", icon: "moon.fill", frequency: .daily,
              reminder: reminder(hour: 22), streak: 0, isCompletedToday: false),
        Habit(id: UUID(uuidString: "00000000-0000-0000-0000-000000000006")!,
              name: "Weekly review", icon: "pencil", frequency: .weekly,
              reminder: nil, streak: 8, isCompletedToday: false, isArchived: true)
    ]

    static let sampleWeek: [DailyCompletion] = [
        DailyCompletion(day: "Mon", completed: 4, total: 5),
        DailyCompletion(day: "Tue", completed: 5, total: 5),
        DailyCompletion(day: "Wed", completed: 3, total: 5),
        DailyCompletion(day: "Thu", completed: 5, total: 5),
        DailyCompletion(day: "Fri", completed: 2, total: 5),
        DailyCompletion(day: "Sat", completed: 4, total: 5),
        DailyCompletion(day: "Sun", completed: 2, total: 5)
    ]
}
