using Finflow.Core.Data;
using Finflow.Core.Analytics;

namespace Finflow.Core.Pipeline;

public class DataPipeline
{
    private readonly string _rawDataPath;
    private readonly string _analyticsOutputPath;

    public DataPipeline(string rawDataPath, string analyticsOutputPath)
    {
        _rawDataPath = rawDataPath;
        _analyticsOutputPath = analyticsOutputPath;

        // Ensure output directory exists
        Directory.CreateDirectory(_analyticsOutputPath);
    }

    public void Run()
    {
        Console.WriteLine("╔═══════════════════════════════════════════════════════════╗");
        Console.WriteLine("║          FINFLOW DATA PIPELINE - STARTING                 ║");
        Console.WriteLine("╚═══════════════════════════════════════════════════════════╝\n");

        // Step 1: Load raw data
        Console.WriteLine("📁 Step 1: Loading raw data...");
        var transactions = DataLoader.LoadTransactions(Path.Combine(_rawDataPath, "transactions.csv"));
        var loans = DataLoader.LoadLoans(Path.Combine(_rawDataPath, "loans.csv"));
        var customers = DataLoader.LoadCustomers(Path.Combine(_rawDataPath, "customers.csv"));
        Console.WriteLine($"   ✓ Loaded {transactions.Count} transactions");
        Console.WriteLine($"   ✓ Loaded {loans.Count} loans");
        Console.WriteLine($"   ✓ Loaded {customers.Count} customers");

        // Step 2: Run analytics transformations
        Console.WriteLine("\n🔄 Step 2: Running analytics transformations...");
        
        Console.WriteLine("   → Analyzing transaction volume over time...");
        var transactionAnalytics = AnalyticsEngine.AnalyzeTransactionVolume(transactions);
        
        Console.WriteLine("   → Analyzing regional loan defaults...");
        var loanAnalytics = AnalyticsEngine.AnalyzeLoanDefaults(loans);
        
        Console.WriteLine("   → Analyzing customer activity...");
        var customerAnalytics = AnalyticsEngine.AnalyzeCustomerActivity(customers, transactions, loans);
        
        Console.WriteLine($"   ✓ Generated {transactionAnalytics.Count} transaction analytics records");
        Console.WriteLine($"   ✓ Generated {loanAnalytics.Count} loan default analytics records");
        Console.WriteLine($"   ✓ Generated {customerAnalytics.Count} customer activity records");

        // Step 3: Write analytics tables
        Console.WriteLine("\n💾 Step 3: Writing analytics tables...");
        AnalyticsWriter.WriteTransactionVolumeAnalytics(
            transactionAnalytics, 
            Path.Combine(_analyticsOutputPath, "transaction_volume_analytics.csv"));
        AnalyticsWriter.WriteLoanDefaultAnalytics(
            loanAnalytics, 
            Path.Combine(_analyticsOutputPath, "loan_default_analytics.csv"));
        AnalyticsWriter.WriteCustomerActivityAnalytics(
            customerAnalytics, 
            Path.Combine(_analyticsOutputPath, "customer_activity_analytics.csv"));
        Console.WriteLine($"   ✓ Analytics tables written to: {_analyticsOutputPath}");

        // Step 4: Display summary report
        AnalyticsWriter.PrintSummaryReport(transactionAnalytics, loanAnalytics, customerAnalytics);

        Console.WriteLine("\n╔═══════════════════════════════════════════════════════════╗");
        Console.WriteLine("║          FINFLOW DATA PIPELINE - COMPLETED                ║");
        Console.WriteLine("╚═══════════════════════════════════════════════════════════╝\n");
    }
}
