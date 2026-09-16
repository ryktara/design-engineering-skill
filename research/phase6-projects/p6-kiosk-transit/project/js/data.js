// MetroLink kiosk — fare table.
// Keep in sync with data/fares.json (the ops team edits that file; this is the runtime copy).

(function (global) {
  'use strict';

  var CURRENCY = { symbol: '£', code: 'GBP' };

  // Prices in pence, indexed by zone extent (1 = zone 1 only, 2 = zones 1–2, 3 = zones 1–3).
  var TICKETS = [
    {
      id: 'single',
      name: 'Single',
      desc: 'One journey, any direction. Valid 90 minutes.',
      prices: { 1: 280, 2: 340, 3: 420 },
      maxQty: 10
    },
    {
      id: 'day',
      name: 'Day pass',
      desc: 'Unlimited travel until 04:00 tomorrow.',
      prices: { 1: 650, 2: 780, 3: 950 },
      maxQty: 10
    },
    {
      id: 'weekly',
      name: 'Weekly',
      desc: '7 days from first use. Bus, tram and metro.',
      prices: { 1: 2450, 2: 2980, 3: 3620 },
      maxQty: 4
    },
    {
      id: 'concession',
      name: 'Child / Senior',
      desc: 'Under 16 or over 65. Single journey. ID may be checked.',
      prices: { 1: 140, 2: 170, 3: 210 },
      maxQty: 10
    }
  ];

  var ZONES = [
    { id: 1, label: 'Zone 1' },
    { id: 2, label: 'Zones 1–2' },
    { id: 3, label: 'Zones 1–3' }
  ];

  // Percentage-off promo codes. Case-insensitive.
  var PROMOS = {
    METRO10: 10,
    STUDENT15: 15,
    WELCOME5: 5
  };

  function findById(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function getTicket(id) { return findById(TICKETS, id); }
  function getZone(id) { return findById(ZONES, id); }

  function unitPrice(ticketId, zoneId) {
    var t = getTicket(ticketId);
    return t ? t.prices[zoneId] || 0 : 0;
  }

  function total(ticketId, zoneId, qty, promoPct) {
    var gross = unitPrice(ticketId, zoneId) * qty;
    if (promoPct) gross = Math.round(gross * (100 - promoPct) / 100);
    return gross;
  }

  function formatMoney(pence) {
    var pounds = Math.floor(pence / 100);
    var rem = pence % 100;
    return CURRENCY.symbol + pounds + '.' + (rem < 10 ? '0' : '') + rem;
  }

  global.FARES = {
    CURRENCY: CURRENCY, TICKETS: TICKETS, ZONES: ZONES, PROMOS: PROMOS,
    getTicket: getTicket, getZone: getZone, unitPrice: unitPrice, total: total, formatMoney: formatMoney
  };
})(window);
