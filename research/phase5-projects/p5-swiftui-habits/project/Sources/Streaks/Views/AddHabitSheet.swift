import SwiftUI

/// Modal form for creating a habit.
///
/// Keyboard behaviour: the name field takes focus when the sheet opens, its
/// return key is "Done" and dismisses the keyboard, dragging the form also
/// dismisses it, and the primary "Save habit" button is pinned in the bottom
/// safe-area inset so it rides above the keyboard instead of scrolling under it.
struct AddHabitSheet: View {
    @Environment(\.theme) private var theme
    @Environment(\.dismiss) private var dismiss

    let onSave: (Habit) -> Void

    @State private var name = ""
    @State private var icon = Store.sampleIcons[0]
    @State private var frequency: HabitFrequency = .daily
    @State private var remindMe = true
    @State private var reminder = Store.reminder(hour: 8)
    @FocusState private var nameFieldFocused: Bool

    private var canSave: Bool {
        !name.trimmingCharacters(in: .whitespaces).isEmpty
    }

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Habit name", text: $name)
                        .font(theme.font.body)
                        .foregroundStyle(theme.color.text)
                        .focused($nameFieldFocused)
                        .submitLabel(.done)
                        .onSubmit { nameFieldFocused = false }
                } header: {
                    sectionHeader("Name")
                }
                .listRowBackground(theme.color.surface)

                Section {
                    iconPicker
                } header: {
                    sectionHeader("Icon")
                }
                .listRowBackground(theme.color.surface)

                Section {
                    Picker("Frequency", selection: $frequency) {
                        ForEach(HabitFrequency.allCases) { option in
                            Text(option.rawValue).tag(option)
                        }
                    }
                    .pickerStyle(.segmented)
                } header: {
                    sectionHeader("Frequency")
                }
                .listRowBackground(theme.color.surface)

                Section {
                    Toggle("Remind me", isOn: $remindMe)
                        .font(theme.font.body)
                        .foregroundStyle(theme.color.text)
                        .tint(theme.color.accent)
                    if remindMe {
                        DatePicker("Time", selection: $reminder, displayedComponents: .hourAndMinute)
                            .font(theme.font.body)
                            .foregroundStyle(theme.color.text)
                    }
                } header: {
                    sectionHeader("Reminder")
                }
                .listRowBackground(theme.color.surface)
            }
            .scrollContentBackground(.hidden)
            .scrollDismissesKeyboard(.interactively)
            // Pinned in the safe-area inset: stays reachable above the keyboard,
            // and the Form gets matching bottom padding so no row hides behind it.
            .safeAreaInset(edge: .bottom) {
                PrimaryButton(title: "Save habit", systemImage: "checkmark") { save() }
                    .disabled(!canSave)
                    .padding(.horizontal, theme.spacing.lg)
                    .padding(.top, theme.spacing.sm)
                    .padding(.bottom, theme.spacing.sm)
                    .background(theme.color.background)
                    // Same hairline the tab bar uses, so the scroll edge reads as an edge.
                    .overlay(alignment: .top) {
                        theme.color.separator.frame(height: theme.shape.hairline)
                    }
            }
            .pageBackground(theme)
            .defaultFocus($nameFieldFocused, true)
            .navigationTitle("New habit")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                        .foregroundStyle(theme.color.textSecondary)
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") { save() }
                        .font(theme.font.headline)
                        .disabled(!canSave)
                }
            }
        }
        .presentationDetents([.large])
        .presentationCornerRadius(theme.shape.cornerRadius)
    }

    private func sectionHeader(_ title: String) -> some View {
        Text(title)
            .font(theme.font.caption)
            .foregroundStyle(theme.color.textSecondary)
    }

    private var iconPicker: some View {
        LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: theme.spacing.sm), count: 5),
                  spacing: theme.spacing.sm) {
            ForEach(Store.sampleIcons, id: \.self) { symbol in
                let selected = symbol == icon
                Button {
                    icon = symbol
                } label: {
                    Image(systemName: symbol)
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundStyle(selected ? theme.color.surface : theme.color.accent)
                        .frame(maxWidth: .infinity)
                        .frame(height: 48)
                        .background(selected ? theme.color.accent : theme.color.accentSoft)
                        .clipShape(RoundedRectangle(cornerRadius: theme.shape.cornerRadiusSmall, style: .continuous))
                }
                .buttonStyle(.plain)
                .accessibilityLabel(symbol.replacingOccurrences(of: ".", with: " "))
                .accessibilityAddTraits(selected ? .isSelected : [])
            }
        }
        .padding(.vertical, theme.spacing.xs)
    }

    private func save() {
        guard canSave else { return }
        nameFieldFocused = false
        let habit = Habit(
            name: name.trimmingCharacters(in: .whitespaces),
            icon: icon,
            frequency: frequency,
            reminder: remindMe ? reminder : nil
        )
        onSave(habit)
        dismiss()
    }
}

#Preview {
    AddHabitSheet { _ in }
}
