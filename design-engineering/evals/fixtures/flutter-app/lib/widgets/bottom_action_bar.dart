import 'package:flutter/material.dart';

/// Sticky bottom bar that animates above the keyboard (IME) inset.
class BottomActionBar extends StatelessWidget {
  const BottomActionBar({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) {
    final inset = MediaQuery.viewInsetsOf(context).bottom;
    return AnimatedPadding(
      duration: const Duration(milliseconds: 150),
      padding: EdgeInsets.only(bottom: inset),
      child: SafeArea(child: Padding(padding: const EdgeInsets.all(16), child: child)),
    );
  }
}
