using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Media;
using Erp.Client.Models;

namespace Erp.Client.Converters;

/// <summary>
/// Status is carried by text + glyph; colour is a third, redundant cue.
/// ConverterParameter: Text | Glyph | Brush | Name.
/// Brushes are theme resources (SystemFillColorSuccess/Caution/Critical/Neutral) so Dark and High Contrast work.
/// </summary>
public sealed class StatusToPresentationConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language)
    {
        var status = value is AdjustmentStatus s ? s : AdjustmentStatus.Draft;
        var (text, glyph, brushKey) = status switch
        {
            AdjustmentStatus.Draft => ("Draft", "", "TextFillColorSecondaryBrush"),            // pencil
            AdjustmentStatus.PendingApproval => ("Pending", "", "SystemFillColorCautionBrush"),          // clock; full text in the UIA name
            AdjustmentStatus.Posted => ("Posted", "", "SystemFillColorSuccessBrush"),         // check
            AdjustmentStatus.Rejected => ("Rejected", "", "SystemFillColorCriticalBrush"),    // cross
            _ => ("Unknown", "", "TextFillColorSecondaryBrush"),
        };

        return (parameter as string) switch
        {
            "Glyph" => glyph,
            "Brush" => Application.Current.Resources.TryGetValue(brushKey, out var b) && b is Brush brush
                ? brush
                : (Brush)Application.Current.Resources["TextFillColorPrimaryBrush"],
            "Name" => status == AdjustmentStatus.PendingApproval ? "Status: Pending approval" : $"Status: {text}",
            _ => text,
        };
    }

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
