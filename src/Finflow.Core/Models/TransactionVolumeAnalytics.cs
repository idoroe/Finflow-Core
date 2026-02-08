namespace Finflow.Core.Models;

public class TransactionVolumeAnalytics
{
    public DateTime Period { get; set; }
    public int TransactionCount { get; set; }
    public decimal TotalAmount { get; set; }
    public decimal AverageAmount { get; set; }
    public string Region { get; set; } = string.Empty;
}
