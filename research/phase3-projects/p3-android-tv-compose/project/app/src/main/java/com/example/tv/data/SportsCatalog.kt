package com.example.tv.data

import androidx.compose.runtime.Immutable

/** Stable ids so focus restoration and LazyRow keys survive recomposition. */
@Immutable
data class Channel(val id: String, val number: Int, val name: String, val logoUrl: String)

@Immutable
data class Competition(val id: String, val name: String, val sport: String, val artUrl: String)

enum class EventStatus { LIVE, UPCOMING, REPLAY }

@Immutable
data class SportsEvent(
    val id: String,
    val title: String,            // "Arsenal v Liverpool"
    val competition: Competition,
    val channel: Channel,
    val status: EventStatus,
    val startEpochMin: Long,      // minutes since epoch, keeps arithmetic trivial and testable
    val durationMin: Int,
    val score: String? = null,    // "2 – 1" while live / after the game
    val clock: String? = null,    // "67'" / "Q3 4:12" / "Set 2"
    val artUrl: String,
    val synopsis: String,
) {
    val endEpochMin: Long get() = startEpochMin + durationMin

    /** 0f..1f of the broadcast elapsed at [nowMin]; null when not live. */
    fun progressAt(nowMin: Long): Float? =
        if (status != EventStatus.LIVE) null
        else ((nowMin - startEpochMin).coerceIn(0, durationMin.toLong()) / durationMin.toFloat())
}

enum class TrackKind { SUBTITLE, AUDIO }

/**
 * One selectable track of a broadcast, as the player's chooser shows it. [id] is stable per stream (Media3 exposes
 * the group id + track index; the sample uses readable ids). [language] is the BCP-47 tag used to remember the
 * household's preference across events; [label] is what the viewer reads ("English (CC)", "Spanish commentary");
 * [detail] is an optional second line (codec/channel layout, "Audio description") — text, never an icon alone.
 */
@Immutable
data class MediaTrack(val id: String, val kind: TrackKind, val language: String, val label: String, val detail: String? = null)

/** Tracks a stream offers. Subtitles may be empty (then the chooser shows "Off" only and says so). */
@Immutable
data class TrackList(val subtitles: List<MediaTrack>, val audio: List<MediaTrack>) {
    val hasSubtitles: Boolean get() = subtitles.isNotEmpty()
}

/** Current choice: [subtitleId] null = subtitles off; [audioId] always points at an audio track. */
@Immutable
data class TrackSelection(val subtitleId: String?, val audioId: String)

/** One row of the EPG entry tile: channel + now/next. */
@Immutable
data class EpgPreviewRow(val channel: Channel, val now: SportsEvent, val next: SportsEvent?)

@Immutable
data class Rail(val id: String, val title: String, val events: List<SportsEvent>)

/** Whole home payload. Loading / error / empty are modelled at the screen level (HomeUiState). */
@Immutable
data class HomeContent(
    val nowMin: Long,
    val liveNow: List<SportsEvent>,
    val epgPreview: List<EpgPreviewRow>,
    val rails: List<Rail>,
) {
    /** Hero defaults to the first live event; falls back to the first upcoming one. */
    val heroDefault: SportsEvent? get() = liveNow.firstOrNull() ?: rails.firstOrNull()?.events?.firstOrNull()
}

/** Static sample used by previews and the offline fixture; a real app maps this from the API DTOs. */
object SampleCatalog {
    private const val NOW = 29_800_000L // arbitrary "minutes since epoch" used consistently below

    private val sky1 = Channel("sky1", 401, "Sports 1", "https://img.example/logo/s1.png")
    private val sky2 = Channel("sky2", 402, "Sports 2", "https://img.example/logo/s2.png")
    private val eur1 = Channel("eur1", 410, "Euro Arena", "https://img.example/logo/ea.png")
    private val moto = Channel("moto", 415, "MotorMax", "https://img.example/logo/mm.png")
    private val tennis = Channel("ten", 420, "Court TV", "https://img.example/logo/ct.png")

    private val pl = Competition("pl", "Premier League", "Football", "https://img.example/comp/pl.jpg")
    private val f1 = Competition("f1", "Formula 1", "Motorsport", "https://img.example/comp/f1.jpg")
    private val nba = Competition("nba", "NBA", "Basketball", "https://img.example/comp/nba.jpg")
    private val atp = Competition("atp", "ATP Tour", "Tennis", "https://img.example/comp/atp.jpg")
    private val ucl = Competition("ucl", "Champions League", "Football", "https://img.example/comp/ucl.jpg")
    private val rugby = Competition("6n", "Six Nations", "Rugby", "https://img.example/comp/6n.jpg")

    private fun ev(
        id: String, title: String, comp: Competition, ch: Channel, status: EventStatus,
        startOffsetMin: Long, duration: Int, score: String? = null, clock: String? = null,
        synopsis: String = "",
    ) = SportsEvent(
        id, title, comp, ch, status, NOW + startOffsetMin, duration, score, clock,
        artUrl = "https://img.example/event/$id.jpg", synopsis = synopsis,
    )

    val liveNow = listOf(
        ev("e1", "Arsenal v Liverpool", pl, sky1, EventStatus.LIVE, -67, 115, "2 – 1", "67'",
            "Title race six-pointer at the Emirates. Saka opened the scoring before Salah levelled; Havertz restored the lead just before the hour."),
        ev("e2", "Singapore Grand Prix", f1, moto, EventStatus.LIVE, -48, 130, null, "Lap 31 / 62",
            "Night race under the lights. Safety car on lap 12 reshuffled the strategy across the field."),
        ev("e3", "Celtics @ Knicks", nba, sky2, EventStatus.LIVE, -95, 150, "88 – 84", "Q4 6:41",
            "Eastern Conference clash at the Garden."),
        ev("e4", "Alcaraz v Sinner — Final", atp, tennis, EventStatus.LIVE, -110, 180, "6-4 3-6 2-1", "Set 3",
            "Rematch of last year's final."),
        ev("e5", "Ireland v France", rugby, eur1, EventStatus.LIVE, -30, 110, "10 – 7", "38'",
            "Round 3 in Dublin."),
    )

    private val upcoming = listOf(
        ev("u1", "Real Madrid v Bayern", ucl, sky1, EventStatus.UPCOMING, 50, 120, synopsis = "Semi-final, first leg."),
        ev("u2", "Man City v Chelsea", pl, sky2, EventStatus.UPCOMING, 75, 115),
        ev("u3", "Lakers @ Warriors", nba, sky2, EventStatus.UPCOMING, 190, 150),
        ev("u4", "MotoGP Qualifying", f1, moto, EventStatus.UPCOMING, 95, 70),
        ev("u5", "Wales v Scotland", rugby, eur1, EventStatus.UPCOMING, 90, 110),
        ev("u6", "Women's Final", atp, tennis, EventStatus.UPCOMING, 80, 150),
    )

    private val replays = listOf(
        ev("r1", "Spurs v Newcastle", pl, sky1, EventStatus.REPLAY, -1440, 115, "1 – 1"),
        ev("r2", "Japanese Grand Prix", f1, moto, EventStatus.REPLAY, -2880, 130),
        ev("r3", "Heat @ Bucks", nba, sky2, EventStatus.REPLAY, -1300, 150, "101 – 97"),
        ev("r4", "Djokovic v Zverev", atp, tennis, EventStatus.REPLAY, -4000, 160, "7-6 6-3"),
        ev("r5", "England v Italy", rugby, eur1, EventStatus.REPLAY, -1500, 110, "27 – 24"),
        ev("r6", "Barcelona v Inter", ucl, sky1, EventStatus.REPLAY, -1600, 120, "3 – 3"),
    )

    /** Everything the catalogue knows about, for lookups by id and for related rails. */
    val allEvents: List<SportsEvent> get() = liveNow + upcoming + replays

    private fun sub(id: String, lang: String, label: String, detail: String? = null) = MediaTrack(id, TrackKind.SUBTITLE, lang, label, detail)
    private fun aud(id: String, lang: String, label: String, detail: String? = null) = MediaTrack(id, TrackKind.AUDIO, lang, label, detail)

    /**
     * Tracks a stream offers, keyed by the event's channel/competition. A real app reads `Player.currentTracks`
     * (Media3) after `onTracksChanged`; the sample mirrors what the broadcasters in the catalogue actually carry:
     * football has home/away commentary and an audio-description mix, motorsport has team radio, tennis has none
     * beyond the world feed, and one replay carries no subtitles at all so the "Off only" state is reachable.
     */
    fun tracksFor(event: SportsEvent): TrackList = when {
        event.id == "r4" -> TrackList(subtitles = emptyList(), audio = listOf(aud("a-en", "en", "English", "Stereo")))
        event.competition.sport == "Football" -> TrackList(
            subtitles = listOf(sub("s-en", "en", "English"), sub("s-en-cc", "en", "English (CC)", "Sound cues"), sub("s-es", "es", "Español"), sub("s-de", "de", "Deutsch"), sub("s-fr", "fr", "Français")),
            audio = listOf(aud("a-en", "en", "English", "5.1 surround"), aud("a-en-ad", "en", "English", "Audio description"), aud("a-es", "es", "Español", "Comentario"), aud("a-stadium", "und", "Stadium only", "No commentary")),
        )
        event.competition.sport == "Motorsport" -> TrackList(
            subtitles = listOf(sub("s-en", "en", "English"), sub("s-es", "es", "Español"), sub("s-it", "it", "Italiano")),
            audio = listOf(aud("a-en", "en", "English", "Stereo"), aud("a-radio", "en", "Team radio", "Commentary off"), aud("a-de", "de", "Deutsch")),
        )
        else -> TrackList(
            subtitles = listOf(sub("s-en", "en", "English"), sub("s-es", "es", "Español")),
            audio = listOf(aud("a-en", "en", "English", "Stereo"), aud("a-es", "es", "Español")),
        )
    }

    /**
     * Related rail for the details screen: same competition first (live, then upcoming, then replays follow the
     * source order), then the same sport. Never includes the event itself; capped so the rail stays scannable.
     */
    fun related(event: SportsEvent, max: Int = 8): List<SportsEvent> {
        val others = allEvents.filter { it.id != event.id }
        val sameCompetition = others.filter { it.competition.id == event.competition.id }
        val sameSport = others.filter { it.competition.id != event.competition.id && it.competition.sport == event.competition.sport }
        return (sameCompetition + sameSport).take(max)
    }

    val content = HomeContent(
        nowMin = NOW,
        liveNow = liveNow,
        epgPreview = listOf(
            EpgPreviewRow(sky1, liveNow[0], upcoming[0]),
            EpgPreviewRow(sky2, liveNow[2], upcoming[1]),
            EpgPreviewRow(moto, liveNow[1], upcoming[3]),
        ),
        rails = listOf(
            Rail("upcoming", "Coming up", upcoming),
            Rail("replays", "Catch up", replays),
            Rail("football", "Football", (liveNow + upcoming + replays).filter { it.competition.sport == "Football" }),
            Rail("motorsport", "Motorsport", (liveNow + upcoming + replays).filter { it.competition.sport == "Motorsport" }),
        ),
    )
}
