namespace FleetDesk.Models;

/// <summary>
/// Service scheduling rule used by the Vehicles screen. Interval based: a vehicle is due
/// <see cref="IntervalDays"/> after its last service and overdue once that date has passed.
/// </summary>
public static class ServicePolicy
{
    public const int IntervalDays = 90;

    /// <summary>Vehicles due within this many days are flagged "due soon".</summary>
    public const int DueSoonDays = 14;

    /// <summary>
    /// Fixed "today" so the deterministic sample data, screenshots and render/twin.html always agree.
    /// SampleData.JobDay uses the same date.
    /// </summary>
    public static DateTime Today { get; set; } = new(2026, 9, 9);
}
