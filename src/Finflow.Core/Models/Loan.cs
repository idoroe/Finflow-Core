namespace Finflow.Core.Models;

public class Loan
{
    public string LoanId { get; set; } = string.Empty;
    public string CustomerId { get; set; } = string.Empty;
    public decimal LoanAmount { get; set; }
    public DateTime LoanDate { get; set; }
    public string Region { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty; // Active, Paid, Defaulted
    public int TermMonths { get; set; }
    public decimal InterestRate { get; set; }
}
