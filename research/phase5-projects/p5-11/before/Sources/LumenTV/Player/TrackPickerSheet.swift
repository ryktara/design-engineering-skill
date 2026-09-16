import SwiftUI

/// Subtitles/audio as a right-side sheet: the video stays visible (dimmed on the sheet side only).
/// Two vertical lists side by side; UP/DOWN inside a list, LEFT/RIGHT between lists (`focusSection` each).
/// Initial focus: the currently selected subtitle row (`prefersDefaultFocus`). Menu closes the sheet and
/// returns focus to the "Subtitles and audio" button (PlayerView restores `lastControlFocus`).
/// Selected ≠ focused: selection is a checkmark + accent text; focus is the raised row + ring.
struct TrackPickerSheet: View {
    @Bindable var model: PlayerModel
    var focus: FocusState<PlayerFocus?>.Binding
    @Namespace private var sheetScope

    var body: some View {
        HStack(spacing: 0) {
            Spacer(minLength: 0)
            HStack(alignment: .top, spacing: LumenSpace.xl) {
                // Audio labels ("English · Audio description") are longer: give that column the width so rows stay
                // one line high and the two columns' rows align.
                column(title: "Subtitles", tracks: SampleCatalogue.subtitleTracks, selected: model.selectedSubtitle, width: 380)
                column(title: "Audio", tracks: SampleCatalogue.audioTracks, selected: model.selectedAudio, width: 540)
            }
            .padding(LumenSpace.safeArea)
            .frame(maxHeight: .infinity, alignment: .top)
            .background(LumenColor.surface.opacity(0.96))
            .overlay(alignment: .leading) { Rectangle().fill(Color.white.opacity(0.08)).frame(width: 1) }
        }
        .ignoresSafeArea()
        .focusScope(sheetScope)
        .focusSection()
        .onExitCommand { model.closeTrackPicker() }
        .accessibilityAddTraits(.isModal)
    }

    private func column(title: String, tracks: [MediaTrack], selected: MediaTrack, width: CGFloat) -> some View {
        VStack(alignment: .leading, spacing: LumenSpace.s) {
            Text(title)
                .font(LumenFont.headline)
                .foregroundStyle(LumenColor.textSecondary)
                .accessibilityAddTraits(.isHeader)
                .padding(.bottom, LumenSpace.xs)
            ForEach(tracks) { track in
                TrackRow(track: track, isSelected: track == selected) { model.select(track) }
                    .focused(focus, equals: .picker(track.id))
                    .prefersDefaultFocus(track == model.selectedSubtitle, in: sheetScope)
            }
        }
        .frame(width: width, alignment: .leading)
        .focusSection()
    }
}

private struct TrackRow: View {
    let track: MediaTrack
    let isSelected: Bool
    let action: () -> Void
    @Environment(\.isFocused) private var isFocused

    var body: some View {
        Button(action: action) {
            HStack(spacing: LumenSpace.s) {
                Image(systemName: "checkmark")
                    .font(.system(size: 24, weight: .semibold))
                    .foregroundStyle(LumenColor.accent)
                    .opacity(isSelected ? 1 : 0)
                    .frame(width: 28)
                Text(track.displayName)
                    .font(LumenFont.body)
                    .foregroundStyle(isSelected ? LumenColor.accent : LumenColor.textPrimary)
                    .lineLimit(1)
                Spacer(minLength: 0)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .buttonStyle(.tvSecondary)
        .accessibilityAddTraits(isSelected ? [.isSelected] : [])
    }
}
