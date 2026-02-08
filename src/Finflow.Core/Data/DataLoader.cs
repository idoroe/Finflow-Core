using System.Globalization;
using Finflow.Core.Models;

namespace Finflow.Core.Data;

public class DataLoader
{
    private static List<string> ParseCsvLine(string line)
    {
        var result = new List<string>();
        var current = new System.Text.StringBuilder();
        bool inQuotes = false;

        for (int i = 0; i < line.Length; i++)
        {
            char c = line[i];

            if (c == '"')
            {
                inQuotes = !inQuotes;
            }
            else if (c == ',' && !inQuotes)
            {
                result.Add(current.ToString().Trim());
                current.Clear();
            }
            else
            {
                current.Append(c);
            }
        }
        result.Add(current.ToString().Trim());

        return result;
    }

    public static List<Transaction> LoadTransactions(string filePath)
    {
        var transactions = new List<Transaction>();
        var lines = File.ReadAllLines(filePath);
        
        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            try
            {
                var parts = ParseCsvLine(lines[i]);
                if (parts.Count >= 7 &&
                    DateTime.TryParse(parts[2], CultureInfo.InvariantCulture, DateTimeStyles.None, out var transactionDate) &&
                    decimal.TryParse(parts[3], NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var amount))
                {
                    transactions.Add(new Transaction
                    {
                        TransactionId = parts[0],
                        CustomerId = parts[1],
                        TransactionDate = transactionDate,
                        Amount = amount,
                        TransactionType = parts[4],
                        Region = parts[5],
                        Description = parts[6]
                    });
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to parse transaction on line {i + 1}: {ex.Message}");
            }
        }
        
        return transactions;
    }

    public static List<Loan> LoadLoans(string filePath)
    {
        var loans = new List<Loan>();
        var lines = File.ReadAllLines(filePath);
        
        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            try
            {
                var parts = ParseCsvLine(lines[i]);
                if (parts.Count >= 8 &&
                    decimal.TryParse(parts[2], NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var loanAmount) &&
                    DateTime.TryParse(parts[3], CultureInfo.InvariantCulture, DateTimeStyles.None, out var loanDate) &&
                    int.TryParse(parts[6], NumberStyles.Integer, CultureInfo.InvariantCulture, out var termMonths) &&
                    decimal.TryParse(parts[7], NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var interestRate))
                {
                    loans.Add(new Loan
                    {
                        LoanId = parts[0],
                        CustomerId = parts[1],
                        LoanAmount = loanAmount,
                        LoanDate = loanDate,
                        Region = parts[4],
                        Status = parts[5],
                        TermMonths = termMonths,
                        InterestRate = interestRate
                    });
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to parse loan on line {i + 1}: {ex.Message}");
            }
        }
        
        return loans;
    }

    public static List<Customer> LoadCustomers(string filePath)
    {
        var customers = new List<Customer>();
        var lines = File.ReadAllLines(filePath);
        
        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            try
            {
                var parts = ParseCsvLine(lines[i]);
                if (parts.Count >= 6 &&
                    DateTime.TryParse(parts[4], CultureInfo.InvariantCulture, DateTimeStyles.None, out var joinDate))
                {
                    customers.Add(new Customer
                    {
                        CustomerId = parts[0],
                        Name = parts[1],
                        Email = parts[2],
                        Region = parts[3],
                        JoinDate = joinDate,
                        AccountType = parts[5]
                    });
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to parse customer on line {i + 1}: {ex.Message}");
            }
        }
        
        return customers;
    }
}
