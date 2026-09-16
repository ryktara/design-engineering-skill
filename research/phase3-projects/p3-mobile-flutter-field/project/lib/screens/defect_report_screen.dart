import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

import '../models/inspection.dart';
import '../state/providers.dart';
import '../state/settings.dart';
import '../theme/app_theme.dart';
import '../widgets/bottom_action_bar.dart';
import '../widgets/offline_banner.dart';

/// Defect report: photo, severity, notes. Labels above fields, inline
/// validation on user interaction, error summary on submit, Save stays
/// reachable above the keyboard, and the focused field is scrolled above the
/// action bar (WCAG 2.4.11 / mobile-keyboard-ime).
///
/// Keyboard: the action bar rides on the IME inset, the list pads for both,
/// tapping outside a field or dragging the list dismisses the keyboard, and a
/// visible "Hide keyboard" control appears while Notes has focus (the notes
/// keyboard uses Return for new lines, so there is no Done key).
/// Photos: two-up 4:3 tiles (~173 x 130 dp at 390 wide) decoded at display
/// size, so a crack or a burn mark is recognisable in the strip itself. One
/// tap opens a full-screen viewer (dark surface, pinch or button zoom,
/// previous/next, Retake / Remove / More) so the photo can be checked in the
/// field before saving; the Retake / Replace / Remove sheet is kept behind
/// "More". A retake replaces the photo in place so numbering stays stable.
class DefectReportScreen extends ConsumerStatefulWidget {
  const DefectReportScreen({super.key, required this.inspectionId, required this.itemId});

  final String inspectionId;
  final String itemId;

  @override
  ConsumerState<DefectReportScreen> createState() => _DefectReportScreenState();
}

class _DefectReportScreenState extends ConsumerState<DefectReportScreen> {
  final _formKey = GlobalKey<FormState>();
  final _notes = TextEditingController();
  final _notesFocus = FocusNode();
  final _picker = ImagePicker();

  final List<XFile> _photos = [];
  Severity? _severity;
  bool _submitted = false; // switches validation from on-blur to always
  bool _saving = false;

  String? get _photoError =>
      _submitted && _photos.isEmpty ? 'Add at least one photo of the defect.' : null;
  String? get _severityError => _submitted && _severity == null ? 'Choose a severity.' : null;

  @override
  void dispose() {
    _notes.dispose();
    _notesFocus.dispose();
    super.dispose();
  }

  Future<XFile?> _pick(ImageSource source) async {
    try {
      return await _picker.pickImage(source: source, maxWidth: 2048, imageQuality: 85);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open the camera. Try again or use the gallery.')),
        );
      }
      return null;
    }
  }

  Future<void> _addPhoto(ImageSource source) async {
    // Close the keyboard first so the camera returns to a stable layout.
    FocusManager.instance.primaryFocus?.unfocus();
    final file = await _pick(source);
    if (file == null || !mounted) return;
    setState(() => _photos.add(file));
  }

  /// Retake replaces the photo at [index] so "Photo 2" stays "Photo 2".
  Future<void> _replacePhoto(int index, ImageSource source) async {
    FocusManager.instance.primaryFocus?.unfocus();
    final file = await _pick(source);
    if (file == null || !mounted) return;
    setState(() => _photos[index] = file);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Photo ${index + 1} replaced')),
    );
  }

  /// Full-screen check of a photo. A pushed route (not a dialog) so the
  /// system back button / predictive back closes it like any other screen.
  Future<void> _openViewer(int index) async {
    FocusManager.instance.primaryFocus?.unfocus();
    final result = await Navigator.of(context).push<_ViewerResult>(
      MaterialPageRoute(
        fullscreenDialog: true,
        builder: (_) => _PhotoViewer(photos: List.unmodifiable(_photos), initialIndex: index),
      ),
    );
    if (result == null || !mounted) return;
    switch (result.action) {
      case _PhotoAction.retake:
        await _replacePhoto(result.index, ImageSource.camera);
      case _PhotoAction.gallery:
        await _replacePhoto(result.index, ImageSource.gallery);
      case _PhotoAction.remove:
        setState(() => _photos.removeAt(result.index));
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Photo ${result.index + 1} removed')),
        );
    }
  }

  Future<void> _photoActions(int index) async {
    final action = await _showPhotoActionsSheet(context, index: index, count: _photos.length);
    if (action == null || !mounted) return;
    switch (action) {
      case _PhotoAction.retake:
        await _replacePhoto(index, ImageSource.camera);
      case _PhotoAction.gallery:
        await _replacePhoto(index, ImageSource.gallery);
      case _PhotoAction.remove:
        setState(() => _photos.removeAt(index));
    }
  }

  /// Shared by the strip (long-press) and the viewer ("More").
  static Future<_PhotoAction?> _showPhotoActionsSheet(BuildContext context, {required int index, required int count}) {
    return showModalBottomSheet<_PhotoAction>(
      context: context,
      useSafeArea: true,
      showDragHandle: true,
      builder: (ctx) {
        final text = Theme.of(ctx).textTheme;
        final scheme = Theme.of(ctx).colorScheme;
        // Same sheet idiom as the checklist "More actions": 56 dp tiles.
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(FieldSizes.space4, 0, FieldSizes.space4, FieldSizes.space2),
                child: Semantics(
                  header: true,
                  child: Text('Photo ${index + 1} of $count', style: text.headlineSmall),
                ),
              ),
              // 8 dp between adjacent 56 dp rows (glove spacing rule).
              ListTile(
                minTileHeight: FieldSizes.control,
                leading: const Icon(Icons.photo_camera, size: 28),
                title: const Text('Retake photo'),
                onTap: () => Navigator.pop(ctx, _PhotoAction.retake),
              ),
              const SizedBox(height: FieldSizes.space2),
              ListTile(
                minTileHeight: FieldSizes.control,
                leading: const Icon(Icons.photo_library, size: 28),
                title: const Text('Replace from gallery'),
                onTap: () => Navigator.pop(ctx, _PhotoAction.gallery),
              ),
              const SizedBox(height: FieldSizes.space2),
              ListTile(
                minTileHeight: FieldSizes.control,
                leading: Icon(Icons.delete, size: 28, color: scheme.error),
                title: Text('Remove photo', style: TextStyle(color: scheme.error)),
                onTap: () => Navigator.pop(ctx, _PhotoAction.remove),
              ),
              const SizedBox(height: FieldSizes.space2),
            ],
          ),
        );
      },
    );
  }

  String? _validateNotes(String? v) {
    final t = v?.trim() ?? '';
    if (t.isEmpty) return 'Describe what you saw and where on the asset.';
    if (t.length < 12) return 'Add a little more detail (at least 12 characters).';
    return null;
  }

  Future<void> _save() async {
    setState(() => _submitted = true);
    final formOk = _formKey.currentState!.validate();
    final problems = <String>[
      if (_photoError != null) 'Photo',
      if (_severityError != null) 'Severity',
      if (!formOk) 'Notes',
    ];
    if (problems.isNotEmpty) {
      // Error summary for screen readers and a visible snackbar; focus the
      // first failing field so the keyboard opens on it.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Fix ${problems.length} field${problems.length == 1 ? '' : 's'}: ${problems.join(', ')}')),
      );
      if (!formOk && problems.length == 1) _notesFocus.requestFocus();
      return;
    }
    setState(() => _saving = true);
    final defect = Defect(
      id: 'd-${DateTime.now().millisecondsSinceEpoch}',
      inspectionId: widget.inspectionId,
      itemId: widget.itemId,
      severity: _severity!,
      notes: _notes.text.trim(),
      photoPaths: _photos.map((p) => p.path).toList(),
      createdAt: DateTime.now(),
    );
    // Write locally first; the queue handles the network.
    ref.read(syncQueueProvider.notifier).enqueue(PendingSync(
          id: defect.id,
          kind: 'defect',
          label: '${defect.severity.label} defect on item ${widget.itemId.toUpperCase()}',
          queuedAt: defect.createdAt,
        ));
    for (final p in _photos) {
      ref.read(syncQueueProvider.notifier).enqueue(PendingSync(
            id: '${defect.id}-${p.name}',
            kind: 'photo',
            label: 'Photo ${p.name}',
            queuedAt: defect.createdAt,
          ));
    }
    ref.read(inspectionProvider(widget.inspectionId).notifier).setStatus(
          widget.itemId,
          ItemStatus.fail,
          defectId: defect.id,
        );
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Defect saved. It will sync when connected.')),
    );
    context.go('/inspection/${widget.inspectionId}');
  }

  Future<bool> _confirmDiscard() async {
    final dirty = _photos.isNotEmpty || _severity != null || _notes.text.isNotEmpty;
    if (!dirty) return true;
    final leave = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Discard this report?'),
        content: const Text('Your photo, severity and notes will be lost.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Keep editing')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Theme.of(ctx).colorScheme.error),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Discard'),
          ),
        ],
      ),
    );
    return leave ?? false;
  }

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    final insets = MediaQuery.viewInsetsOf(context);
    final item = ref.watch(inspectionProvider(widget.inspectionId)).valueOrNull?.items
        .where((i) => i.id == widget.itemId)
        .firstOrNull;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        if (await _confirmDiscard() && context.mounted) context.pop();
      },
      child: Scaffold(
        resizeToAvoidBottomInset: false, // we manage the inset ourselves
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            tooltip: 'Back to checklist',
            onPressed: () async {
              if (await _confirmDiscard() && context.mounted) context.pop();
            },
          ),
          title: const Text('Report defect'),
        ),
        body: Column(
          children: [
            const OfflineBanner(),
            Expanded(
              // Tap on empty space closes the keyboard (mobile-keyboard-ime);
              // translucent so buttons and fields still receive their taps.
              child: GestureDetector(
                behavior: HitTestBehavior.translucent,
                onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
                child: Form(
                key: _formKey,
                autovalidateMode: _submitted ? AutovalidateMode.always : AutovalidateMode.onUserInteraction,
                child: ListView(
                  keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
                  padding: EdgeInsets.fromLTRB(
                    FieldSizes.space4,
                    FieldSizes.space4,
                    FieldSizes.space4,
                    // Room for the action bar plus the keyboard so the focused
                    // field can always scroll above both.
                    BottomActionBar.barHeight + insets.bottom + FieldSizes.space4,
                  ),
                  children: [
                    if (item != null)
                      MergeSemantics(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(item.title, style: text.headlineSmall),
                            Text(item.detail, style: text.bodyLarge?.copyWith(color: scheme.onSurfaceVariant)),
                          ],
                        ),
                      ),
                    const SizedBox(height: FieldSizes.space6),

                    // Photos
                    _SectionLabel('Photo', required: true, error: _photoError),
                    const SizedBox(height: FieldSizes.space2),
                    if (_photos.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(bottom: FieldSizes.space3),
                        // Two tiles per row: at 390 dp that is ~173 x 130 dp,
                        // large enough to recognise the defect in the strip.
                        child: LayoutBuilder(
                          builder: (context, constraints) {
                            final tileWidth = (constraints.maxWidth - FieldSizes.controlGap) / 2;
                            return Semantics(
                              container: true,
                              label: 'Photos, ${_photos.length} added',
                              child: Wrap(
                                spacing: FieldSizes.controlGap,
                                runSpacing: FieldSizes.controlGap,
                                children: [
                                  for (final (i, p) in _photos.indexed)
                                    _PhotoThumb(
                                      file: p,
                                      index: i + 1,
                                      count: _photos.length,
                                      width: tileWidth,
                                      onTap: () => _openViewer(i),
                                      onLongPress: () => _photoActions(i),
                                    ),
                                ],
                              ),
                            );
                          },
                        ),
                      ),
                    Row(
                      children: [
                        Expanded(
                          flex: 3,
                          child: FilledButton.tonalIcon(
                            onPressed: () => _addPhoto(ImageSource.camera),
                            icon: const Icon(Icons.photo_camera, size: 28),
                            label: Text(_photos.isEmpty ? 'Take photo' : 'Add photo'),
                          ),
                        ),
                        const SizedBox(width: FieldSizes.controlGap),
                        Expanded(
                          flex: 2,
                          child: OutlinedButton(
                            onPressed: () => _addPhoto(ImageSource.gallery),
                            child: const Text('Gallery'),
                          ),
                        ),
                      ],
                    ),
                    if (_photoError != null) _FieldError(_photoError!),
                    const SizedBox(height: FieldSizes.space6),

                    // Severity: four 56 dp toggles in a 2x2 grid (gloves), not a
                    // 4-segment button whose segments would be ~85 dp wide with
                    // truncated labels at 18 sp.
                    _SectionLabel('Severity', required: true, error: _severityError),
                    const SizedBox(height: FieldSizes.space2),
                    _SeverityGrid(
                      value: _severity,
                      onChanged: (s) => setState(() => _severity = s),
                      error: _severityError != null,
                    ),
                    if (_severity != null)
                      Padding(
                        padding: const EdgeInsets.only(top: FieldSizes.space2),
                        child: Text(_severity!.guidance, style: text.bodyMedium?.copyWith(color: scheme.onSurfaceVariant)),
                      ),
                    if (_severityError != null) _FieldError(_severityError!),
                    const SizedBox(height: FieldSizes.space6),

                    // Notes. "Hide keyboard" sits in the label row, above the
                    // field, so it is on screen whenever the focused field is
                    // (scrollPadding keeps the field above the bar, not what
                    // sits below it).
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        const Expanded(child: _SectionLabel('Notes', required: true)),
                        ListenableBuilder(
                          listenable: _notesFocus,
                          builder: (context, _) => _notesFocus.hasFocus
                              ? TextButton.icon(
                                  onPressed: () => _notesFocus.unfocus(),
                                  icon: const Icon(Icons.keyboard_hide, size: 24),
                                  label: const Text('Hide keyboard'),
                                )
                              : const SizedBox(height: FieldSizes.control),
                        ),
                      ],
                    ),
                    const SizedBox(height: FieldSizes.space2),
                    TextFormField(
                      controller: _notes,
                      focusNode: _notesFocus,
                      validator: _validateNotes,
                      keyboardType: TextInputType.multiline,
                      textInputAction: TextInputAction.newline,
                      textCapitalization: TextCapitalization.sentences,
                      minLines: 3,
                      maxLines: 6,
                      maxLength: 500,
                      // Keeps the field above the action bar when focused.
                      scrollPadding: EdgeInsets.only(bottom: BottomActionBar.barHeight + insets.bottom + FieldSizes.space6),
                      style: text.bodyLarge,
                      decoration: const InputDecoration(
                        hintText: 'Location on the asset, what you saw, any immediate risk',
                        helperText: 'Voice input works: tap the mic on your keyboard.',
                      ),
                    ),
                  ],
                ),
              ),
              ),
            ),
          ],
        ),
        bottomNavigationBar: BottomActionBar(
          secondary: OutlinedButton(
            onPressed: _saving
                ? null
                : () async {
                    if (await _confirmDiscard() && context.mounted) context.pop();
                  },
            child: const Text('Cancel'),
          ),
          child: FilledButton.icon(
            onPressed: _saving ? null : _save,
            icon: _saving
                ? const SizedBox.square(dimension: 24, child: CircularProgressIndicator(strokeWidth: 3))
                : const Icon(Icons.save),
            label: Text(_saving ? 'Saving…' : 'Save defect'),
          ),
        ),
      ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  const _SectionLabel(this.label, {this.required = false, this.error});
  final String label;
  final bool required;
  final String? error;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final scheme = Theme.of(context).colorScheme;
    return Semantics(
      header: true,
      child: Text.rich(
        TextSpan(
          text: label,
          style: text.titleMedium?.copyWith(color: error != null ? scheme.error : scheme.onSurface),
          children: [
            if (required)
              TextSpan(text: '  Required', style: text.labelMedium?.copyWith(color: scheme.onSurfaceVariant)),
          ],
        ),
      ),
    );
  }
}

class _FieldError extends StatelessWidget {
  const _FieldError(this.message);
  final String message;
  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;
    return Semantics(
      liveRegion: true,
      child: Padding(
        padding: const EdgeInsets.only(top: FieldSizes.space2),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(Icons.error, size: 20, color: scheme.error),
            const SizedBox(width: FieldSizes.space2),
            Expanded(
              child: Text(message, style: text.bodyMedium?.copyWith(color: scheme.error, fontWeight: FontWeight.w600)),
            ),
          ],
        ),
      ),
    );
  }
}

class _SeverityGrid extends StatelessWidget {
  const _SeverityGrid({required this.value, required this.onChanged, required this.error});
  final Severity? value;
  final ValueChanged<Severity> onChanged;
  final bool error;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final sc = Theme.of(context).extension<StatusColors>()!;
    Color fillFor(Severity s) => switch (s) {
          Severity.low => scheme.secondary,
          Severity.medium => scheme.tertiary,
          Severity.high => sc.fail,
          Severity.critical => sc.fail,
        };
    Widget cell(Severity s) {
      final selected = value == s;
      final fill = fillFor(s);
      return Semantics(
        inMutuallyExclusiveGroup: true,
        selected: selected,
        label: '${s.label} severity',
        child: selected
            ? FilledButton.icon(
                style: FilledButton.styleFrom(backgroundColor: fill, foregroundColor: scheme.onPrimary),
                onPressed: () => onChanged(s),
                icon: Icon(s == Severity.critical ? Icons.warning : Icons.check, size: 24),
                label: Text(s.label),
              )
            : OutlinedButton(
                style: OutlinedButton.styleFrom(
                  side: BorderSide(color: error ? scheme.error : scheme.outline, width: 2),
                ),
                onPressed: () => onChanged(s),
                child: Text(s.label),
              ),
      );
    }

    return Column(
      children: [
        Row(children: [
          Expanded(child: cell(Severity.low)),
          const SizedBox(width: FieldSizes.controlGap),
          Expanded(child: cell(Severity.medium)),
        ]),
        const SizedBox(height: FieldSizes.controlGap),
        Row(children: [
          Expanded(child: cell(Severity.high)),
          const SizedBox(width: FieldSizes.controlGap),
          Expanded(child: cell(Severity.critical)),
        ]),
      ],
    );
  }
}

enum _PhotoAction { retake, gallery, remove }

class _ViewerResult {
  const _ViewerResult(this.action, this.index);
  final _PhotoAction action;
  final int index;
}

/// One tile per photo, 4:3 at half the content width, decoded at display
/// size for the device's pixel ratio (not a fixed 208 px). Tap opens the
/// full-screen viewer; long-press is a shortcut to the actions sheet, which
/// is also reachable from the viewer's "More" (no gesture-only path). No
/// small overlay buttons inside the tile (glove spacing rule).
class _PhotoThumb extends StatelessWidget {
  const _PhotoThumb({
    required this.file,
    required this.index,
    required this.count,
    required this.width,
    required this.onTap,
    required this.onLongPress,
  });
  final XFile file;
  final int index;
  final int count;
  final double width;
  final VoidCallback onTap;
  final VoidCallback onLongPress;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final text = Theme.of(context).textTheme;
    final dpr = MediaQuery.devicePixelRatioOf(context);
    final height = width * 3 / 4;
    return Semantics(
      button: true,
      label: 'Photo $index of $count',
      hint: 'Opens full size to check it',
      child: Material(
        color: scheme.surfaceContainerHighest,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(FieldSizes.radius),
          side: BorderSide(color: scheme.outlineVariant),
        ),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: onTap,
          onLongPress: onLongPress,
          child: SizedBox(
            width: width,
            height: height,
            child: Stack(
              fit: StackFit.expand,
              children: [
                ExcludeSemantics(
                  child: Image.file(
                    File(file.path),
                    fit: BoxFit.cover,
                    cacheWidth: (width * dpr).round(),
                    errorBuilder: (_, __, ___) => const Icon(Icons.broken_image, size: 32),
                  ),
                ),
                // Index chip: text on inverse surface so it reads on any photo.
                Positioned(
                  left: FieldSizes.space2,
                  bottom: FieldSizes.space2,
                  child: ExcludeSemantics(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: FieldSizes.space2, vertical: 2),
                      decoration: BoxDecoration(
                        color: scheme.inverseSurface,
                        borderRadius: BorderRadius.circular(FieldSizes.space1),
                      ),
                      child: Text('$index', style: text.labelMedium?.copyWith(color: scheme.onInverseSurface)),
                    ),
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

/// Full-screen photo check. Always the app's dark theme (with the current
/// high-contrast setting) so the photo sits on a near-black surface with
/// high-contrast 56 dp controls that survive glare; the AppBar, buttons and
/// [BottomActionBar] are the same components as the rest of the app.
///
/// Zoom: pinch, double-tap, or the Zoom button (gestures are never the only
/// path). Previous / Next are labelled 56 dp buttons in thumb reach; swiping
/// between photos also works when not zoomed. Retake and Remove act on the
/// photo being viewed; "More" opens the same Retake / Replace / Remove sheet
/// as the strip. System back closes the viewer.
class _PhotoViewer extends ConsumerStatefulWidget {
  const _PhotoViewer({required this.photos, required this.initialIndex});

  final List<XFile> photos;
  final int initialIndex;

  @override
  ConsumerState<_PhotoViewer> createState() => _PhotoViewerState();
}

class _PhotoViewerState extends ConsumerState<_PhotoViewer> {
  static const double _zoomScale = 2.5;

  late final PageController _pages = PageController(initialPage: widget.initialIndex);
  final _transform = TransformationController();
  late int _index = widget.initialIndex;
  bool _zoomed = false;

  @override
  void initState() {
    super.initState();
    _transform.addListener(_onTransform);
  }

  @override
  void dispose() {
    _transform.removeListener(_onTransform);
    _transform.dispose();
    _pages.dispose();
    super.dispose();
  }

  void _onTransform() {
    final zoomed = _transform.value.getMaxScaleOnAxis() > 1.05;
    if (zoomed != _zoomed) setState(() => _zoomed = zoomed);
  }

  /// Zoom into the centre of the viewport (a bare scale would zoom into the
  /// top-left corner). Instant: no animation to respect, nothing to reduce.
  void _toggleZoom(Size viewport) {
    if (_zoomed) {
      _transform.value = Matrix4.identity();
      return;
    }
    final dx = -(viewport.width * (_zoomScale - 1)) / 2;
    final dy = -(viewport.height * (_zoomScale - 1)) / 2;
    _transform.value = Matrix4.identity()
      ..translate(dx, dy)
      ..scale(_zoomScale);
  }

  void _goTo(int index) {
    if (index < 0 || index >= widget.photos.length) return;
    _transform.value = Matrix4.identity();
    final reduceMotion = MediaQuery.disableAnimationsOf(context);
    if (reduceMotion) {
      _pages.jumpToPage(index);
    } else {
      _pages.animateToPage(index, duration: const Duration(milliseconds: 200), curve: Curves.easeOut);
    }
  }

  /// [themedContext] sits under the viewer's dark [Theme] so the sheet
  /// inherits it instead of the captured light app theme.
  Future<void> _more(BuildContext themedContext) async {
    final action = await _DefectReportScreenState._showPhotoActionsSheet(
      themedContext,
      index: _index,
      count: widget.photos.length,
    );
    if (action == null || !mounted) return;
    Navigator.of(context).pop(_ViewerResult(action, _index));
  }

  @override
  Widget build(BuildContext context) {
    final highContrast = ref.watch(settingsProvider.select((s) => s.highContrast));
    final count = widget.photos.length;
    return Theme(
      data: AppTheme.dark(highContrast: highContrast),
      child: Builder(
        builder: (context) {
          final scheme = Theme.of(context).colorScheme;
          return Scaffold(
            appBar: AppBar(
              leading: IconButton(
                icon: const Icon(Icons.close),
                tooltip: 'Back to report',
                onPressed: () => Navigator.of(context).pop(),
              ),
              // Live region: TalkBack / VoiceOver announce the page change.
              title: Semantics(
                liveRegion: true,
                child: Text('Photo ${_index + 1} of $count'),
              ),
              actions: [
                IconButton(
                  icon: Icon(_zoomed ? Icons.zoom_out : Icons.zoom_in),
                  tooltip: _zoomed ? 'Zoom out' : 'Zoom in',
                  onPressed: () => _toggleZoom(_viewportSize(context)),
                ),
                IconButton(
                  icon: const Icon(Icons.more_vert),
                  tooltip: 'More: retake, replace or remove',
                  onPressed: () => _more(context),
                ),
              ],
            ),
            body: Column(
              children: [
                Expanded(
                  child: LayoutBuilder(
                    builder: (context, constraints) {
                      final viewport = constraints.biggest;
                      return PageView.builder(
                        controller: _pages,
                        // When zoomed, drags pan the photo instead of paging.
                        physics: _zoomed ? const NeverScrollableScrollPhysics() : const PageScrollPhysics(),
                        onPageChanged: (i) => setState(() => _index = i),
                        itemCount: count,
                        itemBuilder: (context, i) {
                          final image = Image.file(
                            File(widget.photos[i].path),
                            fit: BoxFit.contain,
                            filterQuality: FilterQuality.medium,
                            errorBuilder: (_, __, ___) => Center(
                              child: Icon(Icons.broken_image, size: 56, color: scheme.onSurfaceVariant),
                            ),
                          );
                          return Semantics(
                            image: true,
                            label: 'Photo ${i + 1} of $count',
                            child: GestureDetector(
                              onDoubleTap: () => _toggleZoom(viewport),
                              child: InteractiveViewer(
                                transformationController: i == _index ? _transform : null,
                                minScale: 1,
                                maxScale: 4,
                                panEnabled: _zoomed,
                                clipBehavior: Clip.hardEdge,
                                child: SizedBox.expand(child: image),
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                ),
                if (count > 1)
                  Padding(
                    padding: const EdgeInsets.fromLTRB(FieldSizes.space4, FieldSizes.space3, FieldSizes.space4, 0),
                    child: Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: _index > 0 ? () => _goTo(_index - 1) : null,
                            icon: const Icon(Icons.chevron_left, size: 28),
                            label: const Text('Previous'),
                          ),
                        ),
                        const SizedBox(width: FieldSizes.controlGap),
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: _index < count - 1 ? () => _goTo(_index + 1) : null,
                            icon: const Icon(Icons.chevron_right, size: 28),
                            label: const Text('Next'),
                          ),
                        ),
                      ],
                    ),
                  ),
              ],
            ),
            bottomNavigationBar: BottomActionBar(
              secondary: OutlinedButton(
                style: OutlinedButton.styleFrom(
                  foregroundColor: scheme.error,
                  side: BorderSide(color: scheme.error, width: highContrast ? 3 : 2),
                ),
                onPressed: () => Navigator.of(context).pop(_ViewerResult(_PhotoAction.remove, _index)),
                child: const Text('Remove'),
              ),
              child: FilledButton.tonalIcon(
                onPressed: () => Navigator.of(context).pop(_ViewerResult(_PhotoAction.retake, _index)),
                icon: const Icon(Icons.photo_camera, size: 28),
                label: const Text('Retake'),
              ),
            ),
          );
        },
      ),
    );
  }

  /// Size of the photo area, for centring the button zoom.
  Size _viewportSize(BuildContext context) {
    final size = MediaQuery.sizeOf(context);
    final padding = MediaQuery.paddingOf(context);
    final navRow = widget.photos.length > 1 ? FieldSizes.control + FieldSizes.space3 : 0.0;
    // 72 = AppBar toolbarHeight in app_theme.dart.
    return Size(size.width, size.height - padding.top - 72 - navRow - BottomActionBar.barHeight - padding.bottom);
  }
}
