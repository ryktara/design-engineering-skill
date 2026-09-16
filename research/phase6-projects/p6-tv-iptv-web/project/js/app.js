/* Meridian TV — screens and routing */
(function (global) {
  'use strict';

  var D = global.Data, F = global.Focus, K = global.Keys.KEY;
  var $screen = document.getElementById('screen');
  var $nav = document.getElementById('topnav');
  var stack = [];
  var currentScreen = null;
  var playerTimer = null;

  function h(tag, cls, html) {
    var el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html != null) el.innerHTML = html;
    return el;
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmtTime(ms) { var d = new Date(ms); return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function fmtClock(sec) { return pad(Math.floor(sec / 60)) + ':' + pad(sec % 60); }

  // ---------- clock ----------
  function tickClock() {
    document.getElementById('clock').textContent = fmtTime(Date.now());
  }
  setInterval(tickClock, 10000);
  tickClock();

  // ---------- routing ----------
  function show(name, params, push) {
    if (currentScreen && currentScreen.destroy) currentScreen.destroy();
    if (push !== false && currentScreen) stack.push({ name: currentScreen.name, params: currentScreen.params });
    $screen.innerHTML = '';
    F.clear();
    var screens = { home: HomeScreen, guide: GuideScreen, detail: DetailScreen, player: PlayerScreen, settings: SettingsScreen };
    currentScreen = screens[name](params || {});
    currentScreen.name = name;
    currentScreen.params = params;
    var navItems = $nav.querySelectorAll('.nav-item');
    for (var i = 0; i < navItems.length; i++) navItems[i].classList.toggle('active', navItems[i].dataset.screen === name);
    document.getElementById('topbar').classList.toggle('hidden', name === 'player');
    F.focusFirst($screen);
  }

  function back() {
    var prev = stack.pop();
    if (!prev) return false;
    show(prev.name, prev.params, false);
    return true;
  }

  // top nav clicks
  var navButtons = $nav.querySelectorAll('.nav-item');
  for (var n = 0; n < navButtons.length; n++) {
    navButtons[n].addEventListener('click', function () { stack.length = 0; show(this.dataset.screen); });
  }

  // ---------- Home ----------
  function card(item) {
    var p = item.p, ch = item.ch;
    var el = h('div', 'card focusable');
    el.tabIndex = -1;
    el.style.setProperty('--art-a', p.art[0]);
    el.style.setProperty('--art-b', p.art[1]);
    var html = '<div class="card-art"></div>';
    if (item.live) html += '<span class="card-badge">LIVE</span>';
    html += '<div class="card-meta"><div class="card-title">' + p.title + '</div>' +
      '<div class="card-sub">' + ch.name + ' · ' + fmtTime(p.start) + '</div></div>';
    if (item.progress) html += '<div class="card-progress"><i style="width:' + Math.round(item.progress * 100) + '%"></i></div>';
    el.innerHTML = html;
    el.addEventListener('click', function () { show('detail', { id: p.id }); });
    return el;
  }

  function HomeScreen() {
    var root = h('div', 'home');
    D.rails.forEach(function (rail) {
      var r = h('section', 'rail');
      r.appendChild(h('h2', 'rail-title', rail.title));
      var track = h('div', 'rail-track');
      track.dataset.focusScope = rail.id;
      track.setAttribute('data-focus-rail', '');
      rail.items.forEach(function (it) { track.appendChild(card(it)); });
      r.appendChild(track);
      root.appendChild(r);
    });
    $screen.appendChild(root);

    // Scroll rail horizontally and page vertically to keep focus in view.
    var off = F.onChange(function (el) {
      var track = el.closest('.rail-track');
      if (!track) return;
      var idx = Array.prototype.indexOf.call(track.children, el);
      var cardW = el.offsetWidth + 24;
      var x = Math.max(0, idx - 1) * cardW;
      if (idx === 0) x = 0;
      track.style.transform = 'translateX(' + (-x) + 'px)';
      var rail = track.closest('.rail');
      var railIdx = Array.prototype.indexOf.call(root.children, rail);
      root.style.transform = 'translateY(' + (-railIdx * (el.offsetHeight + 36 + 60)) + 'px)';
      root.style.transition = 'transform 180ms ease-out';
    });
    return { destroy: function () {} };
  }

  // ---------- Guide ----------
  function GuideScreen() {
    var root = h('div', 'guide');
    var slotW = 240, chW = 260, rowH = 88;
    var slots = D.GUIDE_HOURS * 2;
    var msPerPx = 30 * 60000 / slotW;

    // Header: a fixed anchor in the channel-column gutter that always names the
    // time at the left edge of the visible window, then a clipped track of
    // half-hour labels that scrolls by the same pixel offset as the rows.
    var header = h('div', 'guide-header');
    var anchor = h('div', 'guide-anchor',
      '<span class="anchor-label">From</span><span class="anchor-time" id="guideAnchorTime">--:--</span>' +
      '<span class="nowkey" title="Green key: jump to now">NOW</span>');
    var headerTrack = h('div', 'guide-header-track');
    var headerSlots = h('div', 'guide-slots');
    for (var i = 0; i < slots; i++) {
      headerSlots.appendChild(h('div', 'slot', fmtTime(D.guideStart + i * 30 * 60000)));
    }
    headerTrack.appendChild(headerSlots);
    // Edge marker: when the now-line is scrolled out of view, the header says
    // which way the live edge is and at what time.
    var nowEdge = h('div', 'now-edge hidden');
    headerTrack.appendChild(nowEdge);
    header.appendChild(anchor);
    header.appendChild(headerTrack);
    root.appendChild(header);

    var body = h('div', 'guide-body');
    var rows = h('div', 'guide-rows');
    var cellTracks = [];
    D.channels.forEach(function (ch, ci) {
      var row = h('div', 'guide-row');
      row.appendChild(h('div', 'guide-ch', '<span class="num">' + ch.number + '</span><span class="name">' + ch.name + '</span>'));
      var cells = h('div', 'guide-cells');
      cells.dataset.focusScope = 'row' + ci;
      ch.programmes.forEach(function (p) {
        var s = Math.max(p.start, D.guideStart);
        var e = Math.min(p.end, D.guideStart + D.GUIDE_HOURS * 3600000);
        if (e <= s) return;
        var c = h('div', 'guide-cell focusable');
        c.tabIndex = -1;
        c.style.width = ((e - s) / 60000 / 30 * slotW - 4) + 'px';
        c.style.marginLeft = (s === p.start ? 0 : 0) + 'px';
        if (p.end <= Date.now()) c.classList.add('past');
        c.innerHTML = '<div class="t">' + p.title + '</div><div class="s">' + fmtTime(p.start) + ' – ' + fmtTime(p.end) + '</div>';
        c.dataset.start = p.start;
        c.dataset.end = p.end;
        c.addEventListener('click', function () { show('detail', { id: p.id }); });
        cells.appendChild(c);
      });
      row.appendChild(cells);
      rows.appendChild(row);
      cellTracks.push(cells);
    });
    body.appendChild(rows);

    var nowLine = h('div', 'now-line');
    body.appendChild(nowLine);
    root.appendChild(body);
    $screen.appendChild(root);

    // Continuous pixel scrolling. The timeline never snaps to the half-hour: it
    // moves the smallest distance that keeps the focused programme on screen, so
    // the labels you were reading stay where they were.
    var scrollX = 0, scrollY = 0;
    var timelineW = slots * slotW;
    var keepX = 64, keepY = rowH;   // keep-in-view margins

    function viewW() { return Math.max(0, body.clientWidth - chW); }
    function viewH() { return body.clientHeight; }
    function maxX() { return Math.max(0, timelineW - viewW()); }
    function maxY() { return Math.max(0, rows.children.length * rowH - viewH()); }

    function applyScroll() {
      headerSlots.style.transform = 'translateX(' + (-scrollX) + 'px)';
      cellTracks.forEach(function (t) { t.style.transform = 'translateX(' + (-scrollX) + 'px)'; });
      rows.style.transform = 'translateY(' + (-scrollY) + 'px)';
      document.getElementById('guideAnchorTime').textContent = fmtTime(D.guideStart + scrollX * msPerPx);
      var nowX = chW + (Date.now() - D.guideStart) / msPerPx - scrollX;
      nowLine.style.left = nowX + 'px';
      var visible = nowX >= chW && nowX <= chW + viewW();
      nowLine.style.display = visible ? 'block' : 'none';
      nowEdge.classList.toggle('hidden', visible);
      nowEdge.classList.toggle('right', nowX > chW);
      nowEdge.textContent = fmtTime(Date.now());
    }

    // Scroll only as far as needed to bring the focused cell fully into view.
    function ensureVisibleX(left, width) {
      var lead = Math.min(keepX, Math.max(0, (viewW() - width) / 2));
      if (left - lead < scrollX) scrollX = left - lead;
      else if (left + width + lead > scrollX + viewW()) scrollX = left + width + lead - viewW();
      scrollX = Math.max(0, Math.min(scrollX, maxX()));
    }
    function ensureVisibleY(top) {
      var lead = Math.min(keepY, Math.max(0, (viewH() - rowH) / 2));
      if (top - lead < scrollY) scrollY = top - lead;
      else if (top + rowH + lead > scrollY + viewH()) scrollY = top + rowH + lead - viewH();
      scrollY = Math.max(0, Math.min(scrollY, maxY()));
    }

    var off = F.onChange(function (el) {
      if (!el.classList.contains('guide-cell')) return;
      var row = el.closest('.guide-row');
      var ri = Array.prototype.indexOf.call(rows.children, row);
      ensureVisibleY(ri * rowH);
      ensureVisibleX(el.offsetLeft, el.offsetWidth);
      applyScroll();
    });

    // Jump back to now: scroll the live edge into view and focus the cell on air
    // in the current row, so GREEN always recovers your place.
    function jumpToNow() {
      var cur = F.getCurrent();
      var row = cur && cur.closest ? cur.closest('.guide-row') : null;
      var ri = row ? Array.prototype.indexOf.call(rows.children, row) : 0;
      var track = cellTracks[Math.max(0, ri)];
      var now = Date.now(), target = null;
      if (track) {
        var cells = track.children;
        for (var j = 0; j < cells.length; j++) {
          var s = +cells[j].dataset.start, e = +cells[j].dataset.end;
          if (s <= now && e > now) { target = cells[j]; break; }
        }
        if (!target) target = cells[cells.length - 1] || null;
      }
      if (target) F.setFocus(target);
      else { scrollX = Math.max(0, Math.min((now - D.guideStart) / msPerPx - viewW() / 3, maxX())); applyScroll(); }
    }

    applyScroll();
    var nowTimer = setInterval(applyScroll, 30000);
    return {
      destroy: function () { clearInterval(nowTimer); },
      onKey: function (k) {
        if (k === K.GREEN) { jumpToNow(); return true; }
        return false;
      }
    };
  }

  // ---------- Detail ----------
  function DetailScreen(params) {
    var found = D.findProgramme(params.id);
    var p = found.p, ch = found.ch;
    var root = h('div', 'detail');
    var art = h('div', 'detail-art');
    art.style.setProperty('--art-a', p.art[0]);
    art.style.setProperty('--art-b', p.art[1]);
    root.appendChild(art);
    var info = h('div', 'detail-info');
    info.appendChild(h('h1', 'detail-title', p.title));
    info.appendChild(h('div', 'detail-meta', ch.name + ' · ' + fmtTime(p.start) + ' – ' + fmtTime(p.end) + ' · ' + p.rating + ' · HD'));
    info.appendChild(h('p', 'detail-desc', p.desc));
    var btns = h('div', 'btn-row');
    btns.dataset.focusScope = 'detail-actions';
    var play = h('button', 'btn primary focusable', p.end > Date.now() && p.start <= Date.now() ? 'Watch live' : 'Play');
    play.addEventListener('click', function () { show('player', { id: p.id }); });
    var rec = h('button', 'btn focusable', 'Record');
    rec.addEventListener('click', function () { rec.textContent = 'Recording set'; });
    var fav = h('button', 'btn focusable', 'Add to favourites');
    fav.addEventListener('click', function () { fav.textContent = 'In favourites'; });
    btns.appendChild(play); btns.appendChild(rec); btns.appendChild(fav);
    info.appendChild(btns);
    root.appendChild(info);
    $screen.appendChild(root);
    return { destroy: function () {} };
  }

  // ---------- Player ----------
  function PlayerScreen(params) {
    var found = D.findProgramme(params.id);
    var p = found.p, ch = found.ch;
    var duration = Math.round((p.end - p.start) / 1000);
    var pos = 0, playing = true, subs = false;

    var root = h('div', 'player');
    root.appendChild(h('div', 'video'));
    var ov = h('div', 'overlay');
    ov.innerHTML = '<div class="overlay-title">' + p.title + '</div>' +
      '<div class="overlay-sub">' + ch.name + ' · ' + fmtTime(p.start) + ' – ' + fmtTime(p.end) + '</div>' +
      '<div class="progress"><i id="pbar"></i></div>' +
      '<div class="times"><span id="tcur">00:00</span><span id="tdur">' + fmtClock(duration) + '</span></div>';
    var ctls = h('div', 'controls');
    ctls.dataset.focusScope = 'player-controls';

    var playBtn = h('button', 'ctl focusable');
    playBtn.setAttribute('aria-label', 'Pause');
    playBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
    playBtn.addEventListener('click', togglePlay);

    var subBtn = h('button', 'ctl focusable');
    subBtn.setAttribute('aria-label', 'Subtitles off');
    subBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M3 5h18v14H3zM5 7v10h14V7zM7 10h4v1.5H7zM12 10h5v1.5h-5zM7 13h5v1.5H7zM13 13h4v1.5h-4z"/></svg>';
    subBtn.addEventListener('click', function () {
      subs = !subs;
      subBtn.setAttribute('aria-label', subs ? 'Subtitles on' : 'Subtitles off');
      subBtn.style.color = subs ? 'var(--accent)' : '';
    });

    ctls.appendChild(playBtn);
    ctls.appendChild(subBtn);
    ov.appendChild(ctls);
    root.appendChild(ov);
    $screen.appendChild(root);

    // ----- overlay auto-hide -----
    // The overlay is transient: it appears on any remote input and hides after
    // OVERLAY_MS of no input, so the picture is unobstructed for the whole
    // programme. It never hides while playback is paused.
    var OVERLAY_MS = 5000;
    var overlayVisible = true, hideTimer = null, lastFocus = playBtn;

    function hideOverlay() {
      if (!overlayVisible) return;
      clearTimeout(hideTimer); hideTimer = null;
      if (!playing) return;              // paused: controls stay up
      var cur = F.getCurrent();
      if (cur && ov.contains(cur)) lastFocus = cur;
      overlayVisible = false;
      ov.classList.add('overlay-hidden');
      ov.setAttribute('aria-hidden', 'true');
      // aria-hidden must never wrap focusable controls: take them out of the
      // tab order too (inert where the platform has it, tabindex elsewhere).
      ov.inert = true;
      playBtn.tabIndex = -1; subBtn.tabIndex = -1;
      F.clear();                         // no focus target while controls are gone
    }

    function showOverlay() {
      if (!overlayVisible) {
        overlayVisible = true;
        ov.classList.remove('overlay-hidden');
        ov.removeAttribute('aria-hidden');
        ov.inert = false;
        playBtn.tabIndex = 0; subBtn.tabIndex = 0;
        F.setFocus(lastFocus || playBtn); // focus returns where it was
      }
      resetHideTimer();
    }

    function resetHideTimer() {
      clearTimeout(hideTimer);
      hideTimer = playing ? setTimeout(hideOverlay, OVERLAY_MS) : null;
    }
    resetHideTimer();

    function togglePlay() {
      playing = !playing;
      playBtn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
      playBtn.innerHTML = playing
        ? '<svg viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
        : '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>';
      resetHideTimer();
    }

    function tick() {
      if (playing && pos < duration) pos++;
      document.getElementById('pbar').style.width = (pos / duration * 100) + '%';
      document.getElementById('tcur').textContent = fmtClock(pos);
    }
    playerTimer = setInterval(tick, 1000);

    return {
      destroy: function () {
        clearInterval(playerTimer); playerTimer = null;
        clearTimeout(hideTimer); hideTimer = null;
      },
      onKey: function (k) {
        if (k === K.BACK || k === K.STOP) {
          // BACK leaves the player; it is not an "wake the overlay" key.
          if (k === K.STOP) { back(); return true; }
          return false;
        }
        var wasHidden = !overlayVisible;
        showOverlay();
        if (k === K.PLAY_PAUSE) { togglePlay(); return true; }
        if (k === K.PLAY) { if (!playing) togglePlay(); return true; }
        if (k === K.PAUSE) { if (playing) togglePlay(); return true; }
        if (k === K.FF) { pos = Math.min(duration, pos + 30); return true; }
        if (k === K.REW) { pos = Math.max(0, pos - 30); return true; }
        // The first d-pad / OK press only brings the controls back; it does not
        // also move focus or activate the control underneath it.
        if (wasHidden) return true;
        return false;
      }
    };
  }

  // ---------- Settings ----------
  function SettingsScreen() {
    var root = h('div', 'settings');
    root.appendChild(h('h1', null, 'Settings'));
    var list = h('div', 'settings-list');
    list.dataset.focusScope = 'settings';
    D.settings.forEach(function (s) {
      var row = h('div', 'settings-row focusable', '<span>' + s.label + '</span><span class="val">' + s.value + '</span>');
      row.tabIndex = -1;
      row.addEventListener('click', function () {
        var v = row.querySelector('.val');
        if (s.key === 'subs' || s.key === 'autoplay' || s.key === 'parental') v.textContent = v.textContent === 'On' ? 'Off' : 'On';
      });
      list.appendChild(row);
    });
    root.appendChild(list);
    $screen.appendChild(root);
    return { destroy: function () {} };
  }

  // ---------- global key handling ----------
  function handleKey(k, e) {
    if (currentScreen && currentScreen.onKey && currentScreen.onKey(k)) return true;
    if (k === K.BACK) {
      if (currentScreen.name === 'detail') {
        global.Keys.exitApp();
        return true;
      }
      if (!back()) {
        if (currentScreen.name !== 'home') { show('home'); }
        else { global.Keys.exitApp(); }
      }
      return true;
    }
    if (k === K.GUIDE) { show('guide'); return true; }
    if (k === K.UP && currentScreen.name !== 'player') {
      // From the first row of any screen, Up reaches the top navigation.
      var cur = F.getCurrent();
      if (cur && !cur.classList.contains('nav-item') && !F.move('up')) {
        var active = $nav.querySelector('.nav-item.active') || $nav.querySelector('.nav-item');
        F.setFocus(active);
      }
      return true;
    }
    if (k === K.DOWN) {
      var c = F.getCurrent();
      if (c && c.classList.contains('nav-item')) { F.focusFirst($screen); return true; }
    }
    return false;
  }

  global.App = { show: show, back: back, handleKey: handleKey };

  global.Keys.registerTizenKeys();
  show('home', {}, false);
})(window);
