// MetroLink kiosk — application state machine.
//
// Screens: attract → choose-ticket → quantity → review → pay → printing → done
// Any screen can jump back to attract via the header button or the idle timer.

(function () {
  'use strict';

  var t = I18N.t;
  var F = FARES;

  var IDLE_MS = 20000;
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
  var pollTimer = null;
  var terminal = null; // fake card terminal session

  function resetState() {
    state.ticket = null; state.zone = null; state.qty = 1; state.promo = null; state.ref = null;
    $('#promo-code').value = '';
    setPromoMsg('', '');
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

  function touchIdle() { clearTimeout(idleTimer); idleTimer = setTimeout(goIdle, IDLE_MS); }
  function stopIdle() { clearTimeout(idleTimer); idleTimer = null; }

  function goIdle() {
    if (state.screen === 'printing') { touchIdle(); return; } // never interrupt the printer
    abortTerminal();
    resetState();
    show('attract');
  }

  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) {
    document.addEventListener(ev, function () {
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
        '<span class="ticket-card__name">' + tk.name + '</span>' +
        '<span class="ticket-card__desc">' + tk.desc + '</span>' +
        '<span class="ticket-card__price">from ' + F.formatMoney(tk.prices[1]) + '</span>';
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
      btn.textContent = z.label;
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
      ticket: tk.name,
      zone: state.zone,
      price: F.formatMoney(F.unitPrice(state.ticket, state.zone))
    });
    $('#qty-minus').disabled = state.qty <= 1;
    $('#qty-plus').disabled = state.qty >= tk.maxQty;
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
    $('#rv-ticket').textContent = tk.name;
    $('#rv-zones').textContent = z.label;
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

    $('#btn-pay-confirm').addEventListener('click', beginPayment);
    $('#btn-pay-cancel').addEventListener('click', function () { abortTerminal(); show('review'); });
  }

  function init() {
    I18N.applyAll(document);
    renderTicketGrid();
    renderZones();
    bind();
    show('attract');
  }

  document.addEventListener('DOMContentLoaded', init);

  // Exposed for the ops console / QA scripts.
  window.__kiosk = { state: state, show: show };
})();
