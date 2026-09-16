# Lumen (tvOS, SwiftUI)

Documentary streaming app for Apple TV. Two flows:

- **Sign-in** (`SignIn/`): activation code on screen + QR code, polled against the account service, with an
  "enter on this device" fallback that uses the system keyboard.
- **Player** (`Player/`): custom transport controls over `AVPlayerLayer`, auto-hide after 5 s, subtitle/audio side
  sheet, "next episode" prompt at the credits marker.

Focus engine, Siri Remote gestures and Menu semantics are documented inline; `Theme/Tokens.swift` holds the design
tokens (60 pt safe area, TV type scale, focus ring).

Build: add these sources to a tvOS 17 app target (no Xcode project is checked in).
