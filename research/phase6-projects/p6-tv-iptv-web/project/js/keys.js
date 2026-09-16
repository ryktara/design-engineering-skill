/* Remote key mapping for Tizen / webOS / desktop */
(function (global) {
  'use strict';

  var KEY = {
    LEFT: 'left', RIGHT: 'right', UP: 'up', DOWN: 'down',
    ENTER: 'enter', BACK: 'back', PLAY_PAUSE: 'playpause',
    PLAY: 'play', PAUSE: 'pause', STOP: 'stop',
    REW: 'rew', FF: 'ff', RED: 'red', GREEN: 'green', YELLOW: 'yellow', BLUE: 'blue',
    CH_UP: 'chup', CH_DOWN: 'chdown', INFO: 'info', GUIDE: 'guide'
  };

  var CODES = {
    // desktop / generic
    37: KEY.LEFT, 38: KEY.UP, 39: KEY.RIGHT, 40: KEY.DOWN,
    13: KEY.ENTER, 8: KEY.BACK, 27: KEY.BACK,
    // Tizen (Samsung)
    10009: KEY.BACK, 10252: KEY.PLAY_PAUSE, 415: KEY.PLAY, 19: KEY.PAUSE, 413: KEY.STOP,
    412: KEY.REW, 417: KEY.FF,
    403: KEY.RED, 404: KEY.GREEN, 405: KEY.YELLOW, 406: KEY.BLUE,
    427: KEY.CH_UP, 428: KEY.CH_DOWN, 457: KEY.INFO, 458: KEY.GUIDE,
    // webOS (LG)
    461: KEY.BACK, 1536: KEY.PLAY_PAUSE, 33: KEY.CH_UP, 34: KEY.CH_DOWN
  };

  var NAMES = {
    ArrowLeft: KEY.LEFT, ArrowRight: KEY.RIGHT, ArrowUp: KEY.UP, ArrowDown: KEY.DOWN,
    Enter: KEY.ENTER, Backspace: KEY.BACK, Escape: KEY.BACK,
    MediaPlayPause: KEY.PLAY_PAUSE, MediaPlay: KEY.PLAY, MediaPause: KEY.PAUSE,
    MediaStop: KEY.STOP, MediaRewind: KEY.REW, MediaFastForward: KEY.FF,
    GoBack: KEY.BACK, ColorF0Red: KEY.RED, ColorF1Green: KEY.GREEN,
    ColorF2Yellow: KEY.YELLOW, ColorF3Blue: KEY.BLUE
  };

  function fromEvent(e) {
    if (e.key && NAMES[e.key]) return NAMES[e.key];
    var code = e.keyCode || e.which;
    return CODES[code] || null;
  }

  // Register keys with the Tizen input device API so the platform delivers them.
  function registerTizenKeys() {
    try {
      if (global.tizen && global.tizen.tvinputdevice) {
        ['MediaPlayPause', 'MediaPlay', 'MediaPause', 'MediaStop', 'MediaRewind',
         'MediaFastForward', 'ChannelUp', 'ChannelDown', 'ColorF0Red', 'ColorF1Green',
         'ColorF2Yellow', 'ColorF3Blue', 'Info', 'Guide'].forEach(function (k) {
          try { global.tizen.tvinputdevice.registerKey(k); } catch (err) { /* not supported */ }
        });
      }
    } catch (err) { /* running on desktop */ }
  }

  // Platform exit — Tizen first, webOS fallback, then window.close for desktop.
  function exitApp() {
    try {
      if (global.tizen && global.tizen.application) {
        global.tizen.application.getCurrentApplication().exit();
        return;
      }
    } catch (err) { /* fall through */ }
    try {
      if (global.webOS && global.webOS.platformBack) {
        global.webOS.platformBack();
        return;
      }
    } catch (err) { /* fall through */ }
    global.close();
  }

  global.Keys = { KEY: KEY, fromEvent: fromEvent, registerTizenKeys: registerTizenKeys, exitApp: exitApp };
})(window);
