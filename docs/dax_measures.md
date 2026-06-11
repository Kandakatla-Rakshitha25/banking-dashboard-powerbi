# 📐 DAX Measures Library

All DAX measures used in the Banking Dashboard, organized by category.

---

## 💰 Profitability Measures

```dax
-- Net Interest Income
Net Interest Income = 
    SUM(fact_financials[interest_income]) - SUM(fact_financials[interest_expense])

-- Net Interest Margin (%)
NIM % = 
    DIVIDE(
        [Net Interest Income],
        AVERAGE(fact_financials[total_assets])
    ) * 100

-- Return on Assets (%)
ROA % = 
    DIVIDE(
        SUM(fact_financials[net_profit]),
        AVERAGE(fact_financials[total_assets])
    ) * 100

-- Return on Equity (%)
ROE % = 
    DIVIDE(
        SUM(fact_financials[net_profit]),
        SUM(fact_financials[total_assets]) * 0.1   -- Assuming 10% equity ratio
    ) * 100

-- Cost to Income Ratio (%)
Cost to Income Ratio = 
    DIVIDE(
        SUM(fact_financials[operating_expense]),
        [Net Interest Income] + [Non-Interest Income]
    ) * 100

-- Non-Interest Income
Non-Interest Income = 
    SUM(fact_financials[interest_income]) - SUM(fact_financials[interest_expense])
        + SUM(fact_financials[operating_expense])   -- simplified
```

---

## 🏦 Loan Portfolio Measures

```dax
-- Total Loan Portfolio
Total Loan Portfolio = 
    SUM(fact_loans[loan_amount])

-- Outstanding Loan Amount
Outstanding Amount = 
    SUM(fact_loans[outstanding_amount])

-- Loan Disbursement (Current Period)
Loan Disbursement = 
    CALCULATE(
        SUM(fact_loans[loan_amount]),
        fact_loans[disbursement_date] >= [Period Start Date]
    )

-- NPA Amount
NPA Amount = 
    CALCULATE(
        SUM(fact_loans[outstanding_amount]),
        fact_loans[npa_flag] = TRUE()
    )

-- NPA Ratio (%)
NPA Ratio % = 
    DIVIDE([NPA Amount], [Outstanding Amount]) * 100

-- Loan to Deposit Ratio (%)
Loan to Deposit Ratio = 
    DIVIDE(
        SUM(fact_financials[total_loans]),
        SUM(fact_financials[total_deposits])
    ) * 100

-- Average Loan Size
Avg Loan Size = 
    AVERAGEX(fact_loans, fact_loans[loan_amount])

-- Loan Count
Loan Count = 
    COUNTROWS(fact_loans)

-- Active Loan Count
Active Loan Count = 
    CALCULATE(
        COUNTROWS(fact_loans),
        fact_loans[loan_status] = "Active"
    )

-- Repayment Rate (%)
Repayment Rate % = 
    DIVIDE(
        SUM(fact_loans[loan_amount]) - SUM(fact_loans[outstanding_amount]),
        SUM(fact_loans[loan_amount])
    ) * 100

-- Loan Growth MoM (%)
Loan Growth MoM % = 
    VAR CurrentMonth = [Total Loan Portfolio]
    VAR PriorMonth = CALCULATE(
        [Total Loan Portfolio],
        DATEADD(dim_date[date], -1, MONTH)
    )
    RETURN DIVIDE(CurrentMonth - PriorMonth, PriorMonth) * 100
```

---

## 👥 Customer Measures

```dax
-- Total Customers
Total Customers = 
    DISTINCTCOUNT(dim_customer[customer_id])

-- Active Customers
Active Customers = 
    CALCULATE(
        DISTINCTCOUNT(dim_customer[customer_id]),
        dim_customer[is_active] = TRUE()
    )

-- New Customers (Current Period)
New Customers = 
    CALCULATE(
        DISTINCTCOUNT(dim_customer[customer_id]),
        DATESINPERIOD(dim_date[date], MAX(dim_date[date]), -1, MONTH)
    )

-- Customer Churn Rate (%)
Churn Rate % = 
    DIVIDE(
        CALCULATE(
            DISTINCTCOUNT(dim_customer[customer_id]),
            dim_customer[is_active] = FALSE()
        ),
        [Total Customers]
    ) * 100

-- Avg Credit Score
Avg Credit Score = 
    AVERAGE(dim_customer[credit_score])

-- Avg Annual Income
Avg Annual Income = 
    AVERAGE(dim_customer[annual_income])

-- Customers with Loans
Customers with Loans = 
    DISTINCTCOUNT(fact_loans[customer_id])

-- Loan Penetration Rate (%)
Loan Penetration % = 
    DIVIDE([Customers with Loans], [Active Customers]) * 100
```

---

## 💳 Transaction Measures

```dax
-- Total Transactions
Total Transactions = 
    COUNTROWS(fact_transactions)

-- Total Transaction Value
Total Txn Value = 
    SUM(fact_transactions[txn_amount])

-- Avg Transaction Value
Avg Txn Value = 
    AVERAGE(fact_transactions[txn_amount])

-- Digital Transaction %
Digital Txn % = 
    DIVIDE(
        CALCULATE(
            COUNTROWS(fact_transactions),
            fact_transactions[channel] IN {"NetBanking", "Mobile", "UPI"}
        ),
        [Total Transactions]
    ) * 100

-- Fraud Transactions
Fraud Count = 
    CALCULATE(
        COUNTROWS(fact_transactions),
        fact_transactions[fraud_flag] = TRUE()
    )

-- Fraud Rate (%)
Fraud Rate % = 
    DIVIDE([Fraud Count], [Total Transactions]) * 100

-- Transactions per Customer
Txn per Customer = 
    DIVIDE([Total Transactions], [Active Customers])

-- Daily Average Transactions
Daily Avg Transactions = 
    DIVIDE(
        [Total Transactions],
        DISTINCTCOUNT(fact_transactions[txn_date])
    )
```

---

## 🏢 Branch Performance Measures

```dax
-- Branch Revenue
Branch Revenue = 
    CALCULATE(
        SUM(fact_financials[interest_income]),
        ALLEXCEPT(dim_branch, dim_branch[branch_id])
    )

-- Branch Deposit Share (%)
Branch Deposit Share % = 
    DIVIDE(
        SUM(fact_financials[total_deposits]),
        CALCULATE(SUM(fact_financials[total_deposits]), ALL(dim_branch))
    ) * 100

-- Top Branch Flag
Is Top Branch = 
    IF(
        RANKX(ALL(dim_branch), [Branch Revenue],, DESC) <= 5,
        "Top 5", "Others"
    )

-- Target Achievement (%)
Target Achievement % = 
    DIVIDE([Total Loan Portfolio], [Loan Target]) * 100
```

---

## 📅 Time Intelligence Measures

```dax
-- YTD Loan Disbursement
YTD Disbursement = 
    TOTALYTD([Total Loan Portfolio], dim_date[date])

-- MTD Transactions
MTD Transactions = 
    TOTALMTD([Total Transactions], dim_date[date])

-- QTD Revenue
QTD Revenue = 
    TOTALQTD(SUM(fact_financials[interest_income]), dim_date[date])

-- YoY Loan Growth (%)
YoY Loan Growth % = 
    VAR CY = [Total Loan Portfolio]
    VAR PY = CALCULATE([Total Loan Portfolio], SAMEPERIODLASTYEAR(dim_date[date]))
    RETURN DIVIDE(CY - PY, PY) * 100

-- Rolling 3-Month Avg Transactions
Rolling 3M Avg Txn = 
    AVERAGEX(
        DATESINPERIOD(dim_date[date], LASTDATE(dim_date[date]), -3, MONTH),
        [Total Transactions]
    )
```

---

## 🎨 Formatting Helpers

```dax
-- Dynamic Title with Period
Report Title = 
    "Banking Dashboard — " & FORMAT(MAX(dim_date[date]), "MMM YYYY")

-- KPI Color (Red/Green)
NPA Color = 
    IF([NPA Ratio %] > 5, "#E74C3C", "#27AE60")

-- Trend Arrow
Loan Growth Arrow = 
    IF([Loan Growth MoM %] >= 0, "▲", "▼") & " " 
    & FORMAT(ABS([Loan Growth MoM %]), "0.0") & "%"
```
