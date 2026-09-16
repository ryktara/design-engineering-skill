import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../models/inspection.dart';
import '../state/providers.dart';
import '../theme/app_theme.dart';
import 'sync_queue_sheet.dart';

/// Persistent connectivity strip (states-offline-and-sync): shows when
/// offline, when writes are queued, while they are being sent, when one
/// failed, and for a few seconds after everything went. Never a modal;
/// content below stays usable. Announced to screen readers as a live region.
///
/// Every state says what is happening in words: which item is going out,
/// how many of how many, what failed and why, and what to do next.
/// While offline the strip carries a manual **Retry** as well: signal on a
/// site comes back in patches, the connectivity stream can lag behind it, and
/// an inspector who has walked back to the truck needs a way to say "try now"
/// instead of waiting. [onRetry] lets the host screen reload its own data in
/// the same tap (the report list re-fetches); the queue is always flushed.
class OfflineBanner extends ConsumerWidget {
  const OfflineBanner({super.key, this.onRetry});

  /// Extra work for the manual retry: the screen's own reload. Runs after the
  /// connectivity re-check; may complete before the queue has drained.
  final Future<void> Function()? onRetry;

  static String relative(DateTime? t) {
    if (t == null) return 'never';
    final d = DateTime.now().difference(t);
    if (d.inMinutes < 1) return 'just now';
    if (d.inMinutes < 60) return '${d.inMinutes} min ago';
    if (d.inHours < 24) return 'at ${DateFormat.Hm().format(t)}';
    return DateFormat.MMMd().add_Hm().format(t);
  }

  /// Same fact, fewer characters: the offline strip also carries the chevron
  /// into the queue, and the detail line has to stay on one line at 390 dp.
  static String relativeShort(DateTime? t) {
    if (t == null) return 'never';
    final d = DateTime.now().difference(t);
    if (d.inMinutes < 1) return 'just now';
    if (d.inMinutes < 60) return '${d.inMinutes}m ago';
    if (d.inHours < 24) return '${d.inHours}h ago';
    return DateFormat.MMMd().format(t);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final online = ref.watch(isOnlineProvider);
    final sync = ref.watch(syncQueueProvider);
    final pending = sync.pending.length;
    final justDone = sync.completedAt != null && pending == 0;
    if (online && pending == 0 && !justDone) return const SizedBox.shrink();

    final sc = Theme.of(context).extension<StatusColors>()!;
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;

    // One of five states; each has its own icon, words and colours so the
    // strip is glanceable at arm's length (mobile-field-use).
    final Color bg;
    final Color fg;
    final IconData icon;
    final String headline;
    final String detail;
    // What the screen reader hears. Kept stable while a run is in progress
    // so it is announced once, not on every item (a11y-live-status).
    final String announcement;
    Widget? action;
    // Set in the states where the strip's own button is not the queue, so the
    // queue stays one tap away from the text region (which is 56 dp tall).
    VoidCallback? bodyTap;

    // Manual retry: re-check the radio first (the stream can be stale after
    // walking back into coverage), then flush the queue and reload the host
    // screen. If there is still no signal, say so and keep everything queued.
    Future<void> retryNow() async {
      final back = await ref.read(syncQueueProvider.notifier).retryNow();
      if (back && onRetry != null) await onRetry!();
      if (!back && context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text('Still no signal. Everything stays saved on the device.'),
        ));
      }
    }

    if (!online) {
      bg = sc.offlineBanner;
      fg = sc.onOfflineBanner;
      icon = Icons.cloud_off;
      headline = 'Offline';
      // Short enough to stay on one line at 390 dp / 1.0 scale.
      detail = pending == 0
          ? 'Nothing waiting · synced ${relativeShort(sync.lastSyncedAt)}'
          : '$pending pending · synced ${relativeShort(sync.lastSyncedAt)}';
      announcement = '$headline. $pending pending, last synced ${relative(sync.lastSyncedAt)}. '
          'Retry, or tap for the queue.';
      action = _BannerButton(fg: fg, label: 'Retry', onPressed: retryNow);
      bodyTap = () => showSyncQueueSheet(context);
    } else if (sync.syncing) {
      bg = scheme.tertiaryContainer;
      fg = scheme.onTertiaryContainer;
      icon = Icons.cloud_upload;
      headline = 'Sending ${sync.runSent + 1} of ${sync.runTotal}';
      detail = sync.sending?.label ?? 'Waiting for the server';
      announcement = 'Sending ${sync.runTotal} ${sync.runTotal == 1 ? 'item' : 'items'}.';
      action = _BannerButton(fg: fg, label: 'Queue', onPressed: () => showSyncQueueSheet(context));
    } else if (sync.hasFailures) {
      final failed = sync.failed;
      bg = scheme.errorContainer;
      fg = scheme.onErrorContainer;
      icon = Icons.error;
      headline = '${failed.length} failed to send';
      detail = '${failed.first.label} · ${failed.first.error ?? 'No reason given'}';
      announcement = '$headline. $detail. Retry available.';
      action = _BannerButton(fg: fg, label: 'Retry', onPressed: () => ref.read(syncQueueProvider.notifier).retryFailed());
    } else if (justDone) {
      bg = sc.pass;
      fg = sc.onPass;
      icon = Icons.cloud_done;
      headline = 'All sent';
      detail = 'Synced ${relative(sync.lastSyncedAt)}';
      announcement = '$headline. $detail.';
    } else {
      bg = scheme.tertiaryContainer;
      fg = scheme.onTertiaryContainer;
      icon = Icons.cloud_upload;
      headline = '$pending waiting to send';
      detail = 'Last synced ${relative(sync.lastSyncedAt)}';
      announcement = '$headline. $detail.';
      action = _BannerButton(fg: fg, label: 'Queue', onPressed: () => showSyncQueueSheet(context));
    }

    return Semantics(
      liveRegion: true,
      container: true,
      label: announcement,
      child: Material(
        color: bg,
        child: Stack(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space4, vertical: FieldSizes.space2),
              // The row keeps the button's 56 dp height even when there is no
              // button, so the content below does not jump between states.
              child: ConstrainedBox(
                constraints: const BoxConstraints(minHeight: FieldSizes.control),
                child: Row(
                  children: [
                    Icon(icon, color: fg, size: 28),
                    const SizedBox(width: FieldSizes.space3),
                    Expanded(
                      child: _BannerText(
                        headline: headline,
                        detail: detail,
                        fg: fg,
                        onTap: bodyTap,
                      ),
                    ),
                    if (action != null) ...[const SizedBox(width: FieldSizes.space3), action],
                  ],
                ),
              ),
            ),
            // Run progress sits on the strip's bottom edge (the app-bar
            // progress idiom) so the strip's height is the same in every
            // state and the content below never jumps.
            if (sync.syncing)
              Positioned(
                left: 0,
                right: 0,
                bottom: 0,
                child: SyncProgressBar(value: sync.progress, color: fg),
              ),
          ],
        ),
      ),
    );
  }
}

/// Headline + detail of the strip. When [onTap] is given the region is its own
/// 56 dp control that opens the sync queue, so the strip can spend its button
/// on Retry without losing the way into the queue.
class _BannerText extends StatelessWidget {
  const _BannerText({required this.headline, required this.detail, required this.fg, this.onTap});

  final String headline;
  final String detail;
  final Color fg;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final column = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(headline, style: text.titleMedium?.copyWith(color: fg)),
        Text(
          detail,
          style: text.bodyMedium?.copyWith(color: fg),
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
      ],
    );
    if (onTap == null) return ExcludeSemantics(child: column);
    return Semantics(
      button: true,
      label: 'Sync queue',
      hint: 'Shows queued items',
      child: InkWell(
        onTap: onTap,
        child: ConstrainedBox(
          constraints: const BoxConstraints(minHeight: FieldSizes.control),
          child: ExcludeSemantics(
            // Same chevron the settings "Sync queue" row uses, so the text
            // region reads as a control and not as decoration.
            child: Row(
              children: [
                Flexible(child: column),
                Icon(Icons.chevron_right, color: fg, size: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// 56 dp target; label in text, not colour.
class _BannerButton extends StatelessWidget {
  const _BannerButton({required this.fg, required this.label, required this.onPressed});
  final Color fg;
  final String label;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return TextButton(
      style: TextButton.styleFrom(
        foregroundColor: fg,
        side: BorderSide(color: fg, width: 2),
        minimumSize: const Size(FieldSizes.control, FieldSizes.control),
      ),
      onPressed: onPressed,
      child: Text(label),
    );
  }
}

/// Determinate progress for a sync run. Visual only: the words next to it
/// ("Sending 2 of 3") carry the meaning, so it is excluded from semantics.
/// Thick enough to read in glare; no animation beyond the value change.
class SyncProgressBar extends StatelessWidget {
  const SyncProgressBar({super.key, required this.value, required this.color, this.rounded = false});
  final double value;
  final Color color;

  /// Rounded ends when the bar stands alone (queue sheet); square when it
  /// runs along the banner's bottom edge.
  final bool rounded;

  @override
  Widget build(BuildContext context) {
    return ExcludeSemantics(
      child: LinearProgressIndicator(
        value: value,
        minHeight: 6,
        color: color,
        backgroundColor: color.withOpacity(0.3),
        borderRadius: BorderRadius.circular(rounded ? 3 : 0),
      ),
    );
  }
}

/// Status of one queued item as word + icon + colour (StatusBadge idiom).
class SyncItemChip extends StatelessWidget {
  const SyncItemChip({super.key, required this.status});
  final SyncItemStatus status;

  static IconData icon(SyncItemStatus s) => switch (s) {
        SyncItemStatus.queued => Icons.schedule,
        SyncItemStatus.sending => Icons.cloud_upload,
        SyncItemStatus.sent => Icons.check_circle,
        SyncItemStatus.failed => Icons.error,
      };

  @override
  Widget build(BuildContext context) {
    final sc = Theme.of(context).extension<StatusColors>()!;
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;
    final (bg, fg, border) = switch (status) {
      SyncItemStatus.queued => (sc.pending, sc.onPending, scheme.outline),
      SyncItemStatus.sending => (scheme.primaryContainer, scheme.onPrimaryContainer, scheme.primary),
      SyncItemStatus.sent => (sc.pass, sc.onPass, sc.pass),
      SyncItemStatus.failed => (sc.fail, sc.onFail, sc.fail),
    };
    return ExcludeSemantics(
      // The row's merged semantics carry the status word; this is visual.
      child: Container(
        constraints: const BoxConstraints(minWidth: 96, minHeight: 40),
        padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space3),
        decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(FieldSizes.radius),
          border: Border.all(color: border, width: 2),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon(status), color: fg, size: 20),
            const SizedBox(width: FieldSizes.space1),
            Text(status.label, style: text.labelMedium?.copyWith(color: fg, fontWeight: FontWeight.w700)),
          ],
        ),
      ),
    );
  }
}
