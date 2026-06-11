"""
Banking Dashboard - Data Cleaning & Validation
================================================
Reads raw CSVs, validates, cleans, and outputs processed data.
Run after data_generation.py or when using your own source data.
Run: python scripts/data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(PROCESSED, exist_ok=True)


def log(msg: str):
    print(f"  {msg}")


def validate_and_clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Customers]")
    log(f"Rows in: {len(df):,}")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["customer_id"])
    log(f"Duplicates removed: {before - len(df)}")

    # Fill nulls
    df["gender"] = df["gender"].fillna("Unknown")
    df["credit_score"] = df["credit_score"].fillna(df["credit_score"].median())

    # Clip credit score to valid range
    df["credit_score"] = df["credit_score"].clip(300, 900).astype(int)

    # Add derived columns
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 24, 35, 50, 65, 120],
        labels=["<25", "25-35", "36-50", "51-65", "65+"]
    )
    df["income_segment"] = pd.cut(
        df["annual_income"],
        bins=[0, 300000, 700000, 1500000, float("inf")],
        labels=["<3L", "3-7L", "7-15L", "15L+"]
    )

    log(f"Rows out: {len(df):,}")
    return df


def validate_and_clean_loans(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Loans]")
    log(f"Rows in: {len(df):,}")

    df = df.drop_duplicates(subset=["loan_id"])
    df["loan_amount"] = df["loan_amount"].clip(lower=0)
    df["outstanding_amount"] = df["outstanding_amount"].clip(lower=0)

    # Ensure outstanding never exceeds loan amount
    df["outstanding_amount"] = df[["outstanding_amount", "loan_amount"]].min(axis=1)

    # Derived columns
    df["loan_to_value"] = (df["loan_amount"] / df["collateral_value"].replace(0, np.nan) * 100).round(2)
    df["dpd_bucket"] = pd.cut(
        df["dpd"],
        bins=[-1, 0, 30, 60, 90, float("inf")],
        labels=["0", "1-30", "31-60", "61-90", "90+"]
    )

    log(f"NPA loans: {df['npa_flag'].sum():,} ({df['npa_flag'].mean()*100:.1f}%)")
    log(f"Rows out: {len(df):,}")
    return df


def validate_and_clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Transactions]")
    log(f"Rows in: {len(df):,}")

    df = df.drop_duplicates(subset=["txn_id"])
    df["txn_amount"] = df["txn_amount"].clip(lower=0)

    # Remove extreme outliers (> 99.9th percentile)
    upper = df["txn_amount"].quantile(0.999)
    before = len(df)
    df = df[df["txn_amount"] <= upper]
    log(f"Outliers removed: {before - len(df)}")

    # Derived column
    df["txn_value_band"] = pd.cut(
        df["txn_amount"],
        bins=[0, 10000, 50000, 100000, float("inf")],
        labels=["<10K", "10-50K", "50K-1L", "1L+"]
    )

    log(f"Fraud transactions: {df['fraud_flag'].sum():,} ({df['fraud_flag'].mean()*100:.2f}%)")
    log(f"Rows out: {len(df):,}")
    return df


def validate_and_clean_financials(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[Financials]")
    log(f"Rows in: {len(df):,}")

    df = df.drop_duplicates(subset=["record_id"])
    # Ensure no negative deposits or loans
    for col in ["total_deposits", "total_loans", "interest_income"]:
        df[col] = df[col].clip(lower=0)

    log(f"Rows out: {len(df):,}")
    return df


def main():
    print("=" * 50)
    print("  Banking Dashboard — Data Cleaning")
    print("=" * 50)

    files = {
        "customers": validate_and_clean_customers,
        "loans": validate_and_clean_loans,
        "transactions": validate_and_clean_transactions,
        "financials": validate_and_clean_financials,
    }

    cleaned = {}
    for name, cleaner in files.items():
        path = os.path.join(RAW, f"{name}.csv")
        if not os.path.exists(path):
            print(f"\n⚠️  {name}.csv not found — run data_generation.py first")
            continue
        df = pd.read_csv(path)
        cleaned[name] = cleaner(df)

    # Save cleaned master Excel
    master_path = os.path.join(PROCESSED, "banking_master_clean.xlsx")
    with pd.ExcelWriter(master_path, engine="openpyxl") as writer:
        for name, df in cleaned.items():
            df.to_excel(writer, sheet_name=name, index=False)

    print(f"\n✅ Cleaned data saved to: {master_path}")

    # Print summary
    print("\n── Summary ─────────────────────────────────")
    for name, df in cleaned.items():
        print(f"  {name:<20} {len(df):>8,} rows")


if __name__ == "__main__":
    main()
