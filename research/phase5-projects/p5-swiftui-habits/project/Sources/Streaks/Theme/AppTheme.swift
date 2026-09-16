import SwiftUI
import UIKit

// MARK: - Color(light:dark:)

extension Color {
    /// A dynamic colour that resolves per trait collection (light / dark appearance).
    init(light: Color, dark: Color) {
        self.init(uiColor: UIColor { traits in
            traits.userInterfaceStyle == .dark ? UIColor(dark) : UIColor(light)
        })
    }

    /// Hex convenience used only inside the theme file. `0xRRGGBB`.
    init(hex: UInt32) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: 1
        )
    }
}

// MARK: - Theme

/// Single source of truth for the Streaks design language.
/// Every view reads colours, fonts, radii, spacing and shadows from here.
struct Theme {

    // MARK: Palette
    //
    // Colours are mirrored in `Assets.xcassets/Colors/*.colorset` so the same
    // names can be used from Interface Builder / previews / the HTML twin.
    // The `Color(light:dark:)` values below are the canonical definitions and
    // match the catalog exactly.

    struct Palette {
        /// Brand accent: warm coral. Used for the progress ring, primary button,
        /// selected tab and check-off state.
        let accent = Color(light: Color(hex: 0xFF6B4A), dark: Color(hex: 0xFF8A6E))
        /// Softer accent used for tinted backgrounds (icon chips, ring track).
        let accentSoft = Color(light: Color(hex: 0xFFE7E0), dark: Color(hex: 0x4A2A22))
        /// Page background.
        let background = Color(light: Color(hex: 0xF6F4F0), dark: Color(hex: 0x121110))
        /// Elevated card surface.
        let surface = Color(light: Color(hex: 0xFFFFFF), dark: Color(hex: 0x1E1C1A))
        /// Secondary surface for grouped list rows / sheet backgrounds.
        let surfaceSecondary = Color(light: Color(hex: 0xFBFAF8), dark: Color(hex: 0x262421))
        /// Primary text.
        let text = Color(light: Color(hex: 0x1F1B18), dark: Color(hex: 0xF4F1ED))
        /// Secondary / caption text.
        let textSecondary = Color(light: Color(hex: 0x76706A), dark: Color(hex: 0xA39D96))
        /// Hairline separators and card strokes.
        let separator = Color(light: Color(hex: 0xE8E4DE), dark: Color(hex: 0x33302C))
        /// Success (completed) green.
        let success = Color(light: Color(hex: 0x3BAF7A), dark: Color(hex: 0x5CCB95))
        /// Chart track: the "total / not yet done" portion of a bar behind the
        /// accent-coloured completed portion. Not `accentSoft`: that tint is a
        /// chip/ring-track colour and sits at 1.3:1 on the dark card surface.
        /// Dark value is a desaturated accent at 3.2:1 against `surface`
        /// (WCAG 1.4.11 non-text contrast); light matches `accentSoft`.
        let chartTrack = Color(light: Color(hex: 0xFFE7E0), dark: Color(hex: 0x8E6152))
        /// Shadow colour; opacity applied by `Theme.Shadow`.
        let shadow = Color(light: Color(hex: 0x3A2E26), dark: Color(hex: 0x000000))
    }

    // MARK: Typography
    //
    // Custom font "Nunito" (bundle the .ttf in the app target and list it under
    // UIAppFonts). When it is not registered, `Font.custom` silently falls back
    // to the system font, so we resolve the fallback explicitly to the
    // `.rounded` system design, which is visually closest to Nunito.

    struct Typography {
        static let family = "Nunito"

        private static func isRegistered(_ family: String) -> Bool {
            UIFont.familyNames.contains(family)
        }

        static func font(_ size: CGFloat, weight: Font.Weight = .regular, relativeTo style: Font.TextStyle) -> Font {
            if isRegistered(family) {
                return Font.custom(family, size: size, relativeTo: style).weight(weight)
            }
            return Font.system(style, design: .rounded).weight(weight)
        }

        let largeTitle = Typography.font(34, weight: .bold, relativeTo: .largeTitle)
        let title = Typography.font(28, weight: .bold, relativeTo: .title)
        let title2 = Typography.font(22, weight: .bold, relativeTo: .title2)
        let headline = Typography.font(17, weight: .semibold, relativeTo: .headline)
        let body = Typography.font(17, weight: .regular, relativeTo: .body)
        let callout = Typography.font(16, weight: .regular, relativeTo: .callout)
        let subheadline = Typography.font(15, weight: .medium, relativeTo: .subheadline)
        let caption = Typography.font(13, weight: .medium, relativeTo: .caption)
        let stat = Typography.font(30, weight: .heavy, relativeTo: .title)
    }

    // MARK: Spacing (4-pt base, 8-based rhythm)

    struct Spacing {
        let xs: CGFloat = 4
        let sm: CGFloat = 8
        let md: CGFloat = 12
        let lg: CGFloat = 16
        let xl: CGFloat = 24
    }

    // MARK: Shape

    struct Shape {
        /// Global corner radius for cards, buttons, sheets and tiles.
        let cornerRadius: CGFloat = 16
        /// Smaller radius for icon chips and inline controls.
        let cornerRadiusSmall: CGFloat = 10
        let hairline: CGFloat = 1
    }

    // MARK: Elevation

    struct Shadow {
        let cardOpacity: Double = 0.08
        let cardRadius: CGFloat = 16
        let cardY: CGFloat = 6
        let buttonOpacity: Double = 0.25
        let buttonRadius: CGFloat = 12
        let buttonY: CGFloat = 6
    }

    let color = Palette()
    let font = Typography()
    let spacing = Spacing()
    let shape = Shape()
    let shadow = Shadow()

    static let `default` = Theme()
}

// MARK: - Environment

private struct ThemeKey: EnvironmentKey {
    static let defaultValue = Theme.default
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// MARK: - View helpers

extension View {
    /// Elevated card surface: surface colour, radius 16, soft shadow.
    func cardSurface(_ theme: Theme) -> some View {
        self
            .background(theme.color.surface)
            .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadius, style: .continuous))
            .shadow(
                color: theme.color.shadow.opacity(theme.shadow.cardOpacity),
                radius: theme.shadow.cardRadius,
                x: 0,
                y: theme.shadow.cardY
            )
    }

    /// Full-bleed page background behind scroll content.
    func pageBackground(_ theme: Theme) -> some View {
        self.background(theme.color.background.ignoresSafeArea())
    }
}
