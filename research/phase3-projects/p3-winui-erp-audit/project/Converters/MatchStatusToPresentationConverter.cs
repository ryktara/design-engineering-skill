using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;
using Erp.Client.Models;

namespace Erp.Client.Converters;

/// <summary>
/// Same contract as <see cref="StatusToPresentationConverter"/> but for <see cref="MatchStatus"/>:
/// status is carried by text + glyph, colour is a third, redundant cue.
/// ConverterParameter: Text | Glyph | Brush | Name.
/// </summary>
public sealed class MatchStatusToPresentationConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language)
    {
        var status = value is MatchStatus s ? s : MatchStatus.Unmatched;
        var (text, glyph, brushKey, name) = status switch
        {
            MatchStatus.Unmatched => ("Unmatched", "", "TextFillColorSecondaryBrush", "Status: Not matched"),
            MatchStatus.PriceVariance => ("Price", "", "SystemFillColorCautionBrush", "Status: Price variance"),
            MatchStatus.QuantityVariance => ("Quantity", "", "SystemFillColorCautionBrush", "Status: Quantity variance"),
            MatchStatus.Matched => ("Matched", "", "SystemFillColorSuccessBrush", "Status: Matched"),
            MatchStatus.OnHold => ("On hold", "", "SystemFillColorCriticalBrush", "Status: On hold"),
            _ => ("Unknown", "", "TextFillColorSecondaryBrush", "Status: Unknown"),
        };

        return (parameter as string) switch
        {
            "Glyph" => glyph,
            "Brush" => Application.Current.Resources.TryGetValue(brushKey, out var b) && b is Brush brush
                ? brush
                : (Brush)Application.Current.Resources["TextFillColorPrimaryBrush"],
            "Name" => name,
            _ => text,
        };
    }

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
