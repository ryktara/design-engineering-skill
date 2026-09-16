import SwiftUI
import AVFoundation

/// Full-screen player. Layers, bottom to top: video -> scrim+controls -> track picker sheet -> next-episode prompt.
///
/// Remote/focus contract (tvOS):
/// - Controls hidden: the whole surface is one focusable view. Click (select) or any swipe shows the controls;
///   Play/Pause on the remote toggles playback without showing the overlay (media keys never need chrome).
/// - Controls visible: first focus on Play/Pause (`prefersDefaultFocus`); LEFT/RIGHT move along the transport row;
///   DOWN reaches the scrubber, where LEFT/RIGHT seek +/-10 s. Every remote event restarts the 5 s auto-hide.
/// - Menu (`onExitCommand`) unwinds one layer: picker -> controls -> hide controls -> leave the player. It never
///   leaves the player while something is on screen.
/// - When the controls reappear, focus is restored to the last focused control (`lastControlFocus`).
struct PlayerView: View {
    @State private var model: PlayerModel
    @Environment(\.dismiss) private var dismiss
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Namespace private var playerScope
    @FocusState private var focus: PlayerFocus?
    @State private var lastControlFocus: PlayerFocus = .playPause

    init(episode: Episode, queue: [Episode]) {
        _model = State(initialValue: PlayerModel(episode: episode, queue: queue))
    }

    var body: some View {
        ZStack {
            VideoLayerView(player: model.player)
                .ignoresSafeArea()
                .accessibilityHidden(true)

            if model.overlay == .none {
                // Invisible focus catcher so the remote always has exactly one focused element.
                Color.clear
                    .contentShape(Rectangle())
                    .focusable()
                    .focused($focus, equals: .surface)
                    .prefersDefaultFocus(model.overlay == .none, in: playerScope)
                    .onMoveCommand { _ in model.showControls() }
                    .onTapGesture { model.showControls() }      // Siri Remote click on the surface
                    .onLongPressGesture(minimumDuration: 0.6) { model.showControls(); model.openTrackPicker() }
                    .accessibilityLabel("\(model.episode.label). \(model.isPlaying ? "Playing" : "Paused")")
                    .accessibilityHint("Press to show playback controls")
            }

            // Transport row only while it is the active layer: the picker and the next-episode card sit over
            // plain video, so no half-covered buttons or time readouts ghost through them.
            if model.overlay == .controls {
                TransportControls(model: model, focus: $focus, scope: playerScope)
                    .transition(reduceMotion ? .opacity : .opacity.combined(with: .move(edge: .bottom)))
            }

            if model.overlay == .trackPicker {
                TrackPickerSheet(model: model, focus: $focus)
                    .transition(reduceMotion ? .opacity : .move(edge: .trailing))
            }

            if model.overlay == .nextEpisode, let next = model.nextEpisode {
                NextEpisodePrompt(model: model, next: next, focus: $focus)
                    .transition(.opacity)
            }

            if model.isBuffering {
                // `.controlSize` is unavailable on tvOS; scale the indicator instead.
                ProgressView().scaleEffect(1.6).tint(.white).accessibilityLabel("Loading")
            }
        }
        .background(Color.black)                     // deliberate pure black only behind video (letterboxing)
        .focusScope(playerScope)
        .animation(reduceMotion ? nil : .easeOut(duration: 0.2), value: model.overlay)
        .onPlayPauseCommand { model.togglePlayPause() }          // media key works without the overlay
        .onExitCommand { model.handleMenu() }                    // Menu: unwind one layer
        .onChange(of: model.overlay) { old, new in
            // Focus management on layer changes: restore, never drop.
            switch new {
            case .controls:
                // First show lands on Play/Pause (lastControlFocus starts there); later shows restore the last control.
                focus = lastControlFocus
            case .trackPicker:
                focus = .picker(model.selectedSubtitle.id)
            case .nextEpisode:
                focus = .playNext
            case .none:
                focus = .surface
            }
        }
        .onChange(of: focus) { _, new in
            if let new, new.isTransportControl { lastControlFocus = new; model.touch() }
        }
        .onChange(of: model.wantsToLeave) { _, leave in if leave { dismiss() } }
        .onAppear { model.play(); focus = .surface }
        .onDisappear { model.pause() }
        .persistentSystemOverlays(.hidden)
    }
}

enum PlayerFocus: Hashable {
    case surface
    case skipBack, playPause, skipForward, tracks, next, scrubber
    case picker(String)
    case playNext, watchCredits

    var isTransportControl: Bool {
        switch self {
        case .skipBack, .playPause, .skipForward, .tracks, .next, .scrubber: return true
        default: return false
        }
    }
}
