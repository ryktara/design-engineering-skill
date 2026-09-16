import SwiftUI

/// Circular progress indicator used at the top of the Today screen.
struct ProgressRing: View {
    @Environment(\.theme) private var theme

    /// 0...1
    let progress: Double
    var lineWidth: CGFloat = 14
    var size: CGFloat = 140

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
                Text("\(Int((progress * 100).rounded()))%")
                    .font(theme.font.stat)
                    .foregroundStyle(theme.color.text)
                Text("done")
                    .font(theme.font.caption)
                    .foregroundStyle(theme.color.textSecondary)
            }
        }
        .frame(width: size, height: size)
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("Today's progress")
        .accessibilityValue("\(Int((progress * 100).rounded())) percent")
    }
}

#Preview {
    ProgressRing(progress: 0.4)
        .padding()
}
