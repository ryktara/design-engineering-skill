import 'package:flutter/material.dart';

import '../models/inspection.dart';
import '../theme/app_theme.dart';

/// Glanceable status: word + icon + colour, never colour alone.
/// Sized to read at arm's length in sunlight (mobile-field-use).
class StatusBadge extends StatelessWidget {
  const StatusBadge({
    super.key,
    required this.status,
    this.compact = false,
    this.onTap,
    this.semanticLabel,
  });

  final ItemStatus status;
  final bool compact;

  /// When set the badge becomes the row's own check control: a 88 x 64 dp
  /// target of its own, above the 56 dp glove floor, with a gap to the
  /// neighbouring row target. Without it the badge stays visual-only and the
  /// surrounding row carries the semantics.
  final VoidCallback? onTap;

  /// Accessible name for the interactive variant. Required when [onTap] is
  /// set, ignored otherwise.
  final String? semanticLabel;

  static String label(ItemStatus s) => switch (s) {
        ItemStatus.pending => 'TO DO',
        ItemStatus.pass => 'PASS',
        ItemStatus.fail => 'FAIL',
        ItemStatus.skipped => 'SKIP',
      };

  static IconData icon(ItemStatus s) => switch (s) {
        ItemStatus.pending => Icons.radio_button_unchecked,
        ItemStatus.pass => Icons.check_circle,
        ItemStatus.fail => Icons.error,
        ItemStatus.skipped => Icons.remove_circle,
      };

  @override
  Widget build(BuildContext context) {
    final sc = Theme.of(context).extension<StatusColors>()!;
    final scheme = Theme.of(context).colorScheme;
    final (bg, fg, border) = switch (status) {
      ItemStatus.pending => (sc.pending, sc.onPending, scheme.outline),
      ItemStatus.pass => (sc.pass, sc.onPass, sc.pass),
      ItemStatus.fail => (sc.fail, sc.onFail, sc.fail),
      ItemStatus.skipped => (sc.skipped, sc.onSkipped, sc.skipped),
    };
    final text = Theme.of(context).textTheme;
    final interactive = onTap != null;
    final face = Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon(status), color: fg, size: 24),
        const SizedBox(height: 2),
        Text(label(status), style: text.labelMedium?.copyWith(color: fg, fontWeight: FontWeight.w700)),
      ],
    );

    if (!interactive) {
      return ExcludeSemantics(
        // The row's merged semantics carry the status word; this is visual.
        child: Container(
          width: compact ? 64 : 80,
          height: FieldSizes.control,
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(FieldSizes.radius),
            border: Border.all(color: border, width: 2),
          ),
          child: face,
        ),
      );
    }

    return Semantics(
      button: true,
      checked: status == ItemStatus.pass,
      label: semanticLabel,
      child: Material(
        color: bg,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(FieldSizes.radius),
          side: BorderSide(color: border, width: 2),
        ),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: onTap,
          child: SizedBox(width: 88, height: 64, child: face),
        ),
      ),
    );
  }
}
