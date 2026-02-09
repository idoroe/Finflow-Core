# Data Dictionary — Czech Banking Dataset

## Source Files (8 CSVs, semicolon-delimited)

### account.csv (4,500 rows)
| Column | Type | Description |
|--------|------|-------------|
| account_id | INT | Unique account identifier |
| district_id | INT | District where account was opened |
| frequency | STRING | Statement issuance frequency (POPLATEK MESICNE=monthly, POPLATEK TYDNE=weekly, POPLATEK PO OBRATU=after transaction) |
| date | INT | Account opening date in YYMMDD format |

### trans.csv (~1M rows) — THE MAIN TABLE
| Column | Type | Description |
|--------|------|-------------|
| trans_id | INT | Unique transaction ID |
| account_id | INT | Account involved |
| date | INT | Transaction date in YYMMDD format |
| type | STRING | PRIJEM = credit (money in), VYDAJ = debit (money out), VYBER = withdrawal |
| operation | STRING | Type of operation (VKLAD=deposit, PREVOD Z UCTU=transfer in, VYBER=withdrawal, PREVOD NA UCET=transfer out) |
| amount | DECIMAL | Transaction amount |
| balance | DECIMAL | Account balance after transaction |
| k_symbol | STRING | Category (POJISTNE=insurance, SIPO=household, UVER=loan payment, etc.) |
| bank | STRING | Partner bank code (if applicable) |
| account | INT | Partner account number (if applicable) |

### client.csv (5,369 rows)
| Column | Type | Description |
|--------|------|-------------|
| client_id | INT | Unique customer ID |
| birth_number | INT | Encodes birthday AND gender. Format: YYMMDD. For women, MM is increased by 50. Example: 706213 = female born 1970-12-13 |
| district_id | INT | Customer's home district |

### disp.csv (5,369 rows)
| Column | Type | Description |
|--------|------|-------------|
| disp_id | INT | Unique disposition ID |
| client_id | INT | Which customer |
| account_id | INT | Which account |
| type | STRING | OWNER = account owner, DISPONENT = authorized user (can transact but doesn't own the account) |

### district.csv (77 rows)
| Column | Original Name | Description |
|--------|--------------|-------------|
| district_id | A1 | Unique district ID |
| district_name | A2 | Name of the district |
| region | A3 | Geographic region |
| population | A4 | Number of inhabitants |
| num_municipalities_lt_499 | A5 | Municipalities with < 499 inhabitants |
| num_municipalities_500_1999 | A6 | Municipalities with 500-1999 inhabitants |
| num_municipalities_2000_9999 | A7 | Municipalities with 2000-9999 inhabitants |
| num_cities | A8 | Number of cities (> 10,000 inhabitants) |
| urban_ratio | A9 | Ratio of urban inhabitants |
| avg_salary | A10 | Average salary |
| unemployment_95 | A11 | Unemployment rate 1995 |
| unemployment_96 | A12 | Unemployment rate 1996 |
| num_entrepreneurs | A13 | Number of entrepreneurs per 1000 inhabitants |
| num_crimes_95 | A14 | Number of committed crimes 1995 |
| num_crimes_96 | A15 | Number of committed crimes 1996 |

### loan.csv (682 rows)
| Column | Type | Description |
|--------|------|-------------|
| loan_id | INT | Unique loan ID |
| account_id | INT | Account the loan belongs to |
| date | INT | Loan issue date in YYMMDD format |
| amount | DECIMAL | Loan amount |
| duration | INT | Loan duration in months (12, 24, 36, 48, or 60) |
| payments | DECIMAL | Monthly payment amount |
| status | CHAR | A=contract finished, no problems; B=contract finished, loan not paid; C=running, OK so far; D=running, client in debt |

### order.csv (6,471 rows)
| Column | Type | Description |
|--------|------|-------------|
| order_id | INT | Unique standing order ID |
| account_id | INT | Account the order belongs to |
| bank_to | STRING | Destination bank code |
| account_to | INT | Destination account number |
| amount | DECIMAL | Payment amount |
| k_symbol | STRING | Category (POJISTNE=insurance, SIPO=household, LEASING, UVER=loan) |

### card.csv (892 rows)
| Column | Type | Description |
|--------|------|-------------|
| card_id | INT | Unique card ID |
| disp_id | INT | Disposition (links card to account/client) |
| type | STRING | classic, junior, or gold |
| issued | DATETIME | Card issue date |

## Entity Relationships

```
CLIENT --[disp]--> ACCOUNT --[trans]--> TRANSACTIONS
                      |
                      +--> LOAN
                      +--> ORDER (standing orders)
                      +--> CARD (via disp)
                      +--> DISTRICT
```
