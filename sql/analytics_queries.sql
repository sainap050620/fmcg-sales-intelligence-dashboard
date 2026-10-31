-- ====================================================================
-- Omnichannel Retail Commercial Analytics Queries
-- Demonstrates: Multi-table Joins, CTEs, Window Functions, and Retail KPIs
-- ====================================================================

-- 1. Channel Performance with Multi-Table Joins
SELECT 
    c.Channel,
    COUNT(f.TransactionID) AS total_orders,
    SUM(f.UnitsSold) AS total_units_sold,
    ROUND(SUM(f.NetRevenue), 2) AS net_revenue_eur,
    ROUND(SUM(f.GrossMargin), 2) AS gross_margin_eur,
    ROUND((SUM(f.GrossMargin) / NULLIF(SUM(f.NetRevenue), 0)) * 100, 2) AS margin_pct
FROM fact_sales f
JOIN dim_channel c ON f.channel_id = c.channel_id
GROUP BY c.Channel
ORDER BY net_revenue_eur DESC;

-- 2. Month-over-Month (MoM) Growth using Window Functions (LAG)
WITH monthly_sales AS (
    SELECT 
        d.year_month,
        ROUND(SUM(f.NetRevenue), 2) AS monthly_revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year_month
)
SELECT 
    year_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) 
        / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY year_month), 0)) * 100, 
        2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY year_month;

-- 3. Promotional Lift by Product Category
SELECT 
    p.Category,
    ROUND(AVG(CASE WHEN f.IsPromo = 1 THEN f.UnitsSold ELSE NULL END), 2) AS avg_units_promo,
    ROUND(AVG(CASE WHEN f.IsPromo = 0 THEN f.UnitsSold ELSE NULL END), 2) AS avg_units_base,
    ROUND(
        (AVG(CASE WHEN f.IsPromo = 1 THEN f.UnitsSold ELSE NULL END) -
         AVG(CASE WHEN f.IsPromo = 0 THEN f.UnitsSold ELSE NULL END)) /
        NULLIF(AVG(CASE WHEN f.IsPromo = 0 THEN f.UnitsSold ELSE NULL END), 0) * 100, 
        2
    ) AS promo_lift_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.Category
ORDER BY promo_lift_pct DESC;

-- 4. Category Contribution to Total Revenue (CTE + SUM() OVER() Window Function)
WITH category_totals AS (
    SELECT 
        p.Category,
        SUM(f.NetRevenue) AS category_revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.Category
)
SELECT 
    Category,
    ROUND(category_revenue, 2) AS revenue_eur,
    ROUND(
        (category_revenue / SUM(category_revenue) OVER ()) * 100, 
        2
    ) AS pct_of_total_revenue,
    DENSE_RANK() OVER (ORDER BY category_revenue DESC) AS revenue_rank
FROM category_totals
ORDER BY revenue_rank;