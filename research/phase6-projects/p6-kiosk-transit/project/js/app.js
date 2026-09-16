// MetroLink kiosk — application state machine.
//
// Screens: attract → choose-ticket → quantity → review → pay → printing → done
// Any screen can jump back to attract via the header button or the idle timer.

(function () {
  'use strict';

  var t = I18N.t;
  var F = FARES;

  // Idle handling is two-stage: after IDLE_WARN_MS without input the kiosk asks
  // "are you still there?" over the current screen, then clears the session
  // IDLE_GRACE_MS later. Only the explicit "I'm still here" button extends the
  // session — a passer-by brushing the screen must not keep a stranger's basket
  // alive on a shared public device.
  var IDLE_WARN_MS = 20000;
  var IDLE_GRACE_MS = 10000;
  var PRINT_MS = 3200;
  var DONE_MS = 12000;
  var TERMINAL_POLL_MS = 400;

  var $ = function (sel) { return document.querySelector(sel); };

  // ---------- State ----------

  var state = {
    screen: 'attract',
    ticket: null,      // ticket id
    zone: null,        // zone id (1..3)
    qty: 1,
    promo: null,       // { code, pct }
    ref: null
  };

  var idleTimer = null;
  var graceTimer = null;
  var countTimer = null;
  var graceLeft = 0;
  var pollTimer = null;
  var terminal = null; // fake card terminal session

  // Clears the previous customer completely: state, entered text and every bit of
  // selection still painted in the DOM. Anything left behind here shows up as a
  // half-bought ticket for the next person.
  function resetState() {
    state.ticket = null; state.zone = null; state.qty = 1; state.promo = null; state.ref = null;
    $('#promo-code').value = '';
    setPromoMsg('', '');
    I18N.setLang(I18N.DEFAULT_LANG); // shared device: the next passenger starts in the default language
    clearSelection('.ticket-card');
    clearSelection('.zone-chip');
    $('#qty-value').textContent = '1';
    $('#qty-total').textContent = F.formatMoney(0);
    $('#qty-summary').textContent = '';
    ['#rv-ticket', '#rv-zones', '#rv-qty', '#rv-total', '#pay-amount', '#done-ref'].forEach(function (sel) {
      $(sel).textContent = '';
    });
    var limit = $('#qty-limit');
    if (limit) limit.textContent = ''; // quantity-limit hint, if the qty screen has one
    $('#pay-terminal').className = 'pay__terminal';
    $('#btn-pay-confirm').disabled = false;
    updateChooseNext();
  }

  function clearSelection(sel) {
    var nodes = document.querySelectorAll(sel);
    for (var i = 0; i < nodes.length; i++) nodes[i].classList.remove('is-selected');
  }

  // ---------- Screen switching ----------

  function show(name) {
    var screens = document.querySelectorAll('.screen');
    for (var i = 0; i < screens.length; i++) {
      screens[i].classList.toggle('is-active', screens[i].getAttribute('data-screen') === name);
    }
    state.screen = name;
    document.body.setAttribute('data-screen', name);
    var enter = ENTER[name];
    if (enter) enter();
    if (name === 'attract') stopIdle(); else touchIdle();
  }

  // ---------- Idle handling ----------

  function touchIdle() {
    hideIdleWarning();
    clearTimeout(idleTimer);
    idleTimer = setTimeout(warnIdle, IDLE_WARN_MS);
  }

  function stopIdle() {
    hideIdleWarning();
    clearTimeout(idleTimer);
    idleTimer = null;
  }

  // Stage 1: ask before throwing the basket away.
  function warnIdle() {
    if (state.screen === 'printing' || state.screen === 'done') { touchIdle(); return; } // never interrupt the printer
    if (isWarning()) return;
    graceLeft = Math.round(IDLE_GRACE_MS / 1000);
    renderGrace();
    $('#idle-warn').hidden = false;
    $('#btn-idle-continue').focus();
    countTimer = setInterval(tickGrace, 1000);
    graceTimer = setTimeout(goIdle, IDLE_GRACE_MS);
  }

  function tickGrace() {
    graceLeft = Math.max(0, graceLeft - 1);
    renderGrace();
  }

  function renderGrace() {
    $('#idle-count').textContent = t(graceLeft === 1 ? 'idle.count_one' : 'idle.count_other', { n: graceLeft });
  }

  function isWarning() { return !$('#idle-warn').hidden; }

  function hideIdleWarning() {
    clearTimeout(graceTimer); graceTimer = null;
    clearInterval(countTimer); countTimer = null;
    $('#idle-warn').hidden = true;
  }

  // Stage 2: grace expired — clear everything and go back to attract.
  function goIdle() {
    hideIdleWarning();
    abortTerminal();
    resetState();
    show('attract');
  }

  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
    document.addEventListener(ev, function () {
      // While the warning is up, only its own buttons decide; incidental contact
      // must not silently keep the previous customer's session open.
      if (isWarning()) return;
      if (state.screen !== 'attract') touchIdle();
    }, { passive: true });
  });

  // ---------- Helpers ----------

  function currentTotal() {
    return F.total(state.ticket, state.zone, state.qty, state.promo ? state.promo.pct : 0);
  }

  function setPromoMsg(text, kind) {
    var el = $('#promo-msg');
    el.textContent = text;
    el.className = 'promo__msg' + (kind ? ' is-' + kind : '');
  }

  function makeRef() {
    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    var out = '';
    for (var i = 0; i < 8; i++) out += chars.charAt(Math.floor(Math.random() * chars.length));
    return out;
  }

  // ---------- Locale ----------

  // Fare and zone names live in the fare table (data.js, mirrored from
  // data/fares.json); the translations live in i18n.js keyed by the same ids.
  // The fare table stays the fallback so a new fare is never blank.
  function ticketName(tk) {
    var s = t('ticket.' + tk.id + '.name');
    return s === 'ticket.' + tk.id + '.name' ? tk.name : s;
  }
  function ticketDesc(tk) {
    var s = t('ticket.' + tk.id + '.desc');
    return s === 'ticket.' + tk.id + '.desc' ? tk.desc : s;
  }
  function zoneLabel(z) {
    var s = t('zone.' + z.id);
    return s === 'zone.' + z.id ? z.label : s;
  }

  // The switch sits in the persistent footer, so it is reachable from every
  // screen of the flow. Each option carries its own endonym ('Cymraeg', not
  // 'Welsh') plus the short code, and aria-pressed marks the current locale.
  function renderLangSwitch() {
    var wrap = $('#lang-switch');
    if (!wrap) return;
    wrap.innerHTML = '';
    I18N.LANGS.forEach(function (l) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'lang-btn';
      btn.setAttribute('data-lang', l.id);
      btn.setAttribute('lang', l.htmlLang);
      btn.setAttribute('aria-pressed', String(l.id === I18N.lang));
      btn.textContent = l.endonym;
      btn.addEventListener('click', function () { I18N.setLang(l.id); });
      wrap.appendChild(btn);
    });
  }

  function markLangSwitch() {
    var btns = document.querySelectorAll('.lang-btn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].setAttribute('aria-pressed', String(btns[i].getAttribute('data-lang') === I18N.lang));
    }
  }

  // Switching locale keeps the session: only the text is rebuilt. The lists
  // are re-rendered because their labels are built in JS, then the current
  // screen re-runs its enter hook so its computed copy is re-translated.
  function onLangChange() {
    markLangSwitch();
    renderTicketGrid();
    renderZones();
    if (state.ticket) selectTicket(state.ticket);
    if (state.zone) selectZone(state.zone);
    // Only screens whose copy is computed are re-run. 'printing' and 'done'
    // own timers and a reference number, and 'pay' owns a live terminal
    // session, so re-running their enter hooks would restart them.
    if (state.screen === 'quantity') renderQty();
    if (state.screen === 'review') renderReview();
    if (state.screen === 'pay') $('#pay-amount').textContent = F.formatMoney(currentTotal());
  }

  // ---------- Choose ticket ----------

  function renderTicketGrid() {
    var grid = $('#ticket-grid');
    grid.innerHTML = '';
    F.TICKETS.forEach(function (tk) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ticket-card';
      btn.setAttribute('data-ticket', tk.id);
      btn.innerHTML =
        '<span class="ticket-card__name">' + ticketName(tk) + '</span>' +
        '<span class="ticket-card__desc">' + ticketDesc(tk) + '</span>' +
        '<span class="ticket-card__price">' +
          t('choose.from', { price: F.formatMoney(tk.prices[1]) }) + '</span>';
      btn.addEventListener('click', function () { selectTicket(tk.id); });
      grid.appendChild(btn);
    });
  }

  function renderZones() {
    var wrap = $('#zone-opts');
    wrap.innerHTML = '';
    F.ZONES.forEach(function (z) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'zone-chip';
      btn.textContent = zoneLabel(z);
      btn.setAttribute('data-zone', z.id);
      btn.addEventListener('click', function () { selectZone(z.id); });
      wrap.appendChild(btn);
    });
  }

  function selectTicket(id) {
    state.ticket = id;
    var cards = document.querySelectorAll('.ticket-card');
    for (var i = 0; i < cards.length; i++) {
      cards[i].classList.toggle('is-selected', cards[i].getAttribute('data-ticket') === id);
    }
    updateChooseNext();
  }

  function selectZone(id) {
    state.zone = id;
    var chips = document.querySelectorAll('.zone-chip');
    for (var i = 0; i < chips.length; i++) {
      chips[i].classList.toggle('is-selected', Number(chips[i].getAttribute('data-zone')) === id);
    }
    updateChooseNext();
  }

  function updateChooseNext() {
    $('#btn-choose-next').disabled = !(state.ticket && state.zone);
  }

  // ---------- Quantity ----------

  function renderQty() {
    var tk = F.getTicket(state.ticket);
    $('#qty-value').textContent = state.qty;
    $('#qty-total').textContent = F.formatMoney(currentTotal());
    $('#qty-summary').textContent = t('qty.summary', {
      ticket: ticketName(tk),
      zone: state.zone,
      price: F.formatMoney(F.unitPrice(state.ticket, state.zone))
    });
    $('#qty-minus').disabled = state.qty <= 1;
    $('#qty-plus').disabled = state.qty >= tk.maxQty;
    $('#qty-limit').textContent = state.qty >= tk.maxQty
      ? tk.maxQty + ' tickets is the maximum for this fare.'
      : '';
  }

  function changeQty(delta) {
    var tk = F.getTicket(state.ticket);
    var next = state.qty + delta;
    if (next < 1 || next > tk.maxQty) return;
    state.qty = next;
    renderQty();
  }

  // ---------- Review ----------

  function renderReview() {
    var tk = F.getTicket(state.ticket);
    var z = F.getZone(state.zone);
    $('#rv-ticket').textContent = ticketName(tk);
    $('#rv-zones').textContent = zoneLabel(z);
    $('#rv-qty').textContent = state.qty + ' × ' + F.formatMoney(F.unitPrice(state.ticket, state.zone));
    $('#rv-total').textContent = F.formatMoney(currentTotal());
  }

  function applyPromo() {
    var raw = $('#promo-code').value.trim().toUpperCase();
    if (!raw) { setPromoMsg(t('promo.empty'), 'err'); return; }
    var pct = F.PROMOS[raw];
    if (!pct) {
      state.promo = null;
      setPromoMsg(t('promo.bad'), 'err');
    } else {
      state.promo = { code: raw, pct: pct };
      setPromoMsg(t('promo.ok', { code: raw, pct: pct }), 'ok');
    }
    renderReview();
  }

  // ---------- Pay (fake terminal) ----------

  // Simulates a card terminal that goes idle → reading → approved/declined.
  // Real hardware exposes a similar polled status endpoint over the local bridge.
  function startTerminal(amountPence) {
    var started = Date.now();
    var outcome = Math.random() < 0.9 ? 'approved' : 'declined';
    return {
      amount: amountPence,
      status: function () {
        var age = Date.now() - started;
        if (age < 1800) return 'idle';
        if (age < 4200) return 'reading';
        return outcome;
      },
      cancel: function () { outcome = 'cancelled'; started = -Infinity; }
    };
  }

  function renderPay() {
    var box = $('#pay-terminal');
    box.className = 'pay__terminal';
    $('#pay-status').textContent = t('pay.waiting');
    $('#pay-amount').textContent = F.formatMoney(currentTotal());
    $('#btn-pay-confirm').disabled = false;
  }

  function beginPayment() {
    if (terminal) return;
    $('#btn-pay-confirm').disabled = true;
    terminal = startTerminal(currentTotal());
    pollTerminal();
  }

  function pollTerminal() {
    clearTimeout(pollTimer);
    if (!terminal) return;
    var s = terminal.status();
    var box = $('#pay-terminal');
    var msg = $('#pay-status');

    if (s === 'reading') {
      box.className = 'pay__terminal is-reading';
      msg.textContent = t('pay.reading');
    } else if (s === 'approved') {
      box.className = 'pay__terminal is-approved';
      msg.textContent = t('pay.approved');
      terminal = null;
      setTimeout(function () { show('printing'); }, 900);
      return;
    } else if (s === 'declined') {
      box.className = 'pay__terminal is-declined';
      msg.textContent = t('pay.declined');
      terminal = null;
      $('#btn-pay-confirm').disabled = false;
      return;
    } else if (s === 'cancelled') {
      terminal = null;
      return;
    }
    pollTimer = setTimeout(pollTerminal, TERMINAL_POLL_MS);
  }

  function abortTerminal() { clearTimeout(pollTimer); if (terminal) { terminal.cancel(); terminal = null; } }

  // ---------- Printing / done ----------

  function renderPrinting() {
    state.ref = makeRef();
    setTimeout(function () {
      if (state.screen === 'printing') show('done');
    }, PRINT_MS);
  }

  function renderDone() {
    $('#done-ref').textContent = state.ref;
    setTimeout(function () {
      if (state.screen === 'done') { resetState(); show('attract'); }
    }, DONE_MS);
  }

  // ---------- Enter hooks ----------

  var ENTER = {
    'choose-ticket': function () { updateChooseNext(); },
    'quantity': renderQty,
    'review': renderReview,
    'pay': renderPay,
    'printing': renderPrinting,
    'done': renderDone
  };

  // ---------- Wiring ----------

  function bind() {
    $('#btn-begin').addEventListener('click', function () { show('choose-ticket'); });
    $('#btn-start-over').addEventListener('click', function () { abortTerminal(); resetState(); show('attract'); });

    $('#btn-choose-next').addEventListener('click', function () { show('quantity'); });

    $('#qty-minus').addEventListener('click', function () { changeQty(-1); });
    $('#qty-plus').addEventListener('click', function () { changeQty(1); });
    $('#btn-qty-back').addEventListener('click', function () { show('choose-ticket'); });
    $('#btn-qty-next').addEventListener('click', function () { show('review'); });

    $('#btn-promo-apply').addEventListener('click', applyPromo);
    $('#promo-code').addEventListener('keydown', function (e) { if (e.key === 'Enter') applyPromo(); });
    $('#btn-review-back').addEventListener('click', function () { show('quantity'); });
    $('#btn-review-pay').addEventListener('click', function () { show('pay'); });

    $('#btn-idle-continue').addEventListener('click', function () { touchIdle(); });
    $('#btn-idle-reset').addEventListener('click', function () { goIdle(); });

    $('#btn-pay-confirm').addEventListener('click', beginPayment);
    $('#btn-pay-cancel').addEventListener('click', function () { abortTerminal(); show('review'); });
  }

  function init() {
    I18N.applyAll(document);
    renderLangSwitch();
    I18N.onChange(onLangChange);
    renderTicketGrid();
    renderZones();
    bind();
    show('attract');
  }

  document.addEventListener('DOMContentLoaded', init);

  // Exposed for the ops console / QA scripts.
  window.__kiosk = { state: state, show: show, warnIdle: warnIdle, goIdle: goIdle };
})();
