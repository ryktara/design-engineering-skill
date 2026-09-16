using Avalonia;

namespace FleetDesk;

internal static class Program
{
    // Avalonia configuration, do not remove; also used by the visual designer.
    [STAThread]
    public static void Main(string[] args) =>
        BuildAvaloniaApp().StartWithClassicDesktopLifetime(args);

    public static AppBuilder BuildAvaloniaApp() =>
        AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .WithInterFont()   // "Inter" is the bundled fallback when Segoe UI is not installed
            .LogToTrace();
}
