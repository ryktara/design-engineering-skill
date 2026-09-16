import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../state/providers.dart';
import '../state/settings.dart';
import '../theme/app_theme.dart';
import '../widgets/offline_banner.dart';
import '../widgets/sync_queue_sheet.dart';

/// Settings: grouped rows with the current value visible on every row,
/// toggles with immediate effect, a bottom-sheet picker for the enum with four
/// options and two toggle buttons for units (comp-settings-screen). Same
/// shell as the other screens: 72 dp app bar with back, offline strip, flat
/// outlined tiles, 56 dp controls with 8 dp between adjacent targets.
class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final sync = ref.watch(syncQueueProvider);
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          tooltip: 'Back',
          onPressed: () => context.canPop() ? context.pop() : context.go('/inspection/insp-2091'),
        ),
        title: const Text('Settings'),
      ),
      body: Column(
        children: [
          const OfflineBanner(),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(FieldSizes.space4, FieldSizes.space4, FieldSizes.space4, FieldSizes.space6),
              children: [
                // Save behaviour stated up front (comp-settings-screen).
                Text('Changes apply immediately.', style: text.bodyLarge?.copyWith(color: scheme.onSurfaceVariant)),
                const SizedBox(height: FieldSizes.space4),

                const _GroupHeader('Sync'),
                _SettingTile(
                  icon: Icons.sync,
                  title: 'Sync frequency',
                  value: settings.syncFrequency.label,
                  hint: 'Opens a list of four options',
                  onTap: () => _pickFrequency(context, ref, settings.syncFrequency),
                ),
                const SizedBox(height: FieldSizes.space2),
                _SettingTile(
                  icon: sync.pending.isEmpty ? Icons.cloud_done : Icons.cloud_upload,
                  title: 'Sync queue',
                  value: sync.pending.isEmpty
                      ? 'Everything synced · ${OfflineBanner.relative(sync.lastSyncedAt)}'
                      : '${sync.pending.length} pending · synced ${OfflineBanner.relative(sync.lastSyncedAt)}',
                  hint: 'Shows queued items and Retry sync',
                  onTap: () => showSyncQueueSheet(context),
                ),
                const SizedBox(height: FieldSizes.space6),

                const _GroupHeader('Units'),
                _Tile(
                  child: Padding(
                    padding: const EdgeInsets.all(FieldSizes.space3),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text('Measurements', style: text.titleMedium),
                        Text(
                          '${settings.units.label}: ${settings.units.detail}',
                          style: text.bodyMedium?.copyWith(color: scheme.onSurfaceVariant),
                        ),
                        const SizedBox(height: FieldSizes.space3),
                        // Two separate 56 dp toggles with a 12 dp gap, the same
                        // idiom as the severity chooser, not a SegmentedButton:
                        // adjacent segments have no gap for gloved fingers.
                        Row(
                          children: [
                            for (final (i, u) in Units.values.indexed) ...[
                              if (i > 0) const SizedBox(width: FieldSizes.controlGap),
                              Expanded(
                                child: Semantics(
                                  inMutuallyExclusiveGroup: true,
                                  selected: settings.units == u,
                                  label: '${u.label} units',
                                  child: settings.units == u
                                      ? FilledButton.icon(
                                          onPressed: () => ref.read(settingsProvider.notifier).setUnits(u),
                                          icon: const Icon(Icons.check, size: 24),
                                          label: Text(u.label),
                                        )
                                      : OutlinedButton(
                                          onPressed: () => ref.read(settingsProvider.notifier).setUnits(u),
                                          child: Text(u.label),
                                        ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: FieldSizes.space6),

                const _GroupHeader('Display'),
                _Tile(
                  child: MergeSemantics(
                    child: SwitchListTile.adaptive(
                      minTileHeight: FieldSizes.control + FieldSizes.space4,
                      secondary: const Icon(Icons.contrast, size: 28),
                      title: const Text('High-contrast mode'),
                      subtitle: Text(settings.highContrast
                          ? 'On: stronger borders and darker secondary text'
                          : 'Off: standard sunlight theme'),
                      value: settings.highContrast,
                      onChanged: (v) => ref.read(settingsProvider.notifier).setHighContrast(v),
                    ),
                  ),
                ),
                const SizedBox(height: FieldSizes.space2),
                _Tile(
                  child: ListTile(
                    minTileHeight: FieldSizes.control,
                    leading: const Icon(Icons.text_fields, size: 28),
                    title: const Text('Text size'),
                    subtitle: const Text('Follows the phone setting, up to 160%'),
                    enabled: false,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _pickFrequency(BuildContext context, WidgetRef ref, SyncFrequency current) async {
    final choice = await showModalBottomSheet<SyncFrequency>(
      context: context,
      useSafeArea: true,
      showDragHandle: true,
      builder: (ctx) {
        final text = Theme.of(ctx).textTheme;
        final scheme = Theme.of(ctx).colorScheme;
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(FieldSizes.space4, 0, FieldSizes.space4, FieldSizes.space3),
                child: Semantics(header: true, child: Text('Sync frequency', style: text.headlineSmall)),
              ),
              for (final (i, f) in SyncFrequency.values.indexed) ...[
                if (i > 0) const SizedBox(height: FieldSizes.space2),
                Semantics(
                  inMutuallyExclusiveGroup: true,
                  selected: f == current,
                  child: ListTile(
                    minTileHeight: FieldSizes.control + FieldSizes.space2,
                    leading: Icon(
                      f == current ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                      size: 28,
                      color: f == current ? scheme.primary : scheme.onSurfaceVariant,
                    ),
                    title: Text(f.label),
                    subtitle: Text(f.detail),
                    selected: f == current,
                    onTap: () => Navigator.pop(ctx, f),
                  ),
                ),
              ],
              const SizedBox(height: FieldSizes.space2),
            ],
          ),
        );
      },
    );
    if (choice == null) return;
    ref.read(settingsProvider.notifier).setSyncFrequency(choice);
  }
}

class _GroupHeader extends StatelessWidget {
  const _GroupHeader(this.label);
  final String label;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.only(bottom: FieldSizes.space2),
      child: Semantics(
        header: true,
        child: Text(label.toUpperCase(), style: text.labelMedium?.copyWith(color: scheme.onSurfaceVariant)),
      ),
    );
  }
}

/// Flat outlined tile, the same container as a checklist row.
class _Tile extends StatelessWidget {
  const _Tile({required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Material(
      color: scheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(FieldSizes.radius),
        side: BorderSide(color: scheme.outlineVariant),
      ),
      clipBehavior: Clip.antiAlias,
      child: child,
    );
  }
}

/// Row that opens a picker or sheet: label, current value, chevron.
class _SettingTile extends StatelessWidget {
  const _SettingTile({required this.icon, required this.title, required this.value, required this.onTap, this.hint});
  final IconData icon;
  final String title;
  final String value;
  final String? hint;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return _Tile(
      child: MergeSemantics(
        child: Semantics(
          button: true,
          hint: hint,
          child: ListTile(
            minTileHeight: 72,
            leading: Icon(icon, size: 28),
            title: Text(title),
            subtitle: Text(value),
            trailing: Icon(Icons.chevron_right, color: scheme.onSurfaceVariant, size: 28),
            onTap: onTap,
          ),
        ),
      ),
    );
  }
}
