import Foundation
import Observation

/// Search state for the tvOS search screen. Text entry itself is the system's (`.searchable` shows the tvOS
/// keyboard with Siri dictation); this model owns the query, the debounce, the result grouping and the
/// recent-search memory. States are enumerated so the view never has a blank or dead-end frame.
@Observable
final class SearchModel {
    enum Phase: Equatable {
        case idle                       // no query: recent searches + browse topics
        case searching                  // debounce/lookup in flight (kept short; shows only after 300 ms)
        case results(SearchResults)     // ≥1 hit, grouped into rails
        case empty(String)              // no hits for the query: guidance + browse topics
    }

    var query: String = "" { didSet { if query != oldValue { scheduleSearch() } } }
    private(set) var phase: Phase = .idle
    private(set) var recent: [String] = []
    /// Set by the view to announce "N results for …" once per completed search (a11y-live-status).
    private(set) var announcement: String?

    static let debounce: Duration = .milliseconds(250)
    static let maxRecent = 6
    private var searchTask: Task<Void, Never>?

    private func scheduleSearch() {
        searchTask?.cancel()
        let q = query.trimmingCharacters(in: .whitespaces)
        guard q.count >= 2 else { phase = .idle; announcement = nil; return }
        searchTask = Task { [weak self] in
            try? await Task.sleep(for: Self.debounce)
            guard let self, !Task.isCancelled else { return }
            self.apply(SampleCatalogue.search(q))
        }
    }

    private func apply(_ results: SearchResults) {
        if results.isEmpty {
            phase = .empty(results.query)
            announcement = "No results for \(results.query)"
        } else {
            phase = .results(results)
            announcement = "\(results.count) results for \(results.query)"
        }
    }

    /// Called when the viewer submits (Done on the keyboard) or opens a result: remember the query.
    func commit() {
        let q = query.trimmingCharacters(in: .whitespaces)
        guard q.count >= 2 else { return }
        recent.removeAll { $0.caseInsensitiveCompare(q) == .orderedSame }
        recent.insert(q, at: 0)
        if recent.count > Self.maxRecent { recent.removeLast(recent.count - Self.maxRecent) }
    }

    func useRecent(_ q: String) { query = q }
    func clear() { query = "" }
}
