import Foundation

/// Device-code flow: the TV requests a code, shows it, and polls until the companion device approves it.
protocol ActivationService {
    func requestCode() async throws -> ActivationCode
    /// Returns the account name once approved, nil while still pending.
    func poll(_ code: ActivationCode) async throws -> String?
    func signIn(email: String, password: String) async throws -> String
}

/// Stand-in used by previews and this exercise. A real implementation talks to the account API.
final class MockActivationService: ActivationService {
    private var approveAfterPolls = 6
    private var polls = 0

    func requestCode() async throws -> ActivationCode {
        try await Task.sleep(for: .milliseconds(300))
        polls = 0
        return .random()
    }

    func poll(_ code: ActivationCode) async throws -> String? {
        try await Task.sleep(for: .seconds(2))
        polls += 1
        return polls >= approveAfterPolls ? "Tara" : nil
    }

    func signIn(email: String, password: String) async throws -> String {
        try await Task.sleep(for: .milliseconds(800))
        guard email.contains("@"), password.count >= 8 else {
            throw ActivationError.invalidCredentials
        }
        return String(email.split(separator: "@").first ?? "there")
    }
}

enum ActivationError: LocalizedError {
    case invalidCredentials, network
    var errorDescription: String? {
        switch self {
        case .invalidCredentials: return "That email or password isn't right."
        case .network: return "Can't reach Lumen. Check the Apple TV's network connection."
        }
    }
}
