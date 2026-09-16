using Microsoft.UI.Xaml.Data;

namespace Erp.Client.Converters;

/// <summary>Builds a per-row accessible name for icon-only row buttons: "Approve ADJ-10421".</summary>
public sealed class RowActionNameConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language) =>
        $"{parameter as string ?? "Open"} {value}";

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
