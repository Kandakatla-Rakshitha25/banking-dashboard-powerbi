# 📖 Data Dictionary

All tables and fields used in the Banking Dashboard.

---

## Table: `dim_customer`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `customer_id` | INT | Unique customer identifier | 1001 |
| `full_name` | STRING | Customer full name | John Smith |
| `age` | INT | Customer age in years | 35 |
| `gender` | STRING | M / F / Other | M |
| `city` | STRING | City of residence | Mumbai |
| `state` | STRING | State | Maharashtra |
| `segment` | STRING | Retail / HNI / SME / Corporate | Retail |
| `account_open_date` | DATE | Date account was opened | 2019-03-15 |
| `is_active` | BOOLEAN | Currently active customer | TRUE |
| `credit_score` | INT | CIBIL/credit score (300–900) | 750 |
| `annual_income` | DECIMAL | Annual income in INR | 850000 |

---

## Table: `dim_branch`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `branch_id` | INT | Unique branch identifier | B001 |
| `branch_name` | STRING | Branch display name | Banjara Hills |
| `city` | STRING | City | Hyderabad |
| `state` | STRING | State | Telangana |
| `region` | STRING | North / South / East / West / Central | South |
| `branch_manager` | STRING | Manager name | Priya Reddy |
| `opened_date` | DATE | Branch inauguration date | 2010-06-01 |
| `branch_type` | STRING | Urban / Semi-Urban / Rural | Urban |

---

## Table: `dim_product`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `product_id` | INT | Product identifier | P01 |
| `product_name` | STRING | Name of banking product | Home Loan |
| `product_category` | STRING | Loan / Deposit / Card / Insurance | Loan |
| `interest_rate` | DECIMAL | Annual interest rate % | 8.5 |
| `tenure_months` | INT | Max tenure in months | 240 |

---

## Table: `dim_date`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `date` | DATE | Calendar date | 2024-01-15 |
| `day` | INT | Day of month | 15 |
| `month` | INT | Month number | 1 |
| `month_name` | STRING | Full month name | January |
| `quarter` | INT | Quarter (1–4) | 1 |
| `year` | INT | Calendar year | 2024 |
| `week_number` | INT | ISO week number | 3 |
| `is_weekday` | BOOLEAN | Mon–Fri = TRUE | TRUE |
| `is_holiday` | BOOLEAN | Public holiday flag | FALSE |
| `fiscal_year` | STRING | FY label | FY2024 |
| `fiscal_quarter` | STRING | Fiscal quarter label | Q3 FY2024 |

---

## Table: `fact_loans`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `loan_id` | INT | Unique loan identifier | L10001 |
| `customer_id` | INT | FK → dim_customer | 1001 |
| `branch_id` | INT | FK → dim_branch | B001 |
| `product_id` | INT | FK → dim_product | P01 |
| `disbursement_date` | DATE | Date loan was disbursed | 2023-04-01 |
| `loan_amount` | DECIMAL | Principal amount (INR) | 5000000 |
| `outstanding_amount` | DECIMAL | Current outstanding (INR) | 4200000 |
| `emi_amount` | DECIMAL | Monthly EMI (INR) | 45000 |
| `tenure_months` | INT | Loan tenure in months | 180 |
| `loan_status` | STRING | Active / Closed / NPA / Written-Off | Active |
| `dpd` | INT | Days Past Due | 0 |
| `npa_flag` | BOOLEAN | TRUE if NPA | FALSE |
| `collateral_value` | DECIMAL | Collateral value (INR) | 7000000 |

---

## Table: `fact_transactions`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `txn_id` | STRING | Transaction ID | TXN2024001 |
| `customer_id` | INT | FK → dim_customer | 1001 |
| `branch_id` | INT | FK → dim_branch | B001 |
| `txn_date` | DATE | Date of transaction | 2024-01-15 |
| `txn_time` | TIME | Time of transaction | 14:32:00 |
| `txn_type` | STRING | Credit / Debit / Transfer | Debit |
| `txn_amount` | DECIMAL | Transaction amount (INR) | 25000 |
| `channel` | STRING | Branch / ATM / NetBanking / Mobile / UPI | Mobile |
| `category` | STRING | NEFT / RTGS / IMPS / UPI / Cash | UPI |
| `fraud_flag` | BOOLEAN | TRUE if flagged suspicious | FALSE |
| `balance_after` | DECIMAL | Account balance post-txn | 125000 |

---

## Table: `fact_financials`

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `record_id` | INT | Unique record identifier | 1 |
| `branch_id` | INT | FK → dim_branch | B001 |
| `date` | DATE | Month-end date | 2024-01-31 |
| `total_deposits` | DECIMAL | Total deposits held (INR) | 250000000 |
| `total_loans` | DECIMAL | Total loans disbursed (INR) | 180000000 |
| `interest_income` | DECIMAL | Interest earned (INR) | 1500000 |
| `interest_expense` | DECIMAL | Interest paid on deposits (INR) | 700000 |
| `operating_expense` | DECIMAL | Operating cost (INR) | 400000 |
| `net_profit` | DECIMAL | Net profit for the period (INR) | 400000 |
| `total_assets` | DECIMAL | Total assets (INR) | 300000000 |
| `npa_amount` | DECIMAL | NPA book value (INR) | 9000000 |

---

## Calculated Columns & Flags

| Column | Table | Logic |
|--------|-------|-------|
| `age_group` | dim_customer | `<25 / 25-35 / 36-50 / 51-65 / 65+` |
| `income_segment` | dim_customer | `<3L / 3-7L / 7-15L / 15L+` |
| `loan_to_value` | fact_loans | `loan_amount / collateral_value * 100` |
| `dpd_bucket` | fact_loans | `0 / 1-30 / 31-60 / 61-90 / 90+` |
| `txn_value_band` | fact_transactions | `<10K / 10-50K / 50K-1L / 1L+` |
