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
                CatalogueShell()
            }
        }
        .animation(reduceMotionAware(.easeInOut(duration: 0.25)), value: session.state)
    }

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    private func reduceMotionAware(_ a: Animation) -> Animation? { reduceMotion ? nil : a }
}

/// Signed-in shell: the system top tab bar with Watch (continue watching → player) and Search at the
/// trailing edge (tv-dpad-axes: search lives at a predictable edge). Two sections is the top-tabs case
/// (side navigation is for 4–8). The player is presented full screen over the shell; Menu inside the player
/// unwinds its own layers first (PlayerView), then dismisses back to the tab that opened it.
struct CatalogueShell: View {
    var body: some View {
        TabView {
            ContinueWatchingView()
                .tabItem { Label("Watch", systemImage: "play.fill") }
            SearchView()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
        }
        .background(LumenColor.canvas.ignoresSafeArea())
    }
}

/// Minimal "Watch" tab for this exercise: one continue-watching card that opens the player.
struct ContinueWatchingView: View {
    @State private var playing: Episode?
    @Namespace private var scope

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.l) {
            Text("Continue watching").font(LumenFont.title).foregroundStyle(LumenColor.textPrimary)
                .accessibilityAddTraits(.isHeader)
            Button {
                playing = SampleCatalogue.nextUp
            } label: {
                VStack(alignment: .leading, spacing: LumenSpace.xs) {
                    Text(SampleCatalogue.nextUp.series.title.uppercased()).font(LumenFont.caption).tracking(2).foregroundStyle(LumenColor.textSecondary)
                    Text(SampleCatalogue.nextUp.label).font(LumenFont.headline).foregroundStyle(LumenColor.textPrimary)
                    Text("Resume · 28 min left").font(LumenFont.caption).foregroundStyle(LumenColor.textSecondary)
                }
                .frame(width: 560, alignment: .leading)
            }
            .buttonStyle(.tvPrimary)
            .prefersDefaultFocus(in: scope)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .padding(LumenSpace.safeArea)
        .focusScope(scope)
        .fullScreenCover(item: $playing) { PlayerView(episode: $0, queue: SampleCatalogue.queue) }
    }
}

@Observable
final class SessionStore {
    enum State: Equatable { case signedOut, signedIn(accountName: String) }
    var state: State = .signedOut
}
