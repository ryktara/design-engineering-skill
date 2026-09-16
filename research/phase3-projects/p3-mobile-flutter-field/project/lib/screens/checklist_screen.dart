import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../models/inspection.dart';
import '../state/providers.dart';
import '../theme/app_theme.dart';
import '../widgets/bottom_action_bar.dart';
import '../widgets/offline_banner.dart';
import '../widgets/state_views.dart';
import '../widgets/status_badge.dart';

/// Inspection checklist. One focal element: the large "checked / total"
/// count. Each row is a single 72 dp target that opens a bottom sheet with
/// three big buttons (Pass / Fail / Skip). No swipe-only actions (gloves).
class ChecklistScreen extends ConsumerWidget {
  const ChecklistScreen({super.key, required this.inspectionId});

  final String inspectionId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(inspectionProvider(inspectionId));

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          tooltip: 'Back to work orders',
          onPressed: () => context.canPop() ? context.pop() : null,
        ),
        title: Text(async.valueOrNull?.assetTag ?? 'Inspection'),
        actions: [
          IconButton(
            icon: const Icon(Icons.more_vert),
            tooltip: 'More actions',
            onPressed: () => _showMore(context),
          ),
        ],
      ),
      body: Column(
        children: [
          // Retry on the strip reloads the list too, so one tap covers both
          // "send what is queued" and "fetch what I could not load".
          OfflineBanner(
            onRetry: () => ref.refresh(inspectionProvider(inspectionId).future),
          ),
          Expanded(
            child: async.when(
              skipLoadingOnRefresh: false,
              loading: () => const LoadingView(),
              error: (e, _) => ErrorView(
                message: e.toString(),
                onRetry: () => ref.invalidate(inspectionProvider(inspectionId)),
                onOpenCached: () => context.go('/inspection/insp-2091'),
              ),
              data: (insp) => insp.items.isEmpty
                  ? EmptyView(
                      title: 'No checklist items',
                      message: 'This ${insp.assetType.toLowerCase()} has no inspection template assigned. '
                          'Assign one from the work order, or report a defect directly.',
                      actionLabel: 'Report a defect',
                      onAction: () => context.go('/inspection/${insp.id}/defect/adhoc'),
                    )
                  : _ChecklistBody(inspection: insp, inspectionId: inspectionId),
            ),
          ),
        ],
      ),
      bottomNavigationBar: async.maybeWhen(
        data: (insp) => insp.items.isEmpty
            ? null
            : BottomActionBar(
                child: FilledButton.icon(
                  onPressed: insp.complete ? () => _complete(context, ref, insp) : null,
                  icon: const Icon(Icons.task_alt),
                  label: Text(insp.complete
                      ? 'Complete inspection'
                      : '${insp.items.length - insp.done} left to check'),
                ),
              ),
        orElse: () => null,
      ),
    );
  }

  void _showMore(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      useSafeArea: true,
      showDragHandle: true,
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              minTileHeight: FieldSizes.control,
              leading: const Icon(Icons.map, size: 28),
              title: const Text('Open in maps'),
              onTap: () => Navigator.pop(ctx),
            ),
            ListTile(
              minTileHeight: FieldSizes.control,
              leading: const Icon(Icons.history, size: 28),
              title: const Text('Previous inspections'),
              onTap: () => Navigator.pop(ctx),
            ),
            ListTile(
              minTileHeight: FieldSizes.control,
              leading: const Icon(Icons.settings, size: 28),
              title: const Text('Settings'),
              onTap: () {
                Navigator.pop(ctx);
                context.push('/settings');
              },
            ),
            const SizedBox(height: FieldSizes.space2),
          ],
        ),
      ),
    );
  }

  Future<void> _complete(BuildContext context, WidgetRef ref, Inspection insp) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Complete inspection?'),
        content: Text('${insp.done} items recorded, ${insp.failed} failed. '
            'This queues the report for sync; you can still edit until it is sent.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Not yet')),
          FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Complete')),
        ],
      ),
    );
    if (ok == true && context.mounted) {
      ref.read(syncQueueProvider.notifier).enqueue(PendingSync(
            id: '${insp.id}-complete',
            kind: 'item',
            label: 'Inspection ${insp.assetTag} completed',
            queuedAt: DateTime.now(),
          ));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Inspection queued for sync')),
      );
    }
  }
}

class _ChecklistBody extends ConsumerWidget {
  const _ChecklistBody({required this.inspection, required this.inspectionId});

  final Inspection inspection;
  final String inspectionId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    final sc = Theme.of(context).extension<StatusColors>()!;

    return RefreshIndicator(
      onRefresh: () => ref.refresh(inspectionProvider(inspectionId).future),
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(FieldSizes.space4, FieldSizes.space4, FieldSizes.space4, FieldSizes.space3),
              child: MergeSemantics(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(inspection.assetType, style: text.titleMedium?.copyWith(color: scheme.onSurfaceVariant)),
                    Text(inspection.address, style: text.bodyLarge),
                    const SizedBox(height: FieldSizes.space3),
                    // Focal point: large numerals (mobile-field-use).
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.baseline,
                      textBaseline: TextBaseline.alphabetic,
                      children: [
                        Text(
                          '${inspection.done}',
                          style: text.displaySmall?.copyWith(fontFeatures: const [FontFeature.tabularFigures()]),
                        ),
                        Text(' / ${inspection.items.length} checked', style: text.titleLarge),
                      ],
                    ),
                    if (inspection.failed > 0)
                      Padding(
                        padding: const EdgeInsets.only(top: FieldSizes.space1),
                        child: Row(
                          children: [
                            Icon(Icons.error, color: sc.fail, size: 24),
                            const SizedBox(width: FieldSizes.space2),
                            Text(
                              '${inspection.failed} failed',
                              style: text.titleMedium?.copyWith(color: sc.fail, fontWeight: FontWeight.w700),
                            ),
                          ],
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
          // Rows are flat tiles with an 8 dp gap, not divider-separated list
          // rows: adjacent 72 dp targets need >= 8 dp between them for gloves
          // (mobile-field-use). First render used dividers and measured 1 px.
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space4),
            sliver: SliverList.separated(
            itemCount: inspection.items.length,
            separatorBuilder: (_, __) => const SizedBox(height: FieldSizes.space2),
            itemBuilder: (context, i) => _ItemRow(
              key: ValueKey(inspection.items[i].id),
              item: inspection.items[i],
              index: i,
              total: inspection.items.length,
              onTap: () => _pickStatus(context, ref, inspection.items[i]),
              onToggleCheck: () => _toggleCheck(context, ref, inspection.items[i]),
            ),
            ),
          ),
          const SliverToBoxAdapter(child: SizedBox(height: FieldSizes.space4)),
        ],
      ),
    );
  }

  /// The per-row check control. Pending -> pass and pass -> pending in one
  /// tap (the common case, and its own undo); fail and skip keep their
  /// reason, so the control opens the Pass / Fail / Skip sheet instead.
  void _toggleCheck(BuildContext context, WidgetRef ref, ChecklistItem item) {
    switch (item.status) {
      case ItemStatus.pending:
        ref.read(inspectionProvider(inspectionId).notifier).setStatus(item.id, ItemStatus.pass);
      case ItemStatus.pass:
        ref.read(inspectionProvider(inspectionId).notifier).setStatus(item.id, ItemStatus.pending);
      case ItemStatus.fail:
      case ItemStatus.skipped:
        _pickStatus(context, ref, item);
    }
  }

  Future<void> _pickStatus(BuildContext context, WidgetRef ref, ChecklistItem item) async {
    final sc = Theme.of(context).extension<StatusColors>()!;
    final choice = await showModalBottomSheet<ItemStatus>(
      context: context,
      useSafeArea: true,
      showDragHandle: true,
      builder: (ctx) {
        final text = Theme.of(ctx).textTheme;
        return Padding(
          padding: const EdgeInsets.fromLTRB(FieldSizes.space4, 0, FieldSizes.space4, FieldSizes.space4),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Semantics(header: true, child: Text(item.title, style: text.headlineSmall)),
              const SizedBox(height: FieldSizes.space1),
              Text(item.detail, style: text.bodyLarge),
              const SizedBox(height: FieldSizes.space6),
              // Three 64 dp buttons with 12 dp gaps: word + icon + colour.
              _BigChoice(
                label: 'Pass',
                icon: Icons.check_circle,
                color: sc.pass,
                onColor: sc.onPass,
                onTap: () => Navigator.pop(ctx, ItemStatus.pass),
              ),
              const SizedBox(height: FieldSizes.controlGap),
              _BigChoice(
                label: 'Fail — report defect',
                icon: Icons.error,
                color: sc.fail,
                onColor: sc.onFail,
                onTap: () => Navigator.pop(ctx, ItemStatus.fail),
              ),
              const SizedBox(height: FieldSizes.controlGap),
              _BigChoice(
                label: 'Skip (not accessible)',
                icon: Icons.remove_circle,
                color: sc.skipped,
                onColor: sc.onSkipped,
                onTap: () => Navigator.pop(ctx, ItemStatus.skipped),
                outlined: true,
              ),
            ],
          ),
        );
      },
    );
    if (choice == null || !context.mounted) return;
    if (choice == ItemStatus.fail) {
      context.go('/inspection/$inspectionId/defect/${item.id}');
      return;
    }
    ref.read(inspectionProvider(inspectionId).notifier).setStatus(item.id, choice);
  }
}

class _BigChoice extends StatelessWidget {
  const _BigChoice({
    required this.label,
    required this.icon,
    required this.color,
    required this.onColor,
    required this.onTap,
    this.outlined = false,
  });

  final String label;
  final IconData icon;
  final Color color;
  final Color onColor;
  final VoidCallback onTap;
  final bool outlined;

  @override
  Widget build(BuildContext context) {
    final style = outlined
        ? OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(64), side: BorderSide(color: color, width: 2))
        : FilledButton.styleFrom(minimumSize: const Size.fromHeight(64), backgroundColor: color, foregroundColor: onColor);
    final child = Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [Icon(icon, size: 28), const SizedBox(width: FieldSizes.space3), Text(label)],
    );
    return outlined
        ? OutlinedButton(style: style, onPressed: onTap, child: child)
        : FilledButton(style: style, onPressed: onTap, child: child);
  }
}

class _ItemRow extends StatelessWidget {
  const _ItemRow({
    super.key,
    required this.item,
    required this.index,
    required this.total,
    required this.onTap,
    required this.onToggleCheck,
  });

  final ChecklistItem item;
  final int index;
  final int total;
  final VoidCallback onTap;
  final VoidCallback onToggleCheck;

  String get _checkLabel => switch (item.status) {
        ItemStatus.pending => 'Mark ${item.title} passed',
        ItemStatus.pass => '${item.title} passed. Undo',
        ItemStatus.fail => '${item.title} failed. Change status',
        ItemStatus.skipped => '${item.title} skipped. Change status',
      };

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    // No MergeSemantics here: merging would swallow the check control, which
    // is the one target this row is about. The title/detail column is already
    // ExcludeSemantics, so the row still announces as a single button.
    return Semantics(
      button: true,
      label: '${item.title}. ${StatusBadge.label(item.status)}. Item ${index + 1} of $total.',
      hint: 'Opens Pass, Fail or Skip',
      child: Material(
        color: scheme.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(FieldSizes.radius),
          side: BorderSide(color: scheme.outlineVariant),
        ),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: onTap,
          child: ConstrainedBox(
            constraints: const BoxConstraints(minHeight: 72),
            child: Padding(
              // 8 dp not 12: the check control is 8 dp wider than the old
              // badge, and the title must not lose a line to it.
              padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space2, vertical: FieldSizes.space2),
              child: Row(
                children: [
                  // The check control: its own 88 x 64 dp target inside the
                  // row target, so a gloved tap on the status lands on a
                  // control instead of only opening the sheet.
                  StatusBadge(
                    status: item.status,
                    onTap: onToggleCheck,
                    semanticLabel: _checkLabel,
                  ),
                  const SizedBox(width: FieldSizes.space4),
                  Expanded(
                    child: ExcludeSemantics(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(item.title, style: text.titleMedium),
                          const SizedBox(height: 2),
                          Text(item.detail, style: text.bodyMedium?.copyWith(color: scheme.onSurfaceVariant)),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: FieldSizes.space2),
                  Icon(Icons.chevron_right, color: scheme.onSurfaceVariant, size: 28),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
