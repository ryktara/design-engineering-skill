/* Deterministic catalogue data. Seeded PRNG so every run renders the same guide. */
(function (global) {
  'use strict';

  function rng(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  var CHANNELS = [
    ['Meridian One', 'entertainment'], ['Meridian Two', 'entertainment'], ['News 24', 'news'],
    ['Sport Central', 'sport'], ['Sport Central 2', 'sport'], ['Cinema Gold', 'movies'],
    ['Cinema Classics', 'movies'], ['Kids Zone', 'kids'], ['Junior', 'kids'],
    ['Documentary HD', 'factual'], ['Nature+', 'factual'], ['History Now', 'factual'],
    ['Music Box', 'music'], ['Retro Hits', 'music'], ['Comedy Central Europe', 'entertainment'],
    ['Drama Channel', 'entertainment'], ['Crime & Investigation Network', 'entertainment'],
    ['Lifestyle', 'lifestyle'], ['Food Network', 'lifestyle'], ['Travel Channel International', 'lifestyle'],
    ['Business Report', 'news'], ['World News Tonight Network', 'news'], ['Parliament', 'news'],
    ['Motor TV', 'sport'], ['Fight Night', 'sport'], ['Anime+', 'kids'],
    ['Sci-Fi Channel', 'movies'], ['Horror Vault', 'movies'], ['Local Live', 'entertainment'],
    ['Shopping Direct', 'lifestyle']
  ];

  var TITLES = {
    entertainment: ['The Late Round-Up', 'Family Matters Revisited', 'Quiz Masters', 'Evening Variety Show', 'Neighbourhood Watch: Season Finale Special', 'Studio Sessions', 'Celebrity Kitchen Disasters'],
    news: ['Headlines', 'World Report', 'Business Briefing', 'Morning Edition', 'Late Bulletin', 'Weather and Traffic Update', 'Politics Weekly: The Interview'],
    sport: ['Premier Football Live', 'Tennis: Open Semi-Final', 'Cycling Highlights', 'Motorsport Grand Prix Qualifying Session', 'Rugby Roundup', 'Boxing Classics'],
    movies: ['The Long Winter', 'Harbour Lights', 'Midnight Express to Nowhere', 'Second Chances', 'Station Eleven Point Five', 'A Quiet Kind of Storm', 'The Cartographer\'s Daughter'],
    kids: ['Rocket Pals', 'Dino Detectives', 'Pip and the Paint Pot', 'Adventures of Captain Cabbage and Friends', 'Learn to Draw', 'Puppet Playhouse'],
    factual: ['Planet of Ice', 'The Roman Frontier', 'Engineering Giants: Building the Impossible', 'Ocean Deep', 'Great Railway Journeys of the North', 'Secrets of the Pyramids'],
    music: ['Top 40 Countdown', 'Live from the Arena', 'Acoustic Hour', 'Decades: The Eighties', 'Video Vault', 'Late Night Chill'],
    lifestyle: ['Kitchen Rescue', 'Grand Designs of Europe', 'Escape to the Coast', 'Antique Hunters', 'Street Food Safari: Bangkok', 'Garden Makeover']
  };

  var DESC = 'An episode from the current series. Broadcast in HD with audio description and subtitles where available. Contains mild language and scenes some viewers may find distressing.';

  var ART = [['#5a2d82', '#1b1030'], ['#0f5c78', '#0a1f2a'], ['#8a3b12', '#2a1207'], ['#2d6a4f', '#0f2a1e'], ['#7a1f3d', '#2a0a14'], ['#3a4f9c', '#101a3a'], ['#9c6b00', '#2a1d00'], ['#444', '#111']];

  // Guide window: 6 hours starting on the half-hour before "now".
  var GUIDE_HOURS = 6;
  var SLOT_MIN = 30;

  function guideStart(now) {
    var d = new Date(now);
    d.setSeconds(0, 0);
    d.setMinutes(d.getMinutes() < 30 ? 0 : 30);
    return d.getTime();
  }

  function buildSchedule(start) {
    var rand = rng(20240917);
    var channels = CHANNELS.map(function (c, i) {
      var pool = TITLES[c[1]];
      var progs = [];
      var t = start - 15 * 60000 * Math.floor(rand() * 3); // stagger starts a little
      var end = start + GUIDE_HOURS * 3600000;
      var id = 0;
      while (t < end) {
        var durs = [30, 30, 60, 60, 90, 120, 45];
        var dur = durs[Math.floor(rand() * durs.length)];
        var title = pool[Math.floor(rand() * pool.length)];
        progs.push({
          id: 'p' + i + '-' + (id++),
          channel: i,
          title: title,
          start: t,
          end: t + dur * 60000,
          art: ART[Math.floor(rand() * ART.length)],
          desc: DESC,
          rating: ['U', 'PG', '12', '15'][Math.floor(rand() * 4)]
        });
        t += dur * 60000;
      }
      return { number: 101 + i, name: c[0], genre: c[1], programmes: progs };
    });
    return channels;
  }

  function buildRails(channels) {
    var rand = rng(77);
    function pick(n, filter) {
      var pool = [];
      channels.forEach(function (ch) {
        ch.programmes.forEach(function (p) { if (!filter || filter(ch, p)) pool.push({ p: p, ch: ch }); });
      });
      var out = [];
      while (out.length < n && pool.length) {
        out.push(pool.splice(Math.floor(rand() * pool.length), 1)[0]);
      }
      return out;
    }
    return [
      { id: 'continue', title: 'Continue watching', items: pick(10).map(function (x, i) { x.progress = 0.15 + (i * 0.08) % 0.7; return x; }) },
      { id: 'live', title: 'On now', items: pick(14, function (ch, p) { return p.start <= Date.now() && p.end > Date.now(); }).map(function (x) { x.live = true; return x; }) },
      { id: 'movies', title: 'Movies tonight', items: pick(12, function (ch) { return ch.genre === 'movies'; }) },
      { id: 'kids', title: 'For the kids', items: pick(12, function (ch) { return ch.genre === 'kids'; }) }
    ];
  }

  var start = guideStart(Date.now());
  var channels = buildSchedule(start);

  global.Data = {
    GUIDE_HOURS: GUIDE_HOURS,
    SLOT_MIN: SLOT_MIN,
    guideStart: start,
    channels: channels,
    rails: buildRails(channels),
    findProgramme: function (id) {
      for (var i = 0; i < channels.length; i++) {
        var ps = channels[i].programmes;
        for (var j = 0; j < ps.length; j++) if (ps[j].id === id) return { p: ps[j], ch: channels[i] };
      }
      return null;
    },
    settings: [
      { key: 'lang', label: 'Audio language', value: 'English' },
      { key: 'subs', label: 'Subtitles', value: 'Off' },
      { key: 'subsize', label: 'Subtitle size', value: 'Medium' },
      { key: 'quality', label: 'Streaming quality', value: 'Auto' },
      { key: 'autoplay', label: 'Autoplay next episode', value: 'On' },
      { key: 'parental', label: 'Parental controls', value: 'Off' },
      { key: 'account', label: 'Account', value: 'ryk@example.com' },
      { key: 'about', label: 'About Meridian TV', value: 'v1.4.2' }
    ]
  };
})(window);
