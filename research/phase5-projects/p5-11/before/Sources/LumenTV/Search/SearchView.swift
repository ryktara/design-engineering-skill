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

struct SearchResultsView: View {
    @Bindable var model: SearchModel
    var onPlay: (Episode) -> Void

    var body: some View {
        ScrollView(.vertical) {
            VStack(alignment: .leading, spacing: LumenSpace.xl) {
                switch model.phase {
                case .idle:
                    if !model.recent.isEmpty {
                        TextTileRail(title: "Recent searches", items: model.recent.map { ($0, $0) }) { model.useRecent($0) }
                    }
                    TextTileRail(title: "Browse topics", items: SampleCatalogue.topics.map { ($0.id, $0.name) }) { id in
                        if let t = SampleCatalogue.topics.first(where: { $0.id == id }) { model.query = t.name }
                    }
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
                    }
                    if !r.episodes.isEmpty {
                        CardRail(title: "Episodes", items: r.episodes.map { RailItem(id: $0.id, title: $0.title, subtitle: $0.series.title, eyebrow: "S\($0.seasonNumber) E\($0.episodeNumber) · \(Int($0.duration / 60)) min") }) { id in
                            if let e = SampleCatalogue.allEpisodes.first(where: { $0.id == id }) { model.commit(); onPlay(e) }
                        }
                    }
                    if !r.topics.isEmpty {
                        TextTileRail(title: "Topics", items: r.topics.map { ($0.id, $0.name) }) { id in
                            if let t = SampleCatalogue.topics.first(where: { $0.id == id }) { model.query = t.name }
                        }
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
                }
            }
            .padding(.vertical, LumenSpace.l)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .scrollClipDisabled()   // lifted cards are not clipped by the scroll view
    }
}

struct RailItem: Identifiable, Hashable { let id: String; let title: String; let subtitle: String; let eyebrow: String }

/// 16:9 artwork cards in a horizontal rail (card-poster-landscape): title below the art, eyebrow inside a scrim.
/// One `.focusSection()` per rail so LEFT/RIGHT stay in the rail and UP/DOWN move between rails.
struct CardRail: View {
    let title: String
    let items: [RailItem]
    var onSelect: (String) -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.s) {
            Text(title).font(LumenFont.headline).foregroundStyle(LumenColor.textPrimary)
                .padding(.horizontal, LumenSpace.safeArea)
                .accessibilityAddTraits(.isHeader)
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
                                Text(item.title).font(LumenFont.body).foregroundStyle(LumenColor.textPrimary).lineLimit(1)
                                Text(item.subtitle).font(LumenFont.caption).foregroundStyle(LumenColor.textSecondary).lineLimit(1)
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
            Text(title).font(LumenFont.headline).foregroundStyle(LumenColor.textPrimary)
                .padding(.horizontal, LumenSpace.safeArea)
                .accessibilityAddTraits(.isHeader)
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
