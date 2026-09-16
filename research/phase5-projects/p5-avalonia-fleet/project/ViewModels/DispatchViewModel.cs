using System.Collections.ObjectModel;
using Avalonia.Threading;
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

    // Unsaved-changes guard: the action that was interrupted (select another job,
    // leave the view, close the window) waits here until the user decides.
    private bool _isPromptOpen;
    private string _promptMessage = "";
    private Action? _pendingLeave;

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

        PromptSaveCommand = new RelayCommand(PromptSave, () => IsPromptOpen);
        PromptDiscardCommand = new RelayCommand(PromptDiscard, () => IsPromptOpen);
        PromptKeepEditingCommand = new RelayCommand(PromptKeepEditing, () => IsPromptOpen);

        SelectedJob = PendingJobs.FirstOrDefault();
    }

    public ObservableCollection<Job> PendingJobs { get; }
    public string[] Priorities { get; }
    public string[] VehicleChoices { get; }

    public RelayCommand SaveCommand { get; }
    public RelayCommand CancelCommand { get; }
    public RelayCommand PromptSaveCommand { get; }
    public RelayCommand PromptDiscardCommand { get; }
    public RelayCommand PromptKeepEditingCommand { get; }

    public Job? SelectedJob
    {
        get => _selectedJob;
        set
        {
            if (ReferenceEquals(_selectedJob, value)) return;

            // Guard: never drop edits because a different row was clicked.
            // Keep the dirty job selected, ask, and re-apply the click once answered.
            if (HasChanges && value is not null)
            {
                var target = value;
                OpenPrompt($"switching to {target.Id} - {target.Title}", () => ApplySelection(target));
                // The ListBox already moved its own selection; push the old value back
                // after the binding finishes so the list shows the job still being edited.
                Dispatcher.UIThread.Post(() => OnPropertyChanged(nameof(SelectedJob)));
                return;
            }

            ApplySelection(value);
        }
    }

    private void ApplySelection(Job? value)
    {
        if (SetProperty(ref _selectedJob, value, nameof(SelectedJob)))
        {
            LoadEditor();
            OnPropertyChanged(nameof(HasSelection));
            OnPropertyChanged(nameof(EditorHeading));
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
    public string EditVehicleId
    {
        get => _editVehicleId;
        set
        {
            if (SetProperty(ref _editVehicleId, value))
            {
                // Driver is derived from the vehicle record; it is never entered on this form.
                OnPropertyChanged(nameof(DriverLabel));
                OnPropertyChanged(nameof(DriverDetail));
                Dirty();
            }
        }
    }

    /// <summary>
    /// Driver for the currently selected vehicle. Read-only and derived from
    /// <see cref="Vehicle.Driver"/> so the dispatcher never types driver details that the
    /// fleet record already holds.
    /// </summary>
    public Vehicle? SelectedVehicle =>
        _editVehicleId == Unassigned ? null : SampleData.Vehicles.FirstOrDefault(v => v.Id == _editVehicleId);

    public string DriverLabel => SelectedVehicle?.Driver ?? "No driver - vehicle unassigned";

    /// <summary>Secondary line under the driver name: plate and vehicle status.</summary>
    public string DriverDetail
    {
        get
        {
            var v = SelectedVehicle;
            return v is null
                ? "Assign a vehicle to see its driver."
                : $"{v.Plate} - {v.StatusLabel}";
        }
    }

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

    /// <summary>Short text for the status bar: "Unsaved changes - J-2041" or "" when clean.</summary>
    public string UnsavedLabel => HasChanges && _selectedJob is not null ? $"Unsaved changes - {_selectedJob.Id}" : "";

    // ----- Unsaved-changes prompt -----

    public bool IsPromptOpen
    {
        get => _isPromptOpen;
        private set
        {
            if (SetProperty(ref _isPromptOpen, value))
            {
                PromptSaveCommand?.RaiseCanExecuteChanged();
                PromptDiscardCommand?.RaiseCanExecuteChanged();
                PromptKeepEditingCommand?.RaiseCanExecuteChanged();
            }
        }
    }

    public string PromptTitle => "Unsaved changes";

    public string PromptMessage
    {
        get => _promptMessage;
        private set => SetProperty(ref _promptMessage, value);
    }

    /// <summary>
    /// Run <paramref name="leave"/> now if nothing is unsaved; otherwise open the prompt and
    /// run it only after the user chooses Save or Discard. Returns true when it ran immediately.
    /// </summary>
    public bool TryLeave(string destination, Action leave)
    {
        if (!HasChanges)
        {
            leave();
            return true;
        }
        OpenPrompt(destination, leave);
        return false;
    }

    private void OpenPrompt(string destination, Action leave)
    {
        var j = _selectedJob!;
        _pendingLeave = leave;
        PromptMessage = $"{j.Id} - {j.Title} has unsaved changes. Save them before {destination}?";
        IsPromptOpen = true;
    }

    private void PromptSave()
    {
        var leave = _pendingLeave;
        Save();
        ClosePrompt();
        leave?.Invoke();
    }

    private void PromptDiscard()
    {
        var leave = _pendingLeave;
        LoadEditor();
        StatusMessage = "Changes discarded.";
        ClosePrompt();
        leave?.Invoke();
    }

    private void PromptKeepEditing()
    {
        ClosePrompt();
    }

    private void ClosePrompt()
    {
        _pendingLeave = null;
        IsPromptOpen = false;
    }

    // ----- Editor -----

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
                     nameof(EditPriority), nameof(EditVehicleId), nameof(EditNotes),
                     nameof(DriverLabel), nameof(DriverDetail)
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
        OnPropertyChanged(nameof(UnsavedLabel));
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
