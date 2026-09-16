using System.Collections.ObjectModel;
using FleetDesk.Models;
using FleetDesk.Services;

namespace FleetDesk.ViewModels;

public sealed class VehiclesViewModel : ViewModelBase
{
    private readonly IReadOnlyList<Vehicle> _all = SampleData.Vehicles;
    private string _filterText = "";
    private Vehicle? _selectedVehicle;

    public VehiclesViewModel()
    {
        FilteredVehicles = new ObservableCollection<Vehicle>(_all);
        ClearFilterCommand = new RelayCommand(() => FilterText = "");
    }

    public ObservableCollection<Vehicle> FilteredVehicles { get; }

    public RelayCommand ClearFilterCommand { get; }

    public string FilterText
    {
        get => _filterText;
        set
        {
            if (SetProperty(ref _filterText, value))
                ApplyFilter();
        }
    }

    public Vehicle? SelectedVehicle
    {
        get => _selectedVehicle;
        set
        {
            if (SetProperty(ref _selectedVehicle, value))
                OnPropertyChanged(nameof(SelectionSummary));
        }
    }

    public int TotalCount => _all.Count;
    public int ShownCount => FilteredVehicles.Count;
    public int AvailableCount => _all.Count(v => v.Status == VehicleStatus.Available);
    public int OnJobCount => _all.Count(v => v.Status == VehicleStatus.OnJob);
    public int MaintenanceCount => _all.Count(v => v.Status is VehicleStatus.Maintenance or VehicleStatus.OutOfService);

    public string SelectionSummary => _selectedVehicle is null
        ? "No vehicle selected"
        : $"{_selectedVehicle.Id} - {_selectedVehicle.Plate} - {_selectedVehicle.Driver} - {_selectedVehicle.OdometerKm:N0} km";

    private void ApplyFilter()
    {
        var q = _filterText.Trim();
        FilteredVehicles.Clear();
        foreach (var v in _all)
        {
            if (q.Length == 0 || Matches(v, q))
                FilteredVehicles.Add(v);
        }
        OnPropertyChanged(nameof(ShownCount));
    }

    private static bool Matches(Vehicle v, string q) =>
        v.Id.Contains(q, StringComparison.OrdinalIgnoreCase) ||
        v.Plate.Contains(q, StringComparison.OrdinalIgnoreCase) ||
        v.Driver.Contains(q, StringComparison.OrdinalIgnoreCase) ||
        v.StatusLabel.Contains(q, StringComparison.OrdinalIgnoreCase);
}
