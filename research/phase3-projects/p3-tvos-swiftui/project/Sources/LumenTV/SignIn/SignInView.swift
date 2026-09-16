import SwiftUI

/// Sign-in: code-on-screen + companion device, with a keyboard fallback. Nothing on this screen requires
/// typing; the two focusable buttons live in one row inside the 60 pt safe area.
///
/// Focus engine:
/// - `focusScope` + `prefersDefaultFocus` puts initial focus on the fallback button (the only action the viewer
///   can take on the TV itself). The code and QR are not focusable; VoiceOver reads them via the merged label.
/// - When the code is refreshed the buttons keep their identity, so focus stays where it was.
/// - Menu on this screen is left to the system (suspends the app): there is no layer beneath sign-in to unwind to.
struct SignInView: View {
    @Environment(SessionStore.self) private var session
    @State private var model = SignInModel(service: MockActivationService())
    @Namespace private var signInScope
    @FocusState private var focus: Focus?

    enum Focus: Hashable { case fallback, newCode }

    var body: some View {
        ZStack {
            switch model.route {
            case .activation:
                activation
                    .transition(.opacity)
            case .deviceSignIn:
                DeviceSignInView(model: model)
                    .transition(.opacity)
            }
        }
        .task { await model.start() }
        .onChange(of: model.route) { _, route in
            // Focus restoration: coming back from the fallback route lands on the button that opened it.
            if route == .activation { focus = .fallback }
        }
        .onChange(of: model.approvedAccount) { _, name in
            if let name { session.state = .signedIn(accountName: name) }
        }
    }

    private var activation: some View {
        HStack(alignment: .center, spacing: LumenSpace.xl * 1.5) {
            // Left column: instructions + code (the focal point) + actions.
            VStack(alignment: .leading, spacing: LumenSpace.l) {
                Text("Sign in to Lumen")
                    .font(LumenFont.display)
                    .foregroundStyle(LumenColor.textPrimary)
                    .accessibilityAddTraits(.isHeader)

                Text("On your phone or computer, go to **lumen.tv/activate** and enter this code.")
                    .font(LumenFont.body)
                    .foregroundStyle(LumenColor.textSecondary)
                    .lineSpacing(6)
                    .frame(maxWidth: 960, alignment: .leading)   // one line at 29 pt; avoids an orphaned "this code."

                codeTile

                statusLine

                HStack(spacing: LumenSpace.m) {
                    Button("Sign in on this Apple TV instead") { model.route = .deviceSignIn }
                        .buttonStyle(.tvPrimary)
                        .focused($focus, equals: .fallback)
                        .prefersDefaultFocus(in: signInScope)

                    Button("Get a new code") { Task { await model.refreshCode() } }
                        .buttonStyle(.tvSecondary)
                        .focused($focus, equals: .newCode)
                        .disabled(model.isRequestingCode)
                }
                .focusSection()
                .padding(.top, LumenSpace.s)
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            // Right column: QR twin of the code. Same payload, so either path works.
            VStack(spacing: LumenSpace.m) {
                if let code = model.code {
                    QRCodeView(payload: code.activationURL.absoluteString)
                } else {
                    RoundedRectangle(cornerRadius: LumenFocus.cornerRadius)
                        .fill(LumenColor.surface)
                        .frame(width: 368, height: 368)
                        .overlay(ProgressView().tint(LumenColor.textSecondary))
                }
                Text("Or scan with your phone")
                    .font(LumenFont.caption)
                    .foregroundStyle(LumenColor.textSecondary)
            }
        }
        .padding(LumenSpace.safeArea)           // all persistent UI inside the 60 pt tvOS safe area
        .focusScope(signInScope)
        .background(alignment: .bottomTrailing) { backdrop }
    }

    private var codeTile: some View {
        Group {
            if let code = model.code {
                Text(code.display)
                    .font(LumenFont.code)
                    .tracking(14)
                    .foregroundStyle(LumenColor.textPrimary)
                    .monospacedDigit()
                    .accessibilityLabel(Text("Activation code: \(code.value.map(String.init).joined(separator: " "))"))
                    .accessibilityAddTraits(.updatesFrequently)
            } else {
                Text("–––-–––")
                    .font(LumenFont.code)
                    .tracking(14)
                    .foregroundStyle(LumenColor.textSecondary.opacity(0.4))
                    .accessibilityLabel("Getting a code")
            }
        }
        .padding(.horizontal, LumenSpace.l)
        .padding(.vertical, LumenSpace.m)
        .background(LumenColor.surface, in: RoundedRectangle(cornerRadius: LumenFocus.cornerRadius, style: .continuous))
    }

    @ViewBuilder private var statusLine: some View {
        HStack(spacing: LumenSpace.s) {
            switch model.status {
            case .waiting(let remaining):
                ProgressView().tint(LumenColor.textSecondary)
                Text("Waiting for you to enter the code · expires in \(remaining)")
            case .expired:
                Image(systemName: "clock.badge.exclamationmark")
                Text("This code has expired. Get a new one to continue.")
            case .approved(let name):
                Image(systemName: "checkmark.circle.fill").foregroundStyle(LumenColor.positive)
                Text("Signed in as \(name)")
            case .error(let message):
                Image(systemName: "wifi.exclamationmark")
                Text(message)
            case .idle:
                Text(" ")
            }
        }
        .font(LumenFont.caption)
        .foregroundStyle(LumenColor.textSecondary)
        .frame(minHeight: 40, alignment: .leading)
        .accessibilityElement(children: .combine)
    }

    /// Low-contrast documentary still behind the layout; the gradient scrim keeps text at >=7:1 wherever it lands.
    private var backdrop: some View {
        LinearGradient(colors: [LumenColor.canvas, LumenColor.canvas.opacity(0.0)],
                       startPoint: .leading, endPoint: .trailing)
            .background(
                AsyncImage(url: SampleCatalogue.nextUp.artworkURL) { image in
                    image.resizable().scaledToFill()
                } placeholder: {
                    Color.clear
                }
                .opacity(0.35)
            )
            .ignoresSafeArea()
            .allowsHitTesting(false)
    }
}

/// Fallback: email + password with the system keyboard (never a custom on-screen keyboard).
/// Menu returns to the activation screen; focus restores to the button that opened this route.
struct DeviceSignInView: View {
    @Bindable var model: SignInModel
    @FocusState private var focus: Field?
    @Namespace private var scope
    enum Field { case email, password, submit }

    var body: some View {
        VStack(alignment: .leading, spacing: LumenSpace.l) {
            Text("Sign in on this Apple TV")
                .font(LumenFont.title)
                .foregroundStyle(LumenColor.textPrimary)
                .accessibilityAddTraits(.isHeader)
            Text("Typing with the remote is slow; the code on the previous screen is faster. Press Menu to go back.")
                .font(LumenFont.caption)
                .foregroundStyle(LumenColor.textSecondary)

            TextField("Email", text: $model.email)
                .textContentType(.emailAddress)
                .keyboardType(.emailAddress)
                .textInputAutocapitalization(.never)
                .focused($focus, equals: .email)
                .prefersDefaultFocus(in: scope)
            SecureField("Password", text: $model.password)
                .textContentType(.password)
                .focused($focus, equals: .password)
                .onSubmit { Task { await model.submitCredentials() } }

            if let error = model.credentialError {
                Label(error, systemImage: "exclamationmark.triangle.fill")
                    .font(LumenFont.caption)
                    .foregroundStyle(LumenColor.accent)
            }

            Button(model.isSubmitting ? "Signing in…" : "Sign in") { Task { await model.submitCredentials() } }
                .buttonStyle(.tvPrimary)
                .focused($focus, equals: .submit)
                .disabled(model.isSubmitting || model.email.isEmpty || model.password.isEmpty)
        }
        .frame(maxWidth: 900, alignment: .leading)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        .padding(LumenSpace.safeArea)
        .focusScope(scope)
        .onExitCommand { model.route = .activation }   // Menu unwinds one layer; nothing else
    }
}

@Observable
final class SignInModel {
    enum Route { case activation, deviceSignIn }
    enum Status: Equatable { case idle, waiting(remaining: String), expired, approved(String), error(String) }

    var route: Route = .activation
    var code: ActivationCode?
    var status: Status = .idle
    var isRequestingCode = false
    var approvedAccount: String?

    var email = ""
    var password = ""
    var isSubmitting = false
    var credentialError: String?

    private let service: ActivationService
    private var pollTask: Task<Void, Never>?

    init(service: ActivationService) { self.service = service }

    func start() async { await refreshCode() }

    func refreshCode() async {
        pollTask?.cancel()
        isRequestingCode = true
        defer { isRequestingCode = false }
        do {
            let c = try await service.requestCode()
            code = c
            status = .waiting(remaining: Self.remaining(until: c.expiresAt))
            pollTask = Task { [weak self] in await self?.pollLoop(c) }
        } catch {
            status = .error(ActivationError.network.localizedDescription)
        }
    }

    private func pollLoop(_ c: ActivationCode) async {
        while !Task.isCancelled {
            if Date() >= c.expiresAt { status = .expired; return }
            do {
                if let name = try await service.poll(c) {
                    status = .approved(name)
                    try? await Task.sleep(for: .milliseconds(900))   // let the viewer see the confirmation
                    approvedAccount = name
                    return
                }
                status = .waiting(remaining: Self.remaining(until: c.expiresAt))
            } catch {
                status = .error(ActivationError.network.localizedDescription)
                try? await Task.sleep(for: .seconds(5))
            }
        }
    }

    func submitCredentials() async {
        guard !isSubmitting else { return }
        isSubmitting = true; credentialError = nil
        defer { isSubmitting = false }
        do { approvedAccount = try await service.signIn(email: email, password: password) }
        catch { credentialError = error.localizedDescription }
    }

    private static func remaining(until date: Date) -> String {
        let s = max(0, Int(date.timeIntervalSinceNow))
        return String(format: "%d:%02d", s / 60, s % 60)
    }
}
