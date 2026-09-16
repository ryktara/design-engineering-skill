using System.Collections;
using System.ComponentModel;
using ErpClient.ViewModels;

namespace ErpClient.Models;

public enum LineStatus { Draft, Approved, Ordered, PartiallyReceived, Received, Cancelled }

/// <summary>One purchase-order line. Validation is per cell (INotifyDataErrorInfo) so the grid can mark the cell and the status bar can count errors.</summary>
public sealed class PurchaseOrderLine : ObservableObject, INotifyDataErrorInfo
{
    public static readonly string[] Units = ["EA", "BOX", "KG", "L", "M", "PK", "ROLL"];
    public static readonly string[] Warehouses = ["DXB-01 Main", "DXB-02 Cold", "AUH-01", "SHJ-Bulk", "RUH-01"];

    private readonly Dictionary<string, List<string>> _errors = new();

    private int _lineNo;
    private string _itemCode = "";
    private string _description = "";
    private decimal _quantity = 1;
    private string _unit = "EA";
    private decimal _unitPrice;
    private decimal _discountPct;
    private decimal _taxPct = 5;
    private string _warehouse = Warehouses[0];
    private DateTime? _requestedDate = DateTime.Today.AddDays(7);
    private LineStatus _status = LineStatus.Draft;
    private string _notes = "";
    private bool _isDirty;

    public int LineNo { get => _lineNo; set => Set(ref _lineNo, value); }

    public string ItemCode
    {
        get => _itemCode;
        set { if (Set(ref _itemCode, value?.Trim().ToUpperInvariant() ?? "")) { Validate(); Touch(); } }
    }

    public string Description
    {
        get => _description;
        set { if (Set(ref _description, value ?? "")) { Validate(); Touch(); } }
    }

    public decimal Quantity
    {
        get => _quantity;
        set { if (Set(ref _quantity, value)) { Validate(); Recalc(); } }
    }

    public string Unit
    {
        get => _unit;
        set { if (Set(ref _unit, value ?? "EA")) { Validate(); Touch(); } }
    }

    public decimal UnitPrice
    {
        get => _unitPrice;
        set { if (Set(ref _unitPrice, value)) { Validate(); Recalc(); } }
    }

    public decimal DiscountPct
    {
        get => _discountPct;
        set { if (Set(ref _discountPct, value)) { Validate(); Recalc(); } }
    }

    public decimal TaxPct
    {
        get => _taxPct;
        set { if (Set(ref _taxPct, value)) { Validate(); Recalc(); } }
    }

    public string Warehouse
    {
        get => _warehouse;
        set { if (Set(ref _warehouse, value ?? "")) { Validate(); Touch(); } }
    }

    public DateTime? RequestedDate
    {
        get => _requestedDate;
        set { if (Set(ref _requestedDate, value)) { Validate(); Touch(); } }
    }

    public LineStatus Status
    {
        get => _status;
        set { if (Set(ref _status, value)) Touch(); }
    }

    public string Notes
    {
        get => _notes;
        set { if (Set(ref _notes, value ?? "")) Touch(); }
    }

    /// <summary>Net of discount, before tax.</summary>
    public decimal NetAmount => Math.Round(Quantity * UnitPrice * (1 - DiscountPct / 100m), 2);
    public decimal TaxAmount => Math.Round(NetAmount * TaxPct / 100m, 2);
    public decimal LineTotal => NetAmount + TaxAmount;

    public bool IsDirty { get => _isDirty; private set => Set(ref _isDirty, value); }
    public void AcceptChanges() => IsDirty = false;

    private void Touch() => IsDirty = true;

    private void Recalc()
    {
        OnPropertyChanged(nameof(NetAmount));
        OnPropertyChanged(nameof(TaxAmount));
        OnPropertyChanged(nameof(LineTotal));
        Touch();
        TotalsChanged?.Invoke(this, EventArgs.Empty);
    }

    public event EventHandler? TotalsChanged;

    // ---- INotifyDataErrorInfo -------------------------------------------------

    public bool HasErrors => _errors.Count > 0;
    public event EventHandler<DataErrorsChangedEventArgs>? ErrorsChanged;

    public IEnumerable GetErrors(string? propertyName)
        => propertyName is not null && _errors.TryGetValue(propertyName, out var list) ? list : Array.Empty<string>();

    public IEnumerable<string> AllErrors => _errors.SelectMany(kv => kv.Value.Select(m => $"{kv.Key}: {m}"));

    public void Validate()
    {
        var before = _errors.Keys.ToList();
        _errors.Clear();

        if (string.IsNullOrWhiteSpace(ItemCode)) Add(nameof(ItemCode), "Item is required.");
        else if (ItemCode.Length is < 4 or > 20) Add(nameof(ItemCode), "Item code is 4–20 characters.");
        if (string.IsNullOrWhiteSpace(Description)) Add(nameof(Description), "Description is required.");
        if (Quantity <= 0) Add(nameof(Quantity), "Quantity must be greater than 0.");
        if (Quantity > 1_000_000) Add(nameof(Quantity), "Quantity above 1,000,000 needs a separate order.");
        if (!Units.Contains(Unit)) Add(nameof(Unit), $"Unit must be one of {string.Join(", ", Units)}.");
        if (UnitPrice < 0) Add(nameof(UnitPrice), "Unit price cannot be negative.");
        if (DiscountPct is < 0 or > 100) Add(nameof(DiscountPct), "Discount is 0–100 %.");
        if (TaxPct is < 0 or > 50) Add(nameof(TaxPct), "Tax rate is 0–50 %.");
        if (string.IsNullOrWhiteSpace(Warehouse)) Add(nameof(Warehouse), "Warehouse is required.");
        if (RequestedDate is null) Add(nameof(RequestedDate), "Requested date is required.");
        else if (RequestedDate.Value.Date < DateTime.Today) Add(nameof(RequestedDate), "Requested date is in the past.");

        foreach (var key in before.Union(_errors.Keys).Distinct())
            ErrorsChanged?.Invoke(this, new DataErrorsChangedEventArgs(key));
        OnPropertyChanged(nameof(HasErrors));
        OnPropertyChanged(nameof(AllErrors));
        OnPropertyChanged(nameof(ErrorSummary));
    }

    public string ErrorSummary => string.Join(Environment.NewLine, _errors.SelectMany(kv => kv.Value));

    private void Add(string prop, string message)
    {
        if (!_errors.TryGetValue(prop, out var list)) _errors[prop] = list = new List<string>();
        list.Add(message);
    }
}
