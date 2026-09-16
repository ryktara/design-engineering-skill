// MetroLink kiosk — UI strings.
// Kiosks in this deployment are English-only; the footer badge reflects that.

(function (global) {
  'use strict';

  var STRINGS = {
    'attract.title': 'Touch to buy a ticket',
    'attract.sub': 'Single, day pass, weekly and concession fares',
    'attract.cta': 'Start',

    'choose.title': 'Choose your ticket',
    'choose.zones': 'Zones',

    'qty.title': 'How many tickets?',
    'qty.summary': '{ticket}, zones 1–{zone} · {price} each',

    'review.title': 'Review your order',
    'review.ticket': 'Ticket',
    'review.zones': 'Zones',
    'review.qty': 'Quantity',
    'review.total': 'Total',
    'review.promo': 'Promo code',
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

    'done.title': 'Thank you',
    'done.body': 'Please take your tickets and receipt from the slot below.',

    'common.next': 'Next',
    'common.back': 'Back',
    'common.cancel': 'Cancel',
    'footer.help': 'Need help? Press the call button on the right of the kiosk.'
  };

  /**
   * Look up a string by key and interpolate {placeholders}.
   * Falls back to the key itself so missing strings are visible in QA.
   */
  function t(key, vars) {
    var s = STRINGS[key];
    if (s === undefined) return key;
    if (!vars) return s;
    return s.replace(/\{(\w+)\}/g, function (m, k) {
      return vars[k] !== undefined ? vars[k] : m;
    });
  }

  /** Apply data-i18n attributes across a root element. */
  function applyAll(root) {
    var nodes = (root || document).querySelectorAll('[data-i18n]');
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].textContent = t(nodes[i].getAttribute('data-i18n'));
    }
  }

  global.I18N = { t: t, applyAll: applyAll, lang: 'en' };
})(window);
