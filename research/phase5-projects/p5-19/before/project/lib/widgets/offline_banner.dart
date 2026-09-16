import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../state/providers.dart';
import '../theme/app_theme.dart';
import 'sync_queue_sheet.dart';

/// Persistent connectivity strip (states-offline-and-sync): shows when
/// offline or when writes are queued. Never a modal; content below stays
/// usable. Announced to screen readers as a live region.
class OfflineBanner extends ConsumerWidget {
  const OfflineBanner({super.key});

  static String relative(DateTime? t) {
    if (t == null) return 'never';
    final d = DateTime.now().difference(t);
    if (d.inMinutes < 1) return 'just now';
    if (d.inMinutes < 60) return '${d.inMinutes} min ago';
    if (d.inHours < 24) return 'at ${DateFormat.Hm().format(t)}';
    return DateFormat.MMMd().add_Hm().format(t);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final online = ref.watch(isOnlineProvider);
    final sync = ref.watch(syncQueueProvider);
    final pending = sync.pending.length;
    if (online && pending == 0) return const SizedBox.shrink();

    final sc = Theme.of(context).extension<StatusColors>()!;
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;
    final bg = online ? scheme.tertiaryContainer : sc.offlineBanner;
    final fg = online ? scheme.onTertiaryContainer : sc.onOfflineBanner;

    final headline = online
        ? (sync.syncing ? 'Syncing $pending…' : '$pending waiting to sync')
        : 'Offline';
    // Short enough to stay on one line at 390 dp / 1.0 scale.
    final detail = online
        ? 'Last synced ${relative(sync.lastSyncedAt)}'
        : '$pending pending · synced ${relative(sync.lastSyncedAt)}';

    return Semantics(
      liveRegion: true,
      container: true,
      label: '$headline. $detail.',
      child: Material(
        color: bg,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space4, vertical: FieldSizes.space2),
          child: Row(
            children: [
              Icon(online ? Icons.cloud_upload : Icons.cloud_off, color: fg, size: 28),
              const SizedBox(width: FieldSizes.space3),
              Expanded(
                child: ExcludeSemantics(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(headline, style: text.titleMedium?.copyWith(color: fg)),
                      Text(detail, style: text.bodyMedium?.copyWith(color: fg)),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: FieldSizes.space3),
              // 56 dp target; label in text, not colour.
              TextButton(
                style: TextButton.styleFrom(
                  foregroundColor: fg,
                  side: BorderSide(color: fg, width: 2),
                  minimumSize: const Size(FieldSizes.control, FieldSizes.control),
                ),
                onPressed: () => showSyncQueueSheet(context),
                child: const Text('Queue'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
