using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Erp.Client.Views;

namespace Erp.Client;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        ContentFrame.Navigate(typeof(StockAdjustmentsPage));
    }

    private void Nav_SelectionChanged(NavigationView sender, NavigationViewSelectionChangedEventArgs args)
    {
        if (args.SelectedItem is NavigationViewItem item && item.Tag is string tag)
        {
            var type = tag switch
            {
                "Orders" => typeof(OrdersPage),
                _ => typeof(StockAdjustmentsPage),
            };
            ContentFrame.Navigate(type);
        }
    }
}
