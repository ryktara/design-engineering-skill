import SwiftUI

// MARK: - Design tokens (semantic roles). Values chosen for a 10-foot, dark-first UI at 1920×1080.
// Contrast ratios computed with `tokens.py contrast` (see RESULTS.md): text.primary (#EBEBEB) on canvas 15.7:1,
// text.secondary on canvas 10.2:1, focus ring (white) on canvas 18.8:1, accent on canvas 9.6:1,
// canvas text on accent (primary button) 9.6:1, text.secondary on surface 9.0:1.

enum LumenColor {
    static let canvas        = Color(red: 0x0F/255, green: 0x12/255, blue: 0x18/255) // #0F1218 tinted dark, not pure black
    static let surface       = Color(red: 0x1A/255, green: 0x1F/255, blue: 0x29/255) // #1A1F29 sheets, code tile
    static let surfaceRaised = Color(red: 0x24/255, green: 0x2B/255, blue: 0x38/255) // #242B38 focused rows in sheets
    static let textPrimary   = Color.white.opacity(0.92)
    static let textSecondary = Color(red: 0xB8/255, green: 0xC0/255, blue: 0xCC/255) // #B8C0CC
    static let accent        = Color(red: 0xE8/255, green: 0xB0/255, blue: 0x4B/255) // #E8B04B amber: focus + primary only
    static let focusRing     = Color.white
    static let scrim         = Color.black
    static let positive      = Color(red: 0x7A/255, green: 0xD3/255, blue: 0x9A/255)
}

/// TV type scale: body ≥ 29 pt on tvOS, captions ≥ 23 pt, weights ≥ regular. Fixed sizes are acceptable on tvOS
/// (no Dynamic Type); Bold Text accessibility setting is still honoured by the system.
enum LumenFont {
    static let display   = Font.system(size: 76, weight: .semibold, design: .default)   // title on sign-in
    static let title     = Font.system(size: 48, weight: .semibold)
    static let headline  = Font.system(size: 34, weight: .medium)
    static let body      = Font.system(size: 29, weight: .regular)
    static let caption   = Font.system(size: 23, weight: .regular)
    /// Activation code: monospaced, very large, wide tracking so glyphs read from 3 m.
    static let code      = Font.system(size: 132, weight: .medium, design: .monospaced)
}

enum LumenSpace {
    static let safeArea: CGFloat = 60      // tvOS HIG: 60 pt on all sides at 1920×1080
    static let xs: CGFloat = 8
    static let s: CGFloat = 16
    static let m: CGFloat = 24
    static let l: CGFloat = 40
    static let xl: CGFloat = 64
}

enum LumenFocus {
    static let scale: CGFloat = 1.08        // compact (icon) controls
    static let scaleWide: CGFloat = 1.04    // wide text buttons: keeps the lift inside the 48 pt overscan hard limit
    static let ringWidth: CGFloat = 4
    static let cornerRadius: CGFloat = 16
    static let duration: Double = 0.12   // ≤150 ms feedback
}

enum LumenTiming {
    /// Transport controls hide after this much inactivity (task requirement: 5 s).
    static let controlsAutoHide: TimeInterval = 5
    static let seekStep: TimeInterval = 10
    static let nextEpisodeCountdown: Int = 10
}
