import 'package:flutter/material.dart';

/// Semantic status colours for inspection items. Kept out of ColorScheme so
/// pass/fail/pending never get confused with primary/error roles.
/// Each text/background pair is validated in design-tokens.json (repo root).
@immutable
class StatusColors extends ThemeExtension<StatusColors> {
  const StatusColors({
    required this.pass,
    required this.onPass,
    required this.fail,
    required this.onFail,
    required this.pending,
    required this.onPending,
    required this.skipped,
    required this.onSkipped,
    required this.offlineBanner,
    required this.onOfflineBanner,
  });

  final Color pass;
  final Color onPass;
  final Color fail;
  final Color onFail;
  final Color pending;
  final Color onPending;
  final Color skipped;
  final Color onSkipped;
  final Color offlineBanner;
  final Color onOfflineBanner;

  static const light = StatusColors(
    pass: Color(0xFF085A26), // 8.4:1 on white, 8.4:1 white on it (tokens.py)
    onPass: Color(0xFFFFFFFF),
    fail: Color(0xFFA3151F),
    onFail: Color(0xFFFFFFFF),
    pending: Color(0xFFFFFFFF),
    onPending: Color(0xFF1B1F24),
    skipped: Color(0xFF4A4F57),
    onSkipped: Color(0xFFFFFFFF),
    offlineBanner: Color(0xFF3A2E00),
    onOfflineBanner: Color(0xFFFFE08A),
  );

  static const dark = StatusColors(
    pass: Color(0xFF7BE495),
    onPass: Color(0xFF00210B),
    fail: Color(0xFFFFB3AE),
    onFail: Color(0xFF410006),
    pending: Color(0xFF1B1F24),
    onPending: Color(0xFFF7F8FA),
    skipped: Color(0xFFC4C7CC),
    onSkipped: Color(0xFF1B1F24),
    offlineBanner: Color(0xFFFFE08A),
    onOfflineBanner: Color(0xFF3A2E00),
  );

  @override
  StatusColors copyWith({
    Color? pass,
    Color? onPass,
    Color? fail,
    Color? onFail,
    Color? pending,
    Color? onPending,
    Color? skipped,
    Color? onSkipped,
    Color? offlineBanner,
    Color? onOfflineBanner,
  }) {
    return StatusColors(
      pass: pass ?? this.pass,
      onPass: onPass ?? this.onPass,
      fail: fail ?? this.fail,
      onFail: onFail ?? this.onFail,
      pending: pending ?? this.pending,
      onPending: onPending ?? this.onPending,
      skipped: skipped ?? this.skipped,
      onSkipped: onSkipped ?? this.onSkipped,
      offlineBanner: offlineBanner ?? this.offlineBanner,
      onOfflineBanner: onOfflineBanner ?? this.onOfflineBanner,
    );
  }

  @override
  StatusColors lerp(StatusColors? other, double t) {
    if (other == null) return this;
    return StatusColors(
      pass: Color.lerp(pass, other.pass, t)!,
      onPass: Color.lerp(onPass, other.onPass, t)!,
      fail: Color.lerp(fail, other.fail, t)!,
      onFail: Color.lerp(onFail, other.onFail, t)!,
      pending: Color.lerp(pending, other.pending, t)!,
      onPending: Color.lerp(onPending, other.onPending, t)!,
      skipped: Color.lerp(skipped, other.skipped, t)!,
      onSkipped: Color.lerp(onSkipped, other.onSkipped, t)!,
      offlineBanner: Color.lerp(offlineBanner, other.offlineBanner, t)!,
      onOfflineBanner: Color.lerp(onOfflineBanner, other.onOfflineBanner, t)!,
    );
  }
}

/// Spacing and sizing tokens. Field use with gloves: controls are 56 dp,
/// never Material's 40 dp default.
abstract final class FieldSizes {
  static const double space1 = 4;
  static const double space2 = 8;
  static const double space3 = 12;
  static const double space4 = 16;
  static const double space6 = 24;
  static const double space8 = 32;
  static const double control = 56; // min tap target (glove)
  static const double controlGap = 12; // min gap between adjacent targets
  static const double radius = 8;
}

class AppTheme {
  static ThemeData light() => _build(Brightness.light, StatusColors.light);
  static ThemeData dark() => _build(Brightness.dark, StatusColors.dark);

  static ThemeData _build(Brightness brightness, StatusColors status) {
    final isLight = brightness == Brightness.light;
    // Hand-tuned scheme rather than fromSeed: sunlight demands near-black on
    // near-white body text and a saturated primary that survives glare.
    final scheme = isLight
        ? const ColorScheme(
            brightness: Brightness.light,
            primary: Color(0xFF0B4DA2),
            onPrimary: Color(0xFFFFFFFF),
            primaryContainer: Color(0xFFD6E4FF),
            onPrimaryContainer: Color(0xFF001A41),
            secondary: Color(0xFF3A4551),
            onSecondary: Color(0xFFFFFFFF),
            secondaryContainer: Color(0xFFDDE4EC),
            onSecondaryContainer: Color(0xFF151C23),
            tertiary: Color(0xFF6B4400),
            onTertiary: Color(0xFFFFFFFF),
            tertiaryContainer: Color(0xFFFFE08A),
            onTertiaryContainer: Color(0xFF241A00),
            error: Color(0xFFA3151F),
            onError: Color(0xFFFFFFFF),
            errorContainer: Color(0xFFFFDAD6),
            onErrorContainer: Color(0xFF410002),
            surface: Color(0xFFFFFFFF),
            onSurface: Color(0xFF1B1F24),
            surfaceContainerHighest: Color(0xFFE6E9EE),
            onSurfaceVariant: Color(0xFF3A4048),
            outline: Color(0xFF5C636D),
            outlineVariant: Color(0xFFC4C7CC),
            shadow: Color(0xFF000000),
            scrim: Color(0xFF000000),
            inverseSurface: Color(0xFF2F3338),
            onInverseSurface: Color(0xFFF1F3F6),
            inversePrimary: Color(0xFFA9C7FF),
          )
        : const ColorScheme(
            brightness: Brightness.dark,
            primary: Color(0xFFA9C7FF),
            onPrimary: Color(0xFF002F68),
            primaryContainer: Color(0xFF00458F),
            onPrimaryContainer: Color(0xFFD6E4FF),
            secondary: Color(0xFFC0C9D4),
            onSecondary: Color(0xFF2A333D),
            secondaryContainer: Color(0xFF3A4551),
            onSecondaryContainer: Color(0xFFDDE4EC),
            tertiary: Color(0xFFFFE08A),
            onTertiary: Color(0xFF3A2E00),
            tertiaryContainer: Color(0xFF523F00),
            onTertiaryContainer: Color(0xFFFFE08A),
            error: Color(0xFFFFB4AB),
            onError: Color(0xFF690005),
            errorContainer: Color(0xFF93000A),
            onErrorContainer: Color(0xFFFFDAD6),
            surface: Color(0xFF121417),
            onSurface: Color(0xFFF1F3F6),
            surfaceContainerHighest: Color(0xFF2F3338),
            onSurfaceVariant: Color(0xFFC4C7CC),
            outline: Color(0xFF8E959E),
            outlineVariant: Color(0xFF444A53),
            shadow: Color(0xFF000000),
            scrim: Color(0xFF000000),
            inverseSurface: Color(0xFFF1F3F6),
            onInverseSurface: Color(0xFF2F3338),
            inversePrimary: Color(0xFF0B4DA2),
          );

    // Type scale: body 18 sp (not 16) because of glare and arm's-length
    // reading; status glyphs 24+.
    const textTheme = TextTheme(
      displaySmall: TextStyle(fontSize: 36, fontWeight: FontWeight.w700, height: 1.15),
      headlineMedium: TextStyle(fontSize: 28, fontWeight: FontWeight.w700, height: 1.2),
      headlineSmall: TextStyle(fontSize: 24, fontWeight: FontWeight.w700, height: 1.25),
      titleLarge: TextStyle(fontSize: 22, fontWeight: FontWeight.w600, height: 1.25),
      titleMedium: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, height: 1.3),
      bodyLarge: TextStyle(fontSize: 18, fontWeight: FontWeight.w400, height: 1.4),
      bodyMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, height: 1.4),
      labelLarge: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, height: 1.2, letterSpacing: 0.2),
      labelMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, height: 1.2, letterSpacing: 0.4),
    );

    final shape = RoundedRectangleBorder(borderRadius: BorderRadius.circular(FieldSizes.radius));
    OutlineInputBorder border(Color c, double w) => OutlineInputBorder(
          borderRadius: BorderRadius.circular(FieldSizes.radius),
          borderSide: BorderSide(color: c, width: w),
        );

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      textTheme: textTheme,
      scaffoldBackgroundColor: scheme.surface,
      visualDensity: VisualDensity.standard,
      materialTapTargetSize: MaterialTapTargetSize.padded,
      extensions: <ThemeExtension<dynamic>>[status],
      appBarTheme: AppBarTheme(
        backgroundColor: scheme.surface,
        foregroundColor: scheme.onSurface,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        titleTextStyle: textTheme.titleLarge?.copyWith(color: scheme.onSurface),
        // 72 not 64: a 56 dp icon button centred in the bar leaves 8 dp to
        // the scrolling content below it (glove spacing rule).
        toolbarHeight: 72,
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size.fromHeight(FieldSizes.control),
          shape: shape,
          textStyle: textTheme.labelLarge,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size.fromHeight(FieldSizes.control),
          shape: shape,
          side: BorderSide(color: scheme.outline, width: 2),
          textStyle: textTheme.labelLarge,
          foregroundColor: scheme.onSurface,
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          minimumSize: const Size(FieldSizes.control, FieldSizes.control),
          textStyle: textTheme.labelLarge,
        ),
      ),
      iconButtonTheme: IconButtonThemeData(
        style: IconButton.styleFrom(
          minimumSize: const Size(FieldSizes.control, FieldSizes.control),
          iconSize: 28,
        ),
      ),
      segmentedButtonTheme: SegmentedButtonThemeData(
        style: SegmentedButton.styleFrom(
          minimumSize: const Size(FieldSizes.control, FieldSizes.control),
          textStyle: textTheme.labelLarge,
          side: BorderSide(color: scheme.outline, width: 2),
          selectedBackgroundColor: scheme.primary,
          selectedForegroundColor: scheme.onPrimary,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: scheme.surface,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: FieldSizes.space4,
          vertical: FieldSizes.space4,
        ),
        border: border(scheme.outline, 2),
        enabledBorder: border(scheme.outline, 2),
        focusedBorder: border(scheme.primary, 3),
        errorBorder: border(scheme.error, 3),
        focusedErrorBorder: border(scheme.error, 3),
        labelStyle: textTheme.bodyLarge?.copyWith(color: scheme.onSurfaceVariant),
        errorStyle: textTheme.bodyMedium?.copyWith(color: scheme.error, fontWeight: FontWeight.w600),
        helperStyle: textTheme.bodyMedium?.copyWith(color: scheme.onSurfaceVariant),
        errorMaxLines: 3,
      ),
      listTileTheme: ListTileThemeData(
        minVerticalPadding: FieldSizes.space4,
        contentPadding: const EdgeInsets.symmetric(horizontal: FieldSizes.space4),
        titleTextStyle: textTheme.titleMedium?.copyWith(color: scheme.onSurface),
        subtitleTextStyle: textTheme.bodyMedium?.copyWith(color: scheme.onSurfaceVariant),
      ),
      dividerTheme: DividerThemeData(color: scheme.outlineVariant, thickness: 1, space: 1),
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        contentTextStyle: textTheme.bodyLarge?.copyWith(color: scheme.onInverseSurface),
      ),
      pageTransitionsTheme: const PageTransitionsTheme(builders: {
        TargetPlatform.android: PredictiveBackPageTransitionsBuilder(),
        TargetPlatform.iOS: CupertinoPageTransitionsBuilder(),
      }),
    );
  }
}
