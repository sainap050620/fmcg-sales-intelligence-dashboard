// ===== GetCsv (function; needs parameter DataBaseUrl) =====
(fileName as text) as table =>
let
    // DataBaseUrl is a parameter: an https:// folder URL (default: the GitHub repo)
    // or a local folder path such as C:\Data\fmcg\processed
    Source =
        if Text.StartsWith(DataBaseUrl, "http") then
            Csv.Document(
                Web.Contents(DataBaseUrl, [RelativePath = fileName]),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
            )
        else
            Csv.Document(
                File.Contents(DataBaseUrl & "\" & fileName),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
            ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    Promoted

// ===== dim_date =====
let
    Source = GetCsv("dim_date.csv"),
    Typed = Table.TransformColumnTypes(
        Source,
        {
            {"full_date", type date},
            {"date_id", Int64.Type},
            {"year", Int64.Type},
            {"month", Int64.Type},
            {"year_month", type text},
            {"day_of_week", type text}
        },
        "en-US"
    ),
    AddMonthName = Table.AddColumn(
        Typed, "Month Name", each Date.ToText([full_date], "MMM", "en-US"), type text
    )
in
    AddMonthName

// ===== dim_product =====
let
    Source = GetCsv("dim_product.csv"),
    Typed = Table.TransformColumnTypes(
        Source, {{"Category", type text}, {"product_id", Int64.Type}}, "en-US"
    )
in
    Typed

// ===== dim_channel =====
let
    Source = GetCsv("dim_channel.csv"),
    Typed = Table.TransformColumnTypes(
        Source, {{"Channel", type text}, {"channel_id", Int64.Type}}, "en-US"
    )
in
    Typed

// ===== fact_sales =====
let
    Source = GetCsv("fact_sales.csv"),
    Typed = Table.TransformColumnTypes(
        Source,
        {
            {"TransactionID", type text},
            {"date_id", Int64.Type},
            {"product_id", Int64.Type},
            {"channel_id", Int64.Type},
            {"UnitsSold", Int64.Type},
            {"NetRevenue", type number},
            {"GrossMargin", type number},
            {"MarginPct", type number},
            {"IsPromo", Int64.Type}
        },
        "en-US"
    ),
    AddPromoLabel = Table.AddColumn(
        Typed, "Promo Label", each if [IsPromo] = 1 then "Promo" else "Base", type text
    )
in
    AddPromoLabel

// ===== dq_checks =====
let
    // Mirrors the assertions in src/etl_pipeline.py, plus key-integrity checks.
    // Violations are reported instead of stopping the refresh, so the report can show them.
    Checks = #table(
        type table [Check = text, Rule = text, Violations = Int64.Type],
        {
            {"Units sold is positive", "UnitsSold > 0",
                Table.RowCount(Table.SelectRows(fact_sales, each [UnitsSold] <= 0))},
            {"Net revenue is not negative", "NetRevenue >= 0",
                Table.RowCount(Table.SelectRows(fact_sales, each [NetRevenue] < 0))},
            {"Transaction ID is unique", "No duplicate TransactionID",
                Table.RowCount(fact_sales) - List.Count(List.Distinct(fact_sales[TransactionID]))},
            {"Date keys resolve", "fact.date_id exists in dim_date",
                List.Count(List.Difference(List.Distinct(fact_sales[date_id]), dim_date[date_id]))},
            {"Product keys resolve", "fact.product_id exists in dim_product",
                List.Count(List.Difference(List.Distinct(fact_sales[product_id]), dim_product[product_id]))},
            {"Channel keys resolve", "fact.channel_id exists in dim_channel",
                List.Count(List.Difference(List.Distinct(fact_sales[channel_id]), dim_channel[channel_id]))}
        }
    ),
    WithStatus = Table.AddColumn(
        Checks, "Status", each if [Violations] = 0 then "PASS" else "FAIL", type text
    )
in
    WithStatus

