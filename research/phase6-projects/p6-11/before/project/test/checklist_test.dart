import 'package:field_inspect/models/inspection.dart';
import 'package:field_inspect/screens/checklist_screen.dart';
import 'package:field_inspect/state/providers.dart';
import 'package:field_inspect/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

// Not executed in this environment (no Flutter SDK). Kept as the intended
// verification: semantics guidelines and a 56 dp target floor.
void main() {
  testWidgets('checklist rows meet tap target and label guidelines', (tester) async {
    tester.view.physicalSize = const Size(390 * 3, 844 * 3);
    tester.view.devicePixelRatio = 3;
    final handle = tester.ensureSemantics();

    await tester.pumpWidget(
      ProviderScope(
        overrides: [connectivityProvider.overrideWith((ref) => Stream.value(false))],
        child: MaterialApp(theme: AppTheme.light(), home: const ChecklistScreen(inspectionId: 'insp-2091')),
      ),
    );
    await tester.pump(const Duration(seconds: 1));

    await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
    await expectLater(tester, meetsGuideline(textContrastGuideline));

    expect(find.text('Offline'), findsOneWidget);
    expect(find.textContaining('checked'), findsOneWidget);
    handle.dispose();
  });

  test('inspection progress counts', () {
    const insp = Inspection(id: 'x', assetTag: 'T', assetType: 'Pole', address: 'a', items: [
      ChecklistItem(id: '1', title: 'a', detail: 'b', status: ItemStatus.pass),
      ChecklistItem(id: '2', title: 'a', detail: 'b', status: ItemStatus.fail),
      ChecklistItem(id: '3', title: 'a', detail: 'b'),
    ]);
    expect(insp.done, 2);
    expect(insp.failed, 1);
    expect(insp.complete, isFalse);
  });
}
