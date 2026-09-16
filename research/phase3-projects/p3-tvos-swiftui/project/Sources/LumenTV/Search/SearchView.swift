import SwiftUI

/// Search (comp-search, tv variant): a dedicated screen, the *system* keyboard (never a custom one) via
/// `.searchable`, which on tvOS renders the keyboard with Siri dictation at the top and scrolls our content
/// beneath it; results are rails (Series / Episodes / Topics); with no query the screen offers recent searches
/// and topics to browse, and an empty result never dead-ends (guidance + topics rail).
///
/// Focus engine:
/// - The system search field/keyboard owns initial focus. DOWN from the keyboard enters the first rail
///   (`.focusSection()` per rail keeps LEFT/RIGHT inside a rail and UP/DOWN between rails).
/// - Menu inside the results returns focus to the keyboard (system behaviour of the search container);
///   Menu at the keyboard leaves the screen (tab bar).
/// - Cards use the shared `TVButtonStyle` ring + lift (`.tvCard`), so focus reads the same as the player.
struct SearchView: View {
    @State private var model = SearchModel()
    @State private var playing: Episode?
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        NavigationStack {
            SearchResultsView(model: model, onPlay: { playing = $0 })
                .navigationTitle("Search")
                .background(LumenColor.canvas.ignoresSafeArea())
        }
        .searchable(text: $model.query, placement: .automatic, prompt: "Titles, topics, places")
        .onSubmit(of: .search) { model.commit() }
        .fullScreenCover(item: $playing) { episode in
            PlayerView(episode: episode, queue: SampleCatalogue.allEpisodes.filter { $0.series == episode.series && $0.id != episode.id })
        }
        .onChange(of: model.announcement) { _, text in
            if let text { AccessibilityNotification.Announcement(text).post() }   // "12 results for deep"
        }
        .animation(reduceMotion ? nil : .easeInOut(duration: 0.2), value: model.phase)
    }
}

/// Which rail holds focus, shared by every rail on the screen. A rail binds itself with `.focused($focusedRail,
/// equals: id)` on its container: the binding is set when focus enters any card in that rail. Rails whose id is not
/// the focused one rest at `LumenFocus.restingRowOpacity`, so the focused ROW is obvious from the sofa even before the
/// eye finds the focused card. When focus is elsewhere (search field / keyboard) no rail is focused and none dims.
struct SearchResultsView: View {
    @Bindable var model: SearchModel
    var onPlay: (Episode) -> Void
    @FocusState private var focusedRail: String?

    var body: some View {
        ScrollView(.vertical) {
            VStack(alignment: .leading, spacing: LumenSpace.xl) {
                switch model.phase {
                case .idle:
                    if !model.recent.isEmpty {
                        TextTileRail(title: "Recent searches", items: model.recent.map { ($0, $0) }) { model.useRecent($0) }
                            .railFocus("recent", focused: $focusedRail)
                    }
                    TextTileRail(title: "Browse topics", items: SampleCatalogue.topics.map { ($0.id, $0.name) }) { id in
                        if let t = SampleCatalogue.topics.first(where: { $0.id == id }) { model.query = t.name }
                    }
                    .railFocus("browse", focused: $focusedRail)
                case .searching:
                    ProgressView().scaleEffect(1.6).tint(LumenColor.textSecondary).padding(.top, LumenSpace.xl)
                        .accessibilityLabel("Searching")
                case .results(let r):
                    Text("\(r.count) results for “\(r.query)”")
                        .font(LumenFont.caption).foregroundStyle(LumenColor.textSecondary)
                        .accessibilityHidden(true)   // announced via AccessibilityNotification instead
                    if !r.series.isEmpty {
                        CardRail(title: "Series", items: r.series.map { RailItem(id: $0.id, title: $0.title, subtitle: $0.synopsis, eyebrow: "Series") }) { id in
                            if let first = SampleCatalogue.allEpisodes.first(where: { $0.series.id == id }) { model.commit(); onPlay(first) }
                        }
                        .railFocus("series", focused: $focusedRail)
                    }
                    if !r.episodes.isEmpty {
                        CardRail(title: "Episodes", items: r.episodes.map { RailItem(id: $0.id, title: $0.title, subtitle: $0.series.title, eyebrow: "S\($0.seasonNumber) E\($0.episodeNumber) · \(Int($0.duration / 60)) min") }) { id in
                            if let e = SampleCatalogue.allEpisodes.first(where: { $0.id == id }) { model.commit(); onPlay(e) }
                        }
                        .railFocus("episodes", focused: $focusedRail)
                    }
                    if !r.topics.isEmpty {
                        TextTileRail(title: "Topics", items: r.topics.map { ($0.id, $0.name) }) { id in
                            if let t = SampleCatalogue.topics.first(where: { $0.id == id }) { model.query = t.name }
                        }
                        .railFocus("topics", focused: $focusedRail)
                    }
                case .empty(let q):
                    VStack(alignment: .leading, spacing: LumenSpace.s) {
                        Text("No results for “\(q)”").font(LumenFont.headline).foregroundStyle(LumenColor.textPrimary)
                        Text("Try a series name, a place or a topic — or hold the Siri button and say it.")
                            .font(LumenFont.caption).foregroundStyle(LumenColor.textSecondary)
                    }
                    .padding(.horizontal, LumenSpace.safeArea)
                    TextTileRail(title: "Browse topics", items: SampleCatalogue.topics.map { ($0.id, $0.name) }) { id in
                        if let t = SampleCatalogue.topics.first(where: { $0.id == id }) { model.query = t.name }
                    }
                    .railFocus("browse", focused: $focusedRail)
                }
            }
            .padding(.vertical, LumenSpace.l)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .scrollClipDisabled()   // lifted cards are not clipped by the scroll view
    }
}

struct RailItem: Identifiable, Hashable { let id: String; let title: String; let subtitle: String; let eyebrow: String }

/// Row-level focus cue: the rail that holds focus stays at full opacity, keeps a text.primary heading and shows an
/// accent marker beside it; every other rail rests at `LumenFocus.restingRowOpacity` with a text.secondary heading.
/// With no rail focused (search field / keyboard) every rail is `.neutral` and nothing dims or marks.
/// Opacity is applied to the whole rail (heading + cards) so the *row* reads as one unit from a distance; the
/// ring/fill/lift on the card still marks the exact item. Reduce Motion: the change is instant, not removed.
enum RailFocusState { case neutral, focused, resting }

private struct RailFocusModifier: ViewModifier {
    let id: String
    var focused: FocusState<String?>.Binding
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    private var state: RailFocusState {
        guard let f = focused.wrappedValue else { return .neutral }
        return f == id ? .focused : .resting
    }

    func body(content: Content) -> some View {
        let s = state
        content
            .environment(\.railFocusState, s)
            .focused(focused, equals: id)
            .opacity(s == .resting ? LumenFocus.restingRowOpacity : 1)
            .animation(reduceMotion ? nil : .easeOut(duration: LumenFocus.duration), value: s)
    }
}

private struct RailFocusStateKey: EnvironmentKey { static let defaultValue = RailFocusState.neutral }
extension EnvironmentValues {
    /// Whether the enclosing rail holds focus, rests while another rail does, or no rail holds focus.
    var railFocusState: RailFocusState {
        get { self[RailFocusStateKey.self] }
        set { self[RailFocusStateKey.self] = newValue }
    }
}

extension View {
    func railFocus(_ id: String, focused: FocusState<String?>.Binding) -> some View {
        modifier(RailFocusModifier(id: id, focused: focused))
    }
}

/// Rail heading with the row marker: accent bar (visible only while the rail holds focus, space always reserved)
/// + title in text.primary, or text.secondary while the rail rests.
struct RailHeading: View {
    let title: String
    @Environment(\.railFocusState) private var state

    var body: some View {
        HStack(spacing: LumenSpace.s) {
            Capsule()
                .fill(LumenColor.accent)
                .frame(width: LumenFocus.rowMarkerWidth, height: 30)
                .opacity(state == .focused ? 1 : 0)
                .accessibilityHidden(true)      // VoiceOver already announces the focused item; the bar is visual only
            Text(title).font(LumenFont.headline)
                .foregroundStyle(state == .resting ? LumenColor.textSecondary : LumenColor.textPrimary)
        }
        .padding(.horizontal, LumenSpace.safeArea)
        .accessibilityAddTraits(.isHeader)
    }
}

/// Caption under a rail card. A 400 pt card at 29 pt body type fits roughly 24 characters on one line, so any
/// longer series/episode title was silently truncated with no way to read it (there is no hover or tooltip on TV —
/// the remote only moves focus, so the *focused* card is the only place a longer form can be revealed).
///
/// Resting: title on one line, ellipsised. Focused: the same title expands to two lines
/// (tv-typography-distance: titles ≤ 2 lines at 10 foot), which covers every title in the catalogue.
/// The caption reserves the two-line height as one block at all times, so expanding on focus neither pushes the
/// subtitle down nor moves the rail below it — a focus change must not shift the layout of a rail.
/// The subtitle stays at one line: it is supporting metadata (synopsis / parent series), not the name the viewer
/// is trying to read, and a second reserved line would cost another 30 pt on every card.
/// VoiceOver is unaffected: the button's `accessibilityLabel` already carries the untruncated strings.
private struct RailCardCaption: View {
    let title: String
    let subtitle: String
    @Environment(\.isFocused) private var isFocused

    /// 29 pt body ≈ 38 pt per line × 2 + xs + 23 pt caption ≈ 30 pt = 114 pt, reserved whether focused or not.
    private let captionHeight: CGFloat = 114

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.xs) {
            Text(title)
                .font(LumenFont.body)
                .foregroundStyle(LumenColor.textPrimary)
                .lineLimit(isFocused ? 2 : 1)
                .truncationMode(.tail)
            Text(subtitle)
                .font(LumenFont.caption)
                .foregroundStyle(LumenColor.textSecondary)
                .lineLimit(1)
                .truncationMode(.tail)
        }
        .frame(width: 400, height: captionHeight, alignment: .topLeading)
        .clipped()
        .accessibilityHidden(true)   // the card button carries the full accessible name
    }
}

/// 16:9 artwork cards in a horizontal rail (card-poster-landscape): title below the art, eyebrow inside a scrim.
/// One `.focusSection()` per rail so LEFT/RIGHT stay in the rail and UP/DOWN move between rails.
struct CardRail: View {
    let title: String
    let items: [RailItem]
    var onSelect: (String) -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.s) {
            RailHeading(title: title)
            ScrollView(.horizontal) {
                LazyHStack(alignment: .top, spacing: LumenSpace.m) {
                    ForEach(items) { item in
                        Button { onSelect(item.id) } label: {
                            VStack(alignment: .leading, spacing: LumenSpace.xs) {
                                ZStack(alignment: .bottomLeading) {
                                    AsyncImage(url: URL(string: "https://cdn.example.com/art/\(item.id).jpg")) { $0.resizable().scaledToFill() } placeholder: { LumenColor.surface }
                                        .frame(width: 400, height: 225).clipped()
                                    LinearGradient(colors: [.clear, LumenColor.scrim.opacity(0.75)], startPoint: .top, endPoint: .bottom).frame(height: 90)
                                    Text(item.eyebrow.uppercased()).font(LumenFont.caption).tracking(1.5).foregroundStyle(LumenColor.textPrimary).padding(LumenSpace.s)
                                }
                                .frame(width: 400, height: 225)
                                .clipShape(RoundedRectangle(cornerRadius: LumenFocus.cornerRadius, style: .continuous))
                                RailCardCaption(title: item.title, subtitle: item.subtitle)
                            }
                            .frame(width: 400, alignment: .leading)
                        }
                        .buttonStyle(.tvCard)
                        .accessibilityLabel("\(item.title), \(item.subtitle). \(item.eyebrow)")
                    }
                }
                .scrollTargetLayout()
                .padding(.horizontal, LumenSpace.safeArea)
            }
            .scrollTargetBehavior(.viewAligned)
            .scrollClipDisabled()
            .focusSection()
        }
    }
}

/// Flat text tiles (topics, recent searches): the surface colour is the tile, the ring + lift is the focus.
struct TextTileRail: View {
    let title: String
    let items: [(String, String)]
    var onSelect: (String) -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.s) {
            RailHeading(title: title)
            ScrollView(.horizontal) {
                LazyHStack(spacing: LumenSpace.s) {
                    ForEach(items, id: \.0) { id, label in
                        Button(label) { onSelect(id) }.buttonStyle(.tvSecondary)
                    }
                }
                .scrollTargetLayout()
                .padding(.horizontal, LumenSpace.safeArea)
            }
            .scrollTargetBehavior(.viewAligned)
            .scrollClipDisabled()
            .focusSection()
        }
    }
}
