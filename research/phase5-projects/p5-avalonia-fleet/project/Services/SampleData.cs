using FleetDesk.Models;

namespace FleetDesk.Services;

/// <summary>
/// Deterministic sample data. No randomness: the same 30 vehicles and 8 jobs every run,
/// so screenshots and the HTML twin (render/twin.html) always match.
/// </summary>
public static class SampleData
{
    public const string DepotName = "North Depot";

    private static readonly DateTime JobDay = ServicePolicy.Today;

    public static IReadOnlyList<Vehicle> Vehicles { get; } = new List<Vehicle>
    {
        V("V-101", "KA-7731", "Amira Haddad",    VehicleStatus.Available,    48210,  "2026-07-14"),
        V("V-102", "KB-2204", "Tomasz Wrona",    VehicleStatus.OnJob,        91340,  "2026-05-02"),
        V("V-103", "KC-9187", "Priya Nair",      VehicleStatus.Maintenance,  132870, "2026-08-28"),
        V("V-104", "KD-4410", "Luis Ortega",     VehicleStatus.Available,    27650,  "2026-08-03"),
        V("V-105", "KE-6602", "Chen Wei",        VehicleStatus.OnJob,        66120,  "2026-06-19"),
        V("V-106", "KF-1178", "Fatima Zahra",    VehicleStatus.OutOfService, 154900, "2026-02-11"),
        V("V-107", "KG-3350", "Daniel Reyes",    VehicleStatus.Available,    39480,  "2026-07-30"),
        V("V-108", "KH-8821", "Yuki Tanaka",     VehicleStatus.OnJob,        72310,  "2026-06-05"),
        V("V-109", "KJ-5573", "Olga Petrova",    VehicleStatus.Available,    18930,  "2026-08-21"),
        V("V-110", "KK-2096", "Samuel Okafor",   VehicleStatus.Maintenance,  118400, "2026-08-30"),
        V("V-111", "KL-7315", "Hana Kim",        VehicleStatus.OnJob,        84770,  "2026-05-27"),
        V("V-112", "KM-4482", "Marco Bianchi",   VehicleStatus.Available,    55210,  "2026-07-08"),
        V("V-113", "KN-9930", "Leila Mansour",   VehicleStatus.OnJob,        97650,  "2026-04-16"),
        V("V-114", "KP-1264", "Jonas Berg",      VehicleStatus.Available,    31080,  "2026-08-12"),
        V("V-115", "KR-6619", "Aisha Bello",     VehicleStatus.Maintenance,  143220, "2026-09-01"),
        V("V-116", "KS-3808", "Ravi Shankar",    VehicleStatus.OnJob,        60940,  "2026-06-24"),
        V("V-117", "KT-7147", "Emma Lindqvist",  VehicleStatus.Available,    22370,  "2026-08-25"),
        V("V-118", "KU-2953", "Omar Farouk",     VehicleStatus.OnJob,        108560, "2026-03-30"),
        V("V-119", "KV-8476", "Sofia Rossi",     VehicleStatus.Available,    45830,  "2026-07-19"),
        V("V-120", "KW-5061", "Ibrahim Diallo",  VehicleStatus.OutOfService, 167310, "2026-01-22"),
        V("V-121", "KX-1392", "Mei Ling",        VehicleStatus.Available,    36720,  "2026-08-06"),
        V("V-122", "KY-6748", "Pedro Alves",     VehicleStatus.OnJob,        79140,  "2026-05-13"),
        V("V-123", "KZ-2285", "Nadia Suleiman",  VehicleStatus.Available,    14560,  "2026-08-27"),
        V("V-124", "LA-9034", "Viktor Novak",    VehicleStatus.Maintenance,  126980, "2026-08-29"),
        V("V-125", "LB-4517", "Grace Mwangi",    VehicleStatus.OnJob,        88420,  "2026-04-28"),
        V("V-126", "LC-8802", "Ahmed Khalil",    VehicleStatus.Available,    51290,  "2026-07-11"),
        V("V-127", "LD-3179", "Ingrid Hansen",   VehicleStatus.OnJob,        69830,  "2026-06-10"),
        V("V-128", "LE-7726", "Carlos Mendez",   VehicleStatus.Available,    29410,  "2026-08-15"),
        V("V-129", "LF-1450", "Zainab Rahman",   VehicleStatus.Maintenance,  137650, "2026-08-31"),
        V("V-130", "LG-6093", "Kenji Sato",      VehicleStatus.Available,    42180,  "2026-07-24"),
    };

    /// <summary>Fresh (mutable) copies of the pending jobs so the Dispatch screen can edit them.</summary>
    public static List<Job> CreatePendingJobs() => new()
    {
        J("J-2041", "Pallet delivery - Al Quoz", "Nour Trading LLC",         "North Depot",     "Al Quoz Industrial 3",   "08:30", JobPriority.High,   "V-102", "12 pallets, forklift on site."),
        J("J-2042", "Cold-chain pickup",         "Fresh Farms Co.",          "Jebel Ali Port",  "North Depot",            "09:15", JobPriority.High,   "V-105", "Reefer unit must be pre-cooled to 4 C."),
        J("J-2043", "Office relocation",         "Meridian Consulting",      "DIFC Gate 4",     "Business Bay Tower 2",   "10:00", JobPriority.Normal, null,    "Two-person crew requested."),
        J("J-2044", "Spare parts run",           "Workshop 7",               "South Depot",     "Ras Al Khor",            "11:30", JobPriority.Low,    "V-108", ""),
        J("J-2045", "Return empties",            "Al Ain Water",             "Al Barsha South", "North Depot",            "13:00", JobPriority.Normal, null,    "Collect 40 empty 5-gallon bottles."),
        J("J-2046", "Site materials drop",       "Bright Build Contracting", "South Depot",     "Dubai South Plot 41",    "14:15", JobPriority.High,   "V-111", "Gate pass required; call site manager on arrival."),
        J("J-2047", "Document courier",          "Harbor Legal",             "North Depot",     "Deira Clock Tower",      "15:00", JobPriority.Low,    null,    "Signature required."),
        J("J-2048", "Generator transfer",        "Coastal Events",           "South Depot",     "JBR Beach Stage",        "16:30", JobPriority.Normal, "V-113", "Flatbed only."),
    };

    private static Vehicle V(string id, string plate, string driver, VehicleStatus status, int odometer, string lastService) => new()
    {
        Id = id,
        Plate = plate,
        Driver = driver,
        Status = status,
        OdometerKm = odometer,
        LastService = DateTime.Parse(lastService, System.Globalization.CultureInfo.InvariantCulture)
    };

    private static Job J(string id, string title, string customer, string pickup, string dropoff, string time, JobPriority priority, string? vehicleId, string notes)
    {
        var t = TimeSpan.Parse(time, System.Globalization.CultureInfo.InvariantCulture);
        return new Job
        {
            Id = id,
            Title = title,
            Customer = customer,
            Pickup = pickup,
            Dropoff = dropoff,
            ScheduledAt = JobDay + t,
            Priority = priority,
            Status = vehicleId is null ? JobStatus.Pending : JobStatus.Assigned,
            AssignedVehicleId = vehicleId,
            Notes = notes
        };
    }
}
