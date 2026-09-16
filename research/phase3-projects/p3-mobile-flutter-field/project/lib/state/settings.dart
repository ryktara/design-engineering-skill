import 'package:flutter_riverpod/flutter_riverpod.dart';

/// User preferences. Every change applies immediately (no Save button); the
/// settings screen says so. Values are held in memory here; persistence goes
/// through the same notifier (a `shared_preferences` write in `_persist`)
/// when that dependency is added, so the UI does not change.
enum SyncFrequency {
  whenConnected('As soon as connected', 'Sends queued items the moment a connection returns'),
  every15('Every 15 minutes', 'Batches uploads to save battery on weak signal'),
  hourly('Every hour', 'For long rural routes with little coverage'),
  manual('Manual only', 'Nothing is sent until you tap Retry sync');

  const SyncFrequency(this.label, this.detail);
  final String label;
  final String detail;
}

enum Units {
  metric('Metric', 'metres, °C'),
  imperial('Imperial', 'feet, °F');

  const Units(this.label, this.detail);
  final String label;
  final String detail;
}

class AppSettings {
  const AppSettings({
    this.syncFrequency = SyncFrequency.whenConnected,
    this.units = Units.metric,
    this.highContrast = false,
  });

  final SyncFrequency syncFrequency;
  final Units units;

  /// Stronger borders and secondary text on top of the sunlight theme; also
  /// followed automatically when the OS "increase contrast" setting is on
  /// (MaterialApp.highContrastTheme).
  final bool highContrast;

  AppSettings copyWith({SyncFrequency? syncFrequency, Units? units, bool? highContrast}) => AppSettings(
        syncFrequency: syncFrequency ?? this.syncFrequency,
        units: units ?? this.units,
        highContrast: highContrast ?? this.highContrast,
      );
}

class SettingsNotifier extends Notifier<AppSettings> {
  @override
  AppSettings build() => const AppSettings();

  void setSyncFrequency(SyncFrequency v) => _update(state.copyWith(syncFrequency: v));
  void setUnits(Units v) => _update(state.copyWith(units: v));
  void setHighContrast(bool v) => _update(state.copyWith(highContrast: v));

  void _update(AppSettings next) {
    state = next;
    _persist(next);
  }

  // Persistence hook: write the three values to local storage here.
  void _persist(AppSettings s) {}
}

final settingsProvider = NotifierProvider<SettingsNotifier, AppSettings>(SettingsNotifier.new);
