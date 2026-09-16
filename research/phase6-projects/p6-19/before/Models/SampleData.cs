namespace ErpClient.Models;

/// <summary>Deterministic sample lines for PO-2026-004417 (a real ERP client would load these from the API).</summary>
public static class SampleData
{
    private static readonly (string code, string desc, decimal qty, string unit, decimal price, decimal disc, string wh, int days, LineStatus st, string notes)[] Rows =
    [
        ("STL-RB-12",  "Rebar 12 mm deformed, 12 m",              240, "EA",  14.75m, 0,   "DXB-01 Main", 7,  LineStatus.Approved, ""),
        ("STL-RB-16",  "Rebar 16 mm deformed, 12 m",              160, "EA",  26.10m, 2.5m,"DXB-01 Main", 7,  LineStatus.Approved, "Mill cert required"),
        ("CEM-OPC-50", "Cement OPC 42.5N, 50 kg bag",             800, "EA",  13.20m, 5,   "SHJ-Bulk",    5,  LineStatus.Ordered,  ""),
        ("AGG-20MM",   "Aggregate 20 mm crushed",                 36,  "M",   58.00m, 0,   "SHJ-Bulk",    5,  LineStatus.Ordered,  "Per m³; delivery in 12 m³ loads"),
        ("SND-WASH",   "Washed sand, fine",                       24,  "M",   42.50m, 0,   "SHJ-Bulk",    5,  LineStatus.Draft,    ""),
        ("PLY-18-FF",  "Plywood 18 mm film-faced 1220×2440",      120, "EA",  92.00m, 8,   "DXB-01 Main", 10, LineStatus.Draft,    ""),
        ("TMB-2X4",    "Timber 50×100 mm, 4 m",                   300, "EA",  18.40m, 0,   "DXB-01 Main", 10, LineStatus.Draft,    ""),
        ("NAIL-75",    "Wire nails 75 mm",                        40,  "BOX", 21.00m, 0,   "DXB-01 Main", 10, LineStatus.Draft,    "25 kg box"),
        ("BW-3X3",     "Binding wire 3 mm",                       15,  "ROLL",38.90m, 0,   "DXB-01 Main", 7,  LineStatus.Received, ""),
        ("PVC-110",    "uPVC pipe 110 mm SN4, 6 m",               90,  "EA",  47.30m, 3,   "AUH-01",      14, LineStatus.Approved, ""),
        ("PVC-ELB-110","uPVC elbow 110 mm 90°",                   180, "EA",  6.85m,  3,   "AUH-01",      14, LineStatus.Approved, ""),
        ("PVC-SOL",    "Solvent cement 500 ml",                   24,  "EA",  19.90m, 0,   "AUH-01",      14, LineStatus.Approved, "Hazmat — separate delivery note"),
        ("CBL-4C-16",  "Cable 4C×16 mm² XLPE/SWA/PVC",            2,   "ROLL",2_480.00m, 4, "RUH-01",     21, LineStatus.Ordered,  "500 m drums"),
        ("CBL-3C-2.5", "Cable 3C×2.5 mm² PVC",                    12,  "ROLL",312.00m, 4,  "RUH-01",      21, LineStatus.Ordered,  ""),
        ("CDT-25",     "Conduit 25 mm PVC, 3 m",                  400, "EA",  4.15m,  0,   "RUH-01",      21, LineStatus.Ordered,  ""),
        ("DB-12W",     "Distribution board 12-way TP",            6,   "EA",  640.00m, 10, "RUH-01",      28, LineStatus.Draft,    "Schneider or ABB"),
        ("MCB-32",     "MCB 32 A C-curve 1P",                     72,  "EA",  11.60m, 10,  "RUH-01",      28, LineStatus.Draft,    ""),
        ("PNT-EMU-20", "Emulsion paint white, 20 L",              45,  "EA",  118.00m, 6,  "DXB-02 Cold", 30, LineStatus.Draft,    "Store below 30 °C"),
        ("PNT-PRM-20", "Primer sealer, 20 L",                     30,  "EA",  96.50m, 6,   "DXB-02 Cold", 30, LineStatus.Draft,    ""),
        ("TIL-60-GL",  "Porcelain tile 600×600 glazed, box of 4", 210, "BOX", 74.00m, 12,  "DXB-01 Main", 35, LineStatus.Draft,    "Batch-matched"),
        ("GRT-WHT-5",  "Tile grout white, 5 kg",                  60,  "EA",  17.25m, 0,   "DXB-01 Main", 35, LineStatus.Draft,    ""),
        ("ADH-C2-25",  "Tile adhesive C2TE, 25 kg",               140, "EA",  28.40m, 0,   "DXB-01 Main", 35, LineStatus.Draft,    ""),
        ("SAF-HLM",    "Safety helmet, vented",                   50,  "EA",  22.00m, 0,   "DXB-01 Main", 3,  LineStatus.Received, ""),
        ("SAF-GLV-L",  "Nitrile gloves L, box of 100",            20,  "BOX", 34.90m, 0,   "DXB-01 Main", 3,  LineStatus.Cancelled,"Replaced by SAF-GLV-XL"),
    ];

    public static List<PurchaseOrderLine> Lines()
    {
        var list = new List<PurchaseOrderLine>(Rows.Length);
        var n = 1;
        foreach (var r in Rows)
        {
            var line = new PurchaseOrderLine
            {
                LineNo = n++ * 10,
                ItemCode = r.code,
                Description = r.desc,
                Quantity = r.qty,
                Unit = r.unit,
                UnitPrice = r.price,
                DiscountPct = r.disc,
                TaxPct = 5,
                Warehouse = r.wh,
                RequestedDate = DateTime.Today.AddDays(r.days),
                Status = r.st,
                Notes = r.notes,
            };
            line.AcceptChanges();
            list.Add(line);
        }
        // Two deliberately invalid rows so the validation state is visible in sample data.
        list[4].Quantity = 0;                                  // "Quantity must be greater than 0"
        list[15].RequestedDate = DateTime.Today.AddDays(-2);   // "Requested date is in the past"
        return list;
    }
}
