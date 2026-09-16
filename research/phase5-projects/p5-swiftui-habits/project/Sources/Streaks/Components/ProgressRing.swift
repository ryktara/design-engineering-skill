import SwiftUI

/// Circular progress indicator used at the top of the Today screen.
///
/// Accessibility: the ring is a *data graphic*, not an image. The arcs and the
/// centred percentage are decorative duplicates of the spoken value, so the ring
/// is published as a single element with a name and a value and nothing inside it
/// is exposed separately. `.isImage` is removed explicitly: a custom SwiftUI view
/// built only from `Shape`s is otherwise liable to be surfaced as an unnamed image
/// element, which is what VoiceOver was announcing. The count the arc encodes is
/// spoken as text ("40 percent"), so the graphic is never the only carrier.
struct ProgressRing: View {
    @Environment(\.theme) private var theme

    /// 0...1
    let progress: Double
    var lineWidth: CGFloat = 14
    var size: CGFloat = 140

    private var percent: Int { Int((min(max(progress, 0), 1) * 100).rounded()) }

    var body: some View {
        ZStack {
            Circle()
                .stroke(theme.color.accentSoft, lineWidth: lineWidth)

            Circle()
                .trim(from: 0, to: min(max(progress, 0), 1))
                .stroke(
                    theme.color.accent,
                    style: StrokeStyle(lineWidth: lineWidth, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))
                .animation(.spring(response: 0.6, dampingFraction: 0.8), value: progress)

            VStack(spacing: theme.spacing.xs) {
                Text("\(percent)%")
                    .font(theme.font.stat)
                    .foregroundStyle(theme.color.text)
                    .monospacedDigit()
                Text("done")
                    .font(theme.font.caption)
                    .foregroundStyle(theme.color.textSecondary)
            }
        }
        .frame(width: size, height: size)
        .accessibilityElement(children: .ignore)
        .accessibilityRemoveTraits(.isImage)
        .accessibilityAddTraits(.updatesFrequently)
        .accessibilityLabel("Today's progress")
        .accessibilityValue("\(percent) percent")
    }
}

#Preview {
    ProgressRing(progress: 0.4)
        .padding()
}
