using System.Globalization;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;

namespace Erp.Client.Converters;

/// <summary>
/// Formats numbers for table cells with one precision per column and an explicit sign where asked.
/// ConverterParameter: "N0" | "N2" (plain), "+N0" | "+N2" (always signed), "Brush" (negative = critical,
/// positive = success, zero = primary text).
/// </summary>
public sealed class SignedNumberConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language)
    {
        var p = parameter as string ?? "N0";
        var culture = CultureInfo.CurrentCulture;

        if (value is not decimal d)
            return string.Empty;

        if (p == "Brush")
        {
            var key = d < 0 ? "SystemFillColorCriticalBrush" : d > 0 ? "SystemFillColorSuccessBrush" : "TextFillColorPrimaryBrush";
            return Application.Current.Resources.TryGetValue(key, out var b) && b is Brush brush
                ? brush
                : (Brush)Application.Current.Resources["TextFillColorPrimaryBrush"];
        }

        var signed = p.StartsWith('+');
        var format = signed ? p[1..] : p;
        var text = Math.Abs(d).ToString(format, culture);
        if (d < 0) return "−" + text;          // true minus sign, not a hyphen
        if (d > 0 && signed) return "+" + text;
        return text;
    }

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
