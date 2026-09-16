import XCTest
@testable import Streaks

@MainActor
final class StoreTests: XCTestCase {
    func testSampleDataIsDeterministic() {
        let a = Store()
        let b = Store()
        XCTAssertEqual(a.habits, b.habits)
        XCTAssertEqual(a.activeHabits.count, 5)
        XCTAssertEqual(a.archivedHabits.count, 1)
    }

    func testTodayProgress() {
        let store = Store()
        XCTAssertEqual(store.completedTodayCount, 2)
        XCTAssertEqual(store.todayProgress, 0.4, accuracy: 0.001)
    }

    func testToggleCompletionAdjustsStreak() {
        let store = Store()
        let habit = store.activeHabits[2] // Morning run, streak 3, not completed
        store.toggleCompletion(habit)
        XCTAssertTrue(store.habits[2].isCompletedToday)
        XCTAssertEqual(store.habits[2].streak, 4)
        store.toggleCompletion(store.habits[2])
        XCTAssertEqual(store.habits[2].streak, 3)
    }

    func testArchiveAndRestore() {
        let store = Store()
        let habit = store.activeHabits[0]
        store.archive(habit)
        XCTAssertEqual(store.activeHabits.count, 4)
        store.restore(habit)
        XCTAssertEqual(store.activeHabits.count, 5)
    }
}
