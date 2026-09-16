using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Windows.Data;
using System.Windows.Input;
using ErpClient.Models;

namespace ErpClient.ViewModels;

public enum LoadState { Loading, Ready, Empty, Error }

/// <summary>Screen state for the PO lines grid: rows, selection, totals, load state, and the commands the toolbar / menu / context menu share.</summary>
public sealed class PurchaseOrderLinesViewModel : ObservableObject
{
    private LoadState _state = LoadState.Loading;
    private string _errorMessage = "";
    private string _filterText = "";
    private string _statusMessage = "Ready";
    private string _focusedError = "";
    private int _hiddenColumnCount;
    private bool _simulateFailure;

    public PurchaseOrderLinesViewModel()
    {
        Lines = new ObservableCollection<PurchaseOrderLine>();
        Lines.CollectionChanged += OnLinesChanged;
        SelectedLines = new ObservableCollection<PurchaseOrderLine>();
        SelectedLines.CollectionChanged += (_, _) => { OnPropertyChanged(nameof(SelectedCount)); OnPropertyChanged(nameof(HasSelection)); OnPropertyChanged(nameof(SelectionSummary)); };

        LinesView = CollectionViewSource.GetDefaultView(Lines);
        LinesView.Filter = o => string.IsNullOrWhiteSpace(FilterText) || o is PurchaseOrderLine l && Matches(l, FilterText);

        AddLineCommand = new RelayCommand(_ => AddLine(), _ => State is LoadState.Ready or LoadState.Empty);
        DuplicateCommand = new RelayCommand(_ => Duplicate(), _ => HasSelection);
        DeleteCommand = new RelayCommand(_ => Delete(), _ => HasSelection);
        SetStatusCommand = new RelayCommand(p => SetStatus(p), _ => HasSelection);
        SetWarehouseCommand = new RelayCommand(p => SetWarehouse(p), _ => HasSelection);
        ClearFilterCommand = new RelayCommand(_ => FilterText = "", _ => !string.IsNullOrEmpty(FilterText));
        ReloadCommand = new RelayCommand(_ => _ = LoadAsync(), _ => State != LoadState.Loading);
        SaveCommand = new RelayCommand(_ => Save(), _ => DirtyCount > 0 && ErrorCount == 0);
        UndoDeleteCommand = new RelayCommand(_ => UndoDelete(), _ => _lastDeleted.Count > 0);
        NextErrorCommand = new RelayCommand(_ => NavigateToError?.Invoke(false), _ => ErrorCount > 0);
        PreviousErrorCommand = new RelayCommand(_ => NavigateToError?.Invoke(true), _ => ErrorCount > 0);
    }

    // ---- data -----------------------------------------------------------------

    public string OrderNumber => "PO-2026-004417";
    public string Supplier => "Al Futtaim Building Materials LLC";
    public string Currency => "AED";

    public ObservableCollection<PurchaseOrderLine> Lines { get; }
    public ICollectionView LinesView { get; }
    public ObservableCollection<PurchaseOrderLine> SelectedLines { get; }

    public IReadOnlyList<string> Units => PurchaseOrderLine.Units;
    public IReadOnlyList<string> Warehouses => PurchaseOrderLine.Warehouses;
    public IReadOnlyList<LineStatus> Statuses => Enum.GetValues<LineStatus>();

    // ---- state ----------------------------------------------------------------

    public LoadState State
    {
        get => _state;
        private set
        {
            if (Set(ref _state, value))
            {
                OnPropertyChanged(nameof(IsLoading)); OnPropertyChanged(nameof(IsEmpty));
                OnPropertyChanged(nameof(IsError)); OnPropertyChanged(nameof(IsReady));
                OnPropertyChanged(nameof(ShowGrid));
            }
        }
    }
    public bool IsLoading => State == LoadState.Loading;
    public bool IsEmpty => State == LoadState.Empty;
    public bool IsError => State == LoadState.Error;
    public bool IsReady => State == LoadState.Ready;
    /// <summary>The grid (with its header) stays visible in the empty and loading states so the columns are discoverable; only the error state replaces it.</summary>
    public bool ShowGrid => State != LoadState.Error;

    public string ErrorMessage { get => _errorMessage; private set => Set(ref _errorMessage, value); }
    public string StatusMessage { get => _statusMessage; set => Set(ref _statusMessage, value); }

    /// <summary>Validation message of the focused row/cell ("Line 50: Quantity must be greater than 0."), set by the view; empty when the focused row is valid.</summary>
    public string FocusedError { get => _focusedError; set => Set(ref _focusedError, value); }

    /// <summary>Installed by the view: moves focus to the next (or previous) cell with an error. Returns false when there is none.</summary>
    public Func<bool, bool>? NavigateToError { get; set; }

    /// <summary>Set by the view when it hides low-priority columns for a narrow window, so the status bar can say so.</summary>
    public int HiddenColumnCount { get => _hiddenColumnCount; set { if (Set(ref _hiddenColumnCount, value)) OnPropertyChanged(nameof(HiddenColumnsText)); } }
    public string HiddenColumnsText => HiddenColumnCount == 0 ? "" : $"{HiddenColumnCount} column{(HiddenColumnCount == 1 ? "" : "s")} hidden (View › Columns)";

    public string FilterText
    {
        get => _filterText;
        set { if (Set(ref _filterText, value)) { LinesView.Refresh(); OnPropertyChanged(nameof(VisibleCount)); OnPropertyChanged(nameof(CountSummary)); } }
    }

    /// <summary>Test hook: make the next load fail so the error state can be rendered.</summary>
    public bool SimulateFailure { get => _simulateFailure; set => Set(ref _simulateFailure, value); }

    // ---- derived --------------------------------------------------------------

    public int LineCount => Lines.Count;
    public int VisibleCount => LinesView.Cast<object>().Count();
    public int SelectedCount => SelectedLines.Count;
    public bool HasSelection => SelectedLines.Count > 0;
    public int ErrorCount => Lines.Count(l => l.HasErrors);
    public int DirtyCount => Lines.Count(l => l.IsDirty);
    public decimal Subtotal => Lines.Sum(l => l.NetAmount);
    public decimal TaxTotal => Lines.Sum(l => l.TaxAmount);
    public decimal GrandTotal => Lines.Sum(l => l.LineTotal);

    public string CountSummary => string.IsNullOrWhiteSpace(FilterText)
        ? $"{LineCount} line{(LineCount == 1 ? "" : "s")}"
        : $"{VisibleCount} of {LineCount} lines match “{FilterText}”";
    public string SelectionSummary => SelectedCount == 0 ? "" : $"{SelectedCount} selected";
    public string ErrorSummary => ErrorCount == 0 ? "" : $"{ErrorCount} line{(ErrorCount == 1 ? "" : "s")} with errors";
    public string DirtySummary => DirtyCount == 0 ? "" : $"{DirtyCount} unsaved";

    // ---- commands -------------------------------------------------------------

    public ICommand AddLineCommand { get; }
    public ICommand DuplicateCommand { get; }
    public ICommand DeleteCommand { get; }
    public ICommand SetStatusCommand { get; }
    public ICommand SetWarehouseCommand { get; }
    public ICommand ClearFilterCommand { get; }
    public ICommand ReloadCommand { get; }
    public ICommand SaveCommand { get; }
    public ICommand UndoDeleteCommand { get; }
    public ICommand NextErrorCommand { get; }
    public ICommand PreviousErrorCommand { get; }

    private readonly List<(int index, PurchaseOrderLine line)> _lastDeleted = new();

    public async Task LoadAsync(int delayMs = 700, bool empty = false)
    {
        State = LoadState.Loading;
        StatusMessage = $"Loading lines for {OrderNumber}…";
        try
        {
            if (delayMs > 0) await Task.Delay(delayMs);
            if (SimulateFailure) throw new System.Net.Http.HttpRequestException("GET /api/purchase-orders/4417/lines → 503 Service Unavailable (gateway timeout after 30 s)");
            Lines.Clear();
            if (!empty) foreach (var l in SampleData.Lines()) Lines.Add(l);
            State = Lines.Count == 0 ? LoadState.Empty : LoadState.Ready;
            StatusMessage = Lines.Count == 0 ? "No lines yet" : "Ready";
        }
        catch (Exception ex)
        {
            ErrorMessage = ex.Message;
            State = LoadState.Error;
            StatusMessage = "Could not load lines";
        }
    }

    public PurchaseOrderLine AddLine(int? insertAt = null)
    {
        var line = new PurchaseOrderLine { LineNo = (Lines.Count == 0 ? 0 : Lines.Max(l => l.LineNo)) + 10, ItemCode = "", Description = "" };
        line.Validate();
        if (insertAt is int i && i >= 0 && i < Lines.Count) Lines.Insert(i + 1, line); else Lines.Add(line);
        if (State == LoadState.Empty) State = LoadState.Ready;
        StatusMessage = $"Added line {line.LineNo}";
        return line;
    }

    private void Duplicate()
    {
        var src = SelectedLines.OrderBy(l => Lines.IndexOf(l)).ToList();
        var maxNo = Lines.Max(l => l.LineNo);
        foreach (var s in src)
        {
            maxNo += 10;
            var copy = new PurchaseOrderLine
            {
                LineNo = maxNo, ItemCode = s.ItemCode, Description = s.Description, Quantity = s.Quantity, Unit = s.Unit,
                UnitPrice = s.UnitPrice, DiscountPct = s.DiscountPct, TaxPct = s.TaxPct, Warehouse = s.Warehouse,
                RequestedDate = s.RequestedDate, Status = LineStatus.Draft, Notes = s.Notes,
            };
            copy.Validate();
            Lines.Add(copy);
        }
        StatusMessage = $"Duplicated {src.Count} line{(src.Count == 1 ? "" : "s")}";
    }

    private void Delete()
    {
        _lastDeleted.Clear();
        foreach (var l in SelectedLines.OrderByDescending(l => Lines.IndexOf(l)).ToList())
        {
            _lastDeleted.Add((Lines.IndexOf(l), l));
            Lines.Remove(l);
        }
        SelectedLines.Clear();
        if (Lines.Count == 0) State = LoadState.Empty;
        StatusMessage = $"Deleted {_lastDeleted.Count} line{(_lastDeleted.Count == 1 ? "" : "s")} — Ctrl+Z to undo";
    }

    private void UndoDelete()
    {
        foreach (var (index, line) in _lastDeleted.OrderBy(t => t.index))
            Lines.Insert(Math.Min(index, Lines.Count), line);
        StatusMessage = $"Restored {_lastDeleted.Count} line{(_lastDeleted.Count == 1 ? "" : "s")}";
        _lastDeleted.Clear();
        if (Lines.Count > 0) State = LoadState.Ready;
    }

    private void SetStatus(object? p)
    {
        if (p is not LineStatus s && !(p is string str && Enum.TryParse(str, out s))) return;
        foreach (var l in SelectedLines) l.Status = s;
        StatusMessage = $"Set {SelectedLines.Count} line{(SelectedLines.Count == 1 ? "" : "s")} to {s}";
        RaiseTotals();
    }

    private void SetWarehouse(object? p)
    {
        if (p is not string wh) return;
        foreach (var l in SelectedLines) l.Warehouse = wh;
        StatusMessage = $"Moved {SelectedLines.Count} line{(SelectedLines.Count == 1 ? "" : "s")} to {wh}";
        RaiseTotals();
    }

    private void Save()
    {
        foreach (var l in Lines) l.AcceptChanges();
        StatusMessage = $"Saved {LineCount} lines to {OrderNumber}";
        RaiseTotals();
    }

    // ---- plumbing -------------------------------------------------------------

    private static bool Matches(PurchaseOrderLine l, string q)
    {
        var c = StringComparison.OrdinalIgnoreCase;
        return l.ItemCode.Contains(q, c) || l.Description.Contains(q, c) || l.Warehouse.Contains(q, c)
               || l.Status.ToString().Contains(q, c) || l.Notes.Contains(q, c);
    }

    private void OnLinesChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (e.OldItems != null) foreach (PurchaseOrderLine l in e.OldItems) Detach(l);
        if (e.NewItems != null) foreach (PurchaseOrderLine l in e.NewItems) Attach(l);
        if (e.Action == NotifyCollectionChangedAction.Reset) foreach (var l in Lines) Attach(l);
        RaiseTotals();
    }

    private void Attach(PurchaseOrderLine l) { l.TotalsChanged -= OnLineTotals; l.TotalsChanged += OnLineTotals; l.ErrorsChanged -= OnLineErrors; l.ErrorsChanged += OnLineErrors; l.PropertyChanged -= OnLineProp; l.PropertyChanged += OnLineProp; }
    private void Detach(PurchaseOrderLine l) { l.TotalsChanged -= OnLineTotals; l.ErrorsChanged -= OnLineErrors; l.PropertyChanged -= OnLineProp; }
    private void OnLineTotals(object? s, EventArgs e) => RaiseTotals();
    private void OnLineErrors(object? s, DataErrorsChangedEventArgs e) { OnPropertyChanged(nameof(ErrorCount)); OnPropertyChanged(nameof(ErrorSummary)); }
    private void OnLineProp(object? s, PropertyChangedEventArgs e) { if (e.PropertyName == nameof(PurchaseOrderLine.IsDirty)) { OnPropertyChanged(nameof(DirtyCount)); OnPropertyChanged(nameof(DirtySummary)); } }

    private void RaiseTotals()
    {
        foreach (var n in new[] { nameof(LineCount), nameof(VisibleCount), nameof(CountSummary), nameof(ErrorCount), nameof(ErrorSummary),
                                  nameof(DirtyCount), nameof(DirtySummary), nameof(Subtotal), nameof(TaxTotal), nameof(GrandTotal) })
            OnPropertyChanged(n);
    }
}
