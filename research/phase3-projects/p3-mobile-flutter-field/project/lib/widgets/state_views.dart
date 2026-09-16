import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Loading / empty / error occupy the content region with one action each
/// (layout-states-empty-loading-error). Skeleton rows are at final size so
/// the layout does not jump when data arrives.
class LoadingView extends StatelessWidget {
  const LoadingView({super.key, this.rows = 5});
  final int rows;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Semantics(
      label: 'Loading inspection',
      liveRegion: true,
      child: ExcludeSemantics(
        child: ListView.separated(
          padding: const EdgeInsets.all(FieldSizes.space4),
          itemCount: rows + 1,
          separatorBuilder: (_, __) => const SizedBox(height: FieldSizes.space2),
          // Item 0 mirrors the header block (type, address, big count) so the
          // layout does not jump when data arrives.
          itemBuilder: (_, i) => i == 0
              ? Padding(
                  padding: const EdgeInsets.only(bottom: FieldSizes.space3),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _Bone(width: 200, height: 20, color: scheme.surfaceContainerHighest),
                      const SizedBox(height: FieldSizes.space2),
                      _Bone(width: 260, height: 20, color: scheme.surfaceContainerHighest),
                      const SizedBox(height: FieldSizes.space4),
                      _Bone(width: 180, height: 40, color: scheme.surfaceContainerHighest),
                    ],
                  ),
                )
              : Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(FieldSizes.radius),
              border: Border.all(color: scheme.outlineVariant),
            ),
            padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space3, vertical: FieldSizes.space2),
            child: Row(
              children: [
                _Bone(width: 80, height: FieldSizes.control, color: scheme.surfaceContainerHighest),
                const SizedBox(width: FieldSizes.space4),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _Bone(width: 180, height: 20, color: scheme.surfaceContainerHighest),
                      const SizedBox(height: FieldSizes.space2),
                      _Bone(width: double.infinity, height: 16, color: scheme.surfaceContainerHighest),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Bone extends StatelessWidget {
  const _Bone({required this.width, required this.height, required this.color});
  final double width;
  final double height;
  final Color color;
  @override
  Widget build(BuildContext context) => Container(
        width: width,
        height: height,
        decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(4)),
      );
}

class EmptyView extends StatelessWidget {
  const EmptyView({
    super.key,
    required this.title,
    required this.message,
    required this.actionLabel,
    required this.onAction,
  });

  final String title;
  final String message;
  final String actionLabel;
  final VoidCallback onAction;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(FieldSizes.space6),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Icon(Icons.checklist_rtl, size: 56, color: scheme.onSurfaceVariant),
            const SizedBox(height: FieldSizes.space4),
            Semantics(header: true, child: Text(title, style: text.headlineSmall, textAlign: TextAlign.center)),
            const SizedBox(height: FieldSizes.space2),
            Text(message, style: text.bodyLarge?.copyWith(color: scheme.onSurfaceVariant), textAlign: TextAlign.center),
            const SizedBox(height: FieldSizes.space6),
            FilledButton(onPressed: onAction, child: Text(actionLabel)),
          ],
        ),
      ),
    );
  }
}

class ErrorView extends StatelessWidget {
  const ErrorView({super.key, required this.message, required this.onRetry, this.onOpenCached});

  final String message;
  final VoidCallback onRetry;
  final VoidCallback? onOpenCached;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(FieldSizes.space6),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Icon(Icons.error, size: 56, color: scheme.error),
            const SizedBox(height: FieldSizes.space4),
            Semantics(
              header: true,
              liveRegion: true,
              child: Text('Could not load this inspection', style: text.headlineSmall, textAlign: TextAlign.center),
            ),
            const SizedBox(height: FieldSizes.space2),
            Text(message, style: text.bodyLarge?.copyWith(color: scheme.onSurfaceVariant), textAlign: TextAlign.center),
            const SizedBox(height: FieldSizes.space6),
            FilledButton.icon(onPressed: onRetry, icon: const Icon(Icons.refresh), label: const Text('Try again')),
            if (onOpenCached != null) ...[
              const SizedBox(height: FieldSizes.space3),
              OutlinedButton(onPressed: onOpenCached, child: const Text('Open last saved copy')),
            ],
          ],
        ),
      ),
    );
  }
}
