using Finflow.Core.Models;

namespace Finflow.Core.Analytics;

public class AnalyticsEngine
{
    public static List<TransactionVolumeAnalytics> AnalyzeTransactionVolume(
        List<Transaction> transactions)
    {
        return transactions
            .GroupBy(t => new { t.Region, Period = new DateTime(t.TransactionDate.Year, t.TransactionDate.Month, 1) })
            .Select(g => new TransactionVolumeAnalytics
            {
                Period = g.Key.Period,
                Region = g.Key.Region,
                TransactionCount = g.Count(),
                TotalAmount = g.Sum(t => t.Amount),
                AverageAmount = g.Average(t => t.Amount)
            })
            .OrderBy(a => a.Period)
            .ThenBy(a => a.Region)
            .ToList();
    }

    public static List<LoanDefaultAnalytics> AnalyzeLoanDefaults(
        List<Loan> loans)
    {
        return loans
            .GroupBy(l => l.Region)
            .Select(g => new LoanDefaultAnalytics
            {
                Region = g.Key,
                TotalLoans = g.Count(),
                DefaultedLoans = g.Count(l => l.Status == "Defaulted"),
                DefaultRate = g.Count() > 0 
                    ? (decimal)g.Count(l => l.Status == "Defaulted") / g.Count() * 100 
                    : 0,
                TotalDefaultedAmount = g
                    .Where(l => l.Status == "Defaulted")
                    .Sum(l => l.LoanAmount)
            })
            .OrderByDescending(a => a.DefaultRate)
            .ToList();
    }

    public static List<CustomerActivityAnalytics> AnalyzeCustomerActivity(
        List<Customer> customers,
        List<Transaction> transactions,
        List<Loan> loans)
    {
        var customerTransactions = transactions
            .GroupBy(t => t.CustomerId)
            .ToDictionary(
                g => g.Key,
                g => new { Count = g.Count(), Total = g.Sum(t => t.Amount), LastDate = g.Max(t => t.TransactionDate) }
            );

        var customerLoans = loans
            .Where(l => l.Status == "Active")
            .GroupBy(l => l.CustomerId)
            .ToDictionary(g => g.Key, g => g.Count());

        return customers
            .Select(c => new CustomerActivityAnalytics
            {
                CustomerId = c.CustomerId,
                CustomerName = c.Name,
                Region = c.Region,
                TransactionCount = customerTransactions.ContainsKey(c.CustomerId) 
                    ? customerTransactions[c.CustomerId].Count 
                    : 0,
                TotalTransactionAmount = customerTransactions.ContainsKey(c.CustomerId) 
                    ? customerTransactions[c.CustomerId].Total 
                    : 0,
                ActiveLoans = customerLoans.ContainsKey(c.CustomerId) 
                    ? customerLoans[c.CustomerId] 
                    : 0,
                LastActivityDate = customerTransactions.ContainsKey(c.CustomerId) 
                    ? customerTransactions[c.CustomerId].LastDate 
                    : c.JoinDate
            })
            .OrderByDescending(a => a.TransactionCount)
            .ToList();
    }
}
