using System.IO;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using ErpClient.Models;
using ErpClient.ViewModels;
using ErpClient.Views;

namespace ErpClient;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        ShutdownMode = ShutdownMode.OnMainWindowClose;
        var args = e.Args;
        var captureIdx = Array.IndexOf(args, "--capture");
        if (captureIdx >= 0 && captureIdx + 1 < args.Length)
        {
            var dir = args[captureIdx + 1];
            DispatcherUnhandledException += (_, ex) => { File.AppendAllText(Path.Combine(dir, "capture-error.log"), ex.Exception + Environment.NewLine); ex.Handled = true; Shutdown(2); };
            _ = RunCaptureAsync(args, dir).ContinueWith(t =>
            {
                if (t.IsFaulted) { File.AppendAllText(Path.Combine(dir, "capture-error.log"), t.Exception + Environment.NewLine); Dispatcher.Invoke(() => Shutdown(2)); }
            });
            return;
        }
        new MainWindow().Show();
    }

    // =====================================================================================
    // Capture / interaction-test mode:  ErpClient.exe --capture <dir> [--size 1440x900] [--state ready|loading|empty|error] [--scenario keys] [--prefix first]
    // Renders the window to PNG (RenderTargetBitmap, client area, actual DPI) and, with --scenario keys, drives the grid
    // with real OS keyboard input (keybd_event) and writes a JSON trace of what the grid did after each key.
    // =====================================================================================

    private static string Arg(string[] a, string name, string dflt)
    { var i = Array.IndexOf(a, name); return i >= 0 && i + 1 < a.Length ? a[i + 1] : dflt; }

    private async Task RunCaptureAsync(string[] args, string outDir)
    {
        Directory.CreateDirectory(outDir);
        var size = Arg(args, "--size", "1440x900").Split('x');
        var w = double.Parse(size[0]); var h = double.Parse(size[1]);
        var state = Arg(args, "--state", "ready");
        var scenario = Arg(args, "--scenario", "none");
        var prefix = Arg(args, "--prefix", "first");
        var log = new List<string>();

        var vm = new PurchaseOrderLinesViewModel { SimulateFailure = state == "error" };
        var win = new MainWindow(vm, autoLoad: false) { Width = w, Height = h, WindowStartupLocation = WindowStartupLocation.Manual, Left = 0, Top = 0 };
        MainWindow = win;
        win.Show();
        win.Activate();
        SetForegroundWindow(new WindowInteropHelper(win).Handle);

        if (state == "loading") _ = vm.LoadAsync(delayMs: 600_000);
        else await vm.LoadAsync(delayMs: 0, empty: state == "empty");

        await Idle(); await Task.Delay(400); await Idle();
        var view = win.LinesView;
        if (state == "ready") { view.FocusFirstCell(); await Idle(); }

        var tag = $"{prefix}-{state}-{(int)w}x{(int)h}";
        Save(win, Path.Combine(outDir, tag + ".png"));
        log.Add($"captured {tag}.png (client area {win.ActualWidth}x{win.ActualHeight}, active={win.IsActive})");

        var result = new Dictionary<string, object?>
        {
            ["size"] = $"{(int)w}x{(int)h}", ["state"] = state, ["windowActive"] = win.IsActive,
            ["layout"] = LayoutProbe(win, view),
            ["hiddenColumns"] = vm.HiddenColumnCount,
            ["visibleColumns"] = view.Grid.Columns.Where(c => c.Visibility == Visibility.Visible).Select(c => c.Header?.ToString()).ToArray(),
        };

        if (scenario == "keys" && state == "ready")
            result["interaction"] = await RunKeyScenarioAsync(win, view, vm, outDir, prefix, log);
        if (scenario == "select" && state == "ready")
        {
            var grid = view.Grid; var diag = new List<string>();
            async Task P(byte vk, bool shift) { if (shift) keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero); keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY, UIntPtr.Zero); keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, UIntPtr.Zero); if (shift) keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero); await Task.Delay(80); await Idle(); }
            diag.Add($"start sel={grid.SelectedItems.Count} cur={grid.Items.IndexOf(grid.CurrentCell.Item)}");
            await P(VK_DOWN, false); diag.Add($"Down sel={grid.SelectedItems.Count} cur={grid.Items.IndexOf(grid.CurrentCell.Item)} mods={Keyboard.Modifiers}");
            keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero); await Task.Delay(50); await Idle(); diag.Add($"shift held: mods={Keyboard.Modifiers} shiftDown={Keyboard.IsKeyDown(Key.LeftShift)}");
            keybd_event(VK_DOWN, 0, KEYEVENTF_EXTENDEDKEY, UIntPtr.Zero); keybd_event(VK_DOWN, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, UIntPtr.Zero); await Task.Delay(80); await Idle();
            diag.Add($"Shift+Down sel={grid.SelectedItems.Count} cur={grid.Items.IndexOf(grid.CurrentCell.Item)} mods={Keyboard.Modifiers}");
            keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero); await Task.Delay(50); await Idle();
            result["selectDiag"] = diag;
        }

        result["log"] = log;
        File.WriteAllText(Path.Combine(outDir, tag + ".json"), JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
        Shutdown(0);
    }

    private async Task<object> RunKeyScenarioAsync(MainWindow win, PurchaseOrderLinesView view, PurchaseOrderLinesViewModel vm, string outDir, string prefix, List<string> log)
    {
        var grid = view.Grid;
        var useOs = win.IsActive;
        var steps = new List<Dictionary<string, object?>>();
        var focusBrush = ((SolidColorBrush)win.FindResource("Brush.Focus.Ring")).Color;

        Dictionary<string, object?> Snap(string step, string keys)
        {
            var cellInfo = grid.CurrentCell;
            var rowIdx = cellInfo.IsValid ? grid.Items.IndexOf(cellInfo.Item) : -1;
            var col = cellInfo.IsValid ? cellInfo.Column : null;
            DataGridCell? cell = rowIdx >= 0 && col != null ? view.GetCell(rowIdx, col) : null;
            var focused = Keyboard.FocusedElement as DependencyObject;
            var ringVisible = cell != null && cell.IsKeyboardFocusWithin && cell.BorderBrush is SolidColorBrush b && b.Color == focusBrush && cell.BorderThickness.Left >= 2;
            var header = PurchaseOrderLinesView.FindChild<DataGridColumnHeadersPresenter>(grid);
            double headerTop = double.NaN;
            if (header != null && header.IsVisible) headerTop = header.TransformToAncestor(win).Transform(new Point(0, 0)).Y;
            var sv = PurchaseOrderLinesView.FindChild<ScrollViewer>(grid);
            var line = cellInfo.IsValid ? cellInfo.Item as PurchaseOrderLine : null;
            return new Dictionary<string, object?>
            {
                ["step"] = step, ["keys"] = keys, ["row"] = rowIdx, ["column"] = col?.Header?.ToString(),
                ["editing"] = view.IsEditing, ["focusedElement"] = focused?.GetType().Name,
                ["focusRingVisible"] = ringVisible, ["selectedRows"] = grid.SelectedItems.Count,
                ["headerTopY"] = double.IsNaN(headerTop) ? null : Math.Round(headerTop, 1), ["verticalOffset"] = sv?.VerticalOffset,
                ["currentLineNo"] = line?.LineNo, ["currentQty"] = line?.Quantity, ["lineCount"] = vm.LineCount,
                ["focusedError"] = vm.FocusedError,
            };
        }

        async Task Press(params (byte vk, bool shift, bool ctrl)[] keys)
        {
            foreach (var (vk, shift, ctrl) in keys)
            {
                if (useOs)
                {
                    if (shift) keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
                    if (ctrl) keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
                    // Arrows/Home/End/Ins/Del must be sent as extended keys; otherwise Windows treats them as numpad keys and
                    // injects a fake Shift release around Shift+numpad combinations.
                    var ext = vk is VK_LEFT or VK_UP or VK_RIGHT or VK_DOWN or VK_HOME or VK_END or 0x2D or 0x2E ? KEYEVENTF_EXTENDEDKEY : 0u;
                    keybd_event(vk, 0, ext, UIntPtr.Zero); keybd_event(vk, 0, ext | KEYEVENTF_KEYUP, UIntPtr.Zero);
                    if (ctrl) keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
                    if (shift) keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
                }
                else InjectWpfKey(KeyInterop.KeyFromVirtualKey(vk));
                await Task.Delay(70); await Idle();
            }
        }

        static (byte, bool, bool) K(byte vk) => (vk, false, false);

        log.Add(useOs ? "input: real OS keyboard (keybd_event) into the active window" : "input: window not active; falling back to WPF InputManager injection (no modifiers)");
        steps.Add(Snap("start: first cell focused", ""));

        await Press(K(VK_DOWN), K(VK_DOWN));
        steps.Add(Snap("arrow down x2", "Down Down"));
        await Press(K(VK_RIGHT), K(VK_RIGHT));
        steps.Add(Snap("arrow right x2 (should be Qty)", "Right Right"));
        Save(win, Path.Combine(outDir, $"{prefix}-focus-cell.png"));

        await Press(K(VK_F2));
        steps.Add(Snap("F2 begins edit", "F2"));
        Save(win, Path.Combine(outDir, $"{prefix}-editing.png"));
        await Press(K(VK_END), K((byte)'1'), K((byte)'2'));
        steps.Add(Snap("typed 12 appended", "End 1 2"));
        var rowBefore = grid.Items.IndexOf(grid.CurrentCell.Item);
        var lineBefore = grid.CurrentCell.Item as PurchaseOrderLine;
        await Press(K(VK_RETURN));
        var s = Snap("Enter commits and moves down", "Enter");
        s["rowBefore"] = rowBefore; s["committedQtyOfPreviousRow"] = lineBefore?.Quantity; s["previousRowDirty"] = lineBefore?.IsDirty;
        steps.Add(s);

        await Press(K(VK_TAB));
        steps.Add(Snap("Tab moves right (commits)", "Tab"));
        await Press((VK_TAB, true, false));
        steps.Add(Snap("Shift+Tab moves left", "Shift+Tab"));

        // type-to-edit then Escape cancels
        var qtyBefore = (grid.CurrentCell.Item as PurchaseOrderLine)?.Quantity;
        await Press(K((byte)'9'), K((byte)'9'));
        steps.Add(Snap("type-to-edit starts editing", "9 9"));
        await Press(K(VK_ESCAPE));
        s = Snap("Escape cancels edit", "Esc"); s["qtyBefore"] = qtyBefore; steps.Add(s);

        // Tab from an editing cell must NOT leave the next cell in edit mode
        await Press(K(VK_F2), K(VK_TAB));
        s = Snap("F2 then Tab: next cell focused, not editing", "F2 Tab"); steps.Add(s);
        await Press((VK_TAB, true, false));
        steps.Add(Snap("Shift+Tab back", "Shift+Tab"));

        // invalid entry: 0 quantity → validation error shown on the cell, Enter moves down
        var errLine = grid.CurrentCell.Item as PurchaseOrderLine;
        var errCountBefore = vm.ErrorCount;
        await Press(K(VK_F2), (0x41 /*A*/, false, true), K((byte)'0'), K(VK_RETURN));
        s = Snap("enter 0 qty + Enter → validation error on previous row", "F2 Ctrl+A 0 Enter");
        s["editedRowHasErrors"] = errLine?.HasErrors; s["editedRowErrors"] = errLine?.ErrorSummary; s["errorCountBefore"] = errCountBefore; s["errorCountAfter"] = vm.ErrorCount; steps.Add(s);
        await Press(K(VK_UP));
        s = Snap("Up: back on the invalid row, status bar shows its message", "Up");
        var focusedCell = grid.CurrentCell.IsValid && grid.CurrentCell.Item is PurchaseOrderLine fl ? view.GetCell(grid.Items.IndexOf(fl), grid.CurrentCell.Column) : null;
        s["errorCellBackground"] = (focusedCell?.Background as SolidColorBrush)?.Color.ToString();
        s["errorCellForeground"] = (focusedCell?.Foreground as SolidColorBrush)?.Color.ToString();
        steps.Add(s);
        Save(win, Path.Combine(outDir, $"{prefix}-validation.png"));

        // F8 walks the errors (wrapping), Shift+F8 walks back
        await Press(K(VK_F8));
        s = Snap("F8 moves to the next error cell", "F8"); steps.Add(s);
        Save(win, Path.Combine(outDir, $"{prefix}-next-error.png"));
        await Press(K(VK_F8));
        steps.Add(Snap("F8 again: next error", "F8"));
        await Press((VK_F8, true, false));
        steps.Add(Snap("Shift+F8: previous error", "Shift+F8"));
        await Press((VK_HOME, false, true));
        await Press(K(VK_DOWN), K(VK_DOWN), K(VK_DOWN), K(VK_DOWN), K(VK_RIGHT), K(VK_RIGHT));

        // selection extension needs a real modifier
        await Press((VK_DOWN, true, false), (VK_DOWN, true, false));
        steps.Add(Snap("Shift+Down x2 extends selection", "Shift+Down Shift+Down"));
        Save(win, Path.Combine(outDir, $"{prefix}-selection.png"));
        await Press(K(VK_UP), K(VK_UP));

        // header stays visible while scrolling to the end
        var headerBefore = steps[0]["headerTopY"];
        await Press((VK_END, false, true));
        s = Snap("Ctrl+End scrolls to last row", "Ctrl+End"); s["headerTopYBefore"] = headerBefore; steps.Add(s);
        Save(win, Path.Combine(outDir, $"{prefix}-scrolled.png"));

        // Enter on the last row adds a new line
        var countBefore = vm.LineCount;
        await Press(K(VK_RETURN));
        s = Snap("Enter on last row adds a line", "Enter"); s["lineCountBefore"] = countBefore; steps.Add(s);
        await Press(K(VK_ESCAPE));
        await Press((VK_HOME, false, true));
        steps.Add(Snap("Ctrl+Home back to top", "Ctrl+Home"));

        // numeric alignment: read the TextBlocks of row 0
        var alignment = new Dictionary<string, string?>();
        foreach (var col in grid.Columns.Where(c => c.Visibility == Visibility.Visible))
        {
            var cell = view.GetCell(0, col);
            var tb = cell != null ? PurchaseOrderLinesView.FindChild<TextBlock>(cell) : null;
            alignment[col.Header?.ToString() ?? "?"] = tb?.TextAlignment.ToString() + (tb != null && System.Windows.Documents.Typography.GetNumeralAlignment(tb) == FontNumeralAlignment.Tabular ? "/tabular" : "");
        }

        // F6 pane cycling and Ctrl+F
        await Press(K(VK_F6));
        var f6a = Keyboard.FocusedElement?.GetType().Name;
        await Press(K(VK_F6));
        var f6b = Keyboard.FocusedElement?.GetType().Name;
        await Press(K(VK_F6));
        var f6c = Keyboard.FocusedElement?.GetType().Name;
        await Press((0x46 /*F*/, false, true));
        var ctrlF = Keyboard.FocusedElement?.GetType().Name + (view.FilterBox.IsKeyboardFocused ? "(FilterBox)" : "");

        return new Dictionary<string, object?>
        {
            ["inputMode"] = useOs ? "os-keybd_event" : "wpf-InputManager",
            ["steps"] = steps,
            ["numericAlignmentRow0"] = alignment,
            ["f6Cycle"] = new[] { f6a, f6b, f6c },
            ["ctrlF"] = ctrlF,
            ["reducedMotion"] = new { systemClientAreaAnimation = SystemParameters.ClientAreaAnimation, appAnimations = "none except the indeterminate ProgressBar in the loading state; no storyboards" },
            ["minControlHeight"] = 32,
        };
    }

    /// <summary>Measured left edges (x) and top/bottom (y) of the shell bands, in DIP relative to the window content, to check the shared inset and rhythm.</summary>
    private static Dictionary<string, object?> LayoutProbe(MainWindow win, PurchaseOrderLinesView view)
    {
        var d = new Dictionary<string, object?>();
        void Put(string name, FrameworkElement? fe)
        {
            if (fe == null || !fe.IsVisible) { d[name] = null; return; }
            var p = fe.TransformToAncestor(win).Transform(new Point(0, 0));
            d[name] = new { x = Math.Round(p.X, 1), y = Math.Round(p.Y, 1), w = Math.Round(fe.ActualWidth, 1), h = Math.Round(fe.ActualHeight, 1) };
        }
        var menu = PurchaseOrderLinesView.FindChild<Menu>(view);
        var fileItem = menu?.Items.Count > 0 ? menu.ItemContainerGenerator.ContainerFromIndex(0) as MenuItem : null;
        var fileText = fileItem != null ? PurchaseOrderLinesView.FindChild<TextBlock>(fileItem) : null;
        Put("menuFileText", fileText);
        var title = FindByText(view, "Purchase order lines");
        Put("titleText", title);
        Put("addButton", view.AddButton);
        Put("filterBox", view.FilterBox);
        Put("grid", view.Grid);
        var status = PurchaseOrderLinesView.FindChild<StatusBar>(view);
        Put("statusBar", status);
        var statusText = status != null ? PurchaseOrderLinesView.FindChild<TextBlock>(status) : null;
        Put("statusFirstText", statusText);
        Put("keyHints", view.KeyHints);
        Put("errorLink", view.ErrorLink);
        Put("focusedErrorText", view.FocusedErrorText);
        return d;
    }

    private static TextBlock? FindByText(DependencyObject parent, string text)
    {
        for (var i = 0; i < VisualTreeHelper.GetChildrenCount(parent); i++)
        {
            var child = VisualTreeHelper.GetChild(parent, i);
            if (child is TextBlock tb && tb.Text == text) return tb;
            var r = FindByText(child, text);
            if (r != null) return r;
        }
        return null;
    }

    private static void InjectWpfKey(Key key)
    {
        if (Keyboard.FocusedElement is not UIElement target) return;
        var src = PresentationSource.FromVisual(target);
        if (src == null) return;
        var down = new KeyEventArgs(Keyboard.PrimaryDevice, src, Environment.TickCount, key) { RoutedEvent = Keyboard.PreviewKeyDownEvent };
        target.RaiseEvent(down);
        if (!down.Handled) { var d2 = new KeyEventArgs(Keyboard.PrimaryDevice, src, Environment.TickCount, key) { RoutedEvent = Keyboard.KeyDownEvent }; target.RaiseEvent(d2); }
    }

    private static Task Idle() => Current.Dispatcher.InvokeAsync(() => { }, DispatcherPriority.ApplicationIdle).Task;

    private static void Save(Window win, string path)
    {
        var dpi = VisualTreeHelper.GetDpi(win);
        var content = (FrameworkElement)win.Content;
        var pw = (int)Math.Ceiling(content.ActualWidth * dpi.DpiScaleX);
        var ph = (int)Math.Ceiling(content.ActualHeight * dpi.DpiScaleY);
        var rtb = new RenderTargetBitmap(pw, ph, dpi.PixelsPerInchX, dpi.PixelsPerInchY, PixelFormats.Pbgra32);
        rtb.Render(content);
        var enc = new PngBitmapEncoder();
        enc.Frames.Add(BitmapFrame.Create(rtb));
        using var fs = File.Create(path);
        enc.Save(fs);
    }

    private const byte VK_TAB = 0x09, VK_RETURN = 0x0D, VK_SHIFT = 0x10, VK_CONTROL = 0x11, VK_ESCAPE = 0x1B, VK_END = 0x23, VK_HOME = 0x24,
        VK_LEFT = 0x25, VK_UP = 0x26, VK_RIGHT = 0x27, VK_DOWN = 0x28, VK_F2 = 0x71, VK_F6 = 0x75, VK_F8 = 0x77;
    private const uint KEYEVENTF_KEYUP = 0x0002, KEYEVENTF_EXTENDEDKEY = 0x0001;

    [DllImport("user32.dll")] private static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")] private static extern bool SetForegroundWindow(IntPtr hWnd);
}
