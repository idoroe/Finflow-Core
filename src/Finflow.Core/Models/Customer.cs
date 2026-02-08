namespace Finflow.Core.Models;

public class Customer
{
    public string CustomerId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Region { get; set; } = string.Empty;
    public DateTime JoinDate { get; set; }
    public string AccountType { get; set; } = string.Empty;
}
