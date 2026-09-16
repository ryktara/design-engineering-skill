import SwiftUI

/// Bottom overlay: title/metadata, scrubber, one row of <=5 actions. Everything inside the 60 pt safe area;
/// the scrim bleeds to the edge so text stays >=7:1 over the brightest frame.
struct TransportControls: View {
    @Bindable var model: PlayerModel
    var focus: FocusState<PlayerFocus?>.Binding
    let scope: Namespace.ID
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        VStack {
            Spacer()
            VStack(alignment: .leading, spacing: LumenSpace.m) {
                header
                scrubber
                actions
            }
            .padding(.horizontal, LumenSpace.safeArea)
            .padding(.bottom, LumenSpace.safeArea)
            .padding(.top, 180)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                LinearGradient(stops: [.init(color: LumenColor.scrim.opacity(0), location: 0),
                                       .init(color: LumenColor.scrim.opacity(0.55), location: 0.35),
                                       .init(color: LumenColor.scrim.opacity(0.88), location: 1)],
                               startPoint: .top, endPoint: .bottom)
                    .ignoresSafeArea()
            )
        }
        .focusSection()
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: LumenSpace.xs) {
            Text(model.episode.series.title.uppercased())
                .font(LumenFont.caption).tracking(2)
                .foregroundStyle(LumenColor.textSecondary)
            Text(model.episode.label)
                .font(LumenFont.title)
                .foregroundStyle(LumenColor.textPrimary)
                .lineLimit(1)
        }
        .accessibilityElement(children: .combine)
        .accessibilityAddTraits(.isHeader)
    }

    /// Scrubber: focusable track; LEFT/RIGHT seek in fixed 10 s steps (Siri Remote swipes arrive as move commands).
    private var scrubber: some View {
        let isFocused = focus.wrappedValue == .scrubber
        return VStack(spacing: LumenSpace.s) {
            GeometryReader { geo in
                let progress = model.duration > 0 ? model.currentTime / model.duration : 0
                ZStack(alignment: .leading) {
                    Capsule().fill(Color.white.opacity(0.25))
                    Capsule().fill(LumenColor.accent).frame(width: max(0, geo.size.width * progress))
                    Circle()
                        .fill(.white)
                        .frame(width: isFocused ? 30 : 18, height: isFocused ? 30 : 18)
                        .overlay(
                            Circle()
                                .strokeBorder(LumenColor.focusRing, lineWidth: isFocused ? LumenFocus.ringWidth : 0)
                                .padding(-6)
                        )
                        .offset(x: geo.size.width * progress - (isFocused ? 15 : 9))
                }
            }
            .frame(height: isFocused ? 10 : 6)
            .padding(.vertical, 12)
            .contentShape(Rectangle())
            .focusable()
            .focused(focus, equals: .scrubber)
            .onMoveCommand { dir in
                switch dir {
                case .left: model.seek(by: -LumenTiming.seekStep)
                case .right: model.seek(by: LumenTiming.seekStep)
                default: break
                }
            }
            .accessibilityElement()
            .accessibilityLabel("Progress")
            .accessibilityValue("\(model.currentTime.clockString) of \(model.duration.clockString)")
            .accessibilityAdjustableAction { d in
                model.seek(by: d == .increment ? LumenTiming.seekStep : -LumenTiming.seekStep)
            }
            .animation(reduceMotion ? nil : .easeOut(duration: LumenFocus.duration), value: isFocused)

            HStack {
                Text(model.currentTime.clockString).monospacedDigit()
                Spacer()
                Text("-\((model.duration - model.currentTime).clockString)").monospacedDigit()
            }
            .font(LumenFont.caption)
            .foregroundStyle(LumenColor.textSecondary)
        }
    }

    private var actions: some View {
        HStack(spacing: LumenSpace.m) {
            Button { model.seek(by: -LumenTiming.seekStep) } label: { Image(systemName: "gobackward.10") }
                .buttonStyle(.tvIcon)
                .focused(focus, equals: .skipBack)
                .accessibilityLabel("Back 10 seconds")

            Button { model.togglePlayPause() } label: {
                Image(systemName: model.isPlaying ? "pause.fill" : "play.fill")
            }
            .buttonStyle(.tvIcon)
            .focused(focus, equals: .playPause)
            .prefersDefaultFocus(model.overlay == .controls, in: scope)
            .accessibilityLabel(model.isPlaying ? "Pause" : "Play")

            Button { model.seek(by: LumenTiming.seekStep) } label: { Image(systemName: "goforward.10") }
                .buttonStyle(.tvIcon)
                .focused(focus, equals: .skipForward)
                .accessibilityLabel("Forward 10 seconds")

            Button { model.openTrackPicker() } label: {
                Label(pickerSummary, systemImage: "captions.bubble")
            }
            .buttonStyle(.tvSecondary)
            .focused(focus, equals: .tracks)
            .accessibilityLabel("Subtitles and audio")
            .accessibilityValue(pickerSummary)

            if model.nextEpisode != nil {
                Button { model.playNext() } label: { Label("Next episode", systemImage: "forward.end") }
                    .buttonStyle(.tvSecondary)
                    .focused(focus, equals: .next)
            }
            Spacer()
        }
    }

    private var pickerSummary: String {
        // Name both roles so "English · English" cannot happen.
        let subs = model.selectedSubtitle.isOff ? "Subtitles off" : "\(model.selectedSubtitle.displayName) subtitles"
        let audio = model.selectedAudio.displayName.split(separator: " ").first.map(String.init) ?? ""
        return "\(subs) · \(audio) audio"
    }
}
