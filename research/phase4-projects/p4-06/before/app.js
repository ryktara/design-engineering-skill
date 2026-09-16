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
      const btn = $('#place-order');
      btn.setAttribute('aria-disabled', 'true');
      btn.textContent = 'Placing order…';
      statusEl.textContent = 'Placing your order.';
      setTimeout(() => {
        $('#success-email').textContent = $('#email').value;
        $('.checkout').hidden = true;
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
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
})();
