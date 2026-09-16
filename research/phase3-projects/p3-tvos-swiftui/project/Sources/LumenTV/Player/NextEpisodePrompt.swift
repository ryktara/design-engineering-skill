import SwiftUI

/// "Next episode" prompt shown from the credits marker. Bottom-right card, inside the safe area, video still
/// visible. Focus lands on "Play next" (autoplay in N s). Menu dismisses the prompt only (see PlayerModel.handleMenu);
/// "Watch credits" also cancels the countdown. No time-limited interaction without an escape: the countdown is
/// cancellable and the prompt can be re-triggered from the transport row's "Next episode" button.
struct NextEpisodePrompt: View {
    @Bindable var model: PlayerModel
    let next: Episode
    var focus: FocusState<PlayerFocus?>.Binding
    @Namespace private var promptScope

    var body: some View {
        VStack {
            Spacer()
            HStack {
                Spacer()
                VStack(alignment: .leading, spacing: LumenSpace.m) {
                    Text("UP NEXT")
                        .font(LumenFont.caption).tracking(2)
                        .foregroundStyle(LumenColor.textSecondary)
                    Text(next.label)
                        .font(LumenFont.headline)
                        .foregroundStyle(LumenColor.textPrimary)
                        .lineLimit(2)
                    Text(next.synopsis)
                        .font(LumenFont.caption)
                        .foregroundStyle(LumenColor.textSecondary)
                        .lineLimit(2)
                    HStack(spacing: LumenSpace.s) {
                        Button {
                            model.playNext()
                        } label: {
                            if let n = model.nextEpisodeCountdown {
                                Text("Play next in \(n)").monospacedDigit()
                            } else {
                                Text("Play next")
                            }
                        }
                        .buttonStyle(.tvPrimary)
                        .focused(focus, equals: .playNext)
                        .prefersDefaultFocus(in: promptScope)

                        Button("Watch credits") { model.handleMenu() }   // same effect as Menu: dismiss the prompt
                            .buttonStyle(.tvSecondary)
                            .focused(focus, equals: .watchCredits)
                    }
                    .focusSection()
                }
                .padding(LumenSpace.l)
                .frame(width: 640, alignment: .leading)
                .background(LumenColor.surface.opacity(0.96), in: RoundedRectangle(cornerRadius: 24, style: .continuous))
            }
        }
        .padding(LumenSpace.safeArea)
        .focusScope(promptScope)
        .accessibilityElement(children: .contain)
        .accessibilityLabel("Up next: \(next.label)")
    }
}
