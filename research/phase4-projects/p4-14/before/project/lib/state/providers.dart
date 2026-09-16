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

class SyncState {
  const SyncState({required this.pending, required this.lastSyncedAt, this.syncing = false});
  final List<PendingSync> pending;
  final DateTime? lastSyncedAt;
  final bool syncing;

  SyncState copyWith({List<PendingSync>? pending, DateTime? lastSyncedAt, bool? syncing}) => SyncState(
        pending: pending ?? this.pending,
        lastSyncedAt: lastSyncedAt ?? this.lastSyncedAt,
        syncing: syncing ?? this.syncing,
      );
}

class SyncQueue extends Notifier<SyncState> {
  Timer? _drain;

  @override
  SyncState build() {
    ref.listen<bool>(isOnlineProvider, (prev, online) {
      if (online && state.pending.isNotEmpty) _scheduleDrain();
    });
    ref.onDispose(() => _drain?.cancel());
    return SyncState(pending: const [], lastSyncedAt: DateTime.now().subtract(const Duration(minutes: 42)));
  }

  void enqueue(PendingSync item) {
    state = state.copyWith(pending: [...state.pending, item]);
    if (ref.read(isOnlineProvider)) _scheduleDrain();
  }

  void _scheduleDrain() {
    _drain?.cancel();
    _drain = Timer(const Duration(seconds: 2), drain);
  }

  Future<void> drain() async {
    if (state.pending.isEmpty || state.syncing) return;
    state = state.copyWith(syncing: true);
    // Real implementation posts each item; here we simulate the round trip.
    await Future<void>.delayed(const Duration(milliseconds: 800));
    state = SyncState(pending: const [], lastSyncedAt: DateTime.now(), syncing: false);
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
