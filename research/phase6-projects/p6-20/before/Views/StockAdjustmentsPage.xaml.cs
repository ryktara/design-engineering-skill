using System.ComponentModel;
using CommunityToolkit.WinUI.UI.Controls;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation.Peers;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Windows.Storage;
using Erp.Client.ViewModels;

namespace Erp.Client.Views;

public sealed partial class StockAdjustmentsPage : Page
{
    public StockAdjustmentsViewModel ViewModel { get; } = new();

    private const string CreatedByVisibleKey = "StockAdjustments.CreatedByVisible";

    public StockAdjustmentsPage()
    {
        InitializeComponent();
        Grid.DataContext = ViewModel;
        Loaded += (_, _) =>
        {
            // Restore the persisted view option (desktop: never lose layout state between launches).
            var saved = ApplicationData.Current.LocalSettings.Values[CreatedByVisibleKey] as bool? ?? false;
            CreatedByToggle.IsChecked = saved;
            CreatedByColumn.Visibility = saved ? Visibility.Visible : Visibility.Collapsed;
            Grid.Focus(FocusState.Programmatic);
            // XAML live regions are not announced by setting LiveSetting alone: the app must raise LiveRegionChanged
            // after the text has changed (Accessibility Insights guidance for UWP/WinUI XAML). Subscribed in Loaded so
            // the handler runs after the x:Bind listener (registered at Loading) has already pushed the new text.
            ViewModel.PropertyChanged -= ViewModel_PropertyChanged;
            ViewModel.PropertyChanged += ViewModel_PropertyChanged;
        };
    }

    private void ViewModel_PropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        var target = e.PropertyName switch
        {
            nameof(StockAdjustmentsViewModel.ResultSummary) => ResultSummaryText,
            nameof(StockAdjustmentsViewModel.SelectionLabel) => SelectionLabelText,
            _ => null,
        };
        if (target is null) return;
        var peer = FrameworkElementAutomationPeer.FromElement(target);
        peer?.RaiseAutomationEvent(AutomationEvents.LiveRegionChanged);
    }

    private void CreatedByToggle_Click(object sender, RoutedEventArgs e)
    {
        var show = CreatedByToggle.IsChecked == true;
        CreatedByColumn.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
        ApplicationData.Current.LocalSettings.Values[CreatedByVisibleKey] = show;
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

    // F6 / Shift+F6: move between the page's regions (command bar, filters, grid) without tabbing through every control.
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
        UIElement[] regions = { Commands, Filters, Grid };
        var focused = FocusManager.GetFocusedElement(XamlRoot) as DependencyObject;
        var current = -1;
        for (var i = 0; i < regions.Length && current < 0; i++)
            if (focused is not null && IsWithin(focused, regions[i])) current = i;
        var next = ((current < 0 ? 0 : current + step) + regions.Length) % regions.Length;
        // A region that is itself a tab stop (the DataGrid) takes focus directly; otherwise its first focusable
        // child does (first AppBarButton of the CommandBar, the Search box of the filter row).
        var target = regions[next] is Control { IsTabStop: true } c ? c : FocusManager.FindFirstFocusableElement(regions[next]) as Control;
        target?.Focus(FocusState.Keyboard);
    }

    private static bool IsWithin(DependencyObject element, UIElement ancestor)
    {
        for (var d = element; d is not null; d = VisualTreeHelper.GetParent(d))
            if (ReferenceEquals(d, ancestor)) return true;
        return false;
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
