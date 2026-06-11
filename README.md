# 🏦 Banking Dashboard — Power BI

A comprehensive **Banking Analytics Dashboard** built in Power BI that provides real-time visibility into key financial KPIs, customer metrics, loan performance, and branch-wise analytics.

![Dashboard Preview](assets/images/dashboard-preview.png)

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Overview** | Executive summary — total assets, revenue, NPA ratio, customer count |
| **Loan Analytics** | Loan disbursement trends, repayment rates, NPA breakdown |
| **Customer Insights** | Acquisition funnel, churn, segmentation by age/income |
| **Branch Performance** | Branch-wise revenue, deposits, loans, and target vs actuals |
| **Transaction Monitor** | Daily transaction volumes, fraud flags, channel-wise split |
| **Profitability** | Net interest margin, ROA, ROE, cost-to-income ratio |

---

## 🗂️ Folder Structure

```
banking-dashboard-powerbi/
│
├── 📁 data/
│   ├── raw/                    # Original source data files (CSV/Excel)
│   │   ├── customers.csv
│   │   ├── loans.csv
│   │   ├── transactions.csv
│   │   ├── branches.csv
│   │   └── financials.csv
│   └── processed/              # Cleaned/transformed data
│       └── banking_master.xlsx
│
├── 📁 reports/
│   ├── Banking_Dashboard.pbix  # Main Power BI report file
│   └── Banking_Dashboard.pdf   # Exported PDF snapshot
│
├── 📁 docs/
│   ├── data_dictionary.md      # Field definitions for all tables
│   ├── dax_measures.md         # All DAX measures documented
│   ├── data_model.md           # Star schema / relationships
│   └── setup_guide.md          # Step-by-step setup instructions
│
├── 📁 scripts/
│   ├── data_generation.py      # Python script to generate sample data
│   ├── data_cleaning.py        # Pre-processing & transformation script
│   └── power_query/
│       └── transformations.m   # Power Query M scripts
│
├── 📁 assets/
│   ├── images/                 # Dashboard screenshots
│   └── icons/                  # Custom icons used in the report
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Power BI Desktop** (latest version) — [Download here](https://powerbi.microsoft.com/desktop/)
- **Python 3.8+** (optional, for data generation)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/banking-dashboard-powerbi.git
cd banking-dashboard-powerbi

# 2. (Optional) Generate sample data
pip install -r requirements.txt
python scripts/data_generation.py

# 3. Open the Power BI report
# Open reports/Banking_Dashboard.pbix in Power BI Desktop
```

### Connecting Your Data
1. Open `Banking_Dashboard.pbix` in Power BI Desktop
2. Go to **Home → Transform Data**
3. Update the data source paths to point to your `data/raw/` or `data/processed/` files
4. Click **Close & Apply**

See [`docs/setup_guide.md`](docs/setup_guide.md) for detailed instructions.

---

## 📐 Data Model

The report follows a **Star Schema** design:

```
         ┌─────────────┐
         │  dim_date   │
         └──────┬──────┘
                │
┌──────────┐    │    ┌─────────────┐
│dim_branch├────┼────┤ fact_loans  │
└──────────┘    │    └─────────────┘
                │
┌──────────────┐│    ┌──────────────────┐
│dim_customer  ├┼────┤fact_transactions │
└──────────────┘│    └──────────────────┘
                │
         ┌──────┴──────┐
         │dim_product  │
         └─────────────┘
```

Full details → [`docs/data_model.md`](docs/data_model.md)

---

## 📏 Key DAX Measures

```dax
-- Net Interest Margin
NIM % = DIVIDE([Net Interest Income], [Average Earning Assets]) * 100

-- Non-Performing Asset Ratio
NPA Ratio % = DIVIDE([NPA Amount], [Total Loan Portfolio]) * 100

-- Customer Acquisition Cost
CAC = DIVIDE([Total Marketing Spend], [New Customers Acquired])

-- Return on Assets
ROA % = DIVIDE([Net Profit], [Average Total Assets]) * 100
```

Full DAX library → [`docs/dax_measures.md`](docs/dax_measures.md)

---

## 🎨 Design Highlights

- **Color Theme**: Navy (`#0D2137`) + Gold (`#C9A84C`) — institutional trust palette
- **Font**: Segoe UI (Power BI default, optimized for readability)
- **Visuals used**: KPI Cards, Clustered Bar, Line + Column combo, Donut, Matrix, Map, Slicers
- **Bookmarks**: Pre-built views for Executive, Risk, and Branch Manager personas

---

## 📁 Sample Data

The `data/raw/` folder contains **synthetic sample data** generated for demonstration. It includes:
- 10,000 customer records
- 5,000 loan accounts
- 50,000 transactions (12-month window)
- 25 branches across 5 regions

> ⚠️ All data is **fictitious** and generated using `scripts/data_generation.py`. No real banking data is included.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-page`
3. Commit your changes: `git commit -m 'Add fraud analytics page'`
4. Push to the branch: `git push origin feature/new-page`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [`LICENSE`](LICENSE) for details.

---

## 👤 Author

**Your Name**  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

> ⭐ If you found this useful, please consider giving the repo a star!
