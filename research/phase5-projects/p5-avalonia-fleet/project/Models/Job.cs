namespace FleetDesk.Models;

public enum JobPriority
{
    Low,
    Normal,
    High
}

public enum JobStatus
{
    Pending,
    Assigned,
    InProgress,
    Done
}

public sealed class Job
{
    public required string Id { get; init; }
    public string Title { get; set; } = "";
    public string Customer { get; set; } = "";
    public string Pickup { get; set; } = "";
    public string Dropoff { get; set; } = "";
    public DateTime ScheduledAt { get; set; }
    public JobPriority Priority { get; set; } = JobPriority.Normal;
    public JobStatus Status { get; set; } = JobStatus.Pending;
    /// <summary>Vehicle id (e.g. "V-102") or null when unassigned.</summary>
    public string? AssignedVehicleId { get; set; }
    public string Notes { get; set; } = "";

    public string ScheduledLabel => ScheduledAt.ToString("ddd HH:mm");
    public string AssignmentLabel => AssignedVehicleId ?? "Unassigned";
    public bool IsHighPriority => Priority == JobPriority.High;
    public bool IsNormalPriority => Priority == JobPriority.Normal;

    public Job Clone() => new()
    {
        Id = Id,
        Title = Title,
        Customer = Customer,
        Pickup = Pickup,
        Dropoff = Dropoff,
        ScheduledAt = ScheduledAt,
        Priority = Priority,
        Status = Status,
        AssignedVehicleId = AssignedVehicleId,
        Notes = Notes
    };
}
