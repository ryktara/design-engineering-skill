import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Sticky primary action (cta-sticky-bar): sits in the bottom safe area and,
/// when the keyboard is open, rides on top of it so Submit stays reachable
/// (mobile-keyboard-ime). Height is exposed so scroll content can pad for it.
class BottomActionBar extends StatelessWidget {
  const BottomActionBar({super.key, required this.child, this.secondary});

  final Widget child;
  final Widget? secondary;

  static const double barHeight = FieldSizes.control + FieldSizes.space3 * 2;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final insets = MediaQuery.viewInsetsOf(context);
    final padding = MediaQuery.viewPaddingOf(context);
    final reduceMotion = MediaQuery.disableAnimationsOf(context);
    // Bottom padding: keyboard when open, otherwise the home indicator.
    final bottom = insets.bottom > 0 ? insets.bottom : padding.bottom;
    return AnimatedPadding(
      duration: reduceMotion ? Duration.zero : const Duration(milliseconds: 150),
      curve: Curves.easeOut,
      padding: EdgeInsets.only(bottom: bottom),
      child: Material(
        color: scheme.surface,
        child: DecoratedBox(
          decoration: BoxDecoration(border: Border(top: BorderSide(color: scheme.outlineVariant))),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space4, vertical: FieldSizes.space3),
            child: Row(
              children: [
                if (secondary != null) ...[
                  Expanded(child: secondary!),
                  const SizedBox(width: FieldSizes.controlGap),
                ],
                Expanded(flex: 2, child: child),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
