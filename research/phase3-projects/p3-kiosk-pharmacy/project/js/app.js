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
  // Identify step: only the visitor's own partial typing is on screen (no fetched record yet), so the window between
  // key taps is longer and the countdown slower. Anyone typing one digit a minute still finishes. Screens that show
  // prescription data keep the short window above.
  entryWarnMs: Number(params.get('entryIdle') ?? 90) * 1000,
  entryCountdownS: Number(params.get('entryCount') ?? 30),
  doneAutoResetS: Number(params.get('done') ?? 20),
  revealS: 10,
  steps: 3,
};

// Per-visitor defaults (URL params are the installation's defaults). `chosen` is false until the
// visitor confirms the first-visit chooser or touches Start; resetSession restores all three so the
// next visitor gets the defaults and the chooser again.
const defaults = { lang: params.get('lang') === 'es' ? 'es' : 'en', a11y: params.get('a11y') === 'on', chosen: params.get('chooser') === 'off' };
export const state = { ...defaults, sound: true };
let session = null; // { patient, selected:Set, dob, name, revealed, ticket }

export const t = () => strings[state.lang];
export const getSession = () => session;

const app = document.getElementById('app');
const idleDialog = document.getElementById('idle-dialog');
const helpDialog = document.getElementById('help-dialog');
const live = document.getElementById('live');
const livePolite = document.getElementById('live-polite');

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

// Re-rendering replaces the whole screen; keep keyboard/switch focus on the equivalent control so a user stepping
// through the keypad does not fall back to <body> after every key.
function focusKeyOf(el) {
  if (!el || el === document.body || !app.contains(el)) return null;
  const a = el.dataset?.action; if (!a) return el.id ? `#${el.id}` : null;
  return `[data-action="${a}"]` + (el.dataset.field ? `[data-field="${el.dataset.field}"]` : '') + (el.dataset.key ? `[data-key="${el.dataset.key}"]` : '') + (el.dataset.to ? `[data-to="${el.dataset.to}"]` : '');
}
export function render(opts = {}) {
  const keep = focusKeyOf(document.activeElement);
  app.innerHTML = renderScreen(screen, { state, session, t: t(), icons, config, ...opts });
  bindApp();
  if (keep) app.querySelector(keep)?.focus({ preventScroll: true });
}

// Spoken feedback for the value being built on screen (digits/letters read one by one).
function announceValue() {
  if (!session) return;
  if (screen === 'identify-dob') livePolite.textContent = t().typedDob(session.dob.split('').join(' '));
  else if (screen === 'identify-name') livePolite.textContent = t().typedName(session.name.split('').join(' '));
}

// MMDDYYYY: complete, month 01-12, day within the month, year between 1900 and today.
// Returns a string KEY (errDob / errDobInvalid), not the text: `session.error` holds keys so that a language switch
// re-renders the message in the new language instead of freezing the wording of the moment the error happened.
export function dobProblem(d) {
  if (d.length !== 8) return 'errDob';
  const m = +d.slice(0, 2), day = +d.slice(2, 4), y = +d.slice(4, 8);
  const now = new Date();
  if (m < 1 || m > 12 || y < 1900 || y > now.getFullYear()) return 'errDobInvalid';
  const dim = new Date(y, m, 0).getDate();
  if (day < 1 || day > dim) return 'errDobInvalid';
  if (new Date(y, m - 1, day) > now) return 'errDobInvalid';
  return null;
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
  live.textContent = ''; livePolite.textContent = '';
  screen = 'attract';
  app.dataset.screen = 'attract';
  // Next visitor: default language and view, chooser shown again.
  Object.assign(state, defaults);
  document.documentElement.lang = state.lang;
  document.documentElement.dataset.a11y = state.a11y ? 'on' : 'off';
  paintChrome();
  render();
  stopIdle();
}

// ---------- idle timeout ----------
let idleTimer = null, countdownTimer = null;
const isEntry = () => screen.startsWith('identify');
export function touch() {
  if (screen === 'attract') return;
  stopIdle();
  idleTimer = setTimeout(showIdleWarning, isEntry() ? config.entryWarnMs : config.idleWarnMs);
}
function stopIdle() { clearTimeout(idleTimer); clearInterval(countdownTimer); idleTimer = null; countdownTimer = null; }
// What the visitor has typed so far, formatted as the field shows it, so the warning can prove nothing was lost.
function typedSoFar() {
  if (!session) return '';
  if (screen === 'identify-dob') { const d = session.dob; return `${d.slice(0, 2)}${d.length > 2 ? ' / ' : ''}${d.slice(2, 4)}${d.length > 4 ? ' / ' : ''}${d.slice(4, 8)}`; }
  if (screen === 'identify-name') return session.name;
  return '';
}
function showIdleWarning() {
  if (screen === 'attract') return;
  const entry = isEntry();
  let left = entry ? config.entryCountdownS : config.idleCountdownS;
  idleDialog.dataset.entry = entry ? 'yes' : 'no';
  paintChrome();
  const cd = idleDialog.querySelector('.countdown');
  const paint = () => { cd.textContent = String(left); live.textContent = t().idleLive(left); };
  paint();
  if (!idleDialog.open) idleDialog.showModal();
  countdownTimer = setInterval(() => { left -= 1; paint(); if (left <= 0) resetSession(); }, 1000);
}
// Any touch on the panel counts as presence, not only taps that land on a control (a finger that misses a key,
// a hand resting on the screen while reading). Attract is excluded in touch() itself.
document.addEventListener('pointerdown', () => { if (!idleDialog.open) touch(); }, { passive: true });

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

// ---------- physical keys: scanner (keyboard wedge) and tactile keypad ----------
// A scanner delivers its code as a burst (a few ms between keys) ending with Enter. A person on the tactile keypad
// types at human speed. Human-speed keys go into the current field; a burst stays in the scan buffer.
let scanBuf = '', scanAt = 0, burst = false, pendingKey = null, pendingTimer = null;
const BURST_MS = 80;
function cancelPending() { clearTimeout(pendingTimer); pendingTimer = null; pendingKey = null; }
function applyPhysicalKey(k) {
  if (!session) return;
  if (screen === 'identify-dob') { if (!/^\d$/.test(k) || session.dob.length >= 8) return; session.dob += k; }
  else if (screen === 'identify-name') {
    const up = k.toUpperCase();
    if (!/^[A-Z\-' ]$/.test(up) || session.name.length >= 24) return;
    if (up === ' ') { if (!session.name || session.name.endsWith(' ')) return; }
    session.name += up;
  } else return;
  session.error = null; render(); announceValue(); touch();
}
document.addEventListener('keydown', (e) => {
  if (!screen.startsWith('identify') || !session) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target instanceof HTMLButtonElement && (e.key === 'Enter' || e.key === ' ')) return; // activating an on-screen key
  // Typing on the tactile keypad while the warning is up is the clearest sign someone is still there: dismiss it and
  // let the key go into the field as usual, instead of swallowing it behind the modal.
  if (idleDialog.open && (e.key.length === 1 || e.key === 'Backspace')) { actions['still-here'](); }
  const now = performance.now(), gap = now - scanAt; scanAt = now;
  if (gap > 400) { scanBuf = ''; burst = false; }
  if (e.key === 'Enter') {
    e.preventDefault();
    if (burst && scanBuf.length >= 6) { const code = scanBuf; scanBuf = ''; burst = false; cancelPending(); lookup({ code }); return; }
    cancelPending(); scanBuf = '';
    beep(); touch(); actions[screen === 'identify-dob' ? 'dob-continue' : 'find']();
    return;
  }
  if (e.key === 'Backspace') {
    e.preventDefault(); cancelPending();
    if (screen === 'identify-dob') session.dob = session.dob.slice(0, -1); else session.name = session.name.slice(0, -1);
    session.error = null; render(); announceValue(); touch();
    return;
  }
  if (e.key.length !== 1) return;
  scanBuf += e.key;
  if (pendingKey !== null && gap < BURST_MS) { burst = true; cancelPending(); } // scanner speed: not a person
  if (burst) return;
  pendingKey = e.key; clearTimeout(pendingTimer);
  pendingTimer = setTimeout(() => { const k = pendingKey; cancelPending(); applyPhysicalKey(k); }, BURST_MS + 10);
});

// ---------- lookup ----------
async function lookup(query) {
  if (!session) return;
  session.error = null; session.busy = true; render();
  const res = await findPatient(query);
  session.busy = false;
  if (!res) { session.error = 'errNoMatch'; render(); return; }
  session.patient = res;
  session.selected = new Set(res.prescriptions.filter((p) => p.status === 'ready').map((p) => p.rxNumber));
  go('list');
}

// ---------- actions ----------
// Switching language re-renders the current screen from `session` (typed value, selection, error all kept) and repaints
// the dialogs; the polite region names the new language in that language so a screen-reader user hears the change.
function applyLang(lang) { state.lang = lang; document.documentElement.lang = lang; render(); paintChrome(); livePolite.textContent = t().langChanged; }
function applyA11y(on) { state.a11y = on; document.documentElement.dataset.a11y = on ? 'on' : 'off'; render(); paintChrome(); }

const actions = {
  start: () => { state.chosen = true; go('identify-dob'); },
  lang: () => applyLang(state.lang === 'en' ? 'es' : 'en'),
  a11y: () => applyA11y(!state.a11y),
  // first-visit chooser (attract only): immediate effect, no flow change
  'set-lang': (el) => applyLang(el.dataset.lang === 'es' ? 'es' : 'en'),
  'set-a11y': (el) => applyA11y(el.dataset.a11y === 'on'),
  'chooser-done': () => { state.chosen = true; render(); },
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
    render(); announceValue();
  },
  'dob-continue': () => {
    const problem = dobProblem(session.dob);
    if (problem) { session.error = problem; render(); return; }
    go('identify-name');
  },
  find: () => { if (session.name.trim().length < 2) { session.error = 'errName'; render(); return; } lookup({ dob: session.dob, lastName: session.name.trim() }); },
  toggle: (el) => {
    if (el.getAttribute('aria-disabled') === 'true') return;
    const id = el.dataset.rx;
    session.selected.has(id) ? session.selected.delete(id) : session.selected.add(id);
    session.error = null; render();
  },
  reveal: () => toggleReveal(),
  review: () => { if (session.selected.size === 0) { session.error = 'noneSelected'; render(); return; } go('confirm'); },
  confirm: () => {
    session.ticket = { code: 'B-' + String(14 + Math.floor(Math.random() * 20)), counter: 2 };
    // The pick-up is now recorded; drop the patient record so the done screen carries no personal data.
    session.patient = null; session.dob = ''; session.name = ''; session.selectedCount = session.selected.size; session.selected = new Set();
    go('done'); startDoneTimer();
    // Completion is announced once, in words, through the polite status region: a screen reader user who cannot see
    // the green tick still hears that the pick-up is finished and where the ticket sends them.
    livePolite.textContent = t().doneAnnounce(session.ticket.code, session.ticket.counter);
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
  const entry = idleDialog.dataset.entry === 'yes';
  idleDialog.querySelector('h2').textContent = entry ? s.idleTitleEntry : s.idleTitle;
  idleDialog.querySelector('.lede').textContent = entry ? s.idleLedeEntry : s.idleLede;
  const kept = idleDialog.querySelector('[data-idle-kept]'); const typed = entry ? typedSoFar() : '';
  kept.hidden = !typed;
  kept.innerHTML = typed ? `<span class="dialog__kept-label">${s.idleKept}</span><span class="dialog__kept-value num">${typed.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]))}</span>` : '';
  idleDialog.querySelector('[data-action="still-here"]').textContent = entry ? s.keepTyping : s.stillHere;
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
    if (!el) {
      // Idle warning: a touch anywhere on it (or on the backdrop) means "still here"; only Finish now ends the session.
      if (d === idleDialog) { beep(); actions['still-here'](); }
      return;
    }
    beep(); actions[el.dataset.action]?.(el);
  });
  d.addEventListener('cancel', (e) => { e.preventDefault(); }); // Escape must not silently dismiss the privacy countdown
}

document.documentElement.lang = state.lang;
document.documentElement.dataset.a11y = state.a11y ? 'on' : 'off';
paintChrome();
render();

// Test hooks (read-only): expose the screen name and whether a session exists.
window.__kiosk = { get screen() { return screen; }, get hasSession() { return session !== null; }, get config() { return config; }, get state() { return { lang: state.lang, a11y: state.a11y, chosen: state.chosen }; } };
