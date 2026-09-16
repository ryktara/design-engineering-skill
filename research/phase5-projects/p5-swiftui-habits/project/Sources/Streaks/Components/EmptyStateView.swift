import SwiftUI

/// Zero state for a list or scroll region: icon chip, short heading, one sentence
/// of what to do next, and at most one primary action. Occupies the same layout
/// region as the content it replaces.
struct EmptyStateView: View {
    @Environment(\.theme) private var theme

    let icon: String
    let title: String
    let message: String
    var actionTitle: String? = nil
    var actionSystemImage: String? = nil
    var action: (() -> Void)? = nil

    var body: some View {
        VStack(spacing: theme.spacing.lg) {
            Image(systemName: icon)
                .font(.system(size: 28, weight: .semibold))
                .foregroundStyle(theme.color.accent)
                .frame(width: 72, height: 72)
                .background(theme.color.accentSoft)
                .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadius, style: .continuous))
                .accessibilityHidden(true)

            VStack(spacing: theme.spacing.sm) {
                Text(title)
                    .font(theme.font.title2)
                    .foregroundStyle(theme.color.text)
                    .multilineTextAlignment(.center)

                Text(message)
                    .font(theme.font.callout)
                    .foregroundStyle(theme.color.textSecondary)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
            }

            if let actionTitle, let action {
                PrimaryButton(title: actionTitle, systemImage: actionSystemImage, action: action)
                    .padding(.top, theme.spacing.xs)
            }
        }
        .padding(.horizontal, theme.spacing.xl)
        .padding(.vertical, theme.spacing.xl)
        .frame(maxWidth: .infinity)
        .accessibilityElement(children: .contain)
        .accessibilityLabel(title)
    }
}

#Preview {
    EmptyStateView(
        icon: "checklist",
        title: "No habits yet",
        message: "Habits you add will show up here, with their streak and reminder.",
        actionTitle: "Add your first habit",
        actionSystemImage: "plus"
    ) {}
    .background(Theme.default.color.background)
}
