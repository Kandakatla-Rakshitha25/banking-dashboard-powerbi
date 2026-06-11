// ============================================================
// Banking Dashboard — Power Query M Transformations
// Copy each section into the corresponding query in Power BI
// Home → Transform Data → Advanced Editor
// ============================================================


// ── dim_date (Generate in Power Query — no CSV needed) ────────
let
    StartDate = #date(2020, 1, 1),
    EndDate = #date(2024, 12, 31),
    Duration = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, Duration, #duration(1, 0, 0, 0)),
    Source = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),

    // Type cast
    #"Changed Type" = Table.TransformColumnTypes(Source, {{"Date", type date}}),

    // Add columns
    #"Day" = Table.AddColumn(#"Changed Type", "Day", each Date.Day([Date]), Int64.Type),
    #"Month" = Table.AddColumn(#"Day", "Month", each Date.Month([Date]), Int64.Type),
    #"MonthName" = Table.AddColumn(#"Month", "Month Name", each Date.ToText([Date], "MMMM"), type text),
    #"Quarter" = Table.AddColumn(#"MonthName", "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    #"Year" = Table.AddColumn(#"Quarter", "Year", each Date.Year([Date]), Int64.Type),
    #"WeekNo" = Table.AddColumn(#"Year", "Week Number", each Date.WeekOfYear([Date]), Int64.Type),
    #"IsWeekday" = Table.AddColumn(#"WeekNo", "Is Weekday",
        each Date.DayOfWeek([Date], Day.Monday) < 5, type logical),
    #"FiscalYear" = Table.AddColumn(#"IsWeekday", "Fiscal Year",
        each if Date.Month([Date]) >= 4
             then "FY" & Text.From(Date.Year([Date]) + 1)
             else "FY" & Text.From(Date.Year([Date])), type text),
    #"FiscalQtr" = Table.AddColumn(#"FiscalYear", "Fiscal Quarter",
        each let m = Date.Month([Date]),
                 fq = if m >= 4 and m <= 6 then "Q1"
                      else if m >= 7 and m <= 9 then "Q2"
                      else if m >= 10 and m <= 12 then "Q3"
                      else "Q4"
             in fq & " " & [Fiscal Year], type text)
in
    #"FiscalQtr"


// ── customers.csv ─────────────────────────────────────────────
let
    Source = Csv.Document(
        File.Contents("<YOUR_PATH>\data\raw\customers.csv"),
        [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"customer_id", Int64.Type},
        {"age", Int64.Type},
        {"credit_score", Int64.Type},
        {"annual_income", type number},
        {"is_active", type logical},
        {"account_open_date", type date}
    }),
    #"Added Age Group" = Table.AddColumn(#"Changed Types", "Age Group",
        each if [age] < 25 then "<25"
             else if [age] <= 35 then "25-35"
             else if [age] <= 50 then "36-50"
             else if [age] <= 65 then "51-65"
             else "65+", type text),
    #"Added Income Segment" = Table.AddColumn(#"Added Age Group", "Income Segment",
        each if [annual_income] < 300000 then "<3L"
             else if [annual_income] < 700000 then "3-7L"
             else if [annual_income] < 1500000 then "7-15L"
             else "15L+", type text)
in
    #"Added Income Segment"


// ── loans.csv ─────────────────────────────────────────────────
let
    Source = Csv.Document(
        File.Contents("<YOUR_PATH>\data\raw\loans.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"loan_amount", type number},
        {"outstanding_amount", type number},
        {"emi_amount", type number},
        {"tenure_months", Int64.Type},
        {"dpd", Int64.Type},
        {"npa_flag", type logical},
        {"collateral_value", type number},
        {"disbursement_date", type date}
    }),
    #"Added DPD Bucket" = Table.AddColumn(#"Changed Types", "DPD Bucket",
        each if [dpd] = 0 then "0"
             else if [dpd] <= 30 then "1-30"
             else if [dpd] <= 60 then "31-60"
             else if [dpd] <= 90 then "61-90"
             else "90+", type text),
    #"Added LTV" = Table.AddColumn(#"Added DPD Bucket", "LTV %",
        each if [collateral_value] = 0 then null
             else Number.Round([loan_amount] / [collateral_value] * 100, 2),
             type number)
in
    #"Added LTV"


// ── transactions.csv ──────────────────────────────────────────
let
    Source = Csv.Document(
        File.Contents("<YOUR_PATH>\data\raw\transactions.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers", {
        {"txn_amount", type number},
        {"balance_after", type number},
        {"fraud_flag", type logical},
        {"txn_date", type date}
    }),
    #"Added Value Band" = Table.AddColumn(#"Changed Types", "Txn Value Band",
        each if [txn_amount] < 10000 then "<10K"
             else if [txn_amount] < 50000 then "10-50K"
             else if [txn_amount] < 100000 then "50K-1L"
             else "1L+", type text),
    #"Added Is Digital" = Table.AddColumn(#"Added Value Band", "Is Digital",
        each List.Contains({"Mobile", "NetBanking", "UPI"}, [channel]), type logical)
in
    #"Added Is Digital"
