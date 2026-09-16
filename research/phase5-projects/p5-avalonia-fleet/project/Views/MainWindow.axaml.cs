using System.ComponentModel;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Threading;
using FleetDesk.ViewModels;

namespace FleetDesk.Views;

public partial class MainWindow : Window
{
    private bool _closeApproved;
    private DispatchViewModel? _dispatch;
    private IInputElement? _focusBeforePrompt;

    public MainWindow()
    {
        InitializeComponent();
        DataContextChanged += (_, _) => Attach((DataContext as MainWindowViewModel)?.Dispatch);
    }

    private void Attach(DispatchViewModel? dispatch)
    {
        if (_dispatch is not null) _dispatch.PropertyChanged -= OnDispatchPropertyChanged;
        _dispatch = dispatch;
        if (_dispatch is not null) _dispatch.PropertyChanged += OnDispatchPropertyChanged;
    }

    // Focus management for the unsaved-changes prompt: move focus onto the default
    // button when it opens, and return focus to where the user was when it closes.
    private void OnDispatchPropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName != nameof(DispatchViewModel.IsPromptOpen) || _dispatch is null) return;

        if (_dispatch.IsPromptOpen)
        {
            _focusBeforePrompt = FocusManager?.GetFocusedElement();
            Dispatcher.UIThread.Post(() => PromptSaveButton.Focus(NavigationMethod.Directional));
        }
        else
        {
            var target = _focusBeforePrompt;
            _focusBeforePrompt = null;
            Dispatcher.UIThread.Post(() => target?.Focus());
        }
    }

    // Closing the window is one more way to lose an unsaved job; route it through the same guard.
    protected override void OnClosing(WindowClosingEventArgs e)
    {
        if (!_closeApproved && DataContext is MainWindowViewModel vm)
        {
            var allowed = vm.TryClose(() =>
            {
                _closeApproved = true;
                Close();
            });
            if (!allowed) e.Cancel = true;
        }
        base.OnClosing(e);
    }
}
