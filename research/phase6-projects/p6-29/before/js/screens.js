// Screen renderers. Pure functions: (name, ctx) -> HTML string.
import { maskName, maskDrug } from './lookup.js';

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = (n) => n === 0 ? null : `$${n.toFixed(2)}`;

function topbar(t, icons, stepIndex) {
  const step = stepIndex == null ? '' :
    `<div class="step" aria-live="polite">${t.stepOf(stepIndex + 1, 3)}<strong>${t.stepNames[stepIndex]}</strong></div>`;
  return `<header class="topbar"><div class="brand">${icons.pharmacy}<span>${t.brand}</span></div>${step}</header>`;
}

// Utility bar: present on every screen, always at the bottom (reach zone) — language, accessibility toggle, help, start over.
// The language button is labelled in the language it switches TO (its own `lang`), so "Español" reads the same to an
// English screen reader and to a Spanish speaker looking for it; the attract screen has its own chooser and foot switch.
function utilbar(t, icons, state, { startOver = true, a11yToggle = true, langToggle = true } = {}) {
  const other = state.lang === 'en' ? 'es' : 'en';
  const lang = langToggle ? `<button class="btn btn--util" type="button" data-action="lang" lang="${other}">${icons.language}<span>${t.language}</span></button>` : '';
  return `<nav class="utilbar" aria-label="${t.kioskOptions}">
    ${lang}
    <button class="btn btn--util ${a11yToggle ? '' : 'btn--hidden'}" type="button" data-action="a11y" aria-pressed="${state.a11y}" ${a11yToggle ? '' : 'tabindex="-1" aria-hidden="true"'}>${icons.a11y}<span>${state.a11y ? t.a11yOff : t.a11yOn}</span></button>
    <button class="btn btn--util" type="button" data-action="help">${icons.help}<span>${t.help}</span></button>
    <button class="btn btn--util ${startOver ? '' : 'btn--hidden'}" type="button" data-action="start-over" ${startOver ? '' : 'tabindex="-1" aria-hidden="true"'}>${icons.restart}<span>${t.startOver}</span></button>
  </nav>`;
}

// `session.error` is a string key (see dobProblem in app.js); it is translated here, at render time, so it follows the language.
function errorLine(session, icons, t) {
  return `<p class="field__error" role="alert" id="field-error">${session?.error ? `${icons.alert}<span>${esc(t[session.error] ?? session.error)}</span>` : ''}</p>`;
}

// Read-only value box: labelled, described by the persistent hint and the error line, focusable so a keyboard or
// screen-reader user can read the current value, marked invalid while an error is shown.
function valueBox(session, content) {
  return `<div class="field__value" role="textbox" aria-readonly="true" tabindex="0" id="field-value"
      aria-labelledby="field-label" aria-describedby="field-hint field-error" ${session?.error ? 'aria-invalid="true"' : ''}>${content}</div>`;
}

const screens = {
  attract({ t, icons, state }) {
    // First-visit chooser: language and view, each as a pair of pressed-state buttons with immediate
    // effect. Shown until the visitor continues or touches Start; the foot language switch takes
    // over afterwards. The chooser never blocks Start and does not touch the pick-up flow.
    const chooser = state.chosen ? '' : `
        <section class="chooser" role="group" aria-labelledby="chooser-h">
          <div class="chooser__head">
            <h2 id="chooser-h">${t.chooserTitle}</h2>
            <button class="btn btn--secondary" type="button" data-action="chooser-done">${t.chooserDone}</button>
          </div>
          <div class="chooser__row" role="group" aria-labelledby="chooser-lang">
            <span class="chooser__label" id="chooser-lang">${t.chooserLang}</span>
            <button class="btn btn--choice" type="button" data-action="set-lang" data-lang="en" lang="en" aria-pressed="${state.lang === 'en'}">${icons.check}<span>English</span></button>
            <button class="btn btn--choice" type="button" data-action="set-lang" data-lang="es" lang="es" aria-pressed="${state.lang === 'es'}">${icons.check}<span>Español</span></button>
          </div>
          <div class="chooser__row" role="group" aria-labelledby="chooser-view">
            <span class="chooser__label" id="chooser-view">${t.chooserView}</span>
            <button class="btn btn--choice" type="button" data-action="set-a11y" data-a11y="off" aria-pressed="${!state.a11y}">${icons.check}<span>${t.viewStandard}</span></button>
            <button class="btn btn--choice" type="button" data-action="set-a11y" data-a11y="on" aria-pressed="${state.a11y}" aria-describedby="chooser-hint">${icons.check}<span>${t.viewAccessible}</span></button>
            <p class="chooser__hint" id="chooser-hint">${t.viewHint}</p>
          </div>
        </section>`;
    const foot = state.chosen ? `
        <div class="attract__foot">
          <button class="btn btn--secondary" type="button" data-action="lang" lang="${state.lang === 'en' ? 'es' : 'en'}">${t.language}</button>
        </div>` : '';
    return `
      <section class="screen attract" aria-labelledby="h">
        <div class="attract__field">
          ${icons.bag.replace('<svg ', '<svg class="attract__art" ')}
          <h1 id="h">${t.attractTitle}</h1>
          <p class="lede">${t.attractLede}</p>
          <button class="btn attract__start" type="button" data-action="start">${t.start}</button>
        </div>
        ${chooser}${foot}
      </section>
      ${utilbar(t, icons, state, { startOver: false, a11yToggle: state.chosen, langToggle: false })}`;
  },

  'identify-dob'({ t, icons, state, session }) {
    const d = session.dob;
    const fmt = `${d.slice(0, 2)}${d.length > 2 ? ' / ' : ''}${d.slice(2, 4)}${d.length > 4 ? ' / ' : ''}${d.slice(4, 8)}`;
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
      .map((k) => `<button class="key" type="button" data-action="key" data-field="dob" data-key="${k}">${k}</button>`).join('');
    return `${topbar(t, icons, 0)}
      <section class="screen" aria-labelledby="h">
        <div class="screen__intro"><h1 id="h">${t.dobTitle}</h1><p class="lede">${t.dobLede}</p></div>
        <div class="screen__body">
          <div class="field">
            <span class="field__label" id="field-label">${t.dobLabel}</span>
            ${valueBox(session, d ? `<span>${fmt}</span><span class="caret" aria-hidden="true"></span>` : `<span class="ph">${t.dobPh}</span>`)}
            <span class="field__hint" id="field-hint">${t.dobHint}</span>
            ${errorLine(session, icons, t)}
          </div>
          <div class="keys keys--pad" role="group" aria-label="${t.dobLabel}">
            ${keys}
            <button class="key key--action" type="button" data-action="key" data-field="dob" data-key="clear">${t.clear}</button>
            <button class="key" type="button" data-action="key" data-field="dob" data-key="0">0</button>
            <button class="key" type="button" data-action="key" data-field="dob" data-key="del" aria-label="${t.delete}">${icons.delete}</button>
          </div>
          <div class="scanline">${icons.scan}<p>${t.scanHint}</p></div>
        </div>
        <div class="screen__actions">
          <button class="btn btn--primary" type="button" data-action="dob-continue">${t.continue}</button>
        </div>
      </section>
      ${utilbar(t, icons, state)}`;
  },

  'identify-name'({ t, icons, state, session }) {
    const rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];
    const kb = rows.map((r, i) => {
      const ks = [...r].map((k) => `<button class="key" type="button" data-action="key" data-field="name" data-key="${k}">${k}</button>`).join('');
      if (i === 1) return `<span aria-hidden="true"></span>${ks}`;                 // stagger half a key: use an empty cell
      if (i === 2) return `<span aria-hidden="true"></span>${ks}<button class="key key--wide" type="button" data-action="key" data-field="name" data-key="del" aria-label="${t.delete}">${icons.delete}</button>`;
      return ks;
    }).join('');
    // Bottom row: Clear takes the two cells that were empty spacers, so its label fits at 2 keys wide in both languages
    // ("Limpiar" does not fit one 84 px key); a single key never sizes itself around the English word.
    const bottom = `<button class="key key--action key--wide" type="button" data-action="key" data-field="name" data-key="clear">${t.clear}</button>`;
    return `${topbar(t, icons, 0)}
      <section class="screen" aria-labelledby="h">
        <div class="screen__intro"><h1 id="h">${t.nameTitle}</h1><p class="lede">${t.nameLede}</p></div>
        <div class="screen__body">
          <div class="field">
            <span class="field__label" id="field-label">${t.nameLabel}</span>
            ${valueBox(session, session.name ? `<span>${esc(session.name)}</span><span class="caret" aria-hidden="true"></span>` : `<span class="ph">${t.namePh}</span>`)}
            <span class="field__hint" id="field-hint">${t.nameHint}</span>
            ${errorLine(session, icons, t)}
          </div>
          <div class="keys keys--qwerty" role="group" aria-label="${t.nameLabel}">
            ${kb}
            ${bottom}
            <button class="key key--action key--x4" type="button" data-action="key" data-field="name" data-key="-" aria-label="${t.hyphen}">-</button>
            <button class="key key--action key--x4" type="button" data-action="key" data-field="name" data-key="space">${t.space}</button>
          </div>
        </div>
        <div class="screen__actions">
          <button class="btn btn--primary" type="button" data-action="find" ${session.busy ? 'aria-disabled="true"' : ''}>${session.busy ? t.checking : t.find}</button>
          <button class="btn btn--secondary" type="button" data-action="back" data-to="identify-dob">${icons.back}<span>${t.back}</span></button>
        </div>
      </section>
      ${utilbar(t, icons, state)}`;
  },

  list({ t, icons, state, session }) {
    const p = session.patient;
    const rows = p.prescriptions.map((rx) => {
      const ready = rx.status === 'ready';
      const checked = session.selected.has(rx.rxNumber);
      const name = session.revealed ? rx.drug : maskDrug(rx.drug);
      const price = money(rx.price) ?? t.free;
      return `<button class="rxrow" type="button" role="checkbox" aria-checked="${ready ? checked : 'false'}" ${ready ? '' : 'aria-disabled="true"'} data-action="toggle" data-rx="${rx.rxNumber}">
        <span class="rxrow__box" aria-hidden="true">${icons.check}</span>
        <span class="rxrow__main">
          <span class="rxrow__name">${esc(name)}</span>
          <span class="rxrow__meta num">${t.rxNo} ···${rx.rxNumber.slice(-4)} · ${esc(rx.form)} · ${t.prescriber} ${esc(rx.prescriber)}</span>
          ${ready ? '' : `<span class="rxrow__meta"><span class="pill">${t.processing}</span> ${t.processingHint}</span>`}
        </span>
        <span class="rxrow__price num">${ready ? price : ''}</span>
      </button>`;
    }).join('');
    const total = p.prescriptions.filter((rx) => session.selected.has(rx.rxNumber)).reduce((s, rx) => s + rx.price, 0);
    return `${topbar(t, icons, 1)}
      <section class="screen" aria-labelledby="h">
        <div class="screen__intro">
          <h1 id="h">${t.listTitle(esc(maskName(p.lastName)))}</h1>
          <p class="lede">${t.listLede}</p>
        </div>
        <div class="screen__body">
          <div class="rxlist" role="group" aria-label="${t.stepNames[1]}">${rows}</div>
          <button class="btn btn--secondary" type="button" data-action="reveal" aria-pressed="${session.revealed}">${session.revealed ? icons.eyeOff : icons.eye}<span>${session.revealed ? t.hideNames : t.showNames}</span></button>
          ${errorLine(session, icons, t)}
        </div>
        <div class="screen__actions">
          <div class="summary__row"><span>${t.selectedCount(session.selected.size)}</span><span class="num">${t.dueAtCounter}: <strong>${money(total) ?? t.free}</strong></span></div>
          <button class="btn btn--primary" type="button" data-action="review">${t.reviewPickup}</button>
        </div>
      </section>
      ${utilbar(t, icons, state)}`;
  },

  confirm({ t, icons, state, session }) {
    const p = session.patient;
    const chosen = p.prescriptions.filter((rx) => session.selected.has(rx.rxNumber));
    const total = chosen.reduce((s, rx) => s + rx.price, 0);
    return `${topbar(t, icons, 2)}
      <section class="screen" aria-labelledby="h">
        <div class="screen__intro"><h1 id="h">${t.confirmTitle}</h1><p class="lede">${t.confirmLede}</p></div>
        <div class="screen__body">
          <div class="summary">
            <div class="summary__row"><span>${t.items(chosen.length)}</span><span>${esc(maskName(p.lastName))}</span></div>
            ${chosen.map((rx) => `<div class="summary__row small"><span>${esc(maskDrug(rx.drug))}</span><span class="num">${money(rx.price) ?? t.free}</span></div>`).join('')}
            <div class="summary__row summary__row--total"><span>${t.total}</span><span class="num">${money(total) ?? t.free}</span></div>
          </div>
        </div>
        <div class="screen__actions">
          <button class="btn btn--primary" type="button" data-action="confirm">${icons.check}<span>${t.confirm}</span></button>
          <button class="btn btn--secondary" type="button" data-action="back" data-to="list">${icons.back}<span>${t.change}</span></button>
        </div>
      </section>
      ${utilbar(t, icons, state)}`;
  },

  done({ t, icons, state, session, config }) {
    return `${topbar(t, icons, null)}
      <section class="screen" aria-labelledby="h">
        <div class="screen__intro success">
          ${icons.success.replace('<svg ', '<svg class="success__icon" ')}
          <h1 id="h">${t.doneTitle}</h1>
          <p class="lede">${t.doneLede}</p>
        </div>
        <div class="screen__body">
          <div class="ticket">
            <span class="ticket__label">${t.ticket}</span>
            <span class="ticket__value">${session.ticket.code}</span>
            <span class="ticket__label">${t.counter} ${session.ticket.counter} · ${t.items(session.selectedCount)}</span>
          </div>
          <div class="banner">${icons.alert}<span data-done-countdown aria-live="polite">${t.screenClears(config.doneAutoResetS)}</span></div>
        </div>
        <div class="screen__actions">
          <button class="btn btn--primary" type="button" data-action="done">${t.done}</button>
        </div>
      </section>
      ${utilbar(t, icons, state)}`;
  },
};

export function renderScreen(name, ctx) {
  return (screens[name] ?? screens.attract)(ctx);
}
