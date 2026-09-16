using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;

namespace Erp.Client.ViewModels;

/// <summary>
/// ObservableCollection that can be refilled with one Reset notification instead of one
/// notification per item. Clear() + n * Add() on a collection bound to a DataGrid makes the
/// grid re-measure and re-realise rows n times; at 3,000 rows every keystroke in the search
/// box froze the UI thread. Reset lets the grid rebuild its viewport exactly once.
/// </summary>
public sealed class BulkObservableCollection<T> : ObservableCollection<T>
{
    public void Reset(IEnumerable<T> items)
    {
        CheckReentrancy();
        Items.Clear();
        foreach (var item in items) Items.Add(item);
        OnPropertyChanged(new PropertyChangedEventArgs(nameof(Count)));
        OnPropertyChanged(new PropertyChangedEventArgs("Item[]"));
        OnCollectionChanged(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset));
    }
}
