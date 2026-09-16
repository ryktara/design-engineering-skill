using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Erp.Client.Models;
using Microsoft.UI.Xaml.Controls;

namespace Erp.Client.ViewModels;

/// <summary>
/// Supplier invoice matching: invoices awaiting a three-way match on the left, the selected
/// invoice's lines against the purchase order and goods receipt on the right.
/// Every command is reachable from the command bar, the row context menu and an accelerator,
/// so the screen is fully operable without a pointer.
/// </summary>
public sealed partial class InvoiceMatchingViewModel : ObservableObject
{
    private readonly List<SupplierInvoice> _allInvoices = new();
    private readonly Dictionary<string, List<InvoiceMatchLine>> _linesByInvoice = new(StringComparer.OrdinalIgnoreCase);
    private string? _sortKey;
    private bool _sortDescending;

    public BulkObservableCollection<SupplierInvoice> FilteredInvoices { get; } = new();

    /// <summary>
    /// Also a BulkObservableCollection: the detail grid is refilled on every selection change, and the
    /// page binds its visibility and empty state to Count. Clear() + n * Add() pushes n+1 notifications
    /// and leaves the grid flickering through an empty state on every arrow-key move down the master list.
    /// </summary>
    public BulkObservableCollection<InvoiceMatchLine> MatchLines { get; } = new();

    public IReadOnlyList<MatchStatus?> StatusOptions { get; } =
        new MatchStatus?[] { null, MatchStatus.Unmatched, MatchStatus.PriceVariance, MatchStatus.QuantityVariance, MatchStatus.Matched, MatchStatus.OnHold };

    [ObservableProperty] private string? _searchText;
    [ObservableProperty] private MatchStatus? _statusFilter;
    [ObservableProperty] private SupplierInvoice? _selectedInvoice;
    [ObservableProperty] private InvoiceMatchLine? _selectedLine;
    [ObservableProperty] private bool _isLoading;
    [ObservableProperty] private string? _message;
    [ObservableProperty] private InfoBarSeverity _messageSeverity = InfoBarSeverity.Informational;

    public bool HasMessage => !string.IsNullOrEmpty(Message);
    public bool HasActiveFilters => !string.IsNullOrWhiteSpace(SearchText) || StatusFilter is not null;
    public bool CanMatchSelected => SelectedInvoice is { IsActionable: true };
    public bool CanActOnLine => SelectedLine is { IsActionable: true };

    /// <summary>Named next to the commands so the user always knows what the commands will act on.</summary>
    public string SelectionLabel => SelectedInvoice is { } inv
        ? $"Selected: {inv.InvoiceNumber} · {inv.Supplier}"
        : "No invoice selected";

    /// <summary>
    /// Carries the invoice total as well: the master list is 320 epx wide and only shows status,
    /// identity and variance, so the total lives here next to the lines it is made of.
    /// </summary>
    public string LinesTitle => SelectedInvoice is { } inv
        ? $"Match lines · {inv.InvoiceNumber} against {inv.PurchaseOrder} · {inv.InvoiceTotal:N2} {inv.Currency} invoiced"
        : "Match lines";

    public string ResultSummary => HasActiveFilters
        ? $"{FilteredInvoices.Count:N0} of {_allInvoices.Count:N0} invoices match the current filters"
        : $"{_allInvoices.Count:N0} supplier invoices, {_allInvoices.Count(i => i.IsActionable):N0} awaiting matching";

    public string EmptyTitle => HasActiveFilters ? "No invoices match" : "No supplier invoices";
    public string EmptyBody => HasActiveFilters
        ? "Try a broader search or clear the filters to see every invoice."
        : "Invoices appear here once the supplier has submitted them against a purchase order.";
    public string EmptyActionLabel => HasActiveFilters ? "Clear filters" : "Refresh";
    public IRelayCommand EmptyActionCommand => HasActiveFilters ? ClearFiltersCommand : RefreshCommand;

    public string LinesEmptyBody => SelectedInvoice is null
        ? "Select an invoice on the left to see its lines."
        : "This invoice has no lines to match.";

    /// <summary>Single source for the F1 reference; keep in sync with the KeyboardAccelerators in the page.</summary>
    public IReadOnlyList<ShortcutInfo> Shortcuts { get; } = new[]
    {
        new ShortcutInfo("Ctrl+M", "Match the selected invoice"),
        new ShortcutInfo("Ctrl+Shift+A", "Accept the variance on the selected line"),
        new ShortcutInfo("Ctrl+H", "Put the selected invoice on hold"),
        new ShortcutInfo("F5", "Refresh (selection is kept)"),
        new ShortcutInfo("Ctrl+F", "Go to search"),
        new ShortcutInfo("Esc", "Clear the search text (in the search box)"),
        new ShortcutInfo("Ctrl+Shift+L", "Clear all filters"),
        new ShortcutInfo("F6 / Shift+F6", "Move between commands, filters, invoices and match lines"),
        new ShortcutInfo("↑ ↓ Home End", "Move between rows inside a table"),
        new ShortcutInfo("Shift+F10", "Open the row context menu"),
        new ShortcutInfo("Alt", "Show access keys for the commands"),
        new ShortcutInfo("F1", "This list"),
    };

    public InvoiceMatchingViewModel() => Load();

    partial void OnSearchTextChanged(string? value) => ApplyFilters();
    partial void OnStatusFilterChanged(MatchStatus? value) => ApplyFilters();
    partial void OnMessageChanged(string? value) => OnPropertyChanged(nameof(HasMessage));

    partial void OnSelectedInvoiceChanged(SupplierInvoice? value)
    {
        OnPropertyChanged(nameof(CanMatchSelected));
        OnPropertyChanged(nameof(SelectionLabel));
        OnPropertyChanged(nameof(LinesTitle));
        OnPropertyChanged(nameof(LinesEmptyBody));
        MatchCommand.NotifyCanExecuteChanged();
        HoldCommand.NotifyCanExecuteChanged();
        LoadLines(value);
    }

    partial void OnSelectedLineChanged(InvoiceMatchLine? value)
    {
        OnPropertyChanged(nameof(CanActOnLine));
        AcceptVarianceCommand.NotifyCanExecuteChanged();
    }

    private void LoadLines(SupplierInvoice? invoice)
    {
        SelectedLine = null;
        if (invoice is null || !_linesByInvoice.TryGetValue(invoice.InvoiceNumber, out var lines))
        {
            MatchLines.Reset(Array.Empty<InvoiceMatchLine>());
            return;
        }
        MatchLines.Reset(lines);
        SelectedLine = MatchLines.FirstOrDefault();
    }

    private void Load()
    {
        _allInvoices.Clear();
        _linesByInvoice.Clear();
        var today = DateTimeOffset.Now.Date;

        void Add(SupplierInvoice invoice, params InvoiceMatchLine[] lines)
        {
            _allInvoices.Add(invoice);
            _linesByInvoice[invoice.InvoiceNumber] = lines.ToList();
        }

        Add(new("SI-88214", "Nordfast AB", "PO-40217", today.AddDays(-4), today.AddDays(26), "EUR", 4_218.60m, 4_092.00m, MatchStatus.PriceVariance),
            new("10", "BLT-M8-40", "Hex bolt M8x40 zinc", 12_000m, 12_000m, "ea", 0.090m, 0.080m, MatchStatus.PriceVariance),
            new("20", "SCR-TX20-30", "Torx screw TX20x30", 40_000m, 40_000m, "ea", 0.055m, 0.050m, MatchStatus.PriceVariance),
            new("30", "PLT-0032", "Euro pallet, heat treated", 60m, 60m, "ea", 12.40m, 12.40m, MatchStatus.Matched));

        Add(new("SI-88209", "Rheinöl GmbH", "PO-40203", today.AddDays(-6), today.AddDays(24), "EUR", 2_195.00m, 2_414.50m, MatchStatus.QuantityVariance),
            new("10", "OIL-5W30-5L", "Engine oil 5W-30, 5 L", 100m, 110m, "can", 21.95m, 21.95m, MatchStatus.QuantityVariance));

        Add(new("SI-88198", "Cabletech Ltd", "PO-40188", today.AddDays(-9), today.AddDays(21), "EUR", 9_600.00m, 9_600.00m, MatchStatus.Matched),
            new("10", "CBL-CAT6-305", "Cat6 cable drum 305 m", 100m, 100m, "drum", 96.00m, 96.00m, MatchStatus.Matched));

        Add(new("SI-88186", "Safehands BV", "PO-40171", today.AddDays(-12), today.AddDays(18), "EUR", 1_260.00m, 0m, MatchStatus.Unmatched),
            new("10", "GLV-NIT-L", "Nitrile gloves, L, box 100", 200m, 0m, "box", 6.30m, 6.30m, MatchStatus.Unmatched));

        Add(new("SI-88174", "Adhesia SpA", "PO-40160", today.AddDays(-15), today.AddDays(15), "EUR", 1_173.00m, 1_150.00m, MatchStatus.OnHold),
            new("10", "TAP-PVC-50", "PVC tape 50 mm x 66 m", 1_020m, 1_000m, "roll", 1.15m, 1.15m, MatchStatus.OnHold));

        Add(new("SI-88160", "Filtrair NV", "PO-40144", today.AddDays(-19), today.AddDays(11), "EUR", 2_960.00m, 2_960.00m, MatchStatus.Matched),
            new("10", "FLT-AIR-220", "Air filter 220 mm", 200m, 200m, "ea", 14.80m, 14.80m, MatchStatus.Matched));

        ApplyFilters();
        SelectedInvoice = FilteredInvoices.FirstOrDefault();
    }

    private void ApplyFilters()
    {
        var selectedId = SelectedInvoice?.InvoiceNumber;
        IEnumerable<SupplierInvoice> q = _allInvoices;
        if (!string.IsNullOrWhiteSpace(SearchText))
        {
            var s = SearchText.Trim();
            q = q.Where(i => i.InvoiceNumber.Contains(s, StringComparison.OrdinalIgnoreCase)
                          || i.Supplier.Contains(s, StringComparison.OrdinalIgnoreCase)
                          || i.PurchaseOrder.Contains(s, StringComparison.OrdinalIgnoreCase));
        }
        if (StatusFilter is { } st) q = q.Where(i => i.Status == st);

        var result = ApplySort(q);
        FilteredInvoices.Reset(result);

        SelectedInvoice = selectedId is null ? null : result.Find(i => i.InvoiceNumber == selectedId);
        OnPropertyChanged(nameof(ResultSummary));
        OnPropertyChanged(nameof(HasActiveFilters));
        OnPropertyChanged(nameof(EmptyTitle));
        OnPropertyChanged(nameof(EmptyBody));
        OnPropertyChanged(nameof(EmptyActionLabel));
        OnPropertyChanged(nameof(EmptyActionCommand));
    }

    private List<SupplierInvoice> ApplySort(IEnumerable<SupplierInvoice> source)
    {
        var list = source.ToList();
        Comparison<SupplierInvoice>? comparison = _sortKey switch
        {
            "InvoiceNumber" => (a, b) => string.Compare(a.InvoiceNumber, b.InvoiceNumber, StringComparison.OrdinalIgnoreCase),
            "Supplier" => (a, b) => string.Compare(a.Supplier, b.Supplier, StringComparison.OrdinalIgnoreCase),
            "PurchaseOrder" => (a, b) => string.Compare(a.PurchaseOrder, b.PurchaseOrder, StringComparison.OrdinalIgnoreCase),
            "DueDate" => (a, b) => a.DueDate.CompareTo(b.DueDate),
            "InvoiceTotal" => (a, b) => a.InvoiceTotal.CompareTo(b.InvoiceTotal),
            "VarianceTotal" => (a, b) => a.VarianceTotal.CompareTo(b.VarianceTotal),
            "Status" => (a, b) => a.Status.CompareTo(b.Status),
            _ => null,
        };
        if (comparison is null) return list;
        list.Sort(comparison);
        if (_sortDescending) list.Reverse();
        return list;
    }

    public void Sort(string key, bool descending)
    {
        _sortKey = key;
        _sortDescending = descending;
        ApplyFilters();
    }

    private void Replace(SupplierInvoice invoice, MatchStatus status)
    {
        var index = _allInvoices.FindIndex(i => i.InvoiceNumber == invoice.InvoiceNumber);
        if (index < 0) return;
        _allInvoices[index] = invoice with { Status = status };
        ApplyFilters();
        SelectedInvoice = FilteredInvoices.FirstOrDefault(i => i.InvoiceNumber == invoice.InvoiceNumber);
    }

    [RelayCommand(CanExecute = nameof(CanMatchSelected))]
    private void Match(SupplierInvoice? invoice)
    {
        if (invoice is null) return;
        Replace(invoice, MatchStatus.Matched);
        MessageSeverity = InfoBarSeverity.Success;
        Message = $"{invoice.InvoiceNumber} matched against {invoice.PurchaseOrder}.";
    }

    [RelayCommand(CanExecute = nameof(CanMatchSelected))]
    private void Hold(SupplierInvoice? invoice)
    {
        if (invoice is null) return;
        Replace(invoice, MatchStatus.OnHold);
        MessageSeverity = InfoBarSeverity.Warning;
        Message = $"{invoice.InvoiceNumber} put on hold; the supplier has been notified.";
    }

    [RelayCommand(CanExecute = nameof(CanActOnLine))]
    private void AcceptVariance(InvoiceMatchLine? line)
    {
        if (line is null) return;
        var index = MatchLines.IndexOf(line);
        if (index < 0) return;
        var updated = line with { Status = MatchStatus.Matched };
        MatchLines[index] = updated;
        if (SelectedInvoice is { } inv && _linesByInvoice.TryGetValue(inv.InvoiceNumber, out var stored))
        {
            var si = stored.FindIndex(l => l.LineNumber == line.LineNumber);
            if (si >= 0) stored[si] = updated;
        }
        SelectedLine = updated;
        MessageSeverity = InfoBarSeverity.Informational;
        Message = $"Variance accepted on line {line.LineNumber} ({line.Sku}).";
    }

    [RelayCommand]
    private void Refresh()
    {
        var keep = SelectedInvoice?.InvoiceNumber;
        Load();
        SelectedInvoice = keep is null ? FilteredInvoices.FirstOrDefault() : FilteredInvoices.FirstOrDefault(i => i.InvoiceNumber == keep);
        MessageSeverity = InfoBarSeverity.Informational;
        Message = "Invoice list refreshed.";
    }

    [RelayCommand]
    private void ClearFilters()
    {
        SearchText = null;
        StatusFilter = null;
    }
}
