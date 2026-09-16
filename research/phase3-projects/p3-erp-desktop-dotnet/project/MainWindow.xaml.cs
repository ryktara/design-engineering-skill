using System.Windows;
using ErpClient.ViewModels;

namespace ErpClient;

public partial class MainWindow : Window
{
    public MainWindow() : this(new PurchaseOrderLinesViewModel(), autoLoad: true) { }

    public MainWindow(PurchaseOrderLinesViewModel vm, bool autoLoad)
    {
        InitializeComponent();
        ViewModel = vm;
        DataContext = vm;
        if (autoLoad) Loaded += async (_, _) => await vm.LoadAsync();
    }

    public PurchaseOrderLinesViewModel ViewModel { get; }
}
