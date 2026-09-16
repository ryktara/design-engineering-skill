import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'screens/checklist_screen.dart';
import 'screens/defect_report_screen.dart';
import 'screens/settings_screen.dart';
import 'state/settings.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: FieldInspectApp()));
}

final _router = GoRouter(
  initialLocation: '/inspection/insp-2091',
  routes: [
    GoRoute(
      path: '/inspection/:id',
      builder: (context, state) => ChecklistScreen(inspectionId: state.pathParameters['id']!),
      routes: [
        GoRoute(
          path: 'defect/:itemId',
          builder: (context, state) => DefectReportScreen(
            inspectionId: state.pathParameters['id']!,
            itemId: state.pathParameters['itemId']!,
          ),
        ),
      ],
    ),
    GoRoute(path: '/settings', builder: (context, state) => const SettingsScreen()),
  ],
);

class FieldInspectApp extends ConsumerWidget {
  const FieldInspectApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // In-app high-contrast switch; the OS "increase contrast" setting picks
    // the same themes through highContrastTheme / highContrastDarkTheme.
    final highContrast = ref.watch(settingsProvider.select((s) => s.highContrast));
    return MaterialApp.router(
      title: 'Field Inspect',
      theme: AppTheme.light(highContrast: highContrast),
      darkTheme: AppTheme.dark(highContrast: highContrast),
      highContrastTheme: AppTheme.light(highContrast: true),
      highContrastDarkTheme: AppTheme.dark(highContrast: true),
      // Outdoors the light theme is the working theme; dark follows the
      // system setting for night callouts.
      themeMode: ThemeMode.system,
      routerConfig: _router,
      // Respect the user's font scale but keep the 56 dp control grid
      // intact: clamp at 1.6 and let text wrap instead of clip.
      builder: (context, child) {
        final mq = MediaQuery.of(context);
        return MediaQuery(
          data: mq.copyWith(textScaler: mq.textScaler.clamp(minScaleFactor: 1.0, maxScaleFactor: 1.6)),
          child: child!,
        );
      },
    );
  }
}
