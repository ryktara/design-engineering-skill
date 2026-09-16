namespace Erp.Client.Models;

public enum MatchStatus
{
    Unmatched,
    PriceVariance,
    QuantityVariance,
    Matched,
    OnHold,
}

/// <summary>A supplier invoice awaiting three-way match against its purchase order and goods receipt.</summary>
public sealed record SupplierInvoice(
    string InvoiceNumber,
    string Supplier,
    string PurchaseOrder,
    DateTimeOffset InvoiceDate,
    DateTimeOffset DueDate,
    string Currency,
    decimal InvoiceTotal,
    decimal ReceivedTotal,
    MatchStatus Status)
{
    public decimal VarianceTotal => InvoiceTotal - ReceivedTotal;

    /// <summary>Only an unmatched or variance invoice can be acted on.</summary>
    public bool IsActionable => Status is MatchStatus.Unmatched or MatchStatus.PriceVariance or MatchStatus.QuantityVariance;
}

/// <summary>One invoice line matched against the corresponding purchase-order / goods-receipt line.</summary>
public sealed record InvoiceMatchLine(
    string LineNumber,
    string Sku,
    string Description,
    decimal InvoicedQuantity,
    decimal ReceivedQuantity,
    string Unit,
    decimal InvoicedUnitPrice,
    decimal OrderedUnitPrice,
    MatchStatus Status)
{
    public decimal QuantityVariance => InvoicedQuantity - ReceivedQuantity;
    public decimal PriceVariance => InvoicedUnitPrice - OrderedUnitPrice;
    public decimal ValueVariance => (InvoicedQuantity * InvoicedUnitPrice) - (ReceivedQuantity * OrderedUnitPrice);
    public bool IsActionable => Status is not MatchStatus.Matched;
}
