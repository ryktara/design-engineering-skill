import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/inspection.dart';
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

/// Pending-sync queue: each queued write is a labelled row with its own
/// status (queued / sending / failed + reason); manual retry is available
/// even though the queue drains automatically.
class SyncQueueSheet extends ConsumerWidget {
  const SyncQueueSheet({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final sync = ref.watch(syncQueueProvider);
    final online = ref.watch(isOnlineProvider);
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    final failed = sync.failed.length;

    // The line under the title says what is happening right now.
    final String status;
    if (sync.syncing) {
      status = 'Sending ${sync.runSent + 1} of ${sync.runTotal} · ${sync.sending?.label ?? ''}';
    } else if (failed > 0) {
      status = '$failed failed to send · last synced ${OfflineBanner.relative(sync.lastSyncedAt)}';
    } else {
      status = 'Last synced ${OfflineBanner.relative(sync.lastSyncedAt)}${online ? '' : ' · device is offline'}';
    }

    // The button says what it will do, and while sending, what is happening.
    final String buttonLabel;
    final VoidCallback? onPressed;
    if (sync.syncing) {
      buttonLabel = 'Sending ${sync.runSent + 1} of ${sync.runTotal}…';
      onPressed = null;
    } else if (failed > 0) {
      buttonLabel = 'Retry $failed failed';
      onPressed = online ? () => ref.read(syncQueueProvider.notifier).retryFailed() : null;
    } else {
      buttonLabel = 'Retry sync now';
      onPressed = online && sync.pending.isNotEmpty ? () => ref.read(syncQueueProvider.notifier).drain() : null;
    }

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
          // Not a live region: the banner behind the sheet already announces
          // run start, failure and completion once each.
          Text(
            status,
            style: text.bodyLarge?.copyWith(color: failed > 0 && !sync.syncing ? scheme.error : scheme.onSurfaceVariant),
          ),
          if (sync.syncing)
            Padding(
              padding: const EdgeInsets.only(top: FieldSizes.space2),
              child: SyncProgressBar(value: sync.progress, color: scheme.primary, rounded: true),
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
                itemBuilder: (context, i) => _QueueRow(item: sync.pending[i]),
              ),
            ),
          const SizedBox(height: FieldSizes.space4),
          FilledButton.icon(
            onPressed: onPressed,
            icon: Icon(failed > 0 && !sync.syncing ? Icons.refresh : Icons.sync),
            label: Text(buttonLabel),
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

class _QueueRow extends StatelessWidget {
  const _QueueRow({required this.item});
  final PendingSync item;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    final failed = item.status == SyncItemStatus.failed;
    // Second line: the reason when it failed, what is happening when it is
    // going out, otherwise how long it has waited.
    final subtitle = switch (item.status) {
      SyncItemStatus.failed => item.error ?? 'Could not send',
      SyncItemStatus.sending => 'Sending now',
      SyncItemStatus.sent => 'Sent',
      SyncItemStatus.queued => 'Queued ${OfflineBanner.relative(item.queuedAt)}',
    };
    return MergeSemantics(
      child: Semantics(
        // The chip is visual; the word is read here with the label.
        label: '${item.label}. ${item.status.label.toLowerCase()}. $subtitle.',
        child: ExcludeSemantics(
          child: ListTile(
            minTileHeight: FieldSizes.control,
            leading: Icon(
              switch (item.kind) {
                'defect' => Icons.report,
                'photo' => Icons.photo_camera,
                _ => Icons.checklist,
              },
              size: 28,
            ),
            title: Text(item.label),
            subtitle: Text(
              subtitle,
              style: failed ? text.bodyMedium?.copyWith(color: scheme.error, fontWeight: FontWeight.w600) : null,
            ),
            trailing: SyncItemChip(status: item.status),
          ),
        ),
      ),
    );
  }
}
