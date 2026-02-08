namespace Finflow.Core.Models;

public class CustomerActivityAnalytics
{
    public string CustomerId { get; set; } = string.Empty;
    public string CustomerName { get; set; } = string.Empty;
    public int TransactionCount { get; set; }
    public decimal TotalTransactionAmount { get; set; }
    public int ActiveLoans { get; set; }
    public DateTime LastActivityDate { get; set; }
    public string Region { get; set; } = string.Empty;
}
