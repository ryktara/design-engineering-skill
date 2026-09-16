using Avalonia;
using Avalonia.Controls;

namespace FleetDesk.Views;

public partial class VehiclesView : UserControl
{
    /// <summary>Below this width the filter cluster moves to its own row and Odometer is dropped.</summary>
    private const double NarrowWidth = 1120;

    /// <summary>Below this width "Last service" is dropped as well.</summary>
    private const double CompactWidth = 1000;

    private const int OdometerColumnIndex = 4;
    private const int LastServiceColumnIndex = 5;

    public VehiclesView()
    {
        InitializeComponent();
        // Avalonia has no container queries: watch our own bounds and drive the
        // layout with style classes plus explicit column visibility.
        this.GetObservable(BoundsProperty).Subscribe(new BoundsObserver(this));
    }

    private void ApplyWidth(double width)
    {
        if (width <= 0)
            return;

        var narrow = width < NarrowWidth;
        var compact = width < CompactWidth;

        if (Classes.Contains("narrow") != narrow)
        {
            if (narrow)
                Classes.Add("narrow");
            else
                Classes.Remove("narrow");
        }

        // Column priority, lowest first. The dropped values stay readable in the
        // selection summary at the bottom of the view.
        // DataGrid columns are not visual children, so they are addressed by index
        // (see the column order in VehiclesView.axaml).
        var columns = VehicleGrid.Columns;
        if (columns.Count > OdometerColumnIndex)
            columns[OdometerColumnIndex].IsVisible = !narrow;
        if (columns.Count > LastServiceColumnIndex)
            columns[LastServiceColumnIndex].IsVisible = !compact;
    }

    private sealed class BoundsObserver : IObserver<Rect>
    {
        private readonly VehiclesView _view;

        public BoundsObserver(VehiclesView view) => _view = view;

        public void OnCompleted() { }

        public void OnError(Exception error) { }

        public void OnNext(Rect value) => _view.ApplyWidth(value.Width);
    }
}
