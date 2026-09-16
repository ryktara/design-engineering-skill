using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using FleetDesk.Services;

namespace FleetDesk.ViewModels;

public sealed class MainWindowViewModel : ViewModelBase
{
    private ViewModelBase _currentView;
    private string _statusText = "Ready";

    public MainWindowViewModel()
    {
        Vehicles = new VehiclesViewModel();
        Dispatch = new DispatchViewModel();
        Settings = new SettingsViewModel();
        _currentView = Vehicles;

        ShowVehiclesCommand = new RelayCommand(() => Navigate(Vehicles, "Vehicles"));
        ShowDispatchCommand = new RelayCommand(() => Navigate(Dispatch, "Dispatch"));
        ShowSettingsCommand = new RelayCommand(() => Navigate(Settings, "Settings"));
        RefreshCommand = new RelayCommand(() => StatusText = "Refreshed sample data (static).");
        AboutCommand = new RelayCommand(() => StatusText = "FleetDesk 1.0 - research fixture.");
        ExitCommand = new RelayCommand(Exit);
    }

    public VehiclesViewModel Vehicles { get; }
    public DispatchViewModel Dispatch { get; }
    public SettingsViewModel Settings { get; }

    public RelayCommand ShowVehiclesCommand { get; }
    public RelayCommand ShowDispatchCommand { get; }
    public RelayCommand ShowSettingsCommand { get; }
    public RelayCommand RefreshCommand { get; }
    public RelayCommand AboutCommand { get; }
    public RelayCommand ExitCommand { get; }

    public ViewModelBase CurrentView
    {
        get => _currentView;
        private set
        {
            if (SetProperty(ref _currentView, value))
                OnPropertyChanged(nameof(CurrentViewName));
        }
    }

    public string CurrentViewName => _currentView switch
    {
        VehiclesViewModel => "Vehicles",
        DispatchViewModel => "Dispatch",
        SettingsViewModel => "Settings",
        _ => ""
    };

    public string StatusText
    {
        get => _statusText;
        private set => SetProperty(ref _statusText, value);
    }

    public string DepotLabel => $"Depot: {Settings.DepotName}";
    public string FleetSummary => $"{Vehicles.TotalCount} vehicles - {Vehicles.AvailableCount} available - {Vehicles.OnJobCount} on job";

    private void Navigate(ViewModelBase target, string name)
    {
        CurrentView = target;
        StatusText = $"{name} view";
        OnPropertyChanged(nameof(DepotLabel));
    }

    private static void Exit()
    {
        if (Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            desktop.Shutdown();
    }
}
