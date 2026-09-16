using System.Windows;
using System.Windows.Controls;

namespace ErpClient.Views;

/// <summary>
/// Attached property for progressive column hiding. A column with HideBelow="1180" collapses when the grid is
/// narrower than 1180 DIP, so the least important columns leave first and the essentials (item, description,
/// qty, price, total) keep their width. The user can pin a column back via View › Columns; that overrides the rule.
/// </summary>
public static class ColumnPriority
{
    public static readonly DependencyProperty HideBelowProperty =
        DependencyProperty.RegisterAttached("HideBelow", typeof(double), typeof(ColumnPriority), new PropertyMetadata(0d));

    public static double GetHideBelow(DataGridColumn c) => (double)c.GetValue(HideBelowProperty);
    public static void SetHideBelow(DataGridColumn c, double v) => c.SetValue(HideBelowProperty, v);

    /// <summary>User pinned/unpinned the column explicitly; the width rule no longer applies to it.</summary>
    public static readonly DependencyProperty UserOverrideProperty =
        DependencyProperty.RegisterAttached("UserOverride", typeof(bool), typeof(ColumnPriority), new PropertyMetadata(false));

    public static bool GetUserOverride(DataGridColumn c) => (bool)c.GetValue(UserOverrideProperty);
    public static void SetUserOverride(DataGridColumn c, bool v) => c.SetValue(UserOverrideProperty, v);

    /// <summary>Apply the rule for the given available width; returns how many columns are hidden by the rule.</summary>
    public static int Apply(DataGrid grid, double availableWidth)
    {
        var hidden = 0;
        foreach (var col in grid.Columns)
        {
            var threshold = GetHideBelow(col);
            if (threshold <= 0 || GetUserOverride(col)) { if (col.Visibility != Visibility.Visible) hidden++; continue; }
            var show = availableWidth >= threshold;
            col.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
            if (!show) hidden++;
        }
        return hidden;
    }
}
