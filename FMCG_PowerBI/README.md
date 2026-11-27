# FMCG Sales Intelligence: Power BI version

A Power BI rebuild of the Streamlit dashboard in this repo. It uses the same star schema
(`fact_sales` + `dim_date`, `dim_product`, `dim_channel`) and answers the same four SQL questions with DAX.

| Layer | What it shows |
|---|---|
| **Power Query (M)** | One reusable `GetCsv` function, a `DataBaseUrl` parameter (GitHub URL or local folder), typed columns, derived columns, and a `dq_checks` query that rebuilds the ETL assertions plus key-integrity checks |
| **Data model** | Star schema, 3 one-to-many relationships, marked date table (`dim_date[full_date]`), hidden keys, `Month Name` sorted by month number |
| **DAX** | 14 measures in 4 display folders: core KPIs, promotion, time intelligence (`DATEADD`, `TOTALYTD`), mix and ranking (`ALLSELECTED`, `RANKX`) |
| **Report** | 4 pages: Executive Overview, Channel Performance, Promotion and Growth, Data Quality |

## Open it

1. Power BI Desktop, then File, Options and settings, Options, Preview features. Turn on
   **Power BI Project (.pbip) save option**, **Store semantic model using TMDL format** and
   **Store reports using enhanced metadata format (PBIR)**, then restart Desktop.
   (Newer versions may already have these on.)
2. Open `FMCG_Sales_Intelligence.pbip`.
3. A PBIP stores no data, so click **Refresh**. When asked how to connect to
   `raw.githubusercontent.com`, choose **Anonymous**.
4. To load local files instead: Home, Transform data, Manage parameters, set `DataBaseUrl`
   to the full path of `data\processed` in your clone (for example
   `C:\Users\you\fmcg-sales-intelligence-dashboard\data\processed`).
5. Save as `.pbix` (File, Save as) if you want a single file to share or publish.

If the project will not open, use `fallback/`: create a blank report, paste each query from
`PowerQuery_queries.m` (create `DataBaseUrl` as a text parameter first), set the relationships and
mark `dim_date` as a date table, then paste the measures from `DAX_measures.dax`.

## Check it against the SQL (expected values from the committed data)

Headline KPIs with no filters: net revenue **129,566.76**, gross margin **52,464.10**,
gross margin % **40.49%**, units **82,485**, orders **10,000**.

**Channel performance (SQL query 1)**

| Channel | Orders | Units | Net revenue | Gross margin | Margin % |
|---|---|---|---|---|---|
| Supermarket | 4,514 | 37,323 | 58,448.93 | 23,716.65 | 40.58% |
| Discounter | 2,992 | 24,804 | 39,315.26 | 15,815.13 | 40.23% |
| E-Commerce | 1,488 | 11,947 | 18,688.85 | 7,612.65 | 40.73% |
| Convenience | 1,006 | 8,411 | 13,113.72 | 5,319.67 | 40.57% |

**Month-over-month (SQL query 2)**

| Month | Net revenue | Previous month | MoM % |
|---|---|---|---|
| 2025-01 | 11,500.89 |  |  |
| 2025-02 | 9,973.28 | 11,500.89 | -13.28% |
| 2025-03 | 11,273.58 | 9,973.28 | 13.04% |
| 2025-04 | 10,062.38 | 11,273.58 | -10.74% |
| 2025-05 | 10,636.41 | 10,062.38 | 5.70% |
| 2025-06 | 10,338.79 | 10,636.41 | -2.80% |
| 2025-07 | 11,459.25 | 10,338.79 | 10.84% |
| 2025-08 | 10,939.51 | 11,459.25 | -4.54% |
| 2025-09 | 12,126.87 | 10,939.51 | 10.85% |
| 2025-10 | 10,769.56 | 12,126.87 | -11.19% |
| 2025-11 | 9,342.45 | 10,769.56 | -13.25% |
| 2025-12 | 11,143.79 | 9,342.45 | 19.28% |

**Promotional lift (SQL query 3)**

| Category | Avg units promo | Avg units base | Promo lift % |
|---|---|---|---|
| Snacks | 13.53 | 6.57 | 105.93% |
| Dairy | 13.40 | 6.53 | 105.19% |
| Beverages | 13.29 | 6.52 | 103.82% |

**Category contribution (SQL query 4)**

| Category | Net revenue | % of total | Rank |
|---|---|---|---|
| Dairy | 49,500.55 | 38.20% | 1 |
| Snacks | 46,011.26 | 35.51% | 2 |
| Beverages | 34,054.95 | 26.28% | 3 |

Data Quality page: all six checks should show PASS with 0 violations.

## Verification status

- The semantic model loads in Microsoft's TMDL parser (`Microsoft.AnalysisServices`) with no validation errors.
- The report JSON files that declare a `$schema` validate against Microsoft's published schemas.
- `tests/test_powerbi.py` checks that visuals only use fields that exist in the model, that the fallback
  files match the model, and that the headline figures below match the data.
- The project has **not yet been opened and refreshed in Power BI Desktop**, so the Power Query and DAX
  code has not been executed. Use the figures below to confirm it on first refresh.

## Notes

- Measures are explicit (implicit measures are discouraged), so always use the measure, not the raw column.
- `Revenue MoM %` is blank for January because there is no December 2024 in the data, same as `LAG()` in SQL.
- The refresh uses `Web.Contents(..., [RelativePath = ...])` so the source stays a static URL
  and can be refreshed in the Power BI service later.
