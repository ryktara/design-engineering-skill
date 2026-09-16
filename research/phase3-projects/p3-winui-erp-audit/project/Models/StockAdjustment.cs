namespace Erp.Client.Models;

public enum AdjustmentStatus
{
    Draft,
    PendingApproval,
    Posted,
    Rejected,
}

public enum AdjustmentReason
{
    CycleCount,
    Damage,
    Shrinkage,
    Return,
    Correction,
}

public sealed record StockAdjustment(
    string Id,
    string Sku,
    string Description,
    string Location,
    AdjustmentReason Reason,
    decimal QuantityBefore,
    decimal QuantityDelta,
    string Unit,
    decimal UnitCost,
    AdjustmentStatus Status,
    string CreatedBy,
    DateTimeOffset CreatedAt)
{
    public decimal QuantityAfter => QuantityBefore + QuantityDelta;
    public decimal ValueImpact => QuantityDelta * UnitCost;

    /// <summary>Approve/Reject apply only to drafts and pending adjustments.</summary>
    public bool IsActionable => Status is AdjustmentStatus.Draft or AdjustmentStatus.PendingApproval;
}
