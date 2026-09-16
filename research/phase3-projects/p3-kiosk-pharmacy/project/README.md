# RxPoint pick-up kiosk

Public touch kiosk (portrait 1080x1920) for pharmacy prescription pick-up.
Plain HTML + CSS + vanilla JS modules, no build step, no CDN. Serve `project/` statically.

Flow: attract -> identify (DOB + last name, or scan) -> ready list -> confirm -> done.
The attract screen opens with a first-visit chooser (language EN/ES, standard or accessible view); choices apply immediately, persist through the flow, and reset with the session. `?chooser=off` hides it.
Inside the flow the utility bar at the bottom of every screen carries the language switch (labelled in the other language), the view toggle, help, and start over; switching language keeps what has been typed or selected.
Idle timeout clears the session and any personal data from the DOM.
