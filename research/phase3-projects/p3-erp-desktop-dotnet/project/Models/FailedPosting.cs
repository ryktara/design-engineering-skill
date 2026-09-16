namespace ErpClient.Models;

/// <summary>One ledger posting that the last sync could not write. The status bar shows the count and names each
/// reference and reason, because "sync failed" without the failing document is not actionable.</summary>
public sealed record FailedPosting(string Reference, string Reason, DateTime AttemptedAt);
