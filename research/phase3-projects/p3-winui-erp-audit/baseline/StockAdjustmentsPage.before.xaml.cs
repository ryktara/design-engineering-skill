using Microsoft.UI.Xaml;
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
    }

    // Hover-only reveal of the row action buttons (keyboard users never see them).
    private void Row_PointerEntered(object sender, PointerRoutedEventArgs e)
    {
        if (sender is Grid row && row.FindName("Actions") is UIElement actions)
            actions.Visibility = Visibility.Visible;
    }

    private void Row_PointerExited(object sender, PointerRoutedEventArgs e)
    {
        if (sender is Grid row && row.FindName("Actions") is UIElement actions)
            actions.Visibility = Visibility.Collapsed;
    }
}
