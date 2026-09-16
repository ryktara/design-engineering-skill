using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Erp.Client.Models;
using Microsoft.UI.Dispatching;
using Microsoft.UI.Xaml.Controls;

namespace Erp.Client.ViewModels;

public sealed partial class StockAdjustmentsViewModel : ObservableObject
{
    private readonly List<StockAdjustment> _all = new();
    private string? _sortKey;
    private bool _sortDescending;
    private int _pendingCount;

    /// <summary>
    /// Typing filters a 3,000-row table. Re-running the filter on every keystroke and pushing the
    /// result row by row is what made the grid stutter; the text filters are coalesced into one
    /// pass ~180 ms after the last keystroke and pushed as a single Reset.
    /// </summary>
    private readonly DispatcherQueueTimer? _filterTimer;
    private const int FilterDebounceMs = 180;

    /// <summary>Bound to the DataGrid: refilled with one Reset, never row by row.</summary>
    public BulkObservableCollection<StockAdjustment> FilteredItems { get; } = new();
    public IReadOnlyList<AdjustmentStatus?> StatusOptions { get; } =
        new AdjustmentStatus?[] { null, AdjustmentStatus.Draft, AdjustmentStatus.PendingApproval, AdjustmentStatus.Posted, AdjustmentStatus.Rejected };

    [ObservableProperty] private string? _searchText;
    [ObservableProperty] private string? _locationFilter;
    [ObservableProperty] private AdjustmentStatus? _statusFilter;
    [ObservableProperty] private StockAdjustment? _selected;
    [ObservableProperty] private bool _isLoading;
    [ObservableProperty] private string? _message;
    [ObservableProperty] private InfoBarSeverity _messageSeverity = InfoBarSeverity.Informational;

    public bool HasMessage => !string.IsNullOrEmpty(Message);
    public bool HasActiveFilters => !string.IsNullOrWhiteSpace(SearchText) || !string.IsNullOrWhiteSpace(LocationFilter) || StatusFilter is not null;
    public bool CanApproveSelected => Selected is { IsActionable: true };

    /// <summary>Named next to the commands so the user always knows what Approve/Reject will act on.</summary>
    public string SelectionLabel => Selected is { } s ? $"Selected: {s.Id}" : "No adjustment selected";

    /// <summary>Single source for the F1 reference; keep in sync with the KeyboardAccelerators in the page.</summary>
    public IReadOnlyList<ShortcutInfo> Shortcuts { get; } = new[]
    {
        new ShortcutInfo("Ctrl+N", "New adjustment"),
        new ShortcutInfo("Ctrl+Shift+A", "Approve the selected adjustment"),
        new ShortcutInfo("Ctrl+Shift+R", "Reject the selected adjustment"),
        new ShortcutInfo("F2 / Enter", "Edit the selected adjustment"),
        new ShortcutInfo("F5", "Refresh the list (selection is kept)"),
        new ShortcutInfo("Ctrl+F", "Go to search"),
        new ShortcutInfo("Esc", "Clear the search text (in the search box)"),
        new ShortcutInfo("Ctrl+Shift+L", "Clear all filters"),
        new ShortcutInfo("F6 / Shift+F6", "Move between commands, filters and the table"),
        new ShortcutInfo("\u2191 \u2193 Home End", "Move between rows; \u2192 \u2190 reach the row actions"),
        new ShortcutInfo("Shift+F10", "Open the row context menu"),
        new ShortcutInfo("Alt", "Show access keys for the commands"),
        new ShortcutInfo("F1", "This list"),
    };

    public string ResultSummary => HasActiveFilters
        ? $"{FilteredItems.Count:N0} of {_all.Count:N0} adjustments match the current filters"
        : $"{_all.Count:N0} adjustments, {_pendingCount:N0} pending approval";

    public string EmptyTitle => HasActiveFilters ? "No adjustments match" : "No stock adjustments yet";
    public string EmptyBody => HasActiveFilters
        ? "Try a broader search or clear the filters to see every adjustment."
        : "Adjustments record counted, damaged or returned stock. Create the first one to start.";
    public string EmptyActionLabel => HasActiveFilters ? "Clear filters" : "New adjustment";
    public IRelayCommand EmptyActionCommand => HasActiveFilters ? ClearFiltersCommand : NewAdjustmentCommand;

    public StockAdjustmentsViewModel()
    {
        // Null in unit tests / non-UI threads: then the filter runs synchronously.
        var queue = DispatcherQueue.GetForCurrentThread();
        if (queue is not null)
        {
            _filterTimer = queue.CreateTimer();
            _filterTimer.IsRepeating = false;
            _filterTimer.Interval = TimeSpan.FromMilliseconds(FilterDebounceMs);
            _filterTimer.Tick += (_, _) => ApplyFilters();
        }
        Load();
    }

    private void ApplyFiltersDebounced()
    {
        if (_filterTimer is null) { ApplyFilters(); return; }
        _filterTimer.Stop();
        _filterTimer.Start();
    }

    partial void OnSearchTextChanged(string? value) => ApplyFiltersDebounced();
    partial void OnLocationFilterChanged(string? value) => ApplyFiltersDebounced();
    partial void OnStatusFilterChanged(AdjustmentStatus? value) => ApplyFilters();
    partial void OnSelectedChanged(StockAdjustment? value)
    {
        OnPropertyChanged(nameof(CanApproveSelected));
        OnPropertyChanged(nameof(SelectionLabel));
    }
    partial void OnMessageChanged(string? value) => OnPropertyChanged(nameof(HasMessage));

    private void Load()
    {
        _all.Clear();
        var now = DateTimeOffset.Now;
        _all.Add(new("ADJ-10421", "PLT-0032", "Euro pallet, heat treated", "A-01-03", AdjustmentReason.CycleCount, 148m, -3m, "ea", 12.40m, AdjustmentStatus.PendingApproval, "m.okafor", now.AddMinutes(-14)));
        _all.Add(new("ADJ-10420", "BLT-M8-40", "Hex bolt M8x40 zinc", "B-04-11", AdjustmentReason.Correction, 12_400m, 250m, "ea", 0.08m, AdjustmentStatus.Draft, "j.lindqvist", now.AddHours(-1)));
        _all.Add(new("ADJ-10419", "OIL-5W30-5L", "Engine oil 5W-30, 5 L", "C-02-01", AdjustmentReason.Damage, 36m, -2m, "can", 21.95m, AdjustmentStatus.Posted, "m.okafor", now.AddHours(-3)));
        _all.Add(new("ADJ-10418", "CBL-CAT6-305", "Cat6 cable drum 305 m", "A-07-02", AdjustmentReason.Shrinkage, 9m, -1m, "drum", 96.00m, AdjustmentStatus.Rejected, "r.patel", now.AddDays(-1)));
        _all.Add(new("ADJ-10417", "GLV-NIT-L", "Nitrile gloves, L, box 100", "D-01-05", AdjustmentReason.Return, 210m, 12m, "box", 6.30m, AdjustmentStatus.Posted, "j.lindqvist", now.AddDays(-1)));
        _all.Add(new("ADJ-10416", "PLT-0032", "Euro pallet, heat treated", "A-01-04", AdjustmentReason.CycleCount, 96m, 4m, "ea", 12.40m, AdjustmentStatus.Posted, "r.patel", now.AddDays(-2)));
        _all.Add(new("ADJ-10415", "TAP-PVC-50", "PVC tape 50 mm x 66 m", "B-02-08", AdjustmentReason.Shrinkage, 1_020m, -18m, "roll", 1.15m, AdjustmentStatus.PendingApproval, "m.okafor", now.AddDays(-2)));
        _all.Add(new("ADJ-10414", "FLT-AIR-220", "Air filter 220 mm", "C-05-03", AdjustmentReason.Damage, 44m, -6m, "ea", 14.80m, AdjustmentStatus.Draft, "r.patel", now.AddDays(-3)));
        AddHistory(now, targetTotal: 3_000);
        _pendingCount = _all.Count(a => a.Status == AdjustmentStatus.PendingApproval);
        ApplyFilters();
    }

    /// <summary>
    /// A real warehouse quarter is a few thousand adjustments. The history is generated
    /// deterministically so the screen can be reviewed at its true size (3,000 rows) instead of
    /// at a demo size where every scrolling problem is invisible.
    /// </summary>
    private void AddHistory(DateTimeOffset now, int targetTotal)
    {
        var skus = new[]
        {
            ("PLT-0032", "Euro pallet, heat treated", "ea", 12.40m),
            ("BLT-M8-40", "Hex bolt M8x40 zinc", "ea", 0.08m),
            ("OIL-5W30-5L", "Engine oil 5W-30, 5 L", "can", 21.95m),
            ("CBL-CAT6-305", "Cat6 cable drum 305 m", "drum", 96.00m),
            ("GLV-NIT-L", "Nitrile gloves, L, box 100", "box", 6.30m),
            ("TAP-PVC-50", "PVC tape 50 mm x 66 m", "roll", 1.15m),
            ("FLT-AIR-220", "Air filter 220 mm", "ea", 14.80m),
            ("SCR-TX20-30", "Torx screw TX20x30", "ea", 0.05m),
            ("LBL-THERM-100", "Thermal label 100x150, roll 500", "roll", 8.90m),
            ("STR-WRAP-23", "Stretch wrap 23 um, 300 m", "roll", 4.20m),
        };
        var reasons = new[] { AdjustmentReason.CycleCount, AdjustmentReason.Damage, AdjustmentReason.Shrinkage, AdjustmentReason.Return, AdjustmentReason.Correction };
        var statuses = new[] { AdjustmentStatus.Posted, AdjustmentStatus.Posted, AdjustmentStatus.Posted, AdjustmentStatus.PendingApproval, AdjustmentStatus.Draft, AdjustmentStatus.Rejected };
        var users = new[] { "m.okafor", "j.lindqvist", "r.patel", "s.hauser", "a.dupont" };
        var aisles = new[] { "A", "B", "C", "D", "E" };
        var rng = new Random(20240517);
        var id = 10_413;
        while (_all.Count < targetTotal)
        {
            var (sku, description, unit, cost) = skus[rng.Next(skus.Length)];
            var before = rng.Next(4, 14_000);
            var delta = rng.Next(0, 5) == 0 ? rng.Next(1, 260) : -rng.Next(1, Math.Min(before, 40) + 1);
            _all.Add(new(
                $"ADJ-{id}",
                sku,
                description,
                $"{aisles[rng.Next(aisles.Length)]}-{rng.Next(1, 10):00}-{rng.Next(1, 16):00}",
                reasons[rng.Next(reasons.Length)],
                before,
                delta,
                unit,
                cost,
                statuses[rng.Next(statuses.Length)],
                users[rng.Next(users.Length)],
                now.AddMinutes(-rng.Next(4 * 60, 130 * 24 * 60))));
            id--;
        }
    }

    private void ApplyFilters()
    {
        var selectedId = Selected?.Id;
        IEnumerable<StockAdjustment> q = _all;
        if (!string.IsNullOrWhiteSpace(SearchText))
        {
            var s = SearchText.Trim();
            q = q.Where(a => a.Id.Contains(s, StringComparison.OrdinalIgnoreCase)
                          || a.Sku.Contains(s, StringComparison.OrdinalIgnoreCase)
                          || a.Description.Contains(s, StringComparison.OrdinalIgnoreCase));
        }
        if (!string.IsNullOrWhiteSpace(LocationFilter))
            q = q.Where(a => a.Location.StartsWith(LocationFilter.Trim(), StringComparison.OrdinalIgnoreCase));
        if (StatusFilter is { } st)
            q = q.Where(a => a.Status == st);
        var result = ApplySort(q);

        // One Reset instead of 1 + n notifications: the grid re-realises only the visible rows.
        FilteredItems.Reset(result);

        // Never lose selection on refresh: re-select by key.
        Selected = selectedId is null ? null : result.Find(a => a.Id == selectedId);
        OnPropertyChanged(nameof(ResultSummary));
        OnPropertyChanged(nameof(HasActiveFilters));
        OnPropertyChanged(nameof(EmptyTitle));
        OnPropertyChanged(nameof(EmptyBody));
        OnPropertyChanged(nameof(EmptyActionLabel));
        OnPropertyChanged(nameof(EmptyActionCommand));
    }

    /// <summary>
    /// Sorting 3,000 rows through a <c>Func&lt;T, object&gt;</c> key boxed every decimal and enum on
    /// every comparison. A typed <see cref="Comparison{T}"/> on a materialised list sorts in place
    /// with no allocation per comparison.
    /// </summary>
    private List<StockAdjustment> ApplySort(IEnumerable<StockAdjustment> q)
    {
        var list = q as List<StockAdjustment> ?? q.ToList();
        Comparison<StockAdjustment> cmp = _sortKey switch
        {
            "Status" => static (a, b) => a.Status.CompareTo(b.Status),
            "Id" => static (a, b) => string.CompareOrdinal(a.Id, b.Id),
            "Sku" => static (a, b) => string.CompareOrdinal(a.Sku, b.Sku),
            "Description" => static (a, b) => string.CompareOrdinal(a.Description, b.Description),
            "Location" => static (a, b) => string.CompareOrdinal(a.Location, b.Location),
            "Reason" => static (a, b) => a.Reason.CompareTo(b.Reason),
            "QuantityBefore" => static (a, b) => a.QuantityBefore.CompareTo(b.QuantityBefore),
            "QuantityDelta" => static (a, b) => a.QuantityDelta.CompareTo(b.QuantityDelta),
            "QuantityAfter" => static (a, b) => a.QuantityAfter.CompareTo(b.QuantityAfter),
            "ValueImpact" => static (a, b) => a.ValueImpact.CompareTo(b.ValueImpact),
            "CreatedBy" => static (a, b) => string.CompareOrdinal(a.CreatedBy, b.CreatedBy),
            _ => static (a, b) => a.CreatedAt.CompareTo(b.CreatedAt),
        };
        var descending = _sortDescending || _sortKey is null;
        list.Sort(descending ? (a, b) => cmp(b, a) : cmp);
        return list;
    }

    public void Sort(string key, bool descending)
    {
        _sortKey = key;
        _sortDescending = descending;
        ApplyFilters();
    }

    [RelayCommand] private void NewAdjustment() { }
    [RelayCommand] private void Refresh() => Load();
    [RelayCommand] private void ClearFilters() { SearchText = null; LocationFilter = null; StatusFilter = null; }
    [RelayCommand] private void Edit(StockAdjustment? item) { }

    [RelayCommand]
    private void Approve(StockAdjustment? item)
    {
        if (item is not { IsActionable: true }) return;
        Replace(item, item with { Status = AdjustmentStatus.Posted });
        Notify(InfoBarSeverity.Success, $"{item.Id} approved and posted.");
    }

    [RelayCommand]
    private void Reject(StockAdjustment? item)
    {
        if (item is not { IsActionable: true }) return;
        Replace(item, item with { Status = AdjustmentStatus.Rejected });
        Notify(InfoBarSeverity.Informational, $"{item.Id} rejected.");
    }

    /// <summary>
    /// InfoBar raises its screen-reader notification only on the closed-to-open transition and IsOpen is bound
    /// one-way to HasMessage, so a second message (or one after the user closed the bar) must toggle HasMessage
    /// false then true; otherwise it is neither announced nor, after a manual close, shown at all.
    /// </summary>
    private void Notify(InfoBarSeverity severity, string text)
    {
        Message = null;
        MessageSeverity = severity;
        Message = text;
    }

    private void Replace(StockAdjustment oldItem, StockAdjustment newItem)
    {
        var i = _all.IndexOf(oldItem);
        if (i >= 0) _all[i] = newItem;
        _pendingCount = _all.Count(a => a.Status == AdjustmentStatus.PendingApproval);
        ApplyFilters();
    }
}

public sealed record ShortcutInfo(string Keys, string Description);
