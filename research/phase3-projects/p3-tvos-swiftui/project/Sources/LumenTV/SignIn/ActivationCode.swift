import Foundation

/// Activation code shown on the TV and typed on a phone. Alphabet excludes visually ambiguous glyphs
/// (0/O, 1/I/L, 2/Z, 5/S, 8/B) so the code reads unambiguously from 3 m and survives being read aloud.
struct ActivationCode: Equatable {
    static let alphabet: [Character] = Array("ACDEFGHJKMNPQRTUVWXY34679")
    static let length = 6

    let value: String
    let issuedAt: Date
    let expiresAt: Date

    /// Grouped for display: "H7KM-4QDW" style (two groups) — chunking aids transcription.
    var display: String {
        let mid = value.index(value.startIndex, offsetBy: value.count / 2)
        return "\(value[..<mid])-\(value[mid...])"
    }

    var activationURL: URL {
        var c = URLComponents(string: "https://lumen.tv/activate")!
        c.queryItems = [URLQueryItem(name: "code", value: value)]
        return c.url!
    }

    static func random(ttl: TimeInterval = 15 * 60, using generator: inout some RandomNumberGenerator) -> ActivationCode {
        let chars = (0..<length).map { _ in alphabet.randomElement(using: &generator)! }
        let now = Date()
        return ActivationCode(value: String(chars), issuedAt: now, expiresAt: now.addingTimeInterval(ttl))
    }

    static func random() -> ActivationCode {
        var g = SystemRandomNumberGenerator()
        return random(using: &g)
    }
}
