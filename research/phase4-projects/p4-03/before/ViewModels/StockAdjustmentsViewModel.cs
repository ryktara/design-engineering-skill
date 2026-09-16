using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Erp.Client.Models;
using Microsoft.UI.Xaml.Controls;

namespace Erp.Client.ViewModels;

public sealed partial class StockAdjustmentsViewModel : ObservableObject
{
    private readonly List<StockAdjustment> _all = new();
    private string? _sortKey;
    private bool _sortDescending;

    public ObservableCollection<StockAdjustment> FilteredItems { get; } = new();
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

    public string ResultSummary => HasActiveFilters
        ? $"{FilteredItems.Count} of {_all.Count} adjustments match the current filters"
        : $"{_all.Count} adjustments, {_all.Count(a => a.Status == AdjustmentStatus.PendingApproval)} pending approval";

    public string EmptyTitle => HasActiveFilters ? "No adjustments match" : "No stock adjustments yet";
    public string EmptyBody => HasActiveFilters
        ? "Try a broader search or clear the filters to see every adjustment."
        : "Adjustments record counted, damaged or returned stock. Create the first one to start.";
    public string EmptyActionLabel => HasActiveFilters ? "Clear filters" : "New adjustment";
    public IRelayCommand EmptyActionCommand => HasActiveFilters ? ClearFiltersCommand : NewAdjustmentCommand;

    public StockAdjustmentsViewModel()
    {
        Load();
    }

    partial void OnSearchTextChanged(string? value) => ApplyFilters();
    partial void OnLocationFilterChanged(string? value) => ApplyFilters();
    partial void OnStatusFilterChanged(AdjustmentStatus? value) => ApplyFilters();
    partial void OnSelectedChanged(StockAdjustment? value) => OnPropertyChanged(nameof(CanApproveSelected));
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
        ApplyFilters();
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
        q = ApplySort(q);

        FilteredItems.Clear();
        foreach (var a in q) FilteredItems.Add(a);

        // Never lose selection on refresh: re-select by key.
        Selected = FilteredItems.FirstOrDefault(a => a.Id == selectedId);
        OnPropertyChanged(nameof(ResultSummary));
        OnPropertyChanged(nameof(HasActiveFilters));
        OnPropertyChanged(nameof(EmptyTitle));
        OnPropertyChanged(nameof(EmptyBody));
        OnPropertyChanged(nameof(EmptyActionLabel));
        OnPropertyChanged(nameof(EmptyActionCommand));
    }

    private IEnumerable<StockAdjustment> ApplySort(IEnumerable<StockAdjustment> q)
    {
        Func<StockAdjustment, object> key = _sortKey switch
        {
            "Status" => a => a.Status,
            "Id" => a => a.Id,
            "Sku" => a => a.Sku,
            "Description" => a => a.Description,
            "Location" => a => a.Location,
            "Reason" => a => a.Reason,
            "QuantityBefore" => a => a.QuantityBefore,
            "QuantityDelta" => a => a.QuantityDelta,
            "QuantityAfter" => a => a.QuantityAfter,
            "ValueImpact" => a => a.ValueImpact,
            "CreatedBy" => a => a.CreatedBy,
            _ => a => a.CreatedAt,
        };
        return _sortDescending || _sortKey is null ? q.OrderByDescending(key) : q.OrderBy(key);
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
        MessageSeverity = InfoBarSeverity.Success;
        Message = $"{item.Id} approved and posted.";
    }

    [RelayCommand]
    private void Reject(StockAdjustment? item)
    {
        if (item is not { IsActionable: true }) return;
        Replace(item, item with { Status = AdjustmentStatus.Rejected });
        MessageSeverity = InfoBarSeverity.Informational;
        Message = $"{item.Id} rejected.";
    }

    private void Replace(StockAdjustment oldItem, StockAdjustment newItem)
    {
        var i = _all.IndexOf(oldItem);
        if (i >= 0) _all[i] = newItem;
        ApplyFilters();
    }
}
