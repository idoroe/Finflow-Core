using System.Text;
using Finflow.Core.Models;

namespace Finflow.Core.Analytics;

public class AnalyticsWriter
{
    public static void WriteTransactionVolumeAnalytics(
        List<TransactionVolumeAnalytics> analytics, 
        string outputPath)
    {
        var csv = new StringBuilder();
        csv.AppendLine("Period,Region,TransactionCount,TotalAmount,AverageAmount");
        
        foreach (var item in analytics)
        {
            csv.AppendLine($"{item.Period:yyyy-MM-dd},{item.Region},{item.TransactionCount}," +
                          $"{item.TotalAmount:F2},{item.AverageAmount:F2}");
        }
        
        File.WriteAllText(outputPath, csv.ToString());
    }

    public static void WriteLoanDefaultAnalytics(
        List<LoanDefaultAnalytics> analytics, 
        string outputPath)
    {
        var csv = new StringBuilder();
        csv.AppendLine("Region,TotalLoans,DefaultedLoans,DefaultRate,TotalDefaultedAmount");
        
        foreach (var item in analytics)
        {
            csv.AppendLine($"{item.Region},{item.TotalLoans},{item.DefaultedLoans}," +
                          $"{item.DefaultRate:F2},{item.TotalDefaultedAmount:F2}");
        }
        
        File.WriteAllText(outputPath, csv.ToString());
    }

    public static void WriteCustomerActivityAnalytics(
        List<CustomerActivityAnalytics> analytics, 
        string outputPath)
    {
        var csv = new StringBuilder();
        csv.AppendLine("CustomerId,CustomerName,Region,TransactionCount,TotalTransactionAmount," +
                      "ActiveLoans,LastActivityDate");
        
        foreach (var item in analytics)
        {
            csv.AppendLine($"{item.CustomerId},{item.CustomerName},{item.Region}," +
                          $"{item.TransactionCount},{item.TotalTransactionAmount:F2}," +
                          $"{item.ActiveLoans},{item.LastActivityDate:yyyy-MM-dd}");
        }
        
        File.WriteAllText(outputPath, csv.ToString());
    }

    public static void PrintSummaryReport(
        List<TransactionVolumeAnalytics> transactionAnalytics,
        List<LoanDefaultAnalytics> loanAnalytics,
        List<CustomerActivityAnalytics> customerAnalytics)
    {
        Console.WriteLine("\n╔═══════════════════════════════════════════════════════════╗");
        Console.WriteLine("║          FINFLOW BANKING ANALYTICS REPORT                 ║");
        Console.WriteLine("╚═══════════════════════════════════════════════════════════╝\n");

        // Transaction Volume Summary
        Console.WriteLine("📊 TRANSACTION VOLUME ANALYSIS");
        Console.WriteLine("═══════════════════════════════════════════════════════════");
        var totalTransactions = transactionAnalytics.Sum(t => t.TransactionCount);
        var totalAmount = transactionAnalytics.Sum(t => t.TotalAmount);
        Console.WriteLine($"Total Transactions: {totalTransactions}");
        Console.WriteLine($"Total Amount: ${totalAmount:N2}");
        Console.WriteLine($"\nTop Periods by Transaction Count:");
        foreach (var item in transactionAnalytics.OrderByDescending(t => t.TransactionCount).Take(5))
        {
            Console.WriteLine($"  {item.Period:MMM yyyy} - {item.Region}: {item.TransactionCount} transactions (${item.TotalAmount:N2})");
        }

        // Loan Default Summary
        Console.WriteLine("\n\n⚠️  LOAN DEFAULT ANALYSIS");
        Console.WriteLine("═══════════════════════════════════════════════════════════");
        var totalLoans = loanAnalytics.Sum(l => l.TotalLoans);
        var totalDefaults = loanAnalytics.Sum(l => l.DefaultedLoans);
        var overallDefaultRate = totalLoans > 0 ? (decimal)totalDefaults / totalLoans * 100 : 0;
        Console.WriteLine($"Total Loans: {totalLoans}");
        Console.WriteLine($"Total Defaults: {totalDefaults}");
        Console.WriteLine($"Overall Default Rate: {overallDefaultRate:F2}%");
        Console.WriteLine($"\nRegional Default Rates:");
        foreach (var item in loanAnalytics)
        {
            Console.WriteLine($"  {item.Region}: {item.DefaultRate:F2}% ({item.DefaultedLoans}/{item.TotalLoans} loans, ${item.TotalDefaultedAmount:N2})");
        }

        // Customer Activity Summary
        Console.WriteLine("\n\n👥 CUSTOMER ACTIVITY ANALYSIS");
        Console.WriteLine("═══════════════════════════════════════════════════════════");
        var activeCustomers = customerAnalytics.Count(c => c.TransactionCount > 0);
        Console.WriteLine($"Total Customers: {customerAnalytics.Count}");
        Console.WriteLine($"Active Customers: {activeCustomers}");
        Console.WriteLine($"\nMost Active Customers:");
        foreach (var item in customerAnalytics.Take(10))
        {
            Console.WriteLine($"  {item.CustomerName} ({item.CustomerId}): {item.TransactionCount} transactions, ${item.TotalTransactionAmount:N2}");
        }

        Console.WriteLine("\n═══════════════════════════════════════════════════════════\n");
    }
}
