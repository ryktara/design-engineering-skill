import Foundation

/// How often a habit is expected to be completed.
enum HabitFrequency: String, CaseIterable, Identifiable, Codable {
    case daily = "Daily"
    case weekdays = "Weekdays"
    case weekly = "Weekly"

    var id: String { rawValue }
}

/// A single tracked habit.
struct Habit: Identifiable, Hashable, Codable {
    let id: UUID
    var name: String
    /// SF Symbol name used for the habit's icon.
    var icon: String
    var frequency: HabitFrequency
    /// Optional daily reminder time. Only the hour/minute components are meaningful.
    var reminder: Date?
    /// Consecutive days completed (including today if `isCompletedToday`).
    var streak: Int
    var isCompletedToday: Bool
    var isArchived: Bool

    init(
        id: UUID = UUID(),
        name: String,
        icon: String,
        frequency: HabitFrequency = .daily,
        reminder: Date? = nil,
        streak: Int = 0,
        isCompletedToday: Bool = false,
        isArchived: Bool = false
    ) {
        self.id = id
        self.name = name
        self.icon = icon
        self.frequency = frequency
        self.reminder = reminder
        self.streak = streak
        self.isCompletedToday = isCompletedToday
        self.isArchived = isArchived
    }
}

/// Completed-habit count for one day, used by the weekly chart.
struct DailyCompletion: Identifiable, Hashable {
    let day: String      // "Mon" ... "Sun"
    let completed: Int
    let total: Int

    var id: String { day }
    var ratio: Double { total == 0 ? 0 : Double(completed) / Double(total) }
}
