import SwiftUI

/// Focus treatment for every custom button on tvOS: scale 1.08 + 4 pt white ring + soft glow.
/// The ring, not the colour tint, carries the focus state so it survives any artwork (≥3:1 against surroundings).
/// With Reduce Motion the scale animation is dropped but the ring remains: focus must always be visible.
struct TVButtonStyle: ButtonStyle {
    /// `card`: artwork card in a rail — the label draws its own art/text, the style adds only the ring + lift
    /// (no padding, no background) so the focus treatment matches every other control on the app.
    enum Prominence { case primary, secondary, icon, card }
    var prominence: Prominence = .secondary

    @Environment(\.isFocused) private var isFocused
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(prominence == .icon ? .system(size: 34, weight: .medium) : LumenFont.body)
            .foregroundStyle(foreground)
            .padding(.horizontal, prominence == .icon ? 22 : prominence == .card ? 0 : LumenSpace.l)
            .padding(.vertical, prominence == .icon ? 22 : prominence == .card ? 0 : LumenSpace.m)
            .frame(minWidth: 88, minHeight: 88)          // large targets read from 3 m and survive the scale overflow
            .background(background, in: RoundedRectangle(cornerRadius: LumenFocus.cornerRadius, style: .continuous))
            .overlay(alignment: .top) {
                // Cards: ring around the artwork only (the title sits below the art, outside the ring).
                RoundedRectangle(cornerRadius: LumenFocus.cornerRadius, style: .continuous)
                    .strokeBorder(LumenColor.focusRing, lineWidth: isFocused ? LumenFocus.ringWidth : 0)
                    .frame(height: prominence == .card ? 225 : nil)
            }
            .shadow(color: .black.opacity(isFocused ? 0.45 : 0), radius: 24, y: 12)
            .scaleEffect(isFocused && !reduceMotion ? liftScale : 1)
            .scaleEffect(configuration.isPressed ? 0.97 : 1)  // pressed is brief SELECT feedback, distinct from focus
            .animation(reduceMotion ? nil : .easeOut(duration: LumenFocus.duration), value: isFocused)
            .animation(reduceMotion ? nil : .easeOut(duration: 0.08), value: configuration.isPressed)
    }

    /// Wide text buttons lift less: at 1.08 a 490 pt button at the safe-area edge grows ~20 pt past the 60 pt guide
    /// and outside the 48 pt overscan hard limit. Icon buttons (88 pt) keep the full lift; the ring carries the state.
    /// Cards (400 pt) at a rail's leading edge lift into the 60 pt margin: 1.04 keeps them inside the 48 pt limit.
    private var liftScale: CGFloat { prominence == .icon ? LumenFocus.scale : LumenFocus.scaleWide }

    private var background: Color {
        switch prominence {
        case .primary:   return isFocused ? LumenColor.accent : LumenColor.accent.opacity(0.85)
        case .secondary: return isFocused ? LumenColor.surfaceRaised : LumenColor.surface
        case .icon:      return isFocused ? Color.white.opacity(0.18) : Color.white.opacity(0.08)
        case .card:      return .clear
        }
    }

    private var foreground: Color {
        prominence == .primary ? LumenColor.canvas : LumenColor.textPrimary
    }
}

extension ButtonStyle where Self == TVButtonStyle {
    static var tvPrimary: TVButtonStyle { TVButtonStyle(prominence: .primary) }
    static var tvSecondary: TVButtonStyle { TVButtonStyle(prominence: .secondary) }
    static var tvIcon: TVButtonStyle { TVButtonStyle(prominence: .icon) }
    static var tvCard: TVButtonStyle { TVButtonStyle(prominence: .card) }
}
