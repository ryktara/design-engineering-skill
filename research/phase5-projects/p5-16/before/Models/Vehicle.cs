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
}
