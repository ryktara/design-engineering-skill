using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Data;

namespace Erp.Client.Converters;

public sealed class CountToVisibilityConverter : IValueConverter
{
    public bool ZeroIsVisible { get; set; }

    public object Convert(object value, Type targetType, object parameter, string language)
    {
        var count = value is int i ? i : 0;
        var isZero = count == 0;
        return (isZero == ZeroIsVisible) ? Visibility.Visible : Visibility.Collapsed;
    }

    public object ConvertBack(object value, Type targetType, object parameter, string language) =>
        throw new NotSupportedException();
}
