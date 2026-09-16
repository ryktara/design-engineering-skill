// RxPoint kiosk: attract -> identify (dob -> name | scan) -> list -> confirm -> done
// Vanilla ES modules, no build. Personal data lives only in `session`, which is wiped on reset.
import { strings } from './i18n.js';
import { icons } from './icons.js';
import { renderScreen } from './screens.js';
import { findPatient } from './lookup.js';

const params = new URLSearchParams(location.search);
export const config = {
  idleWarnMs: Number(params.get('idle') ?? 40) * 1000,       // inactivity before the warning dialog
  idleCountdownS: Number(params.get('count') ?? 20),          // seconds shown in the dialog (extendable, WCAG 2.2.1)
  doneAutoResetS: Number(params.get('done') ?? 20),
  revealS: 10,
  steps: 3,
};

export const state = { lang: params.get('lang') === 'es' ? 'es' : 'en', a11y: params.get('a11y') === 'on', sound: true };
let session = null; // { patient, selected:Set, dob, name, revealed, ticket }

export const t = () => strings[state.lang];
export const getSession = () => session;

const app = document.getElementById('app');
const idleDialog = document.getElementById('idle-dialog');
const helpDialog = document.getElementById('help-dialog');
const live = document.getElementById('live');

// ---------- audio + haptic-style feedback on every tap ----------
let audio;
function beep() {
  if (!state.sound) return;
  try {
    audio ??= new (window.AudioContext || window.webkitAudioContext)();
    const o = audio.createOscillator(); const g = audio.createGain();
    o.frequency.value = 880; g.gain.value = 0.04;
    o.connect(g).connect(audio.destination); o.start(); o.stop(audio.currentTime + 0.05);
  } catch { /* audio unavailable: visual pressed state still applies */ }
}

// ---------- navigation ----------
export let screen = 'attract';
export function go(next, opts = {}) {
  if (screen === 'attract' && next !== 'attract') startSession();
  screen = next;
  app.dataset.screen = next;
  render(opts);
  app.querySelector('.screen')?.classList.add('screen--enter');
  const h = app.querySelector('h1');
  if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  touch();
}

export function render(opts = {}) {
  app.innerHTML = renderScreen(screen, { state, session, t: t(), icons, config, ...opts });
  bindApp();
}

function startSession() {
  session = { patient: null, selected: new Set(), dob: '', name: '', revealed: false, ticket: null, error: null };
}

export function resetSession() {
  // Privacy: wipe everything personal, close dialogs, return to attract.
  stopDoneTimer(); stopReveal();
  session = null;
  if (idleDialog.open) idleDialog.close();
  if (helpDialog.open) helpDialog.close();
  live.textContent = '';
  screen = 'attract';
  app.dataset.screen = 'attract';
  render();
  stopIdle();
}

// ---------- idle timeout ----------
let idleTimer = null, countdownTimer = null;
export function touch() {
  if (screen === 'attract') return;
  stopIdle();
  idleTimer = setTimeout(showIdleWarning, config.idleWarnMs);
}
function stopIdle() { clearTimeout(idleTimer); clearInterval(countdownTimer); idleTimer = null; countdownTimer = null; }
function showIdleWarning() {
  if (screen === 'attract') return;
  let left = config.idleCountdownS;
  const cd = idleDialog.querySelector('.countdown');
  const paint = () => { cd.textContent = String(left); live.textContent = t().idleLive(left); };
  paint();
  if (!idleDialog.open) idleDialog.showModal();
  countdownTimer = setInterval(() => { left -= 1; paint(); if (left <= 0) resetSession(); }, 1000);
}

// ---------- done screen auto reset ----------
let doneTimer = null;
export function startDoneTimer() {
  let left = config.doneAutoResetS;
  const el = () => app.querySelector('[data-done-countdown]');
  doneTimer = setInterval(() => {
    left -= 1;
    const e = el(); if (e) e.textContent = t().screenClears(left);
    if (left <= 0) resetSession();
  }, 1000);
}
function stopDoneTimer() { clearInterval(doneTimer); doneTimer = null; }

// ---------- reveal names for a short time ----------
let revealTimer = null;
function stopReveal() { clearTimeout(revealTimer); revealTimer = null; }
function toggleReveal() {
  if (!session) return;
  session.revealed = !session.revealed;
  stopReveal();
  if (session.revealed) revealTimer = setTimeout(() => { if (session) { session.revealed = false; render(); } }, config.revealS * 1000);
  render();
}

// ---------- scanner (keyboard wedge) ----------
let scanBuf = '', scanAt = 0;
document.addEventListener('keydown', (e) => {
  if (!screen.startsWith('identify')) return;
  const now = performance.now();
  if (now - scanAt > 400) scanBuf = '';
  scanAt = now;
  if (e.key === 'Enter') { const code = scanBuf; scanBuf = ''; if (code.length >= 6) lookup({ code }); return; }
  if (e.key.length === 1) scanBuf += e.key;
});

// ---------- lookup ----------
async function lookup(query) {
  if (!session) return;
  session.error = null; session.busy = true; render();
  const res = await findPatient(query);
  session.busy = false;
  if (!res) { session.error = t().errNoMatch; render(); return; }
  session.patient = res;
  session.selected = new Set(res.prescriptions.filter((p) => p.status === 'ready').map((p) => p.rxNumber));
  go('list');
}

// ---------- actions ----------
const actions = {
  start: () => go('identify-dob'),
  lang: () => { state.lang = state.lang === 'en' ? 'es' : 'en'; document.documentElement.lang = state.lang; render(); paintChrome(); },
  a11y: () => { state.a11y = !state.a11y; document.documentElement.dataset.a11y = state.a11y ? 'on' : 'off'; render(); paintChrome(); },
  help: () => { helpDialog.dataset.called = 'no'; paintChrome(); helpDialog.showModal(); },
  'call-staff': () => { helpDialog.dataset.called = 'yes'; paintChrome(); },
  'close-help': () => helpDialog.close(),
  'start-over': () => resetSession(),
  'still-here': () => { idleDialog.close(); stopIdle(); touch(); },
  'finish-now': () => resetSession(),
  back: (el) => go(el.dataset.to),
  key: (el) => {
    const field = el.dataset.field, k = el.dataset.key;
    session.error = null;
    if (field === 'dob') {
      if (k === 'del') session.dob = session.dob.slice(0, -1);
      else if (k === 'clear') session.dob = '';
      else if (session.dob.length < 8) session.dob += k;
    } else {
      if (k === 'del') session.name = session.name.slice(0, -1);
      else if (k === 'clear') session.name = '';
      else if (k === 'space') { if (session.name && !session.name.endsWith(' ')) session.name += ' '; }
      else if (session.name.length < 24) session.name += k;
    }
    render();
  },
  'dob-continue': () => {
    if (session.dob.length !== 8) { session.error = t().errDob; render(); return; }
    go('identify-name');
  },
  find: () => { if (session.name.trim().length < 2) { session.error = t().errNoMatch; render(); return; } lookup({ dob: session.dob, lastName: session.name.trim() }); },
  toggle: (el) => {
    if (el.getAttribute('aria-disabled') === 'true') return;
    const id = el.dataset.rx;
    session.selected.has(id) ? session.selected.delete(id) : session.selected.add(id);
    session.error = null; render();
  },
  reveal: () => toggleReveal(),
  review: () => { if (session.selected.size === 0) { session.error = t().noneSelected; render(); return; } go('confirm'); },
  confirm: () => {
    session.ticket = { code: 'B-' + String(14 + Math.floor(Math.random() * 20)), counter: 2 };
    // The pick-up is now recorded; drop the patient record so the done screen carries no personal data.
    session.patient = null; session.dob = ''; session.name = ''; session.selectedCount = session.selected.size; session.selected = new Set();
    go('done'); startDoneTimer();
  },
  done: () => resetSession(),
};

function bindApp() {
  // Delegated pointer handling; every tap gives a beep and the CSS pressed state.
  app.onclick = (e) => {
    const el = e.target.closest('[data-action]');
    if (!el) { touch(); return; }
    beep(); touch();
    actions[el.dataset.action]?.(el);
  };
}

function paintChrome() {
  const s = t();
  idleDialog.querySelector('h2').textContent = s.idleTitle;
  idleDialog.querySelector('.lede').textContent = s.idleLede;
  idleDialog.querySelector('[data-action="still-here"]').textContent = s.stillHere;
  idleDialog.querySelector('[data-action="finish-now"]').textContent = s.finishNow;
  helpDialog.querySelector('h2').textContent = s.helpTitle;
  helpDialog.querySelector('.lede').textContent = helpDialog.dataset.called === 'yes' ? s.staffCalled : s.helpLede;
  const call = helpDialog.querySelector('[data-action="call-staff"]');
  call.textContent = s.callStaff; call.hidden = helpDialog.dataset.called === 'yes';
  helpDialog.querySelector('[data-action="close-help"]').textContent = s.close;
}

for (const d of [idleDialog, helpDialog]) {
  d.addEventListener('click', (e) => {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    beep(); actions[el.dataset.action]?.(el);
  });
  d.addEventListener('cancel', (e) => { e.preventDefault(); }); // Escape must not silently dismiss the privacy countdown
}

document.documentElement.lang = state.lang;
document.documentElement.dataset.a11y = state.a11y ? 'on' : 'off';
paintChrome();
render();

// Test hooks (read-only): expose the screen name and whether a session exists.
window.__kiosk = { get screen() { return screen; }, get hasSession() { return session !== null; }, get config() { return config; } };
