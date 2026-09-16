import XCTest
@testable import LumenTV

final class ActivationCodeTests: XCTestCase {
    func testAlphabetHasNoAmbiguousGlyphs() {
        let banned: Set<Character> = ["0", "O", "1", "I", "L", "2", "Z", "5", "S", "8", "B"]
        XCTAssertTrue(Set(ActivationCode.alphabet).isDisjoint(with: banned))
    }

    func testDisplayGroupsCode() {
        let c = ActivationCode(value: "H7KM4Q", issuedAt: .now, expiresAt: .now)
        XCTAssertEqual(c.display, "H7K-M4Q")
        XCTAssertEqual(c.activationURL.absoluteString, "https://lumen.tv/activate?code=H7KM4Q")
    }

    func testRandomUsesAlphabetOnly() {
        var g = SystemRandomNumberGenerator()
        for _ in 0..<50 {
            let c = ActivationCode.random(using: &g)
            XCTAssertEqual(c.value.count, ActivationCode.length)
            XCTAssertTrue(c.value.allSatisfy { ActivationCode.alphabet.contains($0) })
        }
    }
}
