# 🗃️ Data Model

The Banking Dashboard uses a **Star Schema** — one central fact table surrounded by dimension tables.

---

## Schema Diagram

```
                        ┌───────────────────┐
                        │    dim_date        │
                        │───────────────────│
                        │ PK: date          │
                        │    day            │
                        │    month_name     │
                        │    quarter        │
                        │    year           │
                        │    fiscal_year    │
                        └─────────┬─────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
┌─────────┴──────────┐  ┌────────┴────────┐  ┌──────────┴─────────┐
│   fact_loans        │  │fact_transactions│  │  fact_financials   │
│────────────────────│  │────────────────│  │────────────────────│
│ PK: loan_id        │  │ PK: txn_id     │  │ PK: record_id      │
│ FK: customer_id    │  │ FK: customer_id│  │ FK: branch_id      │
│ FK: branch_id      │  │ FK: branch_id  │  │ FK: date           │
│ FK: product_id     │  │ FK: date       │  │    total_deposits  │
│ FK: date           │  │    txn_amount  │  │    total_loans     │
│    loan_amount     │  │    channel     │  │    interest_income │
│    npa_flag        │  │    fraud_flag  │  │    net_profit      │
└─────────┬──────────┘  └────────┬───────┘  └──────────┬─────────┘
          │                       │                       │
          └───────────┬───────────┘                       │
                      │                                   │
         ┌────────────┴──────────┐            ┌──────────┴──────────┐
         │     dim_customer      │            │     dim_branch       │
         │───────────────────────│            │─────────────────────│
         │ PK: customer_id       │            │ PK: branch_id        │
         │    full_name          │            │    branch_name       │
         │    segment            │            │    region            │
         │    credit_score       │            │    state             │
         │    annual_income      │            │    branch_type       │
         └───────────────────────┘            └─────────────────────┘

                        ┌───────────────────┐
                        │    dim_product     │
                        │───────────────────│
                        │ PK: product_id    │
                        │    product_name   │
                        │    category       │
                        │    interest_rate  │
                        └───────────────────┘
```

---

## Relationships

| From Table | From Column | To Table | To Column | Cardinality | Active |
|-----------|-------------|----------|-----------|-------------|--------|
| `fact_loans` | `customer_id` | `dim_customer` | `customer_id` | Many-to-One | ✅ Yes |
| `fact_loans` | `branch_id` | `dim_branch` | `branch_id` | Many-to-One | ✅ Yes |
| `fact_loans` | `product_id` | `dim_product` | `product_id` | Many-to-One | ✅ Yes |
| `fact_loans` | `disbursement_date` | `dim_date` | `date` | Many-to-One | ✅ Yes |
| `fact_transactions` | `customer_id` | `dim_customer` | `customer_id` | Many-to-One | ✅ Yes |
| `fact_transactions` | `branch_id` | `dim_branch` | `branch_id` | Many-to-One | ✅ Yes |
| `fact_transactions` | `txn_date` | `dim_date` | `date` | Many-to-One | ✅ Yes |
| `fact_financials` | `branch_id` | `dim_branch` | `branch_id` | Many-to-One | ✅ Yes |
| `fact_financials` | `date` | `dim_date` | `date` | Many-to-One | ✅ Yes |

---

## Design Decisions

### Why Star Schema?
- Optimized for Power BI's Vertipaq engine
- Faster query performance vs. snowflake schema
- Simpler DAX — no need for multi-hop relationships
- Easier for end users to understand

### Date Table
`dim_date` is marked as the **Official Date Table** in Power BI. This ensures:
- Time intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`, etc.) work correctly
- All fact tables connect to a single, continuous date spine

### Inactive Relationships
No inactive relationships exist in this model. All relationships are active and use the default filter direction (single direction from dimension → fact).

### Cross-Filter Direction
All relationships use **Single** cross-filter direction to avoid ambiguous filter paths and improve performance.

---

## Table Row Counts (Sample Data)

| Table | Rows | Size |
|-------|------|------|
| `dim_date` | 1,826 (5 years) | ~150 KB |
| `dim_customer` | 10,000 | ~2 MB |
| `dim_branch` | 25 | ~5 KB |
| `dim_product` | 12 | ~2 KB |
| `fact_loans` | 5,000 | ~1 MB |
| `fact_transactions` | 50,000 | ~8 MB |
| `fact_financials` | 1,500 | ~300 KB |
