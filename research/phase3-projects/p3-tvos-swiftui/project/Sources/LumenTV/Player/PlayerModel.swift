import Foundation
import AVFoundation
import Observation

/// Playback + overlay state for the player. UI-facing state only; AVPlayer owns the media.
@Observable
final class PlayerModel {
    enum Overlay: Equatable { case none, controls, trackPicker, nextEpisode }

    let player: AVPlayer
    private(set) var episode: Episode
    private(set) var queue: [Episode]

    var overlay: Overlay = .none
    var isPlaying = false
    var currentTime: TimeInterval = 0
    var duration: TimeInterval
    var isBuffering = false
    var selectedSubtitle: MediaTrack
    var selectedAudio: MediaTrack
    var nextEpisodeCountdown: Int?
    var didDismissNextPrompt = false
    /// Set when Menu is pressed with nothing left to unwind; the host pops the player.
    var wantsToLeave = false

    private var hideTask: Task<Void, Never>?
    private var countdownTask: Task<Void, Never>?
    private var timeObserver: Any?

    init(episode: Episode, queue: [Episode]) {
        self.episode = episode
        self.queue = queue
        self.duration = episode.duration
        self.player = AVPlayer(url: episode.streamURL)
        self.selectedSubtitle = SampleCatalogue.subtitleTracks[0]
        self.selectedAudio = SampleCatalogue.audioTracks[0]
        observeTime()
    }

    deinit { if let o = timeObserver { player.removeTimeObserver(o) } }

    // MARK: Transport

    func play() { player.play(); isPlaying = true }
    func pause() { player.pause(); isPlaying = false }
    func togglePlayPause() { isPlaying ? pause() : play() }

    func seek(by delta: TimeInterval) { seek(to: currentTime + delta) }

    func seek(to t: TimeInterval) {
        let clamped = min(max(0, t), duration)
        currentTime = clamped
        player.seek(to: CMTime(seconds: clamped, preferredTimescale: 600), toleranceBefore: .zero, toleranceAfter: .zero)
        touch()
    }

    // MARK: Overlay lifecycle
    //
    // Controls: any remote interaction shows them; they hide after `controlsAutoHide` seconds of inactivity,
    // but never while the track picker or the next-episode prompt is open.

    /// Call on every remote event that reaches the player (move, select, play/pause).
    func touch() {
        if overlay == .none { overlay = .controls }
        scheduleAutoHide()
    }

    func showControls() { overlay = .controls; scheduleAutoHide() }
    func hideControls() { hideTask?.cancel(); if overlay == .controls { overlay = .none } }

    private func scheduleAutoHide() {
        hideTask?.cancel()
        guard overlay == .controls else { return }
        hideTask = Task { [weak self] in
            try? await Task.sleep(for: .seconds(LumenTiming.controlsAutoHide))
            guard let self, !Task.isCancelled, self.overlay == .controls else { return }
            self.overlay = .none
        }
    }

    func openTrackPicker() { hideTask?.cancel(); overlay = .trackPicker }
    func closeTrackPicker() { overlay = .controls; scheduleAutoHide() }

    func select(_ track: MediaTrack) {
        switch track.kind {
        case .subtitle: selectedSubtitle = track
        case .audio: selectedAudio = track
        }
        applyTracks()
    }

    /// Menu / BACK semantics, one layer at a time:
    /// picker -> controls; next-episode prompt -> controls; controls visible -> hide them; nothing visible -> leave.
    func handleMenu() {
        switch overlay {
        case .trackPicker:
            closeTrackPicker()
        case .nextEpisode:
            didDismissNextPrompt = true
            countdownTask?.cancel()
            nextEpisodeCountdown = nil
            overlay = .controls
            scheduleAutoHide()
        case .controls:
            hideControls()
        case .none:
            wantsToLeave = true
        }
    }

    // MARK: Next episode

    var nextEpisode: Episode? { queue.first }

    func playNext() {
        guard let next = nextEpisode else { return }
        countdownTask?.cancel(); nextEpisodeCountdown = nil
        queue.removeFirst()
        episode = next
        duration = next.duration
        currentTime = 0
        didDismissNextPrompt = false
        player.replaceCurrentItem(with: AVPlayerItem(url: next.streamURL))
        applyTracks()
        overlay = .none
        play()
    }

    private func maybeShowNextPrompt() {
        guard nextEpisode != nil, !didDismissNextPrompt, overlay == .none || overlay == .controls,
              currentTime >= episode.creditsStart else { return }
        hideTask?.cancel()
        overlay = .nextEpisode
        nextEpisodeCountdown = LumenTiming.nextEpisodeCountdown
        countdownTask = Task { [weak self] in
            while let self, let n = self.nextEpisodeCountdown, n > 0, !Task.isCancelled {
                try? await Task.sleep(for: .seconds(1))
                if Task.isCancelled { return }
                self.nextEpisodeCountdown = n - 1
            }
            if let self, !Task.isCancelled, self.nextEpisodeCountdown == 0 { self.playNext() }
        }
    }

    // MARK: Internals

    private func observeTime() {
        let interval = CMTime(seconds: 0.5, preferredTimescale: 600)
        timeObserver = player.addPeriodicTimeObserver(forInterval: interval, queue: .main) { [weak self] t in
            guard let self else { return }
            self.currentTime = t.seconds
            if let d = self.player.currentItem?.duration.seconds, d.isFinite, d > 0 { self.duration = d }
            self.isBuffering = self.player.timeControlStatus == .waitingToPlayAtSpecifiedRate
            self.maybeShowNextPrompt()
        }
    }

    /// Maps the picked tracks onto AVMediaSelection. "Off" clears the legible selection; otherwise the first option
    /// matching the locale is chosen. Captions styling itself follows the system Accessibility caption preferences.
    private func applyTracks() {
        guard let item = player.currentItem, let asset = item.asset as? AVURLAsset else { return }
        Task {
            if let legible = try? await asset.loadMediaSelectionGroup(for: .legible) {
                if selectedSubtitle.isOff {
                    item.select(nil, in: legible)
                } else if let code = selectedSubtitle.languageCode {
                    let options = AVMediaSelectionGroup.mediaSelectionOptions(from: legible.options, with: Locale(identifier: code))
                    if let opt = options.first { item.select(opt, in: legible) }
                }
            }
            if let audible = try? await asset.loadMediaSelectionGroup(for: .audible), let code = selectedAudio.languageCode {
                let options = AVMediaSelectionGroup.mediaSelectionOptions(from: audible.options, with: Locale(identifier: code))
                if let opt = options.first { item.select(opt, in: audible) }
            }
        }
    }
}

extension TimeInterval {
    var clockString: String {
        let s = max(0, Int(self))
        if s >= 3600 { return String(format: "%d:%02d:%02d", s / 3600, s / 60 % 60, s % 60) }
        return String(format: "%d:%02d", s / 60, s % 60)
    }
}
