using System.ComponentModel;
using CommunityToolkit.WinUI.UI.Controls;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation.Peers;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Erp.Client.ViewModels;

namespace Erp.Client.Views;

public sealed partial class InvoiceMatchingPage : Page
{
    public InvoiceMatchingViewModel ViewModel { get; } = new();

    public InvoiceMatchingPage()
    {
        InitializeComponent();
        InvoiceGrid.DataContext = ViewModel;
        LineGrid.DataContext = ViewModel;
        Loaded += (_, _) =>
        {
            // Keyboard users land on the master table, not on the first chrome control.
            InvoiceGrid.Focus(FocusState.Programmatic);
            // XAML live regions are not announced by setting LiveSetting alone: the app must raise
            // LiveRegionChanged after the text has changed (same pattern as StockAdjustmentsPage).
            ViewModel.PropertyChanged -= ViewModel_PropertyChanged;
            ViewModel.PropertyChanged += ViewModel_PropertyChanged;
        };
    }

    private void ViewModel_PropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        var target = e.PropertyName switch
        {
            nameof(InvoiceMatchingViewModel.ResultSummary) => ResultSummaryText,
            nameof(InvoiceMatchingViewModel.SelectionLabel) => SelectionLabelText,
            nameof(InvoiceMatchingViewModel.LinesTitle) => LinesTitleText,
            _ => (FrameworkElement?)null,
        };
        if (target is null) return;
        var peer = FrameworkElementAutomationPeer.FromElement(target);
        peer?.RaiseAutomationEvent(AutomationEvents.LiveRegionChanged);
    }

    private async void ShowShortcuts_Click(object sender, RoutedEventArgs e)
    {
        // ContentDialog returns focus to the invoking element when it closes.
        ShortcutsDialog.XamlRoot = XamlRoot;
        await ShortcutsDialog.ShowAsync();
    }

    private void ClearSearch_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        if (string.IsNullOrEmpty(ViewModel.SearchText)) return; // nothing to clear: let Escape bubble (flyouts, dialogs)
        ViewModel.SearchText = null;
        args.Handled = true;
    }

    private void FocusSearch_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        SearchBox.Focus(FocusState.Keyboard);
        SearchBox.SelectAll();
        args.Handled = true;
    }

    // F6 / Shift+F6: move between the page's four regions without tabbing through every control.
    private void CycleRegion_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        FocusRegion(+1);
        args.Handled = true;
    }

    private void CycleRegionBack_Invoked(KeyboardAccelerator sender, KeyboardAcceleratorInvokedEventArgs args)
    {
        FocusRegion(-1);
        args.Handled = true;
    }

    private void FocusRegion(int step)
    {
        UIElement[] regions = { Commands, Filters, InvoiceGrid, LineGrid };
        var focused = FocusManager.GetFocusedElement(XamlRoot) as DependencyObject;
        var current = -1;
        for (var i = 0; i < regions.Length && current < 0; i++)
            if (focused is not null && IsWithin(focused, regions[i])) current = i;
        var next = ((current < 0 ? 0 : current + step) + regions.Length) % regions.Length;
        // A region that is itself a tab stop (a DataGrid) takes focus directly; otherwise its first
        // focusable child does (first AppBarButton of the CommandBar, the Search box of the filter row).
        var target = regions[next] is Control { IsTabStop: true } c ? c : FocusManager.FindFirstFocusableElement(regions[next]) as Control;
        target?.Focus(FocusState.Keyboard);
    }

    private static bool IsWithin(DependencyObject element, UIElement ancestor)
    {
        for (var d = element; d is not null; d = VisualTreeHelper.GetParent(d))
            if (ReferenceEquals(d, ancestor)) return true;
        return false;
    }

    // Sorting is done in the view model so the sort indicator and the data never disagree.
    private void InvoiceGrid_Sorting(object sender, DataGridColumnEventArgs e)
    {
        var key = e.Column.Tag as string;
        if (key is null) return;
        var next = e.Column.SortDirection == DataGridSortDirection.Ascending
            ? DataGridSortDirection.Descending
            : DataGridSortDirection.Ascending;
        foreach (var c in InvoiceGrid.Columns) c.SortDirection = null;
        e.Column.SortDirection = next;
        ViewModel.Sort(key, next == DataGridSortDirection.Descending);
    }
}
