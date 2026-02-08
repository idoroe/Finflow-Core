# Finflow-Core

An end-to-end data pipeline system that transforms raw banking data into trusted analytics tables, enabling fast and clean analytics for financial institutions.

## 🎯 Overview

Finflow-Core solves the real-world problem of messy banking data by providing a robust data pipeline that answers critical business questions:

- **How does transaction volume change over time?** - Track transaction patterns by region and period
- **Which regions have higher loan defaults?** - Identify risk areas with detailed default analytics
- **Which customers are most active?** - Understand customer engagement and activity levels

## 🏗️ Architecture

The system follows a classic ETL (Extract, Transform, Load) pattern:

```
Raw Data (CSV) → Data Loader → Analytics Engine → Analytics Tables (CSV)
     ↓                ↓               ↓                    ↓
transactions.csv → Models → Transformations → transaction_volume_analytics.csv
loans.csv        → Load   → Aggregate        → loan_default_analytics.csv
customers.csv    → Parse  → Join & Group     → customer_activity_analytics.csv
```

## 📁 Project Structure

```
Finflow-Core/
├── src/Finflow.Core/
│   ├── Models/              # Data models for raw and analytics data
│   │   ├── Transaction.cs
│   │   ├── Loan.cs
│   │   ├── Customer.cs
│   │   ├── TransactionVolumeAnalytics.cs
│   │   ├── LoanDefaultAnalytics.cs
│   │   └── CustomerActivityAnalytics.cs
│   ├── Data/               # Data loading and ingestion
│   │   └── DataLoader.cs
│   ├── Analytics/          # Analytics engine and output
│   │   ├── AnalyticsEngine.cs
│   │   └── AnalyticsWriter.cs
│   ├── Pipeline/           # Pipeline orchestration
│   │   └── DataPipeline.cs
│   └── Program.cs          # Entry point
├── data/
│   ├── raw/               # Raw input data (CSV files)
│   │   ├── transactions.csv
│   │   ├── loans.csv
│   │   └── customers.csv
│   └── analytics/         # Generated analytics tables
│       ├── transaction_volume_analytics.csv
│       ├── loan_default_analytics.csv
│       └── customer_activity_analytics.csv
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- .NET 10.0 SDK or later

### Installation & Running

1. Clone the repository:
```bash
git clone https://github.com/idoroe/Finflow-Core.git
cd Finflow-Core
```

2. Build the project:
```bash
cd src/Finflow.Core
dotnet build
```

3. Run the data pipeline:
```bash
dotnet run
```

The pipeline will:
1. Load raw data from `data/raw/`
2. Transform and analyze the data
3. Generate analytics tables in `data/analytics/`
4. Display a comprehensive summary report

## 📊 Analytics Outputs

### 1. Transaction Volume Analytics
Analyzes transaction patterns over time by region:
- Transaction count per period and region
- Total and average transaction amounts
- Time-series trends

**Output:** `transaction_volume_analytics.csv`

### 2. Loan Default Analytics
Identifies loan default patterns by region:
- Total loans per region
- Number and percentage of defaulted loans
- Total defaulted amount
- Default rate ranking

**Output:** `loan_default_analytics.csv`

### 3. Customer Activity Analytics
Tracks customer engagement and activity:
- Transaction count and volume per customer
- Active loans count
- Last activity date
- Customer ranking by activity

**Output:** `customer_activity_analytics.csv`

## 📈 Sample Output

When you run the pipeline, you'll see:

```
╔═══════════════════════════════════════════════════════════╗
║          FINFLOW DATA PIPELINE - STARTING                 ║
╚═══════════════════════════════════════════════════════════╝

📁 Step 1: Loading raw data...
   ✓ Loaded 25 transactions
   ✓ Loaded 13 loans
   ✓ Loaded 12 customers

🔄 Step 2: Running analytics transformations...
   ✓ Generated analytics records

💾 Step 3: Writing analytics tables...
   ✓ Analytics tables written

📊 TRANSACTION VOLUME ANALYSIS
📊 LOAN DEFAULT ANALYSIS
👥 CUSTOMER ACTIVITY ANALYSIS
```

## 🔧 Customization

### Adding New Data Sources

1. Create a new model in `Models/`
2. Add a loader method in `Data/DataLoader.cs`
3. Update the pipeline in `Pipeline/DataPipeline.cs`

### Adding New Analytics

1. Create analytics model in `Models/`
2. Add transformation logic in `Analytics/AnalyticsEngine.cs`
3. Add output writer in `Analytics/AnalyticsWriter.cs`

### Changing Data Formats

The current implementation uses CSV files, but you can easily extend to support:
- JSON files
- Database connections (SQL Server, PostgreSQL, etc.)
- API endpoints
- Cloud storage (Azure Blob, AWS S3)

## 🎯 Real-World Use Cases

This mini version demonstrates patterns used in production banking systems for:

- **Risk Management**: Identify high-risk regions and customer segments
- **Business Intelligence**: Track KPIs and trends over time
- **Customer Analytics**: Understand customer behavior and engagement
- **Regulatory Reporting**: Generate compliance reports from raw data
- **Data Warehousing**: Transform operational data into analytical data marts

## 🔐 Data Security Note

This is a demonstration project with sample data. In a production environment, ensure:
- Encryption at rest and in transit
- Access controls and authentication
- Audit logging
- PII data masking
- Compliance with banking regulations (GDPR, PCI-DSS, etc.)

## 📝 License

This project is provided as-is for educational and demonstration purposes.
