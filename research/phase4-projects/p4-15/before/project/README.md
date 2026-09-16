# RxPoint pick-up kiosk

Public touch kiosk (portrait 1080x1920) for pharmacy prescription pick-up.
Plain HTML + CSS + vanilla JS modules, no build step, no CDN. Serve `project/` statically.

Flow: attract -> identify (DOB + last name, or scan) -> ready list -> confirm -> done.
Idle timeout clears the session and any personal data from the DOM.
