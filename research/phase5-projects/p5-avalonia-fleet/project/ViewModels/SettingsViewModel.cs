using FleetDesk.Services;

namespace FleetDesk.ViewModels;

public sealed class SettingsViewModel : ViewModelBase
{
    private string _depotName = SampleData.DepotName;
    private string _units = "Metric (km)";
    private bool _isDarkTheme;
    private string _statusMessage = "";

    public SettingsViewModel()
    {
        SaveCommand = new RelayCommand(() => StatusMessage = "Settings saved (in memory only).");
    }

    public string[] UnitChoices { get; } = { "Metric (km)", "Imperial (mi)" };

    public RelayCommand SaveCommand { get; }

    public string DepotName
    {
        get => _depotName;
        set => SetProperty(ref _depotName, value);
    }

    public string Units
    {
        get => _units;
        set => SetProperty(ref _units, value);
    }

    /// <summary>Theme toggle stub. FleetDesk is light-first; flipping this only updates the hint text.</summary>
    public bool IsDarkTheme
    {
        get => _isDarkTheme;
        set
        {
            if (SetProperty(ref _isDarkTheme, value))
                OnPropertyChanged(nameof(ThemeHint));
        }
    }

    public string ThemeHint => _isDarkTheme
        ? "Dark theme is not implemented in this build. The app stays light."
        : "Light theme (default).";

    public string StatusMessage
    {
        get => _statusMessage;
        private set => SetProperty(ref _statusMessage, value);
    }
}
