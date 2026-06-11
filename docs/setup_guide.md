# ⚙️ Setup Guide

Step-by-step instructions to get the Banking Dashboard running on your machine.

---

## Prerequisites

| Tool | Version | Required? | Notes |
|------|---------|-----------|-------|
| Power BI Desktop | Latest | ✅ Yes | Free download from Microsoft |
| Python | 3.8+ | Optional | For generating/modifying sample data |
| Git | Any | Optional | For cloning the repo |

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/banking-dashboard-powerbi.git
cd banking-dashboard-powerbi
```

Or download the ZIP from GitHub → **Code → Download ZIP**

---

## Step 2 — Generate Sample Data (Optional)

If you want fresh sample data:

```bash
# Install dependencies
pip install pandas numpy faker openpyxl -r requirements.txt

# Run the data generation script
python scripts/data_generation.py
```

This creates all CSV files in `data/raw/` and the master Excel in `data/processed/`.

---

## Step 3 — Open the Power BI Report

1. Open **Power BI Desktop**
2. Go to **File → Open report**
3. Navigate to `reports/Banking_Dashboard.pbix`
4. Click **Open**

---

## Step 4 — Update Data Source Paths

When opening for the first time, Power BI may show a **data source error** because the file paths are different on your machine.

**Fix:**
1. Click **Transform Data** in the Home ribbon
2. In Power Query Editor, go to **Home → Data Source Settings**
3. For each source, click **Change Source** and update the path:
   - Point CSV files to `data/raw/` in your cloned folder
   - Point Excel to `data/processed/banking_master.xlsx`
4. Click **Close & Apply**

---

## Step 5 — Refresh the Data

After updating paths:
1. Click **Home → Refresh** to load all data
2. Wait for the refresh to complete (~10–30 seconds for sample data)
3. All visuals should now populate

---

## Step 6 — Explore the Dashboard

The report has **6 pages** — navigate using the page tabs at the bottom:

| Tab | Contents |
|-----|----------|
| `Overview` | KPI summary cards + trend lines |
| `Loan Analytics` | Loan portfolio deep dive |
| `Customer Insights` | Customer segmentation |
| `Branch Performance` | Map + branch comparison |
| `Transactions` | Channel split + fraud flags |
| `Profitability` | NIM, ROA, ROE, cost ratios |

---

## Slicers Available

Every page has consistent slicers on the left panel:
- **Date Range** — filter by any date window
- **Region** — North / South / East / West / Central
- **Branch** — individual branch filter
- **Customer Segment** — Retail / HNI / SME / Corporate
- **Product Category** — Loan / Deposit / Card / Insurance

---

## Bookmarks

Three preset bookmark views are available in the **Bookmarks pane** (View → Bookmarks):

| Bookmark | Description |
|----------|-------------|
| `Executive View` | High-level KPIs, hides detail tables |
| `Risk View` | NPA, fraud, DPD buckets highlighted |
| `Branch Manager View` | Filtered to branch-level metrics |

---

## Publishing to Power BI Service (Optional)

To publish to Power BI Online:
1. Sign in to your Power BI account in Desktop (top-right)
2. Click **Home → Publish**
3. Select your workspace
4. Open in browser: `app.powerbi.com`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Data source error" on open | Follow Step 4 above to remap paths |
| Visuals show blank | Click Refresh (Step 5) |
| Python script fails | Run `pip install pandas numpy faker openpyxl` |
| Date slicer not filtering | Ensure `dim_date` is marked as Date Table in Model view |
| Map visual not showing | Enable Map visuals: File → Options → Security → Map and Filled Map visuals |
