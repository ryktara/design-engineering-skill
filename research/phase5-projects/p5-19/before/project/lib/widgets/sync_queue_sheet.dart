import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../state/providers.dart';
import '../theme/app_theme.dart';
import 'offline_banner.dart';

Future<void> showSyncQueueSheet(BuildContext context) {
  return showModalBottomSheet<void>(
    context: context,
    useSafeArea: true,
    showDragHandle: true,
    isScrollControlled: true,
    builder: (_) => const SyncQueueSheet(),
  );
}

/// Pending-sync queue: each queued write is a labelled row; manual retry is
/// available even though the queue drains automatically.
class SyncQueueSheet extends ConsumerWidget {
  const SyncQueueSheet({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final sync = ref.watch(syncQueueProvider);
    final online = ref.watch(isOnlineProvider);
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;

    return Padding(
      padding: const EdgeInsets.fromLTRB(FieldSizes.space4, 0, FieldSizes.space4, FieldSizes.space4),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Semantics(
            header: true,
            child: Text('Sync queue', style: text.headlineSmall),
          ),
          const SizedBox(height: FieldSizes.space1),
          Text(
            'Last synced ${OfflineBanner.relative(sync.lastSyncedAt)}'
            '${online ? '' : ' · device is offline'}',
            style: text.bodyLarge?.copyWith(color: scheme.onSurfaceVariant),
          ),
          const SizedBox(height: FieldSizes.space4),
          if (sync.pending.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: FieldSizes.space6),
              child: Text('Everything is synced.', style: text.bodyLarge),
            )
          else
            Flexible(
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: sync.pending.length,
                separatorBuilder: (_, __) => const Divider(),
                itemBuilder: (context, i) {
                  final p = sync.pending[i];
                  return MergeSemantics(
                    child: ListTile(
                      minTileHeight: FieldSizes.control,
                      leading: Icon(
                        switch (p.kind) {
                          'defect' => Icons.report,
                          'photo' => Icons.photo_camera,
                          _ => Icons.checklist,
                        },
                        size: 28,
                      ),
                      title: Text(p.label),
                      subtitle: Text('Queued ${OfflineBanner.relative(p.queuedAt)}'),
                      trailing: Text('Pending', style: text.labelMedium?.copyWith(color: scheme.onSurfaceVariant)),
                    ),
                  );
                },
              ),
            ),
          const SizedBox(height: FieldSizes.space4),
          FilledButton.icon(
            onPressed: online && sync.pending.isNotEmpty && !sync.syncing
                ? () => ref.read(syncQueueProvider.notifier).drain()
                : null,
            icon: const Icon(Icons.sync),
            label: Text(sync.syncing ? 'Syncing…' : 'Retry sync now'),
          ),
          if (!online)
            Padding(
              padding: const EdgeInsets.only(top: FieldSizes.space2),
              child: Text(
                'Items send automatically when a connection returns. Nothing is lost.',
                style: text.bodyMedium?.copyWith(color: scheme.onSurfaceVariant),
              ),
            ),
        ],
      ),
    );
  }
}
