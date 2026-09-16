import Foundation

struct Series: Identifiable, Hashable {
    let id: String
    let title: String
    var synopsis: String = ""
    var topicIds: [String] = []
}

/// A theme the catalogue is tagged with ("Deep sea", "Volcanoes"); search matches topics as well as titles.
struct Topic: Identifiable, Hashable {
    let id: String
    let name: String
}

struct Episode: Identifiable, Hashable {
    let id: String
    let series: Series
    let seasonNumber: Int
    let episodeNumber: Int
    let title: String
    let synopsis: String
    let duration: TimeInterval
    /// Time at which the end credits start; the "next episode" prompt appears here.
    let creditsStart: TimeInterval
    let streamURL: URL
    let artworkURL: URL?

    var label: String { "S\(seasonNumber) E\(episodeNumber) · \(title)" }
}

struct SearchResults: Equatable {
    let query: String
    let series: [Series]
    let episodes: [Episode]
    let topics: [Topic]
    var count: Int { series.count + episodes.count + topics.count }
    var isEmpty: Bool { count == 0 }
}

enum TrackKind: Hashable { case subtitle, audio }

struct MediaTrack: Identifiable, Hashable {
    let id: String
    let kind: TrackKind
    let displayName: String     // "English", "English (SDH)", "Off"
    let languageCode: String?   // nil for "Off"
    var isOff: Bool { languageCode == nil }
}

enum SampleCatalogue {
    static let series = Series(id: "blue-frontier", title: "Blue Frontier",
                               synopsis: "Life in the ocean's last unexplored places.", topicIds: ["deep-sea", "oceans"])

    // MARK: Search index (a real app maps this from the catalogue API)

    static let topics: [Topic] = [
        Topic(id: "deep-sea", name: "Deep sea"), Topic(id: "oceans", name: "Oceans"), Topic(id: "volcanoes", name: "Volcanoes"),
        Topic(id: "arctic", name: "Arctic"), Topic(id: "deserts", name: "Deserts"), Topic(id: "space", name: "Space"),
        Topic(id: "cities", name: "Cities"), Topic(id: "wildlife", name: "Wildlife")
    ]

    static let allSeries: [Series] = [
        series,
        Series(id: "fire-below", title: "Fire Below", synopsis: "The volcanoes that shaped the continents.", topicIds: ["volcanoes"]),
        Series(id: "white-silence", title: "White Silence", synopsis: "A year at the edge of the Arctic ice.", topicIds: ["arctic", "wildlife"]),
        Series(id: "dry-country", title: "Dry Country", synopsis: "How life persists where rain does not fall.", topicIds: ["deserts", "wildlife"]),
        Series(id: "night-sky", title: "Night Sky", synopsis: "What the darkest places on Earth reveal above.", topicIds: ["space"]),
        Series(id: "concrete-jungle", title: "Concrete Jungle", synopsis: "The animals that moved into our cities.", topicIds: ["cities", "wildlife"])
    ]

    private static func ep(_ s: Series, _ season: Int, _ n: Int, _ title: String, _ synopsis: String, minutes: Int) -> Episode {
        Episode(id: "\(s.id)-s\(season)e\(n)", series: s, seasonNumber: season, episodeNumber: n, title: title, synopsis: synopsis,
                duration: TimeInterval(minutes * 60), creditsStart: TimeInterval(minutes * 60 - 110),
                streamURL: URL(string: "https://cdn.example.com/\(s.id)/s\(season)e\(n)/master.m3u8")!,
                artworkURL: URL(string: "https://cdn.example.com/\(s.id)/s\(season)e\(n)/backdrop.jpg"))
    }

    static let allEpisodes: [Episode] = {
        let bf = series, fb = allSeries[1], ws = allSeries[2], dc = allSeries[3], ns = allSeries[4], cj = allSeries[5]
        return [
            ep(bf, 1, 1, "The Sunlit Zone", "Where almost all ocean life begins.", minutes: 51),
            ep(bf, 1, 2, "Kelp Cathedrals", "Forests that grow half a metre a day.", minutes: 50),
            nextUp, queue[0],
            ep(bf, 1, 5, "The Deep Plain", "Four kilometres down, the largest habitat on Earth.", minutes: 53),
            ep(fb, 1, 1, "Ring of Fire", "Four hundred volcanoes and the people who live beside them.", minutes: 48),
            ep(fb, 1, 2, "Deep Vents", "Volcanoes under the sea and the life that feeds on them.", minutes: 49),
            ep(ws, 1, 1, "First Light", "The sun returns after four months of night.", minutes: 47),
            ep(ws, 1, 2, "Open Water", "The ice retreats and the whales arrive.", minutes: 50),
            ep(dc, 1, 1, "After the Rain", "Ten years of waiting, one week of bloom.", minutes: 46),
            ep(ns, 1, 1, "Dark Sky Country", "Chasing the last truly dark places.", minutes: 45),
            ep(cj, 1, 1, "Foxes of the Suburbs", "How a country animal learned the city.", minutes: 44)
        ]
    }()

    /// Simple case- and diacritic-insensitive contains match over titles, synopses and topic names.
    static func search(_ rawQuery: String) -> SearchResults {
        let q = rawQuery.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current).trimmingCharacters(in: .whitespaces)
        guard q.count >= 2 else { return SearchResults(query: rawQuery, series: [], episodes: [], topics: []) }
        func hit(_ s: String) -> Bool { s.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current).contains(q) }
        let topicHits = topics.filter { hit($0.name) }
        let seriesHits = allSeries.filter { s in hit(s.title) || hit(s.synopsis) || s.topicIds.contains { id in topicHits.contains { $0.id == id } } }
        let episodeHits = allEpisodes.filter { e in hit(e.title) || hit(e.synopsis) || seriesHits.contains(e.series) }
        return SearchResults(query: rawQuery, series: seriesHits, episodes: episodeHits, topics: topicHits)
    }

    static let nextUp = Episode(
        id: "bf-s1e3", series: series, seasonNumber: 1, episodeNumber: 3,
        title: "The Twilight Zone",
        synopsis: "Between 200 and 1,000 metres down, sunlight fades and the ocean's largest daily migration begins.",
        duration: 52 * 60 + 14, creditsStart: 50 * 60 + 20,
        streamURL: URL(string: "https://cdn.example.com/bf/s1e3/master.m3u8")!,
        artworkURL: URL(string: "https://cdn.example.com/bf/s1e3/backdrop.jpg"))

    static let queue: [Episode] = [
        Episode(id: "bf-s1e4", series: series, seasonNumber: 1, episodeNumber: 4,
                title: "Cold Seeps",
                synopsis: "Life without light: methane vents and the animals that farm them.",
                duration: 49 * 60 + 2, creditsStart: 47 * 60 + 30,
                streamURL: URL(string: "https://cdn.example.com/bf/s1e4/master.m3u8")!,
                artworkURL: URL(string: "https://cdn.example.com/bf/s1e4/backdrop.jpg"))
    ]

    static let subtitleTracks: [MediaTrack] = [
        MediaTrack(id: "sub-off", kind: .subtitle, displayName: "Off", languageCode: nil),
        MediaTrack(id: "sub-en", kind: .subtitle, displayName: "English", languageCode: "en"),
        MediaTrack(id: "sub-en-sdh", kind: .subtitle, displayName: "English (SDH)", languageCode: "en-SDH"),
        MediaTrack(id: "sub-es", kind: .subtitle, displayName: "Español", languageCode: "es"),
        MediaTrack(id: "sub-fr", kind: .subtitle, displayName: "Français", languageCode: "fr")
    ]
    static let audioTracks: [MediaTrack] = [
        MediaTrack(id: "aud-en", kind: .audio, displayName: "English · Dolby Atmos", languageCode: "en"),
        MediaTrack(id: "aud-en-ad", kind: .audio, displayName: "English · Audio description", languageCode: "en-AD"),
        MediaTrack(id: "aud-es", kind: .audio, displayName: "Español · Stereo", languageCode: "es")
    ]
}
