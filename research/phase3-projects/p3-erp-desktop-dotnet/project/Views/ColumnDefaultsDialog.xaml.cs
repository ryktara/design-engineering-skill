using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using ErpClient.Models;
using ErpClient.ViewModels;

namespace ErpClient.Views;

/// <summary>One row of the "Columns shown" list.</summary>
public sealed class ColumnChoice : ObservableObject
{
    private bool _isShown;
    public required string Key { get; init; }
    public required string Label { get; init; }
    /// <summary>Essential columns (no HideBelow rule) cannot be hidden; the box is ticked and disabled with a hint that says so.</summary>
    public bool CanHide { get; init; } = true;
    public bool IsShown { get => _isShown; set => Set(ref _isShown, value); }
    public string Hint => CanHide ? $"Untick to keep the {Label} column hidden" : "Essential column: cannot be hidden";
}

/// <summary>
/// Owned modal settings dialog for the lines window. Works on a copy of the defaults; OK returns the edited copy through
/// <see cref="Result"/>, Cancel / Escape leave the caller's settings untouched.
/// </summary>
public partial class ColumnDefaultsDialog : Window
{
    private readonly ColumnDefaults _draft;

    public ColumnDefaultsDialog(Window owner, ColumnDefaults current, IReadOnlyList<string> warehouses, IEnumerable<(string key, string label, bool canHide)> columns)
    {
        InitializeComponent();
        Owner = owner;
        _draft = current.Clone();
        WarehouseBox.ItemsSource = warehouses;
        WarehouseBox.SelectedItem = warehouses.Contains(_draft.DefaultWarehouse) ? _draft.DefaultWarehouse : warehouses[0];
        Choices = columns.Select(c => new ColumnChoice { Key = c.key, Label = c.canHide ? c.label : c.label + "  (always shown)", CanHide = c.canHide, IsShown = !c.canHide || !_draft.HiddenColumns.Contains(c.key) }).ToList();
        ColumnList.ItemsSource = Choices;
        // First meaningful control gets focus on open (the rule in the dialog guardrail); Enter = OK, Escape = Cancel via IsDefault / IsCancel.
        Loaded += (_, _) => { WarehouseBox.Focus(); Keyboard.Focus(WarehouseBox); };
    }

    public List<ColumnChoice> Choices { get; }
    public ColumnDefaults? Result { get; private set; }

    private void OnOk(object sender, RoutedEventArgs e)
    {
        _draft.DefaultWarehouse = WarehouseBox.SelectedItem as string ?? _draft.DefaultWarehouse;
        _draft.HiddenColumns = Choices.Where(c => c.CanHide && !c.IsShown).Select(c => c.Key).ToList();
        Result = _draft;
        DialogResult = true;
    }

    private void OnRestore(object sender, RoutedEventArgs e)
    {
        var fresh = new ColumnDefaults();
        WarehouseBox.SelectedItem = fresh.DefaultWarehouse;
        foreach (var c in Choices) c.IsShown = true;
        WarehouseBox.Focus();
    }
}
