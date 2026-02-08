namespace Finflow.Core.Models;

public class LoanDefaultAnalytics
{
    public string Region { get; set; } = string.Empty;
    public int TotalLoans { get; set; }
    public int DefaultedLoans { get; set; }
    public decimal DefaultRate { get; set; }
    public decimal TotalDefaultedAmount { get; set; }
}
