import SwiftUI

/// Root of the tvOS app. Session state decides between the sign-in flow and the catalogue/player.
@main
struct LumenApp: App {
    @State private var session = SessionStore()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(session)
                .preferredColorScheme(.dark)          // dark-first canvas; see Theme/Tokens.swift
        }
    }
}

struct RootView: View {
    @Environment(SessionStore.self) private var session

    var body: some View {
        ZStack {
            LumenColor.canvas.ignoresSafeArea()      // backgrounds may bleed; chrome stays inside the safe area
            switch session.state {
            case .signedOut:
                SignInView()
            case .signedIn:
                // Kept small for this exercise: the catalogue is a single "Continue watching" entry point.
                PlayerView(episode: SampleCatalogue.nextUp, queue: SampleCatalogue.queue)
            }
        }
        .animation(reduceMotionAware(.easeInOut(duration: 0.25)), value: session.state)
    }

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    private func reduceMotionAware(_ a: Animation) -> Animation? { reduceMotion ? nil : a }
}

@Observable
final class SessionStore {
    enum State: Equatable { case signedOut, signedIn(accountName: String) }
    var state: State = .signedOut
}
