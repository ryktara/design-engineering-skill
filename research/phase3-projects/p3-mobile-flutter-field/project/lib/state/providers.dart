import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/inspection.dart';

/// True when the device has any network route. Poor connectivity is not the
/// same as offline; the sync queue drains opportunistically either way.
final connectivityProvider = StreamProvider<bool>((ref) {
  return Connectivity()
      .onConnectivityChanged
      .map((results) => results.any((r) => r != ConnectivityResult.none))
      .distinct();
});

final isOnlineProvider = Provider<bool>((ref) {
  return ref.watch(connectivityProvider).maybeWhen(data: (v) => v, orElse: () => true);
});

/// Sync state the UI can narrate: which item is going out now, how many of
/// this run are done, which ones failed and why, and whether a run just
/// finished (so the banner can say "All sent" once and then clear).
class SyncState {
  const SyncState({
    required this.pending,
    required this.lastSyncedAt,
    this.syncing = false,
    this.runTotal = 0,
    this.runSent = 0,
    this.completedAt,
  });

  /// Items not yet confirmed by the server, in send order. Sent items are
  /// removed; failed items stay with their reason until retried.
  final List<PendingSync> pending;
  final DateTime? lastSyncedAt;
  final bool syncing;

  /// Size of the run in progress and how many of it have been sent, so the
  /// UI can show a determinate "Sending 2 of 3" instead of a spinner.
  final int runTotal;
  final int runSent;

  /// Set when a run has just sent everything; cleared a few seconds later.
  final DateTime? completedAt;

  PendingSync? get sending => pending.cast<PendingSync?>().firstWhere(
        (p) => p!.status == SyncItemStatus.sending,
        orElse: () => null,
      );
  List<PendingSync> get failed => pending.where((p) => p.status == SyncItemStatus.failed).toList();
  List<PendingSync> get queued => pending.where((p) => p.status == SyncItemStatus.queued).toList();
  bool get hasFailures => failed.isNotEmpty;

  /// 0..1 for the run in progress; the item being sent counts as half done
  /// so the bar moves as soon as the run starts.
  double get progress => runTotal == 0 ? 0 : ((runSent + (sending != null ? 0.5 : 0)) / runTotal).clamp(0, 1);

  SyncState copyWith({
    List<PendingSync>? pending,
    DateTime? lastSyncedAt,
    bool? syncing,
    int? runTotal,
    int? runSent,
    DateTime? completedAt,
    bool clearCompleted = false,
  }) =>
      SyncState(
        pending: pending ?? this.pending,
        lastSyncedAt: lastSyncedAt ?? this.lastSyncedAt,
        syncing: syncing ?? this.syncing,
        runTotal: runTotal ?? this.runTotal,
        runSent: runSent ?? this.runSent,
        completedAt: clearCompleted ? null : (completedAt ?? this.completedAt),
      );
}

class SyncQueue extends Notifier<SyncState> {
  Timer? _drain;
  Timer? _clearDone;

  /// How long "All sent" stays in the banner before it clears itself.
  static const doneVisibleFor = Duration(seconds: 4);

  @override
  SyncState build() {
    ref.listen<bool>(isOnlineProvider, (prev, online) {
      if (online && state.queued.isNotEmpty) _scheduleDrain();
    });
    ref.onDispose(() {
      _drain?.cancel();
      _clearDone?.cancel();
    });
    return SyncState(pending: const [], lastSyncedAt: DateTime.now().subtract(const Duration(minutes: 42)));
  }

  void enqueue(PendingSync item) {
    state = state.copyWith(pending: [...state.pending, item], clearCompleted: true);
    if (ref.read(isOnlineProvider)) _scheduleDrain();
  }

  void _scheduleDrain() {
    _drain?.cancel();
    _drain = Timer(const Duration(seconds: 2), drain);
  }

  /// Sends every queued item in order. Failed items are left in the queue
  /// with their reason; [retryFailed] or [retry] puts them back to queued.
  Future<void> drain() async {
    if (state.queued.isEmpty || state.syncing) return;
    final run = state.queued.map((p) => p.id).toList();
    state = state.copyWith(syncing: true, runTotal: run.length, runSent: 0, clearCompleted: true);
    var sent = 0;
    for (final id in run) {
      _mark(id, SyncItemStatus.sending);
      // Real implementation posts the item; here we simulate the round trip
      // and let the transport report a plain-language failure reason.
      final error = await _post(_byId(id));
      if (error == null) {
        sent++;
        state = state.copyWith(pending: state.pending.where((p) => p.id != id).toList(), runSent: sent);
      } else {
        _mark(id, SyncItemStatus.failed, error: error);
      }
    }
    state = state.copyWith(
      syncing: false,
      lastSyncedAt: sent > 0 ? DateTime.now() : null,
      completedAt: state.pending.isEmpty ? DateTime.now() : null,
    );
    if (state.completedAt != null) {
      _clearDone?.cancel();
      _clearDone = Timer(doneVisibleFor, () => state = state.copyWith(clearCompleted: true));
    }
  }

  /// Manual retry from the offline strip. Re-reads connectivity first (the
  /// stream can still say "none" for a few seconds after signal returns),
  /// then puts failed items back in the queue and sends. Returns whether the
  /// device is back online; nothing is dropped when it is not.
  Future<bool> retryNow() async {
    ref.invalidate(connectivityProvider);
    final results = await Connectivity().checkConnectivity();
    final online = results.any((r) => r != ConnectivityResult.none);
    if (!online) return false;
    state = state.copyWith(pending: [
      for (final p in state.pending)
        if (p.status == SyncItemStatus.failed) p.copyWith(status: SyncItemStatus.queued) else p
    ]);
    await drain();
    return true;
  }

  /// Puts one failed item back in the queue and sends again.
  void retry(String id) {
    _mark(id, SyncItemStatus.queued);
    if (ref.read(isOnlineProvider)) drain();
  }

  /// Puts every failed item back in the queue and sends again.
  void retryFailed() {
    state = state.copyWith(pending: [
      for (final p in state.pending)
        if (p.status == SyncItemStatus.failed) p.copyWith(status: SyncItemStatus.queued) else p
    ]);
    if (ref.read(isOnlineProvider)) drain();
  }

  PendingSync _byId(String id) => state.pending.firstWhere((p) => p.id == id);

  void _mark(String id, SyncItemStatus status, {String? error}) {
    state = state.copyWith(pending: [
      for (final p in state.pending)
        if (p.id == id) p.copyWith(status: status, error: error, attempts: p.attempts + (status == SyncItemStatus.sending ? 1 : 0)) else p
    ]);
  }

  /// Simulated transport. Returns null on success or the reason the server
  /// gave. Ids containing 'fail' fail on their first attempt so the failed
  /// state can be exercised; everything succeeds on retry.
  Future<String?> _post(PendingSync item) async {
    await Future<void>.delayed(const Duration(milliseconds: 800));
    if (item.id.contains('fail') && item.attempts <= 1) {
      return item.kind == 'photo' ? 'Server rejected the file (too large)' : 'Server did not answer';
    }
    return null;
  }
}

final syncQueueProvider = NotifierProvider<SyncQueue, SyncState>(SyncQueue.new);

/// Loads an inspection by id. Fails deliberately for id 'err' so the error
/// state can be exercised; 'empty' returns a zero-item inspection.
final inspectionProvider = AsyncNotifierProvider.family<InspectionNotifier, Inspection, String>(
  InspectionNotifier.new,
);

class InspectionNotifier extends FamilyAsyncNotifier<Inspection, String> {
  @override
  Future<Inspection> build(String arg) async {
    await Future<void>.delayed(const Duration(milliseconds: 600));
    if (arg == 'err') throw StateError('Could not load inspection $arg from local store');
    if (arg == 'empty') {
      return const Inspection(
          id: 'empty', assetTag: 'TX-0000', assetType: 'Transformer', address: 'Unassigned', items: []);
    }
    return Inspection(
      id: arg,
      assetTag: 'PL-48211',
      assetType: 'Wood distribution pole',
      address: '1140 Ridgeway Rd, north verge',
      items: const [
        ChecklistItem(
            id: 'c1',
            title: 'Pole condition',
            detail: 'Rot, cracks, woodpecker holes, lean over 5 degrees',
            status: ItemStatus.pass),
        ChecklistItem(
            id: 'c2',
            title: 'Crossarm and insulators',
            detail: 'Cracked, burned or tracking insulators; loose hardware',
            status: ItemStatus.fail,
            defectId: 'd1'),
        ChecklistItem(
            id: 'c3', title: 'Conductor clearance', detail: 'Vegetation, structures, ground clearance per spec'),
        ChecklistItem(id: 'c4', title: 'Guy wires and anchors', detail: 'Tension, corrosion, guy guard present'),
        ChecklistItem(id: 'c5', title: 'Grounding', detail: 'Ground rod, down lead intact, clamp tight'),
        ChecklistItem(
            id: 'c6',
            title: 'Signage and tags',
            detail: 'Pole tag legible; high-voltage sign present',
            status: ItemStatus.skipped),
      ],
    );
  }

  void setStatus(String itemId, ItemStatus status, {String? defectId}) {
    final current = state.valueOrNull;
    if (current == null) return;
    state = AsyncData(current.copyWith(
      items: [
        for (final i in current.items)
          if (i.id == itemId) i.copyWith(status: status, defectId: defectId) else i
      ],
    ));
    ref.read(syncQueueProvider.notifier).enqueue(PendingSync(
          id: '${current.id}-$itemId-${DateTime.now().microsecondsSinceEpoch}',
          kind: 'item',
          label: 'Item ${itemId.toUpperCase()} set to ${status.name}',
          queuedAt: DateTime.now(),
        ));
  }
}
