import Foundation

struct Series: Identifiable, Hashable {
    let id: String
    let title: String
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

enum TrackKind: Hashable { case subtitle, audio }

struct MediaTrack: Identifiable, Hashable {
    let id: String
    let kind: TrackKind
    let displayName: String     // "English", "English (SDH)", "Off"
    let languageCode: String?   // nil for "Off"
    var isOff: Bool { languageCode == nil }
}

enum SampleCatalogue {
    static let series = Series(id: "blue-frontier", title: "Blue Frontier")

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
