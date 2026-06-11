"""
Banking Dashboard - Sample Data Generator
==========================================
Generates realistic synthetic banking data for the Power BI dashboard.
Run: python scripts/data_generation.py
Output: data/raw/*.csv and data/processed/banking_master.xlsx
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import date, timedelta
import random
import os

# ── Configuration ──────────────────────────────────────────────
SEED = 42
NUM_CUSTOMERS = 10_000
NUM_BRANCHES = 25
NUM_LOANS = 5_000
NUM_TRANSACTIONS = 50_000
START_DATE = date(2020, 1, 1)
END_DATE = date(2024, 12, 31)

random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_IN")

OUTPUT_RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_PROCESSED = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(OUTPUT_RAW, exist_ok=True)
os.makedirs(OUTPUT_PROCESSED, exist_ok=True)


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


# ── 1. dim_date ─────────────────────────────────────────────────
def generate_dates() -> pd.DataFrame:
    print("Generating dim_date...")
    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    df = pd.DataFrame({"date": dates})
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["quarter"] = df["date"].dt.quarter
    df["year"] = df["date"].dt.year
    df["week_number"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekday"] = df["date"].dt.dayofweek < 5
    df["is_holiday"] = False  # Placeholder — enrich with actual holidays
    df["fiscal_year"] = df["month"].apply(
        lambda m: f"FY{df.loc[df['month'] == m, 'year'].iloc[0] + 1}"
        if m >= 4 else f"FY{df.loc[df['month'] == m, 'year'].iloc[0]}"
    )
    df["fiscal_quarter"] = df.apply(
        lambda r: f"Q{((r['month'] - 4) % 12) // 3 + 1} {r['fiscal_year']}", axis=1
    )
    return df


# ── 2. dim_branch ────────────────────────────────────────────────
def generate_branches() -> pd.DataFrame:
    print("Generating dim_branch...")
    regions = {
        "South": ["Hyderabad", "Bangalore", "Chennai", "Kochi", "Visakhapatnam"],
        "North": ["Delhi", "Lucknow", "Jaipur", "Chandigarh", "Amritsar"],
        "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nagpur"],
        "East": ["Kolkata", "Bhubaneswar", "Patna", "Ranchi", "Guwahati"],
        "Central": ["Bhopal", "Indore", "Raipur", "Varanasi", "Agra"],
    }
    rows = []
    bid = 1
    for region, cities in regions.items():
        for city in cities:
            rows.append({
                "branch_id": f"B{bid:03d}",
                "branch_name": f"{city} Main",
                "city": city,
                "state": fake.state(),
                "region": region,
                "branch_manager": fake.name(),
                "opened_date": random_date(date(2005, 1, 1), date(2018, 12, 31)),
                "branch_type": random.choice(["Urban", "Urban", "Semi-Urban", "Rural"]),
            })
            bid += 1
    return pd.DataFrame(rows)


# ── 3. dim_product ───────────────────────────────────────────────
def generate_products() -> pd.DataFrame:
    print("Generating dim_product...")
    products = [
        ("P01", "Home Loan", "Loan", 8.5, 240),
        ("P02", "Personal Loan", "Loan", 12.0, 60),
        ("P03", "Auto Loan", "Loan", 9.5, 84),
        ("P04", "Education Loan", "Loan", 7.5, 180),
        ("P05", "Business Loan", "Loan", 11.0, 120),
        ("P06", "Gold Loan", "Loan", 10.0, 24),
        ("P07", "Savings Account", "Deposit", 3.5, None),
        ("P08", "Fixed Deposit", "Deposit", 6.8, 60),
        ("P09", "Recurring Deposit", "Deposit", 6.5, 36),
        ("P10", "Credit Card", "Card", 36.0, None),
        ("P11", "Debit Card", "Card", 0.0, None),
        ("P12", "Term Insurance", "Insurance", 0.0, 240),
    ]
    cols = ["product_id", "product_name", "product_category", "interest_rate", "tenure_months"]
    return pd.DataFrame(products, columns=cols)


# ── 4. dim_customer ──────────────────────────────────────────────
def generate_customers() -> pd.DataFrame:
    print(f"Generating {NUM_CUSTOMERS:,} customers...")
    rows = []
    segments = ["Retail"] * 70 + ["HNI"] * 10 + ["SME"] * 15 + ["Corporate"] * 5
    for i in range(1, NUM_CUSTOMERS + 1):
        seg = random.choice(segments)
        income_base = {"Retail": 400000, "HNI": 2000000, "SME": 1200000, "Corporate": 5000000}[seg]
        rows.append({
            "customer_id": i,
            "full_name": fake.name(),
            "age": random.randint(21, 70),
            "gender": random.choice(["M", "M", "F", "F", "Other"]),
            "city": fake.city(),
            "state": fake.state(),
            "segment": seg,
            "account_open_date": random_date(date(2015, 1, 1), END_DATE),
            "is_active": random.random() > 0.08,
            "credit_score": int(np.clip(np.random.normal(700, 80), 300, 900)),
            "annual_income": round(income_base * np.random.lognormal(0, 0.4), -3),
        })
    return pd.DataFrame(rows)


# ── 5. fact_loans ────────────────────────────────────────────────
def generate_loans(customers: pd.DataFrame, branches: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    print(f"Generating {NUM_LOANS:,} loans...")
    loan_products = products[products["product_category"] == "Loan"]
    rows = []
    for i in range(1, NUM_LOANS + 1):
        cust = customers.sample(1).iloc[0]
        branch = branches.sample(1).iloc[0]
        prod = loan_products.sample(1).iloc[0]
        amount = round(random.randint(50000, 5000000) / 10000) * 10000
        disburse_date = random_date(date(2020, 1, 1), END_DATE)
        dpd = random.choices([0, random.randint(1, 30), random.randint(31, 90), random.randint(91, 365)],
                             weights=[80, 8, 5, 7])[0]
        npa = dpd > 90
        outstanding_pct = random.uniform(0.1, 0.95) if not npa else random.uniform(0.5, 1.0)
        rows.append({
            "loan_id": f"L{i:05d}",
            "customer_id": int(cust["customer_id"]),
            "branch_id": branch["branch_id"],
            "product_id": prod["product_id"],
            "disbursement_date": disburse_date,
            "loan_amount": amount,
            "outstanding_amount": round(amount * outstanding_pct, -2),
            "emi_amount": round(amount * 0.009, -2),
            "tenure_months": int(prod["tenure_months"] or 60),
            "loan_status": "NPA" if npa else random.choice(["Active", "Active", "Active", "Closed"]),
            "dpd": dpd,
            "npa_flag": npa,
            "collateral_value": round(amount * random.uniform(1.1, 2.0), -3),
        })
    return pd.DataFrame(rows)


# ── 6. fact_transactions ─────────────────────────────────────────
def generate_transactions(customers: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    print(f"Generating {NUM_TRANSACTIONS:,} transactions...")
    channels = ["Mobile", "Mobile", "UPI", "UPI", "NetBanking", "ATM", "Branch"]
    categories = ["UPI", "IMPS", "NEFT", "RTGS", "Cash", "Cash"]
    rows = []
    for i in range(1, NUM_TRANSACTIONS + 1):
        cust = customers.sample(1).iloc[0]
        branch = branches.sample(1).iloc[0]
        txn_date = random_date(date(2023, 1, 1), END_DATE)
        amount = round(np.random.lognormal(9.5, 1.2), -2)
        fraud = random.random() < 0.005
        rows.append({
            "txn_id": f"TXN{i:07d}",
            "customer_id": int(cust["customer_id"]),
            "branch_id": branch["branch_id"],
            "txn_date": txn_date,
            "txn_type": random.choice(["Credit", "Debit", "Debit", "Transfer"]),
            "txn_amount": amount,
            "channel": random.choice(channels),
            "category": random.choice(categories),
            "fraud_flag": fraud,
            "balance_after": round(random.uniform(1000, 500000), -2),
        })
    return pd.DataFrame(rows)


# ── 7. fact_financials ───────────────────────────────────────────
def generate_financials(branches: pd.DataFrame) -> pd.DataFrame:
    print("Generating fact_financials...")
    rows = []
    rid = 1
    for _, branch in branches.iterrows():
        for year in range(2020, 2025):
            for month in range(1, 13):
                if date(year, month, 1) > END_DATE:
                    continue
                deposits = round(random.uniform(50e6, 500e6), -3)
                loans = round(deposits * random.uniform(0.6, 0.8), -3)
                interest_income = round(loans * 0.085 / 12, -3)
                interest_expense = round(deposits * 0.045 / 12, -3)
                op_expense = round(interest_income * random.uniform(0.25, 0.40), -3)
                net_profit = interest_income - interest_expense - op_expense
                npa_amount = round(loans * random.uniform(0.02, 0.08), -3)
                rows.append({
                    "record_id": rid,
                    "branch_id": branch["branch_id"],
                    "date": date(year, month, 1),
                    "total_deposits": deposits,
                    "total_loans": loans,
                    "interest_income": interest_income,
                    "interest_expense": interest_expense,
                    "operating_expense": op_expense,
                    "net_profit": net_profit,
                    "total_assets": deposits + loans * 0.1,
                    "npa_amount": npa_amount,
                })
                rid += 1
    return pd.DataFrame(rows)


# ── Main ─────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Banking Dashboard — Data Generation")
    print("=" * 50)

    dim_date = generate_dates()
    dim_branch = generate_branches()
    dim_product = generate_products()
    dim_customer = generate_customers()
    fact_loans = generate_loans(dim_customer, dim_branch, dim_product)
    fact_transactions = generate_transactions(dim_customer, dim_branch)
    fact_financials = generate_financials(dim_branch)

    # Save individual CSVs
    tables = {
        "customers": dim_customer,
        "branches": dim_branch,
        "products": dim_product,
        "loans": fact_loans,
        "transactions": fact_transactions,
        "financials": fact_financials,
    }
    for name, df in tables.items():
        path = os.path.join(OUTPUT_RAW, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"  ✅ Saved {name}.csv ({len(df):,} rows)")

    # Save master Excel
    master_path = os.path.join(OUTPUT_PROCESSED, "banking_master.xlsx")
    with pd.ExcelWriter(master_path, engine="openpyxl") as writer:
        dim_date.to_excel(writer, sheet_name="dim_date", index=False)
        dim_branch.to_excel(writer, sheet_name="dim_branch", index=False)
        dim_product.to_excel(writer, sheet_name="dim_product", index=False)
        dim_customer.to_excel(writer, sheet_name="dim_customer", index=False)
        fact_loans.to_excel(writer, sheet_name="fact_loans", index=False)
        fact_transactions.to_excel(writer, sheet_name="fact_transactions", index=False)
        fact_financials.to_excel(writer, sheet_name="fact_financials", index=False)
    print(f"  ✅ Saved banking_master.xlsx")

    print("\n🎉 Data generation complete!")
    print(f"   Raw CSVs  → {OUTPUT_RAW}")
    print(f"   Master XL → {master_path}")


if __name__ == "__main__":
    main()
