/// Domain models. Plain Dart, no Flutter imports, so they can be unit-tested
/// and serialised for the offline queue.
enum ItemStatus { pending, pass, fail, skipped }

enum Severity {
  low('Low', 'Monitor; fix at next scheduled visit'),
  medium('Medium', 'Schedule repair within 30 days'),
  high('High', 'Repair within 72 hours'),
  critical('Critical', 'Immediate hazard: isolate and dispatch');

  const Severity(this.label, this.guidance);
  final String label;
  final String guidance;
}

class ChecklistItem {
  const ChecklistItem({
    required this.id,
    required this.title,
    required this.detail,
    this.status = ItemStatus.pending,
    this.defectId,
  });

  final String id;
  final String title;
  final String detail;
  final ItemStatus status;
  final String? defectId;

  ChecklistItem copyWith({ItemStatus? status, String? defectId}) => ChecklistItem(
        id: id,
        title: title,
        detail: detail,
        status: status ?? this.status,
        defectId: defectId ?? this.defectId,
      );
}

class Inspection {
  const Inspection({
    required this.id,
    required this.assetTag,
    required this.assetType,
    required this.address,
    required this.items,
  });

  final String id;
  final String assetTag;
  final String assetType;
  final String address;
  final List<ChecklistItem> items;

  int get done => items.where((i) => i.status != ItemStatus.pending).length;
  int get failed => items.where((i) => i.status == ItemStatus.fail).length;
  bool get complete => items.isNotEmpty && done == items.length;

  Inspection copyWith({List<ChecklistItem>? items}) => Inspection(
        id: id,
        assetTag: assetTag,
        assetType: assetType,
        address: address,
        items: items ?? this.items,
      );
}

class Defect {
  const Defect({
    required this.id,
    required this.inspectionId,
    required this.itemId,
    required this.severity,
    required this.notes,
    required this.photoPaths,
    required this.createdAt,
  });

  final String id;
  final String inspectionId;
  final String itemId;
  final Severity severity;
  final String notes;
  final List<String> photoPaths;
  final DateTime createdAt;

  Map<String, Object?> toJson() => {
        'id': id,
        'inspectionId': inspectionId,
        'itemId': itemId,
        'severity': severity.name,
        'notes': notes,
        'photoPaths': photoPaths,
        'createdAt': createdAt.toIso8601String(),
      };
}

/// One unit of work waiting to reach the server.
class PendingSync {
  const PendingSync({required this.id, required this.kind, required this.label, required this.queuedAt});
  final String id;
  final String kind; // 'defect' | 'item' | 'photo'
  final String label;
  final DateTime queuedAt;
}
