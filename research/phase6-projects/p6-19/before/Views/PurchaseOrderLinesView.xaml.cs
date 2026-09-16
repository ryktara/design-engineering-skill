using System.Collections.Specialized;
using System.ComponentModel;
using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Input;
using System.Windows.Media;
using ErpClient.Models;
using ErpClient.ViewModels;

namespace ErpClient.Views;

public partial class PurchaseOrderLinesView : UserControl
{
    private bool _isEditing;
    // Set while a key handler moves focus itself, so the collection watcher does not fight it.
    private bool _focusHandledByCaller;
    private PurchaseOrderLinesViewModel? _watched;
    private readonly Dictionary<DataGridColumn, (double width, int index)> _defaultLayout = new();

    public PurchaseOrderLinesView()
    {
        InitializeComponent();
        Loaded += (_, _) =>
        {
            ApplyCurrencyHeaders();
            if (_defaultLayout.Count == 0)
                foreach (var c in LinesGrid.Columns) _defaultLayout[c] = (c.Width.Value, c.DisplayIndex);
            BuildColumnsMenu();
            ApplyColumnDefaults();
            ApplyColumnPriority();
            // Enum values for the status column; the others bind to VM lists in code because DataGridComboBoxColumn has no DataContext.
            if (DataContext is PurchaseOrderLinesViewModel vm)
            {
                ColUnit.ItemsSource = vm.Units;
                ColWarehouse.ItemsSource = vm.Warehouses;
                ColStatus.ItemsSource = vm.Statuses;
            }
        };
        DataContextChanged += (_, _) =>
        {
            if (_watched != null) _watched.Lines.CollectionChanged -= OnLinesCollectionChanged;
            if (DataContext is PurchaseOrderLinesViewModel vm)
            {
                ApplyCurrencyHeaders();
                ColUnit.ItemsSource = vm.Units;
                ColWarehouse.ItemsSource = vm.Warehouses;
                ColStatus.ItemsSource = vm.Statuses;
                vm.PropertyChanged += (_, e) =>
                {
                    if (e.PropertyName == nameof(vm.IsReady) && vm.IsReady) Dispatcher.BeginInvoke(FocusFirstCell);
                    // The empty state has to take focus too, or the keyboard has nowhere to go once the last line is deleted.
                    if (e.PropertyName == nameof(vm.IsEmpty) && vm.IsEmpty) Dispatcher.BeginInvoke(FocusEmptyState);
                    if (e.PropertyName == nameof(vm.ErrorCount)) UpdateFocusedError();
                };
                vm.NavigateToError = GoToError;
                _watched = vm;
                vm.Lines.CollectionChanged += OnLinesCollectionChanged;
            }
        };
        PreviewKeyDown += OnViewPreviewKeyDown;
    }

    private PurchaseOrderLinesViewModel? Vm => DataContext as PurchaseOrderLinesViewModel;
    public DataGrid Grid => LinesGrid;
    public bool IsEditing => _isEditing;

    /// <summary>Money columns carry the order currency in the header ("Unit price (AED)"): the unit belongs in the header, not in every cell,
    /// and it is the first thing that tells a quantity column and a price column apart.</summary>
    private void ApplyCurrencyHeaders()
    {
        if (Vm == null) return;
        ColPrice.Header = $"Unit price ({Vm.Currency})";
        ColTotal.Header = $"Line total ({Vm.Currency})";
    }

    // ---- focus ------------------------------------------------------------------

    public void FocusFirstCell()
    {
        if (LinesGrid.Items.Count == 0 || LinesGrid.Columns.Count == 0) return;
        FocusCell(0, ColItem);
    }

    public void FocusCell(int rowIndex, DataGridColumn column) => FocusCell(rowIndex, column, retry: true);

    private void FocusCell(int rowIndex, DataGridColumn column, bool retry)
    {
        if (rowIndex < 0 || rowIndex >= LinesGrid.Items.Count) return;
        var item = LinesGrid.Items[rowIndex];
        LinesGrid.CurrentCell = new DataGridCellInfo(item, column);
        LinesGrid.SelectedItem = item;
        LinesGrid.ScrollIntoView(item, column);
        LinesGrid.UpdateLayout();
        var cell = GetCell(rowIndex, column);
        if (cell != null) { cell.Focus(); Keyboard.Focus(cell); return; }
        // Right after a re-sort or a refresh the row container may not be realised yet; try again once the generator
        // has caught up, so focus is never left on nothing (the keyboard would be dead until the grid was clicked).
        LinesGrid.Focus();
        if (!retry) return;
        Dispatcher.BeginInvoke(new Action(() =>
        {
            var idx = LinesGrid.Items.IndexOf(item);
            if (idx < 0 || LinesGrid.Items.Count == 0) return;
            if (Keyboard.FocusedElement is DataGridCell) return;
            FocusCell(Math.Clamp(idx, 0, LinesGrid.Items.Count - 1), column, retry: false);
        }), System.Windows.Threading.DispatcherPriority.Loaded);
    }

    /// <summary>With no rows there is no cell to hold focus, so the empty state's own action takes it: the keyboard never lands nowhere.</summary>
    public void FocusEmptyState()
    {
        if (Vm is not { IsEmpty: true }) return;
        Vm.FocusedError = "";                          // no row, no row error: the status bar must not keep the deleted line's message
        if (FilterBox.IsKeyboardFocusWithin) return;   // the operator is typing a filter; do not yank focus
        EmptyAddButton.Focus();
        Keyboard.Focus(EmptyAddButton);
    }

    private List<DataGridColumn> VisibleColumns() =>
        LinesGrid.Columns.Where(c => c.Visibility == Visibility.Visible).OrderBy(c => c.DisplayIndex).ToList();

    /// <summary>Rows added or removed by a command (toolbar button, menu item, Ctrl+Z) leave the grid with no current cell, so the
    /// arrow keys go dead until the grid is clicked. Put the current cell back on a real row after every such change.</summary>
    private void OnLinesCollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (_focusHandledByCaller) return;
        if (e.Action is not (NotifyCollectionChangedAction.Add or NotifyCollectionChangedAction.Remove or NotifyCollectionChangedAction.Replace)) return;
        if (!IsKeyboardFocusWithin) return;            // another window / pane owns focus: leave it alone
        if (FilterBox.IsKeyboardFocusWithin) return;

        var newItem = e.Action == NotifyCollectionChangedAction.Add ? e.NewItems?[0] : null;
        var column = LinesGrid.CurrentCell.IsValid && LinesGrid.CurrentCell.Column?.Visibility == Visibility.Visible
            ? LinesGrid.CurrentCell.Column
            : VisibleColumns().FirstOrDefault();
        var fallbackRow = LinesGrid.CurrentCell.IsValid ? LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item) : -1;
        if (fallbackRow < 0) fallbackRow = Math.Max(0, e.OldStartingIndex);

        Dispatcher.BeginInvoke(new Action(() =>
        {
            if (LinesGrid.Items.Count == 0) { FocusEmptyState(); return; }
            if (column == null || column.Visibility != Visibility.Visible) column = VisibleColumns().FirstOrDefault();
            if (column == null) return;
            // A line the operator just added is the one they want to type into, in the first column.
            var row = newItem != null && LinesGrid.Items.IndexOf(newItem) >= 0 ? LinesGrid.Items.IndexOf(newItem) : fallbackRow;
            if (newItem != null) column = ColItem.Visibility == Visibility.Visible ? ColItem : column;
            row = Math.Clamp(row, 0, LinesGrid.Items.Count - 1);
            FocusCell(row, column);
        }), System.Windows.Threading.DispatcherPriority.Background);
    }

    public DataGridCell? GetCell(int rowIndex, DataGridColumn column)
    {
        if (LinesGrid.ItemContainerGenerator.ContainerFromIndex(rowIndex) is not DataGridRow row) return null;
        var presenter = FindChild<DataGridCellsPresenter>(row);
        if (presenter == null) return null;
        return presenter.ItemContainerGenerator.ContainerFromIndex(column.DisplayIndex) as DataGridCell;
    }

    public static T? FindChild<T>(DependencyObject parent) where T : DependencyObject
    {
        for (var i = 0; i < VisualTreeHelper.GetChildrenCount(parent); i++)
        {
            var child = VisualTreeHelper.GetChild(parent, i);
            if (child is T t) return t;
            var r = FindChild<T>(child);
            if (r != null) return r;
        }
        return null;
    }

    // ---- keyboard ---------------------------------------------------------------

    private void OnViewPreviewKeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.F && Keyboard.Modifiers == ModifierKeys.Control) { FilterBox.Focus(); FilterBox.SelectAll(); e.Handled = true; return; }
        if (e.Key == Key.F1) { OnShowShortcuts(this, new RoutedEventArgs()); e.Handled = true; return; }
        if (e.Key == Key.F6) { CyclePanes(Keyboard.Modifiers == ModifierKeys.Shift); e.Handled = true; return; }
        if (e.Key == Key.S && Keyboard.Modifiers == (ModifierKeys.Control | ModifierKeys.Shift)) { SortCurrentColumn(); e.Handled = true; return; }
        if (FilterBox.IsKeyboardFocusWithin)
        {
            // The filter is a detour, not a destination: Enter takes the operator back to the rows the filter just produced.
            if (e.Key == Key.Enter) { ReturnToGrid(); e.Handled = true; return; }
            if (e.Key == Key.Escape)
            {
                if (!string.IsNullOrEmpty(FilterBox.Text)) { Vm?.ClearFilterCommand.Execute(null); e.Handled = true; return; }
                ReturnToGrid(); e.Handled = true; return;
            }
        }
    }

    /// <summary>Back to the grid from the filter box, onto the current cell if there still is one.</summary>
    private void ReturnToGrid()
    {
        if (LinesGrid.Items.Count == 0) { FocusEmptyState(); return; }
        var column = LinesGrid.CurrentCell.IsValid && LinesGrid.CurrentCell.Column?.Visibility == Visibility.Visible
            ? LinesGrid.CurrentCell.Column : VisibleColumns().FirstOrDefault();
        var row = LinesGrid.CurrentCell.IsValid ? LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item) : -1;
        if (column == null) return;
        FocusCell(Math.Clamp(row < 0 ? 0 : row, 0, LinesGrid.Items.Count - 1), column);
    }

    // ---- sorting from the keyboard ------------------------------------------------

    private void OnSortCurrentColumn(object sender, RoutedEventArgs e) => SortCurrentColumn();
    private void OnClearSort(object sender, RoutedEventArgs e) => ClearSort();

    /// <summary>Ctrl+Shift+S sorts by the column holding the current cell and toggles the direction; the focused line keeps focus
    /// after the re-sort. Sorting was reachable only by clicking a column header.</summary>
    public void SortCurrentColumn()
    {
        if (Vm == null || !LinesGrid.CurrentCell.IsValid) return;
        var column = LinesGrid.CurrentCell.Column;
        if (column == null || !column.CanUserSort) return;
        if (PropertyOf(column) is not string path) return;

        var direction = column.SortDirection == ListSortDirection.Ascending ? ListSortDirection.Descending : ListSortDirection.Ascending;
        var item = LinesGrid.CurrentCell.Item;
        LinesGrid.CommitEdit(DataGridEditingUnit.Row, true);
        foreach (var c in LinesGrid.Columns) c.SortDirection = null;
        column.SortDirection = direction;
        Vm.LinesView.SortDescriptions.Clear();
        Vm.LinesView.SortDescriptions.Add(new SortDescription(path, direction));
        Vm.LinesView.Refresh();
        Vm.StatusMessage = $"Sorted by {column.Header} {(direction == ListSortDirection.Ascending ? "ascending" : "descending")}";
        RefocusItem(item, column);
    }

    public void ClearSort()
    {
        if (Vm == null) return;
        var item = LinesGrid.CurrentCell.IsValid ? LinesGrid.CurrentCell.Item : null;
        var column = LinesGrid.CurrentCell.IsValid ? LinesGrid.CurrentCell.Column : null;
        foreach (var c in LinesGrid.Columns) c.SortDirection = null;
        Vm.LinesView.SortDescriptions.Clear();
        Vm.LinesView.Refresh();
        Vm.StatusMessage = "Sort cleared — lines back in entry order";
        RefocusItem(item, column);
    }

    private void RefocusItem(object? item, DataGridColumn? column)
    {
        LinesGrid.UpdateLayout();
        if (LinesGrid.Items.Count == 0) { FocusEmptyState(); return; }
        column ??= VisibleColumns().FirstOrDefault();
        if (column == null) return;
        var idx = item != null ? LinesGrid.Items.IndexOf(item) : -1;
        FocusCell(Math.Clamp(idx < 0 ? 0 : idx, 0, LinesGrid.Items.Count - 1), column);
    }

    /// <summary>F6 cycles command bar → grid → filter, like Explorer and Office.</summary>
    private void CyclePanes(bool backwards)
    {
        var panes = new UIElement[] { AddButton, LinesGrid, FilterBox };
        var current = Array.FindIndex(panes, p => p.IsKeyboardFocusWithin);
        var next = current < 0 ? 1 : (current + (backwards ? -1 : 1) + panes.Length) % panes.Length;
        if (panes[next] == LinesGrid)
        {
            if (LinesGrid.CurrentCell.IsValid && LinesGrid.CurrentCell.Item is { } item)
            {
                var idx = LinesGrid.Items.IndexOf(item);
                if (idx >= 0) { FocusCell(idx, LinesGrid.CurrentCell.Column); return; }
            }
            FocusFirstCell();
        }
        else panes[next].Focus();
    }

    private void OnGridPreviewKeyDown(object sender, KeyEventArgs e)
    {
        var vm = Vm;
        if (vm == null) return;

        // F4 / Alt+Down: open the list of a choice cell, the Windows standard. Without it a dropdown column could only be
        // opened by clicking it (F2 starts the edit but leaves the list closed).
        if ((e.Key == Key.F4 || (e.Key == Key.Down && Keyboard.Modifiers == ModifierKeys.Alt)) && LinesGrid.CurrentCell.IsValid
            && LinesGrid.CurrentCell.Column is DataGridComboBoxColumn)
        {
            OpenCurrentComboCell();
            e.Handled = true;
            return;
        }

        // Delete: the command (with undo) unless a cell editor has focus (then it edits text).
        if (e.Key == Key.Delete && !_isEditing)
        {
            if (vm.DeleteCommand.CanExecute(null)) vm.DeleteCommand.Execute(null);
            e.Handled = true;
            return;
        }

        // Enter on the last row: commit, add a new line, and move into it (data-entry grids grow by Enter).
        if (e.Key == Key.Enter && Keyboard.Modifiers == ModifierKeys.None && LinesGrid.CurrentCell.IsValid)
        {
            var idx = LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item);
            if (idx == LinesGrid.Items.Count - 1 && idx >= 0)
            {
                var column = LinesGrid.CurrentCell.Column;
                LinesGrid.CommitEdit(DataGridEditingUnit.Row, true);
                _focusHandledByCaller = true;
                var line = vm.AddLine();
                _focusHandledByCaller = false;
                LinesGrid.UpdateLayout();
                var newIdx = LinesGrid.Items.IndexOf(line);
                if (newIdx >= 0) FocusCell(newIdx, column);
                e.Handled = true;
                return;
            }
        }

        // Tab while editing: commit and move to the next visible cell WITHOUT entering edit mode on it
        // (WPF's default keeps edit mode, so a ComboBox column would swallow the following arrow keys).
        if (e.Key == Key.Tab && _isEditing && LinesGrid.CurrentCell.IsValid)
        {
            var backwards = Keyboard.Modifiers == ModifierKeys.Shift;
            LinesGrid.CommitEdit(DataGridEditingUnit.Cell, true);
            LinesGrid.CommitEdit(DataGridEditingUnit.Row, true);
            _isEditing = false;
            var visible = LinesGrid.Columns.Where(c => c.Visibility == Visibility.Visible).OrderBy(c => c.DisplayIndex).ToList();
            var ci = visible.IndexOf(LinesGrid.CurrentCell.Column);
            var ri = LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item);
            ci += backwards ? -1 : 1;
            if (ci >= visible.Count) { ci = 0; ri = Math.Min(ri + 1, LinesGrid.Items.Count - 1); }
            if (ci < 0) { ci = visible.Count - 1; ri = Math.Max(ri - 1, 0); }
            FocusCell(ri, visible[ci]);
            e.Handled = true;
            return;
        }

        // Insert: add after the current row and move to it, in the Item column.
        if (e.Key == Key.Insert && !_isEditing)
        {
            var idx = LinesGrid.CurrentCell.IsValid ? LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item) : -1;
            LinesGrid.CommitEdit(DataGridEditingUnit.Row, true);
            _focusHandledByCaller = true;
            var line = vm.AddLine(idx);
            _focusHandledByCaller = false;
            LinesGrid.UpdateLayout();
            var newIdx = LinesGrid.Items.IndexOf(line);
            if (newIdx >= 0) FocusCell(newIdx, ColItem);
            e.Handled = true;
        }
    }

    /// <summary>Begins the edit if needed and drops the list open, so the whole choice is made from the keyboard (F4, arrows, Enter).</summary>
    public void OpenCurrentComboCell()
    {
        if (!LinesGrid.CurrentCell.IsValid || LinesGrid.CurrentCell.Column is not DataGridComboBoxColumn column) return;
        var row = LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item);
        if (row < 0) return;
        if (!_isEditing) LinesGrid.BeginEdit();
        Dispatcher.BeginInvoke(new Action(() =>
        {
            var cell = GetCell(row, column);
            var combo = cell != null ? FindChild<ComboBox>(cell) : null;
            if (combo == null) return;
            combo.Focus();
            Keyboard.Focus(combo);
            combo.IsDropDownOpen = true;
        }), System.Windows.Threading.DispatcherPriority.Input);
    }

    private void OnBeginningEdit(object? sender, DataGridBeginningEditEventArgs e) => _isEditing = true;
    private void OnCellEditEnding(object? sender, DataGridCellEditEndingEventArgs e) => _isEditing = false;
    private void OnRowEditEnding(object? sender, DataGridRowEditEndingEventArgs e)
    {
        if (e.Row.Item is PurchaseOrderLine l) l.Validate();
    }

    // ---- validation feedback ------------------------------------------------------

    private void OnCurrentCellChanged(object? sender, EventArgs e)
    {
        // The header of the current column is marked (bar + primary text) so the column is readable from the top of the grid.
        ActiveColumn.Apply(LinesGrid, LinesGrid.CurrentCell.IsValid ? LinesGrid.CurrentCell.Column : null);
        UpdateFocusedError();
    }

    /// <summary>Property name behind a column (DataGridComboBoxColumn has no Binding, only SelectedItemBinding).</summary>
    private static string? PropertyOf(DataGridColumn? column) => column switch
    {
        DataGridBoundColumn b => (b.Binding as Binding)?.Path.Path,
        DataGridComboBoxColumn c => (c.SelectedItemBinding as Binding)?.Path.Path,
        _ => null,
    };

    /// <summary>Status-bar text for the focused row: the focused cell's own error first, otherwise the row's first error, always with the line number.</summary>
    private void UpdateFocusedError()
    {
        if (Vm == null) return;
        var cell = LinesGrid.CurrentCell;
        if (!cell.IsValid || cell.Item is not PurchaseOrderLine line || !line.HasErrors) { Vm.FocusedError = ""; return; }
        var prop = PropertyOf(cell.Column);
        var own = prop != null ? line.GetErrors(prop).Cast<string>().FirstOrDefault() : null;
        var msg = own ?? line.ErrorSummary.Split(Environment.NewLine).FirstOrDefault() ?? "";
        Vm.FocusedError = $"Line {line.LineNo}: {msg}";
        UpdateKeyHints();
    }

    /// <summary>F8 / Shift+F8: move to the next (previous) cell that has a validation error, wrapping around; commits any edit first.</summary>
    public bool GoToError(bool backwards)
    {
        if (LinesGrid.Items.Count == 0) return false;
        LinesGrid.CommitEdit(DataGridEditingUnit.Row, true);
        var visible = LinesGrid.Columns.Where(c => c.Visibility == Visibility.Visible).OrderBy(c => c.DisplayIndex).ToList();
        var start = LinesGrid.CurrentCell.IsValid ? LinesGrid.Items.IndexOf(LinesGrid.CurrentCell.Item) : -1;
        var n = LinesGrid.Items.Count;
        for (var step = 1; step <= n; step++)
        {
            var idx = ((start + (backwards ? -step : step)) % n + n) % n;
            if (LinesGrid.Items[idx] is not PurchaseOrderLine line || !line.HasErrors) continue;
            var col = visible.FirstOrDefault(c => PropertyOf(c) is string p && line.GetErrors(p).Cast<string>().Any()) ?? visible.FirstOrDefault();
            if (col == null) return false;
            FocusCell(idx, col);
            UpdateFocusedError();
            return true;
        }
        return false;
    }

    // ---- selection --------------------------------------------------------------

    private void OnSelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (Vm == null) return;
        foreach (var o in e.RemovedItems) if (o is PurchaseOrderLine l) Vm.SelectedLines.Remove(l);
        foreach (var o in e.AddedItems) if (o is PurchaseOrderLine l && !Vm.SelectedLines.Contains(l)) Vm.SelectedLines.Add(l);
    }

    // ---- column priority ----------------------------------------------------------

    private void OnGridSizeChanged(object sender, SizeChangedEventArgs e) => ApplyColumnPriority();

    private void ApplyColumnPriority()
    {
        if (Vm == null) return;
        var width = LinesGrid.ActualWidth > 0 ? LinesGrid.ActualWidth : ActualWidth - 32;
        Vm.HiddenColumnCount = ColumnPriority.Apply(LinesGrid, width);
        // Chrome priority for narrow windows: key hints go first, then subtotal/tax detail, then the two dropdowns fold into "More".
        UpdateKeyHints();
        var w = ActualWidth;
        TotalsDetail.Visibility = w < 1000 ? Visibility.Collapsed : Visibility.Visible;
        FilterHost.Width = w < 1000 ? 180 : 260;
        var fold = w < 980;
        StatusButton.Visibility = fold ? Visibility.Collapsed : Visibility.Visible;
        WarehouseButton.Visibility = fold ? Visibility.Collapsed : Visibility.Visible;
        MoreButton.Visibility = fold ? Visibility.Visible : Visibility.Collapsed;
        SyncColumnsMenu();
    }

    /// <summary>Key hints are the lowest-priority status segment: they fold below 1180 DIP and whenever a focused-row error message needs the room.</summary>
    private void UpdateKeyHints()
    {
        var show = ActualWidth >= 1180 && string.IsNullOrEmpty(Vm?.FocusedError);
        KeyHints.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
    }

    private void BuildColumnsMenu()
    {
        ColumnsMenu.Items.Clear();
        foreach (var col in LinesGrid.Columns)
        {
            var item = new MenuItem { Header = col.Header?.ToString(), IsCheckable = true, IsChecked = col.Visibility == Visibility.Visible, StaysOpenOnClick = true, Tag = col };
            item.Click += (_, _) =>
            {
                ColumnPriority.SetUserOverride(col, true);
                col.Visibility = item.IsChecked ? Visibility.Visible : Visibility.Collapsed;
                ApplyColumnPriority();
            };
            ColumnsMenu.Items.Add(item);
        }
    }

    private void SyncColumnsMenu()
    {
        foreach (var o in ColumnsMenu.Items)
            if (o is MenuItem { Tag: DataGridColumn col } mi) mi.IsChecked = col.Visibility == Visibility.Visible;
    }

    private void OnResetColumns(object sender, RoutedEventArgs e)
    {
        foreach (var (col, (width, index)) in _defaultLayout)
        {
            ColumnPriority.SetUserOverride(col, false);
            col.Width = new DataGridLength(width, col.Width.UnitType);
            col.DisplayIndex = index;
            col.SortDirection = null;
        }
        ApplyColumnDefaults();
        ApplyColumnPriority();
    }

    // ---- column defaults (settings dialog) ----------------------------------------------

    private static string KeyOf(DataGridColumn col) => col.Header?.ToString() ?? "";

    /// <summary>Columns the clerk keeps hidden are pinned collapsed (a user override); the others go back to the width rule.</summary>
    private void ApplyColumnDefaults()
    {
        if (Vm == null) return;
        foreach (var col in LinesGrid.Columns)
        {
            var hidden = Vm.Defaults.HiddenColumns.Contains(KeyOf(col)) && ColumnPriority.GetHideBelow(col) > 0;
            if (hidden) { ColumnPriority.SetUserOverride(col, true); col.Visibility = Visibility.Collapsed; }
            else if (ColumnPriority.GetUserOverride(col)) { ColumnPriority.SetUserOverride(col, false); col.Visibility = Visibility.Visible; }
        }
    }

    private void OnColumnDefaults(object sender, RoutedEventArgs e) => OpenColumnDefaults();

    /// <summary>Opens the owned modal dialog; on OK applies and stores the defaults. Focus returns to whatever had it (usually the current grid cell).</summary>
    public bool? OpenColumnDefaults()
    {
        if (Vm == null) return null;
        var invoker = Keyboard.FocusedElement as IInputElement;
        var cell = LinesGrid.CurrentCell;
        var columns = LinesGrid.Columns.OrderBy(c => c.DisplayIndex).Select(c => (KeyOf(c), KeyOf(c), ColumnPriority.GetHideBelow(c) > 0));
        var dlg = new ColumnDefaultsDialog(Window.GetWindow(this)!, Vm.Defaults, Vm.Warehouses, columns);
        var result = dlg.ShowDialog();
        if (result == true && dlg.Result != null)
        {
            Vm.Defaults = dlg.Result;
            ApplyColumnDefaults();
            ApplyColumnPriority();
            Vm.StatusMessage = $"Column defaults saved — new lines start in {Vm.Defaults.DefaultWarehouse}";
        }
        // Return focus to the invoker (the grid cell it came from, re-resolved because rows may have been re-virtualised).
        if (invoker is DataGridCell && cell.IsValid && cell.Item != null && cell.Column != null)
        {
            var idx = LinesGrid.Items.IndexOf(cell.Item);
            var col = cell.Column.Visibility == Visibility.Visible ? cell.Column : LinesGrid.Columns.Where(c => c.Visibility == Visibility.Visible).OrderBy(c => c.DisplayIndex).First();
            if (idx >= 0) FocusCell(idx, col);
        }
        else if (invoker != null) Keyboard.Focus(invoker);
        return result;
    }

    // ---- misc commands --------------------------------------------------------------

    private void OnOpenStatusMenu(object sender, RoutedEventArgs e) => OpenMenu(StatusButton);
    private void OnOpenWarehouseMenu(object sender, RoutedEventArgs e) => OpenMenu(WarehouseButton);
    private void OnOpenMoreMenu(object sender, RoutedEventArgs e) => OpenMenu(MoreButton);
    private static void OpenMenu(Button b)
    {
        if (b.ContextMenu == null) return;
        b.ContextMenu.PlacementTarget = b;
        b.ContextMenu.Placement = PlacementMode.Bottom;
        b.ContextMenu.IsOpen = true;
    }

    private void OnExit(object sender, RoutedEventArgs e) => Application.Current.Shutdown();

    private void OnShowShortcuts(object sender, RoutedEventArgs e)
    {
        MessageBox.Show(Window.GetWindow(this),
            "Grid\n  ↑ ↓ ← →  move between cells\n  F2 / typing  edit the cell\n  Enter  commit and move down (adds a line after the last row)\n  Tab / Shift+Tab  commit and move right / left\n  Esc  cancel the edit\n  Home / End, PgUp / PgDn, Ctrl+Home / Ctrl+End\n  Shift+↑↓ / Ctrl+click  extend the selection\n  F8 / Shift+F8  next / previous error\n\nLines\n  Ins / Ctrl+N  add line\n  Ctrl+D  duplicate\n  Del  delete (Ctrl+Z restores)\n  Ctrl+S  save\n  F5  reload\n\nScreen\n  Ctrl+F  filter\n  F6  cycle command bar › grid › filter\n  Alt  menu access keys",
            "Keyboard shortcuts", MessageBoxButton.OK, MessageBoxImage.None);
    }
}

public sealed class NonEmptyToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type t, object p, CultureInfo c) => string.IsNullOrEmpty(value as string) ? Visibility.Collapsed : Visibility.Visible;
    public object ConvertBack(object value, Type t, object p, CultureInfo c) => throw new NotSupportedException();
}

public sealed class HasErrorsToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type t, object p, CultureInfo c) => value is true ? Visibility.Visible : Visibility.Collapsed;
    public object ConvertBack(object value, Type t, object p, CultureInfo c) => throw new NotSupportedException();
}
