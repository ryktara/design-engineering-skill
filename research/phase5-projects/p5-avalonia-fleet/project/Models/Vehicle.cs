namespace FleetDesk.Models;

public enum VehicleStatus
{
    Available,
    OnJob,
    Maintenance,
    OutOfService
}

public sealed class Vehicle
{
    public required string Id { get; init; }
    public required string Plate { get; init; }
    public required string Driver { get; init; }
    public required VehicleStatus Status { get; init; }
    public required int OdometerKm { get; init; }
    public required DateTime LastService { get; init; }

    /// <summary>Human-readable status for grid display ("On job" instead of "OnJob").</summary>
    public string StatusLabel => Status switch
    {
        VehicleStatus.Available => "Available",
        VehicleStatus.OnJob => "On job",
        VehicleStatus.Maintenance => "Maintenance",
        VehicleStatus.OutOfService => "Out of service",
        _ => Status.ToString()
    };

    // ----- Service schedule (see ServicePolicy) -----

    public DateTime NextServiceDue => LastService.AddDays(ServicePolicy.IntervalDays);

    /// <summary>Positive = days past the due date; zero or negative = days until due.</summary>
    public int DaysPastDue => (int)(ServicePolicy.Today.Date - NextServiceDue.Date).TotalDays;

    public bool IsServiceOverdue => DaysPastDue > 0;

    public bool IsServiceDueSoon => !IsServiceOverdue && -DaysPastDue <= ServicePolicy.DueSoonDays;

    /// <summary>True when the row deserves a badge (overdue or due soon).</summary>
    public bool NeedsServiceAttention => IsServiceOverdue || IsServiceDueSoon;

    /// <summary>Text for the Service column. Always words, never colour alone.</summary>
    public string ServiceLabel => IsServiceOverdue
        ? $"Overdue {DaysPastDue} d"
        : IsServiceDueSoon
            ? (DaysPastDue == 0 ? "Due today" : $"Due in {-DaysPastDue} d")
            : "OK";
}
