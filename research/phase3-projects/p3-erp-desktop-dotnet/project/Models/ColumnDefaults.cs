using System.IO;
using System.Text.Json;

namespace ErpClient.Models;

/// <summary>
/// Per-user defaults for the purchase-order lines window: the warehouse new lines start with, and the columns the clerk
/// keeps hidden regardless of window width (the width rule still folds the remaining low-priority columns).
/// Stored as JSON under LocalAppData; <see cref="StorePath"/> = null disables persistence (capture harness, tests).
/// </summary>
public sealed class ColumnDefaults
{
    public string DefaultWarehouse { get; set; } = PurchaseOrderLine.Warehouses[0];
    public List<string> HiddenColumns { get; set; } = new();

    public static string? StorePath { get; set; } =
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "ErpClient", "column-defaults.json");

    public static ColumnDefaults Load()
    {
        try
        {
            if (StorePath != null && File.Exists(StorePath))
                return JsonSerializer.Deserialize<ColumnDefaults>(File.ReadAllText(StorePath)) ?? new ColumnDefaults();
        }
        catch (Exception) { /* unreadable settings fall back to the built-in defaults */ }
        return new ColumnDefaults();
    }

    public void Save()
    {
        if (StorePath == null) return;
        try
        {
            Directory.CreateDirectory(Path.GetDirectoryName(StorePath)!);
            File.WriteAllText(StorePath, JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true }));
        }
        catch (Exception) { /* settings are a convenience; a failed write must not block the clerk */ }
    }

    public ColumnDefaults Clone() => new() { DefaultWarehouse = DefaultWarehouse, HiddenColumns = new List<string>(HiddenColumns) };
}
