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

        Dispatch.PropertyChanged += (_, e) =>
        {
            if (e.PropertyName == nameof(DispatchViewModel.UnsavedLabel))
                OnPropertyChanged(nameof(UnsavedLabel));
        };

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
    public string FleetSummary => $"{Vehicles.TotalCount} vehicles - {Vehicles.AvailableCount} available - {Vehicles.OnJobCount} on job - {Vehicles.OverdueCount} overdue for service";
    /// <summary>Status-bar save state: "Unsaved changes - J-2041" while a dispatch job is dirty, else "".</summary>
    public string UnsavedLabel => Dispatch.UnsavedLabel;

    private void Navigate(ViewModelBase target, string name)
    {
        if (ReferenceEquals(target, _currentView)) return;

        // Leaving Dispatch with a dirty job asks first; the navigation runs after Save / Discard.
        Dispatch.TryLeave($"leaving Dispatch for {name}", () =>
        {
            CurrentView = target;
            StatusText = $"{name} view";
            OnPropertyChanged(nameof(DepotLabel));
        });
    }

    /// <summary>
    /// Window-close guard. Returns true when the window may close now; otherwise shows the
    /// unsaved-changes prompt on the Dispatch screen and calls <paramref name="close"/> once
    /// the user has saved or discarded.
    /// </summary>
    public bool TryClose(Action close)
    {
        if (!Dispatch.HasChanges) return true;
        if (!ReferenceEquals(_currentView, Dispatch))
        {
            CurrentView = Dispatch;
            StatusText = "Dispatch view";
        }
        Dispatch.TryLeave("closing FleetDesk", close);
        return false;
    }

    private void Exit()
    {
        if (Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            // Close (not Shutdown) so File > Exit passes through the window's unsaved-changes guard.
            if (desktop.MainWindow is { } window) window.Close();
            else desktop.Shutdown();
        }
    }
}
