/* Spatial focus manager.
 * Focus moves between `.focusable` elements by geometry. Containers can be
 * scoped with data-focus-scope so that up/down leaves a rail and left/right
 * stays inside it.
 */
(function (global) {
  'use strict';

  var current = null;
  var root = document;
  var listeners = [];

  function rect(el) {
    var r = el.getBoundingClientRect();
    return { l: r.left, t: r.top, r: r.right, b: r.bottom, cx: (r.left + r.right) / 2, cy: (r.top + r.bottom) / 2, w: r.width, h: r.height };
  }

  function candidates() {
    var nodes = root.querySelectorAll('.focusable');
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.offsetParent === null && n !== document.body) continue; // hidden
      if (n.classList.contains('disabled')) continue;
      out.push(n);
    }
    return out;
  }

  function scopeOf(el) {
    return el.closest('[data-focus-scope]');
  }

  // Score a candidate in a direction: primary axis distance + weighted
  // secondary offset. Lower is better. Returns Infinity when not in direction.
  // Gap between two ranges on one axis; 0 when they overlap.
  function gap(a0, a1, b0, b1) {
    if (b0 >= a1) return b0 - a1;
    if (b1 <= a0) return a0 - b1;
    return 0;
  }

  function score(from, to, dir) {
    var dx, dy;
    switch (dir) {
      case 'left':  if (to.r > from.l + 1) return Infinity; dx = from.l - to.r; dy = gap(from.t, from.b, to.t, to.b); return dx + dy * 2;
      case 'right': if (to.l < from.r - 1) return Infinity; dx = to.l - from.r; dy = gap(from.t, from.b, to.t, to.b); return dx + dy * 2;
      case 'up':    if (to.b > from.t + 1) return Infinity; dy = from.t - to.b; dx = gap(from.l, from.r, to.l, to.r); return dy + dx * 2;
      case 'down':  if (to.t < from.b - 1) return Infinity; dy = to.t - from.b; dx = gap(from.l, from.r, to.l, to.r); return dy + dx * 2;
    }
    return Infinity;
  }

  function findNext(dir) {
    if (!current) return null;
    var from = rect(current);
    var fromScope = scopeOf(current);
    var horizontal = dir === 'left' || dir === 'right';
    var best = null, bestScore = Infinity;
    var list = candidates();
    for (var i = 0; i < list.length; i++) {
      var el = list[i];
      if (el === current) continue;
      var sc = scopeOf(el);
      // Horizontal movement stays within the current scope (a rail / a guide row);
      // vertical movement never lands inside the current scope.
      if (horizontal && fromScope && sc !== fromScope) continue;
      if (!horizontal && fromScope && sc === fromScope) continue;
      var s = score(from, rect(el), dir);
      if (s < bestScore) { bestScore = s; best = el; }
    }
    // Vertical movement into a rail: land on the rail's first item.
    if (best && !horizontal) {
      var targetScope = scopeOf(best);
      if (targetScope && targetScope !== fromScope && targetScope.hasAttribute('data-focus-rail')) {
        var first = targetScope.querySelector('.focusable');
        if (first) best = first;
      }
    }
    return best;
  }

  function setFocus(el, opts) {
    if (!el) return;
    if (current && current !== el) current.classList.remove('focused');
    current = el;
    el.classList.add('focused');
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
    listeners.forEach(function (fn) { fn(el, opts || {}); });
  }

  function move(dir) {
    var next = findNext(dir);
    if (next) { setFocus(next, { dir: dir }); return true; }
    return false;
  }

  function focusFirst(container) {
    var el = (container || root).querySelector('.focusable');
    if (el) setFocus(el, { initial: true });
    return el;
  }

  function onKey(e) {
    var k = global.Keys.fromEvent(e);
    if (!k) return;
    var handled = false;
    if (global.App && global.App.handleKey && global.App.handleKey(k, e)) {
      handled = true;
    } else if (k === 'left' || k === 'right' || k === 'up' || k === 'down') {
      handled = move(k);
    } else if (k === 'enter') {
      if (current) { current.click(); handled = true; }
    }
    if (handled) e.preventDefault();
  }

  document.addEventListener('keydown', onKey);

  global.Focus = {
    setFocus: setFocus,
    focusFirst: focusFirst,
    move: move,
    getCurrent: function () { return current; },
    onChange: function (fn) { listeners.push(fn); },
    clear: function () { if (current) current.classList.remove('focused'); current = null; }
  };
})(window);
