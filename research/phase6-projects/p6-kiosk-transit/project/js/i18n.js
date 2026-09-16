// MetroLink kiosk — UI strings.
//
// Two locales: English ('en') and Welsh ('cy'). English is the default and the
// fallback for any key a locale has not translated yet, so a missing Welsh
// string degrades to English rather than to a raw key.
//
// Welsh runs roughly 25–35% longer than English. The layout is fixed at
// 1080 × 1920 with no reflow, so nothing may be sized around the English
// string length — see the notes in css/kiosk.css next to .lang-switch.

(function (global) {
  'use strict';

  var DEFAULT_LANG = 'en';

  var LANGS = [
    { id: 'en', short: 'EN', endonym: 'English', htmlLang: 'en' },
    { id: 'cy', short: 'CY', endonym: 'Cymraeg', htmlLang: 'cy' }
  ];

  var STRINGS = {
    en: {
      'header.reset': 'Start over',

      'attract.title': 'Touch to buy a ticket',
      'attract.sub': 'Single, day pass, weekly and concession fares',
      'attract.cta': 'Start',

      'choose.title': 'Choose your ticket',
      'choose.zones': 'Zones',
      'choose.from': 'from {price}',

      'qty.title': 'How many tickets?',
      'qty.summary': '{ticket}, zones 1–{zone} · {price} each',
      'qty.total': 'Total',
      'qty.fewer': 'One ticket fewer',
      'qty.more': 'One ticket more',
      'idle.title': 'Are you still there?',
      'idle.body': 'Your ticket is still on screen. The kiosk clears it so the next person starts fresh.',
      'idle.count_one': 'Clearing in {n} second',
      'idle.count_other': 'Clearing in {n} seconds',
      'idle.continue': 'I\'m still here',

      'review.title': 'Review your order',
      'review.ticket': 'Ticket',
      'review.zones': 'Zones',
      'review.qty': 'Quantity',
      'review.total': 'Total',
      'review.promo': 'Promo code',
      'review.promo_placeholder': 'e.g. METRO10',
      'review.apply': 'Apply',
      'review.pay': 'Pay',
      'promo.ok': '{code} applied — {pct}% off',
      'promo.bad': 'That code isn\'t valid',
      'promo.empty': 'Enter a code first',

      'pay.title': 'Pay by card',
      'pay.waiting': 'Tap or insert your card on the reader below',
      'pay.reading': 'Reading card… keep it on the reader',
      'pay.approved': 'Approved — printing your tickets',
      'pay.declined': 'Card declined. Try another card or cancel.',
      'pay.confirm': 'Pay',
      'pay.amount': 'Amount due',

      'done.title': 'Thank you',
      'done.body': 'Please take your tickets and receipt from the slot below.',
      'done.ref': 'Ref',

      'common.next': 'Next',
      'common.back': 'Back',
      'common.cancel': 'Cancel',
      'footer.help': 'Need help? Press the call button on the right of the kiosk.',
      'lang.legend': 'Language',

      'ticket.single.name': 'Single',
      'ticket.single.desc': 'One journey, any direction. Valid 90 minutes.',
      'ticket.day.name': 'Day pass',
      'ticket.day.desc': 'Unlimited travel until 04:00 tomorrow.',
      'ticket.weekly.name': 'Weekly',
      'ticket.weekly.desc': '7 days from first use. Bus, tram and metro.',
      'ticket.concession.name': 'Child / Senior',
      'ticket.concession.desc': 'Under 16 or over 65. Single journey. ID may be checked.',

      'zone.1': 'Zone 1',
      'zone.2': 'Zones 1–2',
      'zone.3': 'Zones 1–3'
    },

    cy: {
      'header.reset': 'Dechrau eto',

      'attract.title': 'Cyffyrddwch i brynu tocyn',
      'attract.sub': 'Prisiau sengl, tocyn dydd, wythnosol a chonsesiwn',
      'attract.cta': 'Dechrau',

      'choose.title': 'Dewiswch eich tocyn',
      'choose.zones': 'Parthau',
      'choose.from': 'o {price}',

      'qty.title': 'Faint o docynnau?',
      'qty.summary': '{ticket}, parthau 1–{zone} · {price} yr un',
      'qty.total': 'Cyfanswm',
      'qty.fewer': 'Un tocyn yn llai',
      'qty.more': 'Un tocyn yn fwy',
      'idle.title': 'Ydych chi yno o hyd?',
      'idle.body': 'Mae eich tocyn ar y sgrin o hyd. Bydd y peiriant yn ei glirio fel bod y person nesaf yn cael dechrau newydd.',
      'idle.count_one': 'Yn clirio ymhen {n} eiliad',
      'idle.count_other': 'Yn clirio ymhen {n} eiliad',
      'idle.continue': 'Rwyf yma o hyd',

      'review.title': 'Adolygu eich archeb',
      'review.ticket': 'Tocyn',
      'review.zones': 'Parthau',
      'review.qty': 'Nifer',
      'review.total': 'Cyfanswm',
      'review.promo': 'Cod hyrwyddo',
      'review.promo_placeholder': 'e.e. METRO10',
      'review.apply': 'Gosod',
      'review.pay': 'Talu',
      'promo.ok': '{code} wedi ei osod — {pct}% i ffwrdd',
      'promo.bad': 'Nid yw\'r cod hwnnw\'n ddilys',
      'promo.empty': 'Rhowch god yn gyntaf',

      'pay.title': 'Talu â cherdyn',
      'pay.waiting': 'Cyffyrddwch neu rhowch eich cerdyn yn y darllenydd isod',
      'pay.reading': 'Yn darllen y cerdyn… cadwch ef ar y darllenydd',
      'pay.approved': 'Wedi ei gymeradwyo — yn argraffu eich tocynnau',
      'pay.declined': 'Cerdyn wedi ei wrthod. Defnyddiwch gerdyn arall neu canslwch.',
      'pay.confirm': 'Talu',
      'pay.amount': 'Swm i\'w dalu',

      'done.title': 'Diolch',
      'done.body': 'Cymerwch eich tocynnau a\'ch derbynneb o\'r slot isod.',
      'done.ref': 'Cyf',

      'common.next': 'Nesaf',
      'common.back': 'Yn ôl',
      'common.cancel': 'Canslo',
      'footer.help': 'Angen help? Pwyswch y botwm galw ar ochr dde\'r peiriant.',
      'lang.legend': 'Iaith',

      'ticket.single.name': 'Sengl',
      'ticket.single.desc': 'Un daith, unrhyw gyfeiriad. Dilys am 90 munud.',
      'ticket.day.name': 'Tocyn dydd',
      'ticket.day.desc': 'Teithio diderfyn hyd 04:00 yfory.',
      'ticket.weekly.name': 'Wythnosol',
      'ticket.weekly.desc': '7 diwrnod o\'r defnydd cyntaf. Bws, tram a metro.',
      'ticket.concession.name': 'Plentyn / Hŷn',
      'ticket.concession.desc': 'O dan 16 neu dros 65. Un daith. Gellir gwirio ID.',

      'zone.1': 'Parth 1',
      'zone.2': 'Parthau 1–2',
      'zone.3': 'Parthau 1–3'
    }
  };

  var lang = DEFAULT_LANG;
  var listeners = [];

  /**
   * Look up a string by key and interpolate {placeholders}.
   * Falls back to English, then to the key itself so missing strings are
   * visible in QA rather than silently blank.
   */
  function t(key, vars) {
    var s = STRINGS[lang] && STRINGS[lang][key];
    if (s === undefined) s = STRINGS[DEFAULT_LANG][key];
    if (s === undefined) return key;
    if (!vars) return s;
    return s.replace(/\{(\w+)\}/g, function (m, k) {
      return vars[k] !== undefined ? vars[k] : m;
    });
  }

  /**
   * Apply data-i18n (text), data-i18n-aria (aria-label) and
   * data-i18n-placeholder across a root element.
   */
  function applyAll(root) {
    var el = root || document;
    var nodes = el.querySelectorAll('[data-i18n]');
    var i;
    for (i = 0; i < nodes.length; i++) {
      nodes[i].textContent = t(nodes[i].getAttribute('data-i18n'));
    }
    nodes = el.querySelectorAll('[data-i18n-aria]');
    for (i = 0; i < nodes.length; i++) {
      nodes[i].setAttribute('aria-label', t(nodes[i].getAttribute('data-i18n-aria')));
    }
    nodes = el.querySelectorAll('[data-i18n-placeholder]');
    for (i = 0; i < nodes.length; i++) {
      nodes[i].setAttribute('placeholder', t(nodes[i].getAttribute('data-i18n-placeholder')));
    }
  }

  function has(id) {
    return Object.prototype.hasOwnProperty.call(STRINGS, id);
  }

  /**
   * Switch locale. Re-applies every static string, updates <html lang> for
   * the screen reader's pronunciation, and notifies listeners so the screens
   * that build their text in JS can re-render. The session (ticket, zones,
   * quantity, promo, typed input) is deliberately untouched.
   */
  function setLang(id) {
    if (!has(id) || id === lang) return;
    lang = id;
    document.documentElement.setAttribute('lang', STRINGS[id] ? langMeta(id).htmlLang : id);
    applyAll(document);
    for (var i = 0; i < listeners.length; i++) listeners[i](lang);
  }

  function langMeta(id) {
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i].id === id) return LANGS[i];
    return LANGS[0];
  }

  function onChange(fn) { listeners.push(fn); }

  global.I18N = {
    t: t,
    applyAll: applyAll,
    setLang: setLang,
    onChange: onChange,
    langMeta: langMeta,
    LANGS: LANGS,
    DEFAULT_LANG: DEFAULT_LANG,
    get lang() { return lang; }
  };
})(window);
