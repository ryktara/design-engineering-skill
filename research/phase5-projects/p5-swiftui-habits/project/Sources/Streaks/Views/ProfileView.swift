import SwiftUI

/// Profile: settings-style grouped list.
struct ProfileView: View {
    @Environment(\.theme) private var theme
    @EnvironmentObject private var store: Store

    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack(spacing: theme.spacing.md) {
                        Text("T")
                            .font(theme.font.title2)
                            .foregroundStyle(theme.color.surface)
                            .frame(width: 56, height: 56)
                            .background(theme.color.accent)
                            .clipShape(Circle())

                        VStack(alignment: .leading, spacing: theme.spacing.xs) {
                            Text("Tara")
                                .font(theme.font.headline)
                                .foregroundStyle(theme.color.text)
                            Text("\(store.activeHabits.count) habits · \(store.longestStreak) day best streak")
                                .font(theme.font.caption)
                                .foregroundStyle(theme.color.textSecondary)
                        }
                    }
                    .padding(.vertical, theme.spacing.xs)
                }
                .listRowBackground(theme.color.surface)

                Section {
                    Toggle(isOn: $store.remindersEnabled) {
                        SettingsLabel(title: "Reminders", systemImage: "bell.fill")
                    }
                    .tint(theme.color.accent)

                    Toggle(isOn: $store.weekStartsOnMonday) {
                        SettingsLabel(title: "Week starts on Monday", systemImage: "calendar")
                    }
                    .tint(theme.color.accent)
                } header: {
                    header("Preferences")
                }
                .listRowBackground(theme.color.surface)

                Section {
                    NavigationLink {
                        placeholder("Appearance")
                    } label: {
                        SettingsLabel(title: "Appearance", systemImage: "paintpalette.fill", detail: "System")
                    }
                    NavigationLink {
                        placeholder("Export data")
                    } label: {
                        SettingsLabel(title: "Export data", systemImage: "square.and.arrow.up")
                    }
                } header: {
                    header("App")
                }
                .listRowBackground(theme.color.surface)

                Section {
                    NavigationLink {
                        placeholder("About")
                    } label: {
                        SettingsLabel(title: "About Streaks", systemImage: "info.circle.fill", detail: "1.0")
                    }
                }
                .listRowBackground(theme.color.surface)
            }
            .scrollContentBackground(.hidden)
            .pageBackground(theme)
            .navigationTitle("Profile")
        }
    }

    private func header(_ title: String) -> some View {
        Text(title)
            .font(theme.font.caption)
            .foregroundStyle(theme.color.textSecondary)
    }

    private func placeholder(_ title: String) -> some View {
        Text(title)
            .font(theme.font.body)
            .foregroundStyle(theme.color.textSecondary)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .pageBackground(theme)
            .navigationTitle(title)
    }
}

private struct SettingsLabel: View {
    @Environment(\.theme) private var theme

    let title: String
    let systemImage: String
    var detail: String? = nil

    var body: some View {
        HStack(spacing: theme.spacing.md) {
            Image(systemName: systemImage)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(theme.color.accent)
                .frame(width: 30, height: 30)
                .background(theme.color.accentSoft)
                .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))

            Text(title)
                .font(theme.font.body)
                .foregroundStyle(theme.color.text)

            Spacer()

            if let detail {
                Text(detail)
                    .font(theme.font.subheadline)
                    .foregroundStyle(theme.color.textSecondary)
            }
        }
    }
}

#Preview {
    ProfileView()
        .environmentObject(Store())
}
