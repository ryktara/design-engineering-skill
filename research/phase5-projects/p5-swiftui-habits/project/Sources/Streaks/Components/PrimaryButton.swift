import SwiftUI

/// Full-width accent button used for primary actions (Save, Start).
struct PrimaryButton: View {
    @Environment(\.theme) private var theme
    @Environment(\.isEnabled) private var isEnabled

    let title: String
    var systemImage: String? = nil
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: theme.spacing.sm) {
                if let systemImage {
                    Image(systemName: systemImage)
                }
                Text(title)
            }
            .font(theme.font.headline)
            .foregroundStyle(theme.color.surface)
            .frame(maxWidth: .infinity)
            .frame(height: 52)
            .background(theme.color.accent.opacity(isEnabled ? 1 : 0.45))
            .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadius, style: .continuous))
            .shadow(
                color: theme.color.accent.opacity(isEnabled ? theme.shadow.buttonOpacity : 0),
                radius: theme.shadow.buttonRadius,
                x: 0,
                y: theme.shadow.buttonY
            )
        }
        .buttonStyle(PressScaleButtonStyle())
    }
}

/// Subtle press feedback without changing colour.
struct PressScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

#Preview {
    VStack(spacing: 16) {
        PrimaryButton(title: "Save habit", systemImage: "checkmark") {}
        PrimaryButton(title: "Disabled") {}.disabled(true)
    }
    .padding()
}
