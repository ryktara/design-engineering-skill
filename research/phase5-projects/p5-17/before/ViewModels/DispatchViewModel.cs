using System.Collections.ObjectModel;
using FleetDesk.Models;
using FleetDesk.Services;

namespace FleetDesk.ViewModels;

public sealed class DispatchViewModel : ViewModelBase
{
    private Job? _selectedJob;
    private string _editTitle = "";
    private string _editCustomer = "";
    private string _editPickup = "";
    private string _editDropoff = "";
    private string _editPriority = "Normal";
    private string _editVehicleId = Unassigned;
    private string _editNotes = "";
    private string _statusMessage = "";

    public const string Unassigned = "(unassigned)";

    public DispatchViewModel()
    {
        PendingJobs = new ObservableCollection<Job>(SampleData.CreatePendingJobs());
        Priorities = Enum.GetNames<JobPriority>();
        VehicleChoices = new[] { Unassigned }
            .Concat(SampleData.Vehicles
                .Where(v => v.Status is VehicleStatus.Available or VehicleStatus.OnJob)
                .Select(v => v.Id))
            .ToArray();

        SaveCommand = new RelayCommand(Save, () => SelectedJob is not null && HasChanges);
        CancelCommand = new RelayCommand(Cancel, () => SelectedJob is not null && HasChanges);

        SelectedJob = PendingJobs.FirstOrDefault();
    }

    public ObservableCollection<Job> PendingJobs { get; }
    public string[] Priorities { get; }
    public string[] VehicleChoices { get; }

    public RelayCommand SaveCommand { get; }
    public RelayCommand CancelCommand { get; }

    public Job? SelectedJob
    {
        get => _selectedJob;
        set
        {
            if (SetProperty(ref _selectedJob, value))
            {
                LoadEditor();
                OnPropertyChanged(nameof(HasSelection));
                OnPropertyChanged(nameof(EditorHeading));
            }
        }
    }

    public bool HasSelection => _selectedJob is not null;
    public string EditorHeading => _selectedJob is null ? "Select a job" : $"{_selectedJob.Id} - {_selectedJob.Title}";
    public int PendingCount => PendingJobs.Count;
    public int UnassignedCount => PendingJobs.Count(j => j.AssignedVehicleId is null);

    public string EditTitle { get => _editTitle; set { if (SetProperty(ref _editTitle, value)) Dirty(); } }
    public string EditCustomer { get => _editCustomer; set { if (SetProperty(ref _editCustomer, value)) Dirty(); } }
    public string EditPickup { get => _editPickup; set { if (SetProperty(ref _editPickup, value)) Dirty(); } }
    public string EditDropoff { get => _editDropoff; set { if (SetProperty(ref _editDropoff, value)) Dirty(); } }
    public string EditPriority { get => _editPriority; set { if (SetProperty(ref _editPriority, value)) Dirty(); } }
    public string EditVehicleId { get => _editVehicleId; set { if (SetProperty(ref _editVehicleId, value)) Dirty(); } }
    public string EditNotes { get => _editNotes; set { if (SetProperty(ref _editNotes, value)) Dirty(); } }

    public string StatusMessage
    {
        get => _statusMessage;
        private set => SetProperty(ref _statusMessage, value);
    }

    public bool HasChanges
    {
        get
        {
            if (_selectedJob is null) return false;
            return _editTitle != _selectedJob.Title
                || _editCustomer != _selectedJob.Customer
                || _editPickup != _selectedJob.Pickup
                || _editDropoff != _selectedJob.Dropoff
                || _editPriority != _selectedJob.Priority.ToString()
                || _editVehicleId != (_selectedJob.AssignedVehicleId ?? Unassigned)
                || _editNotes != _selectedJob.Notes;
        }
    }

    private void LoadEditor()
    {
        var j = _selectedJob;
        _editTitle = j?.Title ?? "";
        _editCustomer = j?.Customer ?? "";
        _editPickup = j?.Pickup ?? "";
        _editDropoff = j?.Dropoff ?? "";
        _editPriority = j?.Priority.ToString() ?? "Normal";
        _editVehicleId = j?.AssignedVehicleId ?? Unassigned;
        _editNotes = j?.Notes ?? "";
        foreach (var name in new[]
                 {
                     nameof(EditTitle), nameof(EditCustomer), nameof(EditPickup), nameof(EditDropoff),
                     nameof(EditPriority), nameof(EditVehicleId), nameof(EditNotes)
                 })
        {
            OnPropertyChanged(name);
        }
        StatusMessage = "";
        Dirty();
    }

    private void Dirty()
    {
        OnPropertyChanged(nameof(HasChanges));
        SaveCommand?.RaiseCanExecuteChanged();
        CancelCommand?.RaiseCanExecuteChanged();
    }

    private void Save()
    {
        var j = _selectedJob;
        if (j is null) return;

        j.Title = _editTitle.Trim();
        j.Customer = _editCustomer.Trim();
        j.Pickup = _editPickup.Trim();
        j.Dropoff = _editDropoff.Trim();
        j.Priority = Enum.TryParse<JobPriority>(_editPriority, out var p) ? p : JobPriority.Normal;
        j.AssignedVehicleId = _editVehicleId == Unassigned ? null : _editVehicleId;
        j.Status = j.AssignedVehicleId is null ? JobStatus.Pending : JobStatus.Assigned;
        j.Notes = _editNotes.Trim();

        // Job is a plain model; refresh the list row by re-inserting the same instance.
        var index = PendingJobs.IndexOf(j);
        if (index >= 0)
        {
            PendingJobs.RemoveAt(index);
            PendingJobs.Insert(index, j);
            _selectedJob = null;
            SelectedJob = j;
        }

        OnPropertyChanged(nameof(UnassignedCount));
        OnPropertyChanged(nameof(EditorHeading));
        StatusMessage = $"Saved {j.Id}.";
        Dirty();
    }

    private void Cancel()
    {
        LoadEditor();
        StatusMessage = "Changes discarded.";
    }
}
