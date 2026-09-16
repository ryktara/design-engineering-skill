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

/// <summary>
/// Marks the column that holds the current cell so its header can show a 2 px bar + primary text: operators who land one
/// column too far right (quantity typed into the price column) see it at the top of the grid, not only from the cell ring.
/// </summary>
public static class ActiveColumn
{
    public static readonly DependencyProperty IsCurrentProperty =
        DependencyProperty.RegisterAttached("IsCurrent", typeof(bool), typeof(ActiveColumn), new PropertyMetadata(false));

    public static bool GetIsCurrent(DataGridColumn c) => (bool)c.GetValue(IsCurrentProperty);
    public static void SetIsCurrent(DataGridColumn c, bool v) => c.SetValue(IsCurrentProperty, v);

    /// <summary>Flags <paramref name="current"/> (or none) and clears every other column.</summary>
    public static void Apply(DataGrid grid, DataGridColumn? current)
    {
        foreach (var col in grid.Columns)
        {
            var on = ReferenceEquals(col, current);
            if (GetIsCurrent(col) != on) SetIsCurrent(col, on);
        }
    }
}

/// <summary>
/// Column-group edges drawn as a 1 px strong line by the header and cell templates: Edge="Start" on the first column of a
/// group, Edge="End" on the last, so the money columns (unit price … line total) read as one block next to the quantity block.
/// </summary>
public static class ColumnGroup
{
    public static readonly DependencyProperty EdgeProperty =
        DependencyProperty.RegisterAttached("Edge", typeof(string), typeof(ColumnGroup), new PropertyMetadata(""));

    public static string GetEdge(DataGridColumn c) => (string)c.GetValue(EdgeProperty);
    public static void SetEdge(DataGridColumn c, string v) => c.SetValue(EdgeProperty, v);
}

/// <summary>
/// Affix text shown inside a cell editor (unit after a quantity, currency before a price) so the value being typed is
/// labelled where the eye is. Set on the editing TextBox style; the Edit.Cell.Affix template renders whichever is non-empty.
/// </summary>
public static class Affix
{
    public static readonly DependencyProperty PrefixProperty =
        DependencyProperty.RegisterAttached("Prefix", typeof(string), typeof(Affix), new PropertyMetadata(""));
    public static readonly DependencyProperty SuffixProperty =
        DependencyProperty.RegisterAttached("Suffix", typeof(string), typeof(Affix), new PropertyMetadata(""));

    public static string GetPrefix(DependencyObject d) => (string)d.GetValue(PrefixProperty);
    public static void SetPrefix(DependencyObject d, string v) => d.SetValue(PrefixProperty, v);
    public static string GetSuffix(DependencyObject d) => (string)d.GetValue(SuffixProperty);
    public static void SetSuffix(DependencyObject d, string v) => d.SetValue(SuffixProperty, v);
}
