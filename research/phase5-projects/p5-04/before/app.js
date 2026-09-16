/* Trailhead Supply — variant state, size guide, cart, checkout validation. No dependencies. */
(function () {
  'use strict';

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  const money = (n) => '$' + n.toFixed(2).replace(/\.00$/, '');
  const money2 = (n) => '$' + n.toFixed(2);

  /* ---------- Product page ---------- */
  const atcForm = $('#atc-form');
  if (atcForm) {
    const price = Number($('#price').dataset.base);
    const qtyInput = $('#qty');
    const mainImg = $('#gallery-main');
    const sizeError = $('#size-error');
    const stockNote = $('#stock-note');
    const stickyVariant = $('#sticky-variant');
    const sizeLabel = $('#size-label');
    const colorLabel = $('#color-label');
    const status = $('#atc-status');
    const toast = $('#toast');
    let toastTimer;

    const selectedColor = () => $('input[name="color"]:checked', atcForm);
    const selectedSize = () => $('input[name="size"]:checked', atcForm);

    function render() {
      const qty = Math.min(5, Math.max(1, Number(qtyInput.value) || 1));
      qtyInput.value = qty;
      const total = price * qty;
      $$('[data-total]').forEach((el) => { el.textContent = money(total); });

      const color = selectedColor();
      const size = selectedSize();
      colorLabel.textContent = color ? color.value : '';
      sizeLabel.textContent = size ? ': ' + size.value : '';
      if (size) {
        const stock = Number(size.dataset.stock);
        stockNote.textContent = stock <= 3 ? 'Only ' + stock + ' left in ' + size.value : 'In stock — ships today if ordered by 2 pm';
        stockNote.classList.toggle('stock-note--low', stock <= 3);
        sizeError.textContent = '';
        $('#size-group').removeAttribute('aria-invalid');
      } else {
        stockNote.textContent = '';
        stockNote.classList.remove('stock-note--low');
      }
      stickyVariant.textContent = (color ? color.value : '') + ' · ' + (size ? 'Size ' + size.value : 'choose a size') + (qty > 1 ? ' · Qty ' + qty : '');
    }

    atcForm.addEventListener('change', (e) => {
      if (e.target.name === 'color') {
        const src = e.target.dataset.img;
        swapMain(src, 'Ridgeline 3L Shell Jacket in ' + e.target.value + ', front view, hood up');
        $$('.gallery__thumb').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.src === src)));
      }
      render();
    });
    qtyInput.addEventListener('input', render);
    $('#qty-dec').addEventListener('click', () => { qtyInput.value = Number(qtyInput.value) - 1; render(); });
    $('#qty-inc').addEventListener('click', () => { qtyInput.value = Number(qtyInput.value) + 1; render(); });

    function swapMain(src, alt) {
      mainImg.src = src;
      if (alt) mainImg.alt = alt;
    }
    $$('.gallery__thumb').forEach((btn) => {
      btn.addEventListener('click', () => {
        $$('.gallery__thumb').forEach((b) => b.setAttribute('aria-pressed', 'false'));
        btn.setAttribute('aria-pressed', 'true');
        swapMain(btn.dataset.src, btn.getAttribute('aria-label').replace(/^Image \d of \d: /, 'Ridgeline 3L Shell Jacket — '));
      });
    });

    atcForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const size = selectedSize();
      if (!size) {
        sizeError.textContent = 'Please choose a size before adding to cart.';
        $('#size-group').setAttribute('aria-invalid', 'true');
        const first = $('input[name="size"]:not(:disabled)', atcForm);
        first && first.focus();
        $('#size-group').scrollIntoView({ block: 'center', behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
        return;
      }
      const qty = Number(qtyInput.value);
      const count = $('#cart-count');
      count.textContent = String(Number(count.textContent) + qty);
      $('a[aria-label^="Cart"]').setAttribute('aria-label', 'Cart, ' + count.textContent + (count.textContent === '1' ? ' item' : ' items'));
      try {
        localStorage.setItem('th-cart', JSON.stringify({ color: selectedColor().value, size: size.value, qty, price }));
      } catch (_) { /* storage unavailable: cart still shown in-page */ }
      const msg = 'Added ' + qty + ' × Ridgeline 3L Shell, ' + selectedColor().value + ', size ' + size.value + ' to cart.';
      status.textContent = msg;
      $('#toast-text').textContent = msg;
      toast.hidden = false;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => { toast.hidden = true; }, 6000);
    });

    // Size guide dialog
    const dlg = $('#size-guide');
    $('#open-size-guide').addEventListener('click', () => dlg.showModal());
    $('#close-size-guide').addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });

    // Sticky bar: only while the in-page Add to cart is off-screen (avoids two identical CTAs on screen)
    const sticky = $('#sticky-atc');
    if ('IntersectionObserver' in window && sticky) {
      new IntersectionObserver((entries) => {
        const inView = entries[0].isIntersecting;
        sticky.hidden = inView;
        document.body.classList.toggle('has-sticky', !inView);
      }, { rootMargin: '0px 0px -72px 0px' }).observe($('#atc'));
    }

    render();
  }

  /* ---------- Header menu (phones) ---------- */
  const menuBtn = $('#menu-btn');
  if (menuBtn) {
    const nav = $('#site-nav');
    menuBtn.addEventListener('click', () => {
      const open = nav.dataset.open === 'true';
      nav.dataset.open = String(!open);
      menuBtn.setAttribute('aria-expanded', String(!open));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.dataset.open === 'true') { nav.dataset.open = 'false'; menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.focus(); }
    });
  }

  /* ---------- Checkout ---------- */
  const coForm = $('#checkout-form');
  if (coForm) {
    // hydrate summary from the cart written by the product page
    let cart = { color: 'Moss', size: 'M', qty: 1, price: 329 };
    try { cart = Object.assign(cart, JSON.parse(localStorage.getItem('th-cart') || '{}')); } catch (_) {}
    $('#summary-variant').textContent = cart.color + ' · ' + cart.size + ' · Qty ' + cart.qty;
    const TAX_RATE = 0.0801;
    function totals() {
      const subtotal = cart.price * cart.qty;
      const ship = Number($('input[name="shipping"]:checked').value);
      const tax = subtotal * TAX_RATE;
      const grand = subtotal + ship + tax;
      $('#summary-price').textContent = money2(subtotal);
      $$('[data-subtotal]').forEach((el) => (el.textContent = money2(subtotal)));
      $$('[data-shipping]').forEach((el) => (el.textContent = ship ? money2(ship) : 'Free'));
      $$('[data-tax]').forEach((el) => (el.textContent = money2(tax)));
      $$('[data-grand]').forEach((el) => (el.textContent = money2(grand)));
      const meta = $('#sticky-pay-meta');
      if (meta) meta.textContent = cart.qty + (cart.qty === 1 ? ' item' : ' items') + ' · ' + (ship ? money(ship) + ' shipping' : 'free shipping') + ' · tax incl.';
    }
    coForm.addEventListener('change', (e) => { if (e.target.name === 'shipping') totals(); });
    totals();

    const labels = {
      email: 'Email', first: 'First name', last: 'Last name', addr1: 'Street address',
      city: 'City', region: 'State / province', postal: 'ZIP / postal code', phone: 'Phone',
    };
    const messages = {
      valueMissing: (l) => 'Enter your ' + l.toLowerCase() + '.',
      typeMismatch: (l) => 'Enter a valid ' + l.toLowerCase() + ', like name@example.com.',
    };

    function validateField(input) {
      const id = input.id;
      const err = $('#' + id + '-error');
      if (!err) return true;
      let msg = '';
      if (input.required && !input.value.trim()) msg = messages.valueMissing(labels[id] || id);
      else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) msg = messages.typeMismatch(labels[id]);
      else if (id === 'postal' && !/^[A-Za-z0-9][A-Za-z0-9 -]{2,9}$/.test(input.value.trim())) msg = 'Enter a valid postal code.';
      else if (id === 'phone' && input.value.replace(/\D/g, '').length < 7) msg = 'Enter a phone number with at least 7 digits.';
      err.textContent = msg;
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    }

    // validate on blur after first interaction; re-validate on input once invalid
    $$('input[required], select[required]', coForm).forEach((input) => {
      input.addEventListener('blur', () => { if (input.value || input.dataset.touched) { input.dataset.touched = '1'; validateField(input); } });
      input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') validateField(input); });
    });

    const summary = $('#form-summary');
    const statusEl = $('#checkout-status');
    coForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const invalid = $$('input[required], select[required]', coForm).filter((i) => !validateField(i));
      if (invalid.length) {
        summary.innerHTML = '<strong>' + invalid.length + (invalid.length === 1 ? ' field needs' : ' fields need') + ' your attention</strong><ul>' +
          invalid.map((i) => '<li><a href="#' + i.id + '">' + (labels[i.id] || i.id) + '</a>: ' + $('#' + i.id + '-error').textContent + '</li>').join('') + '</ul>';
        summary.hidden = false;
        statusEl.textContent = invalid.length + ' fields need your attention.';
        summary.focus();
        return;
      }
      summary.hidden = true;
      const btns = [$('#place-order'), $('#sticky-pay .btn')].filter(Boolean);
      btns.forEach((b) => { b.setAttribute('aria-disabled', 'true'); b.textContent = 'Placing order…'; });
      statusEl.textContent = 'Placing your order.';
      setTimeout(() => {
        $('#success-email').textContent = $('#email').value;
        $('.checkout').hidden = true;
        const sp = $('#sticky-pay');
        if (sp) { sp.hidden = true; document.body.classList.remove('has-sticky'); }
        const ok = $('#success');
        ok.hidden = false;
        ok.focus();
        statusEl.textContent = 'Order placed. Confirmation sent to ' + $('#email').value;
      }, 600);
    });

    // summary links focus the field
    summary.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      e.preventDefault();
      const target = $(a.getAttribute('href'));
      target && target.focus();
    });

    $('#promo-form').addEventListener('submit', (e) => { e.preventDefault(); });

    // Order summary: collapsible on phones, always open on wide screens
    const os = $('#order-summary');
    const wide = window.matchMedia('(min-width: 901px)');
    const syncSummary = () => { if (wide.matches) os.open = true; else if (!os.dataset.userToggled) os.open = false; };
    os.addEventListener('toggle', () => { if (!wide.matches) os.dataset.userToggled = '1'; });
    wide.addEventListener('change', syncSummary);
    syncSummary();

    // Sticky Place order (phones): only while the in-form button is off-screen (same rule as the product page's sticky Add to cart)
    const stickyPay = $('#sticky-pay');
    if ('IntersectionObserver' in window && stickyPay) {
      new IntersectionObserver((entries) => {
        const inView = entries[0].isIntersecting;
        stickyPay.hidden = inView;
        document.body.classList.toggle('has-sticky', !inView);
      }, { rootMargin: '0px 0px -72px 0px' }).observe($('#place-order'));
    }
  }


  /* ---------- Product listing (filters, sort, count, URL state) ---------- */
  const plp = $('#filters');
  if (plp) {
    const cards = $$('#catalog .product-card');
    const chips = $$('.chip[data-facet]', plp);
    const applied = $('#applied');
    const count = $('#results-count');
    const sort = $('#sort');
    const empty = $('#plp-empty');
    const facets = $('#facets');
    const badge = $('#facets-badge');
    const PRICE = { under150: (p) => p < 150, '150to300': (p) => p >= 150 && p <= 300, over300: (p) => p > 300 };
    const wide = window.matchMedia('(min-width: 721px)');

    const state = { category: new Set(), price: new Set(), feature: new Set(), sort: 'featured' };

    function readUrl() {
      const q = new URLSearchParams(location.search);
      for (const f of ['category', 'price', 'feature']) {
        state[f] = new Set((q.get(f) || '').split(',').filter(Boolean).filter((v) => chips.some((c) => c.dataset.facet === f && c.dataset.value === v)));
      }
      state.sort = ['featured', 'price-asc', 'price-desc', 'rating'].includes(q.get('sort')) ? q.get('sort') : 'featured';
    }
    function writeUrl() {
      const q = new URLSearchParams();
      for (const f of ['category', 'price', 'feature']) if (state[f].size) q.set(f, [...state[f]].join(','));
      if (state.sort !== 'featured') q.set('sort', state.sort);
      const qs = q.toString();
      history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
    }
    const matches = (card, ignoreFacet) => {
      const price = Number(card.dataset.price);
      const feats = card.dataset.features.split(' ').filter(Boolean);
      if (ignoreFacet !== 'category' && state.category.size && !state.category.has(card.dataset.category)) return false;
      if (ignoreFacet !== 'price' && state.price.size && ![...state.price].some((k) => PRICE[k](price))) return false;
      if (ignoreFacet !== 'feature' && state.feature.size && ![...state.feature].every((f) => feats.includes(f))) return false;
      return true;
    };

    function render() {
      let shown = 0;
      cards.forEach((c) => { const ok = matches(c); c.hidden = !ok; if (ok) shown++; });
      // sort by reordering the DOM so visual order = reading order = Tab order
      const sorted = cards.slice().sort((a, b) => {
        if (state.sort === 'price-asc') return a.dataset.price - b.dataset.price;
        if (state.sort === 'price-desc') return b.dataset.price - a.dataset.price;
        if (state.sort === 'rating') return b.dataset.rating - a.dataset.rating;
        return cards.indexOf(a) - cards.indexOf(b);
      });
      const catalog = $('#catalog');
      sorted.forEach((c) => catalog.appendChild(c));
      // chip pressed state + counts ("how many if I add this", ignoring the chip's own facet)
      chips.forEach((c) => {
        const on = state[c.dataset.facet].has(c.dataset.value);
        c.setAttribute('aria-pressed', String(on));
        const n = c.querySelector('[data-count]');
        if (n) {
          const would = cards.filter((card) => matches(card, c.dataset.facet) && (
            c.dataset.facet === 'category' ? card.dataset.category === c.dataset.value : card.dataset.features.split(' ').includes(c.dataset.value)
          )).length;
          n.textContent = '(' + would + ')';
        }
      });
      // applied chips (removable) + clear all
      const labelOf = (f, v) => chips.find((c) => c.dataset.facet === f && c.dataset.value === v).firstChild.textContent.trim();
      const items = [];
      for (const f of ['category', 'price', 'feature']) for (const v of state[f]) items.push({ f, v, label: labelOf(f, v) });
      applied.innerHTML = items.map((i) =>
        '<button type="button" class="chip" data-remove="' + i.f + ':' + i.v + '" aria-label="Remove filter ' + i.label + '">' + i.label + ' <span class="x" aria-hidden="true">\u2715</span></button>'
      ).join('') + (items.length ? '<button type="button" class="link-btn" data-clear>Clear all</button>' : '');
      // count (live region), empty state, phone badge, title/breadcrumb/nav current
      const total = cards.length;
      count.textContent = shown === total ? total + ' products' : shown + ' of ' + total + ' products';
      empty.hidden = shown > 0;
      catalog.hidden = shown === 0;
      badge.hidden = items.length === 0;
      badge.textContent = String(items.length);
      badge.setAttribute('aria-label', items.length + ' filters applied');
      const cats = [...state.category];
      const title = cats.length === 1 ? labelOf('category', cats[0]) : 'All gear';
      $('#plp-title').textContent = title;
      $('#crumb-current').textContent = title;
      document.title = title + ' \u2014 Trailhead Supply';
      $$('#site-nav a').forEach((a) => { if (cats.length === 1 && a.dataset.category === cats[0]) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
      sort.value = state.sort;
      writeUrl();
    }

    plp.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip[data-facet]');
      const remove = e.target.closest('[data-remove]');
      const clear = e.target.closest('[data-clear]');
      if (chip) {
        const set = state[chip.dataset.facet];
        const on = set.has(chip.dataset.value);
        if (chip.hasAttribute('data-single')) set.clear();
        if (on) set.delete(chip.dataset.value); else set.add(chip.dataset.value);
        render();
      } else if (remove) {
        const parts = remove.dataset.remove.split(':');
        state[parts[0]].delete(parts[1]);
        render();
        // keep focus in the applied row, else on the count, so keyboard users are not dropped at the top
        const next = applied.querySelector('button') || count;
        if (next === count) count.tabIndex = -1;
        next.focus();
      } else if (clear) {
        for (const f of ['category', 'price', 'feature']) state[f].clear();
        render();
        chips[0].focus();
      }
    });
    sort.addEventListener('change', () => { state.sort = sort.value; render(); });
    $('#empty-clear').addEventListener('click', () => { for (const f of ['category', 'price', 'feature']) state[f].clear(); render(); chips[0].focus(); });

    // Facet groups: always open on wide screens, collapsed by default on phones (same rule as the checkout summary)
    const syncFacets = () => { if (wide.matches) facets.open = true; else if (!facets.dataset.userToggled) facets.open = false; };
    facets.addEventListener('toggle', () => { if (!wide.matches) facets.dataset.userToggled = '1'; });
    wide.addEventListener('change', syncFacets);
    syncFacets();

    readUrl();
    render();
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
})();
