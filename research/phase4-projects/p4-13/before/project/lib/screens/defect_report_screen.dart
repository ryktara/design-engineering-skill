import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

import '../models/inspection.dart';
import '../state/providers.dart';
import '../theme/app_theme.dart';
import '../widgets/bottom_action_bar.dart';
import '../widgets/offline_banner.dart';

/// Defect report: photo, severity, notes. Labels above fields, inline
/// validation on user interaction, error summary on submit, Save stays
/// reachable above the keyboard, and the focused field is scrolled above the
/// action bar (WCAG 2.4.11 / mobile-keyboard-ime).
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

  Future<void> _addPhoto(ImageSource source) async {
    final file = await _picker.pickImage(source: source, maxWidth: 2048, imageQuality: 85);
    if (file == null || !mounted) return;
    setState(() => _photos.add(file));
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
                        child: Wrap(
                          spacing: FieldSizes.controlGap,
                          runSpacing: FieldSizes.controlGap,
                          children: [
                            for (final (i, p) in _photos.indexed)
                              _PhotoThumb(
                                file: p,
                                index: i + 1,
                                onRemove: () => setState(() => _photos.removeAt(i)),
                              ),
                          ],
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

                    // Notes
                    const _SectionLabel('Notes', required: true),
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

class _PhotoThumb extends StatelessWidget {
  const _PhotoThumb({required this.file, required this.index, required this.onRemove});
  final XFile file;
  final int index;
  final VoidCallback onRemove;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Semantics(
      label: 'Photo $index',
      child: Stack(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(FieldSizes.radius),
            child: Image.file(
              File(file.path),
              width: 104,
              height: 104,
              fit: BoxFit.cover,
              cacheWidth: 208,
              errorBuilder: (_, __, ___) => Container(
                width: 104,
                height: 104,
                color: scheme.surfaceContainerHighest,
                child: const Icon(Icons.broken_image, size: 32),
              ),
            ),
          ),
          Positioned(
            top: 0,
            right: 0,
            child: IconButton.filled(
              tooltip: 'Remove photo $index',
              style: IconButton.styleFrom(
                backgroundColor: scheme.inverseSurface,
                foregroundColor: scheme.onInverseSurface,
                minimumSize: const Size(48, 48),
              ),
              onPressed: onRemove,
              icon: const Icon(Icons.close, size: 24),
            ),
          ),
        ],
      ),
    );
  }
}
