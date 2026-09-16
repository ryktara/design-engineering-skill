using CommunityToolkit.WinUI.UI.Controls;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Erp.Client.ViewModels;

namespace Erp.Client.Views;

public sealed partial class StockAdjustmentsPage : Page
{
    public StockAdjustmentsViewModel ViewModel { get; } = new();

    public StockAdjustmentsPage()
    {
        InitializeComponent();
        Grid.DataContext = ViewModel;
        Loaded += (_, _) => Grid.Focus(Microsoft.UI.Xaml.FocusState.Programmatic);
    }

    private void FocusSearch_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        SearchBox.Focus(Microsoft.UI.Xaml.FocusState.Keyboard);
        SearchBox.SelectAll();
        args.Handled = true;
    }

    private void EditSelected_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        if (ViewModel.Selected is { } item && ViewModel.EditCommand.CanExecute(item))
            ViewModel.EditCommand.Execute(item);
        args.Handled = true;
    }

    // Sorting is done in the view model so the sort indicator and the data never disagree.
    private void Grid_Sorting(object sender, DataGridColumnEventArgs e)
    {
        var key = e.Column.Tag as string;
        if (key is null) return;
        var next = e.Column.SortDirection == DataGridSortDirection.Ascending
            ? DataGridSortDirection.Descending
            : DataGridSortDirection.Ascending;
        foreach (var c in Grid.Columns) c.SortDirection = null;
        e.Column.SortDirection = next;
        ViewModel.Sort(key, next == DataGridSortDirection.Descending);
    }
}
