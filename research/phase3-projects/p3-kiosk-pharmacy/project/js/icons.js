// Filled icon set (always paired with a visible label). Decorative: aria-hidden.
const wrap = (paths) => `<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false">${paths}</svg>`;
export const icons = {
  pharmacy: wrap('<path d="M24 4l20 8v10c0 11.5-8.5 20.4-20 22C12.5 42.4 4 33.5 4 22V12l20-8zm-3 12v6h-6v6h6v6h6v-6h6v-6h-6v-6h-6z"/>'),
  help: wrap('<path d="M24 4a20 20 0 1 0 0 40 20 20 0 0 0 0-40zm0 32a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm3.2-11.6c-1 .7-1.2 1.2-1.2 2.6h-4c0-2.8.9-4.3 3-5.7 1.6-1.1 2.2-1.8 2.2-3.1 0-1.7-1.3-2.9-3.2-2.9-2 0-3.4 1.3-3.5 3.4h-4.2c.1-4.3 3.2-7.2 7.7-7.2 4.4 0 7.4 2.7 7.4 6.5 0 2.7-1.2 4.5-4.2 6.4z"/>'),
  language: wrap('<path fill-rule="evenodd" d="M24 4a20 20 0 1 0 0 40 20 20 0 0 0 0-40zm0 4a16 16 0 1 1 0 32 16 16 0 0 1 0-32z"/><path fill-rule="evenodd" d="M24 4c-6.6 0-12 9-12 20s5.4 20 12 20 12-9 12-20S30.6 4 24 4zm0 4c4.4 0 8 7.2 8 16s-3.6 16-8 16-8-7.2-8-16 3.6-16 8-16z"/><path d="M6 22h36v4H6z"/>'),
  a11y: wrap('<circle cx="24" cy="8" r="4.5"/><path d="M10 15.5c9.3 1.7 18.7 1.7 28 0l.8 4c-3.4.7-6.7 1.2-10 1.5v6.5l5.6 14.8-3.8 1.4L25.3 30h-2.6l-5.3 13.7-3.8-1.4L19.2 27.5V21c-3.3-.3-6.6-.8-10-1.5l.8-4z"/>'),
  restart: wrap('<path d="M24 8a16 16 0 0 1 13.9 8H32v4h12V8h-4v4.6A20 20 0 1 0 44 24h-4a16 16 0 1 1-16-16z"/>'),
  back: wrap('<path d="M20 8l4 4-9 9h27v6H15l9 9-4 4L4 24z"/>'),
  scan: wrap('<path d="M4 4h12v4H8v8H4zm28 0h12v12h-4V8h-8zM4 32h4v8h8v4H4zm36 0h4v12H32v-4h8zM10 14h3v20h-3zm5 0h5v20h-5zm7 0h3v20h-3zm5 0h6v20h-6zm8 0h3v20h-3z"/>'),
  delete: wrap('<path d="M16 8h28v32H16L2 24 16 8zm6 7l-3 3 6 6-6 6 3 3 6-6 6 6 3-3-6-6 6-6-3-3-6 6-6-6z"/>'),
  check: wrap('<path d="M18 33.2L7.4 22.6l-4.2 4.2L18 41.6 45 14.6l-4.2-4.2z"/>'),
  alert: wrap('<path d="M24 3l22 40H2L24 3zm-2 14v12h4V17h-4zm0 16v4h4v-4h-4z"/>'),
  eye: wrap('<path d="M24 10C13 10 5 18 2 24c3 6 11 14 22 14s19-8 22-14c-3-6-11-14-22-14zm0 22a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm0-12a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/>'),
  eyeOff: wrap('<path d="M4 6l3-3 38 38-3 3-7.6-7.6C31.3 37.4 27.8 38 24 38 13 38 5 30 2 24c1.5-3 4.4-6.6 8.3-9.6L4 6zm14.4 14.4A8 8 0 0 0 27.6 29.6l-9.2-9.2zM24 10c11 0 19 8 22 14-1.2 2.4-3.3 5.2-6 7.8L34.4 26a8 8 0 0 0-8.4-8.4L20.8 12.4C21.8 10.9 22.9 10 24 10z"/>'),
  success: wrap('<path d="M24 4a20 20 0 1 0 0 40 20 20 0 0 0 0-40zm-3 29L11 23l3.5-3.5 6.5 6.5L33.5 12 37 15.5z"/>'),
  counter: wrap('<path d="M4 8h40v6H4zm2 8h36v4H6zm0 6h36v18H6zm6 4v10h6V26zm12 0v10h12V26z"/>'),
  bag: wrap('<path d="M16 14a8 8 0 0 1 16 0h8v30H8V14h8zm4 0h8a4 4 0 0 0-8 0zm2 8v6h-6v6h6v6h6v-6h6v-6h-6v-6h-6z"/>'),
};
