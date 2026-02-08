using System.Globalization;
using Finflow.Core.Models;

namespace Finflow.Core.Data;

public class DataLoader
{
    public static List<Transaction> LoadTransactions(string filePath)
    {
        var transactions = new List<Transaction>();
        var lines = File.ReadAllLines(filePath);
        
        // Skip header
        for (int i = 1; i < lines.Length; i++)
        {
            var parts = lines[i].Split(',');
            if (parts.Length >= 7)
            {
                transactions.Add(new Transaction
                {
                    TransactionId = parts[0],
                    CustomerId = parts[1],
                    TransactionDate = DateTime.Parse(parts[2]),
                    Amount = decimal.Parse(parts[3]),
                    TransactionType = parts[4],
                    Region = parts[5],
                    Description = parts[6]
                });
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
            var parts = lines[i].Split(',');
            if (parts.Length >= 8)
            {
                loans.Add(new Loan
                {
                    LoanId = parts[0],
                    CustomerId = parts[1],
                    LoanAmount = decimal.Parse(parts[2]),
                    LoanDate = DateTime.Parse(parts[3]),
                    Region = parts[4],
                    Status = parts[5],
                    TermMonths = int.Parse(parts[6]),
                    InterestRate = decimal.Parse(parts[7])
                });
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
            var parts = lines[i].Split(',');
            if (parts.Length >= 6)
            {
                customers.Add(new Customer
                {
                    CustomerId = parts[0],
                    Name = parts[1],
                    Email = parts[2],
                    Region = parts[3],
                    JoinDate = DateTime.Parse(parts[4]),
                    AccountType = parts[5]
                });
            }
        }
        
        return customers;
    }
}
